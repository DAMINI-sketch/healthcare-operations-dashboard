import streamlit as st
import pandas as pd
import numpy as np
import io

# ==========================================
# PAGE SETTINGS & CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Healthcare Operations Analytics Dashboard",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for Professional Executive Appeal & Signature
st.markdown("""
<style>
    .reportview-container .main .block-container{ max-width: 1200px; }
    .stMetric { background-color: #f8f9fa; padding: 15px; border-radius: 8px; border: 1px solid #e9ecef; }
    div[data-testid="stNotification"] { border-radius: 6px; }
    .signature-text {
        font-family: 'Courier New', Courier, monospace;
        font-size: 13px;
        font-weight: bold;
        color: #6c757d;
        letter-spacing: 1px;
        border-top: 1px dashed #dee2e6;
        padding-top: 10px;
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# HELPER: SAMPLE DATA GENERATOR
# ==========================================
def generate_sample_data():
    np.random.seed(42)
    records = 1200
    
    dates = pd.date_range(start="2026-01-01", periods=90, freq="D")
    sampled_dates = np.random.choice(dates, size=records)
    
    priorities = np.random.choice(["High", "Medium", "Low"], size=records, p=[0.3, 0.5, 0.2])
    statuses = np.random.choice(["Closed", "Pending"], size=records, p=[0.82, 0.18])
    tats = np.random.normal(loc=3.2, scale=1.0, size=records).clip(1, 10).round(1)
    
    df = pd.DataFrame({
        "Case ID": [f"HC-2026-{i:04d}" for i in range(1, records + 1)],
        "Log Date": sampled_dates,
        "Priority": priorities,
        "Status": statuses,
        "Turnaround Time (Days)": tats
    })
    
    # 45 Missing values
    for i in range(15):
        df.loc[i * 25, "Priority"] = None
    for i in range(30):
        df.loc[i * 35, "Turnaround Time (Days)"] = None
        
    # 18 Duplicate rows
    duplicates = df.sample(n=18, random_state=42)
    df = pd.concat([df, duplicates], ignore_index=True)
    
    return df

# ==========================================
# APP LAYOUT & SIDEBAR
# ==========================================
st.title("🏥 Healthcare Operations Analytics Dashboard")
st.caption("Enterprise-Grade Operational KPI Engine & Executive Report Matrix")

st.sidebar.markdown("### 👤 Candidate Profile")
st.sidebar.info("**Damini Prajapati**\n\nHealthcare Operations & Data Analyst")

st.sidebar.markdown("---")
st.sidebar.markdown("### 📥 Ingestion Controls")

uploaded_file = st.sidebar.file_uploader("Upload Operational Excel/CSV", type=["csv", "xlsx"])
load_sample = st.sidebar.button("📊 Load Flagship Sample Dataset (1,200 Records)")

df_raw = None
if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            df_raw = pd.read_csv(uploaded_file)
        else:
            df_raw = pd.read_excel(uploaded_file)
        st.sidebar.success("Custom Dataset Ingested!")
    except Exception as e:
        st.sidebar.error(f"Error parsing file: {e}")
else:
    df_raw = generate_sample_data() # Pre-populate instantly for recruiter view

# ==========================================
# PROCESSING PIPELINE
# ==========================================

# 1. Data Quality Calculations
total_records = len(df_raw)
missing_records = df_raw.isnull().sum().sum()
duplicate_records = df_raw.duplicated().sum()

total_cells = df_raw.size
if total_cells > 0:
    quality_score = int(((total_cells - (missing_records + duplicate_records)) / total_cells) * 100)
else:
    quality_score = 100

# UPGRADE 1: Data Health Status Logic
if quality_score >= 95:
    data_health_status = "🟢 EXCELLENT"
elif quality_score >= 90:
    data_health_status = "🟡 GOOD"
elif quality_score >= 80:
    data_health_status = "🟠 NEEDS REVIEW"
else:
    data_health_status = "🔴 CRITICAL"

# 2. KPI Pipeline Engine
df_clean = df_raw.dropna(subset=["Status", "Turnaround Time (Days)"]).drop_duplicates()

total_cases = len(df_clean)
avg_tat = round(df_clean["Turnaround Time (Days)"].mean(), 1) if total_cases > 0 else 0

closed_count = len(df_clean[df_clean["Status"] == "Closed"])
pending_count = len(df_clean[df_clean["Status"] == "Pending"])

closed_pct = int((closed_count / total_cases) * 100) if total_cases > 0 else 0
pending_pct = int((pending_count / total_cases) * 100) if total_cases > 0 else 0

# ==========================================
# ALERT ENGINE & UPGRADE 2 LOGIC
# ==========================================
alert_count = 0
alert_messages = []

if pending_pct > 30:
    alert_messages.append(f"⚠️ **High Pending Backlog Detected:** System backlog is at **{pending_pct}%** (Limit: 30%).")
    alert_count += 1

if avg_tat > 3.5:
    alert_messages.append(f"⚠️ **TAT Breach Risk Warning:** Current TAT is **{avg_tat} Days** (Target: 3.5 Days).")
    alert_count += 1

if quality_score < 90:
    alert_messages.append(f"⚠️ **Data Quality Integrity Issue:** Database health score dropped to **{quality_score}%**.")
    alert_count += 1

# UPGRADE 2: Operational Health Rating Rule
if alert_count == 0:
    op_health_rating = "🟢 GREEN"
elif alert_count == 1:
    op_health_rating = "🟡 AMBER"
else:
    op_health_rating = "🔴 RED"

# ==========================================
# RENDER: UI BLOCKS
# ==========================================

# 📥 STEP 1 & 🧹 STEP 2: Preview & Quality Assessment Tabs
st.subheader("🧹 System Ingestion & Data Quality Center")
col_q1, col_q2 = st.columns([3, 2])

with col_q1:
    st.markdown("**Dataset Preview (First 5 Rows)**")
    st.dataframe(df_raw.head(5), use_container_width=True, hide_index=True)

with col_q2:
    st.markdown("**Data Quality Metrics Matrix**")
    quality_data = {
        "Metric Parameter": ["Total Records Ingested", "Total Missing Data Points", "Duplicate Records", "Overall Quality Score", "Data Health Status"],
        "System Log Result": [f"{total_records:,}", f"{missing_records}", f"{duplicate_records}", f"{quality_score}%", data_health_status]
    }
    st.table(pd.DataFrame(quality_data))

st.markdown("---")

# 📊 STEP 3: KPI Engine Row
st.subheader("📊 Operational Core KPI Engine")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("Total Operational Cases", f"{total_cases:,}")
kpi2.metric("Average TAT (Target: 3.5 Days)", f"{avg_tat} Days")
kpi3.metric("Case Closure Rate (%)", f"{closed_pct}%")
kpi4.metric("Pending Backlog (%)", f"{pending_pct}%")

st.markdown("---")

# 📈 STEP 4: Visual Analytics Block
st.subheader("📈 Core Operational Chart Analytics")
v_col1, v_col2, v_col3 = st.columns(3)

try:
    with v_col1:
        st.markdown("**1. Case Operations Volume by Month**")
        if "Log Date" in df_clean.columns:
            df_clean['Log Date'] = pd.to_datetime(df_clean['Log Date'])
            monthly_data = df_clean.groupby(df_clean['Log Date'].dt.strftime('%B')).size()
            st.bar_chart(monthly_data)
        else:
            st.info("Log Date column missing.")

    with v_col2:
        st.markdown("**2. Operational Case Load by Priority**")
        if "Priority" in df_clean.columns:
            priority_data = df_clean.groupby("Priority").size()
            st.bar_chart(priority_data)
        else:
            st.info("Priority parameters not found.")

    with v_col3:
        st.markdown("**3. Allocation Split: Closed vs Pending**")
        if "Status" in df_clean.columns:
            status_data = df_clean.groupby("Status").size()
            st.bar_chart(status_data)
        else:
            st.info("Status vector missing.")
except Exception as e:
    st.warning("Visual rendering skipped due to data variance.")

st.markdown("---")

# 🚨 STEP 5: Operations Alert Engine
st.subheader("🚨 Real-Time Operations Alert Engine")
if alert_count > 0:
    for msg in alert_messages:
        if "High" in msg or "Integrity" in msg:
            st.error(msg)
        else:
            st.warning(msg)
else:
    st.success("✅ **System Status Nominal:** All operational parameters are functioning within healthy baseline thresholds.")

st.markdown("---")

# 📋 STEP 6 & 📥 STEP 7: Executive Summary & Export Operations
st.subheader("📋 Executive Summary Generator (Management Report)")

# System Generated Dynamic Summary with UPGRADE 2
summary_text = (
    f"Executive Report Summary:\n"
    f"-------------------------\n"
    f"Operational Health Rating: {op_health_rating}\n"
    f"Dataset Health Analysis   : {data_health_status} (Quality Score: {quality_score}%)\n\n"
    f"The ingested operations registry contains exactly {total_records:,} operational data records.\n"
    f"The system calculated an active core case closure rate of {closed_pct}% against a pending backlog of {pending_pct}%.\n"
    f"The current operational efficiency registers an Average Turnaround Time (TAT) of {avg_tat} days.\n"
)
if alert_count > 0:
    summary_text += f"Alert Notification: {alert_count} critical threshold warning(s) logged in the Alert Engine panel. Action required."
else:
    summary_text += "Alert Notification: System reports zero critical operational threshold alerts."

st.text_area("Management Insights Report Output (Read-Only Copy)", summary_text, height=160)

# Export Segment Buttons
st.markdown("### 📥 Framework Data Export Hub")
ex_col1, ex_col2 = st.columns(2)

with ex_col1:
    kpi_df = pd.DataFrame({
        "KPI Metric": ["Total Ingested Cases", "Average Turnaround Time", "Closure Percentage", "Pending Backlog Percentage", "Data Quality Score", "Operational Health Rating"],
        "Value": [total_cases, avg_tat, f"{closed_pct}%", f"{pending_pct}%", f"{quality_score}%", op_health_rating]
    })
    csv_buffer = io.StringIO()
    kpi_df.to_csv(csv_buffer, index=False)
    
    st.download_button(
        label="📥 Export KPI Performance Report (CSV)",
        data=csv_buffer.getvalue(),
        file_name="healthcare_kpi_performance_report.csv",
        mime="text/csv",
        use_container_width=True
    )

with ex_col2:
    st.download_button(
        label="📥 Export Executive Summary Insights (TXT)",
        data=summary_text,
        file_name="management_executive_summary.txt",
        mime="text/plain",
        use_container_width=True
    )

# ==========================================
# IMPRESSIVE SIGNATURE ADDITIONS
# ==========================================
# 1. Sidebar Bottom Signature
st.sidebar.markdown("<div class='signature-text'>⚙️ DESIGNED BY DAMINI</div>", unsafe_allow_html=True)

# 2. Main App Footer Signature
st.markdown("<div class='signature-text' style='text-align: center;'>🏥 Healthcare Operations Analytics Dashboard • System Build v1.1.0 • Verified & Developed by Damini Prajapati</div>", unsafe_allow_html=True)
