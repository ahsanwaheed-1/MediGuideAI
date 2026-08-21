# MediGuide AI

"AI-Powered Medical Symptom Assessment and Patient Guidance Assistant"

**IMPORTANT MEDICAL & SAFETY NOTICE**
> The application built in this assignment is an educational AI prototype only. It is NOT a replacement for a licensed doctor, professional diagnosis, emergency service, or medical treatment. It must never present a confirmed diagnosis. Every screen must direct users to consult a qualified healthcare professional and to seek emergency help in urgent situations.

## Setup Instructions

1. Ensure you have Python 3.10+ installed.
2. Clone this repository and navigate to the project directory.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and add your OpenAI API Key.
   ```bash
   cp .env.example .env
   # Edit .env and set OPENAI_API_KEY=sk-...
   ```
5. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```

## Caching Explanation

This application demonstrates two types of caching provided by LangChain to reduce latency and API costs for identical requests:

- **InMemoryCache**: Stored in RAM. It is the fastest caching method but does not survive application restarts. Best for caching requests within a single run session.
- **SQLiteCache**: Stored in a file on disk (`.langchain.db`). It is slightly slower than InMemoryCache but persists across application restarts. Best for reusing cached responses across multiple sessions.

You can toggle between these caching methods using the sidebar in the application.

## Bonus Features Included
- Conversation / Patient Session History
- Multiple language support
- Dark / Light mode toggle
