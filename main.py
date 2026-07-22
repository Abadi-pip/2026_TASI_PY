# ====== IMPORTING LIABRARIES ==========
import numpy as np
import html
import pandas as pd
import streamlit as st
import datetime as dt
import yfinance as yf
import time
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.offline as pyo
from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly
import io
import streamlit.components.v1 as components
import requests
import xml.etree.ElementTree as ET

# ====== PAGE VAR & CONFIG ==========
page_title = "Stock Analysis Selector"
Page_icon = '📈'
layout = 'wide'
initial_sidebar_state= "expanded"
# ====== PAGE CONFIG CODE ===========

st.set_page_config(layout = layout ,initial_sidebar_state = initial_sidebar_state, page_title = page_title ,  page_icon= Page_icon)

#======= STYLING WEB PAGE ===========
CUSTOM_THEME = """
<link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700&family=JetBrains+Mono:wght@500&display=swap" rel="stylesheet">
<style>
:root{--bg-app:#0D1321; --bg-sidebar:#10182B; --bg-card:#161F35; --border-soft: rgba(255,255,255,0.08); --border-soft2: rgba(255,255,255,0.05); --gold:#CBA135; --emerald:#1FAE7A; --rose:#E15361; --text-primary:#EDEFF4; --text-muted:#8991A8; --hero-blue-1:#EAF2FB; --hero-blue-2:#B9D3EC; --hero-accent:#2E6FA6;}
html, body, [data-testid="stAppViewContainer"]{background-color: var(--bg-app) !important; font-family: 'Tajawal', sans-serif !important;}
[data-testid="stHeader"]{ background-color: transparent !important; }
[data-testid="stSidebar"]{ background-color: var(--bg-sidebar) !important; border-inline-end: 1px solid var(--border-soft2); }
[data-testid="stSidebar"] *{ color: var(--text-primary) !important; }
p, li, label, [data-testid="stMarkdownContainer"]{ color: var(--text-primary); }
[data-testid="stCaptionContainer"]{ color: var(--text-muted) !important; }
/* Metrics Styling */
[data-testid="stMetric"], [data-testid="stMetricContainer"], [data-testid="metric-container"]{background-color: var(--bg-card) !important; border: 1px solid var(--border-soft) !important; border-inline-start: 3px solid var(--gold) !important; border-radius: 10px !important; padding: 14px 16px !important; transition: transform .18s ease, border-color .18s ease;}
[data-testid="stMetric"]:hover{ transform: translateY(-3px); border-color: var(--gold) !important; }
[data-testid="stMetricValue"]{ color: var(--gold) !important; font-family:'JetBrains Mono', monospace !important; }
[data-testid="stMetricLabel"]{ color: var(--text-muted) !important; }
/* Buttons & Inputs */
.stButton button, [data-testid="stDownloadButton"] button{background-color: var(--bg-card) !important; color: var(--text-primary) !important; border: 1px solid var(--border-soft) !important; border-radius: 8px !important; transition: all .15s ease !important;}
.stButton button:hover, [data-testid="stDownloadButton"] button:hover{border-color: var(--gold) !important; color: var(--gold) !important; transform: translateY(-1px);}
[data-testid="stFormSubmitButton"] button{background-color: var(--gold) !important; color: var(--bg-app) !important; font-weight: 500 !important; border: none !important;}
[data-testid="stFormSubmitButton"] button:hover{ opacity:.9; transform: translateY(-1px); }
[data-testid="stSelectbox"] div[data-baseweb="select"] > div, [data-testid="stDateInput"] input{background-color: var(--bg-card) !important; border-color: var(--border-soft) !important; color: var(--text-primary) !important; border-radius: 8px !important;}
[data-testid="stToggle"] [role="switch"][aria-checked="true"]{ background-color: var(--gold) !important; }
[data-testid="stExpander"], [data-testid="stForm"]{background-color: var(--bg-card) !important; border: 1px solid var(--border-soft) !important; border-radius: 10px !important;}
hr{ border-color: var(--border-soft) !important; }
/* Hero Section */
.tasi-hero{background: linear-gradient(160deg, var(--hero-blue-1) 0%, var(--hero-blue-2) 100%); padding: 36px 24px 42px; text-align:center; border-radius: 16px 16px 0 0; margin-bottom: 0px; animation: tasiFadeDown .7s ease;}
.tasi-hero-badge{ display:inline-block; background: rgba(46,111,166,0.12); color: var(--hero-accent); font-size:11.5px; padding:5px 14px; border-radius:20px; margin-bottom:12px; }
.tasi-hero-title{ color:#1B2A3D; font-size:23px; font-weight:700; margin-bottom:6px; }
.tasi-hero-sub{ color:#4A5A6E; font-size:13.5px; }
@keyframes tasiFadeDown{ from{ opacity:0; transform: translateY(-10px);} to{ opacity:1; transform:none;} }
.tasi-ticker-wrap {
    background: var(--bg-sidebar);
    border:1px solid var(--border-soft2);
    border-radius:8px;
    overflow:hidden; /* هذا الجزء هو السر: يخفي النص حين يخرج عن الإطار */
    white-space:nowrap;
    padding:7px 0;
    margin-bottom: 10px;
    width: 100%;
}
.tasi-ticker {
    display: inline-block;
    padding-left: 100%; /* يبدأ النص من أقصى اليمين */
    color: var(--gold);
    font-size: 12.5px;
    animation: tasiScroll 20s linear infinite; /* 20 ثانية للسرعة، غير الرقم لزيادة أو تقليل السرعة */
    white-space: nowrap;
}
/* التعديل هنا: تغيير padding-inline-start إلى padding-inline-end لتبدأ من اليسار */
.tasi-ticker-wrap:hover .tasi-ticker {
    animation-play-state: paused;
}
/* التعديل هنا: عكس مسار الحركة (transform) لتتجه نحو اليمين */
# @keyframes tasiScroll {
#     0% { transform: translateX(0%); }
#     100% { transform: translateX(-100%); }
# }
@keyframes tasiScroll{ from{ transform: translateX(-100%);} to{ transform: translateX(0);} } 
/* News Items */
.tasi-news-item{ display:flex; align-items:center; justify-content:space-between; padding:9px 6px; border-bottom:1px solid var(--border-soft2); transition: background .15s ease; }
.tasi-news-item:hover{ background: rgba(255,255,255,0.04); }
.tasi-news-item:hover .tasi-news-arrow{ color: var(--gold); transform: translateX(-3px); }
.tasi-news-arrow{ color: var(--text-muted); transition: all .15s ease; display:inline-block; }
/* =========================================
   التبويبات (Tabs) - التعديل الجديد والمحسن
   ========================================= */
/* 1. الحاوية الرئيسية للتبويبات: زيادة المسافة (gap) بينها */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    gap: 16px !important; 
    background-color: transparent !important;
    border-bottom: 1px solid var(--border-soft) !important;
    padding-bottom: 4px !important;
}
/* 2. تصميم أزرار التبويبات في الحالة العادية */
[data-testid="stTabs"] button[role="tab"] {
    color: var(--text-muted) !important;
    background-color: transparent !important;
    font-family: 'Tajawal', sans-serif !important;
    font-size: 14px !important;
    padding: 8px 16px !important; 
    border-radius: 6px 6px 0 0 !important; 
    transition: all 0.2s ease !important;
}
/* 3. تأثير مرور الماوس (Hover) */
[data-testid="stTabs"] button[role="tab"]:hover {
    color: var(--gold) !important;
    background-color: rgba(203, 161, 53, 0.05) !important; 
}
/* 4. إبراز التبويب النشط (Active State) بشكل واضح جداً */
[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
    color: var(--gold) !important;
    font-weight: 700 !important; 
    background-color: rgba(203, 161, 53, 0.12) !important; 
    border-bottom: 3px solid var(--gold) !important; 
}
/* Tables */
[data-testid="stTable"] table{ color: var(--text-primary) !important; font-family: 'JetBrains Mono', monospace !important; font-size: 12.5px !important; }
[data-testid="stTable"] thead tr th{background-color: var(--bg-sidebar) !important; color: var(--gold) !important; border-color: var(--border-soft) !important; font-family: 'Tajawal', sans-serif !important;}
[data-testid="stTable"] tbody tr td{ border-color: var(--border-soft2) !important; }
[data-testid="stTable"] tbody tr:hover td{ background-color: rgba(203,161,53,0.08) !important; }
/* Scroll Reveal */
.scroll-reveal-el {opacity: 0; transform: translateY(30px); transition: opacity 0.8s ease-out, transform 0.8s ease-out;}
.scroll-reveal-visible {opacity: 1 !important; transform: translateY(0) !important;}
</style>
"""
st.markdown(CUSTOM_THEME, unsafe_allow_html=True)
#======= HERO =========
st.markdown(f"""
<div class="tasi-hero">
    <span class="tasi-hero-badge">و اسواق السلع العالمي TASI · تحديث لحظي</span>
    <div class="tasi-hero-title">{page_title} {Page_icon}</div>
    <div class="tasi-hero-sub">تحليل فني وتوقعات لأسهم السوق السعودي و اسواق السلع العالمي -- بأسلوب واضح وهادئ</div>
</div>
<div style="height:60px; background:linear-gradient(var(--hero-blue-2), var(--bg-app)); margin-top:0px; margin-bottom:15px; border-radius: 0 0 16px 16px;"></div>
""", unsafe_allow_html=True)

#======= MAGIC SCROLL REVEAL EFFECT =========
scroll_reveal_js = """
<script>
document.addEventListener("DOMContentLoaded", function() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('scroll-reveal-visible');
            } else {
                entry.target.classList.remove('scroll-reveal-visible');
            }
        });
    }, { threshold: 0.1 });

    setInterval(() => {
        const targets = window.parent.document.querySelectorAll('[data-testid="stMetric"], [data-testid="stTable"], .stPlotlyChart');
        targets.forEach(el => {
            if (!el.classList.contains('scroll-reveal-el')) {
                el.classList.add('scroll-reveal-el');
                observer.observe(el);
            }
        });
    }, 1000);
});
</script>
"""
components.html(scroll_reveal_js, height=0, width=0)

#======= Ticker =========
st.markdown("""
<div class="tasi-ticker-wrap">
    <div class="tasi-ticker">اللهمَّ لك الحمدُ كلُّه ولك الملكُ كلُّه بيدِك الخيرُ كلُّه إليك يرجعُ الأمرُ كلُّه علانيتُه وسرُّه فأهلٌ أن تُحمدَ إنك على كلِّ شيءٍ قديرٌ و الصلاة و السلام على رسول الله</div>
</div>
""", unsafe_allow_html=True)

date = dt.datetime.now().strftime('TODAY\'S DATE : [%d-%m-%y]   TIME :[ %H:%M]')
st.caption(date)

"---"

#========================= DICTIONARIES ================================
#=========================  Commodities ================================
Section_list1 = ['الذهب', 'الفضة', 'البلاتين', 'النحاس', 'النفط الخام', 'الغاز الطبيعي']

Gold = {'العقود الآجلة للذهب (كومكس)': 'GC=F', 
    'الذهب الفوري (عالمي)': 'XAU=X'
}

Silver = {'العقود الآجلة للفضة (كومكس)': 'SI=F', 
    'الفضة الفورية (عالمي)': 'XAG=X'
}

Platinum = {'العقود الآجلة للبلاتين (نايمكس)': 'PL=F', 
    'البلاتين الفوري': 'XPT=X'
}

Copper = {'العقود الآجلة للنحاس': 'HG=F'
}

Crude_Oil = {'النفط الخام الأمريكي (WTI)': 'CL=F', 
    'نفط خام برنت (Brent)': 'BZ=F'
}

Natural_Gas = {'الغاز الطبيعي': 'NG=F'
}

#========================  TASI & SECTORS ================================
Section_list = ['المؤشر العام TASI','قطاع الطاقة','قطاع المواد الأساسية','قطاع السلع الرأسمالية' ,
                'قطاع الخدمات التجارية والمهنية', 'قطاع النقل' ,
                'قطاع السلع طويلة الاجل' , 'قطاع الخدمات الإستهلاكية', 'قطاع الإعلام والترفيه',
                'قطاع تجزئة السلع الكمالية' , 'قطاع تجزئة الأغذية', 
                'قطاع إنتاج الأغذية', 'قطاع الرعاية الصحية' ,'قطاع الادوية',
                'قطاع البنوك','قطاع الإستثمار والتمويل',  'قطاع التأمين','قطاع التطبيقات وخدمات التقنية',
                 'قطاع الإتصالات' , 'قطاع المرافق العامة', 'الصناديق العقارية المتداولة (ريت)', 'إدارة وتطوير العقارات']

TASI = {'المؤشر العام TASI':'^TASI.SR'}

Energy = {'شركة المصافي العربية السعودية': '2030.SR', 'أرامكو السعودية': '2222.SR', 'شركة رابغ للتكرير والبتروكيماويات(بترو رابغ)': '2380.SR', 'الحفر العربية': '2381.SR', 'أديس' : '2382.SR', 'الشركة الوطنية السعودية للنقل البحري': '4030.SR', 'شركة الدريس للخدمات البترولية والنقليات': '4200.SR'}

Materials = {'شركة تكوين المتطورة للصناعات': '1201.SR', '(مبكو)شركة الشرق الأوسط لصناعة وإنتاج الورق': '1202.SR', '(بي سي آي) شركة الصناعات الكيميائية الأساسية': '1210.SR', 'شركة التعدين العربية السعودية(معادن)': '1211.SR', 'شركة اتحاد مصانع الأسلاك': '1301.SR', 'شركة اليمامة للصناعات الحديدية': '1304.SR', 'الشركة السعودية لأنابيب الصلب (انابيب السعودية)': '1320.SR', 'شركة أنابيب الشرق المتكاملة للصناعة': '1321.SR', 'شركة المصانع الكبرى للتعدين (أماك)': '1322.SR', 'شركة كيمائيات الميثانول(كيمانول)': '2001.SR', 'الشركة السعودية للصناعات الأساسية(سابك)': '2010.SR', 'شركة سابك للمغذيات الزراعية(سافكو)': '2020.SR', 'شركة التصنيع الوطنية': '2060.SR', 'شركة الجبس الأهلية': '2090.SR', 'شركة الصناعات الزجاجية الوطنية': '2150.SR', 'شركة اللجين': '2170.SR', 'شركة تصنيع مواد التعبئة والتغليف(فيبكو)': '2180.SR', 'الشركة العربية للأنابيب': '2200.SR', 'شركة نماء للكيماويات': '2210.SR', 'الشركة الوطنية للتصنيع وسبك المعادن(معدنية)': '2220.SR', 'شركة أرامكو السعودية لزيوت الأساس  (لوبريف)' : '2223.SR', 'شركة الزامل للاستثمار الصناعي': '2240.SR', 'المجموعة السعودية للاستثمار الصناعي': '2250.SR', 'شركة ينبع الوطنية للبتروكيماويات(ينساب)': '2290.SR', 'الشركة السعودية لصناعة الورق': '2300.SR', 'الشركة السعودية العالمية للبتروكيماويات(سبكيم)': '2310.SR', 'الشركة المتقدمة للبتروكيماويات': '2330.SR', 'شركة كيان السعودية للبتروكيماويات': '2350.SR', 'شركة اسمنت حائل': '3001.SR', 'شركة اسمنت نجران': '3002.SR', 'شركة اسمنت المدينة': '3003.SR', 'شركة اسمنت المنطقة الشمالية': '3004.SR', 'شركة اسمنت أم القرى': '3005.SR', 'شركة زهرة الواحة للتجارة' : '3007.SR', 'شركة الكثيري القابضة' : '3008.SR', 'شركة الاسمنت العربية': '3010.SR', 'شركة اسمنت اليمامة السعودية المحدودة': '3020.SR', 'شركة الأسمنت السعودية': '3030.SR', 'شركة اسمنت القصيم': '3040.SR', 'شركة إسمنت المنطقة الجنوبية': '3050.SR', 'شركة اسمنت ينبع': '3060.SR', 'شركة اسمنت المنطقة الشرقية': '3080.SR', 'شركة اسمنت تبوك': '3090.SR', 'شركة اسمنت الجوف': '3091.SR'}

Capital_Goods = {'مجموعة أسترا الصناعية': '1212.SR', 'شركة بوان': '1302.SR', 'شركة الصناعات الكهربائية': '1303.SR', 'شركة الخزف السعودي': '2040.SR', 'شركة الكابلات السعودية': '2110.SR', 'شركة اميانتيت العربية السعودية': '2160.SR', 'شركة البابطين للطاقة والاتصالات': '2320.SR', 'الشركة السعودية لإنتاج الأنابيب الفخارية': '2360.SR', 'شركة الشرق الأوسط للكابلات المتخصصة (مسك)': '2370.SR', 'الشركة السعودية للصادرات الصناعية': '4140.SR', 'شركة العمران للصناعة والتجارة' : '4141.SR', 'شركة مجموعة كابلات الرياض' : '4142.SR'}

Commercial_Professional_Svc = {'شركة مهارة للموارد البشرية' : '1831.SR', 'شركة صدر للخدمات اللوجستية' : '1832.SR', 'شركة الموارد للقوى البشرية': '1833.SR', 'الشركة السعودية للطباعة والتغليف': '4270.SR', 'شركة الخطوط السعودية للتموين': '6004.SR'}

transportation = {'الشركة السعودية للخدمات الصناعية (سيسكو)': '2190.SR', 'الخدمات الأرضية' : '4031.SR', 'الشركة السعودية للنقل الجماعي (سابتكو)': '4040.SR', 'الشركة السعودية للنقل والاستثمار (باتك)': '4110.SR', 'الشركة المتحدة الدولية للمواصلات (بدجت السعودية)': '4260.SR', 'شركة ذيب لتأجير السيارات' : '4261.SR', 'شركة لومي للتأجير': '4262.SR', 'شركة سال السعودية للخدمات اللوجستية' : '4263.SR'}

Consumer_Durables_Apparel = {'شركة مجموعة السريع التجارية الصناعية': '1213.SR', 'الشركة السعودية للتنمية الصناعية (صدق)': '2130.SR', 'شركة العبداللطيف للاستثمار الصناعي': '2340.SR', 'شركة لازوردي للمجوهرات' : '4011.SR', 'الأصيل' : '4012.SR', 'مجموعة فتيحي القابضة': '4180.SR'}

Consumer_Services = {'مجموعة الطيار للسفر القابضة': '1810.SR', 'مجموعة الحكير': '1820.SR', 'وقت اللياقة' : '1830.SR', 'شركة دور للضيافة': '4010.SR', '(شمس)شركة المشروعات السياحية': '4170.SR', 'شركة الخليج للتدريب والتعليم': '4290.SR', 'الشركة الوطنية للتربية و التعليم' : '4291.SR', 'شركة عطاء التعليمية' : '4292.SR', 'هرفي للأغذية' : '6002.SR', 'شركة ريدان الغذائية' : '6012.SR', 'التطويرية الغذائية' : '6013.SR', 'شركة الآمار الغذائية' : '6014.SR', 'أمريكانا' : '6015.SR'}

Media_Entertainment = {'شركة تهامه للاعلان والعلاقات العامة': '4070.SR', 'الشركة العربية للتعهدات الفنية' : '4071.SR', 'المجموعة السعودية للأبحاث والتسويق': '4210.SR'}

Retailing = {'شركة الحسن غازي إبراهيم شاكر': '1214.SR', 'الشركة المتحدة للإلكترونيات (اكسترا)': '4003.SR', '(ساكو)الشركة السعودية للعدد والأدوات': '4008.SR', '(ساسكو)الشركة السعودية لخدمات السيارات والمعدات' : '4050.SR', 'شركة باعظيم التجارية' : '4051.SR', 'شركة جرير للتسويق': '4190.SR', 'أبو معطي' : '4191.SR', 'السيف غاليري' : '4192.SR', '(سينومي ريتيل)شركة فواز عبد العزيز الحكير وشركاه': '4240.SR'}

Food_Staples_Retailing= {'شركة أسواق عبد الله العثيم': '4001.SR', 'الشركة السعودية للتسويق (أسواق المزرعة)': '4006.SR', 'شركة مجموعة أنعام الدولية القابضة': '4061.SR', 'شركة ثمار التنمية القابضة': '4160.SR', 'شركة بن داود القابضة' : '4161.SR', 'المنجم' : '4162.SR', 'الدواء' : '4163.SR', 'النهدي' : '4164.SR'}

Food_Beverages = {'مجموعة صافولا': '2050.SR', 'شركة وفرة للصناعة والتنمية': '2100.SR', 'الشركة السعودية لمنتجات الألبان والأغذية(سدافكو)': '2270.SR', 'شركة المراعي': '2280.SR', 'شركة التنمية الغذائية' : '2281.SR', 'شركة نقي للمياه' : '2282.SR', 'المطاحن الأولى' : '2283.SR', 'حلواني إخوان' : '6001.SR', '(نادك)الشركة الوطنية للتنمية الزراعية': '6010.SR', '(جاكو)شركة القصيم القابضة للاستثمار': '6020.SR', 'شركة تبوك للتنمية الزراعية': '6040.SR', 'الشركة السعودية للأسماك': '6050.SR', 'شركة الشرقية للتنمية': '6060.SR', 'شركة الجوف الزراعية': '6070.SR', 'شركة جازان للتنمية': '6090.SR'}

Health_Care_Equipment_Svc = {'شركة أيان للاستثمار': '2140.SR', 'الشركة الكيميائية السعودية': '2230.SR', 'شركة المواساة للخدمات الطبية': '4002.SR', 'شركة دله للخدمات الصحية': '4004.SR', 'الشركة الوطنية للرعاية الطبية': '4005.SR', 'شركة الحمادي للتنمية والاستثمار': '4007.SR', 'السعودي الألماني الصحية' : '4009.SR', 'سليمان الحبيب' : '4013.SR', 'دار المعدات' : '4014.SR'}

Pharma_Biotech_Life_Science = {'الشركة السعودية للصناعات الدوائية والمستلزمات الطبية': '2070.SR', 'جمجوم فارما' : '4015.SR'}

Banks = {'بنك الرياض': '1010.SR', 'بنك الجزيرة': '1020.SR', 'البنك السعودي للاستثمار': '1030.SR', 'البنك السعودي الفرنسي' : '1050.SR', 'البنك السعودي البريطاني': '1060.SR', 'البنك العربي الوطني': '1080.SR', 'مصرف الراجحي': '1120.SR', 'بنك البلاد': '1140.SR', 'مصرف الإنماء': '1150.SR', 'البنك الاهلي التجاري': '1180.SR', 'أملاك' : '1182.SR', 'سهل' : '1183.SR'}

Diversified_Financials = {'مجموعة تداول' : '1111.SR', 'الشركة السعودية للصناعات المتطورة': '2120.SR', 'شركة سناد القابضة': '4080.SR', 'النايفات' : '4081.SR', 'مرنة' : '4082.SR', 'شركة الباحة للإستثمار والتنمية': '4130.SR', 'شركة المملكة القابضة': '4280.SR'}

insurance = {'شركة التعاونية للتأمين': '8010.SR', 'جزيرة تكافل' : '8012.SR', 'شركة ملاذ للتأمين التعاوني': '8020.SR', 'ميدغلف للتأمين': '8030.SR', 'الشركة السعودية الفرنسية للتأمين التعاوني (أليانز إس إف)': '8040.SR', 'شركة أياك السعودية للتأمين التعاوني (سلامة)': '8050.SR', 'الشركة السعودية المتحدة للتأمين التعاوني (ولاء للتأمين)': '8060.SR', 'شركة الدرع العربي للتأمين التعاوني': '8070.SR', 'الشركة العربية السعودية للتأمين التعاوني (سايكو)': '8100.SR', 'شركة اتحاد الخليج للتأمين التعاوني': '8120.SR', 'المجموعة المتحدة للتأمين التعاوني (أسيج)': '8150.SR', 'شركة التأمين العربية التعاونية': '8160.SR', 'شركة الاتحاد للتأمين التعاوني': '8170.SR', 'شركة الصقر للتأمين التعاوني': '8180.SR', 'الشركة المتحدة للتأمين التعاوني (المتحدة)': '8190.SR', 'الشركة السعودية لإعادة التأمين التعاونية (إعادة)': '8200.SR', 'بوبا العربية للتأمين التعاوني': '8210.SR', 'الراجحي للتأمين التعاوني (تكافل الراجحي)': '8230.SR', 'شركة تْشب العربية للتأمين التعاوني' : '8240.SR', 'جي آي جي' : '8250.SR', 'الخليجية العامة' : '8260.SR', 'شركة بروج للتأمين التعاوني': '8270.SR', 'العالمية' : '8280.SR', 'الوطنية' : '8300.SR', 'أمانة للتأمين' : '8310.SR', 'شركة عناية السعودية للتأمين التعاوني' : '8311.SR'}

Software_Services = {'ام آي اس' : '7200.SR', 'بحر العرب' : '7201.SR', 'سلوشنز' : '7202.SR', 'علم': '7203.SR', 'توبي': '7204.SR'}

Telecommunication_Services = {'شركة الاتصالات السعودية': '7010.SR', 'شركة اتحاد اتصالات': '7020.SR', 'شركة الاتصالات المتنقلة السعودية(زين)': '7030.SR', 'عذيب للاتصالات"جو GO"': '7040.SR'}

Utilities = {'شركة الغاز والتصنيع الاهلية': '2080.SR', 'شركة الخريف لتقنية المياه والطاقة' : '2081.SR', 'أكوا باور' : '2082.SR', 'شركة مرافق الكهرباء والمياه بالجبيل وينبع' : '2083.SR', 'الشركة السعودية للكهرباء': '5110.SR'}

REITs= {'الرياض ريت' : '4330.SR', 'الجزيرة ريت' : '4331.SR', 'جدوى ريت الحرمين' : '4332.SR', 'تعليم ريت' : '4333.SR', 'المعذر ريت' : '4334.SR', 'مشاركة ريت' : '4335.SR', 'ملكية ريت' : '4336.SR', 'سيكو السعودية ريت' : '4337.SR', 'الأهلي ريت 1' : '4338.SR', 'دراية ريت' : '4339.SR', 'الراجحي ريت' : '4340.SR', 'جدوى ريت السعودية' : '4342.SR', 'سدكو كابيتال ريت' : '4344.SR', 'الإنماء ريت للتجزئة' : '4345.SR', 'ميفك ريت' : '4346.SR', 'بنيان ريت' : '4347.SR', 'الخبير ريت' : '4348.SR', 'الإنماء ريت الفندقي' : 'الإنماء ريت الفندقي.SR'}

Real_Estate_Mgmt_Devt = {'الشركة العقارية السعودية': '4020.SR', 'شركة طيبة القابضة': '4090.SR', 'شركة مكة للإنشاء والتعمير': '4100.SR', 'شركة الرياض للتعمير': '4150.SR', 'إعمار المدينة الاقتصادية': '4220.SR', 'شركة البحر الأحمر العالمية': '4230.SR', 'شركة جبل عمر للتطوير': '4250.SR', 'شركة دار الأركان للتطوير العقاري': '4300.SR', 'مدينة المعرفة الاقتصادية': '4310.SR', 'الأندلس' : '4320.SR', '(سينومي سنترز) شركة المراكز العربية' : '4321.SR', 'شركة رتال للتطوير العمراني' : '4322.SR', 'شركة سمو العقارية' : '4323.SR'} 

# ========================= SIDEBAR ===========================================
my_stock = {key:val for (key, val) in TASI.items()}


with st.sidebar:
    st.markdown(f'''<div style="display:flex;align-items:center;gap:8px;margin-bottom:18px;">
    <div style="width:32px;height:32px;border-radius:8px;background:var(--gold);display:flex;align-items:center;justify-content:center;font-size:16px;">{Page_icon}</div>
    <div><div style="color:var(--text-primary);font-size:13.5px;font-weight:500;">{page_title}</div>
    <div style="color:var(--text-muted);font-size:11px;">مؤشر تداول TASI</div></div></div>''', unsafe_allow_html=True)

    section_1 = st.selectbox('أختر نوع البيانات', ['الأسهم السعودية', 'السلع العالمية'], index=0)
    if section_1 == 'الأسهم السعودية': Section_list = Section_list
    if section_1 == 'السلع العالمية': Section_list = Section_list1 
    
    Section = st.selectbox('أختر القطاع', Section_list)
    if Section == 'المؤشر العام TASI': my_stock = my_stock
    if Section == 'قطاع الطاقة': my_stock = Energy
    if Section == 'قطاع المواد الأساسية' : my_stock = Materials
    if Section == 'قطاع السلع الرأسمالية': my_stock = Capital_Goods
    if Section == 'قطاع الخدمات التجارية والمهنية': my_stock = Commercial_Professional_Svc
    if Section == 'قطاع النقل': my_stock = transportation
    if Section == 'قطاع السلع طويلة الاجل': my_stock = Consumer_Durables_Apparel
    if Section == 'قطاع الخدمات الإستهلاكية': my_stock = Consumer_Services
    if Section == 'قطاع الإعلام والترفيه': my_stock = Media_Entertainment
    if Section == 'قطاع تجزئة السلع الكمالية' : my_stock = Retailing
    if Section == 'قطاع تجزئة الأغذية': my_stock = Food_Staples_Retailing
    if Section == 'قطاع إنتاج الأغذية': my_stock = Food_Beverages
    if Section == 'قطاع الرعاية الصحية': my_stock = Health_Care_Equipment_Svc
    if Section == 'قطاع الادوية': my_stock = Pharma_Biotech_Life_Science
    if Section == 'قطاع البنوك': my_stock = Banks
    if Section == 'قطاع الإستثمار والتمويل': my_stock = Diversified_Financials
    if Section == 'قطاع التأمين': my_stock = insurance
    if Section == 'قطاع التطبيقات وخدمات التقنية': my_stock = Software_Services
    if Section == 'قطاع الإتصالات': my_stock = Telecommunication_Services
    if Section == 'قطاع المرافق العامة': my_stock = Utilities
    if Section == 'الصناديق العقارية المتداولة (ريت)': my_stock = REITs
    if Section == 'إدارة وتطوير العقارات': my_stock = Real_Estate_Mgmt_Devt
    if Section == 'الذهب': my_stock = Gold
    if Section == 'الفضة': my_stock = Silver
    if Section == 'البلاتين': my_stock = Platinum
    if Section == 'النحاس': my_stock = Copper
    if Section == 'النفط الخام': my_stock = Crude_Oil
    if Section == 'الغاز الطبيعي': my_stock = Natural_Gas

    drop = st.selectbox('أختر السهم', list(my_stock.keys()))
    start = st.date_input('بداية المدة : اختر التاريخ', value = pd.to_datetime('2022-11-06'))
    end = st.date_input('نهاية المدة : اختر التاريخ', value = pd.to_datetime('today'))

# ========================== MAIN APP ===========================================
if len(drop) > 0:
    txt = "...انتظر قليـــلا"
    my_bar = st.progress(0 , text = txt)
    for pr in range(100):
        time.sleep(0.01)
        my_bar.progress(pr + 1 , text = txt)
    time.sleep(0.5)
    my_bar.empty()

    # ======= دالة جلب البيانات مع شرط مرن =======
    def get_market_data(ticker_symbol, start, end):
        try:
            df = yf.download(ticker_symbol, start=start, end=end, progress=False)
            
            # الشرط الجديد: إذا كان الجدول فارغاً تماماً فهذا يعني لا توجد بيانات
            if df.empty or len(df) == 0:
                raise Exception("لا توجد بيانات متاحة في هذه الفترة")
            
            return df
        except Exception as e:
            st.warning(f"تعذر جلب البيانات من yfinance: {e}.")
            return None

    ticker_symbol = my_stock[f'{drop}']
    Y = get_market_data(ticker_symbol, start, end)

    if Y is None:
        st.error("تعذر جلب البيانات. الرجاء التأكد من الاتصال أو اختيار سهم آخر.")
        st.stop()

    # فك ارتباط الأعمدة المتعددة (MultiIndex) في حال رجوعها من yfinance
    if isinstance(Y.columns, pd.MultiIndex):
        Y.columns = Y.columns.get_level_values(0)
        
    Y['Date'] = Y.index

    @st.cache_data
    def convert_to_csv(df):
        return df.to_csv(index=True).encode('utf-8')

    if st.checkbox(f' اظهر البيانات لـ: {drop}'):  
        display_df = Y.drop(['Adj Close', 'Volume', 'Date', 'price_change'], axis=1, errors='ignore')
        st.table(display_df)
        
        col_csv, col_excel = st.columns(2) 
        with col_csv:
            csv = convert_to_csv(Y)
            st.download_button(label="📥 تحميل البيانات كـ CSV", data=csv, file_name=f'TasiStock-{drop}.csv', mime='text/csv')

        with col_excel:
            buffer_excel = io.BytesIO()
            format_dict = {'Open': '{:.2f}', 'High': '{:.2f}', 'Low': '{:.2f}', 'Close': '{:.2f}'}
            with pd.ExcelWriter(buffer_excel, engine='xlsxwriter') as writer:
                Y.style.format(format_dict).to_excel(writer, sheet_name='Stock Data')
            st.download_button(label="📊 تحميل البيانات كـ Excel", data=buffer_excel.getvalue(), file_name=f'TasiStock-{drop}.xlsx', mime="application/vnd.ms-excel")

    st.divider()
    valid_closes = Y['Close'].dropna()
    last_price = Y['Close'].iloc[-1]
    # في حال رجعت بيانات السعر كـ Series بدلاً من رقم (مشكلة شائعة في yfinance مؤخراً)
    if isinstance(last_price, pd.Series): last_price = last_price.iloc[0]

    def currenc_convert():
        if Section_list == Section_list1:
            return "USD"
        else:
            return "ر.س"

    R = round(float(last_price), 2)
    Y['price_change'] = Y['Close'].pct_change()
    valid_changes = Y['price_change'].dropna()
    pc = valid_changes.iloc[-1]
    if isinstance(pc, pd.Series): pc = pc.iloc[0]
    R1 = round(float(pc), 5)
    R2 = "{0:.2f}%".format(R1 * 100)
    
    # حساب اتجاه السعر لتحديد اللون
    delta_color = "normal"  # الافتراضي (الرمادي)
    if R1 > 0: delta_color = "normal" # الأخضر في Streamlit هو Normal للأسهم
    elif R1 < 0: delta_color = "inverse" # الأحمر

    def currenc_convert_rate():
        if Section_list == Section_list1:
            return R*3.75 

    if Section_list == Section_list1:
        a, b = st.columns(2)
        a.metric(label=f"آخر سعر إغلاق لـ {drop}", value=f"{R:.2f} {currenc_convert()}",delta=f"{R2}", delta_color=delta_color)
        b.metric(label=f"آخر سعر إغلاق لـ {drop}", value=f"{currenc_convert_rate():.2f} ر.س ",delta=f"{R2}", delta_color=delta_color)
    else:
        st.metric( label=f"آخر سعر إغلاق لـ {drop}", value=f"{R:.2f} {currenc_convert()}", delta=f"{R2}", delta_color=delta_color)

    plot_chart = Y.drop(['Adj Close', 'Volume', 'price_change', 'Date'], axis=1, errors='ignore')
    st.subheader(f'  الرسم البياني لــ: {drop}' )
    plot_ = st.radio(label='***اختر نوع الرسم البياني***', options=('(يــومي)خط بياني','(يــومي)شموع'))
    
    if plot_ == '(يــومي)خط بياني':  #===== PLOTING THE LINE CHART =============
        fign = px.line(plot_chart)
        fign.update_layout(height=600)
        fign.update_layout(template='plotly_dark', paper_bgcolor='#161F35', plot_bgcolor='#161F35',
                            font=dict(color='#EDEFF4', family='Tajawal'))
        fign.update_layout(
                            xaxis=dict(
                                    rangeselector=dict(
                                        buttons=list([
                                            dict(count=1,
                                                 label="شهر",
                                                 step="month",
                                                 stepmode="backward"),
                                            dict(count=6,
                                                 label="ستة اشهر",
                                                 step="month",
                                                 stepmode="backward"),
                                            dict(count=1,
                                                 label="YTD",
                                                 step="year",
                                                 stepmode="todate"),
                                            dict(count=1,
                                                 label="سنة",
                                                 step="year",
                                                 stepmode="backward"),
                                            dict(label="الكل",step="all")
                                        ])
                                    ),
                                    rangeslider=dict(
                                        visible=True
                                    ),
                                    type="date"
                                )
                            )
        st.write(fign.update_xaxes(rangeslider_visible=True)) 
    
    if plot_ == '(يــومي)شموع':  
        df = Y.copy()
        if 'Volume' in df.columns:
            df = df[df['Volume'] != 0]

        fig1=make_subplots(rows=5, cols=1, shared_xaxes=True, vertical_spacing=0.01, subplot_titles=(f'{drop}', 'حجم التداول'), row_width=[1,1,1,3,4])
        
        # التأكد من استخراج البيانات أحادية الأبعاد للرسم
        open_data = df['Open'].squeeze()
        high_data = df['High'].squeeze()
        low_data = df['Low'].squeeze()
        close_data = df['Close'].squeeze()
        vol_data = df['Volume'].squeeze() if 'Volume' in df.columns else None

        fig1.add_trace(go.Candlestick(x=df['Date'], open=open_data, high=high_data, low=low_data, close=close_data, name=f'{drop}', increasing_line_color='#1FAE7A', decreasing_line_color='#E15361'), row=1, col=1)
        
        if vol_data is not None:
            fig1.add_trace(go.Bar(x=df['Date'], y=vol_data, marker_color='#1FAE7A', showlegend=False), row=2, col=1)

        if Section in Section_list1:
            market_rangebreaks = [dict(bounds=["sat", "mon"])]
        else:
            # السوق السعودي: الإجازة هي الجمعة والسبت
            market_rangebreaks = [dict(bounds=["fri", "sun"])]
            
        fig1.update_layout(height=900, template='plotly_dark', paper_bgcolor='#161F35', plot_bgcolor='#161F35', font=dict(color='#EDEFF4', family='Tajawal'))
        fig1.update_yaxes(tickfont=dict(size=15))
        fig1.update_layout(
                    xaxis=dict(
                        rangeselector=dict(
                            buttons=list([
                                dict(count=1, label="شهر", step="month", stepmode="backward"),
                                dict(count=6, label="ستة اشهر", step="month", stepmode="backward"),
                                dict(count=1, label="YTD", step="year", stepmode="todate"),
                                dict(count=1, label="سنة", step="year", stepmode="backward"),
                                dict(label="الكل", step="all")
                            ])
                        ),
                        rangeslider=dict(visible=False), # تم إيقاف الشريط السفلي لمنع التعارض
                        type="date",
                        rangebreaks=market_rangebreaks 
                    )
                )        
        with st.expander('التـحـليـل الفنــــــي'):
            with st.form('التحليل الفني'):
                colA, colB = st.columns(2)
                with colA: 
                    if st.toggle('[MA10]المتوسط المتحرك'):
                        df['MA10'] = close_data.rolling(window=10, min_periods=0).mean()
                        fig1.add_trace(go.Scatter(x=df['Date'], y=df['MA10'], marker_color='lightblue', name='MA10'), row=1, col=1)

                    if st.toggle('[MA50]المتوسط المتحرك'):
                        df['MA50'] = close_data.rolling(window=50, min_periods=0).mean()
                        fig1.add_trace(go.Scatter(x=df['Date'], y=df['MA50'], marker_color='rgb(160, 131, 40)', name='MA50'), row=1, col=1)

                    if st.toggle('مؤشر بولينجر باند'):
                        df['SMA'] = close_data.rolling(window=20, min_periods=1).mean()
                        df['stddev'] = close_data.rolling(window=20, min_periods=1).std()
                        df['Upper'] = df.SMA + 2 * df.stddev
                        df['Lower'] = df.SMA - 2 * df.stddev
                        fig1.add_trace(go.Scatter(x=df['Date'], y=df['SMA'], marker_color='rgb(106, 106, 106)', name='SMA'), row=1, col=1)
                        fig1.add_trace(go.Scatter(x=df['Date'], y=df['Upper'], marker_color='rgb(52, 108, 154)', name='stddev_UP'), row=1, col=1)
                        fig1.add_trace(go.Scatter(x=df['Date'], y=df['Lower'], marker_color='rgb(52, 108, 154)', fill='tonexty', fillcolor='rgba(31, 174, 122, 0.1)', name='stddev_LO'), row=1, col=1)
                    
                    if st.toggle('Ichimoku - إيشيموكو'):
                        # 1. حساب الخطوط الأساسية
                        df['tenkan_sen'] = (df['High'].rolling(window=9, min_periods=1).max() + df['Low'].rolling(window=9, min_periods=1).min()) / 2
                        df['kijun_sen'] = (df['High'].rolling(window=26, min_periods=1).max() + df['Low'].rolling(window=26, min_periods=1).min()) / 2
                        df['senkou_span_a'] = ((df['tenkan_sen'] + df['kijun_sen']) / 2).shift(26)
                        df['senkou_span_b'] = ((df['High'].rolling(window=52, min_periods=1).max() + df['Low'].rolling(window=52, min_periods=1).min()) / 2).shift(26)
                        df['bull_kumo'] = np.where(df['senkou_span_a'] > df['senkou_span_b'], df['senkou_span_a'], df['senkou_span_b'])
                        df['bear_kumo'] = np.where(df['senkou_span_a'] < df['senkou_span_b'], df['senkou_span_a'], df['senkou_span_b'])

                        fig1.add_trace(go.Scatter(x=df['Date'], y=df['senkou_span_b'], mode='lines', line=dict(width=0), showlegend=False, hoverinfo='skip'), row=1, col=1)
                        fig1.add_trace(go.Scatter(x=df['Date'], y=df['bull_kumo'], mode='lines', line=dict(width=0), fill='tonexty', fillcolor='rgba(31, 174, 122, 0.3)', showlegend=False, hoverinfo='skip'), row=1, col=1)
                        fig1.add_trace(go.Scatter(x=df['Date'], y=df['senkou_span_b'], mode='lines', line=dict(width=0), showlegend=False, hoverinfo='skip'), row=1, col=1)
                        fig1.add_trace(go.Scatter(x=df['Date'], y=df['bear_kumo'], mode='lines', line=dict(width=0), fill='tonexty', fillcolor='rgba(225, 83, 97, 0.3)', showlegend=False, hoverinfo='skip'), row=1, col=1)

                        fig1.add_trace(go.Scatter(x=df['Date'], y=df['tenkan_sen'], line=dict(color='blue', width=1.5), name='Tenkan-sen (9)'), row=1, col=1)
                        fig1.add_trace(go.Scatter(x=df['Date'], y=df['kijun_sen'], line=dict(color='orange', width=1.5), name='Kijun-sen (26)'), row=1, col=1)
                        fig1.add_trace(go.Scatter(x=df['Date'], y=df['senkou_span_a'], line=dict(color='#1FAE7A', width=1), name='Senkou Span A'), row=1, col=1)
                        fig1.add_trace(go.Scatter(x=df['Date'], y=df['senkou_span_b'], line=dict(color='#E15361', width=1), name='Senkou Span B'), row=1, col=1)


                    if st.toggle(' مؤشر الماك دي - MACD'):
                        df['EMA12'] = close_data.ewm(span=12, min_periods=1).mean()
                        df['EMA26'] = close_data.ewm(span=26, min_periods=1).mean()
                        df['MACD'] = df.EMA12 - df.EMA26
                        df['signal'] = df.MACD.ewm(span=9, min_periods=1).mean()
                        df['hist'] =  df['MACD'] - df['signal']
                        colors = np.array(['green' if x>0 else 'red' for x in df['hist']])
                        fig1.add_trace(go.Bar(x=df.Date, y=df['hist'], name='Histogram', marker=dict(color=colors)), row=4, col=1)
                        fig1.add_trace(go.Scatter(x=df['Date'], y=df['MACD'], marker_color='blue', name='MACD'), row=4, col=1)
                        fig1.add_trace(go.Scatter(x=df['Date'], y=df['signal'], marker_color='red', name='signal'), row=4, col=1)

                with colB:
                    if st.toggle('[MA100]المتوسط المتحرك'):
                        df['MA100']= close_data.rolling(window=100, min_periods=0).mean()
                        fig1.add_trace(go.Scatter(x=df['Date'], y=df['MA100'], marker_color='red', name='MA100'), row=1, col=1)

                    if st.toggle('[MA200]المتوسط المتحرك'):
                        df['MA200']= close_data.rolling(window=200, min_periods=0).mean()
                        fig1.add_trace(go.Scatter(x=df['Date'], y=df['MA200'], marker_color='rgb(254, 246, 186)', name='MA200'), row=1, col=1)
                        
                    if st.toggle('[RSI] مؤشر القوة النسبية '):
                        df['price change'] = close_data.pct_change()
                        df['Upmove'] = df['price change'].apply(lambda x: x if x > 0 else 0)
                        df['Downmove'] = df['price change'].apply(lambda x: abs(x) if x < 0 else 0)
                        df['avg Up'] = df['Upmove'].ewm(span=19).mean()
                        df['avg Down'] = df['Downmove'].ewm(span=19).mean()
                        df['RS'] = df['avg Up'] / df['avg Down']
                        df['RSI'] = df['RS'].apply(lambda x: 100 - (100 / (x + 1)))
                        fig1.add_trace(go.Scatter(x=df['Date'], y=df['RSI'], marker_color='blue', name='RSI'), row=3, col=1)

                    if st.toggle('lagging span - إيشيموكو'):
                        df['lagging_span'] = close_data.shift(-26)
                        fig1.add_trace(go.Scatter(x=df['Date'], y=df['lagging_span'], line=dict(color='purple', width=1.5), name='Lagging Span'), row=1, col=1)

                    if st.toggle('إشارات البيع والشراء'):
                        # حماية: حساب خطوط البولينجر في الخلفية إذا لم يقم المستخدم بتفعيلها من الزر الآخر
                        if 'Lower' not in df.columns or 'Upper' not in df.columns:
                            df['SMA'] = close_data.rolling(window=20).mean()
                            df['stddev'] = close_data.rolling(window=20).std()
                            df['Upper'] = df['SMA'] + 2 * df['stddev']
                            df['Lower'] = df['SMA'] - 2 * df['stddev']

                        # تحديد إشارات البيع والشراء
                        df['Buy_Signal'] = np.where(df['Lower'] > df['Close'], True, False)
                        df['Sell_Signal'] = np.where(df['Upper'] < df['Close'], True, False)

                        # تجهيز بيانات الشراء وإضافتها للرسم (سهم أخضر للأعلى)
                        buy_data = df[df['Buy_Signal'] == True]
                        if not buy_data.empty:
                            fig1.add_trace(go.Scatter(
                                x=buy_data['Date'], 
                                y=buy_data['Close'] * 0.97, # نضرب في 0.97 ليكون السهم أسفل الشمعة بمسافة واضحة
                                mode='markers', 
                                marker=dict(symbol='triangle-up', size=14, color='#1FAE7A'), 
                                name='إشارة شراء'
                            ), row=1, col=1)

                        # تجهيز بيانات البيع وإضافتها للرسم (سهم أحمر للأسفل)
                        sell_data = df[df['Sell_Signal'] == True]
                        if not sell_data.empty:
                            fig1.add_trace(go.Scatter(
                                x=sell_data['Date'], 
                                y=sell_data['Close'] * 1.03, # نضرب في 1.03 ليكون السهم أعلى الشمعة بمسافة واضحة
                                mode='markers', 
                                marker=dict(symbol='triangle-down', size=14, color='#E15361'), 
                                name='إشارة بيع'
                            ), row=1, col=1)
                    if st.toggle('حركة البيع و الشراء(Stochastic)'):       #Stochastic
                        # تطبيق الحل على القمة والقاع
                        df['14-high'] = df['High'].rolling(window=14, min_periods=1).max()
                        df['14-low'] = df['Low'].rolling(window=14, min_periods=1).min()
                        df['%K'] = (df['Close'] - df['14-low']) * 100 / (df['14-high'] - df['14-low'])
                        df['%D'] = df['%K'].rolling(window=3, min_periods=1).mean()
                        fig1.add_trace(go.Scatter(x=df['Date'], y=df['%K'], marker_color='blue', name='%K'), row=5, col=1)
                        fig1.add_trace(go.Scatter(x=df['Date'], y=df['%D'], marker_color='red', name='%D'), row=5, col=1)

                st.form_submit_button(label='تنفيذ')

        if st.checkbox('توقعات السهم'):
            df_train = df[['Date', 'Close']].copy()
            # التأكد من استخراج العمود كسلسلة بسيطة للموديل
            if isinstance(df_train['Close'], pd.DataFrame):
                df_train['Close'] = df_train['Close'].iloc[:, 0]
            df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})
            m = Prophet()
            m.fit(df_train)
            future = m.make_future_dataframe(periods=60, freq='D', include_history=True)
            forecast = m.predict(future)
            fig = plot_plotly(m, forecast)
            st.plotly_chart(fig)
      
        st.write(fig1)

#======= التبويبات المالية الإضافية =========
st.subheader(f'بيانات مالية إضافية لـ: {drop}')

if drop == 'المؤشر العام TASI':
    st.info("اختر الشركة من القائمة لعرض بياناتها المالية")
else:
    ticker = yf.Ticker(my_stock[f'{drop}'])
    dividends_tab, income_tab, cashflow_tab, balance_tab, ratios_tab = st.tabs(['التوزيعات النقدية', 'قائمة الدخل', 'قائمة التدفقات النقدية', 'الميزانية العمومية', 'النسب المالية'])

    with dividends_tab:
        Dividends = ticker.dividends
        if Dividends is not None and not Dividends.empty:
            # إضافة خيار للمستخدم لاختيار أسلوب العرض
            chart_style = st.selectbox("اختر أسلوب عرض التوزيعات:", 
                                       ["مساحي متدرج (حديث)", "أعمدة كلاسيكية", "منحنى النبض"])
            
            df2 = Dividends.reset_index()
            
            if chart_style == "مساحي متدرج (حديث)":
                figx = px.area(df2, x='Date', y='Dividends', template='plotly_dark')
                figx.update_traces(line=dict(color='#CBA135', width=3), fillcolor='rgba(203, 161, 53, 0.2)')
            elif chart_style == "أعمدة كلاسيكية":
                figx = px.bar(df2, x='Date', y='Dividends', template='plotly_dark', color_discrete_sequence=['#CBA135'])
            else: # منحنى النبض
                figx = px.line(df2, x='Date', y='Dividends', template='plotly_dark', markers=True)
                figx.update_traces(line=dict(color='#CBA135', width=2))

            figx.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(family='Tajawal'))
            st.write(figx)
        else:
            st.info('لا تتوفر بيانات توزيعات نقدية لهذا السهم.')

    with income_tab:
        income_stmt = ticker.incomestmt
        if income_stmt is not None and not income_stmt.empty: st.table(income_stmt)
        else: st.info('لا تتوفر قائمة دخل لهذا السهم حالياً.')

    with cashflow_tab:
        cash_flow = ticker.cashflow
        if cash_flow is not None and not cash_flow.empty: st.table(cash_flow)
        else: st.info('لا تتوفر بيانات التدفقات النقدية لهذا السهم حالياً.')

    with balance_tab:
        balance_sheet = ticker.balance_sheet
        if balance_sheet is not None and not balance_sheet.empty: st.table(balance_sheet)
        else: st.info('لا تتوفر بيانات الميزانية العمومية لهذا السهم حالياً.')

    with ratios_tab:
        info = ticker.info
        ratio_fields = {
            'مكرر الربحية (P/E)': 'trailingPE', 'مكرر الربحية المتوقع (Forward P/E)': 'forwardPE',
            'السعر إلى القيمة الدفترية (P/B)': 'priceToBook', 'العائد على حقوق الملكية (ROE)': 'returnOnEquity',
            'العائد على الأصول (ROA)': 'returnOnAssets', 'نسبة الدين إلى حقوق الملكية': 'debtToEquity',
            'النسبة الجارية (Current Ratio)': 'currentRatio', 'النسبة السريعة (Quick Ratio)': 'quickRatio',
            'هامش الربح الإجمالي': 'grossMargins', 'هامش الربح التشغيلي': 'operatingMargins',
            'هامش صافي الربح': 'profitMargins', 'عائد التوزيعات النقدية': 'dividendYield',
        }
        percent_keys = {'returnOnEquity','returnOnAssets','grossMargins','operatingMargins','profitMargins','dividendYield'}
        rows = []
        for label_ar, key in ratio_fields.items():
            val = info.get(key) if info else None
            if val is not None:
                if key in percent_keys and isinstance(val, (int, float)): val = f'{val*100:.2f}%'
                elif isinstance(val, (int, float)): val = round(val, 3)
                rows.append({'المؤشر': label_ar, 'القيمة': val})
        if rows: st.table(pd.DataFrame(rows).set_index('المؤشر'))
        else: st.info('لا تتوفر نسب مالية لهذا السهم حالياً.')

#======= آخر الأخبار =========
st.subheader(f'آخر الأخبار المتعلقة بـ: {drop}')
try:
    news_ticker = yf.Ticker(my_stock[f'{drop}'])
    news_items = (news_ticker.news or [])[:5]
except Exception:
    news_items = []

if news_items:
    news_html = '<div class="tasi-fade">'
    for item in news_items:
        content = item.get('content', item) if isinstance(item, dict) else {}
        headline = content.get('title') or item.get('title', '')
        link = (content.get('canonicalUrl', {}) or {}).get('url') or item.get('link', '#')
        if headline:
            safe_headline = html.escape(headline)
            news_html += (f'<a href="{link}" target="_blank" style="text-decoration:none;">'
                          f'<div class="tasi-news-item"><span style="color:var(--text-primary);font-size:12.5px;">{safe_headline}</span>'
                          f'<span class="tasi-news-arrow">\u2039</span></div></a>')
    news_html += '</div>'
    st.markdown(news_html, unsafe_allow_html=True)
elif drop == 'المؤشر العام TASI':
    st.info('أختر من القائمة الجانبية السهم لعرض أخباره') 
else:
    st.info('لا تتوفر أخبار حالياً لهذا السهم.')
#    st.info(st.checkbox('لا تتوفر أخبار حالياً لهذا السهم هل ترغب في عرض اخبار الاسهم السعودية.'))


#========================= Trending world News via RSS Feed ==========================

def trending_news_rss(rss_url, limit=3):
    try:
        st.subheader("🌐 الأخبار العالمية")
        response = requests.get(rss_url, timeout=5)
        root = ET.fromstring(response.content)
        articles = root.findall('.//item')
        
        for i, article in enumerate(articles[:limit], 1):
            title = article.find('title').text
            link = article.find('link').text
            
            # استخدام الـ CSS الموجود مسبقاً في CUSTOM_THEME الخاص بك
            st.markdown(f"""
            <div style="background-color: var(--bg-card); padding: 15px; border-radius: 10px; border-left: 4px solid var(--gold); margin-bottom: 10px;">
                <p style="font-weight: bold; color: var(--gold); margin-bottom: 5px;">{i}. {title}</p>
                <a href="{link}" target="_blank" style="color: var(--hero-accent); text-decoration: none; font-size: 0.9em;">قراءة المزيد ↤</a>
            </div>
            """, unsafe_allow_html=True)
    except Exception as e:
        st.info("عذراً، خدمة الأخبار غير متوفرة حالياً.")

# عرض الأخبار
url = "https://news.google.com/rss?hl=ar&gl=SA&ceid=SA:ar"
if drop != 'المؤشر العام TASI':
    trending_news_rss(url)


if st.checkbox("Show ASCII Code"):
    st.code('''
                                    ........--======++++++++*****++*********x$$$$$$&&&&&$$#x**+++=============-
                                    .......---======++++++++*****+********x#$&&&X&&&&&&$$&$$$$$$$$#x+==========
                                    +++++==--======+++++++++***+++****x#&&XXXXXXXXX&&&&&&&&$$$$$$$#$##*+-...===
                                    &&&&&$$#xx*++=++++++++++***+++++*$&XX&&X&&X&X&&&&$&&&$$$&##$#xx**=-.     -=
                                    &&&&&$$$$$$$#x++++++++++++.     ....................... .
                                    XX&&$$$#$$$##$#*+++++++++=
                                    &&&&$$#######$&$x*+++++=
                                    &&&$$########$&$#x*+++*=                                               .--=
                                    $$$$$#########$$#xxxxxx#x***+++++=-===-=---------............--.-====+=++++
                                    *xx############$#xx#$$$&X&&&&&XX&#$&&XXXX&$x+=+*#xx****xx****##++*xx*x+***+
                                    xxx**x##########x**+*+x#$&&&&XXX$$&XXXX$x+======+xxx**x##x*x#$$#*x###xx***+
                                    #xxx***x########**x**+++=+x#$$$$x#$&$#*******+++=+xxxxxxxx##$$&$x*x$##x****
                                    xxxx****x#####x#*$$x***+=+x$$$&&&&&$$&$$$##xx*++==*xxxxxxx##$$&&#xx####x*x*
                                    ++++*****x#&&$xx$&$x+===-+#$$&&$&&&&&$$$####xx**+==xxx#xx##$&&&$$x*x#$$x***
                                    ==+++*xx*x&X$x*x&$x+=**==+*+x##$$$$##xxxxxxxxxx*+==##x#x##$$&$&X&#**x#$#x*+
                                    xxxx###xx&&$x+*##x+-+x+-=.---=+*#$#*++=-...---=++==xx##x#$$$&XX$&$x*x####**
                                    $$$$&$#x$$#*++##x*==*+=-=-*#x****$$#+==****+=----==*x#x#$$$&&&&X&$#x*x#$#*+
                                    &$&&$x+*$#x+=##x*+-++==-===...-+x&&x+++*=----=--=-==###$$&&&&X&&&$#xxx####*
                                    $&$#*=+##x*=##x*+-++=-=--==*x#x#&&$x+*xxxxx****+===+*#$$&&&XX&XX&$$#*x###x*
                                    &$*+=+##x*=#$xx+-=++=-====+x##$&X&$x**x#######xxxxxx**$&&&X&XXX&&&$xxxx###x
                                    #*+=+$#x*=*#x**==+++==-=-=+#&&XXX&$##xx#&&&&$$$$##xx*+=x&X&XX&&&&$$#x*x###x
                                    *+=+##x+.=x*++-+**+=======+$&&XXX&$#xxx*$&&&&&&$##x*++==+$&&&X&&&&$##xxx###
                                    *=*##xx+*x*+=.=***=*=+===+*&&&&X&$#*x#x*+$&&&&&$#x**+=====*&&&&&&&$$#xxx###
                                    $&$x*x##x*****x++=+**+==+=*$$#&&&$#x##x*=+#&&&$##x*++==-====x&&&&$$##xxxx##
                                    $#x**#x***x#$x**+=xxx**=+++xx+x##x*=..-=+**x####x**++=========#&&$$$##*x###
                                    x*++**++*x##x**+=*x#x*x++++**+-  ... .....--=+***+++++========-+$$$##x#xx##
                                    ++++++**xxxx***++*xxx###xx*+++ .==*+=-.....   -+*+++*++======--..x$$##xxxxx
                                    ++++*x*xx****++=*x#$$$#x*+==++*++*****++=====-=xx*+***+======-....+$$##xxx#
                                    ++*xxxx###x*+=+#&&$$#*+==-+==+*#xx#$#xx*xxx**+*#x++***+===----.....-$$xxxxx
                                    **xxx#$$$#*+*x$$$$#*+==--==+=++*x#xxxxxx********++++++=-----...... .&####x#
                                    *x##$$$$#x##$$$##*+*$*===+=+++*+x*=.-==++***xx*++++++==--......... .&&$#xxx
                                    #$$$$$$$$$$$###x+*###x==++*+**+***++++*****xx***+++++=-............-&&$##xx
                                    $$$$$$$$$##x**++x*=. -++*+***xx*-......-=--=========--.............-X&&$#xx
                                    $$$$$##xx**+==*=     .+**xxxxxx*=        .    .------.........-....-X&&$$#x
                                    ####xx**+=-=*+        **x*xx##x*++.          ....---........-----..=XX&&$##
                                    ****+++==+*+.         -*xxx###xx*+=-=+++*+=----------.....---------=&&X&$$#
                                    -===---==.             +xxx####**==--+***++-.  -----...-----------.=&XX&$$#
                                      -.                    xx####xx**=--=**x**=.  ..........-...--..--=XX&&$$$
                                    .+                      .######**++===*xxx*=.  ..-.-..-----------===&X&&$$$
                                    .                        .$#$##x*+++=-+xxx*=.  ....----------=++===+&XX&$$#
                                                              -##$#x**+=+++*##x=   .---========-=+++++++&X&&&$$
                                                               -###xx++*+++*##x= ..-=--=====++====+++++*XX&&&$$
                                                                .###***++****##+.---==++**+*++=+++++++++&XX&&$$
                                                                 .xxx*+*****x##=---=+++x*x+**=*****++**+&XX&$$$
                                                                  .xxx****xx*x#====+*++**+**++****+++++*&XX&&$$
                                                                    *x*+*x*x**x=.++*********+**++++++++*&XX&&$$
                                                                     +xx***x*+*=.**********++**+********&XX&$$$
                                                                      =x*xx**++--**********+************&XX&$$$
                                                                       -xx**x*-.=*********+*************&XX&$$$

            
                                                                    .-+++=.
                                                               =x&XXXXXXXXXX&#=.
                                                            *XXXXX&&$#x**+=--...
                                                           --...

                                                                     .....==**xxx+=-..-
                                                        .=*x#$&X&&&XX&&&XXX&#*+===--+*#$.
                                                      ##++xx*x#$&XXX&#x$#x+===---...x*&X&.
                                                    .&X**+---=++**xxx########x*++=.=+=#X&&.
                                                    XXXx+ -+*###x##$&&&&&$$x*++++++=-=*$&X&
                                                   #XXXX$+=*=--...-=*#$$#*=.....-.=+=*#$&XXx
                                                  =XXXXXX$+++*+==..-+x$&#----. ..-+##&&XXXX&.
                                                  &&XXXX@Xx*+=-=*--=xx&X$=++*+--.-+$&XXXXXXX$
                                                  XXXXXXXX$x$###xx#$$$&X&*+xxxx*xx#*==++x$&X&+
                                                 .&X@XXXX@$$&&&&&&&&$$XX&*+*$&&$$$#x+.  .=+*x$.
                                                  &XXX&+=-+#$&XXXX&&$&XX&x**#&&&$#x*=.  ==++++*
                                                  &X&*.   =x#$&&&&$&x-=++. .+#$$#x*==   $xxx*xx*
                                                  &#*=-   .+xx#$#x*+-.      ..-*x*+=.  =&$XX&&&$*
                                                  ***+-.   .==*x+. .=======-.  .+=..   &x&X&&&&$$
                                                  *x*+-.    ...== ++x##$##x*==- -.    +&*XX&XX&&&
                                                  **++--.       .-##x*+=-=--+*+..    .X+$&XXX&&&&
                                                  ***x==-.       .*$$#-...-+**-      $#+XXXXXXX&$
                                                  **x*=++-.       .-==--......      $$=&XXXXXXXXx.
                                                  x*#*=*+++.                       #X+xXXXXXXXXX=+
                                                  **##=+*x*+.                     #X**XXXXXXXXXx-++
                                                  =*+X*+**xx-=                 .-#Xx+&XXXXXXXXX=-=+.
                                                  .x+#X##xxx=*x+-.      ..-==+++#X#*&XXXXXXXXXx=--==
                                                   x###X&&$#+*&&&$#$#########x#&X$*&XXXXXXXXX&+=--==---=..
                                                   .$&$$XXX&$$&&XXXXXX&&&&&&&&&X$*$XXXXXXXXX&*x*x*x+&+&&#$&.
                                                 .=*$&X&&&XXX#&XXXXXXXX@@@XXXXX&*&XXXXXXXXXXx*$&$$$$&#X&&X&
                                                 &@X&@X&XX&XXX&XXXXXX@@@XXXXXXXx$XXXXXXXX@Xx#&XX&&&X&&X&XXx
                                                 .XXXX@$$xx$&&X&&X@@@@@@@&&XXXx$XX@XXXXXXX$&&XXXXXX@&X@X&@+
                                                  +XX&X&$xx=+*x&XX@@@@@@XXX@Xx$XXXX@@XXXX&XXXXXXXXX@XXXX&@=
                                                   $X&&X&X##&&&XXXX@@@@@XXXX#$XX@XXXXXXX&XXXXXXXXXX@XXXX&@+
                                                   .&&XXX&&&$XXXXXX@@@@XXXX#$XXXXX@@@X&$XX@XXXX@XXX@X@XXXX*
                                                    +X&&&&&#XXX@X&@@@@XXX@&&XXXX@XXX&#$X@@XXXX@XXXX@X@XXX&x
                                                     *&&&&&&$XXX&X@@@@XX@&&X@X@XXXXx#&X@@@XXX@@@XXX@X@XXX&#
                                                      =&&&$&$$X&X@@@@XX@X&XXX@@XX&xx&X@@@XXXXX@XXXXXX@XXX&&
                                                       =$&&$&$*&@@@@XXX@&@@@@@XX&$x&X@@@@XXXX@XX@XX$X@XXX&X
                                                        .#$&#$$#&@XXX@XX@@@@@@XXX$&X@@@@XXXXX@X@XXX@X@XX@&X
                                                          *$$##$$$&XX@XXX@@@@@XXX&X@@@@XXXXXX@@XXX@XXXXX@&@
                                                           -#$$x$&$$XXX@@@@X@@XXXXX@@XXXXX&XXXXXXX@@XXXX@$X-
                                                             +#$##$&$$&X@@X@@XXXXX@XXXXXX&X@@&XXX@XXXXXXX&X+
                                                              .*$$##$&$&&@@@@XXXXXXXXXXXXXXX@XXXXXXX@X@XXX&x
                                                                -=++++++++***************+*******+********++

xxx**++***xxxxx##$$#x##$$$$##$$$$$$$$$#$$$$$$$&&&&&&$&$$##x*++=---.-..         .=+*+-.....==---.-=**+==*xxxx************xxxxxxxxxxxx#$$&&$$&&$$&&$#$&&
x#x**++**xxx##xx##$$#xx#$$$$##$$$$$$$$#$$$$$$&&$$&&&&&$$xxxx*=-------.          ...-......=+***+-..--=+*xxxx************xxxxxxxxxxxx#$$&&$$&&$$&&$#$&&
x#xx*+***xxx##xxx##$$#xx#$$$###$$$$$$$#$$$&$$&&$$&&&&&$xx##x+=======-.   ..--.   ....-=*$XXXXXXXX&*.. .+xxxxxxxxx***x****xx*xxxxxxxx#$$&&$&&&$$&&$#$&&
x#xx*+***xxx##xxxx##$$#xx#$$$##$$$$$$$$$$$$$$$&$&&&&&$x*x$#*=====+=-.....-===-  ...-*&XXXXXXXXXXX#-. . +xxxxxxxxx***x****xx**xxxxxxx#$&&&$$&&$$&&$#$&&
x#xx*****xxx##xxx*x##$$###$$$$##$$$$$$$$$$$$$$&$$&&&&#**#$#++=--==--....--=++-....#&XXXXXXXXX&#+.   . +$#xxxxxxxx********xxxxxxxxxxxx$&&&$$X&$$&&&$$&&
x##x*****xxx###xx**x#$$$###$$$$##$$$$$$$$&$$$&&&&&&&$x*x$$x+==-...---...-==++-- +&XXXXX&$#*=-       -#&&&$xxxxxxx********xxxxxxxxxxx#$$&&$$&&$$&&&$$&&
x##x*****xxx###xxx**x#$$$###$&$$#$$$$$$$$$&$&&&&&&&&$x*#$$*+=-....---...-=++=. ..--...          .-+#&&&&&&$xxxxx*********xxxxxxxxxxx#$&&&$$&&$$&&&$$&&
x##x*****xxx###xxxx*xx#$$$###$$$$#$$$$$$$&&&&&&&&&&&$x*#$#*==-.  .---...-==+-.              -=*#$$&$$&&&$&&xxxx**********xxxxxxxxxxx#$&&&$$&&$$&&&$$&&
x##x*****xxx####xxxxxx##$$$###$$$$##$$$$&&&$&&&&&&&&$**#$#+=-..  .---...-==+#$*+=-====+x#&&&&&&&&&&&&&&&#&$#xxxx********xxxxxxxxxxxx#$&&&$$&&$$&&&$$&&
x##x*****xxx####xxxxxx###$$$$##$$$$##$$$&&&&&&&&&&&&$x*x$#==--.  .---. .-==$&&XXX&&&&$$###&&$&&&&&&&XX&$#$$$xx**********xxxxxxxxxxxx#$&&&$$&&$$&&&$$&&
x##xx****xx#####xxxxxx####$$$$##$$$$$$$$&&&&&&&&&&&&&#xx$#+=--=-...--. .-$X&x#+=+x#$#x+===-$$&&&&XXXXXX$$$$&#xxxxxxxxxxxxxxxxxxxxxxx#$&&&$$&&$$&&&$$&&
x##xx****xxx#####xxxxx######$$$$$$$$$$$$&&&&&&&&&&$$$$##$#*=-=*+-..-...*&&&&$x****#$x=--==+x&&&&&XXXXXX&$#$&$xxxxxxxxxxxxxxxxxxxxxxx#$&&&$$&&$$&&&$$&&
xx#xx****xxx#####xxxx########$$$$$$$$$$$&&&&&&$##xx**xxxxx*+=+**=---.-$#$##$#x*=+-+&#*+-=--=&&&&&XXXXXX&&x&&&x*****************+++**x$&&&$$&&$$&&&$$&&
#xxxx***xxx######xxxx#########$$$$$$$$$$&&&&$#xx#$$$&$$#xx*=-.-==-...*$&&$&$#x+*$#XX$$#x**xx#&XXXXXXXXXX&x&&$$#xxxxxxxxxxxxxxxxxxxxxx$$&&&$&&$$&&&$$&&
xxxxx***xxx#######xxx###########$$$$#$$$$$#x**x#$$####xxxx*+-..---. .*&&&&$$x*=*XXX&$$$&&&&&$x#&XXXXXXXX&x&&&&$*******xxxxxxxxx*****x$$&&&$&&$$&&&$$&&
$##xx***xxxx#####xxxx############$$$$$$$$$xxx$$$#*+===+****+=.--=-..=*&&&&$#x*==&XX&$$x$&&&$#*+-*&XXXXXX&xX&&&&#xxxx****xx**xxx****xx$$&&&$&&$$&&&$$&&
&$$#xx**xxxx#####xxxx##############$$$$$$###&&$x+======+++*+---=+=..==#&&&##x*==x*=-.-*#$$#*++-. .$XXXXX&#X&&&&&#x*xxxxxxxxxxxxxxxxxx$&&&&$&&$$&&&$$&&
&&$##x***xxx#####xxxx#############$$$$$$###&&$*++++=-.-+x##x+=+++=. ..=&&$#x$*++-.====-..+*=---. -&*x$XXX$X&&&&&$#xxxxxxxxxxxx**xxxxx$&&&&$&&$$&&&$$&&
&$#xxx***xxx#####xxxx#############$$$$$#xx$$#*++++=-..+x#$#*=-+*+-   ..&$$##$**x*-#$##x*+--......$&*=+#&X&X&&XX&&$##########x#xxxx###$&&&&$&&&$&&&$$&&
&$#xx****xxx#####xxxxx#################xx###*==+===-.-=+*x*---++=.  ---$$$$$&xxxx=++.-*#*-..... +X&++x$$&&X&&XX&$&$#xxxxxxxxxxxxxxxx#$&&&&$&&&$&&&$$&&
$#xxx****xxx#####xxxxxx###################$#++++==-----==-..-=++=. .---$$&&$&$$xx*.---==-.  ....&X#**$&&&&&&XXX&&&&$x*****x#$$$#xx***#$&&&$&&$$&&&$$&&
$xxxx*****xx#####xxxx#############$#$$$$$&$#+*x*==-==......-=++=-.     +&&&&&&$xxx=..    ....-=#X&x*x&&&X&&&XX&X&$&&$$&&&&####X@XXX&$#&&&&$&&$$&&&$$$&
#xxxx*****xx#####xxxxxx###########$#$$&&&&$#xx#*==*x=.   ..-===-.      .*&&&&&$#x*====++++*xx##&X$+x&&&&&&&&&XX&&&$&&&&$$#$$#$&X@#$XX&&&&&$&&&$&&&$$&&
xxxxx*****xxx####xxxxxxx##########$#$$&&&&&$###x++##+.  ..---==. ........-#X&&$#x*=+*x#$$$$$$$&&Xx*#XX&$&X&&XXXXXXXXXX&X@XXX&&x$X&$&$&&X&&$&&&$&&&$$$&
xxxxx******xx####xxxxxxxxx##########$$&&&&&$####**##*...=*+--==.  ......  .$&&$xx+#$&&&&&&&&&&&X&+x&&x=&XXXXXXX@@@@X&*---=+==+#$&&$$XX&$$&&&&&$&&&$$$&
xxxxx******xx#####xxxxxxxxx#########$$&&&&&$$###xx##x=..*x*--==-..........xXXX$#+#X@@@XXX&&X&&XXxx&$x++XX&&XXX@@@X&=.        .##x#*x#x&&$&@$$$$&&&$$$&
x##xx******xx####xxxxxxxxxx#########$$&&&&&$$$$$$$$$$x==*#x---==.........xXX&&$xxX@@@XXXXXXX&&&$*x$&x##&&&&X@@@X&=.   .....   .**x$&&###*x#&$&&&&&$$$&
*xxxx******xx####xxxxxxxxxx#########$$&&&&&$$&&&$$&&$$#xx$$*---....... .+XXX$&#x&@@@@XXXXXX&&X&*=$&$$&$&&X@@@XXx.   ......     -###$$$x#x###$&&&X&$$$&
*x#xx******xx#####xxxxxxxxxx########$$&&&&&$$$&&&&&&&&$$#x*=-......... .&XX$&$x$@@@@XXX@@X&&XX$**X&&&X&&XX@@XX=   .........     *$$####$$$&$$&&X&X$$$&
*x#xx******xx####xxxxxxxxxxx########$$&&&&&$$$$&$&&&&&$#+++=...........+XXX$&x$@@@@@X@@@XX&XX&**$X&&XX$X@@@X$.  ...........     .$$$$$$####&&$$&&&&$$&
*x##x******xx####xxxxxxxxxx#x#######$$&&&&&$$$$$$$$&$#*++*x-...........$XXX$##X@@@@X@@@@X&XXX&+#X&&&X$$XXXX#.  ............      +$$$$$$$###&##X&&&$$&
xxxxxx*****xx####xxxxxxxxxxxxx####$##$&&&&$$$$#######*++*x*.. .  . ....&XXX##X@@@@X@@@XX&&X&&#*$X&&XX#XX@Xx   ...........         x#######x#$xx&$$&$$&
xxxxxx*****xx###xxxxxxxxxxx##xx#$$$&#x$&&&$#x**+++++++++x=   .   .    -X&X&xX@@XX@@@@@X&&&&&&##XXXXX&$XXX#  .......   ..  ...     -xx#x#xxx#$x#@$$&$$&
xxxxxx******xx###xxxxxxxxxxxx#$$$$$$$$$$##$$#$##*+++==++. . ..   .    =X&XXX@@XX@@@@@@X&&X&&&#$XXXX&$&XX$. .. ..  .... ..          +*xxx*x*x#**&$$$$$&
+++****xxx***xx*xx**xxxxxxx##########$$$$$#x##*+++=====.   ...  ...   =XXXXX@XX@@@@@@@XXX&X&$x&XXXX&#$XX-  .  .  .........      .  .********x+$$##$$$&
-===========++++++===++++++*+==+**xxxx####$$$#x++==++. . ..------==   =X&XXXXX@@@XXXX&&XX&&&$#&XX&&##&&x  ....-  ..-......  ..      =***x**+*+$#xx$$$&
.       ..----.. .........------..-====+*x##$$$$#*++==+x$&&XXXXXXXXx. =X&X&#&X@@XXXXX&&&&X&&x$&&&&#x$&$. ...... .---...--.   .    .. +++++++=+*xxx&$$&
........                            .-.   .-=*#$$#x$X&$##&&XX&&&&&&&&*+XXX$=x$&XXXXXX&&X&&&&x&&&&$*#$x.  --. .-..-.--...-.       ... -+==+=+-xxxx#&$$&
.                                   ...---..    .=+*++&$$#x#$$$##XXX&&$&&X=-=x&XXXXX&&&X&&&&x&&$$xx$#.  -.-.. .- ........         ..  ++=+--+*xx*&&$$&
*=-.      -x=*-                           ......    -*++=+x###++=&&&&$$$$$$$$$+-=+x#$&&#$$&$$&$$#x$$-. .-.....     .-....         ... -=+==-xxxxxX&$$&
$$$x-     *X&X&=+&=-+x+.                        ....-=-----.=++=x&&$&$$###&@@X+..  . ......=**+++=+=.        .     ......           . .=+--**#x*$X&$$&
&*-.+&*#*-#XXXXXXX&XXX$-                           .--.-..---==-==+==#####$XXX#.       ..... .....           ...    .....              +==-xxxx*#$$$$$
$x#&XXXXXXXXXXXXXXXXXX&&x-        .==========-----------.....-------.*xx##$&&&#*         ...  . ....          ..-.   ...               =--=*#x*#$$$$$$
X&#&XXXXXXXXX&XXXXXXX&x-.         .-=======....-------..   ..........  .--&&&$#x-              .  .            ...     .               .-.**#xxXXXXXX&
X&$$&&&$&XX&&&&&XXXXXXX&#=-=**xx#x.---=----.......------...---------------====-----===---      .---..           ...                    ..-$#x*$XXXXXX&
&&&XX&&$$$&&$$$&&&&XX&&&&$$&&XX&$=-..-x===+=+++======----............---------------=====-..----========         ..                     -+##xxXXXXXXX&
&$$$$&$*x$X&&&&&XX$**#$&&&&&$$$##$#=+xx-==++++=========++++++=---------------------============+++++===-       .                        -**x++xXXXXXXX
+xx**xxx#&XX&XXXX#*x#$$$######++###&$+**=-======+#x+++++++++--.---================+$#===========--------                                ++**++*####$$$
x**+$&&&&&&&$$&&&$=-=+xxxx##$$&&X&&&x-..--------=+=--======-.-..-------------------==-.---............--                                +*#***x$$$$$$$
**x#&XX&&&&XX&#=+$$*=*x####xx*x$$$$$$#-.-.......-+=---------.-..-..................--..... .  ..........---------...... ....            +*+++++*$$$$$$

            

            
            ''')
    
