import streamlit as st

# =============================
# PAGE CONFIG
# =============================
st.set_page_config(
    page_title="Kewangan Mi-Ha",
    page_icon="💰",
    layout="centered"
)

# =============================
# STYLE (corak + vibe duit)
# =============================
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #fdfcfb, #e2ebf0);
}
.card {
    background: #ffffff;
    padding: 20px;
    border-radius: 16px;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}
h1, h2, h3 {
    color: #2c7a7b;
}
.money {
    background: linear-gradient(120deg, #c6f6d5, #fefcbf);
    padding: 15px;
    border-radius: 14px;
}
</style>
""", unsafe_allow_html=True)

# =============================
# TITLE
# =============================
st.markdown("<h1>💰 Kewangan Mi-Ha</h1>", unsafe_allow_html=True)
st.caption("Urus kewangan tanpa stress 🌱")

# =============================
# SESSION STATE
# =============================
if "barang" not in st.session_state:
    st.session_state.barang = []

if "hutang" not in st.session_state:
    st.session_state.hutang = ["UOB", "Shopee"]

# =============================
# BARANG BELUM DIBELI
# =============================
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("🛒 Barang Nak Beli")

new_item = st.text_input("Tambah barang baru")
if st.button("➕ Tambah Barang"):
    if new_item:
        st.session_state.barang.append(new_item)

for item in st.session_state.barang.copy():
    col1, col2, col3 = st.columns([4, 1, 1])
    col1.write(item)
    sudah = col2.checkbox("Sudah", key=f"sudah_{item}")
    col3.checkbox("Belum", value=True, disabled=True)

    if sudah:
        st.session_state.barang.remove(item)
        st.experimental_rerun()

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
    amount = col2.number_input(f"RM {bank}", min_value=0.0, step=10.0, key=bank)
    total_simpanan += amount

st.success(f"💎 Jumlah Simpanan: RM {total_simpanan:,.2f}")
st.markdown("</div>", unsafe_allow_html=True)

# =============================
# HUTANG
# =============================
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("📉 Hutang")

new_hutang = st.text_input("Tambah hutang baru")
if st.button("➕ Tambah Hutang"):
    if new_hutang:
        st.session_state.hutang.append(new_hutang)

total_hutang = 0
for h in st.session_state.hutang:
    col1, col2 = st.columns([3, 2])
    col1.write(h)
    amount = col2.number_input(f"RM {h}", min_value=0.0, step=10.0, key=f"hutang_{h}")
    total_hutang += amount

st.error(f"💸 Jumlah Hutang: RM {total_hutang:,.2f}")
st.markdown("</div>", unsafe_allow_html=True)

# =============================
# RINGKASAN
# =============================
st.markdown("<div class='card money'>", unsafe_allow_html=True)
st.subheader("📊 Ringkasan")

baki = total_simpanan - total_hutang

if baki >= 0:
    st.success(f"✅ Baki Bersih: RM {baki:,.2f}")
else:
    st.warning(f"⚠️ Baki Bersih: RM {baki:,.2f}")

st.markdown("</div>", unsafe_allow_html=True)

st.caption("✨ Perlahan-lahan, kewangan pun boleh tenang.")
