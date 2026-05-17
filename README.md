#  Interv0id

A premium, AI-powered interview preparation platform designed to help candidates master their interview skills. Built with **Streamlit** and powered by **Groq LPU Inference Engine (Llama 3)**, this application provides a personalized, interactive, and analytical approach to interview coaching with ultra-fast responses and a free tier.

---

##  Key Features

- **Personalized Onboarding**: Tailors interviews based on your domain, experience level, and target company.
- **3-Module AI Architecture**:
  - **Question Generation**: Dynamic creation of technical, behavioral, and coding questions specific to your profile.
  - **Conversational Interviewer**: Real-time human-like interaction with follow-up questions and adaptive responses.
  - **Deep Evaluation**: Comprehensive performance analysis with scoring, strengths, and areas for improvement.
- **Interactive Coding Lab**: Real-time coding environment to test your logic and syntax during technical rounds.
- **Real-Time Voice Features**:
  - **Dictate Answers**: Speak your answers directly into the browser using robust Whisper-powered Speech-to-Text transcription.
  - **AI Voice Interviewer**: Listen to questions spoken aloud by the AI utilizing integrated Text-to-Speech technology.
- **Performance Analytics**: Track your progress over time with visual dashboards and historical data.

---

##  Technology Stack

- **Framework**: [Streamlit](https://streamlit.io/)
- **AI Engine**: [Groq API](https://groq.com/) using Llama 3.1 8B Instant model
- **Styling**: Custom CSS
- **Language**: Python 3.9+
- **Environment Management**: Python-dotenv

---

##  Getting Started

### Prerequisites

- Python 3.9 or higher
- A Groq API Key ([Get it here](https://console.groq.com/keys))

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Farahafifii/AI_Interview_StreamLit.git
   cd AI_Interview_StreamLit
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   Create a `.env` file in the root directory and add your API key:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

### Running the Application

```bash
streamlit run Home.py
```

---

##  Project Structure

```text
AI_Interview_StreamLit/
├── Home.py              # Main entry point and landing page
├── pages/               # Multi-page application structure
│   ├── 1_Onboarding.py  # User profile and data setup
│   ├── 2_Interview.py   # Interactive AI interview session
│   ├── 3_Feedback.py    # Detailed performance analysis
│   ├── 4_Analytics.py   # Performance tracking dashboard
│   └── 5_Profile.py     # User settings 
├── utils/               # Shared utilities
│   ├── llm_engine.py    # Groq API logic and prompt engineering
│   ├── state.py         # Session state management
│   ├── db.py            # Supabase database integration
│   ├── sandbox.py       # Secure code execution environment
│   └── ui.py            # Global CSS and UI components
├── .env                 # Environment variables (API Keys)
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```

---

##  Contributing

This project was developed as part of an advanced AI development initiative. Contributions, issues, and feature requests are welcome!

##  License

Distributed under the MIT License. See `LICENSE` for more information .

---
*Developed with ❤️ by MARYAM RAUF for Future Leaders.*
