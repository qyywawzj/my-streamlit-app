import streamlit as st
import requests
import json
import re
from collections import defaultdict

# ==================== 配置页面 ====================
st.set_page_config(page_title="?? 厨神AI助手", page_icon="??", layout="wide")

# ==================== 样式美化 ====================
st.markdown("""
<style>
.main-header {font-size:2.5rem; color:#FF6B6B; text-align:center; margin-bottom:1rem;}
.recipe-card {background:#FFF9F9; padding:1.5rem; border-radius:15px; margin-bottom:1.5rem; border-left:5px solid #FF6B6B;}
.ai-tag {background:#E3F2FD; padding:3px 8px; border-radius:10px; font-size:0.8rem; margin:2px;}
</style>
""", unsafe_allow_html=True)

# ==================== 页面标题 ====================
st.markdown('<div class="main-header">?? 厨神AI助手</div>', unsafe_allow_html=True)
st.markdown('<div style="text-align:center; color:#666; margin-bottom:2rem;">智能食材分析 · 个性化推荐 · 精准营养指导</div>', unsafe_allow_html=True)

# ==================== 侧边栏设置 ====================
with st.sidebar:
    st.header("?? 个性化设置")
    cooking_time = st.slider("?? 期望烹饪时间(分钟)", 10, 120, 30)
    difficulty = st.selectbox("????? 烹饪难度", ["新手友好", "家常水平", "高手挑战"])
    health_pref = st.multiselect("?? 健康偏好", ["低脂", "低盐", "高蛋白", "高纤维", "低碳水"])
    st.divider()
    api_key = st.text_input("?? 输入API密钥", value="sk-dfa197f8ee7e41dbab7f467b014e788a", type="password")
    st.caption("使用深度求索AI大模型提供智能服务")

# ==================== 本地知识库（备份） ====================
LOCAL_RECIPES = {
    "番茄炒蛋": {"ingredients": {"番茄": "300g", "鸡蛋": "3个", "葱": "10g", "油": "15ml", "盐": "3g", "糖": "5g"},
              "steps": [("番茄切块", "2分钟"), ("鸡蛋打散加盐", "1分钟"), ("热油炒鸡蛋至凝固", "3分钟"), 
                       ("炒番茄至出汁", "5分钟"), ("混合调味", "2分钟")],
              "substitutes": {"番茄": "圣女果200g", "鸡蛋": "鸭蛋3个"},
              "nutrition": "蛋白质15g, 维生素C丰富, 约250大卡",
              "tags": ["快手菜", "家常", "下饭菜"]},
    "青椒肉丝": {"ingredients": {"猪里脊": "200g", "青椒": "150g", "姜": "10g", "蒜": "10g", "生抽": "15ml", "淀粉": "10g"},
              "steps": [("肉切丝加淀粉腌制", "5分钟"), ("青椒切丝", "3分钟"), ("热油滑炒肉丝", "4分钟"),
                       ("炒香姜蒜", "1分钟"), ("加青椒翻炒", "3分钟"), ("调味出锅", "1分钟")],
              "substitutes": {"猪里脊": "鸡胸肉200g", "青椒": "彩椒150g"},
              "nutrition": "蛋白质25g, 维生素丰富, 约300大卡",
              "tags": ["下饭菜", "家常"]}
}

# ==================== 自然语言处理函数 ====================
def parse_natural_language(text):
    """解析自然语言输入"""
    ingredients = []
    patterns = [
        r'有([\\\\u4e00-\\\\u9fa5]+)和([\\\\u4e00-\\\\u9fa5]+)',
        r'冰箱里有([\\\\u4e00-\\\\u9fa5、]+)',
        r'我想用([\\\\u4e00-\\\\u9fa5、]+)做菜',
        r'([\\\\u4e00-\\\\u9fa5]+)[\\\\s,，、]+([\\\\u4e00-\\\\u9fa5]+)'
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            if isinstance(match, tuple):
                ingredients.extend([m.strip() for m in match if m.strip()])
            else:
                ingredients.append(match.strip())
    
    # 如果没有匹配到模式，按分隔符分割
    if not ingredients:
        separators = r'[、，,\\\\s]+'
        ingredients = [i.strip() for i in re.split(separators, text) if i.strip()]
    
    return list(set(ingredients))[:8]  # 最多8种食材

# ==================== AI调用函数 ====================
def call_ai_api(prompt, api_key):
    """调用DeepSeek API"""
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 1500,
        "temperature": 0.7
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=15)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"API错误: {response.status_code}"
    except Exception as e:
        return f"连接失败: {str(e)}"

# ==================== 智能推荐函数 ====================
def generate_ai_recipe(ingredients, preferences, api_key):
    """生成AI菜谱推荐"""
    prompt = f"""作为米其林三星主厨，请根据以下信息创作菜谱：

可用食材：{', '.join(ingredients)}
用户偏好：烹饪时间{preferences['time']}分钟，难度{preferences['difficulty']}，健康需求：{', '.join(preferences['health'])}

请按以下JSON格式严格输出：
{{
    "dish_name": "创意菜名",
    "ingredients": {{"食材1": "用量(克/毫升)", ...}},
    "steps": [["步骤描述", "所需分钟"], ...],
    "substitutes": {{"可替代食材": "替代方案"}},
    "nutrition": "详细营养分析",
    "tips": ["实用小贴士1", "贴士2"],
    "tags": ["标签1", "标签2"]
}}

要求：
1. 用量精确到克/毫升
2. 步骤时间累计不超过{preferences['time']}分钟
3. 体现{preferences['difficulty']}难度
4. 符合健康需求：{', '.join(preferences['health'])}
5. 给出专业厨师的小贴士"""
    
    return call_ai_api(prompt, api_key)

# ==================== 解析AI响应 ====================
def parse_ai_response(response_text):
    """解析AI返回的JSON"""
    try:
        # 提取JSON部分
        json_match = re.search(r'\\\\{.*\\\\}', response_text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
        return None
    except:
        return None

# ==================== 主界面 ====================
col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("??? 告诉我你有什么食材")
    
    # 输入方式选择
    input_method = st.radio("输入方式:", ["自然语言描述", "直接列出食材"], horizontal=True)
    
    if input_method == "自然语言描述":
        user_input = st.text_area("例如：冰箱里有鸡蛋和番茄，还有一点鸡肉", 
                                  height=100,
                                  placeholder="用自然语言描述你的食材，比如：'我有三个鸡蛋、两个番茄和半斤鸡肉，还有些青椒'")
        if user_input:
            ingredients = parse_natural_language(user_input)
            st.success(f"?? 识别到食材: {', '.join(ingredients)}")
    else:
        ingredients_input = st.text_input("用逗号或空格分隔食材", placeholder="鸡蛋, 番茄, 鸡肉, 青椒")
        ingredients = [i.strip() for i in re.split(r'[,\\\\s]+', ingredients_input) if i.strip()] if ingredients_input else []
    
    # 快速选择
    st.caption("或快速选择:")
    quick_cols = st.columns(4)
    quick_choices = [["鸡蛋", "番茄"], ["鸡肉", "土豆"], ["牛肉", "胡萝卜"], ["豆腐", "青菜"]]
    for idx, col in enumerate(quick_cols):
        with col:
            if st.button(f"组合{idx+1}", use_container_width=True):
                ingredients = quick_choices[idx]

with col2:
    st.subheader("?? 智能推荐")
    if st.button("?? 生成个性化菜谱", type="primary", use_container_width=True):
        if not ingredients:
            st.warning("请先输入食材！")
        elif not api_key.startswith("sk-"):
            st.error("请输入有效的API密钥")
        else:
            with st.spinner("?? AI主厨正在为您精心设计..."):
                # 准备用户偏好
                preferences = {
                    "time": cooking_time,
                    "difficulty": difficulty,
                    "health": health_pref
                }
                
                # 调用AI
                ai_response = generate_ai_recipe(ingredients, preferences, api_key)
                
                # 尝试解析AI响应
                recipe_data = parse_ai_response(ai_response)
                
                if recipe_data:
                    # 显示AI生成的菜谱
                    st.success("? AI为您量身定制了以下菜谱:")
                    
                    with st.container():
                        st.markdown(f'<div class="recipe-card">', unsafe_allow_html=True)
                        
                        # 菜名和标签
                        st.markdown(f"## ??? {recipe_data.get('dish_name', '创意菜品')}")
                        tags_html = " ".join([f'<span class="ai-tag">{tag}</span>' for tag in recipe_data.get('tags', [])])
                        st.markdown(tags_html, unsafe_allow_html=True)
                        
                        st.divider()
                        
                        # 食材部分
                        st.markdown("### ?? 精准食材清单")
                        cols = st.columns(2)
                        for idx, (ing, amount) in enumerate(recipe_data.get('ingredients', {}).items()):
                            with cols[idx % 2]:
                                st.markdown(f"**{ing}**: `{amount}`")
                        
                        # 可替代食材
                        if recipe_data.get('substitutes'):
                            st.markdown("#### ?? 食材替代方案")
                            for orig, sub in recipe_data.get('substitutes', {}).items():
                                st.markdown(f"? **{orig}** → {sub}")
                        
                        st.divider()
                        
                        # 步骤
                        st.markdown("### ????? 详细步骤与时间")
                        total_time = 0
                        for step_num, (step_desc, step_time) in enumerate(recipe_data.get('steps', []), 1):
                            time_match = re.search(r'(\\\\d+)', str(step_time))
                            step_minutes = int(time_match.group(1)) if time_match else 5
                            total_time += step_minutes
                            st.markdown(f"**{step_num}. {step_desc}** - ?? {step_time}")
                        
                        st.markdown(f"**总计烹饪时间**: ?? {total_time}分钟")
                        
                        st.divider()
                        
                        # 营养和小贴士
                        col_nut, col_tip = st.columns(2)
                        with col_nut:
                            st.markdown("### ?? 营养分析")
                            st.info(recipe_data.get('nutrition', '营养信息'))
                        
                        with col_tip:
                            st.markdown("### ?? 主厨小贴士")
                            for tip in recipe_data.get('tips', []):
                                st.markdown(f"? {tip}")
                        
                        st.markdown('</div>', unsafe_allow_html=True)
                else:
                    # 如果AI解析失败，使用本地菜谱
                    st.info("?? AI服务响应中，为您推荐本地精选菜谱:")
                    for dish_name, recipe in LOCAL_RECIPES.items():
                        if any(ing in recipe['ingredients'] for ing in ingredients):
                            with st.container():
                                st.markdown(f'<div class="recipe-card">', unsafe_allow_html=True)
                                st.markdown(f"## ??? {dish_name}")
                                
                                # 显示食材
                                st.markdown("**食材:**")
                                for ing, amount in recipe['ingredients'].items():
                                    st.markdown(f"- {ing}: `{amount}`")
                                
                                # 显示步骤
                                st.markdown("**步骤:**")
                                for step_num, (step_desc, step_time) in enumerate(recipe['steps'], 1):
                                    st.markdown(f"{step_num}. {step_desc} ({step_time})")
                                
                                st.markdown('</div>', unsafe_allow_html=True)
                                break

# ==================== 页脚 ====================
st.divider()
st.markdown("""
<div style="text-align:center; color:#888; padding:1rem;">
    <p>????? 项目团队：刘蕊琪 · 戚洋洋 · 王佳慧 · 覃丽娜 · 欧婷 · 贺钰鑫</p>
    <p>《人工智能通识》大作业 · 厨神AI助手 · 基于DeepSeek大模型</p>
</div>
""", unsafe_allow_html=True)

# ==================== 统计信息 ====================
st.sidebar.divider()
st.sidebar.markdown("?? **系统状态**")
st.sidebar.progress(85, text="AI智能度: 85%")
st.sidebar.caption(f"本地菜谱库: {len(LOCAL_RECIPES)}个")
st.sidebar.caption("AI模型: DeepSeek最新版")
