from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder
)
from langchain_core.messages import SystemMessage

# Define the JSON schema structure required by the application
JSON_SCHEMA = """
{
  "summary": "Brief symptom summary",
  "possible_conditions": [ { "name": "Condition Name", "reason": "Why this matches" } ],
  "urgency_level": "LOW or MEDIUM or HIGH or EMERGENCY",
  "recommended_next_steps": ["Step 1", "Step 2"],
  "questions_for_doctor": ["Question 1", "Question 2"],
  "warning_signs": ["Sign 1", "Sign 2"]
}
"""

SYSTEM_PROMPT = f"""You are MediGuide AI, an educational AI-powered medical symptom assessment and patient guidance assistant.

IMPORTANT SAFETY RULES:
1. You are an AI, NOT a doctor.
2. NEVER present a confirmed medical diagnosis. Provide "possible_conditions" for educational purposes only.
3. If symptoms suggest a critical issue (e.g., severe chest pain, shortness of breath, severe bleeding, stroke symptoms), you MUST classify the urgency_level as "EMERGENCY" and urge the user to seek immediate emergency medical help.
4. Always maintain a calm, objective, and supportive tone.
5. Your output must be strictly valid JSON matching the exact schema below.

JSON SCHEMA:
{JSON_SCHEMA}

Return ONLY the raw JSON object. Do NOT wrap it in Markdown code blocks (e.g., ```json) and do not include any other text before or after the JSON.
"""

# Reusable single-string template (for raw generation if needed)
# However, we primarily use ChatPromptTemplate for chat models
raw_patient_template = """
Please assess the following patient information and symptoms, and provide guidance in {language}:

Patient Profile:
- Age: {age}
- Gender: {gender}
- Existing Conditions: {conditions}
- Current Medications: {medications}

Symptom Details:
- Symptoms: {symptoms}
- Duration: {duration}
- Severity (1-10): {severity}
- Additional Notes: {notes}
"""

# Create the ChatPromptTemplate containing system prompt, history, and user input
NARRATIVE_CHAT_TEMPLATE = ChatPromptTemplate.from_messages([
    SystemMessage(content=SYSTEM_PROMPT),
    MessagesPlaceholder(variable_name="chat_history"),
    HumanMessagePromptTemplate.from_template(raw_patient_template)
])
