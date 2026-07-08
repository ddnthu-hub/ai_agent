import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

# ==========================================
# 1. CẤU HÌNH GIAO DIỆN & STYLE CHUẨN BI/DSS WIDE VỚI TYPOGRAPHY ĐỒNG BỘ
# ==========================================
st.set_page_config(page_title="Hệ thống hỗ trợ ra quyết định AI Agent", layout="wide", page_icon="🤖")

st.markdown("""
    <style>
    /* Đồng bộ khoảng cách và khổ rộng màn hình */
    .main .block-container { padding-top: 1.5rem; max-width: 96%; }
    
    /* Đồng bộ Typography cho tất cả các Heading cùng cấp */
    h1 { color: #1E88E5; font-size: 2.5rem !important; font-weight: 800; padding-bottom: 0.5rem; }
    h2 { color: #0D47A1; font-size: 1.8rem !important; margin-top: 1.8rem; margin-bottom: 0.8rem; font-weight: 700; }
    h3 { color: #1976D2; font-size: 1.3rem !important; margin-top: 1.2rem; margin-bottom: 0.6rem; font-weight: 600; }
    
    /* Tăng font chữ mô tả (body text) thêm 1-2px và đồng bộ khoảng cách */
    .stMarkdown p, .stMarkdown li, p, li { font-size: 1.1rem !important; line-height: 1.6 !important; color: #333; }
    
    /* Tăng font chữ và định dạng bảng hiển thị (table text) thêm 1-2px */
    table { width: 100% !important; margin-top: 0.5rem !important; margin-bottom: 1rem !important; }
    table th { font-size: 1.15rem !important; font-weight: bold !important; background-color: #f1f3f4 !important; padding: 10px !important; }
    table td { font-size: 1.1rem !important; padding: 10px !important; }
    
    /* Đồng bộ cấu trúc Metric và Expander */
    .stMetric label { font-size: 1.1rem !important; font-weight: bold; color: #555; }
    .stMetric value { font-size: 2.2rem !important; color: #1E88E5; font-weight: bold; }
    div[data-testid="stExpander"] { border: 1px solid #E0E0E0; border-radius: 8px; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)


# ==========================================
# 2. MODULE TIỀN XỬ LÝ & ÁNH XẠ CHỨC NĂNG (MAPPING ENGINE)
# ==========================================
@st.cache_data
def tai_va_tien_xu_ly_workbank():
    Tep_Du_Lieu = [
        "domain_worker_desires.csv",
        "expert_rated_technological_capability.csv",
        "task_statement_with_metadata.csv",
        "domain_worker_metadata.csv"
    ]
    for file in Tep_Du_Lieu:
        if not os.path.exists(file):
            st.error(f"❌ Không tìm thấy tệp dữ liệu `{file}` trong thư mục hiện hành. Vui lòng đặt đúng 4 file WORKBank gốc cạnh file mã nguồn.")
            st.stop()
            
    df_desire = pd.read_csv("domain_worker_desires.csv")
    df_cap = pd.read_csv("expert_rated_technological_capability.csv")
    df_task = pd.read_csv("task_statement_with_metadata.csv")
    df_meta_worker = pd.read_csv("domain_worker_metadata.csv")
    
    cac_cols_cap = ['Automation Capacity Rating', 'Physical Action Requirement', 'Involved Uncertainty', 
                  'Domain Expertise Requirement', 'Interpersonal Communication Requirement', 'Human Agency Scale Rating']
    cap_agg = df_cap.groupby("Task ID")[cac_cols_cap].mean().reset_index()
    desire_agg = df_desire.groupby("Task ID")["Automation Desire Rating"].mean().reset_index()
    
    df_merged = df_task.merge(cap_agg, on="Task ID", how="inner")
    df_merged = df_merged.merge(desire_agg, on="Task ID", how="inner")
    df_merged['Occupation'] = df_merged['Occupation (O*NET-SOC Title)']
    
    tu_khoa_it = ['Computer', 'Software', 'Information', 'Network', 'Data', 'Systems', 'Programmer', 'Developer', 'Web', 'Database']
    bo_loc = df_merged['Occupation'].str.contains('|'.join(tu_khoa_it), case=False, na=False)
    df_it = df_merged[bo_loc].copy()
    
    if df_it.empty:
        df_it = df_merged.copy()
        
    khao_sat_worker = df_meta_worker['User ID'].nunique()
    khao_sat_expert = df_cap['User ID'].nunique()
    
    return df_it, khao_sat_worker, khao_sat_expert


def anh_xa_tac_vu_sang_agent(task_desc):
    """Quy tắc ánh xạ phi ngẫu nhiên (Functional Mapping Rule) dựa trên mô tả tác vụ thực tế"""
    desc = str(task_desc).lower()
    if any(k in desc for k in ['test', 'quality', 'qa', 'validate', 'inspect', 'verify']): return 'Testing Agent'
    if any(k in desc for k in ['review', 'code', 'debug', 'program', 'develop', 'write code', 'compile']): return 'Code Review Copilot'
    if any(k in desc for k in ['document', 'write', 'manual', 'guide', 'report', 'record', 'specification']): return 'Documentation Agent'
    if any(k in desc for k in ['monitor', 'system', 'performance', 'log', 'analyze', 'tracking']): return 'Monitoring Agent'
    if any(k in desc for k in ['deploy', 'pipeline', 'infrastructure', 'install', 'configure', 'cloud', 'cicd']): return 'DevOps Agent'
    if any(k in desc for k in ['security', 'protect', 'vulnerability', 'encrypt', 'firewall', 'threat', 'audit']): return 'Security Agent'
    if any(k in desc for k in ['database', 'sql', 'data', 'schema', 'storage', 'query', 'migration']): return 'Database Agent'
    if any(k in desc for k in ['backup', 'restore', 'archive', 'recovery', 'disaster']): return 'Backup Agent'
    if any(k in desc for k in ['plan', 'schedule', 'roadmap', 'timeline', 'project', 'budget']): return 'Planning Agent'
    return 'Analytics Agent'


if 'df_dss_core' not in st.session_state:
    df_raw, w_survey, e_survey = tai_va_tien_xu_ly_workbank()
    st.session_state.df_dss_core = df_raw
    st.session_state.w_survey = w_survey
    st.session_state.e_survey = e_survey
    st.session_state.df_dss_core['AI_Agent_Category'] = st.session_state.df_dss_core['Task'].apply(anh_xa_tac_vu_sang_agent)

df = st.session_state.df_dss_core


# ==========================================
# 3. ENGINE TOÁN HỌC ĐỘNG (WEIGHTED SCORING DSS ENGINE)
# ==========================================
def bo_sinh_ma_tran_trong_so(goal, strategy, size, budget):
    """Bộ sinh ma trận trọng số động tối ưu dựa trên hồ sơ tổ chức"""
    w = {
        'Automation Capability': 0.20, 'Automation Desire': 0.15, 'Human Agency': 0.15,
        'Communication Requirement': 0.15, 'Domain Expertise Requirement': 0.15, 'Involved Uncertainty': 0.20
    }
    
    if "Reduce Cost" in goal or "chi phí" in goal:
        w['Automation Capability'] += 0.15
        w['Automation Desire'] += 0.05
        w['Involved Uncertainty'] -= 0.05
    elif "Increase Productivity" in goal or "năng suất" in goal:
        w['Automation Capability'] += 0.05
        w['Automation Desire'] += 0.15
    elif "Improve Quality" in goal or "chất lượng" in goal:
        w['Involved Uncertainty'] += 0.10
        w['Domain Expertise Requirement'] += 0.05
    elif "Enhance Security" in goal or "an ninh" in goal:
        w['Human Agency'] += 0.10
        w['Involved Uncertainty'] += 0.05
        w['Communication Requirement'] += 0.05
        w['Automation Desire'] -= 0.05

    if "Aggressive" in strategy or "Bứt phá" in strategy:
        w['Automation Capability'] += 0.15
        w['Human Agency'] -= 0.10
        if w['Human Agency'] < 0.02: w['Human Agency'] = 0.02
    elif "Conservative" in strategy or "Phòng vệ" in strategy:
        w['Automation Capability'] -= 0.10
        w['Human Agency'] += 0.15
        if w['Automation Capability'] < 0.02: w['Automation Capability'] = 0.02

    tong_w = sum(abs(v) for v in w.values())
    for k in w:
        w[k] = round(abs(w[k]) / tong_w, 2)
        
    bonus = 0.0
    penalty = 0.0
    if budget <= 35:
        penalty += (45 - budget) * 0.40
        
    return w, bonus, penalty


def engine_tinh_diem_quyet_dinh(row, w_matrix, bonus, penalty):
    """Tính điểm ra quyết định chuẩn hóa dựa trên ma trận trọng số"""
    cap = (row['Automation Capacity Rating'] / 5.0) * 10
    des = (row['Automation Desire Rating'] / 5.0) * 10
    ha = (row['Human Agency Scale Rating'] / 5.0) * 10
    comm = (row['Interpersonal Communication Requirement'] / 5.0) * 10
    dex = (row['Domain Expertise Requirement'] / 5.0) * 10
    unc = (row['Involved Uncertainty'] / 5.0) * 10
    
    tich_chap = (cap * w_matrix['Automation Capability']) + (des * w_matrix['Automation Desire']) \
                - (ha * w_matrix['Human Agency']) - (comm * w_matrix['Communication Requirement']) \
                - (dex * w_matrix['Domain Expertise Requirement']) - (unc * w_matrix['Involved Uncertainty'])
                
    score_co_so = ((tich_chap + 10) * 5.0) + bonus - penalty
    return round(max(0, min(100, score_co_so)), 1)


def tinh_he_so_confidence_factor(so_task):
    """Hàm quy đổi hệ số tin cậy dựa trên số lượng tác vụ"""
    if so_task >= 30:   return 1.00, "100%"
    elif so_task >= 20: return 0.98, "98%"
    elif so_task >= 10: return 0.96, "96%"
    elif so_task >= 5:  return 0.94, "94%"
    else:               return 0.92, "92%"


def pipeline_tinh_roi_engine(row, budget_val, size_val):
    """Tính toán tỷ suất sinh lời dựa trên Final Decision Score"""
    diem_goc = row['Final_Decision_Score'] * 0.95
    if budget_val > 70: diem_goc += 3.0
    if "Startup" in size_val or "nhỏ" in size_val: diem_goc += 2.0
    return round(max(0, min(100, diem_goc)), 1)


def phan_lop_mo_hinh_trien_khai(score):
    if score >= 86: return "Fully Autonomous", "Tự động hóa độc lập toàn phần"
    elif score >= 71: return "Execution Agent", "Triển khai chạy tự động độc lập"
    elif score >= 51: return "AI Copilot", "Triển khai trợ lý đồng hành"
    elif score >= 31: return "Human-in-the-loop", "Triển khai có con người giám sát"
    else: return "Human Only", "Giữ nguyên cấu trúc nhân sự xử lý"


def quy_doi_nhan_khuyen_nghi_dau_tu(score, roi):
    if score >= 70 and roi >= 70:   return "Đầu tư ngay"
    elif score >= 60 and roi >= 60: return "Ưu tiên đầu tư"
    elif score >= 50:               return "Triển khai Pilot"
    elif score >= 40:               return "Cân nhắc sau"
    else:                           return "Chưa nên đầu tư"


# ==========================================
# 4. GIAO DIỆN THANH SIDEBAR NHẬN INPUT CẤU HÌNH ĐÃ ĐỒNG BỘ TIẾNG VIỆT
# ==========================================
st.sidebar.markdown("## 🧭 ĐIỀU HƯỚNG CẤU TRÚC DSS")
page = st.sidebar.radio("Lựa chọn Module chức năng DSS:", [
    "Trang 1 — Tổng quan dữ liệu tác vụ",
    "Trang 2 — Cấu hình hệ thống ra quyết định",
    "Trang 3 — Mô hình ra quyết định AI",
    "Trang 4 — Xếp hạng danh mục AI Agent",
    "Trang 5 — Chiến lược đầu tư cuối cùng"
])

st.sidebar.markdown("---")
st.sidebar.markdown("### 🏢 THIẾT LẬP HỒ SƠ DOANH NGHIỆP")

profile_mode = st.sidebar.selectbox("Phương thức cấu hình:", ["Chọn cấu hình doanh nghiệp có sẵn", "Tự nhập tiêu chí tùy chỉnh"])

if profile_mode == "Chọn cấu hình doanh nghiệp có sẵn":
    preset = st.sidebar.selectbox("Loại hình doanh nghiệp hoạt động:", ["Startup Công nghệ", "SME (Doanh nghiệp vừa & nhỏ)", "Enterprise (Tập đoàn lớn)"])
    if preset == "Startup Công nghệ":
        sb_goal = "Tăng cường năng suất (Increase Productivity)"
        sb_size = "Quy mô nhỏ (Startup)"
        sb_budget = 30
        sb_strategy = "Bứt phá (Aggressive)"
    elif preset == "SME (Doanh nghiệp vừa & nhỏ)":
        sb_goal = "Tối ưu chi phí (Reduce Cost)"
        sb_size = "Quy mô vừa (SME)"
        sb_budget = 50
        sb_strategy = "Cân bằng (Balanced)"
    elif preset == "Enterprise (Tập đoàn lớn)":
        sb_goal = "Nâng cao chất lượng (Improve Quality)"
        sb_size = "Quy mô lớn (Enterprise)"
        sb_budget = 80
        sb_strategy = "Cân bằng (Balanced)"
else:
    sb_goal = st.sidebar.selectbox("1. Mục tiêu chiến lược cốt lõi (Business Goal):", ["Tối ưu chi phí (Reduce Cost)", "Tăng cường năng suất (Increase Productivity)", "Nâng cao chất lượng (Improve Quality)", "Đảm bảo an ninh (Enhance Security)"])
    sb_strategy = st.sidebar.selectbox("2. Chiến lược triển khai AI (AI Adoption Strategy):", ["Phòng vệ (Conservative)", "Cân bằng (Balanced)", "Bứt phá (Aggressive)"], index=1)
    sb_size = st.sidebar.selectbox("3. Quy mô tổ chức (Company Size):", ["Quy mô nhỏ (Startup)", "Quy mô vừa (SME)", "Quy mô lớn (Enterprise)"])
    sb_budget = st.sidebar.slider("4. Biên độ ngân sách khả dụng (Budget Scale):", 0, 100, 50)

st.sidebar.caption("💡 Ý nghĩa: Thiết lập hồ sơ đầu vào đồng bộ hóa tham số.")

if "Reduce Cost" in sb_goal or "chi phí" in sb_goal: st.sidebar.caption("💡 Ý nghĩa: Tối ưu hóa chi phí vận hành bằng tự động hóa tác vụ rập khuôn.")
elif "Increase Productivity" in sb_goal or "năng suất" in sb_goal: st.sidebar.caption("💡 Ý nghĩa: Tăng tốc quy trình làm việc, AI trợ lý đồng hành giải phóng hiệu suất lao động.")
elif "Improve Quality" in sb_goal or "chất lượng" in sb_goal: st.sidebar.caption("💡 Ý nghĩa: Nâng cao độ chính xác, tối thiểu lỗi sai hệ thống.")
elif "Enhance Security" in sb_goal or "an ninh" in sb_goal: st.sidebar.caption("💡 Ý nghĩa: Kiểm soát rủi ro bảo mật dữ liệu lõi, ưu tiên con người phê duyệt.")

if "Conservative" in sb_strategy or "Phòng vệ" in sb_strategy: st.sidebar.caption("🛡️ Triết lý: Ưu tiên con người, kiểm soát rủi ro biên phòng vệ.")
elif "Balanced" in sb_strategy or "Cân bằng" in sb_strategy: st.sidebar.caption("⚖️ Triết lý: Cân bằng hài hòa hiệu quả kinh tế và rủi ro kỹ thuật.")
elif "Aggressive" in sb_strategy or "Bứt phá" in sb_strategy: st.sidebar.caption("⚡ Triết lý: Tối đa hóa tỷ lệ tích hợp tự động hóa toàn phần.")

# Khởi chạy nạp và phân bổ biến động điểm số toàn cục
w_matrix, dynamic_bonus, dynamic_penalty = bo_sinh_ma_tran_trong_so(sb_goal, sb_strategy, sb_size, sb_budget)
df['Decision_Score'] = df.apply(lambda r: engine_tinh_diem_quyet_dinh(r, w_matrix, dynamic_bonus, dynamic_penalty), axis=1)

# Tính toán biến động Confidence Factor theo nhóm AI Agent
agent_task_counts = df['AI_Agent_Category'].value_counts().to_dict()

def pipeline_tinh_final_score(row):
    so_task = agent_task_counts.get(row['AI_Agent_Category'], 0)
    factor, _ = tinh_he_so_confidence_factor(so_task)
    return round(row['Decision_Score'] * factor, 1)

# Đồng bộ toán học lõi: Toàn bộ hệ thống kế thừa Final_Decision_Score
df['Final_Decision_Score'] = df.apply(pipeline_tinh_final_score, axis=1)
df['ROI_Score'] = df.apply(lambda r: pipeline_tinh_roi_engine(r, sb_budget, sb_size), axis=1)


# ==========================================
# 5. KHỐI CÁC HÀM RENDER CHI TIẾT TỪNG TRANG
# ==========================================

def render_page_1():
    st.markdown("<h1>📊 TRANG 1 — TỔNG QUAN DỮ LIỆU ĐẦU VÀO CỦA HỆ THỐNG</h1>", unsafe_allow_html=True)
    st.markdown("### Giới thiệu nguồn dữ liệu tri thức cơ sở khoa học WORKBank và quy trình chuyển dịch ánh xạ.")
    st.markdown("---")
    
    tong_task = len(df)
    tong_agent = df['AI_Agent_Category'].nunique()
    
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Tổng số Tác vụ (Tasks)", f"{tong_task:,}")
    col2.metric("Tổng số Ngành nghề", f"{df['Occupation'].nunique():,}")
    col3.metric("Khảo sát người lao động", f"{st.session_state.w_survey:,}")
    col4.metric("Đánh giá từ Chuyên gia", f"{st.session_state.e_survey:,}")
    col5.metric("Tổng số AI Agents ánh xạ", f"{tong_agent:,}")
    
    st.markdown("---")
    st.markdown("#### Tỷ lệ phân bổ Tác vụ theo phân loại dòng AI Agent chức năng")
    
    agent_counts = df['AI_Agent_Category'].value_counts().reset_index()
    agent_counts.columns = ['AI Agent', 'Số lượng Task']
    agent_counts['Ty le %'] = (agent_counts['Số lượng Task'] / tong_task * 100).round(1)
    agent_counts['Legend_Text'] = agent_counts.apply(lambda r: f"{r['AI Agent']} - {r['Số lượng Task']} Tác vụ ({r['Ty le %']:.1f}%)", axis=1)
    
    fig_pie = px.pie(agent_counts, values='Số lượng Task', names='Legend_Text', hole=0.4, color_discrete_sequence=px.colors.sequential.Blugrn)
    fig_pie.update_traces(hovertemplate="<b>%{label}</b><br>Số lượng Task thực tế: %{value}<br>Tỷ lệ phân bổ: %{percent}", textinfo='percent')
    fig_pie.update_layout(height=420, margin=dict(l=0, r=0, t=10, b=10), legend=dict(title_text="Dòng AI Agent & Quy mô"))
    st.plotly_chart(fig_pie, use_container_width=True)
    
    st.markdown(f"""
    <p style='font-size: 0.95rem; line-height: 1.5; color: #444; font-style: italic; padding-top: 5px; text-align: center;'>
        Tổng cộng có <b>{tong_task} Tác vụ</b> từ bộ dữ liệu WORKBank đã được ánh xạ (mapping) vào <b>{tong_agent} nhóm AI Agent</b> chức năng. 
        Biểu đồ thể hiện số lượng và tỷ lệ phân bổ Tác vụ của từng AI Agent.
    </p>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### GIỚI THIỆU 6 TIÊU CHÍ ĐẶC TRƯNG TÁC VỤ (6 TASK FEATURES)")
    comp_df = pd.DataFrame({
        "Tiêu chí đặc trưng tác vụ (Task Features)": ["Automation Capability", "Automation Desire", "Human Agency", "Communication Requirement", "Domain Expertise Requirement", "Involved Uncertainty"],
        "Nguồn dữ liệu thực nghiệm khoa học": ["WORKBank Expert Rating", "WORKBank Worker Survey", "WORKBank Metadata", "WORKBank Metadata", "WORKBank Metadata", "WORKBank Metadata"],
        "Ý nghĩa giải trình bản chất kỹ thuật": [
            "Năng lực tự động hóa: Đo lường mức độ chín muồi và sẵn sàng của giải pháp công nghệ hiện tại đối với tác vụ.",
            "Mong muốn tự động hóa: Nguyện vọng chuyển giao đầu việc và mức độ cởi mở cộng tác từ phía người lao động.",
            "Mức độ can thiệp của con người: Yêu cầu bắt buộc về tính phê duyệt, rà soát và trách nhiệm giải trình của nhân sự.",
            "Yêu cầu năng lực giao tiếp: Tầm quan trọng của khâu trao đổi thông tin, tương tác thấu cảm giữa người với người.",
            "Yêu cầu kỹ năng chuyên môn: Biên độ đòi hỏi khối lượng kiến thức chuyên sâu để xử lý tốt công việc.",
            "Mức độ bất định của quy trình: Tần suất phát sinh biến động, rủi ro hệ thống và các tình huống ngoại lệ phát sinh."
        ]
    })
    st.table(comp_df)


def render_page_2():
    st.markdown("<h1>⚙️ TRANG 2 — CẤU HÌNH HỆ THỐNG RA QUYẾT ĐỊNH</h1>", unsafe_allow_html=True)
    st.markdown("### (Decision Configuration)")
    st.markdown("---")
    
    st.markdown("### 📊 3.1 Hồ sơ yêu cầu doanh nghiệp (Business Requirements)")
    col_req = st.columns([1, 1.4])
    with col_req[0]:
        st.table(pd.DataFrame({
            "Tiêu chí": ["Business Goal", "AI Strategy", "Company Size", "Budget"],
            "Giá trị thiết lập": [sb_goal, sb_strategy, sb_size, f"{sb_budget}/100"]
        }))
    with col_req[1]:
        st.markdown("""
        <div style="background-color: #f8f9fa; padding: 18px; border-radius: 6px; border-left: 5px solid #1E88E5; height: 100%;">
            <p style="font-size: 0.95rem; line-height: 1.5; color: #333; margin-bottom: 0;">
                <b>Business Requirements</b> là tập hợp các điều kiện đầu vào do doanh nghiệp cung cấp. 
                Các thông tin này không trực tiếp quyết định AI Agent nào được chọn, mà tham gia vào bộ điều phối ma trận để hệ thống Decision Engine tính toán và kết xuất kết quả có tính tương hợp tổ chức cao nhất.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("---")
    st.markdown("### ⚖️ 3.2 Bảng quy đổi Hệ số tin cậy thống kê (Confidence Factor Model)")
    
    conf_table_df = pd.DataFrame({
        "Quy mô dữ liệu của AI Agent": ["≥ 30 Tasks", "20–29 Tasks", "10–19 Tasks", "5–9 Tasks", "< 5 Tasks"],
        "Confidence Factor": ["1.00", "0.98", "0.96", "0.94", "0.92"],
        "Hiển thị": ["100%", "98%", "96%", "94%", "92%"]
    })
    st.table(conf_table_df)
    st.markdown("<p style='font-style: italic; margin-top: -0.3rem;'>Confidence phản ánh độ ổn định thống kê của mẫu dữ liệu WORKBank dùng để đánh giá AI Agent, không phản ánh chất lượng kỹ thuật của AI Agent.</p>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("## 🎯 3.3 Mục tiêu kinh doanh (Business Goal)")
    st.write(f"Ma trận trọng số được thiết lập và tự động chuyển dịch trọng tâm dựa trên mục tiêu hiện tại: *{sb_goal}*")
    
    st.markdown("---")
    st.markdown("## 📈 3.4 Chiến lược triển khai AI (AI Adoption Strategy)")
    st.write(f"Chiến lược *{sb_strategy}* trực tiếp can thiệp làm thay đổi trực diện Weight của các Task Features ở mục 3.6 phía dưới.")
        
    # 🌟 CHỈNH SỬA THEO YÊU CẦU: Bổ sung 2 dòng quan trọng nhất Business Goal và AI Adoption Strategy lên đầu bảng 3.5
    st.markdown("---")
    st.markdown("## 🧩 3.5 Thành phần tính Decision Score (Decision Score Components)")
    components_df = pd.DataFrame({
        "Thành phần (Component)": [
            "Business Goal", 
            "AI Adoption Strategy", 
            "Automation Capability", 
            "Automation Desire", 
            "Human Agency", 
            "Communication Requirement", 
            "Domain Expertise Requirement", 
            "Involved Uncertainty", 
            "Company Size", 
            "Budget"
        ],
        "Nguồn dữ liệu (Source)": [
            "Hồ sơ Doanh nghiệp", 
            "Hồ sơ Doanh nghiệp", 
            "WORKBank Expert Rating", 
            "WORKBank Worker Survey", 
            "WORKBank Metadata", 
            "WORKBank Metadata", 
            "WORKBank Metadata", 
            "WORKBank Metadata", 
            "Hồ sơ Doanh nghiệp", 
            "Hồ sơ Doanh nghiệp"
        ],
        "Vai trò định lượng nghiệp vụ": [
            "Xác định mục tiêu tối ưu của doanh nghiệp (Chi phí, Năng suất, Chất lượng...) để sinh Dynamic Weight cho các đặc trưng Task.",
            "Điều chỉnh mức ưu tiên giữa tự động hóa và kiểm soát của con người, từ đó làm thay đổi trọng số (Weight) của các Task Features trong Decision Engine.",
            "Năng lực công nghệ sẵn có bóc tách từ mô hình thực nghiệm danh tiếng WORKBank.", 
            "Nguyện vọng chuyển giao đầu việc và mức độ sẵn sàng cộng tác từ người lao động.", 
            "Yêu cầu rào cản bắt buộc về tính phê duyệt, kiểm soát tối cao từ phía con người.", 
            "Mức độ thâm dụng tương tác giao tiếp giữa người với người trong quy trình nghiệp vụ.", 
            "Yêu cầu trình độ khối lượng kiến thức nghiệp vụ và kỹ năng chuyên môn sâu.", 
            "Biên độ bất định, biến động và nguy cơ phát sinh ngoại lệ ngoài quy trình chuẩn.",
            "Quy mô doanh nghiệp: Cung cấp tham số phản ánh khả năng hấp thụ và mở rộng giải pháp.",
            "Ngân sách tổ chức: Thiết lập ngưỡng giới hạn chi phí đầu tư và biên độ hoàn vốn kỳ vọng."
        ]
    })
    st.table(components_df)
    
    st.markdown("---")
    st.markdown("## 🎛️ 3.6 Ma trận trọng số động đã tối ưu thích ứng (Weight Model)")
    col_w = st.columns([1, 1.4])
    with col_w[0]:
        st.table(pd.DataFrame({"Task Feature Component": list(w_matrix.keys()), "Weight": [f"{v*100:.0f}%" for v in w_matrix.values()]}))
    with col_w[1]:
        st.markdown(f"Các trọng số không cố định. Decision Engine tự động phân bổ lại theo Business Goal kết hợp với AI Strategy mà doanh nghiệp lựa chọn nhằm loại bỏ tính ảnh hưởng trùng lặp.")

    st.markdown("---")
    st.markdown("## 🧠 3.7 Bộ máy xử lý toán học tích chập (Decision Engine)")
    st.markdown("""
    ```
    Business Goal  ➔  AI Strategy  ➔  Company Size  ➔  Budget
                               │
                               ▼
                        Weight Generator
                               │
                               ▼
                        Decision Score = Σ(Task Feature × Dynamic Weight) + Reward − Penalty
                               │
                               ▼
                        Final Decision Score = Decision Score × Confidence Factor
    ```
    """, unsafe_allow_html=True)
    
    st.latex(r"Decision\ Score = \sum_{i=1}^{n} (Task\ Feature_i \times Dynamic\ Weight_i) + Reward - Penalty")
    st.latex(r"Final\ Decision\ Score = Decision\ Score \times Confidence\ Factor")
    
    st.markdown("""
    * **Dynamic Weight:** Được tự động tính toán sinh ra từ cấu hình biên doanh nghiệp cung cấp nhằm đồng bộ hóa chiến lược.
    * **Reward và Penalty:** Giữ nguyên các giá trị điều chỉnh điểm thưởng hoặc điểm phạt phòng vệ rủi ro theo đúng cấu trúc logic mã nguồn hiện hành.
    * **Confidence Factor:** Đóng vai trò là hệ số hiệu chỉnh thống kê toán học nhằm giảm thiểu tối đa tình trạng thiên lệch (bias) do sự chênh lệch quy mô số lượng mẫu Tác vụ giữa các dòng AI Agent chức năng khác nhau gây ra.
    * **Cơ chế tác động:** Hệ số hiệu chỉnh này không làm xáo trộn hay thay đổi thứ tự ưu tiên vốn có nếu hai dòng AI Agent có năng lực tương thích kỹ thuật tương đương, mục tiêu duy nhất là giảm bớt lợi thế sai lệch của những nhóm giải pháp có số lượng tác vụ quá ít dữ liệu chứng minh.
    """)
    
    st.markdown("---")
    st.markdown("## 💰 3.8 Khung ước lượng hiệu quả kinh tế (ROI Estimation)")
    st.latex(r"Estimated\ ROI = Final\ Decision\ Score \times 0.95 + Budget\ Modifier + Size\ Modifier")

    st.markdown("---")
    st.markdown("## 📐 3.9 Ý nghĩa chỉ số Decision Score Final Interpretation")
    st.table(pd.DataFrame({
        "Miền điểm quyết định": ["0 – 35 điểm", "35 – 55 điểm", "55 – 75 điểm", "75 – 100 điểm"],
        "Recommendation": ["Human Only", "Human-in-the-loop", "AI Copilot", "Execution Agent"],
        "Ý nghĩa vận hành": ["Chưa phù hợp triển khai AI", "AI hỗ trợ, con người quyết định cuối cùng", "AI đồng hành cùng nhân viên", "AI tự động thực hiện quy trình"]
    }))

    st.markdown("---")
    st.markdown("## 🕸️ 3.10 Trực quan hóa ma trận trọng số (Radar Weight)")
    f_radar = go.Figure(go.Scatterpolar(r=list(w_matrix.values()) + [list(w_matrix.values())[0]], theta=list(w_matrix.keys()) + [list(w_matrix.keys())[0]], fill='toself', line_color='#1E88E5'))
    f_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, max(w_matrix.values()) + 0.1])), height=260, margin=dict(l=30, r=30, t=10, b=10))
    st.plotly_chart(f_radar, use_container_width=True)

    st.markdown("---")
    st.markdown("## 🔄 3.11 Quy trình ra quyết định của DSS (Decision Flow)")
    st.markdown("```\nWORKBank Dataset ➔ Task Features ➔ AI Agent Mapping ➔ Business Requirements ➔ Weight Generator ➔ Decision Engine ➔ Decision Score ➔ Estimated ROI ➔ AI Agent Ranking ➔ Final Recommendation\n```")


def render_page_3():
    st.markdown("<h1>🧠 TRANG 3 — MÔ HÌNH RA QUYẾT ĐỊNH AI (AI DECISION ENGINE)</h1>", unsafe_allow_html=True)
    st.markdown("### Phân tích đặc trưng tác vụ chi tiết và minh họa chuỗi suy luận định lượng.")
    st.markdown("---")
    
    danh_sach_agent = sorted(df['AI_Agent_Category'].unique())
    sel_agent = st.selectbox("1. Lựa chọn dòng AI Agent chức năng chuyên biệt cần khảo sát:", danh_sach_agent)
    
    tasks_theo_agent = df[df['AI_Agent_Category'] == sel_agent]['Task'].unique()
    sel_task = st.selectbox("2. Lựa chọn tác vụ nghiệp vụ chi tiết thuộc Agent (Task):", tasks_theo_agent)
    
    task_data = df[(df['AI_Agent_Category'] == sel_agent) & (df['Task'] == sel_task)].iloc[0]
    
    score_final = task_data['Final_Decision_Score']
    roi_score = task_data['ROI_Score'] 
    
    so_task_cuc_bo = agent_task_counts.get(sel_agent, 0)
    _, phan_tram_conf = tinh_he_so_confidence_factor(so_task_cuc_bo)
    
    _, seg_vi = phan_lop_mo_hinh_trien_khai(score_final)
    st.markdown(f"**Định hướng phân lớp kỹ thuật:** Điểm Final đạt `{score_final}/100` $\rightarrow$ Mô hình: **{seg_vi}**")
    
    st.markdown("<br>", unsafe_allow_html=True)
    col_metrics = st.columns(3)
    with col_metrics[0]:
        st.metric("Final Decision Score", f"{score_final} / 100")
    with col_metrics[1]:
        st.metric("Estimated ROI", f"{roi_score} %")
    with col_metrics[2]:
        st.metric(
            "Độ tin cậy (Confidence %)", 
            f"{phan_tram_conf}", 
            help="Confidence phản ánh độ ổn định của kết quả do số lượng Task được sử dụng để đánh giá AI Agent."
        )
        
    st.caption("Lưu ý: Chỉ số ROI và điểm số tại trang này chỉ đóng vai trò minh họa quá trình suy luận từ cấp độ Task Feature. Quyết định đầu tư phê duyệt danh mục sẽ được tập trung trình bày tại Trang 4 và Trang 5.")
    st.markdown("---")
    
    c1, c2 = st.columns([1.8, 1.2])
    with c1:
        st.markdown("#### Phân tích đặc trưng đa chiều tác vụ")
        categories = ['Automation Capability', 'Automation Desire', 'Human Agency', 'Communication Requirement', 'Domain Expertise Requirement', 'Involved Uncertainty']
        values = [task_data['Automation Capacity Rating'], task_data['Automation Desire Rating'], task_data['Human Agency Scale Rating'], task_data['Interpersonal Communication Requirement'], task_data['Domain Expertise Requirement'], task_data['Involved Uncertainty']]
        fig = go.Figure(data=go.Scatterpolar(r=values, theta=categories, fill='toself', marker_color='#1976D2'))
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 5])), height=400, margin=dict(l=30, r=30, t=10, b=10))
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        st.markdown("#### Khung phản ánh Decision Score")
        fig_gauge = go.Figure(go.Indicator(mode = "gauge+number", value = score_final, domain = {'x': [0, 1], 'y': [0, 1]}, gauge = {'axis': {'range': [None, 100]}, 'bar': {'color': "#1E88E5"}}))
        fig_gauge.update_layout(height=350)
        st.plotly_chart(fig_gauge, use_container_width=True)
        
    st.markdown("### Ma trận đóng góp chi tiết cấu thành điểm số")
    cap_c = (task_data['Automation Capacity Rating'] / 5.0) * 10 * w_matrix['Automation Capability'] * 5.0
    des_c = (task_data['Automation Desire Rating'] / 5.0) * 10 * w_matrix['Automation Desire'] * 5.0
    ha_c = -1.0 * (task_data['Human Agency Scale Rating'] / 5.0) * 10 * w_matrix['Human Agency'] * 5.0
    comm_c = -1.0 * (task_data['Interpersonal Communication Requirement'] / 5.0) * 10 * w_matrix['Communication Requirement'] * 5.0
    dex_c = -1.0 * (task_data['Domain Expertise Requirement'] / 5.0) * 10 * w_matrix['Domain Expertise Requirement'] * 5.0
    unc_c = -1.0 * (task_data['Involved Uncertainty'] / 5.0) * 10 * w_matrix['Involved Uncertainty'] * 5.0
    
    contrib_df = pd.DataFrame({
        'Tiêu chí đặc trưng tác vụ': ['Automation Capability (+)', 'Automation Desire (+)', 'Human Agency (-)', 'Communication (-)', 'Domain Expertise (-)', 'Involved Uncertainty (-)'],
        'Điểm số đóng góp thực tế': [round(cap_c, 1), round(des_c, 1), round(ha_c, 1), round(comm_c, 1), round(dex_c, 1), round(unc_c, 1)]
    })
    fig_c = px.bar(contrib_df, x='Điểm số đóng góp thực tế', y='Tiêu chí đặc trưng tác vụ', orientation='h', color='Điểm số đóng góp thực tế', color_continuous_scale='RdYlGn', text='Điểm số đóng góp thực tế')
    fig_c.update_layout(height=320, coloraxis_showscale=False)
    st.plotly_chart(fig_c, use_container_width=True)

    st.markdown("---")
    st.markdown("### ĐÁNH GIÁ TỔNG HỢP BIÊN ĐỘ TỶ SUẤT ROI TRUNG BÌNH THEO TỪNG AI AGENT")
    agent_roi_agg = df.groupby('AI_Agent_Category')['ROI_Score'].mean().reset_index().sort_values(by='ROI_Score', ascending=False).reset_index(drop=True)
    fig_bar_roi = px.bar(agent_roi_agg, x='ROI_Score', y='AI_Agent_Category', orientation='h', color='ROI_Score', color_continuous_scale='viridis', text=agent_roi_agg['ROI_Score'].apply(lambda x: f"ROI: {x:.1f}"))
    fig_bar_roi.update_layout(height=400, xaxis_title="Điểm tỷ suất đầu tư định lượng trung bình (ROI)", yaxis_title="Hệ thống dòng AI Agent chức năng")
    st.plotly_chart(fig_bar_roi, use_container_width=True)


def render_page_4():
    st.markdown("<h1>🤖 TRANG 4 — XẾP HẠNG VÀ KHUYẾN NGHỊ ĐẦU TƯ AI AGENT</h1>", unsafe_allow_html=True)
    st.markdown("### Bảng phân tích định lượng hỗ trợ doanh nghiệp ra quyết định giải ngân ngân sách chính xác.")
    st.markdown("---")
    
    agent_rank = df.groupby('AI_Agent_Category').agg(
        Total_Tasks=('Task ID', 'count'),
        Avg_Score=('Final_Decision_Score', 'mean'),
        Avg_ROI=('ROI_Score', 'mean')
    ).reset_index().sort_values(by='Avg_ROI', ascending=False).reset_index(drop=True)
    
    agent_rank['Mô hình triển khai'] = agent_rank['Avg_Score'].apply(lambda s: phan_lop_mo_hinh_trien_khai(s)[0])
    agent_rank['Độ tin cậy (Confidence %)'] = agent_rank['Total_Tasks'].apply(lambda t: tinh_he_so_confidence_factor(t)[1])
    agent_rank['Quyết định đầu tư (Investment Decision)'] = agent_rank.apply(
        lambda r: quy_doi_nhan_khuyen_nghi_dau_tu(r['Avg_Score'], r['Avg_ROI']), axis=1
    )
    
    agent_rank.columns = [
        'Dòng AI Agent chức năng', 'Quy mô số Task', 'Decision Score Final (Mean)', 
        'ROI Score (Mean)', 'Mô hình triển khai', 'Độ tin cậy (Confidence %)', 'Quyết định đầu tư (Investment Decision)'
    ]
    
    st.markdown("### Bảng xếp hạng và Thẩm định Đầu tư Danh mục AI Agent")
    st.table(agent_rank)


def render_page_5():
    st.markdown("<h1>🏆 TRANG 5 — CHIẾN LƯỢC ĐẦU TƯ CUỐI CÙNG (FINAL RECOMMENDATION)</h1>", unsafe_allow_html=True)
    st.write("Khung phân bổ giải ngân kịch bản đầu tư mở rộng thiết lập riêng cho cấu hình hồ sơ hiện tại.")
    st.markdown("---")
    
    df_metrics = []
    for agent_name in df['AI_Agent_Category'].unique():
        df_sub = df[df['AI_Agent_Category'] == agent_name]
        total_mapped_tasks = len(df_sub)
        
        count_autonomous = sum(df_sub['Final_Decision_Score'] >= 86)
        count_execution = sum((df_sub['Final_Decision_Score'] >= 71) & (df_sub['Final_Decision_Score'] < 86))
        count_copilot = sum((df_sub['Final_Decision_Score'] >= 51) & (df_sub['Final_Decision_Score'] < 71))
        count_hitl = sum((df_sub['Final_Decision_Score'] >= 31) & (df_sub['Final_Decision_Score'] < 51))
        count_human = sum(df_sub['Final_Decision_Score'] < 31)
        
        avg_score = round(df_sub['Final_Decision_Score'].mean(), 1)
        avg_roi = round(df_sub['ROI_Score'].mean(), 1)
        
        df_metrics.append({
            'AI_Agent': agent_name, 'Total_Tasks': total_mapped_tasks, 'Autonomous_Count': count_autonomous,
            'Execution_Count': count_execution, 'Copilot_Count': count_copilot, 'HITL_Count': count_hitl, 'Human_Count': count_human,
            'Avg_Score': avg_score, 'Avg_ROI': avg_roi
        })
        
    df_res = pd.DataFrame(df_metrics).sort_values(by='Avg_ROI', ascending=False).reset_index(drop=True)
    
    st.markdown("## Danh mục toàn bộ các dòng AI Agent theo thống kê thứ tự xếp hạng:")
    
    medals = ["🥇 Khuyến nghị số 1", "🥈 Khuyến nghị số 2", "🥉 Khuyến nghị số 3"]
    for i in range(len(df_res)):
        row_res = df_res.iloc[i]
        m_code, _ = phan_lop_mo_hinh_trien_khai(row_res['Avg_Score'])
        
        c_factor, c_pct = tinh_he_so_confidence_factor(row_res['Total_Tasks'])
        quyet_dinh_ngan = quy_doi_nhan_khuyen_nghi_dau_tu(row_res['Avg_Score'], row_res['Avg_ROI'])
        
        agent_type = row_res['AI_Agent']
        if agent_type == 'Code Review Copilot':
            vi_sao = "Cấu phần Code Review chi phối tỷ trọng rất lớn. Chỉ số Automation Capability thực tế của công nghệ ở mức cao, yêu cầu Human Agency vừa phải, tối ưu hóa rà soát lỗi cú pháp."
            loi_ich = "➔ Giảm thời gian rà duyệt mã nguồn thủ công<br>➔ Phát hiện sớm các lỗ hổng logic kiểm thử<br>➔ Chuẩn hóa quy cách lập trình nội bộ tổ chức"
            luu_y = "➔ Cần tích hợp sâu trực tiếp vào luồng CI/CD hiện hành<br>➔ Duy trì nhân sự rà soát lại ở các phân đoạn kiến trúc lõi phức tạp"
        elif agent_type == 'Testing Agent':
            vi_sao = "Các kịch bản kiểm thử có tính chất lặp đi lặp lại tần suất cao, khối lượng test lớn và rất dễ tự động hóa giúp giải phóng triệt để hiệu suất lao động."
            loi_ich = "➔ Rút ngắn chu kỳ kiểm thử luồng quy trình nghiệp vụ<br>➔ Tăng cường biên độ bao phủ các kịch bản Test Case hệ thống"
            luu_y = "➔ Vẫn cần duy trì kiểm thử thủ công (Manual) đối với các trường hợp trải nghiệm UX đặc biệt phức tạp"
        elif agent_type == 'Documentation Agent':
            vi_sao = "Documentation Task chiếm tỷ trọng lớn trong khối lượng vận hành tĩnh. Automation Capability cao, yêu cầu mức độ Human Agency phê duyệt thấp, thích hợp tự động hóa."
            loi_ich = "➔ Tăng tốc tạo lập và chuẩn hóa hệ thống mẫu tài liệu kỹ thuật<br>➔ Tiết kiệm tối đa thời gian soạn thảo cấu trúc thủ công"
            luu_y = "➔ Cần cập nhật và bổ sung nguồn cơ sở tri thức định kỳ thường xuyên<br>➔ Kiểm tra chéo nội dung sinh tự động trước khi chính thức ban hành"
        elif agent_type == 'Monitoring Agent':
            vi_sao = "Yêu cầu quét và giám sát dữ liệu nhật ký băng ghi liên tục thời gian thực vượt quá năng lực xử lý thủ công của con người, tính chất rập khuôn cao."
            loi_ich = "➔ Phát hiện các hành vi bất thường và lỗi hệ thống nhanh hơn thời gian thực<br>➔ Tối ưu chỉ số SLA, giảm thiểu thời gian Down-time vận hành"
            luu_y = "➔ Cần thiết lập ngưỡng cảnh báo thích hợp để tránh tình trạng báo giả luồng<br>➔ Xây dựng quy trình ứng phó khẩn cấp đi kèm"
        elif agent_type == 'Security Agent':
            vi_sao = "Yêu cầu tính toán an toàn bảo mật nghiêm ngặt, đòi hỏi mức độ Human Agency kiểm duyệt tối cao và hàm lượng chuyên môn sâu sắc để đối phó rủi ro ngoại lệ."
            loi_ich = "➔ Hỗ trợ tự động quét lỗ hổng mã nguồn và cấu hình an ninh mạng<br>➔ Tăng tốc độ phân tích và cảnh báo nguy cơ tiềm ẩn"
            luu_y = "➔ Tuyệt đối không thay thế hoàn toàn vai trò của chuyên gia bảo mật con người<br>➔ Luôn xác minh kỹ lưỡng kết quả đầu ra"
        elif agent_type == 'Database Agent':
            vi_sao = "Tác vụ quản trị và tối ưu cơ sở dữ liệu mang tính cấu trúc hệ thống chặt chẽ, các kịch bản di cư hoặc quét schema phù hợp để máy xác minh."
            loi_ich = "➔ Tự động tối ưu hóa các câu lệnh truy vấn và bảo trì SQL định kỳ<br>➔ Phát hiện nhanh các điểm nghẽn kết nối"
            luu_y = "➔ Giám sát chặt chẽ phân quyền đọc/ghi dữ liệu<br>➔ Thử nghiệm trên môi trường Staging trước khi đồng bộ"
        else:
            vi_sao = f"Dòng Agent quản lý danh mục phù hợp mục tiêu chiến lược tổ chức, đặc tính thấp thâm dụng tương tác và phù hợp tích hợp từng phần."
            loi_ich = "➔ Tăng tốc độ phân phối luồng công việc nghiệp vụ nội bộ<br>➔ Chuẩn hóa số liệu báo cáo phân tích đầu ra"
            luu_y = "➔ Kiểm tra định kỳ mức độ sẵn sàng tiếp nhận của đội ngũ lao động<br>➔ Triển khai cuốn chiếu để thấu hiểu"

        prefix_medal = f"Hạng {i+1}" if i >= 3 else medals[i]

        if "Autonomous" in m_code or "Execution" in m_code:
            human_role = "AI thực hiện phần lớn quy trình chạy tự động hóa độc lập. Con người đóng vai trò kiểm tra, hậu kiểm chất lượng và nghiệm thu kết quả đầu ra cuối cùng."
        elif "Copilot" in m_code:
            human_role = "AI đóng vai trò trợ lý, xử lý các thao tác thủ công rập khuôn. Nhân viên trực tiếp đồng hành phối hợp thời gian thực."
        else:
            human_role = "AI chỉ đóng vai trò tra cứu thông tin hỗ trợ thô. Con người trực tiếp xử lý chính và chịu trách nhiệm toàn bộ luồng quy trình việc."

        html_card = f'<div style="background-color: #ffffff; padding: 24px; border-radius: 12px; border: 1px solid #e0e0e0; border-left: 8px solid #1E88E5; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.04); font-family: sans-serif;"><h3 style="margin: 0; color: #0D47A1; font-size: 1.3rem;">{prefix_medal}: {row_res["AI_Agent"]}</h3><hr style="margin: 10px 0; border: 0; border-top: 1px solid #eee;"><table style="width:100%; border-collapse:collapse; margin-bottom:15px; background:transparent;"><tr style="background:transparent;"><td style="padding:5px 0;"><b>Final Decision Score:</b> {row_res["Avg_Score"]} / 100</td><td style="padding:5px 0;"><b>Estimated ROI:</b> {row_res["Avg_ROI"]}%</td><td style="padding:5px 0;"><b>Độ tin cậy thông kê:</b> {c_pct}</td><td style="padding:5px 0;"><b>Quyết định đầu tư:</b> <span style="color:#1976D2; font-weight:bold;">{quyet_dinh_ngan}</span></td></tr></table><p style="margin: 5px 0; font-weight:bold; color:#333;">Vì sao được khuyến nghị?</p><p style="margin: 2px 0 12px 0; color:#555; font-size:0.95rem;">{vi_sao}</p><p style="margin: 5px 0; font-weight:bold; color:#333;">Khuyến nghị hình thức triển khai ({m_code})</p><p style="margin: 2px 0 12px 0; color:#555; font-size:0.95rem;">{human_role}</p><table style="width:100%; border:none; background:transparent;"><tr style="background:transparent; vertical-align: top;"><td style="width:53%; padding:0 10px 0 0;"><span style="color:#2E7D32; font-weight:bold;">✓ Lợi ích kỳ vọng</span><br><span style="font-size:0.9rem; color:#555;">{loi_ich}</span></td><td style="width:47%; padding:0 10px 0 0;"><span style="color:#E65100; font-weight:bold;">✓ Lưu ý vận hành chi tiết</span><br><span style="font-size:0.9rem; color:#555;">{luu_y}</span></td></tr></table></div>'
        st.html(html_card)

    st.markdown("---")
    st.markdown("### 💡 Luận điểm tóm tắt Chiến lược phân bổ (Strategic Portfolio Insight)")
    st.success(f"Dựa trên kịch bản điều hành thực tế, hệ thống DSS khảo sát hồ sơ quy mô `{sb_size}` và ngân sách cấp `{sb_budget}/100`. Lộ trình ra quyết định phân bổ tối ưu hiện tại khuyến nghị tổ chức đồng hành tập trung nguồn lực vào nhóm đặc thù **{df_res.iloc[0]['AI_Agent']}** để đạt giá trị hoàn vốn tốt nhất, kiểm soát và phòng vệ rủi ro chặt chẽ bám sát thực tiễn tổ chức.")


# ==========================================
# 6. KHỐI ĐIỀU PHỐI ĐIỀU HƯỚNG LUỒNG CHẠY DSS CHÍNH
# ==========================================
if page == "Trang 1 — Tổng quan dữ liệu tác vụ":
    render_page_1()
elif page == "Trang 2 — Cấu hình hệ thống ra quyết định":
    render_page_2()
elif page == "Trang 3 — Mô hình ra quyết định AI":
    render_page_3()
elif page == "Trang 4 — Xếp hạng danh mục AI Agent":
    render_page_4()
elif page == "Trang 5 — Chiến lược đầu tư cuối cùng":
    render_page_5()