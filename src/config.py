import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# App Configuration
PAGE_TITLE = "MediGuide AI"
PAGE_ICON = "🩺"

# Form Options
GENDER_OPTIONS = ["Select", "Male", "Female", "Non-binary", "Prefer not to say"]
DURATION_OPTIONS = [
    "Select",
    "Less than 1 day",
    "1-3 days",
    "4-7 days",
    "1-2 weeks",
    "More than 2 weeks",
    "Over a month"
]

LANGUAGE_OPTIONS = [
    "English",
    "Spanish",
    "French",
    "German",
    "Urdu",
    "Hindi",
    "Arabic",
    "Chinese",
    "Japanese"
]

SYMPTOM_SUGGESTIONS = [
    "Fever", "Cough", "Sore throat", "Runny nose", "Headache",
    "Nausea", "Vomiting", "Diarrhea", "Fatigue", "Shortness of breath",
    "Chest pain", "Dizziness", "Muscle aches", "Joint pain", "Rash"
]

# Model Options
MODEL_OPTIONS = ["gpt-4.1-nano", "gpt-4o-mini", "gpt-4o"]
DEFAULT_MODEL = "gpt-4.1-nano"
