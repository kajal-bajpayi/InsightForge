import streamlit as st
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()

# ─────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────
st.set_page_config(
    page_title="InsightForge",
    page_icon="🔬",
    layout="wide"
)

# ─────────────────────────────────────────
# MODEL SETUP
# ─────────────────────────────────────────
@st.cache_resource
def get_model():
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        try:
            api_key = st.secrets["GROQ_API_KEY"]
        except:
            st.error("❌ GROQ_API_KEY not found. Please add it in Streamlit secrets.")
            st.stop()
    return ChatGroq(model="openai/gpt-oss-120b", temperature=0.3, api_key=api_key)

# ─────────────────────────────────────────
# CORE INVOKE FUNCTION
# ─────────────────────────────────────────
def invoke_chain(prompt_template: str, variables: dict) -> str:
    model = get_model()
    prompt = ChatPromptTemplate.from_template(prompt_template)
    messages = prompt.format_messages(**variables)
    response = model.invoke(messages)
    return response.content

# ─────────────────────────────────────────
# SINGLE TOPIC PIPELINE
# ─────────────────────────────────────────
def run_pipeline(topic: str) -> dict:
    research = invoke_chain("""
You are a research assistant.
List 5 important and recent developments about: {topic}
Be factual and concise. Use bullet points.
""", {"topic": topic})

    summary = invoke_chain("""
You are a summarizer.
Given these research points:
{research}
Write a concise 3-paragraph summary capturing the most important ideas.
""", {"research": research})

    critique = invoke_chain("""
You are a critical analyst.
Given this summary:
{summary}
Identify 3 important gaps, open questions, or counterpoints
that were not addressed. Be specific.
""", {"summary": summary})

    report = invoke_chain("""
You are a professional report writer.
Write a polished research digest with these sections:

## Overview
## Key Findings
## Open Questions
## Conclusion

Summary: {summary}
Critical Analysis: {critique}
""", {"summary": summary, "critique": critique})

    return {
        "topic": topic,
        "research": research,
        "summary": summary,
        "critique": critique,
        "report": report
    }

# ─────────────────────────────────────────
# COMPARISON PIPELINE
# ─────────────────────────────────────────
def run_comparison(topic_a: str, topic_b: str) -> dict:
    research_a = invoke_chain("""
You are a research assistant.
List 5 important facts and developments about: {topic}
Be factual and concise. Use bullet points.
""", {"topic": topic_a})

    research_b = invoke_chain("""
You are a research assistant.
List 5 important facts and developments about: {topic}
Be factual and concise. Use bullet points.
""", {"topic": topic_b})

    summary_a = invoke_chain("""
You are a summarizer.
Given these research points about {topic}:
{research}
Write a concise 2-paragraph summary.
""", {"topic": topic_a, "research": research_a})

    summary_b = invoke_chain("""
You are a summarizer.
Given these research points about {topic}:
{research}
Write a concise 2-paragraph summary.
""", {"topic": topic_b, "research": research_b})

    comparison = invoke_chain("""
You are an expert analyst.
Compare these two topics:

Topic A: {topic_a} — Summary: {summary_a}
Topic B: {topic_b} — Summary: {summary_b}

Cover: similarities, differences, strengths, weaknesses, use cases.
""", {"topic_a": topic_a, "summary_a": summary_a,
      "topic_b": topic_b, "summary_b": summary_b})

    report = invoke_chain("""
You are a professional report writer.
Write a polished comparison digest with these sections:

## Overview
## {topic_a} — Key Strengths
## {topic_b} — Key Strengths
## Head to Head Comparison
## Verdict — Which Should You Choose?
## Conclusion

Topic A Summary: {summary_a}
Topic B Summary: {summary_b}
Comparison: {comparison}
""", {"topic_a": topic_a, "topic_b": topic_b,
      "summary_a": summary_a, "summary_b": summary_b,
      "comparison": comparison})

    return {
        "topic_a": topic_a,
        "topic_b": topic_b,
        "report": report
    }

# ─────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────
if "report" not in st.session_state:
    st.session_state.report = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "topic_label" not in st.session_state:
    st.session_state.topic_label = ""

# ─────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────
st.title("🔬 InsightForge")
st.caption("AI-powered research digest and comparison engine")
st.divider()

# ─────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────
with st.sidebar:
    st.title("InsightForge")
    st.markdown("---")
    mode = st.radio(
        "Choose Mode",
        ["🔍 Research", "⚖️ Compare", "💬 Chat"],
        index=0
    )
    st.markdown("---")
    st.markdown("Built with LangChain + Groq + Streamlit")
    st.markdown("---")
    if st.session_state.report:
        st.success("✅ Report ready — switch to Chat mode!")

# ─────────────────────────────────────────
# RESEARCH MODE
# ─────────────────────────────────────────
if mode == "🔍 Research":
    st.subheader("🔍 Research a Topic")
    st.write("Enter any topic and InsightForge will generate a full research digest.")

    topic = st.text_input("Topic", placeholder="e.g. artificial intelligence in healthcare")

    if st.button("Generate Report", type="primary", use_container_width=True):
        if not topic:
            st.warning("Please enter a topic!")
        else:
            with st.spinner("Running 4-step research pipeline... ⏳ (~20-30 seconds)"):
                try:
                    result = run_pipeline(topic)
                    st.session_state.report = result["report"]
                    st.session_state.chat_history = []
                    st.session_state.topic_label = topic
                    st.success("✅ Report generated!")
                except Exception as e:
                    st.error(f"Error: {str(e)}")

    if st.session_state.report and mode == "🔍 Research":
        st.divider()
        st.subheader("📄 Research Report")
        st.markdown(st.session_state.report)
        st.divider()
        st.download_button(
            label="⬇️ Download Report",
            data=st.session_state.report,
            file_name=f"{st.session_state.topic_label.replace(' ', '_')}.txt",
            mime="text/plain",
            use_container_width=True
        )

# ─────────────────────────────────────────
# COMPARE MODE
# ─────────────────────────────────────────
elif mode == "⚖️ Compare":
    st.subheader("⚖️ Compare Two Topics")
    st.write("Enter two topics for a side-by-side AI comparison digest.")

    col1, col2 = st.columns(2)
    with col1:
        topic_a = st.text_input("Topic A", placeholder="e.g. React")
    with col2:
        topic_b = st.text_input("Topic B", placeholder="e.g. Vue")

    if st.button("Compare Topics", type="primary", use_container_width=True):
        if not topic_a or not topic_b:
            st.warning("Please enter both topics!")
        else:
            with st.spinner(f"Comparing {topic_a} vs {topic_b}... ⏳ (~40 seconds)"):
                try:
                    result = run_comparison(topic_a, topic_b)
                    st.session_state.report = result["report"]
                    st.session_state.chat_history = []
                    st.session_state.topic_label = f"{topic_a} vs {topic_b}"
                    st.success("✅ Comparison report generated!")
                except Exception as e:
                    st.error(f"Error: {str(e)}")

    if st.session_state.report and mode == "⚖️ Compare":
        st.divider()
        st.subheader(f"📊 {st.session_state.topic_label}")
        st.markdown(st.session_state.report)
        st.divider()
        st.download_button(
            label="⬇️ Download Report",
            data=st.session_state.report,
            file_name=f"{st.session_state.topic_label.replace(' ', '_').replace(' ', '_')}.txt",
            mime="text/plain",
            use_container_width=True
        )

# ─────────────────────────────────────────
# CHAT MODE
# ─────────────────────────────────────────
elif mode == "💬 Chat":
    st.subheader("💬 Chat About Your Report")

    if not st.session_state.report:
        st.warning("⚠️ No report yet! Go to Research or Compare mode first to generate one.")
    else:
        st.info(f"Chatting about: **{st.session_state.topic_label}**")

        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        question = st.chat_input("Ask anything about the report...")

        if question:
            st.session_state.chat_history.append({
                "role": "user",
                "content": question
            })
            with st.chat_message("user"):
                st.markdown(question)

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        answer = invoke_chain("""
You are a research assistant for InsightForge.
You have access to this research report:

{report}

Answer the following question based on the report only.
Be specific and cite relevant sections where possible.

Question: {question}
""", {"report": st.session_state.report, "question": question})

                        st.markdown(answer)
                        st.session_state.chat_history.append({
                            "role": "assistant",
                            "content": answer
                        })
                    except Exception as e:
                        st.error(f"Error: {str(e)}")