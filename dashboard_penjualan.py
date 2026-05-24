"""
Dashboard Analisis Penjualan Indonesia
Capstone Project - Data Science
Jalankan: streamlit run dashboard_penjualan.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings("ignore")

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Dashboard Penjualan Indonesia",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CUSTOM CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    
    .main-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #4776b6 100%);
        padding: 2rem 2.5rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
        box-shadow: 0 8px 32px rgba(30,60,114,0.35);
    }
    .main-header h1 { font-size: 2.2rem; font-weight: 700; margin-bottom: 0.3rem; }
    .main-header p  { font-size: 1rem; opacity: 0.85; margin: 0; }

    .metric-card {
        background: white;
        border-radius: 14px;
        padding: 1.4rem 1.6rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border-left: 5px solid;
        transition: transform 0.2s;
    }
    .metric-card:hover { transform: translateY(-3px); }
    .metric-card.blue   { border-color: #2196F3; }
    .metric-card.green  { border-color: #4CAF50; }
    .metric-card.orange { border-color: #FF9800; }
    .metric-card.purple { border-color: #9C27B0; }
    .metric-label { font-size: 0.8rem; color: #888; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }
    .metric-value { font-size: 1.9rem; font-weight: 700; color: #1a1a2e; margin: 0.3rem 0; }
    .metric-delta { font-size: 0.8rem; color: #4CAF50; font-weight: 600; }

    .section-title {
        font-size: 1.1rem; font-weight: 700; color: #1e3c72;
        border-bottom: 3px solid #2196F3;
        padding-bottom: 0.5rem; margin-bottom: 1rem;
    }
    
    .insight-box {
        background: linear-gradient(135deg, #e8f4fd, #d1ecfb);
        border-left: 4px solid #2196F3;
        border-radius: 8px;
        padding: 1rem 1.2rem;
        margin: 0.5rem 0;
        font-size: 0.9rem;
        color: #1a3a5c;
    }
    
    .stSelectbox > div > div { border-radius: 8px; }
    
    footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ─── LOAD & CLEAN DATA ───────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("data_bersih_Dataset_Penjualan_Full_Indonesia.csv")

    def parse_rp(s):
        return float(str(s).replace("Rp", "").replace(".", "").replace(",", "."))

    df["Harga_num"]  = df["Harga_Satuan"].apply(parse_rp)
    df["Total_num"]  = df["Total_Penjualan"].apply(parse_rp)
    df["Tanggal"]    = pd.to_datetime(df["Tanggal"])
    df["Tahun"]      = df["Tanggal"].dt.year
    df["Bulan_Num"]  = df["Tanggal"].dt.month
    df["Bulan_Str"]  = df["Tanggal"].dt.strftime("%Y-%m")
    df["Bulan_Label"]= df["Tanggal"].dt.strftime("%b %Y")
    return df

df = load_data()

# ─── SIDEBAR FILTERS ─────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎛️ Filter Data")
    st.divider()

    tahun_list = sorted(df["Tahun"].unique())
    tahun_sel  = st.multiselect("📅 Tahun", tahun_list, default=tahun_list)

    kat_list = sorted(df["Kategori"].unique())
    kat_sel  = st.multiselect("🏷️ Kategori", kat_list, default=kat_list)

    st.divider()
    st.markdown("**📊 Dataset Info**")
    st.info(f"🗂️ Total Baris: **{len(df):,}**\n\n📦 Produk Unik: **{df['Produk'].nunique():,}**\n\n📁 Kategori: **{df['Kategori'].nunique()}**")
    st.markdown("---")
    st.caption("Dashboard Capstone · Data Science")

# ─── FILTER APPLICATION ──────────────────────────────────────────────────────
filtered = df[df["Tahun"].isin(tahun_sel) & df["Kategori"].isin(kat_sel)]

# ─── HEADER ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>🛒 Dashboard Analisis pendapatan dan transaksi</h1>
    <p>Exploratory Data Analysis · Capstone Project Data Science 2024–2026</p>
</div>
""", unsafe_allow_html=True)

# ─── KPI METRICS ─────────────────────────────────────────────────────────────
total_rev   = filtered["Total_num"].sum()
total_order = len(filtered)
avg_order   = filtered["Total_num"].mean()
total_prod  = filtered["Produk"].nunique()

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="metric-card blue">
        <div class="metric-label">💰 Total Pendapatan</div>
        <div class="metric-value">Rp {total_rev/1e9:.2f}M</div>
        <div class="metric-delta">↑ Miliar Rupiah</div>
    </div>""", unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="metric-card green">
        <div class="metric-label">🧾 Total Transaksi</div>
        <div class="metric-value">{total_order:,}</div>
        <div class="metric-delta">↑ Orders</div>
    </div>""", unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="metric-card orange">
        <div class="metric-label">📊 Rata-rata per Order</div>
        <div class="metric-value">Rp {avg_order/1e3:.1f}K</div>
        <div class="metric-delta">↑ Per Transaksi</div>
    </div>""", unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="metric-card purple">
        <div class="metric-label">📦 Produk Unik</div>
        <div class="metric-value">{total_prod:,}</div>
        <div class="metric-delta">↑ SKU Aktif</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── ROW 1: Tren & Kategori ───────────────────────────────────────────────────
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<div class="section-title">📈 Tren Pendapatan Bulanan</div>', unsafe_allow_html=True)
    tren = (filtered.groupby("Bulan_Str")["Total_num"]
            .sum().reset_index().sort_values("Bulan_Str"))
    
    fig_tren = go.Figure()
    fig_tren.add_trace(go.Scatter(
        x=tren["Bulan_Str"], y=tren["Total_num"],
        mode="lines+markers",
        line=dict(color="#2196F3", width=3),
        marker=dict(size=7, color="#1565C0"),
        fill="tozeroy",
        fillcolor="rgba(33,150,243,0.12)",
        name="Pendapatan"
    ))
    fig_tren.update_layout(
        height=320, margin=dict(l=0, r=0, t=10, b=30),
        xaxis=dict(tickangle=-45, tickfont=dict(size=10)),
        yaxis=dict(tickformat=".2s", tickprefix="Rp"),
        plot_bgcolor="white", paper_bgcolor="white",
        showlegend=False,
        hovermode="x unified"
    )
    st.plotly_chart(fig_tren, use_container_width=True)

with col2:
    st.markdown('<div class="section-title">🏷️ Revenue per Kategori</div>', unsafe_allow_html=True)
    by_kat = (filtered.groupby("Kategori")["Total_num"]
              .sum().sort_values().reset_index())
    
    fig_kat = go.Figure(go.Bar(
        x=by_kat["Total_num"], y=by_kat["Kategori"],
        orientation="h",
        marker=dict(
            color=by_kat["Total_num"],
            colorscale="Blues",
            showscale=False
        ),
        text=[f"Rp {v/1e6:.1f}Jt" for v in by_kat["Total_num"]],
        textposition="outside",
        textfont=dict(size=9)
    ))
    fig_kat.update_layout(
        height=320, margin=dict(l=0, r=60, t=10, b=10),
        xaxis=dict(showticklabels=False),
        plot_bgcolor="white", paper_bgcolor="white"
    )
    st.plotly_chart(fig_kat, use_container_width=True)

# ─── ROW 2: Pie & Top Produk ─────────────────────────────────────────────────
col3, col4 = st.columns([1, 2])

with col3:
    st.markdown('<div class="section-title">🥧 Distribusi Order per Kategori</div>', unsafe_allow_html=True)
    orders_kat = filtered.groupby("Kategori").size().reset_index(name="Orders")
    
    fig_pie = px.pie(
        orders_kat, values="Orders", names="Kategori",
        color_discrete_sequence=px.colors.qualitative.Set3,
        hole=0.45
    )
    fig_pie.update_traces(textposition="inside", textinfo="percent+label", textfont_size=10)
    fig_pie.update_layout(
        height=350, margin=dict(l=0, r=0, t=10, b=0),
        showlegend=False, paper_bgcolor="white"
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with col4:
    st.markdown('<div class="section-title">🏆 Top 10 Produk Terlaris (Revenue)</div>', unsafe_allow_html=True)
    top10 = (filtered.groupby("Produk")["Total_num"]
             .sum().sort_values(ascending=False).head(10).reset_index())
    
    colors = ["#1565C0","#1976D2","#1E88E5","#2196F3","#42A5F5",
              "#64B5F6","#90CAF9","#BBDEFB","#E3F2FD","#F0F8FF"]
    
    fig_top = go.Figure(go.Bar(
        x=top10["Produk"], y=top10["Total_num"],
        marker=dict(color=colors),
        text=[f"Rp {v/1e6:.1f}Jt" for v in top10["Total_num"]],
        textposition="outside",
        textfont=dict(size=10)
    ))
    fig_top.update_layout(
        height=350, margin=dict(l=0, r=0, t=10, b=80),
        xaxis=dict(tickangle=-35, tickfont=dict(size=10)),
        yaxis=dict(tickformat=".2s", tickprefix="Rp"),
        plot_bgcolor="white", paper_bgcolor="white"
    )
    st.plotly_chart(fig_top, use_container_width=True)

# ─── ROW 3: Heatmap + Distribusi Jumlah ──────────────────────────────────────
col5, col6 = st.columns([2, 1])

with col5:
    st.markdown('<div class="section-title">🗓️ Heatmap Transaksi (Bulan × Kategori)</div>', unsafe_allow_html=True)
    heatmap_df = (filtered.groupby(["Bulan_Num","Kategori"])
                  .size().reset_index(name="Count"))
    pivot = heatmap_df.pivot(index="Kategori", columns="Bulan_Num", values="Count").fillna(0)
    bulan_names = {1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"Mei",6:"Jun",
                   7:"Jul",8:"Agu",9:"Sep",10:"Okt",11:"Nov",12:"Des"}
    pivot.columns = [bulan_names.get(c, str(c)) for c in pivot.columns]
    
    fig_heat = px.imshow(
        pivot, color_continuous_scale="Blues",
        aspect="auto", text_auto=True
    )
    fig_heat.update_layout(
        height=380, margin=dict(l=0, r=0, t=10, b=0),
        paper_bgcolor="white", coloraxis_showscale=True
    )
    fig_heat.update_traces(textfont_size=9)
    st.plotly_chart(fig_heat, use_container_width=True)

with col6:
    st.markdown('<div class="section-title">📦 Distribusi Kuantitas Order</div>', unsafe_allow_html=True)
    qty_dist = filtered["Jumlah"].value_counts().sort_index().reset_index()
    qty_dist.columns = ["Jumlah", "Count"]
    
    fig_qty = go.Figure(go.Bar(
        x=qty_dist["Jumlah"].astype(str), y=qty_dist["Count"],
        marker=dict(color=["#1565C0","#1E88E5","#42A5F5","#90CAF9","#BBDEFB"]),
        text=qty_dist["Count"], textposition="outside"
    ))
    fig_qty.update_layout(
        height=380, margin=dict(l=0, r=0, t=10, b=30),
        xaxis_title="Jumlah Item", yaxis_title="Frekuensi",
        plot_bgcolor="white", paper_bgcolor="white"
    )
    st.plotly_chart(fig_qty, use_container_width=True)

# ─── ROW 4: Pendapatan per Tahun ─────────────────────────────────────────────
st.markdown('<div class="section-title">📅 Perbandingan Pendapatan per Tahun</div>', unsafe_allow_html=True)

by_tahun = filtered.groupby("Tahun")["Total_num"].sum().reset_index()
by_tahun["Label"] = by_tahun["Total_num"].apply(lambda x: f"Rp {x/1e9:.2f} Miliar")

fig_year = go.Figure(go.Bar(
    x=by_tahun["Tahun"].astype(str), y=by_tahun["Total_num"],
    marker=dict(
        color=by_tahun["Total_num"],
        colorscale=[[0,"#BBDEFB"],[0.5,"#1E88E5"],[1,"#0D47A1"]],
        showscale=False,
        line=dict(color="white", width=2)
    ),
    text=by_tahun["Label"], textposition="outside",
    textfont=dict(size=11, color="#1a1a2e")
))
fig_year.update_layout(
    height=280, margin=dict(l=0, r=0, t=10, b=20),
    xaxis=dict(tickfont=dict(size=13)),
    yaxis=dict(tickformat=".2s", tickprefix="Rp"),
    plot_bgcolor="white", paper_bgcolor="white"
)
st.plotly_chart(fig_year, use_container_width=True)

# ─── INSIGHT SECTION ─────────────────────────────────────────────────────────
st.markdown('<div class="section-title">💡 Business Insights & Kesimpulan</div>', unsafe_allow_html=True)

top_kat    = filtered.groupby("Kategori")["Total_num"].sum().idxmax()
top_rev    = filtered.groupby("Kategori")["Total_num"].sum().max()
top_produk = filtered.groupby("Produk")["Total_num"].sum().idxmax()
best_bulan = filtered.groupby("Bulan_Str")["Total_num"].sum().idxmax()

i1, i2, i3 = st.columns(3)
with i1:
    st.markdown(f"""
    <div class="insight-box">
        🥇 <strong>Kategori Terlaris:</strong><br>
        <strong>{top_kat}</strong> menyumbang Rp {top_rev/1e6:.1f} Juta (revenue tertinggi dari semua kategori).
    </div>""", unsafe_allow_html=True)

with i2:
    st.markdown(f"""
    <div class="insight-box">
        🏆 <strong>Produk #1:</strong><br>
        <strong>{top_produk}</strong> adalah produk dengan total pendapatan tertinggi secara keseluruhan.
    </div>""", unsafe_allow_html=True)

with i3:
    st.markdown(f"""
    <div class="insight-box">
        📅 <strong>Bulan Puncak Penjualan:</strong><br>
        Transaksi tertinggi tercatat pada <strong>{best_bulan}</strong> — pertimbangkan strategi promo di periode ini.
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── DATA TABLE ──────────────────────────────────────────────────────────────
with st.expander("📋 Lihat Data Mentah (Filtered)"):
    st.dataframe(
        filtered[["ID_Pesanan","Tanggal","Produk","Kategori","Jumlah","Harga_Satuan","Total_Penjualan"]]
        .sort_values("Tanggal", ascending=False)
        .head(500),
        use_container_width=True,
        hide_index=True
    )
    st.caption(f"Menampilkan 500 baris pertama dari {len(filtered):,} baris hasil filter")

# ─── FOOTER ──────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align:center; color:#888; font-size:0.85rem; padding: 1rem">
    📊 Dashboard Penjualan Indonesia · Capstone Project Data Science 2026 · Built with Streamlit & Plotly
</div>
""", unsafe_allow_html=True)
