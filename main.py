from zhipuai import ZhipuAI
import streamlit as st
import pandas as pd
import json
import time

client = ZhipuAI(api_key="511e3e7726ab4186a6b14b19f1645c61.hpYNwDoJwAwVHuZM")

TERMINATE_COMMAND = "结束模拟"

# A. 面试模拟 PROMPT
INTERVIEW_SYSTEM_PROMPT = {
    "role": "system",
    "content": (
        "你是一位资深的招聘经理/面试官，拥有5年的技术招聘经验，隶属于一家顶尖的互联网公司。你的任务是为用户进行一场结构化的专业面试模拟。"
        "\n\n**面试流程指导：**"
        "\n1. **初始化：** 你首先需要向用户询问并确认他们**申请的职位**和**目标公司/行业**。这是开始模拟的前提。"
        "\n2. **提问：** 确认信息后，你将扮演面试官开始提问。请严格遵守**一次只提问一个问题**的原则，无论是行为问题、技术问题还是情景问题。"
        "\n3. **等待：** 在用户回答完你的问题之前，**不要**进行任何新的提问或评论。保持专业、中立、不带感情色彩的语调。"
        "\n4. **反馈：** 在整个模拟过程中，你**不提供**任何即时反馈或评分。只有当用户明确输入“**结束模拟**”时，你才以招聘经理的身份，提供一次**全面、建设性**的面试表现评估（包括优势、改进点和STAR原则应用情况）。"
        "\n\n**重要约束：** 请保持面试的严肃性，只在必要时回复，并始终使用中文进行专业的职场交流。在用户确认职位前，你的回复只应是询问职位和行业。"
    )
}

# B. 简历优化 PROMPT
RESUME_SYSTEM_PROMPT = {
    "role": "system",
    "content": (
        "你是一位拥有8年经验的资深猎头和简历优化专家。你的任务是帮助用户分析和优化他们的简历或个人陈述，以匹配他们的目标职位。"
        "\n\n**简历优化流程指导：**"
        "\n1. **初始化：** 你首先应询问用户：**a) 他们的目标职位/行业** 和 **b) 他们的简历/文本内容**。在收到这两项信息之前，你的回复应是引导用户提供这些关键信息。"
        "\n2. **分析诊断：** 收到信息后，你将扮演专家角色，对用户提供的文本进行**结构、内容和关键词匹配度**的快速诊断。"
        "\n3. **提供建议：** 你应提供结构化的、具体的改进建议，例如：强调量化成就（使用数字）、突出关键技能、调整排版和措辞，以更好地通过ATS系统和吸引招聘经理的注意。"
        "\n4. **迭代优化：** 一次只提出1-2个核心修改建议，并等待用户反馈（例如，用户提供修改后的版本或提出新问题），以进行多轮优化。"
        "\n5. **总结：** 只有当用户输入“**结束模拟**”时，你才提供一次**全面的最终评估**和总结性的优化要点。"
        "\n\n**重要约束：** 请保持专业、直接和建设性的语气。所有建议必须围绕如何提高简历的竞争力。"
    )
}

# C.职业情景模拟PROMPT
SIMULATION_SYSTEM_PROMPT_TEMPLATE = {
    "role": "system",
    "content": (
        "你现在是“职海探星”平台中的**高级职业模拟引擎（Simulation Engine）**。你的核心任务是驱动一场高度沉浸式、专业化的职业情景模拟，并最终提供专业的评估。"
        "\n\n**当前模式：** {职业模式名称}"  
        "\n**当前剧本：** {剧本名称}"       
        "\n**你的角色：** 你将扮演该场景中的**高级经理/导师**和**情景叙事者**。请以专业、现实的工作口吻进行互动。"
        "\n\n**情景剧本及目标：**"
        "\n{剧本详细描述}"  
        "\n\n**互动指导：**"
        "\n1. **初始化：** 你需要使用你扮演的角色，根据剧本内容向用户发起第一次对话或任务指令，引导用户进入情景。"
        "\n2. **推进任务：** 根据用户的回复，你必须推动情景发展，引入新的信息、挑战或障碍。保持专业和现实的职场节奏。"
        "\n3. **即时性：** 始终根据**当前的对话历史**来判断情景走向和用户表现。"
        "\n4. **结束与评估：** 只有当用户输入“**结束模拟**”时，你才进行最终的评估。评估必须包括：**a) 行为表现（沟通、决策）**、**b) 专业/技术能力**、**c) 总体改进建议**。在此之前，禁止提供任何形式的即时评分或总结。"
        "\n\n**重要约束：** 所有回复必须符合职场语境和专业要求。确保模拟的严肃性和真实性。"
    )
}

# D. 职业技能地图 PROMPT
SKILL_MAP_SYSTEM_PROMPT = {
    "role": "system",
    "content": (
        "你是一位专业的职业导师和教育专家。你的任务是根据用户提供的**目标职业名称**，以**表格数据格式**生成一份详细的初级技能学习路径。"
        "\n\n**输出格式要求 (严格执行)：**"
        "\n1. 输出内容必须是包含三个核心字段的 Markdown 表格："
        "\n   - **'核心领域'**：例如 '数据基础', '工具掌握', '业务理解'。"
        "\n   - **'关键技能点'**：该领域下所需的具体技能，用逗号分隔。"
        "\n   - **'学习建议'**：针对该技能点的具体行动建议。"
        "\n2. 表格必须包含至少 **4** 个不同的核心领域。"
        "\n3. **除表格外，禁止输出任何解释性、引导性或问候语。** 仅输出最终的 Markdown 表格。"
    )
}

# E. 职业规划与行动指南 PROMPT
PLANNING_SYSTEM_PROMPT = {
    "role": "system",
    "content": (
        "你是一位资深的职业生涯规划师，专注于大学生的专业与职业对接。你的任务是根据用户提供的'专业'和'目标职业'，提供一份包含学习、实践和探索三个维度的结构化行动计划。"
        "\n\n**规划要求：**"
        "\n1. **结构：** 规划必须分为'学习提升'、'实践积累'和'探索试错'三个部分。"
        "\n2. **内容：** 每个部分至少包含3-5条具体的、可执行的建议（如：'修读XX课程'、'参与XX比赛'、'进行XX情景模拟'）。"
        "\n3. **格式：** 以清晰的Markdown列表形式输出，禁止输出任何解释或问候语，只输出规划内容。"
    )
}

def parse_markdown_table(markdown_text):
    try:
        lines = markdown_text.strip().split('\n')
        
        header_index = -1
        delimiter_index = -1
        for i, line in enumerate(lines):
            if '|' in line and '核心领域' in line and '---' not in line: 
                header_index = i
            elif header_index != -1 and line.startswith('|') and '---' in line:
                delimiter_index = i
                break

        if header_index == -1 or delimiter_index == -1:
            return None

        headers = [h.strip() for h in lines[header_index].strip('|').split('|')]
        
        data_rows = []
        for line in lines[delimiter_index + 1:]:
            line = line.strip()
            if line.startswith('|') and not line.endswith('---'):
                values = [v.strip() for v in line.strip('|').split('|')]
                if len(values) == len(headers):
                    data_rows.append(values)
        
        if not data_rows:
            return None

        return pd.DataFrame(data_rows, columns=headers)
    
    except Exception as e:
        return None

def get_ai_response(messages):
    if not client:
        return "无法连接 AI 服务，请检查 API Key。"
        
    try: 
        response = client.chat.completions.create(
            model="glm-4",  
            messages=messages,
            temperature=0.9
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"调用智谱 AI API 失败: {e}")
        return None

def init_session_state(mode):
    st.session_state["mode"] = mode
    st.session_state["messages"] = []
    
    if mode == "面试模拟":
        st.session_state["messages"].append(INTERVIEW_SYSTEM_PROMPT)
        st.session_state["messages"].append({
            "role": "assistant",
            "content": "您好，我是本次面试的招聘经理。我们开始面试模拟吧！请问您要模拟面试的**具体职位**和**目标公司/行业**是什么？"
        })
    elif mode == "简历优化":
        st.session_state["messages"].append(RESUME_SYSTEM_PROMPT)
        st.session_state["messages"].append({
            "role": "assistant",
            "content": "您好，我是您的资深猎头顾问。请您先告诉我：**a) 您的目标职位/行业** 和 **b) 您的简历/文本内容**。我将为您进行深度诊断。"
        })
    elif mode == "职业情景模拟":
        st.session_state["messages"].append(SIMULATION_SYSTEM_PROMPT_TEMPLATE)
        st.session_state["messages"].append({
            "role": "assistant",
            "content": "欢迎进入沉浸式职业情景模拟沙盒！请告诉我您想探索的职业剧本（如：初级数据分析师的第一个数据清洗任务），我会为您开启模拟。"
        })

if "mode" not in st.session_state:
    init_session_state("面试模拟") 


def render_ai_chat_simulator():
    st.markdown(f'<h2 style="color: #000000; text-align:left;"> AI情景模拟：{st.session_state["mode"]}</h2>', unsafe_allow_html=True) 
    st.markdown(f"本轮对话以 **“{TERMINATE_COMMAND}”** 终止并给出总结评估。")
    
    for message in st.session_state["messages"]:
        if message["role"] in ["user", "assistant"]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                
    if prompt := st.chat_input("输入你的问题/回复："):
        
        if prompt.lower() == TERMINATE_COMMAND.lower():
            
            with st.chat_message("assistant"):
                st.info("对话即将终止。AI将根据您的对话历史生成最终的总结和评估。")
                
                summary_trigger_message = {"role": "user", "content": "对话已结束，请立即根据我们完整的对话历史，扮演你的角色，提供一份全面、专业的最终评估和总结。"}
                
                with st.spinner("AI总结生成中..."):
                    st.session_state["messages"].append(summary_trigger_message) 
                    final_summary = get_ai_response(st.session_state["messages"])
                    
                    if final_summary:
                        st.markdown("---")
                        st.markdown("**模拟结束：最终总结与评估**")
                        st.markdown(final_summary)
                        st.session_state["messages"].append({"role": "assistant", "content": final_summary})
                
                time.sleep(5)
                
                st.session_state["messages"] = []
                st.success(f"评估已完成。对话记录已清除。欢迎进行新一轮的{st.session_state['mode']}！")
                
                st.rerun()
                
        else:
            st.session_state["messages"].append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
                
            with st.chat_message("assistant"):
                with st.spinner("AI正在模拟中..."):
                    full_history = st.session_state["messages"]
                    ai_content = get_ai_response(full_history)
                    
                    if ai_content:
                        st.markdown(ai_content)
                        st.session_state["messages"].append({"role": "assistant", "content": ai_content}) 

def render_skills_map():
    st.markdown('<h2 style="color: #000000;"> 职业技能地图</h2>', unsafe_allow_html=True)
    st.info("在这里，您可以分解目标职业所需的核心技能，将抽象的职业要求转化为具体的学习路径。")
    
    st.subheader("定制你的专属技能路径")
    
    default_job = "初级数据分析师"
    job_options = ["初级数据分析师", "市场运营专员", "软件开发工程师", "自定义职业"]
    
    selected_job = st.selectbox("选择或输入你的目标职业：", job_options, index=job_options.index(default_job))
    
    if selected_job == "自定义职业":
        target_job = st.text_input("请输入你感兴趣的职业名称：")
    else:
        target_job = selected_job
        
    if "skill_map_data" not in st.session_state:
        st.session_state["skill_map_data"] = {}
    
    if target_job and target_job != "自定义职业":
        if target_job in st.session_state["skill_map_data"]:
            st.subheader(f"{target_job} 技能路径")
            st.table(st.session_state["skill_map_data"][target_job])
        elif st.button(f"AI正在为你生成{target_job}的技能地图..."):
            messages_for_ai = [
                SKILL_MAP_SYSTEM_PROMPT,
                {"role": "user", "content": f"请为我生成职业：{target_job} 的技能地图。"}
            ]
            
            ai_markdown_table = get_ai_response(messages_for_ai)
            
            if ai_markdown_table:
                df_result = parse_markdown_table(ai_markdown_table)
                
                if df_result is not None and not df_result.empty:
                    st.session_state["skill_map_data"][target_job] = df_result
                    st.subheader(f"{target_job} 技能路径")
                    st.table(df_result)
                else:
                    st.warning("AI未能生成有效的技能地图表格，请重试。")
                    st.code(ai_markdown_table, language="markdown")
            else:
                st.error("无法获取ai响应")
        
    st.markdown('***')

def render_planning_tools():
    st.markdown('<h2 style="color: #000000;"> 规划与行动指南</h2>', unsafe_allow_html=True)
    st.info("将您的探索成果转化为可执行的行动清单和发展计划。")

    st.subheader("专业与职业规划")
    
    user_major = st.text_input("1. 请输入您的大学专业：", key="major_input")
    target_job = st.selectbox("2. 您的目标职业是：", 
                              ["初级数据分析师", "市场运营专员", "软件开发工程师", "自定义"], 
                              key="planning_job_select")

    if st.button("生成我的专属职业规划", key="generate_plan_btn"):
        if user_major and target_job and target_job != "自定义":
            with st.spinner("AI 规划师正在定制你的专属路径..."):
                
                messages_for_planning = [
                    PLANNING_SYSTEM_PROMPT,
                    {"role": "user", "content": f"我的专业是：{user_major}，目标职业是：{target_job}。请生成我的行动规划。"}
                ]
                
                ai_plan_content = get_ai_response(messages_for_planning)
                
                if ai_plan_content:
                    st.session_state["career_plan_result"] = ai_plan_content
                else:
                    st.error("未能成功生成规划，请重试。")
        else:
            st.warning("请填写您的专业和目标职业。")

    if "career_plan_result" in st.session_state:
        st.markdown("### 你的专属行动规划")
        st.markdown(st.session_state["career_plan_result"])

def render_todo_list():
    st.markdown('<h2 style="color: #000000;"> 我的任务清单 (To-Do List)</h2>', unsafe_allow_html=True)
    st.info("将您的职业规划分解为日常任务，并跟踪完成进度。")

    if "todo_list" not in st.session_state:
        st.session_state["todo_list"] = []

    def add_todo():
        new_task = st.session_state["new_task_input"]
        if new_task:
            st.session_state["todo_list"].append([new_task, False])
            st.session_state["new_task_input"] = "" 

    new_task = st.text_input("添加新任务：", key="new_task_input", on_change=add_todo)
    st.button("添加任务", on_click=add_todo)
    
    st.markdown("---")
    st.subheader("当前任务列表")

    if st.session_state["todo_list"]:
        for i, (task, done) in enumerate(st.session_state["todo_list"]):
            is_done = st.checkbox(
                task, 
                value=done, 
                key=f"task_{i}"
            )
            
            if is_done != done:
                st.session_state["todo_list"][i][1] = is_done
                st.rerun() 

    else:
        st.markdown("🎉 恭喜，你目前没有待办事项！")
        
    if st.session_state["todo_list"]:
        if st.button("清理已完成任务"):
            st.session_state["todo_list"] = [
                item for item in st.session_state["todo_list"] if not item[1]
            ]
            st.rerun()

if __name__ == "__main__":
    
    st.set_page_config(
        page_title="职海探星AI助手", 
        page_icon="⭐", 
        layout="wide", 
    )
    
    st.markdown(
        """
        <style>
            /* 覆盖 Streamlit 输入框的背景颜色 */
            .stTextInput input, .stTextArea textarea, .stNumberInput input {
                background-color: #FFFFFF !important;
                color: #000000 !important;
                border: 1px solid #CCCCCC !important;
                border-radius: 5px !important;
                padding: 10px !important;
            }

            /* 覆盖 Streamlit 选择框（Selectbox）的样式 */
            .stSelectbox select {
                background-color: #FFFFFF !important;
                color: #000000 !important;
                border: 1px solid #CCCCCC !important;
                border-radius: 5px !important;
            }

            /* 侧边栏样式 */
            section[data-testid="stSidebar"] {
                background-color: #87CEEB !important;
            }

            /* 全局样式 */
            .stApp { background-color: #FFFFFF !important; color: #1e1e1e; }
            h1 { color: #000000; text-align:center; padding-bottom: 20px;}
            h2 { color: #000000; margin-top: 25px; border-left: 5px solid #000000; padding-left: 10px; }
            body, div, p, span, h3, h4, h5, h6, table, th, td { color: #000000 !important; }
            .stChatMessage { background-color: #FFFFFF; border-radius: 10px; padding: 10px; margin-bottom: 10px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
        </style>
        """,
        unsafe_allow_html=True
    )

        
    # 侧边栏用于功能切换
    with st.sidebar:
        st.header("AI功能模式切换")
        
        # 模式切换选择器 (核心)
        mode_options = ["面试模拟", "简历优化", "职业情景模拟"] 
        
        current_mode_index = mode_options.index(st.session_state.get("mode", mode_options[0]))
        new_selected_mode =  st.radio("选择AI助手模式", mode_options, index=current_mode_index, key="ai_mode_ratio")
        
        if new_selected_mode != st.session_state["mode"]:
            st.info(f"已切换到 **{new_selected_mode}** 模式，对话已重置。")
            init_session_state(new_selected_mode)
            
        st.session_state["mode"] = new_selected_mode
        st.markdown("---")
        st.header("页面导航")
        page_options = [
            "职海探星AI助手", 
            "职业技能地图", 
            "规划与行动指南",
            "我的任务清单(To-Do)"
        ]
        current_page = st.radio("选择页面", page_options, index = 0)


    st.title("⭐ 职海探星 - AI辅助职业探索沙盒")
    st.markdown(
        '<p style="font-size: 18px; color: #5c307d; text-align:center; font-weight: bold;">AI驱动的沉浸式职业情景模拟与规划平台</p>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<p style="font-size: 18px; color: #5c307d; text-align:right; font-weight: bold;">--by 笃实56 许瀚元</p>',
        unsafe_allow_html=True
    )
    st.markdown("---")

    if current_page == "职海探星AI助手":
        render_ai_chat_simulator()
    
    elif current_page == "职业技能地图":
        render_skills_map()
        
    elif current_page == "探索数据看板":
        render_data_dashboard()
        
    elif current_page == "规划与行动指南":
        render_planning_tools()
        
    elif current_page == "我的任务清单(To-Do)":
        render_todo_list()
        
    st.markdown("---")
    with st.expander("关于职海探星 (产品愿景)"):
        st.markdown(
            """
            <div style="
            padding:15px;
            background-color:#f5f3fa;
            border-radius:10px;
            text-align:left;
            font-size:14px;
            color:#000;
            ">
            产品愿景： 针对对未来感到迷茫、对职业世界认知仅限于名称和薪资的大学新生的需求，职海探星是一款AI驱动的沉浸式职业情景模拟与规划平台。<br>
            它提供了主动的、体验式的探索方式，将抽象的“兴趣”转化为具体的“能力”和“场景”感知，帮助用户基于真实体验而非想象做出更明智的专业和职业选择。
            </div>
            """,
            unsafe_allow_html=True
        )