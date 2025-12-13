import streamlit as st
import random
import json

# ==================== 配置页面 ====================
st.set_page_config(
    page_title="🍳 厨神小助手",
    page_icon="🍳",
    layout="wide"
)

# ==================== 自定义CSS美化 ====================
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #FF6B6B;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stButton button {
        background-color: #FF6B6B;
        color: white;
        font-size: 1.2rem;
        font-weight: bold;
        border-radius: 10px;
        padding: 0.5rem 2rem;
        width: 100%;
    }
    .recipe-card {
        background-color: #FFF9F9;
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1.5rem;
        border-left: 5px solid #FF6B6B;
    }
    .team-members {
        background-color: #f0f8ff;
        padding: 1rem;
        border-radius: 10px;
        margin-top: 2rem;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# ==================== 页面标题 ====================
st.markdown('<div class="main-header">🍳 厨神小助手</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">输入食材，智能推荐菜谱 · 解决「今天吃什么」的难题</div>', unsafe_allow_html=True)

# ==================== 侧边栏 ====================
with st.sidebar:
    st.header("⚙️ 设置")
    st.markdown("---")
    
    # 食材输入
    ingredients_input = st.text_area(
        "🥦 输入现有食材",
        placeholder="每行一种食材，例如：\\n鸡蛋\\n番茄\\n土豆\\n鸡肉",
        height=150
    )
    
    # 功能选项
    st.markdown("---")
    num_recipes = st.slider("📊 推荐菜谱数量", 1, 5, 3)
    cooking_style = st.selectbox("👨‍🍳 烹饪偏好", ["家常快手", "健康低脂", "下饭神器", "宴客佳肴", "宝宝辅食"])
    
    st.markdown("---")
    st.info("💡 提示：输入3-5种食材效果最佳")

# ==================== 主内容区 ====================
col1, col2 = st.columns([2, 1])

with col1:
    # 演示示例按钮
    st.subheader("🎯 快速体验")
    demo_cols = st.columns(3)
    with demo_cols[0]:
        if st.button("🥚 鸡蛋+番茄", use_container_width=True):
            ingredients_input = "鸡蛋\\n番茄\\n青椒"
    with demo_cols[1]:
        if st.button("🍗 鸡肉+土豆", use_container_width=True):
            ingredients_input = "鸡肉\\n土豆\\n胡萝卜"
    with demo_cols[2]:
        if st.button("🥦 素食组合", use_container_width=True):
            ingredients_input = "豆腐\\n香菇\\n青菜"

# ==================== 核心：菜谱数据 ====================
# 这里使用我们准备好的菜谱数据（简化版）
RECIPES_DATA = {
    "鸡蛋": [
        {
            "name": "番茄炒蛋",
            "ingredients": ["鸡蛋", "番茄", "葱", "盐", "糖", "油"],
            "steps": ["1. 鸡蛋打散，加少许盐", "2. 番茄切块", "3. 热油先炒鸡蛋盛出", "4. 炒番茄至出汁", "5. 加入鸡蛋翻炒调味"],
            "time": "15分钟",
            "tips": "加少许糖能中和番茄酸味，味道更鲜美"
        },
        {
            "name": "韭菜炒蛋",
            "ingredients": ["鸡蛋", "韭菜", "盐", "油"],
            "steps": ["1. 韭菜洗净切段", "2. 鸡蛋打散加盐", "3. 热油炒鸡蛋至凝固盛出", "4. 炒韭菜至变软", "5. 加入鸡蛋翻炒均匀"],
            "time": "10分钟",
            "tips": "韭菜不宜炒太久，保持翠绿口感更佳"
        },
        {
            "name": "虾仁滑蛋",
            "ingredients": ["鸡蛋", "虾仁", "葱", "盐", "料酒", "淀粉"],
            "steps": ["1. 虾仁用料酒淀粉腌制", "2. 鸡蛋打散加盐", "3. 滑炒虾仁至变色", "4. 倒入蛋液轻轻推动", "5. 蛋液凝固即可出锅"],
            "time": "12分钟",
            "tips": "火要小，动作要轻，才能做出嫩滑口感"
        }
    ],
    "番茄": [
        {
            "name": "番茄鸡蛋汤",
            "ingredients": ["番茄", "鸡蛋", "葱花", "盐", "香油"],
            "steps": ["1. 番茄去皮切块", "2. 炒软番茄加水煮开", "3. 淋入打散的蛋液", "4. 加盐调味，淋香油撒葱花"],
            "time": "15分钟",
            "tips": "淋蛋液时火要小，才能形成漂亮的蛋花"
        },
        {
            "name": "番茄牛腩",
            "ingredients": ["番茄", "牛腩", "土豆", "胡萝卜", "姜", "料酒"],
            "steps": ["1. 牛腩焯水", "2. 炒香番茄和调料", "3. 加入牛腩和水炖煮1小时", "4. 加入土豆胡萝卜再炖30分钟"],
            "time": "100分钟",
            "tips": "番茄去皮后更易出汁，汤汁更浓郁"
        }
    ],
    "鸡肉": [
        {
            "name": "土豆烧鸡块",
            "ingredients": ["鸡肉", "土豆", "姜", "料酒", "生抽", "老抽", "糖"],
            "steps": ["1. 鸡肉切块焯水", "2. 炒糖色后加入鸡肉翻炒", "3. 加入调料和水炖煮30分钟", "4. 加入土豆再炖15分钟"],
            "time": "60分钟",
            "tips": "土豆切块后泡水可以防止氧化变黑"
        },
        {
            "name": "可乐鸡翅",
            "ingredients": ["鸡翅", "可乐", "姜", "料酒", "生抽", "老抽"],
            "steps": ["1. 鸡翅划刀用料酒腌制", "2. 煎至两面金黄", "3. 加入可乐和调料", "4. 大火煮开转小火炖煮15分钟"],
            "time": "30分钟",
            "tips": "收汁时要不停翻动，防止糊锅"
        }
    ],
    "土豆": [
        {
            "name": "酸辣土豆丝",
            "ingredients": ["土豆", "干辣椒", "醋", "葱", "盐", "糖"],
            "steps": ["1. 土豆切丝泡水去淀粉", "2. 干辣椒剪段", "3. 爆香辣椒和葱", "4. 加入土豆丝快速翻炒", "5. 淋醋加盐糖调味"],
            "time": "15分钟",
            "tips": "土豆丝要快速翻炒，保持脆爽口感"
        },
        {
            "name": "红烧土豆",
            "ingredients": ["土豆", "生抽", "老抽", "糖", "葱", "油"],
            "steps": ["1. 土豆切滚刀块", "2. 煎至表面金黄", "3. 加入调料和水", "4. 烧煮至土豆软糯收汁"],
            "time": "25分钟",
            "tips": "土豆煎一下再烧，外酥里嫩更美味"
        }
    ],
    "豆腐": [
        {
            "name": "麻婆豆腐",
            "ingredients": ["豆腐", "牛肉末", "郫县豆瓣酱", "花椒粉", "葱姜蒜", "淀粉"],
            "steps": ["1. 豆腐切块焯水", "2. 炒香牛肉末和豆瓣酱", "3. 加入豆腐轻煮", "4. 勾芡撒花椒粉葱花"],
            "time": "20分钟",
            "tips": "豆腐焯水可以去除豆腥味，不易碎"
        },
        {
            "name": "红烧豆腐",
            "ingredients": ["老豆腐", "猪肉末", "生抽", "老抽", "糖", "葱"],
            "steps": ["1. 豆腐煎至两面金黄", "2. 炒香肉末", "3. 加入豆腐和调料", "4. 加水烧煮入味"],
            "time": "25分钟",
            "tips": "用老豆腐不易碎，煎过后更香"
        }
    ]
}

# ==================== 生成菜谱的逻辑 ====================
def generate_recipes(ingredients_text, num=3):
    """根据食材生成菜谱"""
    
    if not ingredients_text.strip():
        return []
    
    # 解析食材
    ingredients = [i.strip() for i in ingredients_text.split('\\n') if i.strip()]
    
    # 匹配菜谱
    matched_recipes = []
    for ing in ingredients:
        if ing in RECIPES_DATA:
            matched_recipes.extend(RECIPES_DATA[ing])
    
    # 去重并限制数量
    unique_recipes = []
    seen = set()
    for recipe in matched_recipes:
        if recipe['name'] not in seen:
            unique_recipes.append(recipe)
            seen.add(recipe['name'])
    
    # 如果匹配到的菜谱不够，添加一些通用推荐
    if len(unique_recipes) < num:
        all_recipes = []
        for ing_list in RECIPES_DATA.values():
            all_recipes.extend(ing_list)
        
        # 随机补充一些菜谱
        random.shuffle(all_recipes)
        for recipe in all_recipes:
            if recipe['name'] not in seen and len(unique_recipes) < num:
                unique_recipes.append(recipe)
                seen.add(recipe['name'])
    
    return unique_recipes[:num]

# ==================== 主按钮和结果显示 ====================
with col2:
    st.subheader("🚀 开始生成")
    generate_btn = st.button("✨ AI智能推荐", type="primary", use_container_width=True)

# 显示结果
if generate_btn or ingredients_input:
    if not ingredients_input.strip():
        st.warning("请输入食材！")
    else:
        with st.spinner("🔍 AI正在分析食材，为您精心搭配..."):
            # 模拟AI处理时间
            import time
            time.sleep(1.5)
            
            # 生成菜谱
            recipes = generate_recipes(ingredients_input, num_recipes)
            
            if recipes:
                st.success(f"✅ 为您找到 {len(recipes)} 道美味菜谱！")
                
                for i, recipe in enumerate(recipes, 1):
                    with st.container():
                        st.markdown(f'<div class="recipe-card">', unsafe_allow_html=True)
                        
                        # 菜谱标题
                        st.markdown(f"### 🍽️ {i}. {recipe['name']}")
                        
                        # 食材
                        st.markdown("**🥗 食材**")
                        st.code(", ".join(recipe['ingredients']))
                        
                        # 步骤
                        st.markdown("**👨‍🍳 步骤**")
                        for step in recipe['steps']:
                            st.markdown(f"- {step}")
                        
                        # 附加信息
                        col_a, col_b = st.columns(2)
                        with col_a:
                            st.markdown(f"**⏱️ 时间**: {recipe['time']}")
                        with col_b:
                            st.markdown(f"**💡 提示**: {recipe['tips']}")
                        
                        st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.info("🤔 没有找到完全匹配的菜谱，建议：\\n"
                       "1. 检查食材名称是否正确\\n"
                       "2. 减少食材种类\\n"
                       "3. 尝试更常见的食材组合")

# ==================== 页脚和团队信息 ====================
st.markdown("---")

# 团队信息
st.markdown("""
<div class="team-members">
    <h4>👨‍🎓 项目团队</h4>
    <p>刘蕊琪 · 戚洋洋 · 王佳慧 · 覃丽娜 · 欧婷 · 贺钰鑫</p>
    <p style="color: #888; font-size: 0.9rem;">《人工智能通识》大作业 · AI+美食生活项目</p>
</div>
""", unsafe_allow_html=True)

# ==================== 隐藏的AI调用占位符 ====================
# 注释掉的代码，展示如何连接真实AI
"""
# 如需连接真实AI API，取消注释以下代码：

import requests

def call_real_ai(ingredients):
    # 这里替换成您的API Key
    API_KEY = "your_api_key_here"
    API_URL = "https://api.your-ai-platform.com/v1/chat"
    
    prompt = f"根据这些食材推荐菜谱：{ingredients}"
    
    response = requests.post(
        API_URL,
        json={"prompt": prompt, "api_key": API_KEY},
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        return response.json()["result"]
    else:
        return "AI服务暂时不可用"
"""
