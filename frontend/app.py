import json
import requests
import streamlit as st

st.set_page_config(
    page_title="Invoice Extractor",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Invoice Extractor")

st.write("Upload an invoice (PDF/JPG/PNG) to extract structured JSON.")

uploaded_file = st.file_uploader(
    "Choose Invoice",
    type=["pdf", "jpg", "jpeg", "png"]
)

if uploaded_file:

    st.success(f"Uploaded: {uploaded_file.name}")

    if st.button("🚀 Extract Invoice"):

        with st.spinner("Extracting invoice..."):

            response = requests.post(
                "http://127.0.0.1:8000/api/extract",
                files={
                    "file": (
                        uploaded_file.name,
                        uploaded_file,
                        uploaded_file.type
                    )
                }
            )

        if response.status_code == 200:

            result = response.json()

            st.success("✅ Extraction Completed")

            st.subheader("Extracted JSON")

            st.json(result)

            # ----------------------------
            # Download JSON
            # ----------------------------

            json_data = json.dumps(
                result,
                indent=4,
                ensure_ascii=False
            )

            st.download_button(
                label="📥 Download JSON",
                data=json_data,
                file_name=f"{uploaded_file.name.rsplit('.',1)[0]}.json",
                mime="application/json"
            )

        else:

            st.error("Extraction Failed")

            st.code(response.text)