import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="ResearchMate AI",
    page_icon="📚",
    layout="centered"
)

st.title("📚 ResearchMate AI")
st.subheader("AI-Powered Research Paper Analyzer")
st.write("Upload, understand, and explore your research papers.")

api_key = st.secrets.get("GROQ_API_KEY", "")

if not api_key:
    st.error("API key is missing. Please configure your secrets.")
    st.stop()

client = Groq(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

prompt = st.chat_input("Ask anything about research...")

if prompt:
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("ResearchMate is thinking..."):
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are ResearchMate AI, a helpful "
                                "research assistant. Explain research "
                                "topics clearly, summarize academic "
                                "concepts, and help students understand "
                                "scientific papers using simple English. "
                                "Be accurate and never invent sources."
                            )
                        },
                        *st.session_state.messages
                    ]
                )

                answer = response.choices[0].message.content
                st.write(answer)

                st.session_state.messages.append(
                    {"role": "assistant", "content": answer}
                )

            except Exception as e:
                st.error(f"AI Error: {e}")

st.divider()
st.caption("ResearchMate AI | Academic Research Assistant")
