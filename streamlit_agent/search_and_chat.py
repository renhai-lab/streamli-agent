import os
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv

from langchain.agents import AgentExecutor, OpenAIFunctionsAgent
from langchain.memory import ConversationBufferMemory
from langchain_community.callbacks import StreamlitCallbackHandler
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_core.messages import SystemMessage
from langchain_core.runnables import RunnableConfig

from langchain_openai import ChatOpenAI

from tools import search, get_contents, find_similar

load_dotenv()

st.set_page_config(page_title="Arc-Agent: Chat with search in Arc and Landscape Area", page_icon="🦜")
st.title("🦜 Arc-Agent")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")

NOW = datetime.now()

tools = [search, get_contents, find_similar]

msgs = StreamlitChatMessageHistory()
memory = ConversationBufferMemory(
    chat_memory=msgs, return_messages=True, memory_key="chat_history", output_key="output"
)
if len(msgs.messages) == 0 or st.sidebar.button("Reset chat history"):
    msgs.clear()
    msgs.add_ai_message("我可以帮你搜索建筑或景观项目，你想知道什么?")
    st.session_state.steps = {}

avatars = {"human": "user", "ai": "assistant"}
for idx, msg in enumerate(msgs.messages):
    with st.chat_message(avatars[msg.type]):
        # Render intermediate steps if any were saved
        for step in st.session_state.steps.get(str(idx), []):
            if step[0].tool == "_Exception":
                continue
            with st.status(f"**{step[0].tool}**: {step[0].tool_input}", state="complete"):
                st.write(step[0].log)
                st.write(step[1])
        st.write(msg.content)

if prompt := st.chat_input(placeholder="上海最近有哪些火爆的景观项目?"):
    st.chat_message("user").write(prompt)


    llm = ChatOpenAI(model="gpt-4o",
                     base_url=OPENAI_BASE_URL,
                     api_key=OPENAI_API_KEY,
                     streaming=True)

    system_message = SystemMessage(
        content="You are a web researcher tasked with answering user questions by looking up information on the internet and retrieving helpful documents. "
                "Please follow these guidelines: "
                "1. Refine your search query as necessary; do not simply convert the user's question into keywords."
                "2. Cite your sources."
                f"3. Current Time: Shanghai {NOW.strftime('%Y-%m-%d %H:%M:%S')}"
    )

    agent_prompt = OpenAIFunctionsAgent.create_prompt(system_message)
    agent = OpenAIFunctionsAgent(llm=llm, tools=tools, prompt=agent_prompt)

    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        memory=memory,
        verbose=True,
        return_intermediate_steps=True,
        handle_parsing_errors=True
    )
    with st.chat_message("assistant"):
        st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
        cfg = RunnableConfig()
        cfg["callbacks"] = [st_cb]
        response = agent_executor.invoke(prompt, cfg)
        st.write(response["output"])
        st.session_state.steps[str(len(msgs.messages) - 1)] = response["intermediate_steps"]
