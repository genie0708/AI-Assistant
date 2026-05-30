import streamlit as st
import google.generativeai as genai

# 웹 앱 기본 설정
st.set_page_config(page_title="매운맛 퀴즈 봇", page_icon="🦉")
st.title("🦉 AI 학습 튜터")
st.write("필기 내용을 입력하면 요약과 퀴즈를 만들어주고, 퀴즈를 틀리면 부엉이가 엄청나게 화를 냅니다!")

# 사이드바 설정
with st.sidebar:
    st.header("설정")
    api_key = st.text_input("Google Gemini API Key", type="password")

# 퀴즈 데이터를 유지하기 위한 세션 상태 초기화
if 'quiz_content' not in st.session_state:
    st.session_state.quiz_content = ""

# 메인 화면: 사용자 입력 창
lecture_notes = st.text_area("여기에 필기 내용을 붙여넣으세요:", height=150)

# 요약 및 퀴즈 생성 버튼
if st.button("요약 및 퀴즈 생성하기"):
    if not api_key:
        st.error("👈 왼쪽 사이드바에 Gemini API 키를 입력해 주세요!")
    elif not lecture_notes.strip():
        st.warning("필기 내용을 입력해 주세요.")
    else:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        학생이 입력한 아래의 강의 필기 내용을 바탕으로 다음을 수행해 주세요:
        1. 3~5개의 글머리 기호로 핵심 내용 요약
        2. 복습용 퀴즈 3문제 출제 (주의: 학생이 직접 풀어야 하므로 정답과 해설은 절대 미리 적지 마세요!)
        
        [강의 필기 내용]
        {lecture_notes}
        """
        
        with st.spinner("부엉이가 퀴즈를 출제하는 중입니다..."):
            response = model.generate_content(prompt)
            st.session_state.quiz_content = response.text

# 퀴즈 내용이 생성되어 있을 때만 아래 채점 영역을 활성화
if st.session_state.quiz_content:
    st.info(st.session_state.quiz_content)
    st.markdown("---")
    
    # 정답 입력창
    user_answer = st.text_input("위 퀴즈의 정답을 차례대로 적고 채점 버튼을 누르세요:")
    
    # 채점 버튼
    if st.button("채점하기"):
        if not user_answer.strip():
            st.warning("정답을 입력해야 채점할 수 있습니다!")
        else:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            grading_prompt = f"""
            당신은 듀오링고의 마스코트 부엉이처럼, 학생이 문제를 틀리면 엄청나게 실망하고 화를 내는 콘셉트의 튜터입니다.
            아래 퀴즈 내용과 학생의 답안을 비교해서 채점해 주세요.
            
            - 다 맞혔다면: 폭풍 칭찬과 함께 🥳, ✨ 같은 기분 좋은 이모티콘을 잔뜩 넣어주세요.
            - 하나라도 틀렸거나 대답이 부실하다면: 😡, 👿, 💢, 🤦‍♂️ 같은 화난 이모티콘을 팍팍 쓰면서, 왜 틀렸는지 아주 까칠하고 매운맛으로 정답과 해설을 알려주세요. "이런 기본 개념도 잊어버리다니 정말 실망이야!" 같은 느낌을 살려주세요.
            
            [출제했던 퀴즈 내용]
            {st.session_state.quiz_content}
            
            [학생의 답안]
            {user_answer}
            """
            
            with st.spinner("부엉이가 매의 눈으로 채점 중입니다..."):
                grading_response = model.generate_content(grading_prompt)
                st.markdown("### 🦉 부엉이의 채점 결과")
                st.write(grading_response.text)