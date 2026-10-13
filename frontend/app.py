"""Streamlit question screen with evidence citations and friendly errors."""

import streamlit as st

from src.pipeline import ask


st.set_page_config(page_title="Khula Gyan", page_icon="📄")
st.title("Khula Gyan")
st.caption("Cited answers from official Nepali documents — Palika Guide")
st.info(
    "Answers use passages from official municipal citizen charters (नागरिक बडापत्र). "
    "If the sources do not support a response, Khula Gyan says it cannot find the answer."
)

# Municipality selector (for Palika Guide)
municipality = st.selectbox(
    "Choose a municipality (पालिका)",
    options=("", "Lalitpur", "Kathmandu", "Bhaktapur", "Pokhara", "Biratnagar", "Biratnagar"),
    format_func=lambda value: value if value else "— Select a municipality —",
    help="Required for Palika Guide questions. Answers only come from the selected municipality's citizen charter."
)

service = st.selectbox(
    "Choose a service",
    options=("palika_guide", "driving_license", "citizenship", "passport"),
    format_func=lambda value: {
        "palika_guide": "Palika Guide (municipal services)",
        "driving_license": "Driving license",
        "citizenship": "Citizenship certificate",
        "passport": "Passport",
    }[value],
)
question = st.text_input(
    "What would you like to know?",
    placeholder="What do I need for birth registration in Lalitpur ward 5?",
)

if st.button("Ask", type="primary"):
    if not question.strip():
        st.warning("Type a question first.")
    else:
        try:
            with st.spinner("Searching official sources…"):
                response = ask(question, service=service, municipality=municipality if municipality else None)
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
                    st.markdown("**Officer / Time / Fee**")
                    # Display fee, time, officer from steps/where or show not stated
                    fee_items = [item for item in checklist["fees"] if item]
                    if fee_items:
                        st.markdown("**Fees:** " + "; ".join(fee_items))
                    else:
                        st.caption("Fees: Not stated in the retrieved passages")
                    # Time and officer are typically in steps or where
                    time_items = [item for item in checklist["steps"] if any(kw in item.lower() for kw in ["day", "week", "month", "time", "दिन", "हप्ता", "महिना", "समय"])]
                    if time_items:
                        st.markdown("**Time:** " + "; ".join(time_items))
                    else:
                        st.caption("Time: Not stated in the retrieved passages")

                st.subheader("Citations")
                for citation in response["citations"]:
                    source_info = f"**{citation['source']} · page {citation['page']}**"
                    if citation.get('municipality'):
                        source_info += f" · {citation['municipality']}"
                    st.markdown(source_info)
                    st.markdown(f"> {citation['quote']}")
                st.caption(f"Confidence: {response['confidence']}")

            st.caption(response["disclaimer"])

st.caption("Khula Gyan explains official procedures; it does not provide legal advice.")