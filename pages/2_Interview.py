import streamlit as st
import time
from utils.state import init_session_state
from utils.ui import hide_sidebar_and_render_navbar
from utils.llm_engine import InterviewEngine
from streamlit_ace import st_ace
import sys
from io import StringIO
import streamlit.components.v1 as components
from audio_recorder_streamlit import audio_recorder

st.set_page_config(page_title="Mock Interview", layout="wide", page_icon="📝")
hide_sidebar_and_render_navbar()
init_session_state()

# Initialize Engine
if "engine" not in st.session_state:
    st.session_state.engine = InterviewEngine()

def start_interview():
    with st.spinner("Generating personalized questions..."):
        questions = st.session_state.engine.generate_questions(st.session_state.user_data)
        if questions:
            st.session_state.questions = questions
            st.session_state.interview_started = True
            st.session_state.current_question_index = 0
            st.session_state.answers = []
            st.rerun()
        else:
            st.error("Failed to generate questions. Please check your API key / configuration.")

if not st.session_state.onboarded:
    st.title("Interview Session")
    st.warning("Please complete onboarding first!")
    if st.button("Go to Onboarding"):
        st.switch_page("pages/1_Onboarding.py")
    st.stop()

if not st.session_state.interview_started:
    st.title("Ready for your interview?")
    st.write(f"This session will consist of 10 questions and should take about 30 minutes.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        **Parameters:**
        - Target Role: {st.session_state.user_data['target_role']}
        - Experience Level: {st.session_state.user_data['experience_level']}
        - Target Company: {st.session_state.user_data['target_company']}
        - Skills Keyword: {st.session_state.user_data['skills_keywords']}
        """)
    
    if st.button("Start Interview"):
        start_interview()
else:
    # Interview session in progress
    idx = st.session_state.current_question_index
    total = len(st.session_state.questions)
    
    if idx < total:
        q = st.session_state.questions[idx]
        
        st.progress((idx) / total)
        st.subheader(f"Question {idx + 1} of {total} ({q.get('type', 'Unknown').capitalize()})")
        
        # Humanizer Logic
        interaction_text = q.get("question", "")
        if q.get('type') != 'coding' and len(st.session_state.answers) > 0:
            last_ans = st.session_state.answers[-1]
            with st.spinner("Interviewer is thinking..."):
                humanized = st.session_state.engine.humanize_and_score(q, last_ans, st.session_state.answers)
                interaction_text = humanized.get("next_interaction", q.get("question", ""))
        
        st.markdown(f'<h3>{interaction_text}</h3>', unsafe_allow_html=True)
        
        # Interviewer TTS (Autoplay once per question)
        tts_played_key = f"tts_played_{idx}"
        audio_cache_key = f"tts_audio_cache_{idx}"
        
        if tts_played_key not in st.session_state:
            st.session_state[tts_played_key] = False
            
        if audio_cache_key not in st.session_state:
            with st.spinner("Interviewer is speaking..."):
                st.session_state[audio_cache_key] = st.session_state.engine.generate_tts_audio(interaction_text)
                
        autoplay_audio = not st.session_state[tts_played_key]
        
        if st.session_state.get(audio_cache_key):
            st.audio(st.session_state[audio_cache_key], format="audio/mp3", autoplay=autoplay_audio)
            if autoplay_audio:
                st.session_state[tts_played_key] = True
        else:
            st.error("Failed to generate audio.")
        

        # Handle different question types
        if q.get('type') == 'coding':
            st.info("Coding Lab: Write your solution below in Python. You can Run and Test it before submitting.")
            user_answer = st_ace(
                placeholder="def solution():\n    pass",
                language="python",
                theme="monokai",
                keybinding="vscode",
                font_size=14,
                tab_size=4,
                show_gutter=True,
                show_print_margin=False,
                wrap=True,
                auto_update=True,
                min_lines=15,
                key=f"ace_{idx}"
            )
            
            if st.button("▶ Run & Test Code"):
                st.write("### Execution Output:")
                old_stdout = sys.stdout
                sys.stdout = mystdout = StringIO()
                try:
                    exec(user_answer, {})
                    val = mystdout.getvalue()
                    if val:
                        st.success(val)
                    else:
                        st.success("NO code executed.")
                except Exception as e:
                    st.error(f"Error: {e}")
                finally:
                    sys.stdout = old_stdout
            
        else:
            text_key = f"q_text_{idx}"
            if text_key not in st.session_state:
                st.session_state[text_key] = ""
                
            st.write("**Answer via Text or Voice:**")
            
            col_text, col_mic = st.columns([11, 1])
            
            with col_mic:
                st.write("") # small vertical nudge
                st.write("")
                # Audio Recorder (WhatsApp Style layout)
                audio_bytes = audio_recorder(
                    text="", 
                    recording_color="#ff4b4b",
                    neutral_color="#6b6b6b",
                    icon_name="microphone",
                    icon_size="2x",
                    key=f"audio_recorder_{idx}"
                )
            
            if audio_bytes and st.session_state.get(f"last_audio_{idx}") != audio_bytes:
                st.session_state[f"last_audio_{idx}"] = audio_bytes
                with st.spinner("Transcribing your answer via Whisper..."):
                    transcript = st.session_state.engine.transcribe_audio(audio_bytes)
                    if transcript and not transcript.startswith("Error"):
                        st.session_state[text_key] = (st.session_state[text_key] + " " + transcript).strip()
                    else:
                        st.error(transcript)
                        
            with col_text:
                user_answer = st.text_area("Your Answer", height=100, key=text_key, label_visibility="collapsed", placeholder="Type your response here or dictate via the microphone...")

        
        col_btn1, col_btn2 = st.columns([5, 1])
        with col_btn2:
            submit_clicked = st.button("Submit Answer", key=f"submit_{idx}")
            
        if submit_clicked:
            if user_answer and user_answer.strip():
                st.session_state.answers.append(user_answer)
                st.session_state.current_question_index += 1
                # Progress to next
                if st.session_state.current_question_index >= total:
                    st.session_state.interview_complete = True
                st.rerun()
            else:
                st.error("Please provide an answer before moving on.")
                
        # JS script to intercept Enter key on text_area specifically for normal questions
        if q.get('type') != 'coding':
            js_code = """
            <script>
            setTimeout(function() {
                const doc = window.parent.document;
                const textareas = doc.querySelectorAll('textarea');
                textareas.forEach(ta => {
                    if (ta.dataset.enterBound === 'true') return;
                    ta.dataset.enterBound = 'true';
                    ta.addEventListener('keydown', function(event) {
                        if (event.key === 'Enter' && !event.shiftKey) {
                            event.preventDefault();
                            if (this.value.trim() !== '') {
                                this.blur(); 
                                const buttons = Array.from(doc.querySelectorAll('button'));
                                const submitBtn = buttons.find(b => b.innerText.includes('Submit Answer'));
                                if (submitBtn) {
                                    setTimeout(() => submitBtn.click(), 50);
                                }
                            } else {
                                alert('Please provide an answer before moving on.');
                            }
                        }
                    });
                });
            }, 1500);
            </script>
            """
            components.html(js_code, height=0, width=0)
    else:
        st.success("Interview Complete! Click below to see your feedback.")
        if st.button("Analyze & View Feedback"):
            st.switch_page("pages/3_Feedback.py")
