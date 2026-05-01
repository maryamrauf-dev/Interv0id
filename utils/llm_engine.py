from groq import Groq
import json
import streamlit as st
import os
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
    def __init__(self, model_name="llama-3.1-8b-instant"): 
        self.model_name = model_name
        self.api_key = get_api_key()
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
        
        if not self.client:
            st.error("Groq API Key not found. Please set it in your Profile.")
            return []

        try:
            logger.info(f"Attempting to generate questions using model: {self.model_name}")
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model_name,
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            text = response.choices[0].message.content.strip()
            
            # Extract JSON
            if "```json" in text:
                text = text.split("```json")[-1].split("```")[0].strip()
            elif "```" in text:
                text = text.split("```")[-1].split("```")[0].strip()
            
            data = json.loads(text)
            logger.info(f"Successfully generated {len(data.get('questions', []))} questions.")
            return data.get("questions", data) # Fallback to `data` if they output a list anyway
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
        
        if not self.client:
            return {"score": 5, "feedback": "API key missing.", "next_interaction": question_obj['question']}

        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model_name,
                temperature=0.5,
                response_format={"type": "json_object"}
            )
            text = response.choices[0].message.content.strip()

            if "```json" in text:
                text = text.split("```json")[-1].split("```")[0].strip()
            elif "```" in text:
                text = text.split("```")[-1].split("```")[0].strip()
            return json.loads(text)
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
        
        if not self.client:
            return {"score": 0, "error": "Evaluation failed: Missing API Key"}

        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model_name,
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            text = response.choices[0].message.content.strip()

            if "```json" in text:
                text = text.split("```json")[-1].split("```")[0].strip()
            elif "```" in text:
                text = text.split("```")[-1].split("```")[0].strip()
            return json.loads(text)
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
