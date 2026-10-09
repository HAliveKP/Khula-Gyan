"""Beginner-friendly Streamlit screen for the Day 1 mock pipeline."""

import streamlit as st

from src.pipeline import ask


st.set_page_config(page_title="Khula Gyan", page_icon="📄")
st.title("Khula Gyan")
st.caption("Cited answers from official Nepali documents")
st.warning(
    "Demo screen: the answer below is sample data. Official sources and search are not connected yet.",
    icon="⚠️",
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
question = st.text_input("What would you like to know?", placeholder="How do I renew a driving license?")

if st.button("Ask", type="primary"):
    response = ask(question, service=service)
    st.subheader("Sample answer")
    st.write(response["answer"])

    with st.expander("Checklist"):
        checklist = response["checklist"]
        for label in ("documents", "fees", "steps"):
            st.markdown(f"**{label.title()}**")
            if checklist[label]:
                for item in checklist[label]:
                    st.write(f"- {item}")
            else:
                st.caption("No items in this demo")
        st.markdown("**Where**")
        st.write(checklist["where"] or "Not available in this demo")

    st.subheader("Citations")
    if response["citations"]:
        for citation in response["citations"]:
            st.markdown(f"**{citation['source']} · page {citation['page']}**")
            st.markdown(f"> {citation['quote']}")
    else:
        st.info("No citation is available for this empty question.")

    st.caption(f"Confidence: {response['confidence']} · {response['disclaimer']}")

st.caption("Khula Gyan explains official procedures; it does not provide legal advice.")
