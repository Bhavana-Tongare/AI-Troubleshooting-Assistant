import streamlit as st
from retrieve import search
from ai_assistant import ask_groq

MIN_SCORE = 0.20

st.set_page_config(
    page_title="AI Troubleshooting Assistant",
    page_icon="🛠️",
    layout="wide"
)

# Custom styling
st.markdown(
"""
<style> 

    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&display=swap');

    :root {
        --accent: #0E7C86;
        --accent-dark: #0A5F67;
        --accent-soft: rgba(14, 124, 134, 0.10);
        --line: rgba(128, 140, 155, 0.30);
        --card: rgba(128, 140, 155, 0.07);
    }

    html, body, [class*="css"], .stMarkdown, .stTextArea textarea {
        font-family: 'IBM Plex Sans', sans-serif;
    }

    .stMarkdown h1 {
        font-size: 26px !important;
    }

    .stMarkdown h2 {
        font-size: 24px !important;
    }

    .stMarkdown h3 {
        font-size: 21px !important;
        font-weight: 600 !important;
    }

    .stMarkdown h4 {
        font-size: 16px !important;
    }

    .block-container {
        max-width: 1050px;
        padding-top: 2rem;
    }

    .main-title {
        text-align: center;
        font-size: 48px !important;
        font-weight: 700 !important;
        line-height: 1.2 !important;
        color: var(--text-color);
    }

    .subtitle {
        text-align: center;
        font-size: 20px !important;
        color: var(--text-color);
        opacity: 0.75;
        margin-bottom: 30px;
    }

    .step-card {
        border: 1px solid var(--line);
        border-radius: 12px;
        padding: 16px;
        min-height: 135px;
        background-color: var(--card);
    }

    .step-card h4 {
        color: var(--accent);
        margin-top: 0;
    }

    .step-card p {
        opacity: 0.75;
        font-size: 14px;
    }

    /* Text area */
    .stTextArea textarea {
        border-radius: 10px;
        font-size: 15px;
    }

    /* Metric cards (Knowledge Base ID, Similarity Score) */
    [data-testid="stMetric"] {
        border: 1px solid var(--line);
        border-radius: 12px;
        padding: 14px 18px;
        background: var(--card);
    }

    /* Info / success / warning boxes */
    [data-testid="stAlert"] {
        border-radius: 10px;
    }

    /* Expander and bordered answer container */
    [data-testid="stExpander"] {
        border-radius: 10px;
        border-color: var(--line);
    }

    [data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 12px;
        border-color: var(--line);
        background: var(--card);
    }

    /* Find Solution Button */
    div.stButton > button {
        background-color: #0E7C86 !important;
        color: #FFFFFF !important;
        border: 1px solid #0E7C86 !important;
        border-radius: 8px;
        padding: 10px 28px;
        font-size: 16px;
        font-weight: 600;
        opacity: 1 !important;
        visibility: visible !important;
    }

    /* Button hover */
    div.stButton > button:hover {
        background-color: #0A5F67 !important;
        color: #FFFFFF !important;
        border-color: #0A5F67 !important;
    }

    /* Button focus */
    div.stButton > button:focus {
        color: #FFFFFF !important;
        outline: 3px solid rgba(14, 124, 134, 0.25);
        outline-offset: 2px;
    }

    /* Button text */
    div.stButton > button p {
        color: #FFFFFF !important;
        font-weight: 600;
    }
    }
</style>
""", unsafe_allow_html=True)


# Sidebar settings
st.sidebar.title("⚙️ Settings")

show_context = st.sidebar.checkbox(
    "Show retrieved context",
    value=True
)

st.sidebar.caption(
    "View the knowledge-base information matched to your question."
)


# Main heading
st.markdown(
    '<div class="main-title"> 🛠️ AI Troubleshooting Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Find technical solutions using intelligent knowledge retrieval.</div>',
    unsafe_allow_html=True
)

st.divider()


# Ask a question
st.subheader("💬 Ask a Question")

question = st.text_area(
    "Your technical problem",
    placeholder="Example: Payment API returning HTTP 500 error...",
    height=100
)


# Search button
if st.button("Find Solution"):

    if not question.strip():
        st.warning("Please enter a technical problem.")

    else:
        # Step 1: Retrieve relevant information
        kb_entry, score = search(question)

        if kb_entry is None or score is None or score < MIN_SCORE:
            st.warning(
                "This problem is not present in the knowledge base."
            )

            if score is not None:

                col1, col2 = st.columns(2)

                with col1:
                    st.metric(
                        label="Similarity Score",
                        value=f"{score:.2f}"
                    )

                with col2:
                    st.metric(
                        label = "Minimum Required",
                        value=f"{MIN_SCORE:.2f}"
                    )

            st.info(
                "Please add more details and try again,for example:\n"
                "-The exact error message or error code."
                "-The system, service or API invovled."
                "-What you were doing when the problem occurred"
            )


        else:
            st.success("Relevant knowledge-base information found!")

            st.markdown("### 📋 Troubleshooting Report")


            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    label = "Knowledge Base ID",
                    value=kb_entry["id"]
                )

            with col2:
                st.metric(
                    label="Similarity Score",
                    value=f"{score:.2f}"
                )

            st.markdown("### Identified Issue")
            st.info(kb_entry["issue"])

            # Display retrieved information 
            if show_context:
                with st.expander("View Retrieved Context"):
                    st.json(kb_entry)


            # Generate AI answer using Groq

            st.markdown("#### AI Troubleshooting Answer")

            with st.spinner("Generating ..."):
            
                try:
                    print("Sending question to Groq..... ",flush=True)

                    answer = ask_groq(question, kb_entry)

                    print("Groq response  received !!",flush=True)

                    st.caption("AI Model: openai/gpt-oss-20b")
                    with st.container(border=True):
                        st.markdown(answer)

                except Exception as error:
                    st.error("AI models failed to generate an answer.")
                    st.exception(error)



                    