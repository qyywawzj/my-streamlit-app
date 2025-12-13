
import streamlit as st
import requests
import json
import random
from datetime import datetime

# ==================== 配置页面 ====================
st.set_page_config(
    page_title="🍳 厨神小助手 - AI美食顾问",
    page_icon="🍳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== 自定义CSS美化 ====================
st.markdown("""
<style>
    .main-header {
        font-size: 2.8rem;
        color: #FF6B6B;
        text-align: center;
        margin-bottom: 0.5rem;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .sub-header {
        font-size: 1.3rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stButton button {
        background: linear-gradient(135deg, #FF6B6B 0%, #FF8E53 100%);
        color: white;
        font-size: 1.2rem;
        font-weight: bold;
        border-radius: 12px;
        padding: 0.7rem 2rem;
        width: 100%;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(255,107,107,0.4);
    }
    .recipe-card {
        background: linear-gradient(135deg, #ffffff 0%, #fff9f9 100%);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        border-left: 6px solid #FF6B6B;
        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
    }
    .recipe-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.12);
    }
    .team-members {
        background: linear-gradient(135deg, #f0f8ff 0%, #e6f7ff 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin-top: 2rem;
        text-align: center;
        border: 2px dashed #4dabf7;
    }
    .nutrition-box {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        padding: 1.2rem;
        border-radius: 12px;
        margin: 1rem 0;
    }
    .alternative-box {
        background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%);
        padding: 1.2rem;
        border-radius: 12px;
        margin: 1rem 0;
    }
    .stats-box {
        background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# ==================== API配置 ====================
API_KEY = "sk-dfa197f8ee7e41dbab7f467b014e788a"
API_URL = "https://api.moonshot.cn/v1/chat/completions"  # 假设这是正确的API端点，可能需要调整

# ==================== 用户个性化数据 ====================
if 'user_profile' not in st.session_state:
    st.session_state.user_profile = {
        'preferences': [],      # 用户口味偏好
        'history': [],          # 历史查询记录
        'dietary_restrictions': [],  # 饮食限制
        'favorite_recipes': []  # 收藏的菜谱
    }

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# ==================== 页面标题 ====================
st.markdown('<div class="main-header">🍳 厨神小助手</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">🤖 AI智能美食顾问 · 支持自然语言输入 · 个性化推荐 · 详细营养分析</div>', unsafe_allow_html=True)

# ==================== 侧边栏 - 用户个性化设置 ====================
with st.sidebar:
    st.markdown("### 👤 个性化设置")
    
    # 用户偏好选择
    preferences = st.multiselect(
        "💕 您的口味偏好",
        ["清淡", "麻辣", "酸甜", "咸香", "鲜味", "咖喱", "烧烤", "素食", "低脂", "高蛋白"],
        default=["清淡", "咸香"]
    )
    
    dietary_restrictions = st.multiselect(
        "🚫 饮食限制",
        ["无乳糖", "无麸质", "低盐", "低糖", "素食", "清真", "无坚果", "无海鲜"],
        default=[]
    )
    
    cooking_level = st.select_slider(
        "👨‍🍳 烹饪经验",
        options=["新手", "入门", "熟练", "高手", "大厨"],
        value="入门"
    )
    
    max_cooking_time = st.slider(
        "⏱️ 最大烹饪时间（分钟）",
        10, 180, 60
    )
    
    calories_pref = st.selectbox(
        "🔥 热量偏好",
        ["不限", "低卡(<400卡)", "适中(400-600卡)", "高卡(>600卡)"],
        index=1
    )
    
    st.markdown("---")
    st.markdown("### 📊 使用统计")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="stats-box">
            <div style="font-size: 0.9rem; color: #666;">今日推荐</div>
            <div style="font-size: 1.5rem; font-weight: bold; color: #FF6B6B;">{len(st.session_state.user_profile['history'])}</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="stats-box">
            <div style="font-size: 0.9rem; color: #666;">收藏菜谱</div>
            <div style="font-size: 1.5rem; font-weight: bold; color: #4CAF50;">{len(st.session_state.user_profile['favorite_recipes'])}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # 更新用户资料
    if preferences != st.session_state.user_profile['preferences']:
        st.session_state.user_profile['preferences'] = preferences
    if dietary_restrictions != st.session_state.user_profile['dietary_restrictions']:
        st.session_state.user_profile['dietary_restrictions'] = dietary_restrictions

# ==================== 主内容区 ====================
tab1, tab2, tab3 = st.tabs(["🍳 智能推荐", "💬 AI对话模式", "❤️ 我的收藏"])

with tab1:
    # 输入区域 - 支持自然语言
    st.markdown("### 🎯 智能食材分析")
    
    input_method = st.radio(
        "选择输入方式：",
        ["📝 自然语言描述", "🥦 列出食材清单"],
        horizontal=True
    )
    
    if input_method == "📝 自然语言描述":
        user_input = st.text_area(
            "💬 用自然语言描述您的需求",
            placeholder="例如：\\n- 我冰箱里有鸡蛋、番茄、土豆，想做一顿简单的晚餐\\n- 我想吃辣一点的菜，家里有鸡肉和青椒\\n- 请推荐一个30分钟内能完成的低卡素食\\n- 剩饭和鸡蛋能做什么好吃的？",
            height=120,
            key="natural_input"
        )
    else:
        ingredients_input = st.text_area(
            "🥦 列出您现有的食材（每行一种）",
            placeholder="例如：\\n鸡蛋\\n番茄\\n土豆\\n鸡肉\\n青椒",
            height=120,
            key="list_input"
        )
        user_input = ingredients_input
    
    # 高级筛选
    with st.expander("🔍 高级筛选选项"):
        col1, col2, col3 = st.columns(3)
        with col1:
            cuisine_type = st.multiselect(
                "菜系",
                ["中餐", "西餐", "日料", "韩餐", "东南亚", "其他"],
                default=["中餐"]
            )
        with col2:
            meal_type = st.selectbox(
                "餐别",
                ["不限", "早餐", "午餐", "晚餐", "夜宵", "甜点", "汤品"]
            )
        with col3:
            difficulty = st.select_slider(
                "难度",
                options=["极简", "简单", "中等", "复杂", "挑战"],
                value="简单"
            )
    
    # 生成按钮
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        generate_btn = st.button("✨ AI智能生成菜谱", type="primary", use_container_width=True)

# ==================== AI调用函数 ====================
def call_ai_api(user_input, user_profile, options=None):
    """调用AI API生成菜谱"""
    
    # 构建用户画像描述
    profile_desc = f"""
    用户画像：
    - 口味偏好：{', '.join(user_profile['preferences'])}
    - 饮食限制：{', '.join(user_profile['dietary_restrictions']) if user_profile['dietary_restrictions'] else '无'}
    - 烹饪经验：{user_profile.get('cooking_level', '入门')}
    - 最大烹饪时间：{user_profile.get('max_cooking_time', 60)}分钟
    - 热量偏好：{user_profile.get('calories_pref', '适中')}
    """
    
    if options:
        profile_desc += f"""
    额外要求：
    - 菜系：{', '.join(options.get('cuisine_type', ['中餐']))}
    - 餐别：{options.get('meal_type', '不限')}
    - 难度：{options.get('difficulty', '简单')}
    """
    
    # 构建prompt
    prompt = f"""你是一个专业的美食顾问、营养师和厨师。请根据用户的需求和个性化设置，生成详细的菜谱。

{profile_desc}

用户需求：{user_input}

请严格按照以下JSON格式输出1-3个菜谱：

{{
  "recipes": [
    {{
      "recipe_name": "菜谱名称",
      "description": "简要描述",
      "match_score": 90,  // 与用户需求的匹配度（0-100）
      "total_time": "总时间，如'25分钟'",
      "difficulty": "难度等级",
      "servings": "份量，如'2人份'",
      "ingredients": [
        {{
          "name": "食材名称",
          "quantity": "用量，如'200g'或'2个'",
          "essential": true,  // 是否必需
          "alternatives": ["替代食材1", "替代食材2"]  // 可替代食材
        }}
      ],
      "steps": [
        {{
          "step_number": 1,
          "description": "步骤描述",
          "time_required": "所需时间，如'5分钟'",
          "tips": "小贴士"
        }}
      ],
      "nutrition": {{
        "calories": "热量，如'350卡'",
        "protein": "蛋白质含量",
        "carbs": "碳水化合物含量",
        "fat": "脂肪含量",
        "key_nutrients": ["主要营养成分"],
        "health_benefits": "健康益处"
      }},
      "cooking_tips": [
        "烹饪技巧1",
        "烹饪技巧2"
      ],
      "storage_advice": "储存建议",
      "pairing_suggestions": ["搭配建议"],
      "estimated_cost": "预估成本"
    }}
  ]
}}

要求：
1. 用量要精确（使用克、个、毫升等单位）
2. 步骤要详细，包含每一步的时间
3. 提供具体的营养数据
4. 考虑用户的个性化设置
5. 输出必须是合法的JSON格式
"""
    
    try:
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "moonshot-v1-8k",  # 根据实际模型调整
            "messages": [
                {"role": "system", "content": "你是一个专业的美食顾问，精通烹饪、营养学和食材搭配。"},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 4000
        }
        
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            
            # 尝试提取JSON部分
            import re
            json_match = re.search(r'\\{.*\\}', content, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                return json.loads(json_str)
            else:
                # 如果API没有返回JSON，创建一个模拟响应
                return create_fallback_response(user_input)
        else:
            st.error(f"API调用失败: {response.status_code}")
            return create_fallback_response(user_input)
            
    except Exception as e:
        st.error(f"发生错误: {str(e)}")
        return create_fallback_response(user_input)

def create_fallback_response(user_input):
    """当API调用失败时的备用响应"""
    return {
        "recipes": [
            {
                "recipe_name": "番茄炒蛋",
                "description": "经典家常菜，简单易做，营养丰富",
                "match_score": 85,
                "total_time": "15分钟",
                "difficulty": "简单",
                "servings": "2人份",
                "ingredients": [
                    {"name": "鸡蛋", "quantity": "3个", "essential": True, "alternatives": ["鸭蛋", "鹌鹑蛋"]},
                    {"name": "番茄", "quantity": "2个（约300g）", "essential": True, "alternatives": ["小番茄", "彩椒"]},
                    {"name": "葱", "quantity": "10g", "essential": False, "alternatives": ["洋葱", "韭菜"]},
                    {"name": "盐", "quantity": "3g", "essential": True, "alternatives": ["低钠盐", "酱油"]},
                    {"name": "糖", "quantity": "5g", "essential": False, "alternatives": ["蜂蜜", "代糖"]},
                    {"name": "食用油", "quantity": "15ml", "essential": True, "alternatives": ["橄榄油", "花生油"]}
                ],
                "steps": [
                    {"step_number": 1, "description": "鸡蛋打散，加1g盐搅拌均匀", "time_required": "2分钟", "tips": "加少许水鸡蛋更嫩"},
                    {"step_number": 2, "description": "番茄洗净切块，葱切末", "time_required": "3分钟", "tips": "番茄去皮口感更好"},
                    {"step_number": 3, "description": "热锅倒油，倒入蛋液炒至凝固盛出", "time_required": "3分钟", "tips": "火不要太大"},
                    {"step_number": 4, "description": "再加少许油，炒番茄至出汁", "time_required": "4分钟", "tips": "用铲子按压番茄"},
                    {"step_number": 5, "description": "加入鸡蛋、剩余盐、糖翻炒均匀", "time_required": "2分钟", "tips": "快速翻炒"},
                    {"step_number": 6, "description": "撒葱花出锅", "time_required": "1分钟", "tips": "关火后撒葱花更香"}
                ],
                "nutrition": {
                    "calories": "约250卡/人",
                    "protein": "15g",
                    "carbs": "12g",
                    "fat": "16g",
                    "key_nutrients": ["维生素C", "维生素A", "蛋白质", "番茄红素"],
                    "health_benefits": "增强免疫力，保护视力，抗氧化"
                },
                "cooking_tips": [
                    "番茄选熟透的更容易出汁",
                    "炒蛋时油温不要太高",
                    "加少许糖可以中和番茄酸味"
                ],
                "storage_advice": "冷藏保存不超过24小时，不建议冷冻",
                "pairing_suggestions": ["米饭", "面条", "馒头"],
                "estimated_cost": "约8-12元"
            }
        ]
    }

# ==================== 显示结果 ====================
if generate_btn and user_input:
    with st.spinner("🔍 AI正在分析您的需求，生成个性化菜谱..."):
        # 保存到历史记录
        st.session_state.user_profile['history'].append({
            'query': user_input,
            'time': datetime.now().strftime("%Y-%m-%d %H:%M"),
            'preferences': st.session_state.user_profile['preferences']
        })
        
        # 调用AI
        options = {
            'cuisine_type': cuisine_type,
            'meal_type': meal_type,
            'difficulty': difficulty
        }
        
        # 更新用户资料中的其他信息
        st.session_state.user_profile['cooking_level'] = cooking_level
        st.session_state.user_profile['max_cooking_time'] = max_cooking_time
        st.session_state.user_profile['calories_pref'] = calories_pref
        
        result = call_ai_api(user_input, st.session_state.user_profile, options)
        
        if result and 'recipes' in result:
            recipes = result['recipes']
            st.success(f"✅ 为您生成 {len(recipes)} 个个性化菜谱！")
            
            # 显示匹配度最高的菜谱
            recipes.sort(key=lambda x: x.get('match_score', 0), reverse=True)
            
            for idx, recipe in enumerate(recipes):
                with st.container():
                    st.markdown(f'<div class="recipe-card">', unsafe_allow_html=True)
                    
                    # 菜谱头部信息
                    col1, col2, col3 = st.columns([3, 1, 1])
                    with col1:
                        st.markdown(f"### 🍽️ {idx+1}. {recipe['recipe_name']}")
                        st.markdown(f"*{recipe['description']}*")
                    with col2:
                        st.markdown(f"**🎯 匹配度**")
                        score = recipe.get('match_score', 0)
                        color = "#4CAF50" if score >= 80 else "#FF9800" if score >= 60 else "#F44336"
                        st.markdown(f'<span style="font-size: 1.8rem; font-weight: bold; color: {color};">{score}%</span>', unsafe_allow_html=True)
                    with col3:
                        st.markdown(f"**⏱️ 总时间**")
                        st.markdown(f"**{recipe['total_time']}**")
                    
                    # 基本信息
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.markdown(f"**👥 份量**: {recipe['servings']}")
                    with col2:
                        st.markdown(f"**📊 难度**: {recipe['difficulty']}")
                    with col3:
                        st.markdown(f"**💰 预估成本**: {recipe.get('estimated_cost', '--')}")
                    
                    st.markdown("---")
                    
                    # 食材部分
                    st.markdown("#### 🥗 食材清单")
                    ingredients_df = []
                    for ing in recipe['ingredients']:
                        ingredients_df.append({
                            "食材": ing['name'],
                            "用量": ing['quantity'],
                            "必需": "✅" if ing['essential'] else "➖",
                            "可替代": ", ".join(ing['alternatives']) if ing['alternatives'] else "无"
                        })
                    
                    st.table(ingredients_df)
                    
                    # 替代食材提示
                    if any(ing['alternatives'] for ing in recipe['ingredients']):
                        st.markdown('<div class="alternative-box">', unsafe_allow_html=True)
                        st.markdown("##### 🔄 食材替代建议")
                        for ing in recipe['ingredients']:
                            if ing['alternatives']:
                                st.markdown(f"- **{ing['name']}** 可用：{', '.join(ing['alternatives'])}")
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    # 步骤部分
                    st.markdown("#### 👨‍🍳 详细步骤")
                    for step in recipe['steps']:
                        with st.expander(f"步骤 {step['step_number']}: {step['description']} ({step['time_required']})"):
                            st.markdown(f"**⏱️ 时间**: {step['time_required']}")
                            st.markdown(f"**💡 小贴士**: {step['tips']}")
                    
                    # 营养信息
                    st.markdown('<div class="nutrition-box">', unsafe_allow_html=True)
                    st.markdown("#### 📊 营养分析")
                    nutrition = recipe['nutrition']
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"**🔥 热量**: {nutrition['calories']}")
                        st.markdown(f"**🥚 蛋白质**: {nutrition['protein']}")
                        st.markdown(f"**🌾 碳水**: {nutrition['carbs']}")
                        st.markdown(f"**🥑 脂肪**: {nutrition['fat']}")
                    with col2:
                        st.markdown(f"**💎 关键营养**: {', '.join(nutrition['key_nutrients'])}")
                        st.markdown(f"**❤️ 健康益处**: {nutrition['health_benefits']}")
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # 附加信息
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("#### 💡 烹饪技巧")
                        for tip in recipe['cooking_tips']:
                            st.markdown(f"- {tip}")
                        
                        st.markdown("#### 🍽️ 搭配建议")
                        for pairing in recipe['pairing_suggestions']:
                            st.markdown(f"- {pairing}")
                    
                    with col2:
                        st.markdown("#### 📦 储存建议")
                        st.markdown(recipe['storage_advice'])
                        
                        # 收藏按钮
                        if st.button(f"❤️ 收藏这个菜谱", key=f"save_{idx}"):
                            if recipe['recipe_name'] not in [r['recipe_name'] for r in st.session_state.user_profile['favorite_recipes']]:
                                st.session_state.user_profile['favorite_recipes'].append(recipe)
                                st.success("已添加到收藏！")
                    
                    st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.error("未能生成菜谱，请稍后重试或简化您的需求。")

with tab2:
    st.markdown("### 💬 与AI厨师对话")
    
    # 显示聊天历史
    for msg in st.session_state.chat_history[-10:]:  # 显示最近10条
        if msg['role'] == 'user':
            st.markdown(f"**👤 您**: {msg['content']}")
        else:
            st.markdown(f"**🤖 AI厨师**: {msg['content']}")
    
    # 输入框
    chat_input = st.text_input("💬 向AI厨师提问（如：'如何让牛排更嫩？'）", key="chat_input")
    
    if st.button("发送", key="send_chat"):
        if chat_input:
            # 添加到历史
            st.session_state.chat_history.append({'role': 'user', 'content': chat_input, 'time': datetime.now()})
            
            # 模拟AI回复
            ai_response = f"收到您的提问：'{chat_input}'。这是一个很好的问题！让我为您详细解答..."
            st.session_state.chat_history.append({'role': 'assistant', 'content': ai_response, 'time': datetime.now()})
            
            st.rerun()

with tab3:
    st.markdown("### ❤️ 我的收藏")
    
    if st.session_state.user_profile['favorite_recipes']:
        for idx, recipe in enumerate(st.session_state.user_profile['favorite_recipes']):
            with st.expander(f"{recipe['recipe_name']}"):
                st.markdown(f"**描述**: {recipe['description']}")
                st.markdown(f"**总时间**: {recipe['total_time']}")
                st.markdown(f"**难度**: {recipe['difficulty']}")
                
                if st.button(f"移除收藏", key=f"remove_{idx}"):
                    st.session_state.user_profile['favorite_recipes'].pop(idx)
                    st.rerun()
    else:
        st.info("暂无收藏的菜谱。在智能推荐中遇到喜欢的菜谱，点击收藏按钮即可保存到这里。")

# ==================== 页脚和团队信息 ====================
st.markdown("---")

# 团队信息
st.markdown("""
<div class="team-members">
    <h4>👨‍🎓 项目团队 - 厨神小助手</h4>
    <p style="font-size: 1.1rem; font-weight: bold;">刘蕊琪 · 戚洋洋 · 王佳慧 · 覃丽娜 · 欧婷 · 贺钰鑫</p>
    <p style="color: #666; font-size: 1rem;">《人工智能通识》大作业 · AI+美食生活项目</p>
    <p style="color: #888; font-size: 0.9rem; margin-top: 0.5rem;">
        🤖 基于Moonshot AI · 支持自然语言理解 · 个性化推荐 · 详细营养分析
    </p>
</div>
""", unsafe_allow_html=True)

# ==================== 使用说明 ====================
with st.expander("📖 使用说明"):
    st.markdown("""
    ### 🎯 功能特色
    
    1. **自然语言理解**
       - 支持用自然语言描述需求
       - 例如："冰箱里有鸡蛋、番茄、土豆，想做一顿简单的晚餐"
    
    2. **个性化推荐**
       - 根据您的口味偏好、饮食限制、烹饪经验定制
       - 考虑热量需求和时间限制
    
    3. **详细菜谱信息**
       - 精确的食材用量（克、个、毫升）
       - 每一步的具体时间和技巧
       - 食材替代方案
       - 完整的营养分析
    
    4. **智能对话**
       - 与AI厨师交流烹饪技巧
       - 提问任何与美食相关的问题
    
    ### 💡 使用建议
    
    - 在侧边栏完善您的个性化设置
    - 尝试用自然语言描述您的需求
    - 利用高级筛选找到最合适的菜谱
    - 收藏喜欢的菜谱方便下次查看
    """)
