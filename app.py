import streamlit as st
import random

# 页面基础配置
st.set_page_config(
    page_title="智能菜谱推荐系统",
    page_icon="🍳",
    layout="wide"
)

# 菜谱数据（包含菜品名称、食材、步骤、配图链接）
RECIPE_DATA = [
    {
        "name": "番茄炒蛋",
        "ingredients": ["番茄2个", "鸡蛋3个", "盐1小勺", "糖半勺", "葱花适量"],
        "steps": [
            "鸡蛋打入碗中，加少许盐打散备用",
            "番茄洗净切块，热锅倒油，倒入蛋液炒至凝固盛出",
            "锅中留底油，放入番茄块翻炒至出汁，加少许糖调味",
            "倒入炒好的鸡蛋，翻炒均匀，加盐调味，撒葱花即可"
        ],
        "image_url": "https://img0.baidu.com/it/u=1825291622,3857401299&fm=253&fmt=auto&app=138&f=JPEG?w=800&h=500"
    },
    {
        "name": "青椒炒肉丝",
        "ingredients": ["猪里脊200g", "青椒3个", "生抽1勺", "料酒1勺", "淀粉1小勺", "盐少许"],
        "steps": [
            "里脊肉切丝，加料酒、生抽、淀粉抓匀腌制10分钟",
            "青椒去籽切丝，热锅倒油，放入肉丝滑炒至变色盛出",
            "锅中留底油，放入青椒丝翻炒至断生",
            "倒入肉丝，加少许盐调味，翻炒均匀即可出锅"
        ],
        "image_url": "https://img1.baidu.com/it/u=3092092129,1710522105&fm=253&fmt=auto&app=138&f=JPEG?w=800&h=533"
    },
    {
        "name": "清炒西兰花",
        "ingredients": ["西兰花1颗", "大蒜3瓣", "盐1小勺", "蚝油1勺", "食用油适量"],
        "steps": [
            "西兰花掰成小朵，焯水1分钟后捞出过凉水",
            "大蒜切末，热锅倒油，放入蒜末爆香",
            "倒入西兰花翻炒2分钟，加盐、蚝油调味",
            "翻炒均匀后即可出锅"
        ],
        "image_url": "https://img2.baidu.com/it/u=2144050690,3122212281&fm=253&fmt=auto&app=138&f=JPEG?w=800&h=600"
    },
    {
        "name": "酸辣土豆丝",
        "ingredients": ["土豆2个", "干辣椒5个", "醋2勺", "盐1小勺", "葱花适量"],
        "steps": [
            "土豆切丝，用清水浸泡去淀粉，沥干水分",
            "热锅倒油，放入干辣椒爆香",
            "倒入土豆丝快速翻炒2分钟",
            "加醋、盐调味，翻炒均匀，撒葱花即可"
        ],
        "image_url": "https://img0.baidu.com/it/u=2770500290,1810711795&fm=253&fmt=auto&app=138&f=JPEG?w=800&h=500"
    },
    {
        "name": "可乐鸡翅",
        "ingredients": ["鸡翅8个", "可乐1罐", "生抽1勺", "老抽半勺", "姜片3片", "料酒1勺"],
        "steps": [
            "鸡翅焯水，加姜片、料酒煮2分钟，捞出沥干",
            "热锅倒油，放入鸡翅煎至两面金黄",
            "倒入可乐、生抽、老抽，大火烧开后转小火",
            "煮至汤汁浓稠，翻炒均匀即可出锅"
        ],
        "image_url": "https://img2.baidu.com/it/u=1509122191,3127330292&fm=253&fmt=auto&app=138&f=JPEG?w=800&h=533"
    }
]

# 侧边栏
st.sidebar.title("🍽️ 菜谱推荐设置")
st.sidebar.markdown("### 选择推荐方式")
recommend_mode = st.sidebar.radio(
    "",
    ["随机推荐", "按食材筛选"]
)

# 食材筛选选项（仅按食材筛选时显示）
selected_ingredient = ""
if recommend_mode == "按食材筛选":
    all_ingredients = []
    for recipe in RECIPE_DATA:
        all_ingredients.extend([i.split(" ")[0] for i in recipe["ingredients"]])
    all_ingredients = list(set(all_ingredients))  # 去重
    selected_ingredient = st.sidebar.selectbox("选择食材", all_ingredients)

# 主页面标题
st.title("🍳 智能菜谱推荐系统")
st.divider()

# 推荐按钮
if st.button("📋 智能推荐菜谱", type="primary"):
    # 筛选菜谱
    if recommend_mode == "随机推荐":
        recommended_recipes = random.sample(RECIPE_DATA, 2)  # 随机推荐2个
    else:
        recommended_recipes = [
            recipe for recipe in RECIPE_DATA 
            if any(selected_ingredient in ing for ing in recipe["ingredients"])
        ]
        if not recommended_recipes:
            st.warning(f"暂无包含「{selected_ingredient}」的菜谱，已为你随机推荐！")
            recommended_recipes = random.sample(RECIPE_DATA, 2)
    
    # 展示推荐结果
    for idx, recipe in enumerate(recommended_recipes):
        st.subheader(f"🥘 推荐菜谱 {idx+1}：{recipe['name']}")
        
        # 分栏展示图片和详情
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.image(
                recipe["image_url"],
                caption=f"{recipe['name']} - 成品图",
                width=300,
                use_column_width=True
            )
        
        with col2:
            st.markdown("#### 📝 食材清单")
            for ing in recipe["ingredients"]:
                st.markdown(f"• {ing}")
            
            st.markdown("#### 👩🍳 烹饪步骤")
            for step_idx, step in enumerate(recipe["steps"]):
                st.markdown(f"{step_idx+1}. {step}")
        
        st.divider()

# 底部说明
st.markdown("---")
st.markdown("### 💡 说明")
st.markdown("本系统支持随机推荐和按食材筛选两种模式，所有菜谱均为家常易做款，适合新手操作！")
