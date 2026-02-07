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
# STYLE (ringan & duit vibe)
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
# BARANG NAK BELI
# =============================
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("🛒 Barang Nak Beli")

with st.form("form_barang", clear_on_submit=True):
    new_item = st.text_input("Tambah barang baru")
    submit = st.form_submit_button("➕ Tambah Barang")

    if submit and new_item:
        st.session_state.barang.append(
            {"nama": new_item, "id": len(st.session_state.barang)}
        )

st.divider()

if st.session_state.barang:
    to_remove = []
    for item in st.session_state.barang:
        # 3 column: nama | spacer | checkboxes
        col1, col2, col3 = st.columns([4, 0.1, 2])
        col1.write(item["nama"])
        
        with col3:
            checkbox_cols = st.columns([1, 1])
            sudah = checkbox_cols[0].checkbox(
                "Sudah",
                key=f"sudah_{item['id']}"
            )
            checkbox_cols[1].checkbox(
                "Belum",
                value=True,
                disabled=True,
                key=f"belum_{item['id']}"
            )
        
        if sudah:
            to_remove.append(item)
    
    # Remove barang selepas loop, elak hilang widget
    for item in to_remove:
        st.session_state.barang.remove(item)
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
