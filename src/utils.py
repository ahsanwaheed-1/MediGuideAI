import json
import re

def parse_json(response_text: str) -> dict:
    """
    Safely parses JSON from the LLM response text.
    Handles potential markdown fences (e.g. ```json ... ```)
    and falls back gracefully on failure.
    """
    # Strip markdown formatting if present
    cleaned_text = response_text.strip()
    if cleaned_text.startswith("```"):
        # Use regex to remove first line like ```json and last line like ```
        cleaned_text = re.sub(r"^```(?:json)?\s*", "", cleaned_text, flags=re.MULTILINE)
        cleaned_text = re.sub(r"\s*```$", "", cleaned_text, flags=re.MULTILINE)
    
    cleaned_text = cleaned_text.strip()
    
    try:
        data = json.loads(cleaned_text)
        return data
    except json.JSONDecodeError as e:
        # Return a fallback dict if parsing fails to avoid crashing
        return {
            "summary": "Error parsing response.",
            "possible_conditions": [],
            "urgency_level": "UNKNOWN",
            "recommended_next_steps": ["Please try submitting again."],
            "questions_for_doctor": [],
            "warning_signs": [],
            "_raw_error": str(e),
            "_raw_content": response_text
        }
