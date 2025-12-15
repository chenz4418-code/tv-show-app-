import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
import base64
import requests
import streamlit.components.v1 as components

# ==========================================
# 1. 核心工具函数：创建Base64 SVG图片
# ==========================================

def create_svg_avatar(name, color):
    """
    创建带首字母的圆形SVG头像，并转换为Base64字符串
    :param name: 人物名称
    :param color: 背景颜色
    :return: Base64编码的SVG图片字符串
    """
    # 提取姓名首字母（最多两个）
    initials = "".join([n[0] for n in name.split()[:2]]).upper()
    
    # SVG模板
    svg = f"""
    <svg width="100" height="100" xmlns="http://www.w3.org/2000/svg">
        <!-- 圆形背景 -->
        <circle cx="50" cy="50" r="48" fill="{color}" stroke="#ffffff" stroke-width="2"/>
        <!-- 文字 -->
        <text x="50%" y="55%" font-family="Arial, sans-serif" font-size="40" font-weight="bold" 
              fill="#ffffff" text-anchor="middle" dominant-baseline="middle">
            {initials}
        </text>
    </svg>
    """
    
    # 转换为Base64
    b64 = base64.b64encode(svg.encode('utf-8')).decode('utf-8')
    return f"data:image/svg+xml;base64,{b64}"

def create_svg_poster(title, color):
    """
    创建剧集海报的SVG图片，并转换为Base64字符串
    :param title: 剧集名称
    :param color: 背景颜色
    :return: Base64编码的SVG图片字符串
    """
    svg = f"""
    <svg width="300" height="450" xmlns="http://www.w3.org/2000/svg">
        <!-- 渐变背景 -->
        <defs>
            <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:{color};stop-opacity:1" />
                <stop offset="100%" style="stop-color:{color.replace('#', '#333333')};stop-opacity:1" />
            </linearGradient>
        </defs>
        <rect width="100%" height="100%" fill="url(#bg)"/>
        
        <!-- 标题 -->
        <text x="50%" y="40%" font-family="Arial, sans-serif" font-size="24" font-weight="bold" 
              fill="#ffffff" text-anchor="middle" dominant-baseline="middle">
            {title}
        </text>
        
        <!-- 装饰元素 -->
        <rect x="20" y="380" width="260" height="2" fill="#ffffff" opacity="0.7"/>
        <text x="50%" y="90%" font-family="Arial, sans-serif" font-size="14" 
              fill="#ffffff" text-anchor="middle" dominant-baseline="middle">
            欧美剧剧情速通系统
        </text>
    </svg>
    """
    
    b64 = base64.b64encode(svg.encode('utf-8')).decode('utf-8')
    return f"data:image/svg+xml;base64,{b64}"

def get_real_poster(url):
    """
    下载真实的海报图片并转换为Base64字符串
    :param url: 海报图片的URL
    :return: Base64编码的图片字符串
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        b64 = base64.b64encode(response.content).decode('utf-8')
        return f"data:image/jpeg;base64,{b64}"
    except Exception as e:
        st.warning(f"海报加载失败，使用默认海报: {e}")
        return create_svg_poster("Default", "#3498DB")

def get_local_poster(file_path):
    """
    读取本地海报图片并转换为Base64字符串
    :param file_path: 本地海报图片的路径
    :return: Base64编码的图片字符串
    """
    try:
        with open(file_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode('utf-8')
            return f"data:image/jpeg;base64,{b64}"
    except Exception as e:
        st.warning(f"本地海报加载失败，使用默认海报: {e}")
        return create_svg_poster("Default", "#3498DB")

def get_local_avatar(file_path):
    """
    读取本地头像图片并转换为Base64字符串
    :param file_path: 本地头像图片的路径
    :return: Base64编码的图片字符串
    """
    try:
        with open(file_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode('utf-8')
            return f"data:image/jpeg;base64,{b64}"
    except Exception as e:
        st.warning(f"本地头像加载失败，使用默认头像: {e}")
        # 使用角色名称的首字母创建默认SVG头像
        name = file_path.split('/')[-1].split('.')[0].replace('_', ' ').title()
        return create_svg_avatar(name, "#95A5A6")

# ==========================================
# 2. 页面配置
# ==========================================

st.set_page_config(
    page_title="欧美剧剧情速通系统",
    layout="wide",
    page_icon="📼"
)

# ==========================================
# 3. 核心数据库
# ==========================================

DB = {
    "怪奇物语 (Stranger Things)": {
        "poster": get_local_poster("posters/stranger_things.jpg"),
        "genre": "科幻 / 惊悚 / 80年代",
        "rates": {"豆瓣": "9.4", "IMDb": "8.7"},
        "summary": "上世纪80年代的霍金斯小镇，男孩威尔失踪，引出了超能力少女Eleven、秘密实验室以及恐怖的\"逆世界\"。",
        "theme_color": "#E71D36",
        "nodes": [
            ("Eleven", get_local_avatar("avatars/eleven.jpg")),
            ("Mike", get_local_avatar("avatars/mike.jpg")),
            ("Will", get_local_avatar("avatars/will.jpg")),
            ("Hopper", get_local_avatar("avatars/hopper.jpg")),
            ("Joyce", get_local_avatar("avatars/joyce.jpg")),
            ("Max", get_local_avatar("avatars/max.jpg")),
            ("Vecna", get_local_avatar("avatars/vecna.jpg"))
        ],
        "edges": [
            ("Eleven", "Mike", "恋人"),
            ("Hopper", "Eleven", "养父女"),
            ("Joyce", "Hopper", "情侣"),
            ("Joyce", "Will", "母子"),
            ("Mike", "Will", "挚友"),
            ("Eleven", "Max", "闺蜜"),
            ("Vecna", "Eleven", "宿敌")
        ],
        "episodes": {
            "第一季 (S1)": [
                "E01 威尔失踪 - 威尔被抓走；Eleven逃出实验室。",
                "E02 迷雾重重 - 孩子们开始寻找威尔；Eleven展现超能力。",
                "E03 圣诞快乐 - 经典的彩灯沟通名场面。",
                "E04 逆世界入口 - 发现通往逆世界的通道。",
                "E05 实验室的秘密 - 揭露霍金斯实验室的黑暗历史。",
                "E06 小11的过去 - Eleven回忆起实验室的经历。",
                "E07 寻找威尔 - 众人进入逆世界寻找威尔。",
                "E08 逆世界 - 霍珀救出威尔；Eleven消失。"
            ],
            "第二季 (S2)": [
                "E01 回归 - 威尔从逆世界回来，但身上带着秘密。",
                "E02 迷雾 - 威尔再次进入逆世界；十一在实验室。",
                "E03 圣诞灯 - Eleven与霍珀在小木屋生活；威尔用彩灯沟通。",
                "E04 心灵怪 - 威尔被逆世界的生物附身。",
                "E05 洞 - 乔伊斯和鲍勃发现实验室的秘密。",
                "E06 间谍 - 威尔被用作间谍追踪团队。",
                "E07 实验室之战 - 众人对抗来自逆世界的怪物。",
                "E08 封闭通道 - Eleven关闭通往逆世界的通道。",
                "E09 最终决战 - 击败心灵怪；威尔康复。"
            ],
            "第三季 (S3)": [
                "E01 新的威胁 - 星庭购物中心出现新的威胁；霍珀和艾尔的冲突。",
                "E02 火球 - 孩子们发现俄罗斯人的活动痕迹。",
                "E03 中国食物 - 霍珀调查星庭购物中心；艾尔和麦克斯成为朋友。",
                "E04 桑拿测试 - 乔伊斯和霍珀发现俄罗斯人的基地。",
                "E05 亲爱的比利 - 麦克斯遭遇危险；霍珀被捕。",
                "E06 艾登 - 团队策划营救霍珀；艾尔失去超能力。",
                "E07 疯狂的科学家 - 揭露俄罗斯人的秘密基地；霍珀逃脱。",
                "E08 最后的战斗 - 星庭购物中心的最终决战；霍珀牺牲。"
            ],
            "第四季 (S4)": [
                "E01 新的开始 - 众人各奔东西，新的威胁出现；霍金斯出现新的受害者。",
                "E02 维克纳的诅咒 - 麦克斯回忆比利；团队开始调查。",
                "E03 我想念你 - 乔伊斯收到来自俄罗斯的神秘消息；艾尔适应新生活。",
                "E04 亲爱的比利 - Max听着Running Up That Hill逃离魔爪；霍金斯团队找到入口。",
                "E05 纳丁 - 艾尔恢复记忆；乔伊斯和默里前往俄罗斯。",
                "E06 恐惧之家 - 团队进入逆世界；艾尔与001号相遇。",
                "E07 屠杀 - 揭秘001号就是威克那；霍珀与怪物战斗。",
                "E08 逆世界 - 众人在逆世界对抗威克那；霍珀获救。",
                "E09 偷渡 - 决战时刻，霍金斯陷落；艾尔击败威克那。"
            ]
        },
        "quiz": [
            {"q": "Eleven 最喜欢的食物是什么？", "options": ["Eggo华夫饼", "披萨", "冰淇淋", "汉堡"], "ans": "Eggo华夫饼"},
            {"q": "威克那的真实身份是什么？", "options": ["001号", "魔王", "布伦纳博士", "霍珀"], "ans": "001号"},
            {"q": "第一季中用来与威尔沟通的道具是什么？", "options": ["圣诞彩灯", "对讲机", "电视", "电话"], "ans": "圣诞彩灯"},
            {"q": "Max逃离威克那时听的歌曲是什么？", "options": ["Running Up That Hill", "Sweet Child O' Mine", "Heroes", "Thriller"], "ans": "Running Up That Hill"}
        ]
    },
    
    "权力的游戏 (Game of Thrones)": {
        "poster": get_local_poster("posters/game_of_thrones.jpg"),
        "genre": "史诗 / 奇幻 / 权谋",
        "rates": {"豆瓣": "9.3", "IMDb": "9.2"},
        "summary": "在虚构的维斯特洛大陆，九大家族为争夺铁王座展开了残酷的权力斗争。北境长城之外，异鬼大军正在逼近。",
        "theme_color": "#154360",
        "nodes": [
            ("Jon Snow", get_local_avatar("avatars/jon_snow.jpg")),
            ("Daenerys", get_local_avatar("avatars/daenerys.jpg")),
            ("Tyrion", get_local_avatar("avatars/tyrion.jpg")),
            ("Cersei", get_local_avatar("avatars/cersei.jpg")),
            ("Night King", get_local_avatar("avatars/night_king.jpg")),
            ("Arya", get_local_avatar("avatars/arya.jpg")),
            ("Sansa", get_local_avatar("avatars/sansa.jpg"))
        ],
        "edges": [
            ("Jon Snow", "Daenerys", "姑侄/恋人"),
            ("Tyrion", "Daenerys", "国王之手"),
            ("Cersei", "Tyrion", "死敌"),
            ("Jon Snow", "Night King", "死敌"),
            ("Arya", "Sansa", "姐妹"),
            ("Jon Snow", "Arya", "兄妹"),
            ("Jon Snow", "Sansa", "兄妹")
        ],
        "episodes": {
            "第一季 (S1)": [
                "E01 凛冬将至 - 史塔克家族发现异鬼；龙妈嫁给卓戈。",
                "E02 国王之路 - 奈德前往君临任国王之手。",
                "E03 雪诺大人 - 琼恩前往长城；龙妈适应新环境。",
                "E04 残缺之躯 - 布兰康复但瘫痪；奈德调查琼恩·艾林之死。",
                "E05 狼与狮 - 奈德发现瑟曦和詹姆的乱伦关系。",
                "E06 黄金王冠 - 卓戈为龙妈袭击兰尼斯特军队。",
                "E07 不胜则死 - 奈德与瓦里斯交谈；琼恩与守夜人出发。",
                "E08 剑之尖端 - 罗柏率军南下；龙妈怀孕。",
                "E09 贝勒大圣堂 - 奈德被斩首。",
                "E10 火与血 - 龙诞生。"
            ],
            "第二季 (S2)": [
                "E01 北境不忘 - 罗柏称北境之王；琼恩加入野人。",
                "E02 夜之国度 - 史坦尼斯加冕；龙妈抵达魁尔斯。",
                "E03 逝者永恒 - 席恩背叛史塔克；龙妈拜访不朽之殿。",
                "E04 骸骨花园 - 提利昂成为国王之手；琼恩与耶哥蕊特同行。",
                "E05 古堡幽灵 - 艾莉亚与詹德利逃亡；龙妈在不朽之殿。",
                "E06 新旧诸神 - 罗伯与弗雷家族联姻；龙妈获得龙的控制权。",
                "E07 毁誉之人 - 席恩占领临冬城；琼恩返回城堡。",
                "E08 临冬城的王子 - 布兰与瑞肯逃亡；龙妈离开魁尔斯。",
                "E09 黑水之战 - 史坦尼斯进攻君临，被提利昂击败。",
                "E10 凡人皆需侍奉 - 提利昂受伤；龙妈获得三只船。"
            ],
            "第三季 (S3)": [
                "E01 自北境来 - 琼恩与野人同行；龙妈抵达奴隶湾。",
                "E02 黑色的翅膀，黑色的消息 - 布兰与琼恩擦身而过；龙妈解放阿斯塔波。",
                "E03 惩罚之旅 - 罗柏处决瑞卡德·卡史塔克；龙妈解放渊凯。",
                "E04 至死方休 - 泰温成为国王之手；龙妈面临新挑战。",
                "E05 火吻而生 - 琼恩与耶哥蕊特在一起；艾莉亚与猎狗同行。",
                "E06 群鸦的盛宴 - 布兰抵达血鸦处；龙妈进入弥林。",
                "E07 御前比武 - 乔佛里的婚礼准备；山姆威尔抵达旧镇。",
                "E08 第二场婚礼 - 泰丽莎与罗柏结婚；提利昂与珊莎结婚。",
                "E09 卡斯特梅的雨季 - 红色婚礼，罗柏、凯特琳和泰丽莎被杀。",
                "E10 弥莎 - 布兰与血鸦见面；龙妈锁起龙。"
            ],
            "第四季 (S4)": [
                "E01 两剑 - 乔佛里的婚礼；布兰学习绿视。",
                "E02 狮子与玫瑰 - 乔佛里与玛格丽结婚；龙妈治理弥林。",
                "E03 碎镣之人 - 琼恩回到城堡；龙妈解放奴隶。",
                "E04 守誓之剑 - 艾莉亚与猎狗遇到无旗兄弟会；詹姆回到君临。",
                "E05 第一剑 - 布兰预见过去；龙妈面对鹰身女妖之子。",
                "E06 长城守望者 - 琼恩成为守夜人总司令；艾莉亚失明。",
                "E07 卡斯特梅的雨季 - 奥柏伦与魔山决斗；奥柏伦死亡。",
                "E08 弥莎 - 乔佛里被毒杀；提利昂被指控。",
                "E09 长城之战 - 野人进攻城堡；琼恩击败曼斯。",
                "E10 孩子们 - 提利昂杀死泰温；龙妈征服弥林。"
            ],
            "第五季 (S5)": [
                "E01 战争将至 - 琼恩成为守夜人总司令；瑟曦失势。",
                "E02 黑白之院 - 艾莉亚在黑白之院；龙妈面临挑战。",
                "E03 大麻雀 - 大麻雀崛起；珊莎与小指头前往鹰巢城。",
                "E04 剥皮人 - 珊莎嫁给拉姆斯；琼恩与野人结盟。",
                "E05 杀死男孩 - 琼恩处决奥利；龙妈嫁给西茨达拉。",
                "E06 不屈者 - 艾莉亚成为无面者；詹姆前往多恩。",
                "E07 礼物 - 琼恩送山姆威尔去旧镇；龙妈打开角斗场。",
                "E08 艰难屯 - 异鬼攻击野人营地；琼恩救援野人。",
                "E09 圣母慈悲 - 瑟曦游街；琼恩被守夜人背叛。",
                "E10 母亲的 Mercy - 艾莉亚复仇；丹妮莉丝骑龙离开。"
            ],
            "第六季 (S6)": [
                "E01 红袍女巫 - 梅丽珊卓复活琼恩；丹妮莉丝在多斯拉克。",
                "E02 家 - 琼恩处决背叛者；艾莉亚逃离布拉福斯。",
                "E03 破誓者 - 琼恩离开守夜人；丹妮莉丝成为卡丽熙。",
                "E04 陌客之书 - 艾莉亚回到维斯特洛；布兰看到疯王。",
                "E05 门 - 布兰与夜王对抗；阿多牺牲。",
                "E06 血门 - 艾莉亚与无旗兄弟会重逢；丹妮莉丝准备起航。",
                "E07 破碎的人 - 詹姆回到君临；艾莉亚受伤。",
                "E08 无名之辈 - 艾莉亚失明恢复；丹妮莉丝抵达龙石岛。",
                "E09 私生子之战 - 琼恩与拉姆斯的史诗对决；琼恩获胜。",
                "E10 凛冬的寒风 - 琼恩被宣布为北境之王；瑟曦成为女王。"
            ],
            "第七季 (S7)": [
                "E01 龙石岛 - 琼恩与龙妈结盟；夜王获得龙。",
                "E02 风暴降生 - 龙妈召集盟友；琼恩前往龙石岛。",
                "E03 女王的审判 - 龙妈烧死塔利父子；艾莉亚回到临冬城。",
                "E04 战利品 - 詹姆与波隆北上；艾莉亚与珊莎重逢。",
                "E05 东海望 - 琼恩、詹姆和托蒙德前往长城外；龙妈救援。",
                "E06 长城之外 - 众人在长城外捕获尸鬼；夜王获得冰龙。",
                "E07 龙石岛 - 琼恩与龙妈相爱；夜王摧毁长城。"
            ],
            "第八季 (S8)": [
                "E01 临冬城 - 众人聚集临冬城；琼恩得知自己的真实身份。",
                "E02 七国骑士 - 大战前夜；琼恩与丹妮莉丝在一起。",
                "E03 长夜 - 击败夜王，艾莉亚杀死夜王。",
                "E04 最后的史塔克 - 众人庆祝胜利；丹妮莉丝失去一条龙。",
                "E05 钟声 - 丹妮莉丝屠城；詹姆与瑟曦死亡。",
                "E06 铁王座 - 结局，布兰成为国王。"
            ]
        },
        "quiz": [
            {"q": "兰尼斯特家族的俗语是什么？", "options": ["有债必偿", "听我怒吼", "凛冬将至", "血火同源"], "ans": "有债必偿"},
            {"q": "谁最终成为七国的统治者？", "options": ["布兰", "琼恩", "龙妈", "提利昂"], "ans": "布兰"},
            {"q": "谁杀死了夜王？", "options": ["艾莉亚", "琼恩", "龙妈", "提利昂"], "ans": "艾莉亚"},
            {"q": "龙妈有几条龙？", "options": ["3", "2", "4", "1"], "ans": "3"}
        ]
    },
    
    "绝命毒师 (Breaking Bad)": {
        "poster": get_local_poster("posters/breaking_bad.jpg"),
        "genre": "犯罪 / 剧情 / 化学",
        "rates": {"豆瓣": "9.6", "IMDb": "9.5"},
        "summary": "身患绝症的高中化学老师老白，为了给家人留后路，利用专业知识制毒，黑化成为大毒枭。",
        "theme_color": "#1E8449",
        "nodes": [
            ("Walter White", get_local_avatar("avatars/walter_white.jpg")),
            ("Jesse Pinkman", get_local_avatar("avatars/jesse_pinkman.jpg")),
            ("Gus Fring", get_local_avatar("avatars/gus_fring.jpg")),
            ("Hank Schrader", get_local_avatar("avatars/hank_schrader.jpg")),
            ("Skyler White", get_local_avatar("avatars/skyler_white.jpg")),
            ("Saul Goodman", get_local_avatar("avatars/saul_goodman.jpg")),
            ("Mike Ehrmantraut", get_local_avatar("avatars/mike_ehrmantraut.jpg"))
        ],
        "edges": [
            ("Walter White", "Jesse Pinkman", "搭档"),
            ("Walter White", "Gus Fring", "雇佣/死敌"),
            ("Walter White", "Hank Schrader", "连襟/追捕"),
            ("Walter White", "Skyler White", "夫妻"),
            ("Walter White", "Saul Goodman", "律师"),
            ("Gus Fring", "Mike Ehrmantraut", "手下"),
            ("Jesse Pinkman", "Mike Ehrmantraut", "合作/冲突")
        ],
        "episodes": {
            "第一季 (S1)": [
                "E01 试播集 - 老白确诊癌症；决定制毒。",
                "E02 猫鼠游戏 - 老白和杰西开始制毒；汉克调查冰毒案。",
                "E03 你是我的人 - 杰西遇到麻烦；老白帮助杰西。",
                "E04 癌症之王 - 老白开始化疗；杰西与简相遇。",
                "E05 灰度 - 老白和杰西遇到毒贩图科。",
                "E06 一把好牌 - 光头老白；杰西被抓。",
                "E07 灰飞烟灭 - 图科死亡；老白和杰西逃亡。"
            ],
            "第二季 (S2)": [
                "E01 七个33 - 老白和杰西寻找新的分销渠道。",
                "E02 猫和老鼠 - 汉克开始追踪海森堡。",
                "E03 比特 - 杰西与简同居；老白家庭出现问题。",
                "E04 尽在掌握 - 老白和杰西与古斯会面。",
                "E05 粉 - 杰西沉迷毒品；老白继续制毒。",
                "E06  peekaboo - 杰西与毒贩的孩子；老白家庭矛盾加剧。",
                "E07 否定 - 杰西戒毒；老白的婚姻面临危机。",
                "E08 四十 - 老白的生日；杰西与简复合。",
                "E09 四日 - 杰西在沙漠中制毒；老白与简的父亲相遇。",
                "E10 滑行 - 老白和杰西的毒品生意扩张；简开始复吸。",
                "E11 阿布奎基 - 汉克发现杰西的车；老白的婚姻破裂。",
                "E12 凤凰 - 简去世；老白看着简窒息。",
                "E13 结局 - 汉克在车祸中受伤；老白回到家庭。"
            ],
            "第三季 (S3)": [
                "E01 无中生有 - 老白和古斯合作；汉克康复。",
                "E02 凯瑟尔 - 老白与格斯的关系；杰西加入格斯的团队。",
                "E03 我叫迈尔斯 - 老白与格斯的手下发生冲突；杰西开始新的生活。",
                "E04 绿色 - 老白的家庭问题；杰西与格斯的关系。",
                "E05 鼠 - 杰西的朋友被格斯杀死；老白与杰西产生矛盾。",
                "E06 日落 - 老白与格斯的手下在沙漠中制毒；杰西与老白和解。",
                "E07 一击 - 老白和杰西遇到麻烦；格斯开始怀疑老白。",
                "E08 我是你爸爸 - 老白向儿子坦白；格斯与墨西哥毒枭会面。",
                "E09 卡夫卡式的 - 格斯与墨西哥毒枭的冲突；老白和杰西的困境。",
                "E10 苍蝇 - 老白和杰西在实验室中追逐苍蝇；两人的对话。",
                "E11 深渊 - 杰西的女友被格斯杀死；杰西陷入绝望。",
                "E12 一半措施 - 老白救了杰西；杰西杀死格斯的手下。",
                "E13 结局 - 汉克被袭击；老白与格斯的关系破裂。"
            ],
            "第四季 (S4)": [
                "E01 盒子里的人 - 老白和杰西处于格斯的监控下；汉克调查格斯。",
                "E02 三十秒 - 老白计划杀死格斯；杰西与格斯的关系。",
                "E03 开放日 - 老白的家庭问题；汉克继续调查格斯。",
                "E04 子弹点 - 老白和杰西与格斯的冲突；汉克发现线索。",
                "E05 碎纸机 - 老白的家庭破裂；汉克与格斯会面。",
                "E06 角落 - 老白和杰西产生矛盾；格斯计划除掉老白。",
                "E07 问题狗 - 杰西与格斯的手下发生冲突；老白继续计划。",
                "E08 Hermanos - 格斯的过去；老白和杰西的困境。",
                "E09 脸 - 格斯与墨西哥毒枭的冲突；老白和杰西的计划。",
                "E10 萨尔瓦多 - 老白和杰西实施计划；格斯与赫克托会面。",
                "E11 爬虫 - 老白和杰西等待机会；格斯开始怀疑。",
                "E12 结局 - 老白和杰西实施爆炸计划；格斯受伤。",
                "E13 变脸 - 炸鸡叔之死；实验室被毁。"
            ],
            "第五季 (S5)": [
                "E01 活死人 - 老白和杰西开始大规模制毒；汉克开始怀疑老白。",
                "E02 良好的电话 - 老白和杰西处理格斯的后事；汉克继续调查。",
                "E03 死锁 - 老白和杰西与迈克合作；汉克发现线索。",
                "E04 五十 - 老白庆祝生日；迈克与老白的冲突。",
                "E05 死 - 老白和迈克的矛盾；杰西开始质疑。",
                "E06 Buyout - 杰西想退出；老白和迈克的计划。",
                "E07 说我的名字 - 老白成为毒品帝国的老大；迈克死亡。",
                "E08 坠落 - 汉克开始怀疑老白；老白的家庭问题。",
                "E09 血液钱 - 汉克确认老白是海森堡；两人摊牌。",
                "E10 弹孔 - 老白和汉克的冲突；杰西陷入困境。",
                "E11  confession - 杰西被汉克审问；老白和汉克的博弈。",
                "E12 Rabid Dog - 杰西计划报复老白；老白家庭破裂。",
                "E13 托德 - 老白和托德处理尸体；杰西被绑架。",
                "E14 这里的全知 - 汉克牺牲；杰西被囚禁。",
                "E15 花岗岩州 - 老白逃亡；杰西被强迫制毒。",
                "E16 结局 - 老白谢幕；杰西获救。"
            ]
        },
        "quiz": [
            {"q": "老白的代号是什么？", "options": ["Heisenberg", "Einstein", "Chef", "Mr. White"], "ans": "Heisenberg"},
            {"q": "老白原本的职业是什么？", "options": ["化学老师", "医生", "律师", "警察"], "ans": "化学老师"},
            {"q": "谁是炸鸡店老板兼大毒枭？", "options": ["Gus Fring", "Tuco Salamanca", "Hector Salamanca", "Jesse Pinkman"], "ans": "Gus Fring"},
            {"q": "老白患的是什么癌症？", "options": ["肺癌", "胃癌", "肝癌", "胰腺癌"], "ans": "肺癌"}
        ]
    }
}

# ==========================================
# 4. 侧边栏选择
# ==========================================

with st.sidebar:
    st.title("📼 欧美剧速通系统")
    st.markdown("---")
    
    # 剧集选择 - 显示所有三部剧集的按钮
    st.markdown("### 📌 选择剧集：")
    
    # 为每个剧集创建一个按钮
    for show_name in DB.keys():
        if st.button(show_name, key=show_name):
            st.session_state.current_show = show_name
            st.session_state.quiz_idx = 0
            st.session_state.score = 0
            st.session_state.show_next = False
    
    # 初始化当前剧集
    if 'current_show' not in st.session_state:
        st.session_state.current_show = list(DB.keys())[0]
    
    selected_show = st.session_state.current_show

# 获取当前剧集数据
data = DB[selected_show]

# ==========================================
# 5. 动态主题（变色龙引擎）
# ==========================================

theme_color = data['theme_color']
show_name = selected_show

# 根据不同剧集创建独特的CSS样式
if show_name == "怪奇物语 (Stranger Things)":
    # 怪奇物语：80年代复古风格，霓虹色调，暗背景
    css = """
    <style>
        /* 页面背景 - 更具体的选择器 */
        .main, .reportview-container, .stApp {
            background-color: #1a1a2e !important;
            background-image: linear-gradient(135deg, #1a1a2e 0%%, #16213e 100%%) !important;
        }
        
        body {
            background-color: #1a1a2e !important;
            font-family: 'Consolas', 'Courier New', monospace !important;
            color: #ffffff !important;
            font-size: 16px;
            line-height: 1.8;
            font-weight: 500;
        }
        
        /* 标题样式 */
        h1, h2, h3, h4 {
            color: {0} !important;
            text-shadow: 0 0 10px {0}aa, 0 0 20px {0}88;
            font-family: 'Impact', sans-serif;
            letter-spacing: 2px;
            font-size: 1.8em;
            font-weight: bold;
        }
        
        /* 按钮样式 */
        .stButton > button {
            color: white;
            background-color: {0};
            border: none;
            border-radius: 5px;
            padding: 10px 20px;
            font-weight: bold;
            box-shadow: 0 4px 15px rgba(231, 29, 54, 0.3);
            transition: all 0.3s ease;
            font-size: 14px;
        }
        
        .stButton > button:hover {
            background-color: #ff385c;
            box-shadow: 0 6px 20px rgba(231, 29, 54, 0.5);
            transform: translateY(-2px);
        }
        
        /* 侧边栏样式 */
        [data-testid="stSidebar"] {
            background-color: rgba(26, 26, 46, 0.98) !important;
            border-right: 3px solid {0} !important;
            padding: 20px !important;
            color: #ffffff !important;
            font-weight: 600 !important;
            font-size: 16px !important;
        }
        
        /* 侧边栏标题样式 */
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
            color: {0} !important;
            text-shadow: 0 0 10px {0}aa;
            margin-bottom: 15px !important;
        }
        
        /* 卡片样式 */
        .stExpander {
            border-left: 4px solid {0};
            background-color: rgba(255, 255, 255, 0.1) !important;
            border-radius: 8px;
            margin-bottom: 10px;
            padding: 15px;
        }
        
        /* 文本样式 */
        p, span, div, .markdown-text-container {
            color: #ffffff !important;
            font-weight: 600;
            font-size: 17px;
            text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.7);
        }
        
        /* 进度条样式 */
        .stProgress > div > div > div {
            background-color: {0};
            box-shadow: 0 0 10px {0};
        }
        
        /* 分隔线样式 */
        .css-1n7v3ny {
            border-top: 2px solid {0}44;
        }
        
        /* 确保所有容器都使用深色背景 */
        .block-container, .css-18e3th9 {
            background-color: transparent !important;
        }
        
        /* 优化链接颜色 */
        a {
            color: #4facfe !important;
            text-decoration: none !important;
        }
        
        /* 优化图片容器 */
        .stImage > div {
            background-color: transparent !important;
        }
        
        /* 人物关系图背景样式 - 怪奇物语 */
        [data-testid="stAppViewContainer"] .streamlit-agraph, 
        [data-testid="stAppViewContainer"] .streamlit-agraph > div, 
        [data-testid="stAppViewContainer"] .streamlit-agraph > div > div, 
        [data-testid="stAppViewContainer"] .vis-network, 
        [data-testid="stAppViewContainer"] .vis-network canvas {
            background: #1a1a2e !important;
            background-color: #1a1a2e !important;
        }
        
        @keyframes backgroundAnimation {
            0% { background-position: 0% 50%, 0% 50%, 0% 50%; }
            50% { background-position: 100% 50%, 100% 50%, 100% 50%; }
            100% { background-position: 0% 50%, 0% 50%, 0% 50%; }
        }
    </style>
    """
    css = css.replace('{0}', theme_color)
elif show_name == "权力的游戏 (Game of Thrones)":
    # 权力的游戏：中世纪史诗风格，暗红金色，厚重感
    css = """
    <style>
        /* 页面背景 - 更具体的选择器 */
        .main, .reportview-container, .stApp {
            background-color: #1a0d00 !important;
            background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100"><rect width="100" height="100" fill="%%231a0d00"/><path d="M0 0 L100 100 M100 0 L0 100" stroke="%%23331a00" stroke-width="0.5" opacity="0.3"/></svg>') !important;
        }
        
        body {
            background-color: #1a0d00 !important;
            font-family: 'Cambria', 'Times New Roman', serif !important;
            color: #f4e4b3 !important;
            font-size: 16px;
            line-height: 1.8;
            font-weight: 500;
        }
        
        /* 标题样式 */
        h1, h2, h3, h4 {
            color: #f4d03f !important;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.9);
            font-family: 'Georgia', serif;
            letter-spacing: 1px;
            border-bottom: 2px solid #f4d03f;
            padding-bottom: 5px;
            font-size: 1.8em;
            font-weight: bold;
        }
        
        /* 按钮样式 */
        .stButton > button {
            color: #1a0d00;
            background-color: #f4d03f;
            border: 2px solid #d4af37;
            border-radius: 0;
            padding: 10px 20px;
            font-weight: bold;
            font-family: 'Georgia', serif;
            background-image: linear-gradient(to bottom, #f4d03f, #d4af37);
            transition: all 0.3s ease;
            font-size: 14px;
        }
        
        .stButton > button:hover {
            background-color: #f9e79f;
            background-image: linear-gradient(to bottom, #f9e79f, #f4d03f);
            box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.5);
        }
        
        /* 侧边栏样式 */
        [data-testid="stSidebar"] {
            background-color: rgba(26, 13, 0, 0.98) !important;
            border-right: 3px solid #f4d03f !important;
            padding: 20px !important;
            color: #f4e4b3 !important;
            font-weight: 600 !important;
            font-size: 16px !important;
        }
        
        /* 侧边栏标题样式 */
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
            color: #f4d03f !important;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.9);
            margin-bottom: 15px !important;
        }
        
        /* 卡片样式 */
        .stExpander {
            border-left: 4px solid #f4d03f;
            background-color: rgba(40, 20, 0, 0.85) !important;
            border-radius: 0;
            margin-bottom: 15px;
            padding: 15px;
        }
        
        /* 文本样式 */
        p, span, div, .markdown-text-container {
            color: #f4e4b3 !important;
            font-weight: 600;
            font-size: 17px;
            text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.8);
        }
        
        /* 进度条样式 */
        .stProgress > div > div > div {
            background-color: #f4d03f;
            background-image: linear-gradient(to right, #f4d03f, #d4af37);
        }
        
        /* 分隔线样式 */
        .css-1n7v3ny {
            border-top: 2px solid #f4d03f44;
        }
        
        /* 确保所有容器都使用深色背景 */
        .block-container, .css-18e3th9 {
            background-color: transparent !important;
        }
        
        /* 优化链接颜色 */
        a {
            color: #d4af37 !important;
            text-decoration: none !important;
        }
        
        /* 优化图片容器 */
        .stImage > div {
            background-color: transparent !important;
        }
        
        /* 人物关系图背景样式 - 权力的游戏 */
        [data-testid="stAppViewContainer"] .streamlit-agraph, 
        [data-testid="stAppViewContainer"] .streamlit-agraph > div, 
        [data-testid="stAppViewContainer"] .streamlit-agraph > div > div, 
        [data-testid="stAppViewContainer"] .vis-network, 
        [data-testid="stAppViewContainer"] .vis-network canvas {
            background: #1a0d00 !important;
            background-color: #1a0d00 !important;
        }
    </style>
    """
    css = css.replace('{0}', theme_color)
elif show_name == "绝命毒师 (Breaking Bad)":
    # 绝命毒师：改为深色背景，保持绿色主题
    css = """
    <style>
        /* 页面背景 - 更具体的选择器 */
        .main, .reportview-container, .stApp {
            background-color: #0d1b2a !important;
            background-image: linear-gradient(135deg, #0d1b2a 0%%, #1b263b 100%%) !important;
        }
        
        body {
            background-color: #0d1b2a !important;
            font-family: 'Segoe UI', 'Arial', sans-serif !important;
            color: #e0e1dd !important;
            font-size: 16px;
            line-height: 1.8;
            font-weight: 500;
        }
        
        /* 标题样式 */
        h1, h2, h3, h4 {
            color: {0} !important;
            text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.5);
            font-family: 'Helvetica Neue', sans-serif;
            letter-spacing: 0.5px;
            font-size: 1.8em;
            font-weight: bold;
        }
        
        /* 按钮样式 */
        .stButton > button {
            color: white;
            background-color: {0};
            border: none;
            border-radius: 8px;
            padding: 12px 24px;
            font-weight: bold;
            box-shadow: 0 2px 8px rgba(30, 132, 73, 0.3);
            transition: all 0.3s ease;
            font-size: 14px;
        }
        
        .stButton > button:hover {
            background-color: #27ae60;
            box-shadow: 0 4px 12px rgba(30, 132, 73, 0.5);
            transform: translateY(-1px);
        }
        
        /* 侧边栏样式 */
        [data-testid="stSidebar"] {
            background-color: rgba(13, 27, 42, 0.98) !important;
            border-right: 3px solid {0} !important;
            padding: 20px !important;
            color: #e0e1dd !important;
            font-weight: 600 !important;
            font-size: 16px !important;
        }
        
        /* 侧边栏标题样式 */
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
            color: {0} !important;
            text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.5);
            margin-bottom: 15px !important;
        }
        
        /* 卡片样式 */
        .stExpander {
            border-left: 4px solid {0};
            background-color: rgba(30, 41, 59, 0.9) !important;
            border-radius: 8px;
            margin-bottom: 10px;
            padding: 15px;
        }
        
        /* 文本样式 */
        p, span, div, .markdown-text-container {
            color: #e0e1dd !important;
            font-weight: 600;
            font-size: 17px;
            text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.7);
        }
        
        /* 进度条样式 */
        .stProgress > div > div > div {
            background-color: {0};
            background-image: linear-gradient(to right, #1e8449, #27ae60);
        }
        
        /* 分隔线样式 */
        .css-1n7v3ny {
            border-top: 2px solid {0}44;
        }
        
        /* 确保所有容器都使用深色背景 */
        .block-container, .css-18e3th9 {
            background-color: transparent !important;
        }
        
        /* 优化链接颜色 */
        a {
            color: #1e8449 !important;
            text-decoration: none !important;
        }
        
        /* 优化图片容器 */
        .stImage > div {
            background-color: transparent !important;
        }
        
        /* 人物关系图背景样式 - 绝命毒师 */
        [data-testid="stAppViewContainer"] .streamlit-agraph, 
        [data-testid="stAppViewContainer"] .streamlit-agraph > div, 
        [data-testid="stAppViewContainer"] .streamlit-agraph > div > div, 
        [data-testid="stAppViewContainer"] .vis-network, 
        [data-testid="stAppViewContainer"] .vis-network canvas {
            background: #0d1b2a !important;
            background-color: #0d1b2a !important;
        }
        
        @keyframes backgroundAnimation {
            0% { background-position: 0% 50%, 0% 50%, 0% 50%; }
            50% { background-position: 100% 50%, 100% 100%, 100% 0%; }
            100% { background-position: 0% 50%, 0% 50%, 0% 50%; }
        }
    </style>
    """
    css = css.replace('{0}', theme_color)
else:
    # 默认样式
    css = """
    <style>
        /* 标题颜色 */
        h1, h2, h3, h4 {{
            color: {theme_color} !important;
        }}
        
        /* 按钮颜色 */
        .stButton > button {{
            color: white;
            background-color: {theme_color};
            border-radius: 5px;
        }}
        
        /* 侧边栏高亮 */
        .css-1d391kg {{
            background-color: {theme_color}22;
        }}
        
        /* 进度条颜色 */
        .stProgress > div > div > div {{
            background-color: {theme_color};
        }}
        
        /* 卡片样式 */
        .stExpander {{
            border-left: 4px solid {theme_color};
        }}
    </style>
    """
    css = css.format(theme_color)

# 应用动态CSS
st.markdown(css, unsafe_allow_html=True)

# ==========================================
# 6. 主内容区域
# ==========================================

# Banner
col1, col2 = st.columns([1, 4])
with col1:
    st.image(data['poster'], width='stretch', caption="剧集海报")
with col2:
    st.markdown(f"# {selected_show.split('(')[0]}")
    st.markdown(f"### {data['genre']}")
    st.markdown(f"> {data['summary']}")
    st.markdown(f"**豆瓣**: {data['rates']['豆瓣']} | **IMDb**: {data['rates']['IMDb']}")

st.divider()

# Tabs
tab1, tab2, tab3 = st.tabs(["🕸️ 人物关系图谱", "📖 剧情速通", "🧠 趣味闯关"])

# --- Tab 1: 人物关系图谱 ---
with tab1:
    
    try:
        nodes = []
        edges = []
        
        # 创建节点
        for n_id, n_img in data['nodes']:
            nodes.append(Node(
                id=n_id, 
                label=n_id, 
                size=30, 
                shape="circularImage", 
                image=n_img
            ))
        
        # 创建边
        for src, tgt, lbl in data['edges']:
            edges.append(Edge(
                source=src, 
                target=tgt, 
                label=lbl, 
                color="#bdc3c7", 
                length=250
            ))
        
        # 配置
        config = Config(
            width="100%", 
            height=600, 
            directed=True, 
            physics=True, 
            nodeHighlightBehavior=True, 
            highlightColor="#F7A072", 
            collapsible=False
        )
        
        # 为Config添加背景配置
        if show_name == "怪奇物语 (Stranger Things)":
            config.background = "#1a1a2e"
        elif show_name == "权力的游戏 (Game of Thrones)":
            config.background = "#1a0d00"
        elif show_name == "绝命毒师 (Breaking Bad)":
            config.background = "#0d1b2a"
        
        # 绘制图谱
        agraph(nodes=nodes, edges=edges, config=config)
        

        
    except Exception as e:
        st.error(f"图谱加载失败: {e}")

# --- Tab 2: 剧情速通 ---
with tab2:
    st.markdown("### 📝 全季剧情速通")
    
    # 展开所有季度
    for season_name, episodes in data['episodes'].items():
        with st.expander(season_name, expanded=True):
            for idx, ep in enumerate(episodes, 1):
                st.write(f"**{ep}**")

# --- Tab 3: 趣味闯关 ---
with tab3:
    st.markdown("### 🧠 剧迷大挑战")
    
    # 初始化状态
    if 'quiz_idx' not in st.session_state:
        st.session_state.quiz_idx = 0
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'show_next' not in st.session_state:
        st.session_state.show_next = False
    
    quiz_list = data['quiz']
    current_idx = st.session_state.quiz_idx
    
    # 显示进度
    st.progress(current_idx / len(quiz_list))
    
    if current_idx < len(quiz_list):
        # 当前题目
        current_question = quiz_list[current_idx]
        st.markdown(f"**问题 {current_idx + 1}/{len(quiz_list)}**: {current_question['q']}")
        
        # 用户选择
        user_answer = st.radio(
            "请选择答案：",
            current_question['options'],
            key=f"quiz_{selected_show}_{current_idx}"
        )
        
        # 提交答案表单
        with st.form(key=f"form_{current_idx}"):
            submit_button = st.form_submit_button("提交答案")
        
        if submit_button:
            # 检查答案
            if user_answer == current_question['ans']:
                st.success("✅ 正确！")
                st.session_state.score += 1
            else:
                st.error(f"❌ 错误，正确答案是：{current_question['ans']}")
            
            st.session_state.show_next = True
        
        # 下一题按钮
        if st.session_state.show_next:
            if st.button("➡️ 下一题", key=f"next_{current_idx}"):
                st.session_state.quiz_idx += 1
                st.session_state.show_next = False
                st.rerun()
    
    else:
        # 显示结果
        st.balloons()
        st.success(f"🏆 挑战结束！你的得分：{st.session_state.score} / {len(quiz_list)}")
        
        # 重玩按钮
        if st.button("🔄 再玩一次", key="restart_quiz"):
            st.session_state.quiz_idx = 0
            st.session_state.score = 0
            st.session_state.show_next = False
            st.rerun()

# 页脚
st.markdown("---")
st.caption("© 2025 Python Coursework | 欧美剧剧情速通系统")