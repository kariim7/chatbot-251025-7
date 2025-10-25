import streamlit as st
from openai import OpenAI

# 앱 제목과 설명
st.title("💬 답변이")
st.write(
    "이 앱은 OpenAI의 GPT 모델을 사용한 간단한 챗봇입니다. "
    "사용하려면 OpenAI API 키를 입력해야 합니다. "
    "[API 키 발급하기](https://platform.openai.com/account/api-keys)"
)

# OpenAI API 키 입력
openai_api_key = st.text_input("🔑 OpenAI API Key", type="password")

# 종료(초기화) 버튼 추가
if st.button("🔄 종료 / 초기화"):
    st.session_state.clear()
    st.success("✅ 대화가 초기화되었습니다. 새로 시작할 수 있습니다.")
    st.stop()

# API 키 없으면 안내 메시지
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")

else:
    # OpenAI 클라이언트 생성
    client = OpenAI(api_key=openai_api_key)

    # 세션 상태에 messages 초기화
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 이전 메시지 표시
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 사용자 입력 받기
    if prompt := st.chat_input("무엇을 도와드릴까요?"):
        # 사용자 메시지 저장 및 표시
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # OpenAI 응답 생성 (스트리밍)
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        # 응답 스트리밍 표시
        with st.chat_message("assistant"):
            response = st.write_stream(stream)

        # 응답 저장
        st.session_state.messages.append({"role": "assistant", "content": response})
