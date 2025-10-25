import streamlit as st
from openai import OpenAI

# App title and description
st.title("🗣️ 언어 학습 도우미 (Language Study Guide Chatbot)")
st.write(
    "이 챗봇은 다양한 언어 학습을 돕기 위한 도우미입니다. 🧠\n\n"
    "문법 설명, 단어 연습, 회화 예문, 학습 계획 등 다양한 질문을 해보세요!\n"
    "예시 질문:\n"
    "- '영어로 시제 공부를 도와줘'\n"
    "- '한국어 회화 연습할래요'\n"
    "- '스페인어 단어 암기법 알려줘'\n\n"
    "[OpenAI API 키 발급하기](https://platform.openai.com/account/api-keys)"
)

# OpenAI API key input
openai_api_key = st.text_input("🔑 OpenAI API Key", type="password")

# Reset/End button
if st.button("🔄 종료 / 초기화"):
    st.session_state.clear()
    st.success("✅ 대화가 초기화되었습니다. 새 언어 학습을 시작할 수 있습니다!")
    st.stop()

# Check for API key
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")

else:
    # Initialize OpenAI client
    client = OpenAI(api_key=openai_api_key)

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "system",
                "content": (
                    "You are an expert **language learning guide** who helps users study any language "
                    "such as English, Korean, Spanish, Japanese, or others. "
                    "Give explanations, exercises, and friendly encouragement. "
                    "Use both the target language and the user's language when helpful. "
                    "Encourage practice and suggest learning techniques."
                ),
            }
        ]

    # Display chat history
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # User input
    if prompt := st.chat_input("배우고 싶은 언어나 질문을 입력하세요!"):
        # Store and show user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate response (streaming)
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages,
            stream=True,
        )

        # Stream and display response
        with st.chat_message("assistant"):
            response = st.write_stream(stream)

        # Store assistant response
        st.session_state.messages.append({"role": "assistant", "content": response})
