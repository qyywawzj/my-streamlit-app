import streamlit as st
import requests
import json
import re
from datetime import datetime
import hashlib

# ==================== 配置页面 ====================
st.set_page_config(
    page_title="🍳 厨神小助手 - AI智能美食推荐",
    page_icon="🍳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== API配置 ====================
API_KEY = "sk-dfa197f8ee7e41dbab7f467b014e788a"  # 您的API Key
API_URL = "https://api.deepseek.com/v1/chat/completions"  # DeepSeek API

# ==================== 自定义CSS美化 ====================
st.markdown("""
<style>
    .main-header {
        font-size: 2.8rem;
        background: linear-gradient(90deg, #FF6B6B, #FF8E53);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
        font-weight: bold;
    }
    .sub-header {
        font-size: 1.3rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 300;
    }
    .stButton button {
        background: linear-gradient(135deg, #FF6B6B, #FF8E53);
        color: white;
        font-size: 1.1rem;
        font-weight: bold;
        border-radius: 12px;
        padding: 0.8rem 2.5rem;
        border: none;
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(255, 107, 107, 0.3);
    }
    .recipe-card {
        background: linear-gradient(145deg, #ffffff, #f5f5f5);
        padding: 1.8rem;
        border-radius: 18px;
        margin-bottom: 2rem;
        border-left: 6px solid #FF6B6B;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        transition: transform 0.3s ease;
    }
    .recipe-card:hover {
        transform: translateY(-3px);
    }
    .ingredient-badge {
        display: inline-block;
        background: #E8F4FD;
        color: #2C7BE5;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        margin: 0.2rem;
        font-size: 0.9rem;
    }
    .time-badge {
        background: #FFE8E8;
        color: #FF6B6B;
        padding: 0.3rem 1rem;
        border-radius: 15px;
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
    }
    .nutrition-badge {
        background: #E8F7F0;
        color: #00B894;
        padding: 0.3rem 1rem;
        border-radius: 15px;
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
    }
    .step-box {
        background: #FFF9F9;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.8rem 0;
        border-left: 3px solid #FFC8C8;
    }
    .team-section {
        background: linear-gradient(135deg, #f8f9fa, #e9ecef);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# ==================== 自然语言食材映射 ====================
INGREDIENT_SYNONYMS = {
    "番茄": ["西红柿", "蕃茄", "tomato"],
    "鸡蛋": ["蛋", "鸡卵", "egg"],
    "土豆": ["马铃薯", "洋芋", "potato"],
    "鸡肉": ["鸡胸肉", "鸡腿肉", "鸡块", "chicken"],
    "牛肉": ["牛腩", "牛排", "牛肉片", "beef"],
    "猪肉": ["猪肉片", "猪肉末", "五花肉", "pork"],
    "米饭": ["白饭", "米饭", "rice"],
    "面条": ["面", "面条", "noodle"],
    "豆腐": ["豆干", "豆制品", "tofu"],
    "青菜": ["蔬菜", "绿叶菜", "vegetable"],
    "鱼": ["鱼肉", "鱼片", "fish"],
    "虾": ["虾仁", "鲜虾", "shrimp"],
    "牛奶": ["奶", "鲜奶", "milk"],
    "糖": ["白糖", "砂糖", "sugar"],
    "盐": ["食盐", "精盐", "salt"],
    "酱油": ["生抽", "老抽", "soy sauce"],
    "醋": ["陈醋", "米醋", "vinegar"],
    "油": ["食用油", "植物油", "oil"],
}

def normalize_ingredient(ingredient):
    """将食材名称标准化"""
    ingredient = ingredient.strip().lower()
    
    # 检查同义词
    for std_name, synonyms in INGREDIENT_SYNONYMS.items():
        if ingredient == std_name.lower() or ingredient in [s.lower() for s in synonyms]:
            return std_name
    
    # 去除量词和描述
    ingredient = re.sub(r'[0-9]+[克g毫升ml个份]+', '', ingredient)
    ingredient = re.sub(r'[少许适量少量大量多些]+', '', ingredient)
    
    return ingredient.title()

# ==================== 用户偏好系统 ====================
class UserPreference:
    def __init__(self):
        if 'user_prefs' not in st.session_state:
            st.session_state.user_prefs = {
                'favorite_cuisines': [],
                'allergies': [],
                'diet_restrictions': [],
                'cooking_level': '新手',
                'preferred_cooking_time': '30分钟内',
                'history': []
            }
    
    def add_history(self, ingredients, recipes):
        """记录用户查询历史"""
        history_entry = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'ingredients': ingredients,
            'recipes_selected': [r['name'] for r in recipes[:2]] if recipes else []
        }
        st.session_state.user_prefs['history'].append(history_entry)
        
        # 限制历史记录数量
        if len(st.session_state.user_prefs['history']) > 20:
            st.session_state.user_prefs['history'] = st.session_state.user_prefs['history'][-20:]

# ==================== AI API调用函数 ====================
def call_ai_api(ingredients, preferences=None, num_recipes=3):
    """调用AI API生成智能菜谱推荐"""
    
    # 构建智能提示词
    system_prompt = """你是一位五星级主厨兼营养师。请根据用户提供的食材和偏好，生成专业、详细、可操作的菜谱。
    
    每道菜谱必须包含以下部分：
    1. 菜谱名称（要求：有创意、吸引人）
    2. 食材清单（精确到克/毫升，例如：番茄200克、鸡蛋3个约150克）
    3. 可替代食材（如果缺某种食材的解决方案）
    4. 详细步骤（每步包含：具体操作、所需时间、小技巧）
    5. 总烹饪时间
    6. 营养贴士（热量、蛋白质、维生素等含量分析）
    7. 小提示（烹饪秘诀、注意事项）
    
    根据用户偏好调整："""
    
    if preferences:
        system_prompt += f"""
        - 烹饪水平：{preferences.get('cooking_level', '通用')}
        - 偏好时间：{preferences.get('preferred_cooking_time', '任意')}
        - 饮食限制：{preferences.get('diet_restrictions', '无')}
        """
    
    user_prompt = f"""
    用户现有食材：{ingredients}
    请推荐{num_recipes}道不同类别的菜谱（涵盖：炒菜、汤羹、主食、甜点等）。
    要求：
    1. 基于现有食材，可适当添加常见调味料
    2. 考虑食材的合理搭配和营养均衡
    3. 步骤详细可操作，时间精确
    4. 输出格式为JSON数组，每个菜谱是一个对象，包含：
       - name: 菜名
       - category: 类别（炒菜/汤羹/主食/甜点/凉菜/炖菜）
       - ingredients: 数组，每个元素是"食材名: 用量(如:200克)"
       - alternatives: 对象，{"缺某食材": "可用某食材代替"}
       - steps: 数组，每个元素是"第X步: 操作 (时间: X分钟)"
       - total_time: 总时间(如:25分钟)
       - nutrition: 营养分析文本
       - tips: 小提示文本
    
    请只输出JSON，不要其他文字。"""
    
    try:
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 2000
        }
        
        response = requests.post(API_URL, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            
            # 提取JSON部分
            json_match = re.search(r'\\[.*\\]', content, re.DOTALL)
            if json_match:
                recipes_json = json_match.group(0)
                recipes = json.loads(recipes_json)
                return recipes
            else:
                # 如果没找到JSON，尝试解析为纯文本
                st.error("AI返回格式异常，使用备用方案")
                return generate_fallback_recipes(ingredients, num_recipes)
        else:
            st.error(f"API调用失败: {response.status_code}")
            return generate_fallback_recipes(ingredients, num_recipes)
            
    except Exception as e:
        st.error(f"网络错误: {str(e)}")
        return generate_fallback_recipes(ingredients, num_recipes)

def generate_fallback_recipes(ingredients, num_recipes):
    """备用菜谱生成（当API不可用时）"""
    fallback_recipes = []
    categories = ["家常炒菜", "营养汤羹", "健康主食", "美味甜点"]
    
    for i in range(min(num_recipes, 3)):
        recipe = {
            "name": f"{ingredients}创意料理{i+1}",
            "category": categories[i % len(categories)],
            "ingredients": [f"{ing}: 适量" for ing in ingredients.split(",")[:3]],
            "alternatives": {"缺某食材": "可用类似食材代替"},
            "steps": [
                f"第1步: 准备食材 (时间: 5分钟)",
                f"第2步: 清洗处理 (时间: 10分钟)",
                f"第3步: 烹饪制作 (时间: 15分钟)",
                f"第4步: 调味装盘 (时间: 5分钟)"
            ],
            "total_time": "约35分钟",
            "nutrition": "营养均衡，富含蛋白质和维生素",
            "tips": "根据个人口味调整调料用量"
        }
        fallback_recipes.append(recipe)
    
    return fallback_recipes

# ==================== 主界面 ====================
st.markdown('<div class="main-header">🍳 厨神小助手</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">AI智能美食推荐 · 让每一餐都充满惊喜</div>', unsafe_allow_html=True)

# ==================== 侧边栏 ====================
with st.sidebar:
    st.header("⚙️ 个性化设置")
    
    # 食材输入
    ingredients_input = st.text_area(
        "🥦 输入现有食材",
        placeholder="例如：西红柿2个、鸡蛋3个、米饭一碗\\n或：番茄、蛋、剩饭\\n支持自然语言描述",
        height=120,
        help="可以用任何方式描述你的食材"
    )
    
    # 烹饪偏好
    st.markdown("---")
    st.subheader("👤 个人偏好")
    
    cooking_level = st.selectbox(
        "你的烹饪水平",
        ["新手入门", "家庭煮夫/妇", "厨房达人", "专业厨师"]
    )
    
    preferred_time = st.selectbox(
        "期望烹饪时间",
        ["15分钟内", "30分钟内", "60分钟内", "任意"]
    )
    
    diet_options = st.multiselect(
        "饮食限制/偏好",
        ["无", "少油", "少盐", "少糖", "素食", "无麸质", "低卡路里"]
    )
    
    # 快速食材按钮
    st.markdown("---")
    st.subheader("🎯 常用食材")
    
    quick_cols = st.columns(3)
    with quick_cols[0]:
        if st.button("🥚 蛋类", use_container_width=True):
            ingredients_input = "鸡蛋、皮蛋、咸蛋"
    with quick_cols[1]:
        if st.button("🍅 茄果", use_container_width=True):
            ingredients_input = "番茄、茄子、青椒"
    with quick_cols[2]:
        if st.button("🥩 肉类", use_container_width=True):
            ingredients_input = "鸡肉、猪肉、牛肉"
    
    # 推荐数量
    st.markdown("---")
    num_recipes = st.slider("📊 推荐菜谱数量", 1, 5, 3)

# ==================== 主内容区 ====================
col1, col2 = st.columns([3, 1])

with col1:
    # 智能解析示例
    if not ingredients_input:
        st.info("💡 智能提示：你可以输入：'冰箱里有西红柿和鸡蛋，还有一点剩饭' 或 '番茄炒蛋需要什么食材？'")
    
    # 演示按钮
    st.subheader("🚀 快速体验")
    demo_cols = st.columns(4)
    with demo_cols[0]:
        if st.button("🍅 番茄炒蛋", use_container_width=True):
            ingredients_input = "番茄2个、鸡蛋3个、葱"
    with demo_cols[1]:
        if st.button("🍲 暖心汤羹", use_container_width=True):
            ingredients_input = "排骨、玉米、胡萝卜、香菇"
    with demo_cols[2]:
        if st.button("🍰 下午茶点", use_container_width=True):
            ingredients_input = "面粉、鸡蛋、牛奶、糖、黄油"
    with demo_cols[3]:
        if st.button("🥗 轻食沙拉", use_container_width=True):
            ingredients_input = "鸡胸肉、生菜、番茄、黄瓜、鸡蛋"

# ==================== 生成按钮和偏好收集 ====================
with col2:
    st.subheader("✨ 开始烹饪")
    generate_btn = st.button("🤖 AI智能推荐", type="primary", use_container_width=True)

# 收集用户偏好
user_prefs = {
    'cooking_level': cooking_level,
    'preferred_cooking_time': preferred_time,
    'diet_restrictions': diet_options
}

user_preference = UserPreference()

# ==================== 结果显示 ====================
if generate_btn and ingredients_input:
    # 标准化食材
    ingredients_list = [normalize_ingredient(ing) for ing in re.split(r'[,，、\\n]', ingredients_input) if ing.strip()]
    standardized_ingredients = "、".join(set(ingredients_list))
    
    if not standardized_ingredients:
        st.warning("请输入有效的食材名称！")
    else:
        with st.spinner("🔮 AI大厨正在思考..."):
            progress_bar = st.progress(0)
            
            # 模拟进度
            for i in range(100):
                progress_bar.progress(i + 1)
            
            # 调用AI生成菜谱
            recipes = call_ai_api(standardized_ingredients, user_prefs, num_recipes)
            
            if recipes:
                # 记录用户偏好
                user_preference.add_history(standardized_ingredients, recipes)
                
                st.success(f"✅ 根据你的食材和偏好，推荐 {len(recipes)} 道美味！")
                
                # 显示菜谱
                for i, recipe in enumerate(recipes):
                    with st.container():
                        st.markdown(f'<div class="recipe-card">', unsafe_allow_html=True)
                        
                        # 标题和类别
                        col_title = st.columns([4, 1])
                        with col_title[0]:
                            st.markdown(f"### 🍽️ {i+1}. {recipe.get('name', '未知菜谱')}")
                        with col_title[1]:
                            category = recipe.get('category', '家常菜')
                            st.markdown(f'<div class="time-badge">🏷️ {category}</div>', unsafe_allow_html=True)
                        
                        # 总时间
                        total_time = recipe.get('total_time', '约30分钟')
                        st.markdown(f'<div class="time-badge">⏱️ {total_time}</div>', unsafe_allow_html=True)
                        
                        # 食材列表
                        st.markdown("**🥗 食材清单**")
                        ingredients = recipe.get('ingredients', [])
                        for ing in ingredients[:8]:  # 最多显示8种
                            st.markdown(f'<span class="ingredient-badge">{ing}</span>', unsafe_allow_html=True)
                        
                        if len(ingredients) > 8:
                            with st.expander("查看更多食材"):
                                for ing in ingredients[8:]:
                                    st.markdown(f'<span class="ingredient-badge">{ing}</span>', unsafe_allow_html=True)
                        
                        # 可替代食材
                        alternatives = recipe.get('alternatives', {})
                        if alternatives:
                            st.markdown("**🔄 食材替代方案**")
                            for orig, alt in list(alternatives.items())[:3]:  # 最多显示3个
                                st.write(f"• 没有**{orig}**？可以用 **{alt}** 代替")
                        
                        # 详细步骤
                        st.markdown("**👨‍🍳 烹饪步骤**")
                        steps = recipe.get('steps', [])
                        for step in steps:
                            st.markdown(f'<div class="step-box">{step}</div>', unsafe_allow_html=True)
                        
                        # 营养贴士
                        nutrition = recipe.get('nutrition', '')
                        if nutrition:
                            st.markdown(f'<div class="nutrition-badge">📊 {nutrition[:100]}...</div>', unsafe_allow_html=True)
                        
                        # 小提示
                        tips = recipe.get('tips', '')
                        if tips:
                            st.info(f"💡 {tips}")
                        
                        st.markdown('</div>', unsafe_allow_html=True)
                
                # 用户反馈
                st.markdown("---")
                feedback_cols = st.columns(3)
                with feedback_cols[0]:
                    if st.button("👍 推荐很准", use_container_width=True):
                        st.success("感谢反馈！AI会学习你的偏好")
                with feedback_cols[1]:
                    if st.button("👎 不太满意", use_container_width=True):
                        st.info("我们会改进推荐算法")
                with feedback_cols[2]:
                    if st.button("💾 保存菜谱", use_container_width=True):
                        st.success("已保存到本地（模拟功能）")
                
            else:
                st.error("😢 暂时无法生成推荐，请检查网络或稍后再试")

# ==================== 页脚和团队信息 ====================
st.markdown("---")

# 技术亮点展示
st.subheader("✨ 系统特色")
tech_cols = st.columns(4)
with tech_cols[0]:
    st.markdown("**🧠 智能理解**")
    st.caption("自然语言识别食材")
with tech_cols[1]:
    st.markdown("**🎯 个性推荐**")
    st.caption("根据偏好定制")
with tech_cols[2]:
    st.markdown("**📊 营养分析**")
    st.caption("每道菜都有营养贴士")
with tech_cols[3]:
    st.markdown("**⚡ 精准计量**")
    st.caption("食材用量精确到克")

# 团队信息
st.markdown("""
<div class="team-section">
    <h4>👨‍🎓 项目团队：厨神小助手</h4>
    <p>刘蕊琪 · 戚洋洋 · 王佳慧 · 覃丽娜 · 欧婷 · 贺钰鑫</p>
    <p style="color: #666; font-size: 0.9rem; margin-top: 0.5rem;">
        《人工智能通识》大作业 · 基于DeepSeek API的智能美食推荐系统
    </p>
</div>
""", unsafe_allow_html=True)

# ==================== 使用说明折叠区 ====================
with st.expander("📖 使用说明"):
    st.markdown("""
    ### 如何使用厨神小助手
    
    1. **输入食材**：在左侧输入你现有的食材，可以用任何方式描述
       - 例如："番茄2个、鸡蛋3个、葱"
       - 或："冰箱里有西红柿和鸡蛋，还有一点剩饭"
    
    2. **设置偏好**：调整烹饪水平、时间等个性化设置
    
    3. **点击生成**：AI会根据你的食材和偏好推荐菜谱
    
    4. **查看结果**：每道菜谱包含：
       - 食材清单（精确到克）
       - 步骤详解（每步有时间）
       - 营养分析
       - 烹饪小贴士
    
    ### 支持的食材类型
    - 🥦 蔬菜水果：番茄、土豆、青菜等
    - 🥩 肉类禽蛋：鸡肉、牛肉、鸡蛋等
    - 🍚 主食谷物：米饭、面条、面粉等
    - 🧂 调味料：油、盐、酱油、醋等
    
    ### 特色功能
    - **自然语言理解**：自动识别"西红柿"就是"番茄"
    - **个性化推荐**：根据你的烹饪水平调整难度
    - **智能替代**：提供食材替代方案
    - **营养均衡**：每道菜都有营养分析
    """)

# 运行统计（模拟）
st.caption(f"🔄 最后更新：{datetime.now().strftime('%Y-%m-%d %H:%M')} 
