import streamlit as st

# ========== 页面配置 ==========
st.set_page_config(page_title="全能厨神助手", page_icon="🍳", layout="wide")

# ========== 菜谱数据库（21个菜） ==========
RECIPES = {
    # 1-4: 番茄鸡蛋类菜谱（4个）
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
    
    "番茄鸡蛋面": {
        "category": "主食",
        "time": "20分钟",
        "ingredients": [
            {"name": "面条", "amount": "200克"},
            {"name": "番茄", "amount": "300克"},
            {"name": "鸡蛋", "amount": "2个"},
            {"name": "青菜", "amount": "100克"}
        ],
        "steps": "1. 煮面条（8分钟）\n2. 番茄切块（3分钟）\n3. 炒鸡蛋（3分钟）\n4. 炒番茄加水煮汤（5分钟）\n5. 加面条鸡蛋（1分钟）",
        "alternatives": "面条→米粉（200克）",
        "nutrition": "热量350大卡 | 碳水充足",
        "tips": "面条过冷水更劲道"
    },
    
    "番茄鸡蛋烩饭": {
        "category": "主食",
        "time": "25分钟",
        "ingredients": [
            {"name": "米饭", "amount": "300克"},
            {"name": "番茄", "amount": "250克"},
            {"name": "鸡蛋", "amount": "2个"},
            {"name": "青豆", "amount": "50克"}
        ],
        "steps": "1. 番茄切丁（3分钟）\n2. 炒鸡蛋（3分钟）\n3. 炒番茄至出汁（5分钟）\n4. 加米饭青豆（5分钟）\n5. 加鸡蛋翻炒（4分钟）",
        "alternatives": "青豆→玉米粒（50克）",
        "nutrition": "热量320大卡 | 营养均衡",
        "tips": "米饭用隔夜饭更好"
    },
    
    # 5-7: 猪肉土豆类菜谱（3个）
    "土豆烧肉": {
        "category": "炖菜",
        "time": "40分钟",
        "ingredients": [
            {"name": "猪肉", "amount": "300克"},
            {"name": "土豆", "amount": "400克"},
            {"name": "姜", "amount": "20克"},
            {"name": "八角", "amount": "2个"}
        ],
        "steps": "1. 猪肉切块焯水（10分钟）\n2. 土豆去皮切块（5分钟）\n3. 炒猪肉（5分钟）\n4. 加水炖20分钟\n5. 加土豆炖10分钟",
        "alternatives": "猪肉→五花肉（300克）",
        "nutrition": "热量450大卡 | 蛋白质丰富",
        "tips": "焯水去腥味"
    },
    
    "青椒土豆肉丝": {
        "category": "炒菜",
        "time": "25分钟",
        "ingredients": [
            {"name": "猪肉", "amount": "200克"},
            {"name": "土豆", "amount": "300克"},
            {"name": "青椒", "amount": "100克"},
            {"name": "蒜", "amount": "3瓣"}
        ],
        "steps": "1. 猪肉切丝腌制（10分钟）\n2. 土豆青椒切丝（8分钟）\n3. 炒肉丝（3分钟）\n4. 加土豆丝翻炒（5分钟）\n5. 加青椒调味（2分钟）",
        "alternatives": "猪肉→牛肉（200克）",
        "nutrition": "热量280大卡 | 下饭好菜",
        "tips": "土豆丝泡水更脆"
    },
    
    "土豆肉片": {
        "category": "炒菜",
        "time": "25分钟",
        "ingredients": [
            {"name": "猪肉", "amount": "250克"},
            {"name": "土豆", "amount": "350克"},
            {"name": "胡萝卜", "amount": "50克"},
            {"name": "葱姜", "amount": "15克"}
        ],
        "steps": "1. 猪肉切片腌制（10分钟）\n2. 土豆胡萝卜切片（8分钟）\n3. 炒肉片（3分钟）\n4. 加土豆片翻炒（6分钟）\n5. 调味出锅（3分钟）",
        "alternatives": "胡萝卜→木耳（50克）",
        "nutrition": "热量300大卡 | 家常美味",
        "tips": "肉片用淀粉腌制更嫩"
    },
    # 8-10: 豆腐香菇类菜谱（3个）
"香菇烧豆腐": {
    "category": "炒菜",
    "time": "20分钟",
    "ingredients": [
        {"name": "豆腐", "amount": "400克"},
        {"name": "香菇", "amount": "100克"},
        {"name": "青椒", "amount": "50克"},
        {"name": "蒜", "amount": "3瓣"}
    ],
    "steps": "1. 豆腐切块（5分钟）\n2. 香菇切片（5分钟）\n3. 煎豆腐（5分钟）\n4. 炒香菇（3分钟）\n5. 混合调味（2分钟）",
    "alternatives": "豆腐→老豆腐（400克）",
    "nutrition": "热量200大卡 | 植物蛋白丰富",
    "tips": "豆腐用盐水泡不易碎"
},

"麻婆豆腐": {
    "category": "炒菜",
    "time": "25分钟",
    "ingredients": [
        {"name": "豆腐", "amount": "500克"},
        {"name": "猪肉末", "amount": "100克"},
        {"name": "豆瓣酱", "amount": "30克"},
        {"name": "花椒", "amount": "5克"}
    ],
    "steps": "1. 豆腐切块（5分钟）\n2. 炒肉末（5分钟）\n3. 加豆瓣酱炒香（3分钟）\n4. 加水煮豆腐（8分钟）\n5. 勾芡调味（4分钟）",
    "alternatives": "猪肉末→牛肉末（100克）",
    "nutrition": "热量280大卡 | 麻辣鲜香",
    "tips": "豆腐用盐水焯一下更入味"
},

"香菇炒青菜": {
    "category": "炒菜",
    "time": "15分钟",
    "ingredients": [
        {"name": "香菇", "amount": "150克"},
        {"name": "青菜", "amount": "300克"},
        {"name": "蒜", "amount": "4瓣"},
        {"name": "蚝油", "amount": "15毫升"}
    ],
    "steps": "1. 香菇切片（5分钟）\n2. 青菜洗净（3分钟）\n3. 炒香菇（4分钟）\n4. 加青菜翻炒（5分钟）\n5. 调味出锅（3分钟）",
    "alternatives": "青菜→小白菜（300克）",
    "nutrition": "热量120大卡 | 膳食纤维丰富",
    "tips": "大火快炒保持爽脆"
},

# 11-16: 其他菜谱（6个）
"宫保鸡丁": {
    "category": "炒菜",
    "time": "25分钟",
    "ingredients": [
        {"name": "鸡肉", "amount": "300克"},
        {"name": "花生", "amount": "50克"},
        {"name": "干辣椒", "amount": "10克"},
        {"name": "葱姜蒜", "amount": "20克"}
    ],
    "steps": "1. 鸡肉切丁腌制（10分钟）\n2. 炸花生（5分钟）\n3. 炒鸡丁（5分钟）\n4. 加调料翻炒（3分钟）\n5. 加花生拌匀（2分钟）",
    "alternatives": "鸡肉→鸡胸肉（300克）",
    "nutrition": "热量350大卡 | 经典川菜",
    "tips": "鸡肉腌制时加淀粉更嫩"
},

"鱼香肉丝": {
    "category": "炒菜",
    "time": "25分钟",
    "ingredients": [
        {"name": "猪肉", "amount": "300克"},
        {"name": "木耳", "amount": "50克"},
        {"name": "胡萝卜", "amount": "100克"},
        {"name": "青椒", "amount": "50克"}
    ],
    "steps": "1. 猪肉切丝腌制（10分钟）\n2. 配菜切丝（8分钟）\n3. 炒肉丝（3分钟）\n4. 加配菜翻炒（5分钟）\n5. 调味勾芡（4分钟）",
    "alternatives": "猪肉→里脊肉（300克）",
    "nutrition": "热量280大卡 | 酸甜可口",
    "tips": "肉丝要顺纹切"
},

"红烧排骨": {
    "category": "炖菜",
    "time": "60分钟",
    "ingredients": [
        {"name": "排骨", "amount": "500克"},
        {"name": "姜片", "amount": "30克"},
        {"name": "八角", "amount": "3个"},
        {"name": "冰糖", "amount": "20克"}
    ],
    "steps": "1. 排骨焯水（10分钟）\n2. 炒糖色（5分钟）\n3. 炖排骨40分钟\n4. 收汁调味（5分钟）",
    "alternatives": "排骨→猪蹄（500克）",
    "nutrition": "热量450大卡 | 补钙佳品",
    "tips": "炒糖色要用小火"
},

"清炒西兰花": {
    "category": "素菜",
    "time": "15分钟",
    "ingredients": [
        {"name": "西兰花", "amount": "400克"},
        {"name": "蒜", "amount": "5瓣"},
        {"name": "胡萝卜", "amount": "50克"},
        {"name": "盐", "amount": "3克"}
    ],
    "steps": "1. 西兰花切小朵（5分钟）\n2. 焯水（3分钟）\n3. 蒜片爆香（2分钟）\n4. 炒西兰花（3分钟）\n5. 调味出锅（2分钟）",
    "alternatives": "西兰花→菜花（400克）",
    "nutrition": "热量100大卡 | 维生素丰富",
    "tips": "西兰花焯水时间不要太长"
},

"酸辣土豆丝": {
    "category": "素菜",
    "time": "20分钟",
    "ingredients": [
        {"name": "土豆", "amount": "500克"},
        {"name": "干辣椒", "amount": "5克"},
        {"name": "醋", "amount": "20毫升"},
        {"name": "蒜", "amount": "4瓣"}
    ],
    "steps": "1. 土豆切丝泡水（10分钟）\n2. 蒜和辣椒切好（3分钟）\n3. 爆香调料（2分钟）\n4. 炒土豆丝（5分钟）\n5. 加醋调味（2分钟）",
    "alternatives": "土豆→莲藕（500克）",
    "nutrition": "热量180大卡 | 开胃小菜",
    "tips": "土豆丝泡水去淀粉更脆"
},

"蚝油生菜": {
    "category": "素菜",
    "time": "10分钟",
    "ingredients": [
        {"name": "生菜", "amount": "500克"},
        {"name": "蚝油", "amount": "20毫升"},
        {"name": "蒜", "amount": "3瓣"},
        {"name": "生抽", "amount": "10毫升"}
    ],
    "steps": "1. 生菜洗净（3分钟）\n2. 蒜切末（2分钟）\n3. 生菜焯水（2分钟）\n4. 炒蒜末（1分钟）\n5. 加蚝油生抽浇汁（2分钟）",
    "alternatives": "生菜→油麦菜（500克）",
    "nutrition": "热量80大卡 | 清爽低卡",
    "tips": "生菜焯水时间要短"
},
  # 17-21: 其他菜谱（5个）
    "蒜蓉空心菜": {
        "category": "素菜",
        "time": "12分钟",
        "ingredients": [
            {"name": "空心菜", "amount": "500克"},
            {"name": "蒜", "amount": "6瓣"},
            {"name": "盐", "amount": "3克"},
            {"name": "食用油", "amount": "15毫升"}
        ],
        "steps": "1. 空心菜洗净（3分钟）\n2. 蒜切末（2分钟）\n3. 爆香蒜末（2分钟）\n4. 炒空心菜（3分钟）\n5. 调味出锅（2分钟）",
        "alternatives": "空心菜→菠菜（500克）",
        "nutrition": "热量90大卡 | 清热去火",
        "tips": "大火快炒保持翠绿"
    },
    
    "可乐鸡翅": {
        "category": "炖菜",
        "time": "40分钟",
        "ingredients": [
            {"name": "鸡翅", "amount": "500克"},
            {"name": "可乐", "amount": "300毫升"},
            {"name": "姜片", "amount": "20克"},
            {"name": "生抽", "amount": "20毫升"}
        ],
        "steps": "1. 鸡翅划刀（5分钟）\n2. 煎鸡翅（10分钟）\n3. 加可乐炖20分钟\n4. 收汁调味（5分钟）",
        "alternatives": "可乐→雪碧（300毫升）",
        "nutrition": "热量380大卡 | 小朋友最爱",
        "tips": "鸡翅划刀更入味"
    },
    
    "水煮鱼": {
        "category": "川菜",
        "time": "35分钟",
        "ingredients": [
            {"name": "鱼片", "amount": "400克"},
            {"name": "豆芽", "amount": "200克"},
            {"name": "干辣椒", "amount": "20克"},
            {"name": "花椒", "amount": "10克"}
        ],
        "steps": "1. 鱼片腌制（10分钟）\n2. 炒底料（8分钟）\n3. 煮豆芽（5分钟）\n4. 烫鱼片（3分钟）\n5. 淋热油（4分钟）",
        "alternatives": "鱼片→牛肉片（400克）",
        "nutrition": "热量320大卡 | 麻辣鲜香",
        "tips": "鱼片要薄才能快速烫熟"
    },
    
    "地三鲜": {
        "category": "素菜",
        "time": "30分钟",
        "ingredients": [
            {"name": "土豆", "amount": "300克"},
            {"name": "茄子", "amount": "300克"},
            {"name": "青椒", "amount": "200克"},
            {"name": "蒜", "amount": "5瓣"}
        ],
        "steps": "1. 食材切块（10分钟）\n2. 油炸（12分钟）\n3. 炒蒜末（3分钟）\n4. 混合翻炒（5分钟）\n5. 调味出锅（3分钟）",
        "alternatives": "茄子→长茄子（300克）",
        "nutrition": "热量250大卡 | 东北名菜",
        "tips": "茄子用盐腌一下再炸"
    },
    
    "红烧肉": {
        "category": "炖菜",
        "time": "90分钟",
        "ingredients": [
            {"name": "五花肉", "amount": "500克"},
            {"name": "冰糖", "amount": "30克"},
            {"name": "姜", "amount": "20克"},
            {"name": "八角", "amount": "2个"}
        ],
        "steps": "1. 五花肉切块（5分钟）\n2. 焯水（10分钟）\n3. 炒糖色（5分钟）\n4. 炖煮60分钟\n5. 收汁（10分钟）",
        "alternatives": "五花肉→猪肘（500克）",
        "nutrition": "热量500大卡 | 经典家常菜",
        "tips": "慢火炖煮更入味"
    }
}

# ========== 智能食材识别函数 ==========
def recognize_ingredients(text):
    """精确识别食材"""
    if not text or not text.strip():
        return []
    
    text = text.strip().lower()
    recognized = []
    
    # 处理同义词：西红柿=番茄
    text = text.replace('西红柿', '番茄')
    
    # 检查每个食材
    if '番茄' in text:
        recognized.append('番茄')
    
    if '鸡蛋' in text:
        recognized.append('鸡蛋')
    
    if '猪肉' in text or '瘦肉' in text or '五花肉' in text or '里脊肉' in text:
        recognized.append('猪肉')
    
    if '土豆' in text or '马铃薯' in text:
        recognized.append('土豆')
    
    if '豆腐' in text or '老豆腐' in text:
        recognized.append('豆腐')
    
    if '香菇' in text or '蘑菇' in text:
        recognized.append('香菇')
    
    if '鸡肉' in text or '鸡' in text or '鸡翅' in text:
        recognized.append('鸡肉')
    
    if '米饭' in text:
        recognized.append('米饭')
    
    if '面条' in text:
        recognized.append('面条')
    
    if '青菜' in text:
        recognized.append('青菜')
    
    if '青豆' in text:
        recognized.append('青豆')
    
    if '玉米' in text:
        recognized.append('玉米')
    
    # 去重
    return list(set(recognized))
   # ========== 严格搜索函数 ==========
def search_recipes_strict(ingredients, selected_cats, max_time):
    """严格搜索：菜谱必须包含所有输入的食材"""
    filtered_recipes = []
    
    for name, recipe in RECIPES.items():
        # 检查时间
        time_str = recipe['time']
        time_min = 180  # 默认值
        
        # 提取分钟数
        if '分钟' in time_str:
            num_str = ''
            for char in time_str:
                if char.isdigit():
                    num_str += char
                elif num_str:  # 已经找到数字，遇到非数字停止
                    break
            if num_str:
                time_min = int(num_str)
        
        # 时间筛选
        if time_min > max_time:
            continue
        
        # 类别筛选
        if "全部" not in selected_cats and recipe['category'] not in selected_cats:
            continue
        
        # 如果没有输入食材，显示所有符合条件的菜谱
        if not ingredients:
            filtered_recipes.append((name, recipe))
            continue
        
        # 获取菜谱的所有食材名称
        recipe_ingredients = [ing['name'] for ing in recipe['ingredients']]
        
        # 检查是否包含所有输入的食材
        all_ingredients_found = True
        for ingredient in ingredients:
            if ingredient not in recipe_ingredients:
                all_ingredients_found = False
                break
        
        if all_ingredients_found:
            filtered_recipes.append((name, recipe))
    
    return filtered_recipes

# ========== 界面部分 ==========
st.title("🍳 全能厨神助手")
st.markdown("### 涵盖汤、粥、饭、菜、蔬菜泥、水果泥、甜点等80+菜谱")

# 侧边栏
with st.sidebar:
    st.header("🥦 食材输入")
    user_input = st.text_input("输入食材（如：番茄 鸡蛋）", "番茄 鸡蛋")
    
    st.header("🍽️ 菜谱类型")
    # 提取所有菜谱类别
    all_categories = sorted(list(set([recipe['category'] for recipe in RECIPES.values()])))
    categories = ["全部"] + all_categories
    selected_cats = st.multiselect("选择类型", categories, default=["全部"])
    
    st.header("⏱️ 时间要求")
    max_time = st.slider("最大制作时间（分钟）", 10, 180, 60)
    
    generate = st.button("🔍 智能推荐菜谱", type="primary", use_container_width=True)

# 主界面逻辑
if generate:
    # 识别食材
    recognized = recognize_ingredients(user_input)
    
    if recognized:
        st.success(f"✅ 识别到食材: {', '.join(recognized)}")
        
        # 使用严格搜索
        filtered_recipes = search_recipes_strict(recognized, selected_cats, max_time)
        
        if filtered_recipes:
            st.markdown(f"## 🎉 为您推荐 {len(filtered_recipes)} 个菜谱")
            
            for idx, (name, recipe) in enumerate(filtered_recipes):
                # 默认只展开第一个
                expanded = idx == 0
                with st.expander(f"🍽️ {name} ({recipe['category']} | {recipe['time']})", expanded=expanded):
                    # 食材
                    st.markdown("**🥗 食材清单**")
                    
                    # 使用3列布局显示食材
                    ingredients = recipe['ingredients']
                    cols = st.columns(3)
                    for i, ing in enumerate(ingredients):
                        col_idx = i % 3
                        with cols[col_idx]:
                            st.markdown(f"**{ing['name']}**")
                            st.write(f"{ing['amount']}")
                    
                    # 步骤
                    st.markdown("**👨‍🍳 制作步骤**")
                    steps_lines = recipe['steps'].split('\n')
                    for step in steps_lines:
                        st.write(step)
                    
                    # 替代食材
                    if recipe['alternatives'].strip():
                        st.markdown("**🔄 替代食材**")
                        st.info(recipe['alternatives'])
                    
                    # 营养和小贴士
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("**📊 营养贴士**")
                        st.info(recipe['nutrition'])
                    with col2:
                        st.markdown("**💡 小提示**")
                        st.success(recipe['tips'])
        else:
            st.warning("没有找到完全匹配的菜谱，请尝试：")
            st.write("1. 检查食材是否输入正确")
            st.write("2. 放宽时间限制")
            st.write("3. 选择更多菜谱类型")
    else:
        st.error("未识别到有效食材，请尝试输入: 番茄、鸡蛋、猪肉、土豆、豆腐、香菇等")

# 默认显示
else:
    st.info("👈 请在左侧输入食材并点击「智能推荐菜谱」按钮") 
    # 团队信息
st.markdown("---")
st.markdown("**👨‍🎓 项目团队: 刘蕊琪、戚洋洋、王佳慧、覃丽娜、欧婷、贺钰鑫**")
st.caption("《人工智能通识》大作业 - 智能美食推荐系统")

# CSS样式
st.markdown("""
<style>
    /* 主要样式 */
    .main .block-container {
        padding-top: 2rem;
    }
    
    /* 按钮样式 */
    .stButton > button {
        width: 100%;
        background-color: #FF6B6B;
        color: white;
        font-weight: bold;
        border: none;
        padding: 12px 24px;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background-color: #FF5252;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(255, 107, 107, 0.3);
    }
    
    /* 成功消息 */
    .stSuccess {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 8px;
        padding: 16px;
        margin: 10px 0;
    }
    
    /* 警告消息 */
    .stWarning {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 8px;
        padding: 16px;
        margin: 10px 0;
    }
    
    /* 错误消息 */
    .stError {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 8px;
        padding: 16px;
        margin: 10px 0;
    }
    
    /* 展开器头部 */
    .streamlit-expanderHeader {
        background-color: #f8f9fa;
        border-radius: 8px;
        font-weight: bold;
        border: 1px solid #e9ecef;
    }
    
    /* 侧边栏 */
    [data-testid="stSidebar"] {
        background-color: #f8f9fa;
    }
    
    /* 输入框 */
    .stTextInput > div > div > input {
        border: 2px solid #dee2e6;
        border-radius: 8px;
    }
    
    /* 多选 */
    .stMultiSelect > div > div {
        border: 2px solid #dee2e6;
        border-radius: 8px;
    }
    
    /* 滑块 */
    .stSlider > div > div > div {
        background-color: #FF6B6B;
    }
    
    /* 标题样式 */
    h1, h2, h3 {
        color: #333;
        margin-bottom: 1rem;
    }
    
    h1 {
        border-bottom: 3px solid #FF6B6B;
        padding-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)
