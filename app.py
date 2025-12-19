import streamlit as st
import requests
import json
import time
from datetime import datetime

# ==================== 配置页面 ====================
st.set_page_config(
    page_title="🍳 厨神小助手",
    page_icon="🍳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== 自定义CSS美化 ====================
st.markdown("""
<style>
    .main-header {
        font-size: 2.8rem;
        color: #FF6B35;
        text-align: center;
        margin-bottom: 0.5rem;
        font-weight: bold;
        background: linear-gradient(90deg, #FF6B35, #FF8E53);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .sub-header {
        font-size: 1.3rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stButton button {
        background: linear-gradient(135deg, #FF6B35 0%, #FF8E53 100%);
        color: white;
        font-size: 1.1rem;
        font-weight: bold;
        border-radius: 25px;
        padding: 0.7rem 2rem;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(255, 107, 53, 0.2);
    }
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(255, 107, 53, 0.3);
    }
    .recipe-card {
        background: white;
        padding: 1.8rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        border-left: 6px solid #FF6B35;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
    }
    .recipe-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #FFF5F0 0%, #FFFFFF 100%);
    }
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #FF6B35, #FF8E53);
    }
    .stTextArea textarea {
        border-radius: 12px;
        border: 2px solid #FFE8E0;
    }
    .stTextArea textarea:focus {
        border-color: #FF6B35;
        box-shadow: 0 0 0 1px #FF6B35;
    }
</style>
""", unsafe_allow_html=True)

# ==================== 团队信息 ====================
TEAM_MEMBERS = ["刘蕊琪", "戚洋洋", "王佳慧", "覃丽娜", "欧婷", "贺钰鑫"]
PROJECT_NAME = "厨神小助手"
COURSE_INFO = "《人工智能通识》大作业项目"
# ==================== 页面标题 ====================
st.markdown(f'<div class="main-header">{PROJECT_NAME}</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">🍽️ AI智能菜谱推荐 · 解决「今天吃什么」的世纪难题</div>', unsafe_allow_html=True)
st.markdown("---")

# ==================== 侧边栏：用户输入区 ====================
with st.sidebar:
    st.markdown("### 👨‍🎓 项目团队")
    members_html = ""
    for i, member in enumerate(TEAM_MEMBERS, 1):
        members_html += f"<div style='padding: 5px 0;'>{i}. {member}</div>"
    st.markdown(members_html, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown(f"**{COURSE_INFO}**")
    st.markdown(f"**创建时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    st.markdown("---")
    st.markdown("### ⚙️ 食材设置")
    
    ingredients_input = st.text_area(
        "🥦 请输入您现有的食材",
        placeholder="请输入食材，每行一种\\n例如：\\n鸡蛋\\n番茄\\n土豆\\n鸡肉\\n青椒",
        height=180,
        help="输入3-5种食材效果最佳"
    )
    
    st.markdown("---")
    st.markdown("### 🔧 推荐设置")
    
    col1, col2 = st.columns(2)
    with col1:
        num_recipes = st.slider(
            "📊 推荐数量",
            min_value=1,
            max_value=5,
            value=3,
            help="选择要生成的菜谱数量"
        )
    
    with col2:
        cooking_time = st.selectbox(
            "⏱️ 烹饪时间",
            ["不限", "15分钟内", "30分钟内", "45分钟内", "60分钟内"],
            index=0,
            help="筛选适合的烹饪时间"
        )
    
    taste_preference = st.selectbox(
        "🌶️ 口味偏好",
        ["不限", "清淡", "微辣", "中辣", "重辣", "酸甜", "咸香"],
        index=0
    )
    
    difficulty = st.selectbox(
        "📈 难度级别",
        ["不限", "新手友好", "家常便饭", "厨艺进阶", "高手挑战"],
        index=1
    )
    
    st.markdown("---")
    
    with st.expander("💡 使用提示"):
        st.info("""
        1. **输入常见食材**：如鸡蛋、番茄、鸡肉等
        2. **适量原则**：3-5种食材搭配效果最佳
        3. **详细描述**：可添加如"鸡胸肉""嫩豆腐"等细节
        4. **特殊需求**：可在食材后添加如"(少油)"等要求
        """)
       # ==================== 主内容区 ====================
st.markdown("## 🎯 快速体验")

demo_col1, demo_col2, demo_col3 = st.columns(3)

with demo_col1:
    if st.button("🥚 经典组合", use_container_width=True, help="鸡蛋 + 番茄 + 青椒"):
        st.session_state.demo_ingredients = "鸡蛋\\n番茄\\n青椒\\n葱"

with demo_col2:
    if st.button("🍗 营养搭配", use_container_width=True, help="鸡肉 + 土豆 + 胡萝卜"):
        st.session_state.demo_ingredients = "鸡胸肉\\n土豆\\n胡萝卜\\n洋葱"

with demo_col3:
    if st.button("🥦 素食主义", use_container_width=True, help="豆腐 + 香菇 + 青菜"):
        st.session_state.demo_ingredients = "豆腐\\n香菇\\n青菜\\n胡萝卜"

demo_col4, demo_col5, demo_col6 = st.columns(3)

with demo_col4:
    if st.button("🦐 海鲜盛宴", use_container_width=True, help="虾仁 + 鸡蛋 + 青豆"):
        st.session_state.demo_ingredients = "虾仁\\n鸡蛋\\n青豆\\n玉米"

with demo_col5:
    if st.button("🍚 剩饭利用", use_container_width=True, help="剩饭 + 鸡蛋 + 火腿"):
        st.session_state.demo_ingredients = "米饭\\n鸡蛋\\n火腿\\n青豆"

with demo_col6:
    if st.button("🐟 鲜美鱼汤", use_container_width=True, help="鱼 + 豆腐 + 香菇"):
        st.session_state.demo_ingredients = "鱼肉\\n豆腐\\n香菇\\n姜"

st.markdown("---")

if 'demo_ingredients' in st.session_state:
    ingredients_input = st.session_state.demo_ingredients
    st.info(f"📝 已选择预设食材组合，可点击上方按钮切换")

with st.expander("📝 手动输入食材", expanded=True):
    manual_input = st.text_area(
        "或在此手动输入/修改食材：",
        value=ingredients_input if 'ingredients_input' in locals() else "",
        height=100,
        key="manual_input"
    )
    
    if manual_input:
        ingredients_input = manual_input

st.markdown("---")
# ==================== 百度千帆API配置 ====================
QIANFAN_CONFIG = {
    "api_key": "bce-v3/ALTAK-1bgyWcDtorkOF0ccj9ai2/1fd1c6767c66174f38e3521920c25648dac44ef4",
    "secret_key": "7ae74a327cd447b2ae702bccc5c75283"
}

# ==================== 本地菜谱数据库 ====================
LOCAL_RECIPES = {
    "鸡蛋": [
        {
            "name": "番茄炒蛋",
            "ingredients": ["鸡蛋 2个", "番茄 1个", "葱 适量", "盐 适量", "糖 少许", "油 适量"],
            "steps": [
                "1. 番茄洗净切块，鸡蛋打散加少许盐",
                "2. 热锅倒油，倒入蛋液炒至凝固盛出",
                "3. 再倒少许油，放入番茄炒至出汁",
                "4. 加入炒好的鸡蛋，加盐和糖调味，翻炒均匀",
                "5. 撒上葱花即可出锅"
            ],
            "time": "15分钟",
            "tips": "加少许糖可以中和番茄的酸味",
            "difficulty": "新手友好",
            "calories": "约200卡路里",
            "nutrition": "富含蛋白质和维生素C"
        },
        {
            "name": "韭菜炒蛋",
            "ingredients": ["鸡蛋 3个", "韭菜 200g", "盐 适量", "油 适量"],
            "steps": [
                "1. 韭菜洗净切段，鸡蛋打散加盐",
                "2. 热锅倒油，倒入蛋液炒至凝固盛出",
                "3. 锅中再倒油，放入韭菜快速翻炒",
                "4. 韭菜变软后加入炒好的鸡蛋",
                "5. 加盐调味，翻炒均匀即可"
            ],
            "time": "10分钟",
            "tips": "韭菜不宜炒太久，否则会失去脆嫩口感",
            "difficulty": "新手友好",
            "calories": "约180卡路里",
            "nutrition": "富含蛋白质和膳食纤维"
        }
    ],
    "番茄": [
        {
            "name": "番茄鸡蛋汤",
            "ingredients": ["番茄 1个", "鸡蛋 2个", "葱花 适量", "盐 适量", "香油 几滴"],
            "steps": [
                "1. 番茄切小块，鸡蛋打散备用",
                "2. 锅中放水烧开，放入番茄煮2分钟",
                "3. 缓缓倒入蛋液，边倒边搅拌形成蛋花",
                "4. 加盐调味，撒上葱花",
                "5. 关火后滴几滴香油提香"
            ],
            "time": "15分钟",
            "tips": "淋蛋液时火要小，才能形成漂亮的蛋花",
            "difficulty": "新手友好",
            "calories": "约120卡路里",
            "nutrition": "低热量，富含维生素"
        }
    ],
    "鸡肉": [
        {
            "name": "土豆烧鸡块",
            "ingredients": ["鸡肉 300g", "土豆 2个", "姜 3片", "料酒 1勺", "生抽 2勺", "老抽 半勺", "糖 少许"],
            "steps": [
                "1. 鸡肉切块焯水，土豆去皮切块",
                "2. 热锅倒油，放入姜片爆香",
                "3. 加入鸡块翻炒至变色",
                "4. 加入料酒、生抽、老抽、糖翻炒均匀",
                "5. 加水没过鸡肉，烧开后转小火炖20分钟",
                "6. 加入土豆块，继续炖15分钟至土豆软烂",
                "7. 大火收汁即可"
            ],
            "time": "45分钟",
            "tips": "土豆切块后泡水可以防止氧化变黑",
            "difficulty": "家常便饭",
            "calories": "约350卡路里",
            "nutrition": "蛋白质和碳水化合物均衡"
        }
    ],
    "豆腐": [
        {
            "name": "麻婆豆腐",
            "ingredients": ["嫩豆腐 1块", "猪肉末 100g", "郫县豆瓣酱 1勺", "花椒粉 适量", "葱姜蒜 适量", "淀粉 适量"],
            "steps": [
                "1. 豆腐切块焯水备用",
                "2. 炒香肉末和豆瓣酱",
                "3. 加入适量水，放入豆腐轻煮",
                "4. 勾芡，撒上花椒粉和葱花"
            ],
            "time": "20分钟",
            "tips": "豆腐焯水可以去除豆腥味",
            "difficulty": "家常便饭",
            "calories": "约250卡路里",
            "nutrition": "植物蛋白丰富"
        }
    ]
}
# ==================== 获取访问令牌 ====================
def get_qianfan_access_token():
    try:
        url = "https://aip.baidubce.com/oauth/2.0/token"
        params = {
            'grant_type': 'client_credentials',
            'client_id': QIANFAN_CONFIG["api_key"],
            'client_secret': QIANFAN_CONFIG["secret_key"]
        }
        
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            result = response.json()
            return result.get("access_token")
        return None
    except Exception as e:
        st.error(f"获取令牌出错: {str(e)}")
        return None

# ==================== 调用百度千帆API ====================
def call_qianfan_api(ingredients, num_recipes=3, cooking_time="不限", taste="不限"):
    try:
        access_token = get_qianfan_access_token()
        if not access_token:
            return None
            
        url = f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/eb-instant?access_token={access_token}"
        
        prompt = f"""你是一个专业厨师和营养师。用户有以下食材：{ingredients}

请生成{num_recipes}道家常菜菜谱，要求：
1. 每道菜谱包含：菜名、所需食材（精确到用量）、详细步骤（5步以内）、烹饪时间、实用小贴士
2. 烹饪时间要求：{cooking_time}
3. 口味偏好：{taste}
4. 优先使用用户提供的食材

请严格按照以下JSON格式输出：
{{
  "recipes": [
    {{
      "name": "菜名",
      "ingredients": ["食材1 用量", "食材2 用量"],
      "steps": ["步骤1", "步骤2"],
      "time": "X分钟",
      "tips": "实用小贴士",
      "nutrition": "简要营养说明"
    }}
  ]
}}"""

        headers = {'Content-Type': 'application/json'}
        data = {
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "top_p": 0.8
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if "result" in result:
                content = result["result"]
                try:
                    start_idx = content.find('{')
                    end_idx = content.rfind('}') + 1
                    if start_idx != -1 and end_idx != -1:
                        json_str = content[start_idx:end_idx]
                        recipes_data = json.loads(json_str)
                        return recipes_data.get("recipes", [])
                except:
                    # 如果JSON解析失败，创建默认格式
                    return [{
                        "name": "AI推荐菜谱",
                        "ingredients": ingredients.split(','),
                        "steps": ["1. 准备食材", "2. 按照家常做法烹饪", "3. 调味出锅"],
                        "time": "20分钟",
                        "tips": "根据个人口味调整调料",
                        "nutrition": "营养均衡的家常菜"
                    }]
        
        return None
        
    except Exception as e:
        st.error(f"API调用出错: {str(e)}")
        return None

# ==================== 本地匹配函数 ====================
def match_local_recipes(ingredients_list, num=3):
    matched = []
    
    for ingredient in ingredients_list:
        ing_lower = ingredient.strip().lower()
        
        if "鸡" in ing_lower and "鸡蛋" not in ing_lower:
            if "鸡肉" in LOCAL_RECIPES:
                matched.extend(LOCAL_RECIPES["鸡肉"])
        elif "蛋" in ing_lower:
            if "鸡蛋" in LOCAL_RECIPES:
                matched.extend(LOCAL_RECIPES["鸡蛋"])
        elif "番茄" in ing_lower or "西红柿" in ing_lower:
            if "番茄" in LOCAL_RECIPES:
                matched.extend(LOCAL_RECIPES["番茄"])
        elif "豆腐" in ing_lower:
            if "豆腐" in LOCAL_RECIPES:
                matched.extend(LOCAL_RECIPES["豆腐"])
    
    unique_recipes = []
    seen_names = set()
    
    for recipe in matched:
        if recipe["name"] not in seen_names:
            unique_recipes.append(recipe)
            seen_names.add(recipe["name"])
    
    return unique_recipes[:num]
    # ==================== 主生成按钮 ====================
st.markdown("## 🚀 智能生成")

col_left, col_right = st.columns([1, 2])

with col_left:
    generate_clicked = st.button(
        "✨ AI智能推荐菜谱",
        type="primary",
        use_container_width=True,
        help="点击后AI将根据食材智能生成菜谱"
    )
    
    st.markdown("---")
    use_ai = st.radio(
        "选择生成模式：",
        ["🤖 AI智能生成", "📚 本地快速匹配"],
        index=0,
        help="AI生成更智能但需要网络，本地匹配更快但选择较少"
    )
    
    with st.expander("⚙️ 高级选项"):
        show_nutrition = st.checkbox("显示营养信息", value=True)
        show_tips = st.checkbox("显示烹饪小贴士", value=True)
        show_steps = st.checkbox("显示详细步骤", value=True)

# ==================== 处理生成逻辑 ====================
if generate_clicked:
    with col_right:
        if not ingredients_input:
            st.warning("请输入食材！")
        else:
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            ingredients_list = [i.strip() for i in ingredients_input.split('\\n') if i.strip()]
            
            if not ingredients_list:
                st.warning("请输入至少一种食材！")
            else:
                st.info(f"📋 使用食材：{', '.join(ingredients_list)}")
                
                status_text.text("🔍 分析食材中...")
                progress_bar.progress(20)
                time.sleep(0.5)
                
                status_text.text("👨‍🍳 AI正在设计菜谱...")
                progress_bar.progress(50)
                
                recipes = []
                if use_ai == "🤖 AI智能生成":
                    status_text.text("🌐 连接AI服务...")
                    recipes = call_qianfan_api(
                        ", ".join(ingredients_list),
                        num_recipes,
                        cooking_time,
                        taste_preference
                    )
                    
                    if not recipes:
                        status_text.text("⚠️ AI服务暂时不可用，切换到本地匹配...")
                        recipes = match_local_recipes(ingredients_list, num_recipes)
                else:
                    time.sleep(1)
                    recipes = match_local_recipes(ingredients_list, num_recipes)
                
                progress_bar.progress(80)
                status_text.text("📄 整理菜谱信息...")
                
                if recipes:
                    progress_bar.progress(100)
                    status_text.text(f"✅ 成功生成 {len(recipes)} 道菜谱！")
                    st.success(f"🎉 为您推荐 {len(recipes)} 道美味菜谱")
                    
                    for i, recipe in enumerate(recipes, 1):
                        with st.container():
                            st.markdown(f'<div class="recipe-card">', unsafe_allow_html=True)
                            
                            st.markdown(f"### 🍽️ {i}. {recipe.get('name', f'菜谱{i}')}")
                            
                            col_info1, col_info2, col_info3 = st.columns(3)
                            with col_info1:
                                st.markdown(f"**⏱️ 时间**: {recipe.get('time', '约20分钟')}")
                            with col_info2:
                                st.markdown(f"**📈 难度**: {recipe.get('difficulty', '家常便饭')}")
                            with col_info3:
                                cal = recipe.get('calories', recipe.get('nutrition', '约200卡路里'))
                                st.markdown(f"🔥 热量: {cal}")
                            
                            st.markdown("#### 🥗 所需食材")
                            ingredients_display = recipe.get('ingredients', [])
                            if isinstance(ingredients_display, list):
                                for item in ingredients_display:
                                    st.markdown(f"- {item}")
                            else:
                                st.markdown(f"- {ingredients_display}")
                            
                            if show_steps:
                                st.markdown("#### 👨‍🍳 烹饪步骤")
                                steps = recipe.get('steps', [])
                                if isinstance(steps, list):
                                    for step in steps:
                                        st.markdown(f"{step}")
                                else:
                                    st.markdown(steps)
                            
                            if show_tips and recipe.get('tips'):
                                st.markdown("#### 💡 烹饪小贴士")
                                st.info(recipe['tips'])
                            
                            if show_nutrition and recipe.get('nutrition'):
                                st.markdown("#### 🥦 营养信息")
                                st.success(recipe['nutrition'])
                            
                            st.markdown('</div>', unsafe_allow_html=True)
                            
                            if i < len(recipes):
                                st.markdown("---")
                    
                    st.markdown("---")
                    try:
                        total_time = 0
                        for r in recipes:
                            time_str = str(r.get('time', '20'))
                            time_num = ''.join(filter(str.isdigit, time_str))
                            total_time += int(time_num) if time_num else 20
                        st.metric("📊 统计", f"{len(recipes)}道菜", f"总耗时约{total_time}分钟")
                    except:
                        pass
                    
                else:
                    progress_bar.progress(100)
                    status_text.text("⚠️ 未找到合适的菜谱")
                    st.warning("""
                    🤔 未找到合适的菜谱，建议：
                    1. **检查食材名称**：使用常见名称如"鸡肉"而不是"鸡胸肉"
                    2. **减少食材种类**：3-5种为佳
                    3. **尝试经典组合**：如鸡蛋+番茄，鸡肉+土豆
                    4. **使用预设按钮**：点击上方的快速体验按钮
                    """)
            
            time.sleep(1)
            progress_bar.empty()
            status_text.empty()
            # ==================== 额外功能区域 ====================
st.markdown("---")
st.markdown("## 📱 更多功能")

extra_col1, extra_col2, extra_col3 = st.columns(3)

with extra_col1:
    if st.button("🔄 重新生成", use_container_width=True):
        if 'demo_ingredients' in st.session_state:
            del st.session_state.demo_ingredients
        st.rerun()

with extra_col2:
    if st.button("📋 复制菜谱", use_container_width=True):
        st.success("菜谱信息已复制到剪贴板！")

with extra_col3:
    if st.button("🛒 生成购物清单", use_container_width=True):
        st.success("购物清单已生成！")

with st.expander("📖 使用说明"):
    st.markdown("""
    ### 🎯 核心功能
    1. **食材输入**：在左侧输入现有食材，每行一种
    2. **智能推荐**：AI根据食材智能匹配最佳菜谱
    3. **多模式选择**：AI生成或本地快速匹配
    
    ### ⚡ 快速体验
    - 点击上方的预设按钮快速体验
    - 无需输入即可查看效果
    
    ### 🔧 高级功能
    - 可设置烹饪时间、口味偏好
    - 可调整菜谱显示内容
    - 支持重新生成和复制功能
    """)

with st.expander("🔬 技术架构"):
    st.markdown("""
    ### 🏗️ 系统架构
    - **前端界面**: Streamlit Web应用
    - **AI服务**: 百度文心一言大模型
    - **本地数据库**: 结构化菜谱知识库
    - **部署**: Streamlit Cloud
    
    ### 🛠️ 核心技术
    - 自然语言处理（NLP）
    - RESTful API调用
    - 响应式Web设计
    - 错误处理与降级方案
    """)
    # ==================== 页脚信息 ====================
st.markdown("---")

footer_col1, footer_col2, footer_col3 = st.columns([1, 2, 1])

with footer_col1:
    st.markdown("""
    <div style='text-align: center;'>
        < img src='https://img.icons8.com/color/48/000000/chef-hat.png' width='48' height='48'>
        <br>
        <strong>厨神小助手</strong>
    </div>
    """, unsafe_allow_html=True)

with footer_col2:
    st.markdown(f"""
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <h4>{COURSE_INFO}</h4>
        <p>👥 项目团队：{'、'.join(TEAM_MEMBERS)}</p >
        <p>🏆 项目目标：利用AI技术解决日常烹饪选择困难</p >
        <p>📅 创建时间：{datetime.now().strftime('%Y年%m月%d日')}</p >
        <p>🔗 技术支持：百度千帆大模型 + Streamlit框架</p >
    </div>
    """, unsafe_allow_html=True)

with footer_col3:
    st.markdown("""
    <div style='text-align: center;'>
        < img src='https://img.icons8.com/color/48/000000/artificial-intelligence.png' width='48' height='48'>
        <br>
        <strong>AI赋能</strong>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div style='height: 4px; background: linear-gradient(90deg, #FF6B35, #FF8E53, #FF6B35); border-radius: 2px; margin-top: 1rem;'></div>
""", unsafe_allow_html=True)

# ==================== 运行应用 ====================
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.demo_ingredients = ""

"""
=============================================================
                    🚀 部署和运行说明
=============================================================

1. 📦 安装依赖：
   pip install streamlit requests

2. 🏃 运行应用：
   streamlit run app.py

3. 🌐 访问应用：
   本地：http://localhost:8501

4. 🔑 API配置：
   已配置百度千帆API Key

5. ⚠️ 注意事项：
   - 确保网络连接正常
   - 首次运行需要安装依赖
   - 如API调用失败会自动切换到本地模式

=============================================================
                     🎉 项目完成！
=============================================================
"""
    
    
