"""Streamlit question screen with evidence citations and friendly errors."""

import streamlit as st

from src.pipeline import ask


st.set_page_config(page_title="Khula Gyan", page_icon="📄")
st.title("Khula Gyan")
st.caption("Cited answers from official Nepali documents")
st.info(
    "Answers appear only when the connected official sources support them. "
    "Search and answer modules are still being connected."
)

service = st.selectbox(
    "Choose a service",
    options=("driving_license", "citizenship", "passport"),
    format_func=lambda value: {
        "driving_license": "Driving license",
        "citizenship": "Citizenship certificate",
        "passport": "Passport",
    }[value],
)
question = st.text_input(
    "What would you like to know?",
    placeholder="How do I renew a driving license?",
)

if st.button("Ask", type="primary"):
    if not question.strip():
        st.warning("Type a question first.")
    else:
        try:
            with st.spinner("Searching official sources…"):
                response = ask(question, service=service)
        except Exception:
            st.error("We could not complete that search. Please try again later.")
        else:
            if response["status"] == "not_found":
                st.info(response["answer"])
            else:
                st.subheader("Answer")
                st.write(response["answer"])

                checklist = response["checklist"]
                with st.expander("Checklist"):
                    for label in ("documents", "fees", "steps"):
                        st.markdown(f"**{label.title()}**")
                        if checklist[label]:
                            for item in checklist[label]:
                                st.markdown(f"- {item}")
                        else:
                            st.caption("No supported items found")
                    st.markdown("**Where**")
                    st.write(checklist["where"] or "Not stated in the retrieved passages")

                st.subheader("Citations")
                for citation in response["citations"]:
                    st.markdown(f"**{citation['source']} · page {citation['page']}**")
                    st.markdown(f"> {citation['quote']}")
                st.caption(f"Confidence: {response['confidence']}")

            st.caption(response["disclaimer"])

st.caption("Khula Gyan explains official procedures; it does not provide legal advice.")
