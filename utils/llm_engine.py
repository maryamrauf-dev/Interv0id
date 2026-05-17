from groq import Groq
import json
import streamlit as st
import os
import time
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load .env file
load_dotenv()

# Set up the API Key 
def get_api_key():
    # 1. Check environment variables
    api_key = os.getenv("GROQ_API_KEY") 
    if api_key:
        logger.info("Using API key from environment variables.")
        return api_key
    
    logger.warning("No Groq API key found in env.")
    return None

class InterviewEngine:
    def __init__(self, model_name=None): 
        self.model_name = model_name or os.getenv("GROQ_MODEL_NAME", "llama3-8b-8192")
        self.api_key = get_api_key()
        self._cache = {}
        if self.api_key:
            try:
                self.client = Groq(api_key=self.api_key)
                logger.info(f"Groq Client initialized successfully using {model_name}.")
            except Exception as e:
                self.client = None
                logger.error(f"Failed to initialize Groq client: {e}")
        else:
            self.client = None
            logger.error("Groq configuration failed due to missing API key.")

    def _get_cache_key(self, prefix, **kwargs):
        key_parts = [prefix]
        for k, v in sorted(kwargs.items()):
            # Handle non-string types safely
            key_parts.append(f"{k}:{str(v)[:200]}") # limit length of value in key
        return "|".join(key_parts)

    def _call_groq_api_with_retry(self, prompt, temperature=0.7, max_retries=3):
        if not self.client:
            raise Exception("Groq client not initialized")
            
        last_error = None
        models_to_try = [self.model_name, "llama3-8b-8192", "mixtral-8x7b-32768", "gemma2-9b-it"]
        
        for attempt in range(max_retries):
            current_model = models_to_try[attempt % len(models_to_try)]
            try:
                response = self.client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model=current_model,
                    temperature=temperature,
                    response_format={"type": "json_object"}
                )
                text = response.choices[0].message.content.strip()
                
                return json.loads(text)
            except Exception as e:
                last_error = e
                logger.warning(f"Groq API call failed with model {current_model} (attempt {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff: 1s, 2s
                    
        raise last_error

    def generate_questions(self, user_data):
        """LLM 1: Question Generator"""
        prompt = f"""
        You are an expert Interview Question Generator.
        Generate 10 interview questions for a candidate with the following profile:
        - Name: {user_data['name']}
        - Target Role: {user_data['target_role']}
        - Experience Level: {user_data['experience_level']}
        - Target Company: {user_data['target_company'] if user_data['target_company'] else 'Any'}
        - Skills Keywords: {user_data['skills_keywords']}
        - Resume/Background: {user_data['resume_text'] if user_data['resume_text'] else 'None provided'}
    
        CRITICAL REQUIREMENT: Focus ONLY on the provided "Skills Keywords". All technical and coding questions MUST be directly related to the skills entered by the candidate. Tailor the behavioral/culture-fit questions based on their resume if provided.

        The questions must include:
        - 3 Behavioral/Culture-fit questions customized to the candidate's resume/profile
        - 4 Technical questions specifically testing the "Skills Keywords" at the "{user_data['experience_level']}" level
        - 3 Coding or Scenario-based logic questions specifically testing the "Skills Keywords" at the "{user_data['experience_level']}" level

        Output EXACTLY a JSON object with a single key "questions" containing a list of objects with these keys: 
        "type" (behavioral, technical, coding), "question", "category".
        Do not output any text other than the JSON object.
        
        Example structure:
        {{
            "questions": [
                {{"type": "behavioral", "question": "...", "category": "..."}},
                {{"type": "technical", "question": "...", "category": "..."}}
            ]
        }}
        """
        
        cache_key = self._get_cache_key("gen_q", **user_data)
        if cache_key in self._cache:
            logger.info("Using cached questions.")
            return self._cache[cache_key]

        if not self.client:
            st.error("Groq API Key not found. Please set it in your Profile.")
            return []

        try:
            logger.info(f"Attempting to generate questions with primary model: {self.model_name}")
            data = self._call_groq_api_with_retry(prompt, temperature=0.7)
            
            # Schema Validation
            questions = data.get("questions", data)
            if not isinstance(questions, list):
                raise ValueError("Expected 'questions' to be a list")
                
            valid_questions = []
            for q in questions:
                if isinstance(q, dict) and "type" in q and "question" in q:
                    valid_questions.append(q)
            
            if not valid_questions:
                raise ValueError("No valid questions found in response")
                
            logger.info(f"Successfully generated questions.")
            self._cache[cache_key] = valid_questions
            return valid_questions
        except Exception as e:
            logger.error(f"Error in generate_questions: {e}")
            st.error(f"API Error: {e}")
            return []

    def humanize_and_score(self, question_obj, last_answer, history):
        """LLM 2: Humanizer & Short-term Evaluator"""
        prompt = f"""
        You are a friendly but professional interviewer. 
        Current Question Objective: {question_obj['question']}
        Candidate's Last Answer: "{last_answer}"
        
        Task:
        1. Score the last answer (1-10).
        2. If score > 5, ask a brief follow-up question based on the answer.
        3. If score <= 5, give a small encouraging remark and move to the current question objective.
        
        Rules:
        - Be conversational.
        - Short response.
        
        Output EXACTLY a JSON object. No text before or after JSON.
        {{
            "score": 8,
            "feedback": "string",
            "next_interaction": "string"
        }}
        """
        
        cache_key = self._get_cache_key("score", q=question_obj.get('question', ''), ans=last_answer)
        if cache_key in self._cache:
            logger.info("Using cached humanize_and_score result.")
            return self._cache[cache_key]

        if not self.client:
            return {"score": 5, "feedback": "API key missing.", "next_interaction": question_obj['question']}

        try:
            data = self._call_groq_api_with_retry(prompt, temperature=0.5)
            
            # Schema Validation
            if not isinstance(data, dict):
                raise ValueError("Expected a dictionary response")
            
            score = data.get("score", 5)
            if not isinstance(score, (int, float)):
                data["score"] = 5
                
            data["feedback"] = str(data.get("feedback", ""))
            data["next_interaction"] = str(data.get("next_interaction", question_obj.get("question", "")))

            self._cache[cache_key] = data
            return data
        except Exception as e:
            logger.error(f"Error in humanize_and_score: {e}")
            return {"score": 5, "feedback": "Good progress.", "next_interaction": question_obj['question']}

    def evaluate_interview(self, user_data, questions, answers):
        """LLM 3: Deep Insights Evaluator"""
        interview_summary = ""
        for q, a in zip(questions, answers):
            interview_summary += f"Q: {q['question']}\nA: {a}\n\n"
        
        prompt = f"""
        Analyze this interview for {user_data['name']} (Target Role: {user_data['target_role']}).
        Interview Transcript:
        {interview_summary}
        
        CRITICAL EVALUATION RULES:
        1. If the candidate's answers are gibberish, just random characters (e.g. "asdfasdf", "jkl;"), extremely short, or completely avoid answering the questions, you MUST heavily penalize the score (give 0, 1, or 2 out of 10).
        2. DO NOT hallucinate or make up "strengths" if the answers do not demonstrate any. You can leave the strengths array empty or just state "No visible strengths due to vague/invalid responses" in the feedback.
        3. Be brutally honest and accurate. Evaluate the actual content of their answers. If they did not provide valid code or clear explanations, reflect that harshly in the feedback.
        
        Provide deep insights following the rules above:
        1. Overall score (0-10)
        2. Strengths (List of strings)
        3. Areas of Improvement (List of strings)
        4. Detailed Review for each category (Technical, Behavioral, Coding)
        
        Output EXACTLY this structured JSON object. Do not output anything outside of the JSON block:
        {{
            "score": 8,
            "strengths": ["string1", "string2"],
            "areas_of_improvement": ["string1", "string2"],
            "category_feedback": {{
                "Technical": "feedback string",
                "Behavioral": "feedback string",
                "Coding": "feedback string"
            }}
        }}
        """
        
        q_str = "[SEP]".join([q.get('question', '') for q in questions])
        a_str = "[SEP]".join(answers)
        cache_key = self._get_cache_key("eval", user=user_data.get('name', ''), q=q_str, a=a_str)
        if cache_key in self._cache:
            logger.info("Using cached interview evaluation.")
            return self._cache[cache_key]

        if not self.client:
            return {"score": 0, "error": "Evaluation failed: Missing API Key"}

        try:
            data = self._call_groq_api_with_retry(prompt, temperature=0.7)
            
            # Schema Validation
            if not isinstance(data, dict):
                raise ValueError("Expected a dictionary response")
                
            score = data.get("score", 0)
            if not isinstance(score, (int, float)):
                data["score"] = 0
                
            if not isinstance(data.get("strengths"), list):
                data["strengths"] = []
                
            if not isinstance(data.get("areas_of_improvement"), list):
                data["areas_of_improvement"] = []
                
            if not isinstance(data.get("category_feedback"), dict):
                data["category_feedback"] = {
                    "Technical": "No feedback provided",
                    "Behavioral": "No feedback provided",
                    "Coding": "No feedback provided"
                }

            self._cache[cache_key] = data
            return data
        except Exception as e:
            logger.error(f"Error in evaluate_interview: {e}")
            return {"score": 0, "error": f"Evaluation failed: {e}"}

    def transcribe_audio(self, audio_bytes):
        """Transcribe audio using Groq Whisper model."""
        if not self.client:
            return "Error: API key missing."
        
        try:
            response = self.client.audio.transcriptions.create(
              file=("audio.wav", audio_bytes),
              model="whisper-large-v3",
            )
            return response.text
        except Exception as e:
            logger.error(f"Error in transcribe_audio: {e}")
            return f"Error: {e}"

    def generate_tts_audio(self, text):
        """Generate TTS audio using gTTS and return as bytes."""
        try:
            from gtts import gTTS
            from io import BytesIO
            tts = gTTS(text=text, lang='en', slow=False)
            fp = BytesIO()
            tts.write_to_fp(fp)
            return fp.getvalue()
        except Exception as e:
            logger.error(f"Error in generate_tts_audio: {e}")
            return None

@st.cache_resource
def get_engine():
    """
    Returns a globally cached singleton of InterviewEngine.
    This prevents the engine (and Groq client) from being reinitialized or duplicated across sessions,
    and isolates it from the user's `st.session_state` to prevent cross-session leaks.
    """
    return InterviewEngine()
