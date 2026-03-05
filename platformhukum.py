import streamlit as st
from groq import Groq
import PyPDF2 # Buat baca teks dari PDF

# Setup API Groq
# Pastiin baris ini tertulis lengkap seperti ini:
api_key_groq = st.secrets['GROQ_API_KEY']
client = Groq(api_key=api_key_groq)

st.set_page_config(page_title="Legal Partner AI", layout="wide")

# Inisialisasi State agar pilihan tidak hilang saat refresh
if "mode" not in st.session_state:
    st.session_state.mode = None

# --- MENU UTAMA ---
if st.session_state.mode is None:
    st.title("⚖️ Selamat Datang di Legal Partner")
    st.subheader("Pilih metode interaksi lo hari ini, dher:")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📚 Belajar Interaktif (Mata Kuliah)"):
            st.session_state.mode = "belajar"
            st.rerun()
    with col2:
        if st.button("📄 Bedah Berkas (Analisis PDF)"):
            st.session_state.mode = "bedah"
            st.rerun()

# --- FUNGSI RESET MENU ---
if st.sidebar.button("🏠 Kembali ke Menu Utama"):
    st.session_state.mode = None
    st.session_state.messages = [] # Reset chat
    st.rerun()

# ---------------------------------------------------------
# FUNGSI 1: BELAJAR INTERAKTIF
# ---------------------------------------------------------
if st.session_state.mode == "belajar":
    st.title("📖 Mode Belajar Interaktif")
    matkul = st.selectbox("Pilih Mata Kuliah:", ["Hukum Pidana", "Hukum Perdata", "HTN", "Filsafat Hukum"])
    
    st.write(f"Sistem: 'Oke bro, kita bahas **{matkul}**. Lo mau mulai dari bab mana?'")
    
    # [Logika Chat Groq di sini...]
if st.session_state.mode == "belajar":
    st.title(f"📖 Belajar {matkul}")
    st.write(f"Sistem: 'Halo bro, gue asisten hukum lo. Kita bedah **{matkul}** secara tajam ya.'")

    # 1. Inisialisasi Memori Chat (Biar AI inget obrolan sebelumnya)
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": f"Lo adalah asisten ahli hukum yang provokatif dan cerdas. Lo sedang menemani mahasiswa diskusi mata kuliah {matkul}. Gunakan logika hukum yang kuat, hubungkan dengan sejarah (Sapiens) atau taktik (Robert Greene) jika relevan. Selalu akhiri jawaban dengan pertanyaan yang memancing logika user."}
        ]

    # 2. Tampilin History Chat
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # 3. Input Chat dari User
    if prompt := st.chat_input("Tanya materi atau minta AI jelasin bab tertentu..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # 4. Panggil Groq buat Jawab
        with st.chat_message("assistant"):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile", # Model paling pinter di Groq
                messages=st.session_state.messages,
            )
            full_response = response.choices[0].message.content
            st.markdown(full_response)
        
        st.session_state.messages.append({"role": "assistant", "content": full_response})

# ---------------------------------------------------------
# FUNGSI 2: BEDAH BERKAS (PDF)
# ---------------------------------------------------------
elif st.session_state.mode == "bedah":
    st.title("🔍 Mode Bedah Berkas PDF")
    uploaded_file = st.file_uploader("Upload PDF (Putusan/Materi):", type="pdf")
    
    if uploaded_file:
        # Ekstrak teks dari PDF
        reader = PyPDF2.PdfReader(uploaded_file)
        text_pdf = ""
        for page in reader.pages:
            text_pdf += page.extract_text()
            
        st.success("PDF Berhasil dibaca!")
        
        # Tanya user mau fokus ke mana
     # --- MULAI COPY DARI SINI ---
        fokus = st.text_input("Apa yang mau lo bedah dari PDF ini? (Contoh: Amar putusan, Pertimbangan Hakim, atau Celah Hukum)")
        
        if st.button("Mulai Bedah"):
            if fokus:
                prompt_bedah = f"Berikut adalah teks dari PDF: {text_pdf[:4000]}... \n\n Pertanyaan: {fokus}"
                with st.spinner("Sabar bro, lagi dibedah..."):
                    try:
                        response = client.chat.completions.create(
                            model="llama-3.3-70b-versatile",
                            messages=[{"role": "user", "content": prompt_bedah}]
                        )
                        st.markdown("### Hasil Analisis:")
                        st.write(response.choices[0].message.content)
                    except Exception as e:
                        st.error(f"Ada masalah koneksi ke Groq nih dher: {e}")
            else:
                st.warning("Kasih tau dulu dher apa yang mau dibedah!")
           








