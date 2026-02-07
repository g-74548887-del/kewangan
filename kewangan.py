import streamlit as st
import pandas as pd

# =============================
# PAGE CONFIG
# =============================
st.set_page_config(
    page_title="Kewangan Mi-Ha",
    page_icon="💰",
    layout="wide"
)

# =============================
# STYLE
# =============================
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #fdfcfb, #e2ebf0);
}
.card {
    background: white;
    padding: 18px;
    border-radius: 16px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}
.money {
    background: linear-gradient(120deg, #c6f6d5, #fefcbf);
    padding: 18px;
    border-radius: 16px;
}
.table-container {
    max-height: 400px;
    overflow-y: auto;
}
</style>
""", unsafe_allow_html=True)

# =============================
# TITLE
# =============================
st.title("💰 Kewangan Mi-Ha")
st.caption("Urus kewangan perlahan-lahan, janji tenang 🌱")

# =============================
# SESSION STATE
# =============================
if "barang" not in st.session_state:
    st.session_state.barang = []

if "hutang" not in st.session_state:
    st.session_state.hutang = ["UOB", "Shopee"]

# =============================
# FORM TAMBAH BARANG
# =============================
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("🛒 Barang Nak Beli")

with st.form("form_barang", clear_on_submit=True):
    new_item = st.text_input("Tambah barang baru")
    submit = st.form_submit_button("➕ Tambah Barang")
    if submit and new_item:
        st.session_state.barang.append({"nama": new_item, "id": len(st.session_state.barang)})

st.divider()

# =============================
# PAPAR BARANG DALAM TABLE
# =============================
if st.session_state.barang:
    # buat DataFrame sementara untuk paparan
    df = pd.DataFrame(st.session_state.barang)
    df_display = df[['nama']].copy()
    df_display.index = range(1, len(df_display)+1)
    df_display.rename(columns={'nama': 'Barang'}, inplace=True)
    
    st.markdown("<div class='table-container'>", unsafe_allow_html=True)
    
    for i, row in df_display.iterrows():
        col1, col2 = st.columns([4, 1])
        col1.write(row['Barang'])
        btn = col2.button("Klik jika Sudah", key=f"sudah_{st.session_state.barang[i-1]['id']}")
        if btn:
            st.session_state.barang.pop(i-1)
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)
else:
    st.info("Tiada barang dalam senarai")

st.markdown("</div>", unsafe_allow_html=True)

# =============================
# SIMPANAN
# =============================
st.markdown("<div class='card money'>", unsafe_allow_html=True)
st.subheader("🏦 Simpanan")

simpanan = ["Ambank", "CIMB", "Maybank", "Tabung Haji", "Bank Islam"]
total_simpanan = 0

for bank in simpanan:
    col1, col2 = st.columns([3, 2])
    col1.write(bank)
    nilai = col2.number_input(
        f"RM {bank}",
        min_value=0.0,
        step=10.0,
        key=f"simpan_{bank}"
    )
    total_simpanan += nilai

st.success(f"💎 Jumlah Simpanan: RM {total_simpanan:,.2f}")
st.markdown("</div>", unsafe_allow_html=True)

# =============================
# HUTANG
# =============================
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("📉 Hutang")

with st.form("form_hutang", clear_on_submit=True):
    hutang_baru = st.text_input("Tambah hutang baru")
    submit_hutang = st.form_submit_button("➕ Tambah Hutang")
    if submit_hutang and hutang_baru:
        st.session_state.hutang.append(hutang_baru)

total_hutang = 0
for h in st.session_state.hutang:
    col1, col2 = st.columns([3, 2])
    col1.write(h)
    nilai = col2.number_input(
        f"RM {h}",
        min_value=0.0,
        step=10.0,
        key=f"hutang_{h}"
    )
    total_hutang += nilai

st.error(f"💸 Jumlah Hutang: RM {total_hutang:,.2f}")
st.markdown("</div>", unsafe_allow_html=True)

# =============================
# RINGKASAN
# =============================
st.markdown("<div class='card money'>", unsafe_allow_html=True)
st.subheader("📊 Ringkasan Kewangan")

baki = total_simpanan - total_hutang
if baki >= 0:
    st.success(f"✅ Baki Bersih: RM {baki:,.2f}")
else:
    st.warning(f"⚠️ Baki Bersih: RM {baki:,.2f}")

st.markdown("</div>", unsafe_allow_html=True)

st.caption("✨ Tak apa sikit-sikit. Yang penting istiqamah.")
