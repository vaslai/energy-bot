import streamlit as st
import google.generativeai as genai

# --- Ρυθμίσεις Σελίδας ---
st.set_page_config(page_title="Pilot Assistant 1-15", page_icon="👨‍✈️")
st.title("⚡ Pilot Assistant 1-15")
st.caption("Powered by Gemini 2.0 Flash (Online)")

# --- ΑΣΦΑΛΗΣ ΣΥΝΔΕΣΗ (Το σημαντικό σημείο) ---
# Ελέγχουμε αν υπάρχει το κλειδί στις "μυστικές ρυθμίσεις" του Cloud
try:
    if "GOOGLE_API_KEY" in st.secrets:
        GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
    else:
        # Αν τρέχει τοπικά και δεν βρίσκει secrets, σταματάει για ασφάλεια
        st.error("Δεν βρέθηκε το API Key. Ρύθμισε τα Secrets στο Streamlit Cloud.")
        st.stop()
except FileNotFoundError:
    st.error("Δεν βρέθηκε το αρχείο secrets.")
    st.stop()

genai.configure(api_key=GOOGLE_API_KEY)

# --- Η Προσωπικότητα ---
system_prompt = """
Είσαι ένας εξειδικευμένος Σύμβουλος Ενέργειας στην Ελλάδα.
Απαντάς ΜΟΝΟ σε θέματα ενέργειας:
- Λογαριασμοί Ρεύματος & Τιμολόγια.
- Φωτοβολταϊκά (Net Metering, Net Billing).
- Αντλίες Θερμότητας & Εξοικονόμηση.
- Φυσικό Αέριο.

Οδηγίες:
1. Να είσαι ευγενικός, σύντομος και σαφής.
2. Αν σε ρωτήσουν για άσχετα θέματα, πες ευγενικά: 
   "Συγγνώμη, ως Ενεργειακός Σύμβουλος απαντώ μόνο σε θέματα ενέργειας."
"""

# --- Μοντέλο ---
try:
    model = genai.GenerativeModel(
        model_name="models/gemini-flash-latest", 
        system_instruction=system_prompt
    )
except Exception as e:
    st.error(f"Σφάλμα μοντέλου: {e}")

# --- Μνήμη Συνομιλίας ---
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# --- Εμφάνιση Chat ---
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# --- Λήψη Ερώτησης ---
if prompt := st.chat_input("Ρώτησέ με..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    try:
        response = st.session_state.chat.send_message(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        st.chat_message("assistant").write(response.text)
    except Exception as e:

        st.error(f"Υπήρξε σφάλμα: {e}")
