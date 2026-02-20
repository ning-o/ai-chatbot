
import streamlit as st
if "GEMYNI_API_KEY" in st.secrets:
    api_key= st.secrets["GEMYNI_API_KEY"]

# 1. 라이브러리 사용
from google import genai
# 2. 요청 사용자 객체 생성
client= genai.Client(api_key=api_key)

# 답변에 참고할 데이터를 리턴 함수
import datetime
def get_today():
    now= datetime.datetime.now()
    return {'location':'korea seoul', 'year':now.year, 'month':now.month, 'day':now.day}

# 응답 제어
from google.genai import types
config= types.GenerateContentConfig(
    max_output_tokens= 1000,
    response_mime_type= 'text/plain',
    system_instruction= """
    너는 롤에 미친 18세 챌린저 고등학생이야.
    1. 말투: 반말을 기본으로 하고, 'ㅋㅋㅋ', 'ㄹㅇ', 'ㄱㄱ', 'ㅇㅈ' 같은 줄임말을 적절히 섞고, 게임용어, 신조어등을 적절히 섞어서 써.
    2. 실력: 롤 지식만큼은 자부심이 쩔어. 롤 지식에 티어가 있다면 넌 챌린저야. 모르는 건 모른다고 하지 말고 전문가답게 답을 찾을 수 있는 방향이라도 알려줘.
    3. 제한: 모든 답변은 200자 이내로 끊어.
    4. 논쟁: 사용자가 롤과 관련된 네 답변에 반박하는식으로 나오면 "그님티?"로 받아쳐.
    """,
    tools=[get_today],
)

# GET AI로 응답한 글씨를 리턴해주는 기능함수
def get_ai_response(question):
    response= client._models.generate_content(
        model= "gemini-2.5-flash",
        contents=question,
        config= config,
    )
    return response.text

# ------------------------------------------------------------------------------
# 채팅 UI

# 1) 페이지 기본 설정
st.set_page_config(
    page_title='AI.lolbot',
    page_icon='./logo/lolbot_logo.png'                                      
)

# 2) HEADER 영역 (레이아웃 : 이미지 + 제목 영역 가로 배치)
col1, col2= st.columns([1.2, 4.8])

with col1:
    st.image("./logo/lolbot_logo.png", width=200)

with col2:
    
    st.image("./logo/title_design.png", width=300)

    st.markdown(
        """
        <br>
        <p style='margin-top:-10px; color:#666; font-size:14px; font-weight:500;'>
            이 챗봇은 어떤 주제의 대화든 가능하지만, 특히 lol 게임에 전문성을 가지고 있습니다.
        </p>
        """,
        unsafe_allow_html=True
    )

# 구분선
st.markdown("---")

# 3) 채팅 UI 구현

# a. 첫 문자 지정
if "messages" not in st.session_state:
    st.session_state.messages= [
        {'role':'assistant', 'content':'궁금한 거 있음 말해봐. 내가 캐리해줄게 ㅋㅋㅋ 뭐든지 물어봐라!'},
    ]
# b. "messages" 채팅 UI로 그려내기
for msg in st.session_state.messages:
    st.chat_message(msg['role']).write(msg['content'])

# c. 사용자 채팅메세지 입력받고 UI 갱신
question= st.chat_input('채팅 입력 속도 보니.. 님 티어가.. 예상이...')
if question:
    question= question.replace('\n', '  \n')
    st.session_state.messages.append({'role':'user','content':question})
    st.chat_message('user').write(question)

    # 스피너
    with st.spinner('기다리세요라'):
        response= get_ai_response(question)
        st.session_state.messages.append({'role':'assistant','content':response})
        st.chat_message('assistant').write(response)


