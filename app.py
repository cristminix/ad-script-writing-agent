import traceback
import streamlit as st
from datetime import datetime

from src.ui_components.utils import format_enum_value
from src.ui_components.forms import dynamic_list_input
from src.agent.state import (CampaignGoal, AdPlatform, Product, SupportedPlatform,
                             CreativeDirection, ScriptTone, Gender, Countries,
                             IncomeRange, EducationLevel, AudiencePersona, AgentState, )


def initial_input_ui():
    """
    Merender formulir awal untuk pengguna memasukkan detail kampanye.
    """
    st.set_page_config(
        page_title="Generator Skrip Iklan AI",
        layout="wide",
        initial_sidebar_state="collapsed",
        page_icon="🚀"
    )

    # Enhanced CSS with modern design
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Hide sidebar completely */
    section[data-testid="stSidebar"] {display: none !important}
    .css-1d391kg {display: none}
    .css-14xtw13.e8zbici0 {display: none}
    .css-15zrgzn {display: none}
    .css-eczf16 {display: none}
    .css-jn99sy {display: none}
    .css-17ziqus {display: none}
    .css-1rs6os {display: none}
    .css-1lcbmhc {display: none}
    .css-1outpf7 {display: none}

    /* DARK THEME IMPLEMENTATION */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background-color: #0f172a !important;
        color: #e2e8f0 !important;
    }

    /* Main app dark background */
    .stApp {
        background-color: #0f172a !important;
        color: #e2e8f0 !important;
    }

    /* Main container dark background */
    .main .block-container {
        padding-left: 2rem;
        padding-right: 2rem;
        padding-top: 2rem;
        max-width: none;
        background-color: #0f172a !important;
    }

    /* Header styling - Dark theme */
    .main-header {
        text-align: center;
        padding: 2rem 0 3rem 0;
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
        border-radius: 20px;
        margin-bottom: 3rem;
        color: white;
        box-shadow: 0 10px 30px rgba(79, 70, 229, 0.3);
    }

    .main-header h1 {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }

    .main-header p {
        font-size: 1.2rem;
        font-weight: 400;
        opacity: 0.9;
        margin-bottom: 0;
    }

    /* Section cards - Dark theme */
    .section-card {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%) !important;
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
        border: 1px solid #475569;
        transition: all 0.3s ease;
    }

    .section-card:hover {
        box-shadow: 0 8px 30px rgba(79, 70, 229, 0.2);
        transform: translateY(-2px);
        border-color: #4f46e5;
    }

    .section-header {
        display: flex;
        align-items: center;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
    }

    .section-number {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
        color: white;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 600;
        font-size: 1.1rem;
        margin-right: 1rem;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.4);
    }

    .section-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #f1f5f9 !important;
        margin: 0;
    }

    .section-subtitle {
        font-size: 1rem;
        color: #94a3b8 !important;
        margin-top: 0.25rem;
        margin-bottom: 0;
    }

    /* Progress indicator - Dark theme */
    .progress-steps {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 2rem 0;
        padding: 1rem;
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%) !important;
        border-radius: 12px;
        border: 1px solid #475569;
    }

    .step {
        display: flex;
        align-items: center;
        color: #94a3b8;
        font-weight: 500;
    }

    .step.active {
        color: #a855f7;
        font-weight: 600;
    }

    .step-circle {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        background: #64748b;
        margin-right: 0.5rem;
    }

    .step.active .step-circle {
        background: #a855f7;
        box-shadow: 0 0 0 4px rgba(168, 85, 247, 0.2);
    }

    .step-connector {
        width: 50px;
        height: 2px;
        background: #475569;
        margin: 0 1rem;
    }

    /* Form elements - Dark theme */
    .stSelectbox label, .stTextInput label, .stTextArea label, .stMultiSelect label {
        font-weight: 500 !important;
        color: #e2e8f0 !important;
        font-size: 0.95rem !important;
    }

    .stSelectbox > div > div, .stTextInput > div > div, .stTextArea > div > div, .stMultiSelect > div > div {
        border-radius: 8px;
        border: 1.5px solid #475569;
        transition: all 0.2s ease;
        background-color: #334155 !important;
        color: #e2e8f0 !important;
    }

    .stSelectbox > div > div:focus-within, .stTextInput > div > div:focus-within, .stTextArea > div > div:focus-within {
        border-color: #4f46e5;
        box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.2);
    }

    /* Input text color */
    .stSelectbox select, .stTextInput input, .stTextArea textarea {
        color: #e2e8f0 !important;
        background-color: #334155 !important;
    }

    /* Container backgrounds */
    .element-container {
        background-color: transparent !important;
    }

    .stContainer {
        background-color: transparent !important;
    }

    [data-testid="column"] {
        background-color: transparent !important;
    }

    /* Button styling - Dark theme */
    .stButton > button {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%) !important;
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(79, 70, 229, 0.4);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(79, 70, 229, 0.6);
    }

    /* Alert styling - Dark theme */
    .stAlert {
        border-radius: 12px !important;
        border: none !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
    }

    .stAlert[data-baseweb="notification"] {
        background-color: #7f1d1d !important;
        color: #fecaca !important;
        border-left: 4px solid #ef4444 !important;
    }

    .stSuccess {
        background-color: #14532d !important;
        color: #bbf7d0 !important;
        border-left: 4px solid #22c55e !important;
    }

    /* Info boxes - Dark theme */
    .info-box {
        background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%) !important;
        border: 1px solid #3b82f6;
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0;
        color: #dbeafe !important;
    }

    .info-box-icon {
        color: #60a5fa;
        margin-right: 0.5rem;
    }

    /* Divider styling - Dark theme */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, #475569, transparent);
        margin: 3rem 0;
    }

    /* Fix any remaining containers */
    .block-container > div {
        background-color: transparent !important;
    }

    .element-container div {
        background-color: transparent !important;
    }

    /* Text colors for dark theme */
    p, span, div {
        color: #e2e8f0 !important;
    }

    h1, h2, h3, h4, h5, h6 {
        color: #f1f5f9 !important;
    }

    /* Caption text */
    .caption {
        color: #94a3b8 !important;
    }
    
    </style>
    """, unsafe_allow_html=True)

    # Main Header
    st.markdown("""
    <div class="main-header">
        <h1>🚀 Agen Generator Skrip Iklan</h1>
        <p>Ubah ide Anda menjadi skrip iklan media sosial yang konversi tinggi dengan AI canggih</p>
    </div>
    """, unsafe_allow_html=True)

    # --- 1. Campaign & Creative Details ---
    st.markdown("""
    <div class="section-card">
        <div class="section-header">
            <div class="section-number">1</div>
            <div>
                <h2 class="section-title">Detail Kampanye & Iklan</h2>
                <p class="section-subtitle">Tentukan tujuan inti dan platform target untuk iklan Anda</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        col1, col2 = st.columns(2, gap="large")
        with col1:
            st.markdown("**🎯 Tujuan Kampanye**")
            campaign_goal = st.selectbox(
                label="Tujuan Kampanye",
                options=[goal.value for goal in CampaignGoal],
                format_func=format_enum_value,
                help="Tujuan utama dari kampanye iklan ini.",
                label_visibility="collapsed"
            )

            st.markdown("**🎨 Arah Kreatif**")
            creative_direction = st.selectbox(
                label="Arah Kreatif",
                options=[cd.value for cd in CreativeDirection],
                index=[cd.value for cd in CreativeDirection].index(CreativeDirection.user_generated_content.value),
                format_func=format_enum_value,
                help="Sudut pesan atau pendekatan kreatif keseluruhan dari iklan.",
                label_visibility="collapsed"
            )

        with col2:
            st.markdown("**📱 Platform Iklan**")
            ad_platform = st.selectbox(
                label="Platform Iklan",
                options=[platform.value for platform in AdPlatform],
                format_func=format_enum_value,
                help="Penempatan media sosial spesifik untuk iklan.",
                label_visibility="collapsed"
            )

            st.markdown("**🗣️ Nada Skrip**")
            script_tone = st.selectbox(
                label="Nada Skrip",
                options=[st.value for st in ScriptTone],
                index=[st.value for st in ScriptTone].index(ScriptTone.friendly.value),
                format_func=format_enum_value,
                help="Suara merek atau nada yang diminta untuk skrip iklan.",
                label_visibility="collapsed"
            )

    # Info box for campaign section
    st.markdown("""
    <div class="info-box">
        <span class="info-box-icon">💡</span>
        <strong>Tip Profesional:</strong> Pilih platform dan nada yang selaras dengan preferensi audiens target Anda. Konten bergaya UGC biasanya paling baik performanya di Instagram Reels dan TikTok.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # --- 2. Product & Features ---
    st.markdown("""
    <div class="section-card">
        <div class="section-header">
            <div class="section-number">2</div>
            <div>
                <h2 class="section-title">Produk & Fitur</h2>
                <p class="section-subtitle">Berikan detail tentang aplikasi seluler yang ingin Anda iklankan</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        col1, col2 = st.columns([3, 2], gap="large")

        with col1:
            st.markdown("**📱 Nama Produk**")
            product_name = st.text_input(
                label="Nama Produk",
                value="Delisio - Chef Pribadi Anda",
                help="Nama aplikasi Anda.",
                label_visibility="collapsed"
            )

        with col2:
            st.markdown("**🔧 Platform yang Didukung**")
            supported_platforms = st.multiselect(
                label="Platform yang Didukung",
                options=[p.value for p in SupportedPlatform],
                default=[SupportedPlatform.ios.value],
                format_func=format_enum_value,
                help="Pilih semua platform yang didukung aplikasi Anda.",
                label_visibility="collapsed"
            )

        st.markdown("**📝 Deskripsi Produk**")
        product_description = st.text_area(
            label="Deskripsi Produk",
            value="Delisio adalah asisten chef pribadi dan nutrisi. Saat pengguna mendaftar, mereka memasukkan usia, berat badan, tinggi badan, diet (misalnya vegan, keto), tujuan nutrisi (misalnya penurunan berat badan, penambahan otot), alergi, dan tingkat keterampilan memasak. Selanjutnya mereka dapat menggunakan 3 fitur utama, pertama adalah ketika mereka memindai makanan, Delisio akan mempersonalisasi resep makanan yang sehat dan sesuai dengan kebutuhan unik mereka. Kedua adalah 'kejutkan saya' yang membuat resep tak terduga dari masakan atau negara lain yang memenuhi kebutuhan mereka, dan terakhir jika mereka memindai hidangan mereka, mereka dapat melihat detail mendalam tentang makanan seperti kalori, lemak, vitamin C, B12, zat besi, dll.",
            help="Ikhtisar singkat tentang aplikasi Anda.",
            height=100,
            label_visibility="collapsed"
        )

        col_features_left, col_features_right = st.columns(2, gap="large")

        with col_features_left:
            st.markdown("**📋 Fitur Produk**")
            st.caption("Masukkan setiap fitur pada baris baru dengan format: `Nama Fitur: Deskripsi`")
            product_features_raw = st.text_area(
                label="Fitur Produk (Nama: Deskripsi)",
                value="Foto ke Resep: Pengguna mengunggah foto hidangan apa pun, tentukan peralatan, tentukan preferensi kalori, dan Delisio menghasilkan resep yang dipersonalisasi sesuai profil mereka.\n"
                      "Nama ke Resep: Pengguna menulis nama hidangan apa pun, tentukan peralatan, tentukan preferensi kalori, dan Delisio menghasilkan resep yang dipersonalisasi sesuai profil mereka.\n"
                      "Kejutkan Saya: Pengguna memilih jenis makanan, masakan, tentukan peralatan, tentukan preferensi kalori; Delisio menghasilkan resep unik yang dipersonalisasi (misalnya, sarapan vegetarian Cina).\n"
                      "Pemindai Nutrisi: Pengguna memindai makanan mereka; Delisio menganalisis dan melaporkan nutrisi, vitamin, dan mineral.\n"
                      "Pelacak Hidrasi: Menghitung asupan air harian yang diperlukan berdasarkan BMI dan tujuan, dan membantu pengguna melacak asupan air harian mereka.\n",
                height=200,
                label_visibility="collapsed"
            )
            product_features_dict = {}
            for line in product_features_raw.strip().split('\n'):
                if ":" in line:
                    key, value = line.split(":", 1)
                    product_features_dict[key.strip()] = value.strip()

            feature_options = list(product_features_dict.keys())
            if not feature_options:
                feature_options = ["Masukkan fitur di atas terlebih dahulu"]

            st.markdown("**⭐ Fitur yang Difokuskan**")
            product_feature_focus = st.selectbox(
                label="Fitur yang Difokuskan",
                options=feature_options,
                help="Fitur tunggal mana yang harus disorot oleh iklan?",
                label_visibility="collapsed"
            )

        with col_features_right:
            unique_selling_point = dynamic_list_input(
                label="🚀 Poin Penjualan Unik (USP)",
                key="usp_list",
                default_value=[
                    "Ubah gambar makanan apa pun menjadi resep yang dipersonalisasi dan selaras dengan tujuan secara instan.",
                    "Resep yang disesuaikan secara unik dengan metrik tubuh, diet, tujuan, alergi, dan keterampilan memasak pengguna.",
                    "Temukan makanan favorit baru, yang dihasilkan secara unik untuk diet dan selera pengguna.",
                    "Pindai makanan apa pun untuk wawasan nutrisi instan dan mendetail (makro, mikro, vitamin).",
                    "Target air berbasis BMI dengan pelacakan visual yang memotivasi.",
                    "Chef pribadi AI, panduan nutrisi, dan pelacak hidrasi semua dalam satu."
                ]
            )

            problems_solved = dynamic_list_input(
                label="🎯 Masalah yang Dipecahkan",
                key="problems_solved_list",
                default_value=[
                    "Dilema apa yang harus saya masak malam ini",
                    "Kebosanan dengan makanan berulang",
                    "Kesulitan menemukan resep yang sesuai dengan kebutuhan/tujuan diet spesifik",
                    "Ketidakpastian tentang kandungan nutrisi makanan",
                    "Kesulitan menjaga hidrasi yang memadai",
                    "Keterbatasan waktu untuk memasak sehat",
                    "Kurangnya kepercayaan diri di dapur",
                    "Saran kesehatan generik yang tidak cocok"
                ]
            )

    st.markdown("<hr>", unsafe_allow_html=True)

    # --- 3. Audience Profile ---
    st.markdown("""
    <div class="section-card">
        <div class="section-header">
            <div class="section-number">3</div>
            <div>
                <h2 class="section-title">Profil Audiens Target</h2>
                <p class="section-subtitle">Bantu AI memahami kepada siapa Anda berbicara dengan persona yang detail</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        # Demographics row
        col1, col2, col3 = st.columns(3, gap="large")

        with col1:
            st.markdown("**👥 Rentang Usia**")
            age_range = st.text_input(
                label="Rentang Usia",
                value="25-33",
                help="Contoh: '25-33' atau '18+'.",
                label_visibility="collapsed"
            )

            st.markdown("**⚧️ Jenis Kelamin**")
            gender = st.selectbox(
                label="Jenis Kelamin",
                options=[g.value for g in Gender],
                format_func=format_enum_value,
                help="Jenis kelamin audiens target.",
                label_visibility="collapsed"
            )

        with col2:
            st.markdown("**🌍 Lokasi**")
            location = st.multiselect(
                label="Lokasi",
                options=[c.value for c in Countries],
                default=[Countries.usa.value, Countries.uk.value, Countries.canada.value],
                format_func=format_enum_value,
                help="Negara-negara audiens target.",
                label_visibility="collapsed"
            )

            st.markdown("**💰 Rentang Penghasilan**")
            options_income = [i.value for i in IncomeRange]
            income_range = st.selectbox(
                label="Rentang Penghasilan",
                options=options_income,
                index=options_income.index(IncomeRange.middle.value),
                help="Kategori penghasilan audiens.",
                label_visibility="collapsed"
            )

        with col3:
            st.markdown("**🎓 Tingkat Pendidikan**")
            education_level = st.selectbox(
                label="Tingkat Pendidikan",
                options=[e.value for e in EducationLevel],
                help="Tingkat pendidikan tertinggi audiens.",
                label_visibility="collapsed"
            )

        st.markdown("<br>", unsafe_allow_html=True)

        # Psychographics row
        col_lifestyle, col_painpoints, col_aspirations = st.columns(3, gap="large")

        with col_lifestyle:
            lifestyle = dynamic_list_input(
                label="🏃‍♀️ Kata Kunci Gaya Hidup",
                key="lifestyle_list",
                default_value=["gym", "makan sehat", "diet"]
            )

        with col_painpoints:
            pain_points = dynamic_list_input(
                label="😤 Titik Nyeri",
                key="pain_points_list",
                default_value=["Melihat foto hidangan di media sosial tetapi tidak memiliki resepnya"]
            )

        with col_aspirations:
            aspiration = dynamic_list_input(
                label="✨ Aspirasi",
                key="aspirations_list",
                default_value=[""]
            )

    # Info box for audience section
    st.markdown("""
    <div class="info-box">
        <span class="info-box-icon">🎯</span>
        <strong>Wawasan Audiens:</strong> Semakin spesifik Anda tentang gaya hidup, titik nyeri, dan aspirasi audiens Anda, semakin tertarget dan efektif skrip iklan Anda.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # Generate Button Section
    st.markdown("""
    <div class="section-card" style="text-align: center; background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);">
        <h3 style="color: #1e293b; margin-bottom: 1rem;">🚀 Siap Menghasilkan Skrip Iklan Anda?</h3>
        <p style="color: #64748b; margin-bottom: 2rem;">Agen AI kami akan menganalisis masukan Anda dan membuat skrip iklan profesional yang dioptimalkan untuk platform dan audiens Anda.</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚀 Mulai Generasi Skrip Iklan!", type="primary", use_container_width=True):
        # Validation function
        def validate_inputs():
            errors = []
            if not product_name.strip():
                errors.append("Nama produk diperlukan")
            if not product_description.strip():
                errors.append("Deskripsi produk diperlukan")
            if not product_features_dict:
                errors.append("Setidaknya satu fitur produk diperlukan")
            if not unique_selling_point or not any(usp.strip() for usp in unique_selling_point):
                errors.append("Setidaknya satu poin penjualan unik diperlukan")
            if not problems_solved or not any(prob.strip() for prob in problems_solved):
                errors.append("Setidaknya satu masalah yang dipecahkan diperlukan")
            if not lifestyle or not any(life.strip() for life in lifestyle):
                errors.append("Setidaknya satu item gaya hidup diperlukan")
            if not pain_points or not any(pain.strip() for pain in pain_points):
                errors.append("Setidaknya satu titik nyeri diperlukan")
            if not location:
                errors.append("Setidaknya satu lokasi harus dipilih")
            if not supported_platforms:
                errors.append("Setidaknya satu platform yang didukung harus dipilih")

            return errors

        # Validate inputs
        validation_errors = validate_inputs()

        if validation_errors:
            st.error("🚨 Harap perbaiki kesalahan berikut sebelum melanjutkan:")
            for error in validation_errors:
                st.write(f"• {error}")
        else:
            try:
                with st.spinner("🔄 Mempersiapkan data kampanye Anda..."):
                    # Create the Product object
                    product = Product(
                        product_name=product_name,
                        product_description=product_description,
                        product_features=product_features_dict,
                        supported_platforms=[SupportedPlatform(p) for p in supported_platforms],
                        unique_selling_point=[usp for usp in unique_selling_point if usp.strip()],
                        problems_solved=[prob for prob in problems_solved if prob.strip()]
                    )

                    # Create the AudiencePersona object
                    audience_persona = AudiencePersona(
                        age_range=age_range,
                        gender=Gender(gender),
                        location=[Countries(c) for c in location],
                        income_range=IncomeRange(income_range),
                        education_level=EducationLevel(education_level) if education_level != "none" else None,
                        lifestyle=[life for life in lifestyle if life.strip()],
                        pain_points=[pain for pain in pain_points if pain.strip()],
                        aspiration=[asp for asp in aspiration if asp.strip()] if aspiration and any(
                            aspiration) else None
                    )

                    # Create the complete AgentState object
                    agent_state = AgentState(
                        campaign_goal=CampaignGoal(campaign_goal),
                        ad_platform=AdPlatform(ad_platform),
                        product=product,
                        product_feature_focus=product_feature_focus,
                        audience_persona=audience_persona,
                        creative_direction=CreativeDirection(creative_direction),
                        script_tone=ScriptTone(script_tone),
                        timestamp=datetime.now()
                    )

                    # Store in session state
                    st.session_state['agent_state'] = agent_state
                    st.session_state['workflow_status'] = 'ready'

                st.success("✅ Kampanye berhasil dikonfigurasi! Mengalihkan ke pemrosesan AI...")

                # Navigate to processing page
                st.switch_page("pages/processing.py")

            except Exception as e:
                st.error(f"❌ Kesalahan membuat status alur kerja: {str(e)}")
                with st.expander("🔍 Lihat kesalahan detail"):
                    st.code(traceback.format_exc())


if __name__ == "__main__":
    initial_input_ui()
