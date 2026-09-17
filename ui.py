import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:8000"

# ─────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────
st.set_page_config(
    page_title="InsightForge",
    page_icon="🔬",
    layout="wide"
)

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
    st.image("https://img.icons8.com/fluency/96/research.png", width=80)
    st.title("InsightForge")
    st.markdown("---")
    mode = st.radio(
        "Choose Mode",
        ["🔍 Research", "⚖️ Compare", "💬 Chat"],
        index=0
    )
    st.markdown("---")
    st.markdown("Built with LangChain + Groq + FastAPI")

# ─────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────
if "session_id" not in st.session_state:
    st.session_state.session_id = None
if "report" not in st.session_state:
    st.session_state.report = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

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
            with st.spinner("Running 4-step research pipeline... this may take 20-30 seconds ⏳"):
                try:
                    response = requests.post(
                        f"{BASE_URL}/research",
                        json={"topic": topic}
                    )
                    if response.status_code == 200:
                        data = response.json()
                        st.session_state.session_id = data["session_id"]
                        st.session_state.report = data["report"]
                        st.session_state.chat_history = []
                        st.success("✅ Report generated successfully!")
                    else:
                        st.error(f"Error: {response.text}")
                except Exception as e:
                    st.error(f"Could not connect to server: {e}")

    if st.session_state.report and mode == "🔍 Research":
        st.divider()
        st.subheader("📄 Research Report")
        st.markdown(st.session_state.report)
        st.divider()

        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                label="⬇️ Download Report",
                data=st.session_state.report,
                file_name=f"{topic.replace(' ', '_')}.txt",
                mime="text/plain",
                use_container_width=True
            )
        with col2:
            st.info(f"💬 Session ID: `{st.session_state.session_id}`")

# ─────────────────────────────────────────
# COMPARE MODE
# ─────────────────────────────────────────
elif mode == "⚖️ Compare":
    st.subheader("⚖️ Compare Two Topics")
    st.write("Enter two topics and InsightForge will generate a side-by-side comparison digest.")

    col1, col2 = st.columns(2)
    with col1:
        topic_a = st.text_input("Topic A", placeholder="e.g. React")
    with col2:
        topic_b = st.text_input("Topic B", placeholder="e.g. Vue")

    if st.button("Compare Topics", type="primary", use_container_width=True):
        if not topic_a or not topic_b:
            st.warning("Please enter both topics!")
        else:
            with st.spinner(f"Comparing {topic_a} vs {topic_b}... this may take 30-40 seconds ⏳"):
                try:
                    response = requests.post(
                        f"{BASE_URL}/compare",
                        json={"topic_a": topic_a, "topic_b": topic_b}
                    )
                    if response.status_code == 200:
                        data = response.json()
                        st.session_state.session_id = data["session_id"]
                        st.session_state.report = data["report"]
                        st.session_state.chat_history = []
                        st.success("✅ Comparison report generated!")
                    else:
                        st.error(f"Error: {response.text}")
                except Exception as e:
                    st.error(f"Could not connect to server: {e}")

    if st.session_state.report and mode == "⚖️ Compare":
        st.divider()
        st.subheader(f"📊 Comparison: {topic_a} vs {topic_b}")
        st.markdown(st.session_state.report)
        st.divider()

        st.download_button(
            label="⬇️ Download Report",
            data=st.session_state.report,
            file_name=f"{topic_a}_vs_{topic_b}.txt",
            mime="text/plain",
            use_container_width=True
        )

# ─────────────────────────────────────────
# CHAT MODE
# ─────────────────────────────────────────
elif mode == "💬 Chat":
    st.subheader("💬 Chat About Your Report")

    if not st.session_state.session_id:
        st.warning("⚠️ No report generated yet! Go to Research or Compare mode first.")
    else:
        st.info(f"Chatting about report — Session: `{st.session_state.session_id}`")

        # Display chat history
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Chat input
        question = st.chat_input("Ask anything about the report...")

        if question:
            # Show user message
            st.session_state.chat_history.append({
                "role": "user",
                "content": question
            })
            with st.chat_message("user"):
                st.markdown(question)

            # Get response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        response = requests.post(
                            f"{BASE_URL}/chat",
                            json={
                                "session_id": st.session_state.session_id,
                                "question": question
                            }
                        )
                        if response.status_code == 200:
                            answer = response.json()["answer"]
                            st.markdown(answer)
                            st.session_state.chat_history.append({
                                "role": "assistant",
                                "content": answer
                            })
                        else:
                            st.error(f"Error: {response.text}")
                    except Exception as e:
                        st.error(f"Could not connect to server: {e}")