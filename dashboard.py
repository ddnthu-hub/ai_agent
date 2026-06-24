import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import numpy as np

# ==================================================================
# CONFIG
# ==================================================================
st.set_page_config(
    page_title="PHÂN TÍCH AI AGENT - KHOA HỌC MÁY TÍNH",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==================================================================
# PREMIUM LIGHT CSS
# ==================================================================
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">

<style>
:root{
  --bg:#F6F8FF;
  --surface:#FFFFFF;
  --line: rgba(17,24,39,.08);
  --text:#0F172A;
  --muted:#5B6478;
  --brand:#4F46E5;       /* indigo vivid */
  --brand-2:#06B6D4;     /* cyan vivid */
  --accent:#F43F5E;      /* rose */
  --lime:#84CC16;
  --amber:#F59E0B;
  --emerald:#10B981;
  --sky:#0EA5E9;
  --violet:#8B5CF6;
}

.stApp{
  background:
    radial-gradient(900px 500px at 5% -10%, rgba(79,70,229,.18), transparent 60%),
    radial-gradient(700px 500px at 100% 0%, rgba(6,182,212,.18), transparent 60%),
    radial-gradient(700px 500px at 50% 110%, rgba(244,63,94,.12), transparent 60%),
    var(--bg) !important;
  color: var(--text);
  font-family:'Inter', system-ui, sans-serif;
}
#MainMenu, footer, header {visibility:hidden;}
.block-container{padding-top:2.2rem; padding-bottom:4rem; max-width:1400px;}

h1,h2,h3,h4,h5{
  font-family:'Space Grotesk','Inter',sans-serif;
  letter-spacing:.02em; color:var(--text);
  text-transform: uppercase;
}
h1{font-weight:700;} h2{font-weight:700;} h3{font-weight:600;}
.stMarkdown p, label, span, div { color: var(--text); }
.small-muted{color:var(--muted); font-size:.92rem; text-transform:none;}

/* HERO */
.hero{
  position:relative; padding:30px 34px; border-radius:24px;
  background: linear-gradient(135deg, #EEF2FF, #ECFEFF 55%, #FFE4E6);
  border:1px solid var(--line);
  box-shadow: 0 30px 60px -30px rgba(79,70,229,.35);
  overflow:hidden; margin-bottom:26px;
}
.hero .eyebrow{
  font-size:.78rem; letter-spacing:.28em; color:var(--brand);
  font-weight:700; margin-bottom:10px; text-transform:uppercase;
}
.hero h1{
  font-size:2rem; line-height:1.15; margin:0; text-transform:uppercase;
  background: linear-gradient(90deg,#4F46E5,#06B6D4 60%,#F43F5E);
  -webkit-background-clip:text; -webkit-text-fill-color:transparent;
}
.hero p{color:var(--muted); margin:.7rem 0 0; max-width:920px; text-transform:none;}

/* KPI */
.kpi{
  position:relative; padding:22px 22px 20px; border-radius:18px;
  background: var(--surface);
  border:1px solid var(--line);
  box-shadow: 0 10px 30px -18px rgba(15,23,42,.18);
  transition: transform .25s ease, box-shadow .25s ease, border-color .25s ease;
  height:100%;
}
.kpi:hover{transform:translateY(-3px); box-shadow:0 20px 40px -20px rgba(79,70,229,.35); border-color:rgba(79,70,229,.35);}
.kpi .label{font-size:.74rem; letter-spacing:.18em; color:var(--muted); font-weight:700; text-transform:uppercase;}
.kpi .value{
  margin-top:10px; font-family:'Space Grotesk',sans-serif; font-weight:700;
  font-size:2.1rem; line-height:1;
  background: linear-gradient(90deg,#4F46E5,#06B6D4);
  -webkit-background-clip:text; -webkit-text-fill-color:transparent;
}
.kpi.good .value{background: linear-gradient(90deg,#10B981,#84CC16); -webkit-background-clip:text; -webkit-text-fill-color:transparent;}
.kpi.warn .value{background: linear-gradient(90deg,#F59E0B,#F43F5E); -webkit-background-clip:text; -webkit-text-fill-color:transparent;}
.kpi.bad  .value{background: linear-gradient(90deg,#F43F5E,#8B5CF6); -webkit-background-clip:text; -webkit-text-fill-color:transparent;}
.kpi .sub{margin-top:8px; color:var(--muted); font-size:.85rem; text-transform:uppercase; letter-spacing:.08em;}
.kpi .bar{
  position:absolute; left:18px; right:18px; bottom:10px; height:3px; border-radius:3px;
  background: linear-gradient(90deg, var(--brand), var(--brand-2), var(--accent));
  opacity:.85;
}

/* Sidebar */
section[data-testid="stSidebar"]{
  background: linear-gradient(180deg,#FFFFFF 0%, #F1F5FF 100%) !important;
  border-right:1px solid var(--line);
}
section[data-testid="stSidebar"] *{color:var(--text) !important;}
section[data-testid="stSidebar"] h2{text-transform:uppercase; font-family:'Space Grotesk',sans-serif;}
section[data-testid="stSidebar"] [role="radiogroup"] label{
  padding:10px 12px; border-radius:12px; margin-bottom:6px;
  border:1px solid transparent; transition: all .2s ease;
  text-transform: uppercase; font-size:.82rem; letter-spacing:.06em; font-weight:600;
}
section[data-testid="stSidebar"] [role="radiogroup"] label:hover{
  background: rgba(79,70,229,.08); border-color: rgba(79,70,229,.25);
}

/* Alerts */
div[data-testid="stAlert"]{
  border-radius:14px; border:1px solid var(--line);
  background: #fff;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"]{gap:6px; border-bottom:1px solid var(--line);}
.stTabs [data-baseweb="tab"]{
  background:transparent; color:var(--muted);
  border-radius:12px 12px 0 0; padding:10px 18px; font-weight:700;
  text-transform: uppercase; letter-spacing:.08em; font-size:.82rem;
}
.stTabs [aria-selected="true"]{
  color:var(--brand) !important;
  background: linear-gradient(180deg, rgba(79,70,229,.10), transparent) !important;
  border-bottom: 2px solid var(--brand) !important;
}

/* Expanders */
.streamlit-expanderHeader, details > summary{
  background:#fff !important;
  border:1px solid var(--line) !important;
  border-radius:12px !important;
  font-weight:700 !important;
  text-transform: uppercase; letter-spacing:.04em;
}

/* Plot wrapper */
.element-container:has(.js-plotly-plot){
  border-radius:18px; padding:6px;
  background: var(--surface);
  border:1px solid var(--line);
  box-shadow: 0 10px 30px -22px rgba(15,23,42,.18);
}

/* LaTeX */
.stMarkdown .katex-display{
  background: #EEF2FF; border:1px solid rgba(79,70,229,.25);
  border-radius:14px; padding:14px;
}
</style>
""", unsafe_allow_html=True)

# ==================================================================
# PLOTLY TEMPLATE - LIGHT VIVID
# ==================================================================
PLOTLY_TEMPLATE = go.layout.Template(
    layout=dict(
        font=dict(family="Inter, sans-serif", color="#0F172A", size=13),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        title=dict(font=dict(family="Space Grotesk, sans-serif", size=17, color="#0F172A"),
                   x=0.02, xanchor="left"),
        xaxis=dict(gridcolor="rgba(15,23,42,.06)", zerolinecolor="rgba(15,23,42,.12)",
                   linecolor="rgba(15,23,42,.18)"),
        yaxis=dict(gridcolor="rgba(15,23,42,.06)", zerolinecolor="rgba(15,23,42,.12)",
                   linecolor="rgba(15,23,42,.18)"),
        legend=dict(bgcolor="rgba(255,255,255,.6)",
                    bordercolor="rgba(15,23,42,.08)", borderwidth=1),
        margin=dict(l=60, r=30, t=70, b=60),
        colorway=["#4F46E5","#06B6D4","#F43F5E","#10B981","#F59E0B","#8B5CF6","#0EA5E9","#84CC16"],
    )
)
pio.templates["fresh"] = PLOTLY_TEMPLATE
pio.templates.default = "fresh"

BRAND_SEQ = ["#4F46E5","#06B6D4","#F43F5E","#10B981","#F59E0B","#8B5CF6","#0EA5E9","#84CC16"]

# ==================================================================
# HELPERS
# ==================================================================
def kpi_card(value, label, sub="", kind=""):
    cls = f"kpi {kind}".strip()
    st.markdown(f"""
    <div class="{cls}">
      <div class="label">{label}</div>
      <div class="value">{value}</div>
      <div class="sub">{sub}</div>
      <div class="bar"></div>
    </div>
    """, unsafe_allow_html=True)

def hero(eyebrow, title, subtitle=""):
    st.markdown(f"""
    <div class="hero">
      <div class="eyebrow">{eyebrow}</div>
      <h1>{title}</h1>
      {f'<p>{subtitle}</p>' if subtitle else ''}
    </div>
    """, unsafe_allow_html=True)

# ==================================================================
# DATA LOADING
# ==================================================================
@st.cache_data
def load_and_preprocess_data():
    desires_df = pd.read_csv("domain_worker_desires.csv")
    caps_df    = pd.read_csv("expert_rated_technological_capability.csv")
    tasks_df   = pd.read_csv("task_statement_with_metadata.csv")
    workers_df = pd.read_csv("domain_worker_metadata.csv")

    for df in [desires_df, caps_df, tasks_df, workers_df]:
        df.columns = df.columns.str.strip()

    cs_keywords = ["Computer","Software","Database","Network","Web","Information Technology"]
    all_occs = desires_df['Occupation (O*NET-SOC Title)'].dropna().unique()
    cs_occs = [o for o in all_occs if any(k in o for k in cs_keywords)]

    task_desire = desires_df.groupby(['Task ID','Occupation (O*NET-SOC Title)','Task']).agg({
        'Automation Desire Rating':'mean',
        'Human Agency Scale Rating':'mean',
        'Interpersonal Communication Requirement':'mean',
        'Domain Expertise Requirement':'mean',
        'Involved Uncertainty':'mean'
    }).reset_index()

    task_cap = caps_df.groupby(['Task ID']).agg({'Automation Capacity Rating':'mean'}).reset_index()
    merged_tasks = pd.merge(task_desire, task_cap, on='Task ID', how='inner')
    cs_tasks = merged_tasks[merged_tasks['Occupation (O*NET-SOC Title)'].isin(cs_occs)].copy()
    cs_tasks['Gap'] = cs_tasks['Automation Desire Rating'] - cs_tasks['Automation Capacity Rating']

    raw_score = (0.4*cs_tasks['Automation Capacity Rating']
                 + 0.4*cs_tasks['Automation Desire Rating']
                 - 0.2*cs_tasks['Human Agency Scale Rating'])
    if not cs_tasks.empty and (raw_score.max()-raw_score.min()) != 0:
        cs_tasks['Agent Priority Score'] = (raw_score-raw_score.min())/(raw_score.max()-raw_score.min())*100
    else:
        cs_tasks['Agent Priority Score'] = 50.0

    def classify_agent(row):
        cap, agency = row['Automation Capacity Rating'], row['Human Agency Scale Rating']
        if cap >= 3.5 and agency <= 2.5: return "Execution Agent"
        if cap >= 3.5 and agency > 2.5:  return "Collaboration Agent"
        return "Advisory Agent"
    cs_tasks['Agent Type'] = cs_tasks.apply(classify_agent, axis=1)
    return desires_df, caps_df, tasks_df, workers_df, cs_tasks, cs_occs

desires_df, caps_df, tasks_df, workers_df, cs_tasks, cs_occs = load_and_preprocess_data()

AGENT_COLORS = {
    'Execution Agent':'#10B981',
    'Collaboration Agent':'#4F46E5',
    'Advisory Agent':'#F59E0B',
}

# ==================================================================
# SIDEBAR
# ==================================================================
st.sidebar.markdown("## AI · KHMT")
st.sidebar.markdown('<div class="small-muted">Bảng phân tích và khuyến nghị triển khai AI Agent trong ngành Khoa học Máy tính.</div>', unsafe_allow_html=True)
st.sidebar.markdown("---")
st.sidebar.markdown("### ĐIỀU HƯỚNG")
page = st.sidebar.radio(
    "Chọn nội dung phân tích:",
    ["1. TỔNG QUAN DỮ LIỆU",
     "2. MỨC ĐỘ MONG MUỐN AI",
     "3. NĂNG LỰC THỰC TẾ CỦA AI",
     "4. SO SÁNH DESIRE VS CAPABILITY",
     "5. LỘ TRÌNH ƯU TIÊN TRIỂN KHAI",
     "6. RÀO CẢN TRIỂN KHAI",
     "7. KHUYẾN NGHỊ ỨNG DỤNG"],
    label_visibility="collapsed"
)
st.sidebar.markdown("---")
st.sidebar.markdown('<div class="small-muted">Nguồn: O*NET · Expert Rating 2025</div>', unsafe_allow_html=True)

# ==================================================================
# PAGE 1
# ==================================================================
if page.startswith("1"):
    hero("OVERVIEW", "PHÂN TÍCH VÀ KHUYẾN NGHỊ ỨNG DỤNG AI AGENT",
         "Tổng quan hệ thống dữ liệu lực lượng lao động Khoa học Máy tính — dữ liệu O*NET, đánh giá chuyên gia và mong muốn người lao động.")

    total_tasks = tasks_df['Task ID'].nunique()
    total_occs  = tasks_df['Occupation (O*NET-SOC Title)'].nunique()
    total_workers = workers_df['User ID'].nunique()
    cs_tasks_count = cs_tasks['Task ID'].nunique()

    c1,c2,c3,c4 = st.columns(4)
    with c1: kpi_card(f"{total_tasks:,}", "TỔNG SỐ TÁC VỤ", "BỘ CHUẨN O*NET")
    with c2: kpi_card(f"{total_occs:,}", "TỔNG SỐ NGHỀ NGHIỆP", "PHÂN LOẠI SOC")
    with c3: kpi_card(f"{total_workers:,}", "NGƯỜI LAO ĐỘNG KHẢO SÁT", "DOMAIN WORKERS")
    with c4: kpi_card(f"{cs_tasks_count:,}", "TÁC VỤ THUỘC KHMT", "FOCUS SEGMENT", kind="good")

    st.markdown("### PHÂN BỐ TÁC VỤ THEO CÁC NGÀNH KHOA HỌC MÁY TÍNH")
    occ_counts = (cs_tasks.groupby('Occupation (O*NET-SOC Title)')['Task ID']
                  .count().reset_index().sort_values(by='Task ID', ascending=True))
    fig = px.bar(occ_counts, x='Task ID', y='Occupation (O*NET-SOC Title)', orientation='h',
                 labels={'Task ID':'SỐ LƯỢNG TÁC VỤ','Occupation (O*NET-SOC Title)':'VỊ TRÍ CÔNG VIỆC'},
                 color='Task ID', color_continuous_scale=['#A5B4FC','#4F46E5','#06B6D4'])
    fig.update_layout(height=520, margin=dict(l=260), coloraxis_showscale=False,
                      title="SỐ LƯỢNG TÁC VỤ ĐƯỢC KIỂM ĐỊNH TRÊN TỪNG VỊ TRÍ CÔNG NGHỆ")
    st.plotly_chart(fig, use_container_width=True)

# ==================================================================
# PAGE 2
# ==================================================================
elif page.startswith("2"):
    hero("DEMAND SIGNAL", "MỨC ĐỘ MONG MUỐN SỬ DỤNG AI",
         "Người lao động ngành KHMT có thực sự muốn AI hỗ trợ các tác vụ hằng ngày của họ không?")

    mean_desire = cs_tasks['Automation Desire Rating'].mean()
    median_desire = cs_tasks['Automation Desire Rating'].median()

    c1,c2 = st.columns(2)
    with c1: kpi_card(f"{mean_desire:.2f} / 5", "ĐIỂM MONG MUỐN TRUNG BÌNH", "MEAN DESIRE",
                      kind="good" if mean_desire>=3.5 else "warn")
    with c2: kpi_card(f"{median_desire:.2f} / 5", "TRUNG VỊ MONG MUỐN", "MEDIAN DESIRE")

    c3,c4 = st.columns(2)
    with c3:
        fig = px.histogram(cs_tasks, x='Automation Desire Rating', nbins=15,
                           title="PHÂN PHỐI ĐIỂM MONG MUỐN TỰ ĐỘNG HÓA",
                           labels={'Automation Desire Rating':'ĐIỂM MONG MUỐN (1-5)'},
                           color_discrete_sequence=['#4F46E5'])
        fig.update_traces(marker_line_color='#fff', marker_line_width=1)
        st.plotly_chart(fig, use_container_width=True)
    with c4:
        fig = px.box(cs_tasks, y='Automation Desire Rating', x='Occupation (O*NET-SOC Title)',
                     title="BIẾN THIÊN MONG MUỐN THEO VỊ TRÍ",
                     color='Occupation (O*NET-SOC Title)', color_discrete_sequence=BRAND_SEQ,
                     labels={'Automation Desire Rating':'ĐIỂM (1-5)','Occupation (O*NET-SOC Title)':'VỊ TRÍ'})
        fig.update_layout(showlegend=False, xaxis={'tickangle':35})
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("### NHẬN XÉT TỰ ĐỘNG VỀ NHU CẦU")
    if mean_desire >= 3.5:
        st.info(f"Mức độ khao khát ứng dụng AI trong khối KHMT ở mức **CAO** ({mean_desire:.2f}/5). Kỹ sư phần mềm chịu áp lực lớn từ tác vụ lặp lại và sẵn sàng giao phó cho hệ thống Agent thông minh, giải phóng thời gian cho công việc thiết kế kiến trúc cấp cao.")
    else:
        st.warning(f"Mức độ sẵn sàng đón nhận tự động hóa ở mức trung bình ({mean_desire:.2f}/5). Có sự phân hóa và tâm lý lo ngại về quyền kiểm soát ở một số đầu việc cốt lõi.")

# ==================================================================
# PAGE 3
# ==================================================================
elif page.startswith("3"):
    hero("SUPPLY SIGNAL", "NĂNG LỰC THỰC TẾ CỦA AI",
         "Trình độ công nghệ AI hiện nay (2025) đã mạnh đến đâu dưới góc nhìn chuyên gia?")

    mean_cap = cs_tasks['Automation Capacity Rating'].mean()
    median_cap = cs_tasks['Automation Capacity Rating'].median()

    c1,c2 = st.columns(2)
    with c1: kpi_card(f"{mean_cap:.2f} / 5", "NĂNG LỰC KỸ THUẬT TRUNG BÌNH", "MEAN CAPABILITY",
                      kind="good" if mean_cap>=3.5 else "warn")
    with c2: kpi_card(f"{median_cap:.2f} / 5", "TRUNG VỊ NĂNG LỰC AI", "MEDIAN CAPABILITY")

    c3,c4 = st.columns(2)
    with c3:
        fig = px.histogram(cs_tasks, x='Automation Capacity Rating', nbins=15,
                           title="PHÂN PHỐI NĂNG LỰC TỰ ĐỘNG HÓA",
                           labels={'Automation Capacity Rating':'NĂNG LỰC KỸ THUẬT (1-5)'},
                           color_discrete_sequence=['#06B6D4'])
        fig.update_traces(marker_line_color='#fff', marker_line_width=1)
        st.plotly_chart(fig, use_container_width=True)
    with c4:
        fig = px.box(cs_tasks, y='Automation Capacity Rating', x='Occupation (O*NET-SOC Title)',
                     title="PHÂN TÁN NĂNG LỰC THEO NGHỀ NGHIỆP",
                     color='Occupation (O*NET-SOC Title)', color_discrete_sequence=BRAND_SEQ,
                     labels={'Automation Capacity Rating':'ĐIỂM (1-5)','Occupation (O*NET-SOC Title)':'VỊ TRÍ'})
        fig.update_layout(showlegend=False, xaxis={'tickangle':35})
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("### NHẬN XÉT TỰ ĐỘNG VỀ NĂNG LỰC AI")
    if mean_cap >= 3.5:
        st.success(f"Khả năng kỹ thuật đạt mức **RẤT KHẢ THI** ({mean_cap:.2f}/5). LLM và Compound AI hiện nay đủ khả năng vận hành các tác vụ xử lý mã nguồn, cấu hình hệ thống một cách tự chủ.")
    else:
        st.info(f"Năng lực trung bình của AI đạt mức khá ({mean_cap:.2f}/5). Tốt với tác vụ văn bản và code cơ bản, nhưng còn rào cản với suy luận kiến trúc đa tầng & phối hợp công cụ phức tạp.")

# ==================================================================
# PAGE 4
# ==================================================================
elif page.startswith("4"):
    hero("GAP ANALYSIS", "SO SÁNH DESIRE VÀ CAPABILITY",
         "Chỉ số Gap = Desire − Capability giúp phát hiện điểm mất cân đối cung – cầu công nghệ.")

    mean_desire = cs_tasks['Automation Desire Rating'].mean()
    mean_cap = cs_tasks['Automation Capacity Rating'].mean()
    mean_gap = cs_tasks['Gap'].mean()

    c1,c2,c3 = st.columns(3)
    with c1: kpi_card(f"{mean_desire:.2f}", "MONG MUỐN TB (DESIRE)", "NGƯỜI LAO ĐỘNG")
    with c2: kpi_card(f"{mean_cap:.2f}", "NĂNG LỰC TB (CAPABILITY)", "CHUYÊN GIA AI")
    with c3: kpi_card(f"{mean_gap:+.2f}", "KHOẢNG CÁCH TB (GAP)",
                      "DESIRE − CAPABILITY", kind="bad" if mean_gap>0 else "good")

    occ_gap = cs_tasks.groupby('Occupation (O*NET-SOC Title)').agg({
        'Automation Desire Rating':'mean','Automation Capacity Rating':'mean'
    }).reset_index()

    fig = go.Figure()
    fig.add_trace(go.Bar(x=occ_gap['Occupation (O*NET-SOC Title)'],
                         y=occ_gap['Automation Desire Rating'],
                         name='MONG MUỐN (DESIRE)', marker_color='#4F46E5'))
    fig.add_trace(go.Bar(x=occ_gap['Occupation (O*NET-SOC Title)'],
                         y=occ_gap['Automation Capacity Rating'],
                         name='NĂNG LỰC AI (CAPABILITY)', marker_color='#06B6D4'))
    fig.update_layout(title='SO SÁNH MONG MUỐN VS NĂNG LỰC THEO TỪNG NGÀNH CS',
                      xaxis_title='VỊ TRÍ NGHỀ NGHIỆP', yaxis_title='THANG ĐIỂM (1-5)',
                      barmode='group', xaxis={'tickangle':35})
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### KẾT LUẬN ĐỐI CHIẾU CUNG - CẦU")
    if mean_gap < 0:
        st.success(f"**AI ĐANG VƯỢT KỲ VỌNG (Gap = {mean_gap:.2f}):** năng lực AI phát triển nhanh hơn mức sẵn sàng bàn giao của kỹ sư. Cần đầu tư đào tạo quy trình đón nhận AI để không lãng phí năng lực sẵn có.")
    else:
        st.warning(f"**AI CHƯA ĐÁP ỨNG ĐỦ KỲ VỌNG (Gap = {mean_gap:.2f}):** nhu cầu tự động hóa rất lớn nhưng công nghệ chưa xử lý triệt để — đây là cơ hội vàng để R&D tạo lợi thế cạnh tranh.")

# ==================================================================
# PAGE 5
# ==================================================================
elif page.startswith("5"):
    hero("PRIORITY ROADMAP", "LỘ TRÌNH ƯU TIÊN TRIỂN KHAI AI AGENT",
         "Chỉ số Agent Priority Score (APS) tổng hợp Capability, Desire và Human Agency thành một thang 0–100.")

    st.latex(r"APS = \frac{(0.4 \cdot Capability + 0.4 \cdot Desire - 0.2 \cdot HumanAgency) - Min}{Max - Min} \times 100")

    top_15 = cs_tasks.sort_values(by='Agent Priority Score', ascending=False).head(15)
    fig = px.bar(top_15, x='Agent Priority Score', y='Task', orientation='h',
                 color='Agent Type', color_discrete_map=AGENT_COLORS,
                 title='TOP 15 TÁC VỤ ƯU TIÊN ĐÓNG GÓI THÀNH AI AGENT',
                 labels={'Agent Priority Score':'ĐIỂM ƯU TIÊN (APS)','Task':'TÁC VỤ'})
    fig.update_layout(yaxis={'autorange':'reversed'}, height=650, margin=dict(l=380))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### PHÂN LOẠI CHIẾN LƯỢC")
    exec_tasks   = top_15[top_15['Agent Type']=="Execution Agent"]
    collab_tasks = top_15[top_15['Agent Type']=="Collaboration Agent"]
    adv_tasks    = top_15[top_15['Agent Type']=="Advisory Agent"]

    c1,c2,c3 = st.columns(3)
    with c1:
        st.markdown("#### TRIỂN KHAI NGAY")
        st.caption("CAPABILITY ≥ 3.5 & HUMAN AGENCY ≤ 2.5")
        if not exec_tasks.empty:
            for t in exec_tasks['Task'].head(3): st.write(f"- {t[:80]}…")
        else: st.write("—")
    with c2:
        st.markdown("#### HỖ TRỢ SONG HÀNH (COPILOT)")
        st.caption("CAPABILITY ≥ 3.5 & HUMAN AGENCY > 2.5")
        if not collab_tasks.empty:
            for t in collab_tasks['Task'].head(3): st.write(f"- {t[:80]}…")
        else: st.write("—")
    with c3:
        st.markdown("#### CHƯA NÊN ĐẦU TƯ")
        st.caption("NĂNG LỰC AI CÒN THẤP")
        if not adv_tasks.empty:
            for t in adv_tasks['Task'].head(3): st.write(f"- {t[:80]}…")
        else: st.write("—")

# ==================================================================
# PAGE 6
# ==================================================================
elif page.startswith("6"):
    hero("BARRIERS", "CÁC RÀO CẢN TRIỂN KHAI AI AGENT",
         "Xác định bản chất cốt lõi đang làm chậm tiến trình tự động hóa hệ thống phần mềm.")

    corr_cols = ['Human Agency Scale Rating','Interpersonal Communication Requirement',
                 'Domain Expertise Requirement','Involved Uncertainty']
    corr_matrix = cs_tasks[corr_cols].corr()

    c1,c2 = st.columns(2)
    with c1:
        st.markdown("#### MA TRẬN TƯƠNG QUAN CÁC RÀO CẢN")
        fig = px.imshow(corr_matrix, text_auto=".2f",
                        color_continuous_scale=['#06B6D4','#FFFFFF','#F43F5E'],
                        x=['QUYỀN CON NGƯỜI','GIAO TIẾP','CHUYÊN MÔN','BẤT ĐỊNH'],
                        y=['QUYỀN CON NGƯỜI','GIAO TIẾP','CHUYÊN MÔN','BẤT ĐỊNH'])
        fig.update_layout(coloraxis_colorbar=dict(title="TƯƠNG QUAN"))
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        st.markdown("#### TOP 15 TÁC VỤ YÊU CẦU QUYỀN CON NGƯỜI CAO NHẤT")
        top_has = cs_tasks.sort_values(by='Human Agency Scale Rating', ascending=False).head(15)
        fig = px.bar(top_has, x='Human Agency Scale Rating', y='Task', orientation='h',
                     color='Involved Uncertainty',
                     color_continuous_scale=['#A5B4FC','#F43F5E','#F59E0B'],
                     labels={'Human Agency Scale Rating':'ĐIỂM HAS'})
        fig.update_layout(yaxis={'autorange':'reversed'}, margin=dict(l=300), height=520)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("### CƠ CHẾ HUMAN-IN-THE-LOOP")
    st.markdown("""
    Rào cản lớn nhất ngăn việc triển khai AI tự trị hoàn toàn không phải là cú pháp dòng lệnh, mà là
    **yêu cầu giao tiếp liên cá nhân** và **xử lý tình huống bất định rủi ro cao**.

    **Khuyến nghị cho CTO doanh nghiệp phần mềm:**
    - Với các tác vụ có rào cản tích hợp lớn (Sprint planning, đàm phán kiến trúc với khách hàng), **bắt buộc** thiết kế theo **Human-in-the-loop**.
    - AI Agent chỉ trích xuất – xử lý dữ liệu thô, quyền phán quyết cuối cùng thuộc về kỹ sư con người.
    """)

# ==================================================================
# PAGE 7
# ==================================================================
elif page.startswith("7"):
    hero("RECOMMENDATIONS", "KHUYẾN NGHỊ ỨNG DỤNG AI AGENT THỰC CHIẾN",
         "Phân loại danh mục đầu tư công nghệ tối ưu hóa ROI cho doanh nghiệp phần mềm.")

    now_agents     = cs_tasks[cs_tasks['Agent Type']=="Execution Agent"].sort_values('Agent Priority Score', ascending=False)
    copilot_agents = cs_tasks[cs_tasks['Agent Type']=="Collaboration Agent"].sort_values('Agent Priority Score', ascending=False)
    not_agents     = cs_tasks[cs_tasks['Agent Type']=="Advisory Agent"].sort_values('Agent Priority Score', ascending=True)

    tab1,tab2,tab3 = st.tabs(["TRIỂN KHAI NGAY","COPILOT CỘNG TÁC","GIỮ NGUYÊN CON NGƯỜI"])

    with tab1:
        st.success("### DANH SÁCH AI AGENT TRIỂN KHAI NGAY")
        st.markdown("Công nghệ chín muồi, nhân sự khao khát bàn giao, không có rào cản bảo mật / tương tác lớn.")
        for _, row in now_agents.head(4).iterrows():
            with st.expander(f"{row['Occupation (O*NET-SOC Title)']} — APS {row['Agent Priority Score']:.1f}"):
                st.write(f"**TÁC VỤ:** {row['Task']}")
                st.caption(f"DESIRE `{row['Automation Desire Rating']:.2f}` · CAPABILITY `{row['Automation Capacity Rating']:.2f}` · HAS `{row['Human Agency Scale Rating']:.2f}`")
                st.info("Đóng gói Multi-Agent tự chạy, tích hợp vào CI/CD (Jenkins/GitHub Actions) hoặc Ops scripts nội bộ.")

    with tab2:
        st.info("### DANH SÁCH AI AGENT DẠNG COPILOT")
        st.markdown("AI mạnh kỹ thuật, nhưng tác vụ rủi ro hệ thống / liên phòng ban cao — cần phối hợp hai chiều.")
        for _, row in copilot_agents.head(4).iterrows():
            with st.expander(f"{row['Occupation (O*NET-SOC Title)']} — APS {row['Agent Priority Score']:.1f}"):
                st.write(f"**TÁC VỤ:** {row['Task']}")
                st.caption(f"DESIRE `{row['Automation Desire Rating']:.2f}` · CAPABILITY `{row['Automation Capacity Rating']:.2f}` · HAS `{row['Human Agency Scale Rating']:.2f}`")
                st.warning("Agent đóng vai 'đối tác phản biện kỹ thuật' — Tech Lead phê duyệt cuối cùng.")

    with tab3:
        st.warning("### TÁC VỤ CHƯA NÊN ĐẦU TƯ TỰ ĐỘNG HÓA")
        st.markdown("Tác vụ cốt lõi dựa trên thấu cảm khách hàng, tư duy đổi mới và trách nhiệm pháp lý cao.")
        for _, row in not_agents.head(4).iterrows():
            with st.expander(f"{row['Occupation (O*NET-SOC Title)']}"):
                st.write(f"**TÁC VỤ:** {row['Task']}")
                st.caption(f"DOMAIN EXPERTISE `{row['Domain Expertise Requirement']:.2f}` · INTERPERSONAL `{row['Interpersonal Communication Requirement']:.2f}`")
                st.error("AI chưa xử lý được tư duy phi tuyến / thấu cảm phức tạp — tự động hóa vùng này rủi ro cao.")
