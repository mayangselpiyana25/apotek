import streamlit as st
import pandas as pd
from datetime import datetime
import os
import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_FILE)
    df.columns = df.columns.str.strip()
    return df

@st.cache_data
def load_riwayat():
    return pd.read_csv(RIWAYAT_FILE)

# File utama dan riwayat pengeluaran
DATA_FILE = 'apotekpj.xlsx'
RIWAYAT_FILE = 'riwayat_pengeluaran.xlsx'

# Buat file utama jika belum ada
if not os.path.exists(DATA_FILE):
    df_init = pd.DataFrame(columns=[
        "No", "Kode_barang", "Nama_barang", "Stok_awal", "Satuan_obat", "Tanggal_Kadaluarsa", "Harga"
    ])
    df_init.to_excel(DATA_FILE, index=False)

# Buat file riwayat pengeluaran jika belum ada
if not os.path.exists(RIWAYAT_FILE):
    df_riwayat = pd.DataFrame(columns=[
        "Tanggal", "Kode_barang", "Nama_barang", "Jumlah_keluar", "Tanggal_Kadaluarsa_batch", "Harga"
    ])
    df_riwayat.to_excel(RIWAYAT_FILE, index=False)

# Fungsi load dan save
def load_data():
    df = pd.read_excel(DATA_FILE)
    df.columns = df.columns.str.strip()
    return df

def save_data(df):
    df.to_excel(DATA_FILE, index=False)

def load_riwayat():
    return pd.read_excel(RIWAYAT_FILE)

def save_riwayat(df):
    df.to_excel(RIWAYAT_FILE, index=False)

# CSS Tema Merah Estetik
st.markdown("""
    <style>
        .main { background-color: #fffafa; }

        .stButton>button {
            background-color: #e60000;
            color: white;
            border-radius: 8px;
            font-weight: bold;
        }

        .stButton>button:hover {
            background-color: #990000;
            color: white;
        }

        h1, h2, h3 {
            color: #990000;
        }

        [data-testid="stSidebar"] {
            background-color: #fff0f0;
        }

        [data-testid="stSidebar"] .block-container {
            padding-top: 1rem;
        }

        [data-testid="stSidebar"] .stRadio label {
            padding: 10px 16px;
            background-color: #fff5f5;
            border: 2px solid #e60000;
            border-radius: 8px;
            color: #333;
            font-weight: 500;
            transition: all 0.2s ease;
            margin-bottom: 8px;
            width: 100%;
            display: flex;
            gap: 8px;
        }

        [data-testid="stSidebar"] .stRadio label:has(input:checked) {
            background-color: #e60000;
            color: white;
            border: 2px solid #990000;
            font-weight: bold;
        }

        [data-testid="stSidebar"] .stRadio input {
            display: none;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("Menu Utama")
menu = st.sidebar.radio("", [
    "Halaman Utama",
    "Update Stok",
    "Pengeluaran Obat (FIFO)",
    "Cek Stok",
    "Riwayat Distribusi",
    "Analisis SCM"
])
# =====================Halaman Utama=====================
if menu == "Halaman Utama":
    st.markdown("<h1 style='color:#990000; text-align:center;'>SELAMAT DATANG DI APOTEK <br> RISA FARMA</h1>", unsafe_allow_html=True)
    st.image("apotek.jpg", use_container_width=True, caption="Apotek Risa Farma - Solusi Kesehatan Anda")

    st.markdown("""
    <div >
        <p style="font-size:17px; text-align:justify;">
        Sistem ini dirancang untuk mempermudah pengelolaan obat di Apotek Risa Farma, 
        dengan metode <strong>FIFO (First-In First-Out)</strong> dan pendekatan <strong>Supply Chain Management (SCM)</strong>. 
        Anda dapat melakukan input obat baru, mencatat pengeluaran obat, melihat riwayat distribusi, 
        serta menganalisis kebutuhan stok secara efisien dan real-time.
        </p>
        <p style="font-size:16px; font-style:italic; text-align:right; margin-top:30px;">
        -- Tim Digital Apotek Risa Farma
        </p>
    </div>
    """, unsafe_allow_html=True)

#=================Halaman Update Stok=====================
elif menu == "Update Stok":
    st.markdown(
    "<h1 style='color:#990000; text-align:center;'>Update Stok</h1>",
    unsafe_allow_html=True)
    df = load_data()

    # Siapkan daftar pilihan kode obat
    if not df.empty:
        daftar_kode = df[["Kode_barang", "Nama_barang"]].drop_duplicates()
        daftar_kode["Label"] = daftar_kode["Kode_barang"] + " - " + daftar_kode["Nama_barang"]
        kode_pilihan = daftar_kode["Label"].tolist()
    else:
        kode_pilihan = []

    # ✅ Panduan tampil di atas form
    st.markdown("""
    <div style='background-color:#f9f9f9; padding:10px; border-left:5px solid #0c6cf2;'>
        <b>Panduan Pengisian Data Obat:</b><br>
        • Pastikan semua kolom terisi dengan lengkap dan benar.<br>
        • Isi harga hanya dalam angka akan ditambahkan otomatis.<br>
        • Tanggal kadaluarsa wajib diisi sesuai tanggal resmi.<br>
        • Untuk data baru, isi kode dan nama obat secara unik.
    </div>
    """, unsafe_allow_html=True)

    kode_pilihan.append("Tambahkan Kode Baru")
    pilih_kode = st.selectbox("Pilih Kode Obat:", kode_pilihan)

    # Input kode baru atau ambil dari pilihan
    if pilih_kode == "Tambahkan Kode Baru":
        kode_barang = st.text_input("Masukkan Kode Barang Baru")
        nama_barang = st.text_input("Masukkan Nama Obat Baru")
        satuan_obat = st.text_input("Masukkan Satuan Obat Baru")
    else:
        kode_barang = pilih_kode.split(" - ")[0]
        nama_barang = pilih_kode.split(" - ")[1]
        satuan_obat_value = df.loc[df["Kode_barang"] == kode_barang, "Satuan_obat"].iloc[0]
        satuan_obat = st.text_input("Satuan Obat", value=satuan_obat_value, disabled=True)

    # Form input data
    with st.form("form_obat"):
        stok_awal = st.number_input("Stok Awal", min_value=1)
        tgl_kadaluarsa = st.date_input("Tanggal Kadaluwarsa")
        harga_nominal = st.number_input("Harga (dalam Rupiah, tanpa IDR)", min_value=0, step=100)

        submitted = st.form_submit_button("Masukkan")

        if submitted:
            if not kode_barang or not nama_barang:
                st.warning("Kode dan Nama Obat harus diisi.")
            elif pilih_kode == "Tambahkan Kode Baru" and (not satuan_obat or satuan_obat.strip() == ""):
                st.warning("Satuan Obat harus diisi.")
            elif harga_nominal == 0:
                st.warning("Harga tidak boleh kosong atau nol.")
            else:
                df = load_data()
                no_baru = 1 if df.empty else int(df["No"].max()) + 1
                new_data = pd.DataFrame({
                    "No": [no_baru],
                    "Kode_barang": [kode_barang],
                    "Nama_barang": [nama_barang],
                    "Stok_awal": [stok_awal],
                    "Satuan_obat": [satuan_obat],
                    "Tanggal_Kadaluarsa": [tgl_kadaluarsa],
                    "Harga": [harga_nominal]
                })
                df = pd.concat([df, new_data], ignore_index=True)
                save_data(df)

                if pilih_kode == "Tambahkan Kode Baru":
                    st.success(f"Obat **{nama_barang}** berhasil ditambahkan sebagai **data baru** dengan kode **{kode_barang}**.")
                else:
                    st.success(f"Obat **{nama_barang}** berhasil ditambahkan sebagai **stok tambahan** untuk kode **{kode_barang}**.")

#==================Pengeluaran Obat FIFO====================
elif menu == "Pengeluaran Obat (FIFO)":
    st.markdown(
        "<h1 style='color:#990000; text-align:center;'>Pengeluaran Obat (Metode FIFO)</h1>",
        unsafe_allow_html=True)

    df = load_data()
    df["Tanggal_Kadaluarsa"] = pd.to_datetime(df["Tanggal_Kadaluarsa"], errors='coerce')

    # Gabungkan Kode + Nama untuk dropdown
    df_kode_nama = df[["Kode_barang", "Nama_barang"]].drop_duplicates()
    df_kode_nama["Label"] = df_kode_nama["Kode_barang"] + " - " + df_kode_nama["Nama_barang"]
    kode_list = df_kode_nama["Label"].tolist()

    pilih_label = st.selectbox("Pilih Kode Obat:", kode_list)
    kode_terpilih = pilih_label.split(" - ")[0]
    nama_terpilih = pilih_label.split(" - ")[1]

    # Filter FIFO
    df_fifo = df[df["Kode_barang"] == kode_terpilih].sort_values("Tanggal_Kadaluarsa")

    if not df_fifo.empty:
        satuan = df_fifo["Satuan_obat"].iloc[0]
        harga = df_fifo["Harga"].iloc[0]
        tgl_kadaluarsa_terdekat = df_fifo["Tanggal_Kadaluarsa"].iloc[0]

        # Tampilkan info otomatis (readonly style)
        st.text_input("Nama Obat", value=nama_terpilih, disabled=True)
        st.text_input("Satuan Obat", value=satuan, disabled=True)
        st.date_input("Tanggal Kadaluarsa Terdekat", value=tgl_kadaluarsa_terdekat, disabled=True)
        st.number_input("Harga per Satuan", value=float(harga), step=100.0, disabled=True)

    jumlah_keluar = st.number_input("Jumlah Keluar", min_value=1)

    if st.button("Keluarkan"):
        keluar_log = []
        sisa = jumlah_keluar

        for i, row in df_fifo.iterrows():
            if sisa <= 0:
                break

            stok = row["Stok_awal"]
            ambil = min(sisa, stok)

            df.at[i, "Stok_awal"] -= ambil

            keluar_log.append({
                "Tanggal": datetime.now(),
                "Kode_barang": row["Kode_barang"],
                "Nama_barang": row["Nama_barang"],
                "Jumlah_keluar": ambil,
                "Tanggal_Kadaluarsa_batch": row["Tanggal_Kadaluarsa"],
                "Harga": row["Harga"]
            })

            sisa -= ambil

        if sisa > 0:
            st.warning("Stok tidak mencukupi.")
        else:
            save_data(df)

            df_log = pd.DataFrame(keluar_log)
            riwayat = load_riwayat()
            riwayat = pd.concat([riwayat, df_log], ignore_index=True)
            save_riwayat(riwayat)

            total_biaya = sum(int(str(item["Harga"]).replace("IDR", "")) * item["Jumlah_keluar"] for item in keluar_log)

            st.success("Obat berhasil dikeluarkan sesuai FIFO.")
            st.info(f"Total biaya pengeluaran: IDR{total_biaya:,}")


#==================Cek Stok========================
elif menu == "Cek Stok":
    st.markdown(
        "<h1 style='color:#990000; text-align:center;'>Cek Stok</h1>",
        unsafe_allow_html=True
    )

    # Keterangan warna
    st.markdown("""
    <p style='font-weight:bold; margin-bottom: 8px;'>Keterangan Warna Status Obat:</p>

    <p>Berikut adalah arti warna yang digunakan untuk menunjukkan status kadaluarsa obat agar memudahkan pemantauan:</p>

    <table style='border-collapse: collapse; width: 100%;'>
    <tr style='border: none;'>
        <td style='color:blue; font-weight:bold; padding: 4px 10px; border: none;'>🔵 Aman</td>
        <td style='padding: 4px 10px; border: none;'>: Tanggal kadaluarsa masih lebih dari 30 hari ke depan.</td>
    </tr>
    <tr style='border: none;'>
        <td style='color:orange; font-weight:bold; padding: 4px 10px; border: none;'>🟠 Mendekati Kadaluarsa</td>
        <td style='padding: 4px 10px; border: none;'>: Tanggal kadaluarsa dalam 30 hari ke depan.</td>
    </tr>
    <tr style='border: none;'>
        <td style='color:red; font-weight:bold; padding: 4px 10px; border: none;'>🔴 Sudah Kadaluarsa</td>
        <td style='padding: 4px 10px; border: none;'>: Tanggal kadaluarsa sudah lewat atau hari ini.</td>
    </tr>
    </table>

    <p style='margin-top: 8px;'>Mohon perhatikan warna status untuk memastikan pengelolaan stok obat tetap optimal dan aman digunakan.</p>
    """, unsafe_allow_html=True)

    df = load_data()
    df["Tanggal_Kadaluarsa"] = pd.to_datetime(df["Tanggal_Kadaluarsa"], errors='coerce', dayfirst=True)
    today = pd.to_datetime(datetime.now().date())
    soon_expired = today + pd.Timedelta(days=30)

    def status_kadaluarsa(x):
        if pd.isna(x):
            return "Tidak ada tanggal"
        elif x <= today:  # Diperbaiki agar hari ini juga dianggap kadaluarsa
            return "Sudah Kadaluarsa"
        elif x <= soon_expired:
            return "Mendekati Kadaluarsa"
        else:
            return "Aman"

    df["Status"] = df["Tanggal_Kadaluarsa"].apply(status_kadaluarsa)

    def color_status(val):
        if val == "Sudah Kadaluarsa":
            return 'color: red; font-weight: bold;'
        elif val == "Mendekati Kadaluarsa":
            return 'color: orange; font-weight: bold;'
        elif val == "Aman":
            return 'color: blue; font-weight: bold;'
        else:
            return 'color: gray;'

    styled_df = df.style.applymap(color_status, subset=["Status"])
    st.dataframe(styled_df)

# ==============Riwayat Distribusi===================
elif menu == "Riwayat Distribusi":
    st.markdown(
    "<h1 style='color:#990000; text-align:center;'>Riwayat Pengeluaran Obat</h1>",
    unsafe_allow_html=True
)
    riwayat = load_riwayat()
    riwayat["Tanggal"] = pd.to_datetime(riwayat["Tanggal"])
    st.dataframe(riwayat.sort_values("Tanggal", ascending=False))

# ===================Analisis SCM=====================
elif menu == "Analisis SCM":
    st.markdown("""
    <h1 style="color:#990000; text-align:center;">Analisis Kebutuhan dan Penggunaan Obat</h1>
    """, unsafe_allow_html=True)

    st.markdown("""
    <p style='text-align: justify'>
    Halaman ini menampilkan analisis stok obat berdasarkan sisa stok, jumlah penggunaan (barang keluar), serta status safety stok. Jika stok di bawah 50, sistem akan memberikan peringatan untuk segera diajukan ke supplier.
    </p>
    """, unsafe_allow_html=True)

    # Load data
    df = load_data()
    riwayat = load_riwayat()

    # Gabung data stok dan riwayat keluar
    df_group = df.groupby("Kode_barang")["Stok_awal"].sum().reset_index(name="Stok_Barang")
    riwayat_group = riwayat.groupby("Kode_barang")["Jumlah_keluar"].sum().reset_index(name="Barang_Keluar")

    analisis = pd.merge(df_group, riwayat_group, on="Kode_barang", how="outer").fillna(0)

    analisis["Barang_Keluar"] = analisis["Barang_Keluar"].astype(int)
    analisis["Stok_Barang"] = analisis["Stok_Barang"].astype(int)
    analisis["Jumlah_Barang"] = analisis["Stok_Barang"] + analisis["Barang_Keluar"]

    # Ambil nama barang
    nama_obat = df[["Kode_barang", "Nama_barang"]].drop_duplicates()
    analisis = pd.merge(analisis, nama_obat, on="Kode_barang", how="left")

    # Tambahkan kolom Safety Stok
    analisis["Safety_Stok"] = analisis["Stok_Barang"].apply(
        lambda x: "Ajukan ke Supplier" if x < 50 else "Stok Aman"
    )

    # Tambahkan nomor urut
    analisis.insert(0, "No", range(1, len(analisis) + 1))

    # Urutkan kolom
    cols = ["No", "Kode_barang", "Nama_barang", "Stok_Barang", "Barang_Keluar", "Jumlah_Barang", "Safety_Stok"]
    analisis = analisis[cols]

    # Tampilkan tabel
    st.dataframe(analisis)
