import json
import requests
import streamlit as st

st.set_page_config(
    page_title="AI Invoice Extraction",
    page_icon="📄",
    layout="wide"
)

st.title("📄 AI Invoice Extraction")
st.caption("Extract structured invoice data using PaddleOCR + Llama 3.2")

uploaded_file = st.file_uploader(
    "Upload Invoice",
    type=["pdf", "png", "jpg", "jpeg"]
)

if uploaded_file:

    col1, col2 = st.columns([1, 1])

    with col1:

        st.subheader("Uploaded File")

        if uploaded_file.type.startswith("image"):
            st.image(uploaded_file)

        else:
            st.info(uploaded_file.name)

        if st.button("Extract Invoice", use_container_width=True):

            with st.spinner("Processing invoice..."):

                files = {
                    "file": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        uploaded_file.type
                    )
                }

                response = requests.post(
                    "http://127.0.0.1:8000/api/extract",
                    files=files
                )

            with col2:

                st.subheader("Extracted JSON")

                if response.status_code == 200:

                    data = response.json()

                    st.success("Extraction completed")

                    st.json(data["invoice"])

                    st.download_button(
                        "Download JSON",
                        json.dumps(
                            data["invoice"],
                            indent=4
                        ),
                        file_name="invoice.json",
                        mime="application/json",
                        use_container_width=True
                    )

                else:

                    st.error(response.text)