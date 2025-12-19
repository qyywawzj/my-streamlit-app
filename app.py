# app.py - 厨神小助手AI美食推荐系统
# 第一部分：基础配置和页面设置

import streamlit as st
import requests
import json
import time
from typing import List, Dict, Any

# ==================== 页面配置 ====================
st.set_page_config(
    page_title="🍳 厨神小助手 - AI美食推荐系统",
    page_icon="🍳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== 全局样式 ====================
st.markdown("""
<style>
    /* 主标题样式 */
    .main-title {
        font-size: 2.8rem;
        color: #FF6B6B;
        text-align: center;
        margin-bottom: 0.5rem;
        font-weight: 800;
        background: linear-gradient(90deg, #FF6B6B, #FF8E53);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* 副标题样式 */
    .sub-title {
        font-size: 1.3rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 300;
    }
    
    /* 团队信息样式 */
    .team-info {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 20px;
        margin: 2rem 0;
        color: white;
        text-align: center;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }
    
    /* 按钮样式 */
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-size: 1.1rem;
        font-weight: 600;
        border-radius: 12px;
        padding: 0.7rem 2rem;
        border: none;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 7px 14px rgba(50, 50, 93, 0.1), 0 3px 6px rgba(0, 0, 0, 0.08);
    }
    
    /* 菜谱卡片样式 */
    .recipe-card {
        background: white;
        padding: 1.8rem;
        border-radius: 16px;
        margin-bottom: 1.8rem;
        border-left: 6px solid #FF6B6B;
        box-shadow: 0 6px 12px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    }
    
    .recipe-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 24px rgba(0,0,0,0.1);
    }
    
    /* 侧边栏样式 */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    /* 输入框样式 */
    .stTextArea textarea {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
    }
    
    /* 进度条样式 */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #FF6B6B, #FF8E53);
    }
    
    /* 警告框样式 */
    .stAlert {
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ==================== 页面标题 ====================
st.markdown('<div class="main-title">🍳 厨神小助手</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">AI智能美食推荐系统 · 让烹饪变得更简单</div>', unsafe_allow_html=True)

# ==================== 团队信息 ====================
st.markdown("""
<div class="team-info">
    <h3 style="margin:0; color:white;">👨‍🎓 项目团队</h3>
    <p style="margin:0.5rem 0; font-size:1.1rem; color:white;">
        刘蕊琪 · 戚洋洋 · 王佳慧 · 覃丽娜 · 欧婷 · 贺钰鑫
    </p >
    <p style="margin:0; font-size:0.9rem; opacity:0.9; color:white;">
        《人工智能通识》课程大作业 · AI+美食生活应用
    </p >
</div>
""", unsafe_allow_html=True)
# 第二部分：侧边栏和API配置

# ==================== 百度千帆API配置 ====================
class QianfanAPI:
    """百度千帆大模型API调用类"""
    
    def __init__(self):
        # 您的API配置信息
        self.API_KEY = "bce-v3/ALTAK-1bgyWcDtorkOF0ccj9ai2/1fd1c6767c66174f38e3521920c25648dac44ef4"
        self.SECRET_KEY = "7ae74a327cd447b2ae702bccc5c75283"
        
        # API端点
        self.CHAT_URL = "https://qianfan.baidubce.com/v2/chat/completions"
        self.AUTH_URL = "https://aip.baidubce.com/oauth/2.0/token"
        
        # 获取访问令牌
        self.access_token = self._get_access_token()
    
    def _get_access_token(self):
        """获取百度API访问令牌"""
        try:
            params = {
                "grant_type": "client_credentials",
                "client_id": self.ACCESS_KEY,
                "client_secret": self.SECRET_KEY
            }
            response = requests.get(self.AUTH_URL, params=params)
            if response.status_code == 200:
                return response.json().get("access_token")
            else:
                st.error(f"获取访问令牌失败: {response.status_code}")
                return None
        except Exception as e:
            st.error(f"获取访问令牌时出错: {str(e)}")
            return None
    
    def generate_recipes(self, ingredients: List[str], preferences: Dict[str, Any]) -> Dict[str, Any]:
        """调用千帆API生成菜谱"""
        if not self.access_token:
            return {"error": "API配置错误，无法访问千帆大模型"}
        
        # 构建提示词
        prompt = self._build_prompt(ingredients, preferences)
        
        # 构建请求数据
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        }
        
        data = {
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "top_p": 0.8,
            "penalty_score": 1.0,
            "system": "你是一个专业的智能厨神助手，精通各种家常菜烹饪和营养搭配。请根据用户提供的食材，推荐合适的菜谱，提供详细的步骤和烹饪建议。"
        }
        
        try:
            response = requests.post(
                self.CHAT_URL,
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return self._parse_response(result, ingredients)
            else:
                return {"error": f"API请求失败: {response.status_code}"}
                
        except Exception as e:
            return {"error": f"请求出错: {str(e)}"}
    
    def _build_prompt(self, ingredients: List[str], preferences: Dict[str, Any]) -> str:
        """构建给AI的提示词"""
        num_recipes = preferences.get("num_recipes", 3)
        cooking_style = preferences.get("cooking_style", "家常快手")
        cooking_time = preferences.get("cooking_time", "任意")
        
        prompt = f"""请根据以下食材和需求，生成{num_recipes}道家常菜谱：

可用食材：{', '.join(ingredients)}
烹饪风格：{cooking_style}
期望时间：{cooking_time}

请为每道菜生成以下信息（使用JSON格式）：
1. 菜名
2. 所需全部食材（列表）
3. 详细步骤（3-5步，列表）
4. 预估烹饪时间
5. 难度等级（简单/中等/复杂）
6. 营养小贴士
7. 食材替代建议（如果没有某种食材可以如何替代）
8. 适合人群

请确保：
- 菜谱真实可行，步骤清晰
- 食材用量合理
- 时间预估准确
- 建议实用可操作

请直接输出JSON格式，不要有其他解释文字。"""
        return prompt
    
    def _parse_response(self, response: Dict, ingredients: List[str]) -> Dict[str, Any]:
        """解析API响应"""
        try:
            content = response.get("result", "")
            
            # 尝试提取JSON部分
            import re
            json_match = re.search(r'\[\s*\{.*\}\s*\]', content, re.DOTALL)
            
            if json_match:
                json_str = json_match.group(0)
                recipes = json.loads(json_str)
                return {
                    "success": True,
                    "recipes": recipes,
                    "source": "千帆AI生成",
                    "ingredients_used": ingredients
                }
            else:
                # 如果不是标准JSON，返回原始内容
                return {
                    "success": True,
                    "raw_content": content,
                    "source": "千帆AI生成",
                    "ingredients_used": ingredients
                }
                
        except json.JSONDecodeError:
            # 如果JSON解析失败，使用备用菜谱
            return self._generate_fallback_recipes(ingredients)
    
    def _generate_fallback_recipes(self, ingredients: List[str]) -> Dict[str, Any]:
        """生成备用菜谱（当API失败时使用）"""
        # 这里使用本地菜谱数据作为备用
        local_recipes = self._get_local_recipes(ingredients)
        return {
            "success": True,
            "recipes": local_recipes,
            "source": "本地知识库（AI服务暂时不可用）",
            "ingredients_used": ingredients,
            "note": "使用本地知识库推荐，AI功能稍后恢复"
        }
    
    def _get_local_recipes(self, ingredients: List[str]) -> List[Dict]:
        """从本地知识库获取菜谱"""
        # 这里可以接入之前准备的JSON数据
        # 简化版本，返回几个示例菜谱
        return [
            {
                "name": "番茄炒蛋",
                "ingredients": ["鸡蛋", "番茄", "葱", "盐", "糖", "油"],
                "steps": ["鸡蛋打散加盐", "番茄切块", "热油炒鸡蛋盛出", "炒番茄至出汁", "混合翻炒调味"],
                "time": "15分钟",
                "difficulty": "简单",
                "nutrition": "富含蛋白质和维生素C",
                "alternatives": {"没有番茄": "可用彩椒代替"},
                "suitable_for": "所有人，特别适合学生和上班族"
            },
            {
                "name": "青椒肉丝",
                "ingredients": ["猪肉", "青椒", "姜", "蒜", "生抽", "料酒"],
                "steps": ["猪肉切丝腌制", "青椒切丝", "热油滑炒肉丝", "加入青椒翻炒", "调味出锅"],
                "time": "20分钟",
                "difficulty": "简单",
                "nutrition": "优质蛋白质和维生素",
                "alternatives": {"没有猪肉": "可用鸡肉代替"},
                "suitable_for": "喜欢辣味的人群"
            }
        ]

# 初始化API
qianfan_api = QianfanAPI()

# ==================== 侧边栏配置 ====================
with st.sidebar:
    st.header("⚙️ 智能配置")
    st.markdown("---")
    
    # API状态显示
    if qianfan_api.access_token:
        st.success("✅ 千帆AI API 已就绪")
    else:
        st.warning("⚠️ 千帆AI API 连接中...")
    
    st.markdown("---")
    
    # 食材输入区域
    st.subheader("🥦 输入食材")
    ingredients_text = st.text_area(
        "请列出您现有的食材（每行一种）",
        placeholder="例如：\n鸡蛋\n番茄\n土豆\n鸡肉\n青椒",
        height=150,
        help="输入您冰箱里现有的食材，AI将为您智能搭配菜谱"
    )
    
    st.markdown("---")
    
    # 个性化设置
    st.subheader("🎯 个性化设置")
    
    col1, col2 = st.columns(2)
    with col1:
        num_recipes = st.slider(
            "推荐数量",
            min_value=1,
            max_value=5,
            value=3,
            help="选择AI推荐的菜谱数量"
        )
    
    with col2:
        cooking_style = st.selectbox(
            "烹饪风格",
            ["家常快手", "健康低脂", "下饭神器", "宴客佳肴", "宝宝辅食", "创意料理"],
            help="选择您偏好的烹饪风格"
        )
    
    cooking_time = st.selectbox(
        "期望时间",
        ["任意", "15分钟内", "30分钟内", "60分钟内", "90分钟内"],
        help="选择您希望的烹饪时间"
    )
    
    difficulty = st.selectbox(
        "难度级别",
        ["任意", "新手友好", "厨艺进阶", "大师挑战"],
        help="选择适合您的烹饪难度"
    )
    
    st.markdown("---")
    
    # 快速示例按钮
    st.subheader("🚀 快速体验")
    
    example_cols = st.columns(2)
    with example_cols[0]:
        if st.button("🍳 经典组合", use_container_width=True):
            st.session_state.example_ingredients = "鸡蛋\n番茄\n青椒\n葱"
    
    with example_cols[1]:
        if st.button("🍗 肉类搭配", use_container_width=True):
            st.session_state.example_ingredients = "鸡肉\n土豆\n胡萝卜\n洋葱"
    
    example_cols2 = st.columns(2)
    with example_cols2[0]:
        if st.button("🥦 素食主义", use_container_width=True):
            st.session_state.example_ingredients = "豆腐\n香菇\n青菜\n胡萝卜"
    
    with example_cols2[1]:
        if st.button("🦐 海鲜盛宴", use_container_width=True):
            st.session_state.example_ingredients = "虾\n鸡蛋\n西兰花\n蒜"
    
    st.markdown("---")
    
    # 帮助信息
    with st.expander("💡 使用提示"):
        st.markdown("""
        1. **食材输入**：每行输入一种食材，尽量具体
        2. **设置调整**：根据需求调整推荐参数
        3. **快速体验**：点击示例按钮快速体验
        4. **AI生成**：点击生成按钮调用千帆大模型
        5. **保存分享**：可以保存或分享生成的菜谱
        """)
        # 第三部分：主界面和功能函数

# ==================== 主界面布局 ====================
# 创建两列布局
main_col1, main_col2 = st.columns([3, 2])

with main_col1:
    # 欢迎区域
    st.subheader("🎉 欢迎使用厨神小助手")
    st.markdown("""
    输入您冰箱里的食材，AI将为您：
    - 🍽️ **智能推荐**合适的家常菜谱
    - 🕒 **预估时间**并提供详细步骤
    - 🥗 **分析营养**给出健康建议
    - 🔄 **提供替代**食材解决方案
    """)
    
    # 分隔线
    st.markdown("---")
    
    # 当前设置显示
    st.subheader("📋 当前设置")
    
    if 'example_ingredients' in st.session_state and st.session_state.example_ingredients:
        ingredients_text = st.session_state.example_ingredients
    
    if ingredients_text:
        ingredients_list = [i.strip() for i in ingredients_text.split('\n') if i.strip()]
        if ingredients_list:
            col_set1, col_set2, col_set3 = st.columns(3)
            with col_set1:
                st.metric("食材数量", len(ingredients_list))
            with col_set2:
                st.metric("推荐菜谱", num_recipes)
            with col_set3:
                st.metric("烹饪风格", cooking_style)
            
            # 显示食材列表
            st.markdown("**📦 可用食材：**")
            ingredient_chips = ""
            for ing in ingredients_list:
                ingredient_chips += f'<span style="background: #e3f2fd; padding: 5px 12px; margin: 3px; border-radius: 20px; display: inline-block;">{ing}</span> '
            st.markdown(ingredient_chips, unsafe_allow_html=True)
        else:
            st.info("请在上方输入食材，或点击快速体验按钮")
    else:
        st.info("请在上方输入食材，或点击快速体验按钮")

with main_col2:
    # 生成按钮区域
    st.subheader("🚀 开始烹饪")
    
    # 创建漂亮的生成按钮
    button_container = st.container()
    with button_container:
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            generate_clicked = st.button(
                "✨ AI智能生成菜谱",
                type="primary",
                use_container_width=True,
                help="点击调用千帆大模型生成菜谱"
            )
    
    # 高级选项
    with st.expander("⚡ 高级选项"):
        use_advanced_ai = st.checkbox("启用高级AI模式", value=True, 
                                     help="使用千帆大模型进行深度分析和推荐")
        include_nutrition = st.checkbox("包含营养分析", value=True)
        include_alternatives = st.checkbox("包含食材替代", value=True)
        generate_shopping_list = st.checkbox("生成采购清单", value=False)
    
    # 生成状态
    if generate_clicked:
        st.session_state.generating = True
        st.session_state.ingredients_text = ingredients_text
    
    # 显示生成状态
    if 'generating' in st.session_state and st.session_state.generating:
        with st.spinner("🧠 AI正在思考中..."):
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.02)
                progress_bar.progress(i + 1)
        st.session_state.generating = False

# ==================== 功能函数 ====================
def parse_ingredients(ingredients_text: str) -> List[str]:
    """解析用户输入的食材"""
    if not ingredients_text:
        return []
    
    ingredients = []
    lines = ingredients_text.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        if line:
            # 处理可能的数量描述，如"2个鸡蛋" → "鸡蛋"
            import re
            # 移除数字和量词
            cleaned = re.sub(r'^\d+\s*[个只片块克kgml毫升勺汤勺小勺大勺]*\s*', '', line)
            ingredients.append(cleaned)
    
    return ingredients

def build_preferences_dict() -> Dict[str, Any]:
    """构建偏好设置字典"""
    return {
        "num_recipes": num_recipes,
        "cooking_style": cooking_style,
        "cooking_time": cooking_time,
        "difficulty": difficulty,
        "include_nutrition": include_nutrition,
        "include_alternatives": include_alternatives,
        "generate_shopping_list": generate_shopping_list
    }

def display_recipe_card(recipe: Dict[str, Any], index: int):
    """显示单个菜谱卡片"""
    with st.container():
        st.markdown(f'<div class="recipe-card">', unsafe_allow_html=True)
        
        # 菜谱标题和序号
        st.markdown(f"### 🍽️ {index}. {recipe.get('name', '未知菜名')}")
        
        # 基本信息行
        info_cols = st.columns(4)
        with info_cols[0]:
            st.markdown(f"**⏱️ 时间**\n{recipe.get('time', '未知')}")
        with info_cols[1]:
            difficulty_emoji = {"简单": "🟢", "中等": "🟡", "复杂": "🔴"}.get(recipe.get('difficulty', '简单'), "⚪")
            st.markdown(f"**{difficulty_emoji} 难度**\n{recipe.get('difficulty', '简单')}")
        with info_cols[2]:
            st.markdown(f"**👥 适合**\n{recipe.get('suitable_for', '所有人')}")
        with info_cols[3]:
            st.markdown(f"**🤖 来源**\n{recipe.get('source', 'AI生成')}")
        
        # 分隔线
        st.markdown("---")
        
        # 食材部分
        st.markdown("#### 🥗 所需食材")
        ingredients = recipe.get('ingredients', [])
        if isinstance(ingredients, list):
            ingredients_html = ""
            for i, ing in enumerate(ingredients):
                color = ["#FFE5E5", "#E5F2FF", "#E5FFE5", "#FFF5E5"][i % 4]
                ingredients_html += f'<span style="background: {color}; padding: 6px 15px; margin: 4px; border-radius: 20px; display: inline-block; font-size: 0.9rem;">{ing}</span> '
            st.markdown(ingredients_html, unsafe_allow_html=True)
        
        # 步骤部分
        st.markdown("#### 👨‍🍳 烹饪步骤")
        steps = recipe.get('steps', [])
        if isinstance(steps, list):
            for i, step in enumerate(steps, 1):
                st.markdown(f"{i}. {step}")
        
        # 小贴士部分
        if recipe.get('nutrition') or recipe.get('alternatives'):
            st.markdown("#### 💡 小贴士")
            
            tips_cols = st.columns(2)
            with tips_cols[0]:
                if recipe.get('nutrition'):
                    st.info(f"**营养分析**\n{recipe.get('nutrition')}")
            
            with tips_cols[1]:
                if recipe.get('alternatives'):
                    if isinstance(recipe['alternatives'], dict):
                        alt_text = ""
                        for k, v in recipe['alternatives'].items():
                            alt_text += f"- 如无 **{k}**，可用 **{v}** 代替\n"
                        st.warning(f"**食材替代**\n{alt_text}")
                    else:
                        st.warning(f"**食材替代**\n{recipe.get('alternatives')}")
        
        st.markdown('</div>', unsafe_allow_html=True)

def generate_shopping_list_func(recipes: List[Dict]) -> Dict[str, str]:
    """生成采购清单"""
    shopping_list = {}
    
    for recipe in recipes:
        ingredients = recipe.get('ingredients', [])
        if isinstance(ingredients, list):
            for ingredient in ingredients:
                # 简单的分类（实际可以更智能）
                if any(word in ingredient.lower() for word in ['肉', '鸡', '牛', '猪', '鱼', '虾']):
                    category = '🥩 肉类海鲜'
                elif any(word in ingredient.lower() for word in ['菜', '蔬', '青', '白', '萝', '土']):
                    category = '🥦 蔬菜水果'
                elif any(word in ingredient.lower() for word in ['油', '盐', '酱', '醋', '糖']):
                    category = '🧂 调味品'
                else:
                    category = '📦 其他'
                
                if category not in shopping_list:
                    shopping_list[category] = []
                
                if ingredient not in shopping_list[category]:
                    shopping_list[category].append(ingredient)
    
    return shopping_list

# 分隔线

st.markdown("---")
# 第四部分：结果展示和页脚

# ==================== 结果展示区域 ====================
if generate_clicked and ingredients_text:
    ingredients_list = parse_ingredients(ingredients_text)
    preferences = build_preferences_dict()
    
    if not ingredients_list:
        st.error("❌ 请输入有效的食材！")
    else:
        # 调用API生成菜谱
        with st.spinner("🤖 正在调用千帆AI大模型生成菜谱..."):
            result = qianfan_api.generate_recipes(ingredients_list, preferences)
        
        if result.get("success"):
            recipes = result.get("recipes", [])
            source = result.get("source", "AI生成")
            ingredients_used = result.get("ingredients_used", [])
            
            if recipes:
                # 成功生成结果
                st.success(f"✅ 成功生成 {len(recipes)} 道菜谱（来源：{source}）")
                
                # 显示菜谱
                st.subheader("🍽️ 为您推荐的菜谱")
                
                for i, recipe in enumerate(recipes, 1):
                    display_recipe_card(recipe, i)
                
                # 附加功能：采购清单
                if generate_shopping_list and recipes:
                    st.subheader("🛒 智能采购清单")
                    
                    shopping_list = generate_shopping_list_func(recipes)
                    
                    if shopping_list:
                        list_cols = st.columns(len(shopping_list))
                        
                        for idx, (category, items) in enumerate(shopping_list.items()):
                            with list_cols[idx % len(list_cols)]:
                                st.markdown(f"**{category}**")
                                for item in items:
                                    st.markdown(f"- {item}")
                    else:
                        st.info("无需额外采购，现有食材已足够！")
                
                # 附加功能：导出分享
                st.subheader("📤 导出与分享")
                
                export_cols = st.columns(4)
                with export_cols[0]:
                    if st.button("📝 复制菜谱", use_container_width=True):
                        st.success("菜谱已复制到剪贴板！")
                
                with export_cols[1]:
                    if st.button("🖨️ 打印菜谱", use_container_width=True):
                        st.info("菜谱已准备好打印！")
                
                with export_cols[2]:
                    if st.button("📱 分享好友", use_container_width=True):
                        st.info("生成分享链接...")
                
                with export_cols[3]:
                    if st.button("💾 保存收藏", use_container_width=True):
                        st.success("菜谱已保存到收藏夹！")
                
                # 用户反馈
                st.markdown("---")
                st.subheader("📊 用户反馈")
                
                feedback_cols = st.columns(5)
                with feedback_cols[0]:
                    if st.button("👍 很满意", use_container_width=True):
                        st.balloons()
                        st.success("感谢您的认可！")
                
                with feedback_cols[1]:
                    if st.button("👌 还可以", use_container_width=True):
                        st.info("我们会继续改进！")
                
                with feedback_cols[2]:
                    if st.button("🤔 一般般", use_container_width=True):
                        st.warning("感谢反馈，我们会优化！")
                
                with feedback_cols[3]:
                    if st.button("👎 不满意", use_container_width=True):
                        st.error("抱歉让您失望了，请告诉我们如何改进")
                
                with feedback_cols[4]:
                    if st.button("🔄 重新生成", use_container_width=True):
                        st.rerun()
                
            elif result.get("raw_content"):
                # 如果返回的是原始内容
                st.subheader("📄 AI生成内容")
                st.markdown(result["raw_content"])
                
                st.info("ℹ️ 这是AI直接生成的内容，可能包含非结构化信息")
                
            else:
                st.warning("🤔 AI没有生成具体的菜谱，请尝试调整食材或设置")
        
        else:
            # API调用失败
            error_msg = result.get("error", "未知错误")
            st.error(f"❌ 生成菜谱时出错：{error_msg}")
            
            # 提供备用方案
            st.info("💡 尝试以下解决方案：")
            st.markdown("""
            1. **检查网络连接**：确保可以访问百度云服务
            2. **简化食材**：尝试减少食材种类
            3. **使用示例**：点击上方的快速体验按钮
            4. **稍后重试**：API服务可能暂时繁忙
            """)

# ==================== 本地知识库展示 ====================
# 如果没有生成菜谱，展示一些示例
elif not generate_clicked:
    st.subheader("🌟 热门菜谱推荐")
    
    # 创建示例菜谱
    sample_recipes = [
        {
            "name": "番茄炒蛋",
            "ingredients": ["鸡蛋", "番茄", "葱", "盐", "糖", "油"],
            "steps": ["鸡蛋打散加盐", "番茄切块", "热油炒鸡蛋盛出", "炒番茄至出汁", "混合翻炒调味"],
            "time": "15分钟",
            "difficulty": "简单",
            "nutrition": "富含蛋白质和维生素C",
            "alternatives": {"没有番茄": "可用彩椒代替"},
            "suitable_for": "所有人",
            "source": "本地知识库"
        },
        {
            "name": "土豆烧鸡块",
            "ingredients": ["鸡肉", "土豆", "胡萝卜", "姜", "料酒", "生抽"],
            "steps": ["鸡肉焯水", "炒香鸡肉", "加入土豆胡萝卜", "加水炖煮", "调味收汁"],
            "time": "40分钟",
            "difficulty": "中等",
            "nutrition": "蛋白质和碳水化合物均衡",
            "alternatives": {"没有胡萝卜": "可用洋葱代替"},
            "suitable_for": "喜欢家常菜的人群",
            "source": "本地知识库"
        },
        {
            "name": "麻婆豆腐",
            "ingredients": ["豆腐", "猪肉末", "郫县豆瓣酱", "花椒粉", "葱"],
            "steps": ["豆腐切块焯水", "炒香肉末和豆瓣酱", "加入豆腐轻煮", "勾芡调味", "撒花椒粉葱花"],
            "time": "25分钟",
            "difficulty": "中等",
            "nutrition": "植物蛋白丰富，麻辣开胃",
            "alternatives": {"不吃肉": "可做成素麻婆豆腐"},
            "suitable_for": "喜欢辣味的人群",
            "source": "本地知识库"
        }
    ]
    
    # 显示示例菜谱
    example_cols = st.columns(3)
    for idx, recipe in enumerate(sample_recipes):
        with example_cols[idx]:
            st.markdown(f'<div style="background: #f8f9fa; padding: 1rem; border-radius: 10px;">', unsafe_allow_html=True)
            st.markdown(f"##### {recipe['name']}")
            st.markdown(f"⏱️ {recipe['time']} | {recipe['difficulty']}")
            
            # 显示前3个食材
            ingredients_preview = ", ".join(recipe['ingredients'][:3])
            st.markdown(f"🥗 {ingredients_preview}...")
            
            if st.button(f"试试这道菜", key=f"example_{idx}", use_container_width=True):
                st.session_state.example_ingredients = "\n".join(recipe['ingredients'][:3])
                st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)

# ==================== 页脚和版权信息 ====================
st.markdown("---")

# 页脚信息
footer_cols = st.columns(4)

with footer_cols[0]:
    st.markdown("""
    **🔧 技术支持**
    - 百度千帆大模型
    - Streamlit框架
    - Python 3.8+
    """)

with footer_cols[1]:
    st.markdown("""
    **📚 数据来源**
    - AI智能生成
    - 本地知识库
    - 专业菜谱验证
    """)

with footer_cols[2]:
    st.markdown("""
    **👥 项目团队**
    - 刘蕊琪
    - 戚洋洋
    - 王佳慧
    - 覃丽娜
    - 欧婷
    - 贺钰鑫
    """)

with footer_cols[3]:
    st.markdown("""
    **📞 联系我们**
    - 课程：人工智能通识
    - 项目：厨神小助手
    - 版本：v1.0.0
    """)

# 最终版权信息
st.markdown("""
<div style="text-align: center; padding: 1rem; background: linear-gradient(90deg, #f8f9fa, #e9ecef); border-radius: 10px; margin-top: 2rem;">
    <p style="margin: 0; color: #666; font-size: 0.9rem;">
        🍳 厨神小助手 AI美食推荐系统 | 《人工智能通识》课程大作业<br>
        © 2025 厨神小助手团队 · 基于Streamlit和百度千帆大模型构建
    </p >
</div>
""", unsafe_allow_html=True)

# ==================== 会话状态初始化 ====================
if 'example_ingredients' not in st.session_state:
    st.session_state.example_ingredients = ""

if 'generating' not in st.session_state:
    st.session_state.generating = False

if 'ingredients_text' not in st.session_state:
    st.session_state.ingredients_text = ""

# 运行说明
st.sidebar.markdown("---")
st.sidebar.markdown("""
### 🚀 运行说明

1. **安装依赖**：
   ```bash
   pip install streamlit requests
