import streamlit as st
import fitz
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load API Key
load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

st.set_page_config(page_title="DDR Generator")

st.title("AI DDR Report Generator")

# Upload PDFs
inspection_file = st.file_uploader(
    "Upload Inspection Report",
    type=["pdf"]
)

thermal_file = st.file_uploader(
    "Upload Thermal Report",
    type=["pdf"]
)

# Extract Text Function
def extract_text(pdf_file):
    text = ""

    pdf_bytes = pdf_file.read()

    pdf = fitz.open(
        stream=pdf_bytes,
        filetype="pdf"
    )

    for page in pdf:
        text += page.get_text()

    return text


if inspection_file and thermal_file:

    inspection_text = extract_text(inspection_file)
    thermal_text = extract_text(thermal_file)

    st.success("PDFs Processed Successfully")

    st.subheader("Inspection Report Preview")
    st.text_area(
        "Inspection Text",
        inspection_text[:2000],
        height=200
    )

    st.subheader("Thermal Report Preview")
    st.text_area(
        "Thermal Text",
        thermal_text[:2000],
        height=200
    )

    st.subheader("Generate DDR Report")

    if st.button("Generate DDR"):

        prompt = f"""
        You are a professional building inspection expert.

        Using the Inspection Report and Thermal Report below,
        generate a Detailed Diagnostic Report (DDR).

        Follow this structure:

        1. Property Issue Summary
        2. Area-wise Observations
        3. Probable Root Cause
        4. Severity Assessment (with reasoning)
        5. Recommended Actions
        6. Additional Notes
        7. Missing or Unclear Information

        Rules:
        - Do not invent facts
        - Mention conflicts if present
        - Mention Not Available where needed
        - Use client-friendly language

        Inspection Report:
        {inspection_text}

        Thermal Report:
        {thermal_text}
        """

        model = genai.GenerativeModel(
            "gemini-2.5-flash"
        )

        response = model.generate_content(prompt)

        st.subheader("Generated DDR Report")

        st.write(response.text)

        st.download_button(
            label="Download DDR Report",
            data=response.text,
            file_name="DDR_Report.txt",
            mime="text/plain"
        )


