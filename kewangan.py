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
st.caption("Urus perlahan-lahan, yang penting konsisten 🌱")

# =============================
# BARANG NAK BELI
# =============================
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("🛒 Barang Nak Beli")

with st.form("form_barang", clear_on_submit=True):
    barang_baru = st.text_input("Tambah barang")
    if st.form_submit_button("➕ Tambah"):
        if barang_baru:
            data["barang"].append(barang_baru)
            save_data(data)

if data["barang"]:
    buang = []
    for i, b in enumerate(data["barang"]):
        col1, col2 = st.columns([4, 1])
        col1.write(b)
        if col2.checkbox("Sudah", key=f"barang_{i}"):
            buang.append(b)
    for b in buang:
        data["barang"].remove(b)
        save_data(data)
else:
    st.info("Tiada barang")

st.markdown("</div>", unsafe_allow_html=True)

# =============================
# SIMPANAN
# =============================
st.markdown("<div class='card money'>", unsafe_allow_html=True)
st.subheader("🏦 Simpanan")

simpanan_bank = ["Ambank", "CIMB", "Maybank", "Tabung Haji", "Bank Islam"]
total_simpanan = 0

for bank in simpanan_bank:
    if bank != "Maybank":
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
        f"RM Baris {i+1}",
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

st.success(f"Jumlah Maybank: RM {jumlah_maybank:,.2f}")
total_simpanan += jumlah_maybank

save_data(data)

st.success(f"💎 Jumlah Simpanan Keseluruhan: RM {total_simpanan:,.2f}")
st.markdown("</div>", unsafe_allow_html=True)

# =============================
# HUTANG
# =============================
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("📉 Hutang")

hutang_baru = st.text_input("Tambah hutang")
if st.button("➕ Tambah Hutang"):
    if hutang_baru:
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

st.caption("✨ Kecil tak apa. Asal istiqamah.")
