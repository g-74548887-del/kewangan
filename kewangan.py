import streamlit as st
import json
import os

# =============================
# FILE SAVE
# =============================
DATA_FILE = "data_kewangan.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {
        "barang": [],
        "simpanan": {},
        "hutang": {},
        "maybank_detail": [
            {"rm": 0.0, "catatan": ""},
            {"rm": 0.0, "catatan": ""},
            {"rm": 0.0, "catatan": ""},
            {"rm": 0.0, "catatan": ""}
        ]
    }

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

data = load_data()

# =============================
# PAGE CONFIG
# =============================
st.set_page_config(
    page_title="Kewangan Mi-Ha",
    page_icon="💰",
    layout="centered"
)

# =============================
# STYLE
# =============================
st.markdown("""
<style>
.card {
    background: white;
    padding: 18px;
    border-radius: 16px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}
.money {
    background: linear-gradient(120deg, #c6f6d5, #fefcbf);
}
</style>
""", unsafe_allow_html=True)

# =============================
# TITLE
# =============================
st.title("💰 Kewangan Mi-Ha")
st.caption("Sikit-sikit, lama-lama jadi bukit 🌱")

# =============================
# BARANG NAK BELI (PILIH DULU)
# =============================
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("🛒 Barang Nak Beli")

if "selected_barang" not in st.session_state:
    st.session_state.selected_barang = []

with st.form("form_barang", clear_on_submit=True):
    barang_baru = st.text_input("Tambah barang")
    if st.form_submit_button("➕ Tambah"):
        if barang_baru.strip():
            data["barang"].append(barang_baru.strip())
            save_data(data)

st.divider()

if data["barang"]:
    col_left, col_right = st.columns([3, 2])

    # ===== KIRI: SENARAI BARANG =====
    with col_left:
        st.markdown("**📋 Senarai Barang**")
        for i, barang in enumerate(data["barang"]):
            pilih = st.checkbox(
                barang,
                key=f"pilih_{i}",
                value=barang in st.session_state.selected_barang
            )

            if pilih and barang not in st.session_state.selected_barang:
                st.session_state.selected_barang.append(barang)

            if not pilih and barang in st.session_state.selected_barang:
                st.session_state.selected_barang.remove(barang)

    # ===== KANAN: DIPILIH =====
    with col_right:
        st.markdown("**✅ Dipilih / Sudah**")
        if st.session_state.selected_barang:
            for b in st.session_state.selected_barang:
                st.write("•", b)
        else:
            st.caption("Belum pilih barang")

    st.divider()

    if st.button("✔️ Tandakan Sudah"):
        for b in st.session_state.selected_barang:
            if b in data["barang"]:
                data["barang"].remove(b)

        st.session_state.selected_barang = []
        save_data(data)
        st.rerun()
else:
    st.info("Tiada barang dalam senarai")

st.markdown("</div>", unsafe_allow_html=True)

# =============================
# SIMPANAN
# =============================
st.markdown("<div class='card money'>", unsafe_allow_html=True)
st.subheader("🏦 Simpanan")

bank_list = ["Ambank", "CIMB", "Tabung Haji", "Bank Islam"]
total_simpanan = 0

for bank in bank_list:
    nilai = st.number_input(
        f"RM {bank}",
        min_value=0.0,
        step=10.0,
        value=data["simpanan"].get(bank, 0.0)
    )
    data["simpanan"][bank] = nilai
    total_simpanan += nilai

# =============================
# MAYBANK (4 BARIS + CATATAN)
# =============================
st.markdown("### 🏦 Maybank (Pecahan Simpanan)")

jumlah_maybank = 0
for i in range(4):
    col1, col2 = st.columns([2, 3])
    rm = col1.number_input(
        f"RM {i+1}",
        min_value=0.0,
        step=10.0,
        value=data["maybank_detail"][i]["rm"],
        key=f"maybank_rm_{i}"
    )
    catatan = col2.text_input(
        "Catatan",
        value=data["maybank_detail"][i]["catatan"],
        key=f"maybank_cat_{i}"
    )

    data["maybank_detail"][i]["rm"] = rm
    data["maybank_detail"][i]["catatan"] = catatan
    jumlah_maybank += rm

total_simpanan += jumlah_maybank

st.success(f"Jumlah Maybank: RM {jumlah_maybank:,.2f}")
st.success(f"💎 Jumlah Simpanan: RM {total_simpanan:,.2f}")

save_data(data)
st.markdown("</div>", unsafe_allow_html=True)

# =============================
# HUTANG
# =============================
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("📉 Hutang")

hutang_baru = st.text_input("Tambah hutang")
if st.button("➕ Tambah Hutang"):
    if hutang_baru.strip():
        data["hutang"][hutang_baru] = 0.0
        save_data(data)

total_hutang = 0
for h in data["hutang"]:
    nilai = st.number_input(
        f"RM {h}",
        min_value=0.0,
        step=10.0,
        value=data["hutang"][h],
        key=f"hutang_{h}"
    )
    data["hutang"][h] = nilai
    total_hutang += nilai

save_data(data)

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
