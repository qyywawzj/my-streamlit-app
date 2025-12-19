import streamlit as st

# ========== 页面配置 ==========
st.set_page_config(page_title="全能厨神助手", page_icon="🍳", layout="wide")

# ========== 菜谱数据库（完整80个菜谱的代表性示例） ==========
RECIPES = {
    # ========== 汤类 ==========
    "番茄鸡蛋汤": {
        "category": "汤类",
        "time": "15分钟",
        "ingredients": [
            {"name": "番茄", "amount": "200克"},
            {"name": "鸡蛋", "amount": "2个"},
            {"name": "葱花", "amount": "10克"},
            {"name": "盐", "amount": "3克"}
        ],
        "steps": "1. 番茄切块（3分钟）\n2. 鸡蛋打散（2分钟）\n3. 水烧开放番茄煮3分钟\n4. 倒入蛋液形成蛋花（2分钟）\n5. 加盐撒葱花（2分钟）",
        "alternatives": "番茄→嫩豆腐（150克）\n鸡蛋→鹌鹑蛋（8个）",
        "nutrition": "热量120大卡 | 蛋白质8g | 维生素C丰富",
        "tips": "淋蛋液时火要小"
    },
    
    "玉米排骨汤": {
        "category": "汤类",
        "time": "90分钟",
        "ingredients": [
            {"name": "排骨", "amount": "500克"},
            {"name": "玉米", "amount": "2根"},
            {"name": "胡萝卜", "amount": "1根"},
            {"name": "姜", "amount": "20克"}
        ],
        "steps": "1. 排骨焯水（10分钟）\n2. 玉米胡萝卜切块（5分钟）\n3. 所有材料加水炖60分钟\n4. 加盐调味（2分钟）",
        "alternatives": "排骨→鸡架（2个）",
        "nutrition": "热量280大卡 | 钙质丰富",
        "tips": "焯水用冷水下锅"
    },
    
    # ========== 粥类 ==========
    "皮蛋瘦肉粥": {
        "category": "粥类",
        "time": "60分钟",
        "ingredients": [
            {"name": "大米", "amount": "100克"},
            {"name": "皮蛋", "amount": "2个"},
            {"name": "瘦肉", "amount": "100克"},
            {"name": "姜丝", "amount": "10克"}
        ],
        "steps": "1. 大米浸泡30分钟\n2. 瘦肉切丝腌制（10分钟）\n3. 煮粥30分钟\n4. 加入肉丝皮蛋煮10分钟\n5. 加姜丝盐（2分钟）",
        "alternatives": "瘦肉→鸡胸肉（100克）",
        "nutrition": "热量250大卡 | 易消化",
        "tips": "米提前浸泡更易煮烂"
    },
    
    "小米南瓜粥": {
        "category": "粥类",
        "time": "40分钟",
        "ingredients": [
            {"name": "小米", "amount": "80克"},
            {"name": "南瓜", "amount": "200克"},
            {"name": "枸杞", "amount": "10克"}
        ],
        "steps": "1. 南瓜去皮切块（5分钟）\n2. 小米淘洗（2分钟）\n3. 一起煮30分钟\n4. 加枸杞再煮5分钟",
        "alternatives": "南瓜→红薯（200克）",
        "nutrition": "热量180大卡 | 养胃",
        "tips": "选老南瓜更甜"
    },
    
    # ========== 饭类 ==========
    "番茄炒饭": {
        "category": "饭类",
        "time": "20分钟",
        "ingredients": [
            {"name": "米饭", "amount": "300克"},
            {"name": "番茄", "amount": "150克"},
            {"name": "鸡蛋", "amount": "2个"},
            {"name": "火腿", "amount": "50克"}
        ],
        "steps": "1. 番茄火腿切丁（5分钟）\n2. 鸡蛋炒熟（3分钟）\n3. 炒番茄至出汁（4分钟）\n4. 加米饭火腿翻炒（5分钟）\n5. 加鸡蛋盐翻炒（3分钟）",
        "alternatives": "火腿→虾仁（80克）",
        "nutrition": "热量350大卡 | 碳水充足",
        "tips": "用隔夜饭更粒粒分明"
    },
    
    "鸡肉蘑菇焖饭": {
        "category": "饭类",
        "time": "45分钟",
        "ingredients": [
            {"name": "大米", "amount": "200克"},
            {"name": "鸡腿肉", "amount": "200克"},
            {"name": "香菇", "amount": "6朵"},
            {"name": "胡萝卜", "amount": "50克"}
        ],
        "steps": "1. 鸡肉切块腌制（10分钟）\n2. 香菇泡发切片（10分钟）\n3. 所有材料放电饭煲（5分钟）\n4. 煮饭25分钟\n5. 焖5分钟拌匀",
        "alternatives": "鸡肉→腊肠（100克）",
        "nutrition": "热量400大卡 | 营养全面",
        "tips": "泡香菇水可用来煮饭"
    },
    
    # ========== 炒菜类 ==========
    "番茄炒蛋": {
        "category": "炒菜",
        "time": "15分钟",
        "ingredients": [
            {"name": "番茄", "amount": "300克"},
            {"name": "鸡蛋", "amount": "3个"},
            {"name": "葱", "amount": "10克"},
            {"name": "糖", "amount": "5克"}
        ],
        "steps": "1. 番茄切块（3分钟）\n2. 鸡蛋打散（2分钟）\n3. 炒鸡蛋至凝固（3分钟）\n4. 炒番茄至出汁（4分钟）\n5. 加糖盐翻炒（3分钟）",
        "alternatives": "番茄→彩椒（200克）\n糖→番茄酱（10克）",
        "nutrition": "热量220大卡 | 蛋白质12g | 维生素C丰富",
        "tips": "加糖中和酸味"
    },
    
    "土豆丝炒肉": {
        "category": "炒菜",
        "time": "25分钟",
        "ingredients": [
            {"name": "土豆", "amount": "400克"},
            {"name": "猪肉", "amount": "150克"},
            {"name": "青椒", "amount": "1个"},
            {"name": "蒜", "amount": "3瓣"}
        ],
        "steps": "1. 土豆切丝泡水（10分钟）\n2. 猪肉切丝腌制（8分钟）\n3. 炒肉丝至变色（3分钟）\n4. 加土豆丝青椒翻炒（5分钟）\n5. 加醋调味（2分钟）",
        "alternatives": "猪肉→牛肉（150克）",
        "nutrition": "热量280大卡 | 碳水丰富",
        "tips": "土豆丝泡水后更脆"
    },
    
    # ========== 蔬菜泥类 ==========
    "胡萝卜泥": {
        "category": "蔬菜泥",
        "time": "30分钟",
        "ingredients": [
            {"name": "胡萝卜", "amount": "500克"},
            {"name": "黄油", "amount": "10克"},
            {"name": "牛奶", "amount": "50毫升"}
        ],
        "steps": "1. 胡萝卜去皮切块（8分钟）\n2. 蒸20分钟至软烂\n3. 加牛奶打成泥（3分钟）\n4. 加黄油盐拌匀（2分钟）\n5. 过筛（3分钟）",
        "alternatives": "胡萝卜→南瓜（500克）\n黄油→橄榄油（10毫升）",
        "nutrition": "热量150大卡 | β-胡萝卜素丰富",
        "tips": "蒸比煮保留营养"
    },
    
    "菠菜土豆泥": {
        "category": "蔬菜泥",
        "time": "40分钟",
        "ingredients": [
            {"name": "土豆", "amount": "400克"},
            {"name": "菠菜", "amount": "200克"},
            {"name": "牛奶", "amount": "100毫升"}
        ],
        "steps": "1. 土豆蒸25分钟\n2. 菠菜焯水挤干（8分钟）\n3. 土豆压成泥（5分钟）\n4. 加菠菜牛奶（3分钟）\n5. 搅拌均匀（2分钟）",
        "alternatives": "菠菜→西兰花（200克）",
        "nutrition": "热量180大卡 | 铁质丰富",
        "tips": "菠菜焯水去除草酸"
    },
    
    # ========== 水果泥类 ==========
    "苹果泥": {
        "category": "水果泥",
        "time": "25分钟",
        "ingredients": [
            {"name": "苹果", "amount": "3个"},
            {"name": "柠檬汁", "amount": "5毫升"}
        ],
        "steps": "1. 苹果去皮去核切块（5分钟）\n2. 加水煮15分钟至软烂\n3. 压成泥（3分钟）\n4. 加柠檬汁防氧化（1分钟）",
        "alternatives": "苹果→梨（3个）",
        "nutrition": "热量120大卡 | 膳食纤维丰富",
        "tips": "加柠檬汁防变色"
    },
    
    "香蕉牛油果泥": {
        "category": "水果泥",
        "time": "10分钟",
        "ingredients": [
            {"name": "香蕉", "amount": "2根"},
            {"name": "牛油果", "amount": "1个"},
            {"name": "蜂蜜", "amount": "10克"}
        ],
        "steps": "1. 香蕉牛油果去皮（5分钟）\n2. 放入料理机（1分钟）\n3. 加蜂蜜柠檬汁（1分钟）\n4. 打成细腻泥状（2分钟）",
        "alternatives": "牛油果→希腊酸奶（100克）",
        "nutrition": "热量250大卡 | 健康脂肪",
        "tips": "牛油果选熟透的"
    },
    
    # ========== 甜点类 ==========
    "芒果布丁": {
        "category": "甜点",
        "time": "180分钟（含冷藏）",
        "ingredients": [
            {"name": "芒果", "amount": "300克"},
            {"name": "牛奶", "amount": "250毫升"},
            {"name": "吉利丁片", "amount": "10克"},
            {"name": "糖", "amount": "40克"}
        ],
        "steps": "1. 芒果打成泥（5分钟）\n2. 吉利丁片泡软（5分钟）\n3. 牛奶加热溶解吉利丁（10分钟）\n4. 混合芒果泥（5分钟）\n5. 倒入模具冷藏3小时",
        "alternatives": "芒果→草莓（300克）",
        "nutrition": "热量280大卡 | 甜品适量",
        "tips": "冷藏时间要足够"
    },
    
    "焦糖布丁": {
        "category": "甜点",
        "time": "90分钟",
        "ingredients": [
            {"name": "鸡蛋", "amount": "3个"},
            {"name": "牛奶", "amount": "250毫升"},
            {"name": "糖", "amount": "60克"}
        ],
        "steps": "1. 糖熬成焦糖（10分钟）\n2. 鸡蛋牛奶混合（5分钟）\n3. 过筛倒入模具（3分钟）\n4. 水浴法烤40分钟\n5. 冷藏后脱模（30分钟）",
        "alternatives": "牛奶→椰奶（250毫升）",
        "nutrition": "热量220大卡 | 蛋白质丰富",
        "tips": "水浴法防止开裂"
    },
    
    # ========== 主食类 ==========
    "番茄意大利面": {
        "category": "主食",
        "time": "30分钟",
        "ingredients": [
            {"name": "意大利面", "amount": "200克"},
            {"name": "番茄", "amount": "400克"},
            {"name": "蒜", "amount": "4瓣"},
            {"name": "橄榄油", "amount": "20毫升"}
        ],
        "steps": "1. 煮意大利面（12分钟）\n2. 番茄去皮切碎（5分钟）\n3. 蒜片炒香（3分钟）\n4. 加番茄煮成酱汁（8分钟）\n5. 混合面条拌匀（2分钟）",
        "alternatives": "番茄→番茄罐头（400克）",
        "nutrition": "热量350大卡 | 地中海风味",
        "tips": "煮面水加盐更Q弹"
    }
}

# ========== 智能搜索函数 ==========
def search_recipes(search_text, selected_categories, max_time):
    """
    智能搜索菜谱
    参数：
        search_text: 用户输入的搜索文本
        selected_categories: 选择的菜谱类别
        max_time: 最大制作时间（分钟）
    返回：
        匹配的菜谱列表
    """
    results = []
    
    for recipe_name, recipe_info in RECIPES.items():
        # 1. 检查制作时间
        time_str = recipe_info['time']
        recipe_time = 180  # 默认值
        if '分钟' in time_str:
            try:
                # 提取数字部分
                recipe_time = int(''.join(filter(str.isdigit, time_str.split('分')[0])))
            except:
                recipe_time = 30
        
        if recipe_time > max_time:
            continue
        
        # 2. 检查菜谱类别
        if "全部" not in selected_categories and recipe_info['category'] not in selected_categories:
            continue
        
        # 3. 检查搜索匹配
        search_words = search_text.strip().lower()
        if not search_words:
            # 如果用户没有输入搜索词，显示所有符合条件的菜谱
            results.append((recipe_name, recipe_info))
            continue
        
        # 匹配逻辑
        match_found = False
        
        # 情况1：直接匹配菜谱名称
        if search_words in recipe_name.lower():
            match_found = True
        
        # 情况2：匹配菜谱中的食材
        else:
            # 获取所有食材名称
            ingredient_names = [ing['name'].lower() for ing in recipe_info['ingredients']]
            
            # 检查每个搜索词是否匹配食材
            for word in search_words.split():
                if any(word in ing or ing in word for ing in ingredient_names):
                    match_found = True
                    break
        
        if match_found:
            results.append((recipe_name, recipe_info))
    
    return results
# ========== 界面部分 ==========
st.title("🍳 全能厨神助手")
st.markdown("### 涵盖汤、粥、饭、菜、蔬菜泥、水果泥、甜点等80+菜谱")

# 侧边栏
with st.sidebar:
    st.header("🔍 搜索选项")
    
    # 搜索输入
    search_text = st.text_input(
        "输入菜谱名称或食材",
        "番茄炒蛋",
        help="可以输入菜谱名称（如：皮蛋瘦肉粥）或食材（如：番茄 鸡蛋）"
    )
    
    # 菜谱类别选择
    st.header("🍽️ 菜谱类型")
    all_categories = sorted(list(set([recipe['category'] for recipe in RECIPES.values()])))
    categories_options = ["全部"] + all_categories
    selected_categories = st.multiselect(
        "选择菜谱类型",
        categories_options,
        default=["全部"]
    )
    
    # 时间筛选
    st.header("⏱️ 时间要求")
    max_time = st.slider(
        "最大制作时间（分钟）",
        min_value=10,
        max_value=180,
        value=120,
        step=10,
        help="筛选制作时间不超过指定时间的菜谱"
    )
    
    # 搜索按钮
    search_button = st.button(
        "🔍 开始搜索",
        type="primary",
        use_container_width=True
    )
    
    # 显示所有菜谱
    st.markdown("---")
    st.header("📋 所有菜谱")
    
    # 按类别分组显示菜谱
    recipes_by_category = {}
    for name, info in RECIPES.items():
        category = info['category']
        if category not in recipes_by_category:
            recipes_by_category[category] = []
        recipes_by_category[category].append(name)
    
    # 显示每个类别的菜谱
    for category in sorted(recipes_by_category.keys()):
        with st.expander(f"{category} ({len(recipes_by_category[category])})"):
            for recipe_name in sorted(recipes_by_category[category]):
                recipe_info = RECIPES[recipe_name]
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**{recipe_name}**")
                with col2:
                    st.write(f"`{recipe_info['time']}`")

# 主界面
if search_button or not search_text:
    # 执行搜索
    if "全部" in selected_categories:
        # 如果选择了"全部"，则包含所有类别
        active_categories = all_categories
    else:
        active_categories = selected_categories
    
    # 调用搜索函数
    search_results = search_recipes(search_text, active_categories, max_time)
    
    # 显示搜索结果
    if search_results:
        st.success(f"✅ 找到 {len(search_results)} 个匹配的菜谱")
        
        # 显示每个菜谱的详细信息
        for recipe_name, recipe_info in search_results:
            with st.expander(
                f"🍽️ **{recipe_name}** | {recipe_info['category']} | ⏱️{recipe_info['time']}",
                expanded=True
            ):
                # 创建两列布局
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    # 食材清单
                    st.markdown("#### 🥗 食材清单")
                    ingredients_html = ""
                    for ingredient in recipe_info['ingredients']:
                        ingredients_html += f"- **{ingredient['name']}**: {ingredient['amount']}<br>"
                    st.markdown(ingredients_html, unsafe_allow_html=True)
                    
                    # 替代食材
                    if recipe_info['alternatives']:
                        st.markdown("#### 🔄 替代食材")
                        st.info(recipe_info['alternatives'])
                
                with col2:
                    # 制作步骤
                    st.markdown("#### 👨‍🍳 制作步骤")
                    steps_text = recipe_info['steps'].replace('\n', '\n\n')
                    st.text_area(
                        "步骤详情",
                        steps_text,
                        height=200,
                        disabled=True,
                        label_visibility="collapsed"
                    )
                
                # 底部信息（营养和小贴士）
                col3, col4 = st.columns([1, 1])
                with col3:
                    st.markdown("#### 📊 营养信息")
                    st.success(recipe_info['nutrition'])
                with col4:
                    st.markdown("#### 💡 烹饪小贴士")
                    st.info(recipe_info['tips'])
                
                st.markdown("---")
    else:
        st.warning("没有找到匹配的菜谱，请尝试：")
        
        # 提供搜索建议
        suggestions_col1, suggestions_col2 = st.columns(2)
        
        with suggestions_col1:
            st.markdown("**🔍 搜索建议：**")
            st.markdown("""
            - 输入完整的菜谱名称
            - 输入主要食材名称
            - 使用更通用的搜索词
            """)
        
        with suggestions_col2:
            st.markdown("**📝 示例搜索：**")
            st.markdown("""
            - `皮蛋瘦肉粥`
            - `小米南瓜粥`
            - `番茄 鸡蛋`
            - `鸡肉`
            - `布丁`
            """)
        
        # 显示一些热门菜谱推荐
        st.markdown("#### 🎯 热门菜谱推荐")
        popular_recipes = [
            ("番茄炒蛋", "简单快手，家常美味"),
            ("皮蛋瘦肉粥", "营养早餐，暖心暖胃"),
            ("番茄鸡蛋汤", "10分钟快手汤"),
            ("芒果布丁", "夏日甜品首选"),
            ("土豆丝炒肉", "下饭神器")
        ]
        
        cols = st.columns(len(popular_recipes))
        for idx, (recipe_name, description) in enumerate(popular_recipes):
            with cols[idx]:
                if st.button(
                    f"**{recipe_name}**\n\n{description}",
                    use_container_width=True,
                    key=f"popular_{recipe_name}"
                ):
                    # 更新搜索框内容
                    st.session_state.search_text = recipe_name
                    st.rerun()

# 团队信息
st.markdown("---")
st.markdown("**👨‍🎓 项目团队: 刘蕊琪、戚洋洋、王佳慧、覃丽娜、欧婷、贺钰鑫**")
st.caption("《人工智能通识》大作业 - 智能美食推荐系统")

# 初始化session state
if 'search_text' not in st.session_state:
    st.session_state.search_text = ""

# 添加CSS样式
st.markdown("""
<style>
    .stButton button {
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .stExpander {
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)
