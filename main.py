import streamlit as st
import pandas as pd
from openai import OpenAI
import warnings
warnings.filterwarnings('ignore')
client = OpenAI(api_key="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")
st.set_page_config(layout="wide",
                   page_title='생성 AI를 사용한 홍보 문구 생성기',
                   initial_sidebar_state="expanded")


col1, col2 = st.columns(2)
model = st.sidebar.selectbox(
    "Model",
    ("gpt-3.5-turbo-0125", "gpt-4-0125-preview")
)
lan = st.sidebar.selectbox(
    " ",
    ("KR", "EN")
)

if lan == "EN":
    csv_path = './EN.csv'
    df = pd.read_csv(csv_path)

if lan=='KR':
    csv_path = './KR.csv'
    df = pd.read_csv(csv_path, encoding='cp949')

if model == "gpkt-3.5-turbo-0125":
    st.write("저의 크레딧을 지켜주세요... 🙏")
    st.stop()
    
with col1:
    prompts = []
    for j in range(len(df)):
        if df['Default'][j] == 0:
            prompts.append(st.sidebar.checkbox(df['Prompt'][j]))
        else:
            prompts.append(st.sidebar.checkbox(df['Prompt'][j],value=True))
    inputs = {}
    for i in range(len(df)):
        if (df['Need input'][i] == 1) & prompts[i]:
            inputs[df['Prompt'][i]] = st.text_input(df['Full text'][i], value=df['Default input'][i])


    final_prompt = ""

    st.write('### 프롬프트 생성 결과')


    for i in range(len(df)):
        if prompts[i]:
            if df['Need input'][i] == 1:
                if inputs[df["Prompt"][i]]:
                    if df['Quote'][i] == 1:
                        final_prompt += df['Prefix'][i] +'"'+ inputs[df["Prompt"][i]] +'"'+ df["Suffix"][i] + ' '
                        
                    else:
                        final_prompt += df['Prefix'][i] +  inputs[df["Prompt"][i]] + df["Suffix"][i] + ' '
            else:
                final_prompt += df["Full text"][i] + '. '
            final_prompt+='  \n'
    prompt = final_prompt
    st.write(final_prompt)

    st.button("생성하기", type="primary", key='pressed')
    st.button("초기화", type="primary", key='reset')


with col2:

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo-0125"

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    if st.session_state.get('reset'):
        st.session_state.messages = []
        st.session_state["openai_model"] = model
        st.rerun()

    if st.session_state.get('pressed'):

        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
        del st.session_state['pressed']


    if prompt2:= st.chat_input("프롬프트를 입력하세요"):
        st.session_state.messages.append({"role": "user", "content": prompt2})

        with st.chat_message("user"):
            st.markdown(prompt2)        
        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
        del prompt2
        








