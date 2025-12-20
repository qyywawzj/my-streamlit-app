import streamlit as st
from datetime import datetime

# ====================== 页面样式配置 ======================
def set_page_style():
    st.set_page_config(
        page_title="10道核心菜谱助手",
        page_icon="🍳",
        layout="centered",
        initial_sidebar_state="expanded"
    )
    st.markdown("""
    <style>
    .main-header {
        color: #FF6B6B;
        text-align: center;
        padding: 10px 0;
        font-size: 2rem;
    }
    .subtitle {
        text-align: center;
        color: #666;
        margin-bottom: 20px;
        font-size: 1.1rem;
    }
    .recipe-card {
        background-color: white;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 20px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .recipe-name {
        color: #333;
        font-size: 1.3rem;
        margin-top: 10px;
        margin-bottom: 5px;
    }
    .recipe-info {
        color: #666;
        font-size: 0.9rem;
        margin-bottom: 10px;
    }
    .team-section {
        text-align: center;
        margin-top: 30px;
        padding-top: 20px;
        border-top: 1px solid #eee;
    }
    .team-header {
        color: #555;
        margin-bottom: 10px;
    }
    .team-member {
        display: inline-block;
        margin: 5px;
        padding: 5px 10px;
        background-color: #f0f7ff;
        border-radius: 5px;
        font-size: 0.9rem;
    }
    .course-info {
        color: #888;
        font-size: 0.9rem;
        margin-top: 10px;
    }
    .tip-text {color: #27ae60; font-size: 14px; line-height: 1.6;}
    .nutri-text {color: #3498db; font-size: 14px;}
    .stExpander {
        border-radius: 10px;
        margin: 10px 0;
        border: 1px solid #f0f0f0;
    }
    .stImage {
        border-radius: 8px;
        margin: 5px 0;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# ====================== 10道核心菜谱数据库 ======================
def get_core_recipes():
    CORE_RECIPES = {
        # ========== 土豆猪肉系列（4道） ==========
        "土豆丝炒肉": {
            "category": "炒菜",
            "time": "25分钟",
            "img_url": "https://images.unsplash.com/photo-1563245372-f21724e3856d?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
            "ingredients": [
                {"name": "土豆", "amount": "400g"},
                {"name": "猪肉里脊", "amount": "150g"},
                {"name": "青椒", "amount": "1个"},
                {"name": "香醋", "amount": "10ml"},
                {"name": "蒜末", "amount": "3瓣"}
            ],
            "steps": [
                "土豆切丝，清水浸泡10分钟去淀粉，沥干",
                "猪肉切丝，加生抽、淀粉腌制8分钟",
                "热锅冷油，滑炒肉丝至变色盛出",
                "留底油爆香蒜末、青椒，加土豆丝大火快炒3分钟",
                "倒回肉丝，淋香醋、加盐翻炒均匀出锅"
            ],
            "tips": ["大火快炒保脆爽，避免出水", "香醋最后放，香味不挥发"],
            "nutrition": {"热量": "280大卡", "蛋白质": "15g", "碳水": "35g"}
        },
        "土豆烧肉": {
            "category": "炒菜",
            "time": "40分钟",
            "img_url": "https://images.unsplash.com/photo-1594046243098-4d6c0475d0f8?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
            "ingredients": [
                {"name": "土豆", "amount": "300g"},
                {"name": "五花肉", "amount": "200g"},
                {"name": "八角", "amount": "1个"},
                {"name": "冰糖", "amount": "5g"},
                {"name": "姜片", "amount": "3片"}
            ],
            "steps": [
                "五花肉切块，冷水下锅加姜片焯水，撇沫捞出沥干",
                "土豆切块，清水浸泡防氧化",
                "热锅冷油，小火炒冰糖至浅褐色，加五花肉裹糖色",
                "加生抽、老抽翻炒上色，加热水没过肉，焖20分钟",
                "加土豆块焖15分钟，大火收汁加盐调味"
            ],
            "tips": ["加热水防肉质变柴", "土豆晚放，避免煮烂"],
            "nutrition": {"热量": "380大卡", "蛋白质": "18g", "碳水": "25g"}
        },
                "土豆猪肉粥": {
            "category": "粥类",
            "time": "50分钟",
            "img_url": "https://images.unsplash.com/photo-1563245372-f21724e3856d?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
            "ingredients": [
                {"name": "大米", "amount": "100g"},
                {"name": "土豆", "amount": "150g"},
                {"name": "猪肉瘦肉", "amount": "100g"},
                {"name": "姜丝", "amount": "5g"},
                {"name": "葱花", "amount": "5g"}
            ],
            "steps": [
                "大米淘洗后浸泡30分钟，口感更软糯",
                "猪肉切丝，加姜丝、少许盐腌制10分钟",
                "土豆切丁，清水浸泡去淀粉",
                "锅中加1000ml水烧开，放大米小火煮20分钟",
                "加土豆丁煮10分钟，再放肉丝煮5分钟",
                "加盐、白胡椒粉调味，撒葱花淋香油"
            ],
            "tips": ["煮粥全程搅拌防粘锅", "肉丝别煮太久，避免变老"],
            "nutrition": {"热量": "260大卡", "蛋白质": "12g", "碳水": "40g"}
        },
        "土豆猪肉焖饭": {
            "category": "饭类",
            "time": "45分钟",
            "img_url": "https://images.unsplash.com/photo-1563245372-f21724e3856d?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
            "ingredients": [
                {"name": "大米", "amount": "200g"},
                {"name": "土豆", "amount": "200g"},
                {"name": "猪肉丁", "amount": "150g"},
                {"name": "生抽", "amount": "15ml"},
                {"name": "蚝油", "amount": "5ml"}
            ],
            "steps": [
                "大米淘洗，加水浸泡10分钟，水量比平时少1cm",
                "猪肉丁加生抽、老抽、蚝油腌制10分钟",
                "土豆切丁，清水浸泡防氧化",
                "热锅冷油，爆香姜片，加猪肉丁炒至变色",
                "加土豆丁翻炒均匀，倒入电饭煲铺在大米上",
                "启动煮饭程序，结束后焖5分钟，搅拌均匀即可"
            ],
            "tips": ["水量减少防米饭软烂", "肉菜炒香后焖饭更入味"],
            "nutrition": {"热量": "350大卡", "蛋白质": "15g", "碳水": "50g"}
        },
        # ========== 番茄鸡蛋系列（3道） ==========
        "番茄炒蛋": {
            "category": "炒菜",
            "time": "15分钟",
            "img_url": "https://images.unsplash.com/photo-1593909011743-40b2a5c3eb5e?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
            "ingredients": [
                {"name": "番茄", "amount": "300g"},
                {"name": "鸡蛋", "amount": "3个"},
                {"name": "白糖", "amount": "5g"},
                {"name": "盐", "amount": "3g"},
                {"name": "葱花", "amount": "5g"}
            ],
            "steps": [
                "番茄顶部划十字，开水烫去皮切块",
                "鸡蛋打散，加少许盐搅匀",
                "热锅冷油，倒入蛋液炒至金黄结块，盛出备用",
                "留底油，放番茄块翻炒出汁，加白糖中和酸味",
                "倒回鸡蛋，加盐翻炒均匀，撒葱花出锅"
            ],
            "tips": ["鸡蛋炒老一点更香", "白糖量随番茄酸度调整"],
            "nutrition": {"热量": "220大卡", "蛋白质": "15g", "碳水": "15g"}
        },
        "番茄鸡蛋汤": {
            "category": "汤类",
            "time": "15分钟",
            "img_url": "https://images.unsplash.com/photo-1593909011743-40b2a5c3eb5e?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
            "ingredients": [
                {"name": "番茄", "amount": "200g"},
                {"name": "鸡蛋", "amount": "2个"},
                {"name": "葱花", "amount": "10g"},
                {"name": "盐", "amount": "3g"},
                {"name": "水淀粉", "amount": "10ml"}
            ],
            "steps": [
                "番茄去皮切块，鸡蛋打散备用",
                "热锅冷油，炒番茄块出汁，加500ml清水烧开",
                "转大火，沿锅边缓慢淋入蛋液，形成均匀蛋花",
                "淋水淀粉勾薄芡，加盐调味，撒葱花出锅"
            ],
            "tips": ["火大蛋花更均匀", "番茄去皮口感更佳"],
            "nutrition": {"热量": "120大卡", "蛋白质": "8g", "碳水": "10g"}
        },
        "番茄鸡蛋豆腐羹": {
            "category": "汤羹",
            "time": "20分钟",
            "img_url": "https://images.unsplash.com/photo-1593909011743-40b2a5c3eb5e?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
            "ingredients": [
                {"name": "番茄", "amount": "1个"},
                {"name": "鸡蛋", "amount": "1个"},
                {"name": "嫩豆腐", "amount": "150g"},
                {"name": "盐", "amount": "2g"},
                {"name": "香油", "amount": "2ml"}
            ],
            "steps": [
                "番茄去皮切丁，嫩豆腐切小块，鸡蛋打散",
                "锅中加清水烧开，放番茄丁煮3分钟出汁",
                "加豆腐块煮5分钟，淋入蛋液搅拌成蛋花",
                "水淀粉勾薄芡，加盐调味，淋香油撒葱花"
            ],
            "tips": ["豆腐轻轻推，避免搅碎", "勾薄芡口感更顺滑"],
            "nutrition": {"热量": "150大卡", "蛋白质": "12g", "碳水": "8g"}
        },
        # ========== 豆腐香菇系列（3道） ==========
        "香菇豆腐汤": {
            "category": "汤类",
            "time": "25分钟",
            "img_url": "https://images.unsplash.com/photo-1547592180-85f173990554?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
            "ingredients": [
                {"name": "嫩豆腐", "amount": "250g"},
                {"name": "香菇", "amount": "4朵"},
                {"name": "青菜", "amount": "30g"},
                {"name": "盐", "amount": "3g"},
                {"name": "鸡精", "amount": "1g"}
            ],
            "steps": [
                "香菇泡发后切片，嫩豆腐切小块焯水防碎",
                "锅中加清水烧开，放香菇片煮10分钟出香味",
                "加豆腐块煮5分钟，放入青菜煮2分钟至断生",
                "加盐、鸡精调味，淋少许香油出锅"
            ],
            "tips": ["豆腐焯水去豆腥味", "后放盐，豆腐不易碎"],
            "nutrition": {"热量": "90大卡", "蛋白质": "8g", "碳水": "5g"}
        },
        "香菇酿豆腐": {
            "category": "蒸菜",
            "time": "30分钟",
            "img_url": "https://images.unsplash.com/photo-1547592180-85f173990554?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
            "ingredients": [
                {"name": "北豆腐", "amount": "300g"},
                {"name": "香菇", "amount": "6朵"},
                {"name": "猪肉馅", "amount": "100g"},
                {"name": "生抽", "amount": "10ml"},
                {"name": "蚝油", "amount": "5ml"}
            ],
            "steps": [
                "香菇泡发切碎，和猪肉馅、生抽、蚝油拌匀成馅料",
                "北豆腐切成小块，中间挖小坑，填入馅料",
                "蒸锅上汽后，放入豆腐蒸15分钟",
                "锅中加少许清水、生抽、蚝油烧开，水淀粉勾芡，淋在豆腐上"
            ],
            "tips": ["豆腐选北豆腐，不易碎", "馅料可加葱花提香"],
            "nutrition": {"热量": "220大卡", "蛋白质": "18g", "碳水": "10g"}
        },
        "香菇豆腐炒青菜": {
            "category": "炒菜",
            "time": "20分钟",
            "img_url": "https://images.unsplash.com/photo-1547592180-85f173990554?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
            "ingredients": [
                {"name": "香菇", "amount": "6朵"},
                {"name": "北豆腐", "amount": "300g"},
                {"name": "上海青", "amount": "200g"},
                {"name": "蚝油", "amount": "10ml"},
                {"name": "盐", "amount": "2g"}
            ],
            "steps": [
                "香菇切片焯水，北豆腐切块煎至两面金黄盛出",
                "热锅冷油，炒香菇片出香味，加上海青炒至断生",
                "倒回煎好的豆腐块，淋蚝油、加盐翻炒均匀",
                "撒少许蒜末，翻炒两下出锅"
            ],
            "tips": ["豆腐煎定型再炒，不易碎", "青菜断生即可，保持脆嫩"],
            "nutrition": {"热量": "150大卡", "蛋白质": "12g", "碳水": "8g"}
        }
    }
    return CORE_RECIPES

# ====================== 筛选与页面渲染 ======================
def render_recipes():
    set_page_style()
    recipes = get_core_recipes()
    
    st.markdown('<h1 class="main-header">🍳 10道核心菜谱助手</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">简单食材 · 精准做法 · 营养搭配</p>', unsafe_allow_html=True)
    
    st.info(f"💡 当前共有 {len(recipes)} 道核心菜谱，涵盖多种烹饪方式")
    
    # 侧边栏筛选
    with st.sidebar:
        st.header("🔍 筛选条件")
        
        # 系列筛选
        st.subheader("菜品系列")
        series_options = ["全部", "土豆猪肉系列", "番茄鸡蛋系列", "豆腐香菇系列"]
        selected_series = st.selectbox("选择菜品系列", series_options)
                # 烹饪类型筛选
        st.subheader("烹饪类型")
        cook_types = set([data["category"] for data in recipes.values()])
        type_options = ["全部"] + sorted(list(cook_types))
        selected_type = st.selectbox("选择烹饪类型", type_options)
        
        # 烹饪时间筛选
        st.subheader("烹饪时间")
        time_filter = st.slider("最大烹饪时间（分钟）", 15, 60, 60)
        
        # 食材搜索
        st.subheader("食材搜索")
        search_ingredient = st.text_input("输入食材名称（如：土豆、鸡蛋）")
        
        # 重置按钮
        if st.button("🔄 重置筛选条件"):
            st.rerun()
    
    # 筛选逻辑
    filtered_recipes = []
    for name, data in recipes.items():
        # 系列筛选
        series_flag = True
        if selected_series == "土豆猪肉系列":
            series_flag = ("土豆" in name) and ("猪肉" in name)
        elif selected_series == "番茄鸡蛋系列":
            series_flag = ("番茄" in name) and ("鸡蛋" in name)
        elif selected_series == "豆腐香菇系列":
            series_flag = ("豆腐" in name) and ("香菇" in name)
        
        # 类型筛选
        type_flag = (selected_type == "全部") or (data["category"] == selected_type)
        
        # 时间筛选
        time_str = data["time"]
        time_minutes = int(''.join(filter(str.isdigit, time_str)) or 60)
        time_flag = time_minutes <= time_filter
        
        # 食材搜索筛选
        search_flag = True
        if search_ingredient:
            search_flag = False
            if search_ingredient in name:
                search_flag = True
            for ing in data["ingredients"]:
                if search_ingredient in ing["name"]:
                    search_flag = True
                    break
        
        if series_flag and type_flag and time_flag and search_flag:
            filtered_recipes.append((name, data))
    
    # 显示筛选结果
    st.markdown(f'<h2 style="color:#333; margin:20px 0;">📋 筛选结果 ({len(filtered_recipes)}道)</h2>', unsafe_allow_html=True)
    
    if filtered_recipes:
        # 每个菜品单独一行
        for idx, (name, data) in enumerate(filtered_recipes, 1):
            with st.container():
                st.markdown('<div class="recipe-card">', unsafe_allow_html=True)
                
                # 左侧图片，右侧基本信息
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    st.image(data["img_url"], use_column_width=True)
                
                with col2:
                    st.markdown(f'<h3 class="recipe-name">{name}</h3>', unsafe_allow_html=True)
                    st.markdown(f'<p class="recipe-info">⏱️ {data["time"]} 
