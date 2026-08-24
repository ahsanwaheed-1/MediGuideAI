import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage

from src.config import (
    PAGE_TITLE, PAGE_ICON, GENDER_OPTIONS, DURATION_OPTIONS,
    SYMPTOM_SUGGESTIONS, LANGUAGE_OPTIONS, MODEL_OPTIONS, DEFAULT_MODEL
)
from src.chains import get_llm, stream_narrative
from src.cache_manager import configure_cache
from src.utils import parse_json

# --- Page Config ---
st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout="wide")

# --- Initialize Session State ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "Light"

# --- Inject Custom CSS for Dark Mode ---
def apply_theme(theme_mode):
    if theme_mode == "Dark":
        dark_css = """
        <style>
        .stApp {
            background-color: #1E1E1E;
            color: #FFFFFF;
        }
        [data-testid="stSidebar"] {
            background-color: #2D2D2D;
        }
        /* Make most texts white in dark mode */
        h1, h2, h3, h4, h5, h6, p, span, div, label {
            color: #FFFFFF !important;
        }
        /* Exception for inputs to keep them readable if they don't override well */
        input, textarea, select {
            color: #000000 !important;
            background-color: #FFFFFF !important;
        }
        </style>
        """
        st.markdown(dark_css, unsafe_allow_html=True)
    else:
        # Default Streamlit light mode, no heavy override needed
        pass

# --- Sidebar ---
with st.sidebar:
    st.title(f"{PAGE_ICON} {PAGE_TITLE}")
    st.write("An educational AI-powered medical symptom assessment assistant.")
    
    st.markdown("---")
    
    st.session_state.theme_mode = st.radio("Theme Mode", ["Light", "Dark"], index=0 if st.session_state.theme_mode == "Light" else 1)
    apply_theme(st.session_state.theme_mode)

    st.markdown("---")
    openai_api_key = st.text_input("OpenAI API Key", type="password", help="Enter your OpenAI API key to power the medical assistant.")

    selected_model = st.selectbox("Model", MODEL_OPTIONS, index=MODEL_OPTIONS.index(DEFAULT_MODEL))
    cache_mode = st.selectbox("Caching Strategy", ["None", "InMemory", "SQLite"])
    selected_language = st.selectbox("Language", LANGUAGE_OPTIONS, index=0)
    
    st.markdown("---")
    st.error("**MEDICAL DISCLAIMER**\n\nThis application is an educational prototype. It is NOT a doctor. Do not use for confirmed medical diagnosis. Seek emergency help in urgent situations.")

# Apply cache config
configure_cache(cache_mode)

# --- Main App ---
st.header("Medical Symptom Assessment")
st.warning("⚠️ **Reminder**: This tool provides educational guidance only. Please consult a qualified healthcare professional for medical advice.")

# --- History View ---
if st.session_state.chat_history:
    with st.expander("Patient Session History", expanded=False):
        for msg in st.session_state.chat_history:
            if isinstance(msg, HumanMessage):
                st.markdown(f"**Patient Input**: {msg.content}")
            elif isinstance(msg, AIMessage):
                st.markdown(f"**MediGuide AI**: {msg.content}")
            st.divider()

# --- Input Form ---
with st.form("symptom_form"):
    col1, col2 = st.columns(2)
    with col1:
        age = st.text_input("Age")
        gender = st.selectbox("Gender", GENDER_OPTIONS)
        duration = st.selectbox("Duration of Symptoms", DURATION_OPTIONS)
        severity = st.slider("Severity (1-10)", 1, 10, 5)
    
    with col2:
        symptoms = st.multiselect("Symptoms", SYMPTOM_SUGGESTIONS)
        custom_symptoms = st.text_input("Other Symptoms (Optional)")
        conditions = st.text_area("Existing Medical Conditions")
        medications = st.text_area("Current Medications")
        notes = st.text_area("Additional Notes")
    
    submit_btn = st.form_submit_button("Assess Symptoms")

# --- Processing & Output ---
if submit_btn:
    if not symptoms and not custom_symptoms:
        st.error("Please select or enter at least one symptom.")
    elif not age.strip():
        st.error("Please enter your age.")
    elif gender == "Select" or duration == "Select":
        st.error("Please select gender and duration.")
    elif not openai_api_key or not openai_api_key.startswith("sk-"):
        st.error("Please provide a valid OpenAI API key in the sidebar.")
    else:
        st.info("Analyzing symptoms... Please wait.")
        
        # Build inputs for LLM
        all_symptoms = ", ".join(symptoms)
        if custom_symptoms:
            all_symptoms += f", {custom_symptoms}"
            
        inputs = {
            "age": age,
            "gender": gender,
            "conditions": conditions if conditions else "None",
            "medications": medications if medications else "None",
            "symptoms": all_symptoms,
            "duration": duration,
            "severity": str(severity),
            "notes": notes if notes else "None",
            "language": selected_language,
            "chat_history": st.session_state.chat_history
        }
        
        # Initialize Model
        llm = get_llm(model_name=selected_model, api_key=openai_api_key)
        
        # Streaming Output Container
        st.subheader("Guidance Narrative")
        narrative_container = st.empty()
        full_response = ""
        
        try:
            # Stream the narrative live
            with narrative_container:
                stream_generator = stream_narrative(llm, inputs)
                full_response = st.write_stream(stream_generator)
            
            # Parse JSON
            parsed_data = parse_json(full_response)
            
            # Render Dashboard
            st.markdown("---")
            st.header("Assessment Results")
            
            # Urgency Metric
            urgency = parsed_data.get("urgency_level", "UNKNOWN").upper()
            if urgency == "EMERGENCY":
                st.error(f"🚨 URGENCY LEVEL: {urgency} - SEEK IMMEDIATE MEDICAL HELP!")
            elif urgency == "HIGH":
                st.warning(f"⚠️ URGENCY LEVEL: {urgency} - Please consult a doctor promptly.")
            elif urgency == "MEDIUM":
                st.info(f"🟡 URGENCY LEVEL: {urgency} - Monitor closely and consider seeing a doctor.")
            else:
                st.success(f"🟢 URGENCY LEVEL: {urgency} - Monitor symptoms.")
                
            # Summary
            st.subheader("Summary")
            st.write(parsed_data.get("summary", "No summary provided."))
            
            # Dashboard Columns
            res_col1, res_col2 = st.columns(2)
            
            with res_col1:
                st.subheader("Possible Conditions")
                conditions_list = parsed_data.get("possible_conditions", [])
                if conditions_list:
                    for cond in conditions_list:
                        with st.expander(cond.get("name", "Unknown")):
                            st.write(cond.get("reason", "No reason provided."))
                else:
                    st.write("None identified.")
                    
                st.subheader("Recommended Next Steps")
                steps = parsed_data.get("recommended_next_steps", [])
                for step in steps:
                    st.markdown(f"- {step}")
            
            with res_col2:
                st.subheader("Questions for Your Doctor")
                questions = parsed_data.get("questions_for_doctor", [])
                for q in questions:
                    st.markdown(f"- {q}")
                    
                st.subheader("Warning Signs (Seek Immediate Help)")
                warnings = parsed_data.get("warning_signs", [])
                for w in warnings:
                    st.markdown(f"🚨 {w}")

            # Append to session history (simplified context)
            human_msg = HumanMessage(content=f"Age: {age}, Gender: {gender}, Symptoms: {all_symptoms}, Severity: {severity}")
            ai_msg = AIMessage(content=full_response)
            st.session_state.chat_history.append(human_msg)
            st.session_state.chat_history.append(ai_msg)

        except Exception as e:
            st.error(f"An error occurred during assessment: {str(e)}")
            st.error("Please ensure your OpenAI API key is correct and has sufficient quota.")
