from zhipuai import ZhipuAI
import streamlit as st
import pandas as pd
import json

client = ZhipuAI(api_key="511e3e7726ab4186a6b14b19f1645c61.hpYNwDoJwAwVHuZM")

#终止对话的标志
TERMINATE_COMMAND = "结束模拟"

if "messages" not in st.session_state:
    # 智谱 AI API 的 messages 格式：[{"role": "user", "content": "你好"}, ...]
    st.session_state["messages"] = []

def get_ai_response(prompt):
    if not client:
        return "无法连接 AI 服务，请检查 API Key。"
        
    try:
        response = client.chat.completions.create(
            model="glm-4",  
            messages=prompt,
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"调用智谱 AI API 失败: {e}")
        return None
    
if __name__ == "__main__":
    
    st.set_page_config(
        page_title="职海探星AI助手", 
        page_icon="", 
        layout="wide", 
    )

    st.markdown(
        """
        <style>
            .stApp {
                background-color: #fff !important;
            }
            body, div, p, span, h1, h2, h3, h4, h5, h6, table, th, td {
                color: #000 !important;
            }
            button, .stButton>button, .stDownloadButton>button {
                background-color: #fff !important;
            }
            div.object-key-val {
                background-color: #fff !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    tab_info, tab_ai = st.tabs(["个人主页", "职海探星AI助手"])

    with tab_info:
        st.markdown('<h1 style="color: #5c307d; text-align:center;">职海探星--AI辅助职业探索沙盒</h1>', unsafe_allow_html=True) # 大标题
        
        st.subheader("个人信息")
        col1, col2 = st.columns([2,5]) 
        col1.image("data/photo.jpg", width=200)
        with col2.container(): 
            col2_1, col2_2 = st.columns(2)
            col2_1.markdown("**姓名**：许瀚元")
            col2_2.markdown("**年龄**：18")
            col2_1, col2_2 = st.columns(2)
            col2_1.markdown("**性别**：男")
            col2_2.markdown("**家乡**：江苏省淮安市")
            col2_1, col2_2 = st.columns(2)
            col2_1.markdown("**学校**：清华大学")
            col2_2.markdown("**专业**：笃实书院")
            col2_1, col2_2 = st.columns(2)
            col2_1.markdown("**爱好**：编程 打篮球 拉小提琴")
            col2_2.markdown("**生日**：20070704")
            col2_1, col2_2 = st.columns(2)
            col2_1.markdown("**Tel**：18800660556")
            col2_2.markdown("**E-Mail**：xhy25@mails.tsinghua.edu.cn")
            col2_1, col2_2 = st.columns(2)
            col2_1.markdown("**地址**：北京市海淀区清华大学紫荆公寓7号楼")
            col2_2.markdown("**我的github**： [fallingstar56](https://github.com/fallingstar56)")

        st.markdown(
            """
            <div style="
            margin-top:40px;
            margin-bottom:0px;
            padding:20px;
            background-color:#f5f3fa;
            border-radius:20px;
            box-shadow:0 2px 8px rgba(92,48,125,0.08);
            text-align:center;
            font-size:18px;
            color:#000;
            ">
            针对对未来感到迷茫、对职业世界认知仅限于名称和薪资的大学新生的需要低成本、高效率试错，了解职业真实面貌的需求，职海探星是一款AI驱动的沉浸式职业情景模拟与规划平台。<br>
            你可以在高度仿真的AI生成的工作场景中处理典型任务、做出决策并获得即时反馈，从而深度理解不同职业所需技能、思维模式和日常工作内容。<br>
            此产品提供了主动的、体验式的探索方式，将抽象的“兴趣”转化为具体的“能力”和“场景”感知，帮助用户基于真实体验而非想象做出更明智的专业和职业选择。
        </div>
        """,
        unsafe_allow_html=True
        )
        
        center_col = st.columns([2, 1, 2])[1]
        with center_col:
            st.image("data/thu.jpg", width=150)
    
    with tab_ai:
        st.markdown('<h1 style="color: #5c307d; text-align:center;">20251106创意软件汇报</h1>', unsafe_allow_html=True) # 大标题
        st.markdown(
            '<p style="font-size: 18px; color: #5c307d; text-align: right; font-weight: bold;">by 许瀚元 笃实56</p>',
            unsafe_allow_html=True
        )
        
        st.markdown(
            '<p style="font-size: 24px; color: #5c307d; text-align: left; font-weight: bold;">职业情景模拟与规划平台</p>',
            unsafe_allow_html=True
        )
        st.markdown("本轮对话以 **“结束模拟”** 终止")
        
        for message in st.session_state["messages"]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                
        if prompt := st.chat_input("输入你感兴趣的问题："):
            if prompt.lower() == TERMINATE_COMMAND:
                st.session_state["messages"] = []
                st.success("对话已终止并清除记录，欢迎进行新一轮的模拟！")
                st.rerun()
            else:
                st.session_state["messages"].append({"role": "user", "content": prompt})
                
                with st.chat_message("user"):
                    st.markdown(prompt)
                    
                with st.chat_message("assistant"):
                    with st.spinner("AI正在思考中..."):
                        full_history = st.session_state["messages"]
                        ai_content = get_ai_response(full_history)
                        
                        if ai_content:
                            st.markdown(ai_content)
                            st.session_state["messages"].append({"role": "assistant", "content": ai_content})   
