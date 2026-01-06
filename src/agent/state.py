"""
Mendefinisikan model Pydantic dan enumerasi untuk merepresentasikan kampanye, produk, audiens, dan state alur kerja dalam
sistem generasi kampanye iklan.

Author: Peyman Kh
Last Edit: 27-07-2025
"""
# Import libraries
import json
from enum import Enum
from datetime import datetime
from typing import Dict, List, Optional, Union
from pydantic import BaseModel, Field, field_validator


class CampaignGoal(str, Enum):
    """
    Enumerasi dari berbagai tujuan yang mungkin untuk kampanye iklan.
    """
    awareness = 'awareness'
    traffic = 'traffic'
    engagement = 'engagement'
    leads = 'leads'
    app_installs = 'app_installs'


class AdPlatform(str, Enum):
    """
    Enumerasi dari berbagai penempatan iklan spesifik di berbagai platform sosial.
    """
    instagram_reels = 'instagram_reels'
    instagram_stories = 'instagram_stories'
    instagram_feeds = 'instagram_feeds'
    facebook_feeds = 'facebook_feeds'
    facebook_stories = 'facebook_stories'
    youtube_shorts = 'youtube_shorts'
    tiktok_feed = 'tiktok_feed'
    snapchat_spotlight = 'snapchat_spotlight'


class SupportedPlatform(str, Enum):
    """
    Platform mobile yang didukung oleh produk.
    """
    ios = "ios"
    android = "android"
    web="web"


class Product(BaseModel):
    """
    Detail tentang aplikasi yang dipromosikan.
    """
    product_name: str = Field(
        ..., description="nama aplikasi."
    )
    product_description: str = Field(
        ..., description="Ringkasan singkat tentang aplikasi."
    )
    product_features: Dict[str, str] = Field(
        ..., description="Kamus yang memetakan nama fitur ke deskripsi."
    )
    supported_platforms: List[SupportedPlatform] = Field(
        description="Platform yang didukung untuk aplikasi.",
        default_factory=lambda: [SupportedPlatform.ios]
    )
    unique_selling_point: List[str] = Field(
        ..., description="Daftar poin penjualan unik untuk produk."
    )
    problems_solved: List[str] = Field(
        ..., description="Daftar masalah yang dipecahkan oleh produk."
    )


class Gender(str, Enum):
    """
    Opsi identitas gender untuk audiens target.
    """
    male = "pria"
    female = "wanita"
    all = "semua"


class Countries(str, Enum):
    """
    Enumerasi dari negara-negara audiens yang didukung.
    """
    usa = "usa"
    uk = "uk"
    canada = "canada"
    australia = "australia"
    indonesia = "indonesia"


class IncomeRange(str, Enum):
    """
    Kategori kisaran pendapatan untuk segmentasi audiens.
    """
    low = "<$30k"
    lower_middle = "$30k–$60k"
    middle = "$60k–$100k"
    upper_middle = "$100k–$200k"
    high = ">$200k"


class EducationLevel(str, Enum):
    """
    Pencapaian pendidikan tertinggi dari segmen audiens.
    """
    none = "none"
    high_school = "high_school"
    some_college = "some_college"
    bachelors = "bachelors"
    masters = "masters"
    doctorate = "doctorate"


class AudiencePersona(BaseModel):
    """
    Profil terstruktur yang merepresentasikan karakteristik dari audiens target.
    """
    age_range: str = Field(
        ..., description="Rentang usia dari audiens target."
    )
    gender: Gender = Field(
        ..., description="Gender dari audiens target."
    )
    location: List[Countries] = Field(
        ..., description="Daftar negara audiens target."
    )
    income_range: IncomeRange = Field(
        ..., description="Kategori kisaran pendapatan dari audiens target."
    )
    education_level: Optional[EducationLevel] = Field(
        default=None,
        description="Tingkat pendidikan dari audiens target."
    )
    lifestyle: List[str] = Field(
        ..., description="Karakteristik gaya hidup dari audiens target."
    )
    pain_points: List[str] = Field(
        ..., description="Poin-poin utama masalah dan tantangan yang dihadapi oleh audiens."
    )
    aspiration: Optional[List[str]] =  Field(
        default=None,
        description="Apa yang ingin dicapai oleh audiens."
    )


class CreativeDirection(str, Enum):
    """
    Enumerasi dari pendekatan kreatif umum untuk sudut pesan iklan.
    """
    user_generated_content = "user_generated_content"
    problem_solution = "problem_solution"
    testimonial = "testimonial"
    lifestyle = "lifestyle"
    educational = "educational"
    motivational = "motivational"
    product_in_action = "product_in_action"
    gamification = "gamification"
    humor = "humor"
    storytelling = "storytelling"
    day_in_life = "day_in_life"


class ScriptTone(str, Enum):
    """
    Enumerasi dari nada yang dapat diterapkan dalam penulisan skrip untuk konten iklan yang efektif dan menarik.
    """
    friendly = "friendly"                   # Hangat, mudah didekati, dan ramah
    conversational = "conversational"       # Santai dan alami, seperti obrolan pribadi
    authoritative = "authoritative"         # Menunjukkan keahlian dan kepercayaan diri
    energetic = "energetic"                 # Lincah, dinamis, dan bersemangat tinggi
    enthusiastic = "enthusiastic"           # Mengekspresikan semangat dan energi positif
    humorous = "humorous"                   # Menggunakan kecerdasan atau keceriaan untuk keterlibatan
    emotional = "emotional"                 # Menyentuh perasaan (kebahagiaan, empati, dll.)
    inspirational = "inspirational"         # Mengangkat dan memotivasi dengan pesan positif
    motivational = "motivational"           # Mendorong tindakan melalui semangat
    trustworthy = "trustworthy"             # Tulus, dapat dipercaya, dan andal
    sincere = "sincere"                     # Jujur, tulus, dan otentik
    playful = "playful"                     # Seru, hidup, dan kadang-kadang usil
    urgent = "urgent"                       # Menyampaikan sensitivitas waktu untuk merangsang respons cepat
    dramatic = "dramatic"                   # Menggunakan ketegangan atau intensitas untuk dampak
    sophisticated = "sophisticated"         # Halus, dipoles, dan elegan
    professional = "professional"           # Formal, sopan, dan seperti bisnis
    calm = "calm"                           # Lembut, rileks, dan menenangkan
    bold = "bold"                           # Berani dan menarik perhatian
    clever = "clever"                       # Pintar, cerdas, dan inovatif dalam pesan
    reassuring = "reassuring"               # Memberikan kenyamanan dan kepercayaan terhadap produk/brand


class AudienceInsight(BaseModel):
    """
    detail psikografik dan perilaku terstruktur dari persona pengguna
    """
    # Interests & Hobbies (Psychographic)
    common_interests: List[str] = Field(
        ...,
        description="Daftar 3 hobi, minat, dan gairah umum yang masuk akal untuk segmen audiens ini. Bersifat spesifik (misalnya, 'hidup berkelanjutan', 'perbaikan rumah DIY', 'komunitas game online')."
    )

    # Media Consumption Habits (Behavioral)
    media_consumption_habits: List[str] = Field(
        ...,
        description="3 cara utama audiens ini mengonsumsi media, termasuk jenis konten dan platform (misalnya, 'menghabiskan waktu berjam-jam di TikTok menonton konten pendidikan bentuk pendek', 'lebih suka artikel mendalam di blog teknologi', 'mendengarkan podcast selama perjalanan')."
    )

    # Lifestyle & Daily Routine (Psychographic/Behavioral)
    typical_daily_routine_snippets: List[str] = Field(
        ...,
        description="3 deskripsi singkat dari aktivitas harian atau skenario umum yang mendefinisikan gaya hidup mereka (misalnya, 'berangkat kerja di kota sibuk', 'mengatur rumah tangga dan pengasuhan anak', 'bekerja dari rumah')."
    )

    # Core Values & Beliefs (Psychographic)
    core_values_and_beliefs: List[str] = Field(
        ...,
        description="3 nilai atau keyakinan fundamental yang kemungkinan mempengaruhi keputusan dan pandangan dunia mereka (misalnya, 'menghargai stabilitas dan keamanan finansial', 'memprioritaskan keberlanjutan lingkungan', 'percaya pada peningkatan diri berkelanjutan')."
    )

    # Purchasing Behavior & Decision-Making (Behavioral)
    decision_making_factors: List[str] = Field(
        ...,
        description="3 faktor utama yang mempengaruhi keputusan pembelian mereka untuk produk seperti milik Anda (misalnya, 'dipengaruhi oleh ulasan dan rekomendasi rekan', 'mencari nilai untuk uang', 'memprioritaskan kenyamanan dan penghematan waktu', 'loyalitas merek penting')."
    )

    # Preferred Content Formats & Tone (Behavioral)
    preferred_content_formats_and_tone: List[str] = Field(
        ...,
        description="3 jenis konten dan nada yang paling baik mereka respon dalam iklan (misalnya, 'tutorial video pendek yang menarik', 'konten asli yang dibuat pengguna', 'infografik informatif dengan nada profesional')."
    )

    # Elaborated Pain Points & Desired Outcomes (Psychographic/Motivational)
    elaborated_pain_points: List[str] = Field(
        ...,
        description="3 deskripsi lebih terperinci, berbasis skenario dari tantangan dan frustrasi utama mereka terkait masalah yang dipecahkan produk Anda."
    )
    elaborated_aspiration_outcomes: List[str] = Field(
        ...,
        description="3 deskripsi spesifik dan jelas tentang apa yang ingin mereka capai, bagaimana mereka membayangkan kesuksesan, dan manfaat emosionalnya."
    )

    # Brand Perception & Trust (Psychographic/Behavioral)
    how_they_perceive_brands_like_yours: List[str] = Field(
        ...,
        description="3 wawasan tentang bagaimana audiens ini biasanya melihat atau berinteraksi dengan merek di kategori produk Anda (misalnya, 'skeptis terhadap klaim berlebihan', 'mengharapkan layanan pelanggan yang luar biasa', 'mencari bukti sosial')."
    )

    # Unique or Niche Characteristics (Psychographic)
    unique_or_niche_insights: List[str] = Field(
        ...,
        description="2 wawasan unik, tidak jelas, atau ceruk lainnya yang menonjol untuk profil audiens spesifik ini yang mungkin mempengaruhi strategi iklan. Di sinilah LLM benar-benar bisa bersinar."
    )


class Scene(BaseModel):
    """
    Mewakili satu adegan dalam skrip iklan video.
    """
    scene_number: int = Field(..., description="Nomor urut adegan.")
    visual_description: str = Field(..., description="Deskripsi terperinci tentang apa yang harus ditampilkan di layar.")
    audio_description: str = Field(..., description="Deskripsi musik latar, efek suara, atau kebisingan sekitar.")
    on_screen_text: Optional[str] = Field(None, description="Overlay teks yang muncul di layar selama adegan ini.")
    voiceover_dialogue: Optional[str] = Field(None, description="Dialog yang diucapkan oleh seorang narator atau karakter dalam adegan ini.")
    duration_seconds: float = Field(..., description="Durasi perkiraan adegan dalam detik.")


class VideoScriptDraft(BaseModel):
    """
    Representasi terstruktur dari skrip iklan video.
    """
    script_type: str = Field("Video", description="Jenis skrip (misalnya, 'Video').")
    ad_platform_target: str = Field(..., description="Platform iklan spesifik yang dioptimalkan untuk skrip ini.")
    duration_estimate_seconds: float = Field(..., description="Perkiraan durasi total skrip dalam detik.")
    scenes: List[Scene] = Field(
        default_factory=list,
        description="Daftar adegan terstruktur untuk iklan video."
    )
    call_to_action_text: str = Field(..., description="Teks ajakan utama yang akan digunakan.")
    suggested_hashtags: List[str] = Field(
        default_factory=list,
        description="Tagar relevan untuk disertakan dengan postingan iklan."
    )
    key_takeaway: str = Field(..., description="Kalimat ringkas yang merangkum poin utama iklan.")


class StaticAdDraft(BaseModel):
    """
    Representasi terstruktur dari skrip iklan statis (gambar/feed).
    """
    script_type: str = Field("Static", description="Jenis skrip (misalnya, 'Static').")
    ad_platform_target: str = Field(..., description="Platform iklan spesifik yang dioptimalkan untuk skrip ini.")
    headline: str = Field(..., description="Judul utama atau judul primer dari salinan iklan.")
    body_copy: str = Field(..., description="Teks tubuh utama dari salinan iklan.")
    image_description: str = Field(..., description="Deskripsi terperinci dari visual utama iklan.")
    on_image_text: str = Field(..., description="Teks pada gambar")
    call_to_action_text: str = Field(..., description="Teks ajakan utama yang akan digunakan.")
    suggested_hashtags: List[str] = Field(
        default_factory=list,
        description="Tagar relevan untuk disertakan dengan postingan iklan."
    )
    key_takeaway: str = Field(..., description="Kalimat ringkas yang merangkum poin utama iklan.")


ScriptDraft = Union[VideoScriptDraft, StaticAdDraft]


class EvaluationCriterion(str, Enum):
    """
    Kriteria spesifik yang digunakan untuk mengevaluasi skrip iklan.
    """
    hook = "hook"
    clarity = "clarity"
    conciseness = "conciseness"
    emotional_appeal = "emotional_appeal"
    call_to_action_strength = "call_to_action_strength"
    brand_voice_adherence = "brand_voice_adherence"
    platform_compliance = "platform_compliance"
    relevance_to_audience = "relevance_to_audience"
    feature_highlight_effectiveness = "feature_highlight_effectiveness"
    uniqueness_originality = "uniqueness_originality"
    overall_impact = "overall_impact"


class EvaluationMetric(BaseModel):
    """
    Mewakili skor metrik evaluasi tunggal.
    """
    score: int = Field(..., ge=1, le=5, description="Skor untuk kriteria (1=Kurang, 5=Sangat Baik).")
    feedback: str = Field(..., description="Umpan balik spesifik dan konstruktif untuk kriteria ini.")


class EvaluationReport(BaseModel):
    """
    Laporan komprehensif tentang evaluasi skrip iklan, merinci skor dan umpan balik per kriteria.
    """
    overall_score: float = Field(..., ge=1, le=5, description="Skor agregat keseluruhan untuk skrip (1=Kurang, 5=Sangat Baik).")
    detailed_scores: Dict[EvaluationCriterion, EvaluationMetric] = Field(
        ..., description="Kamus yang memetakan setiap kriteria evaluasi ke skor dan umpan balik spesifiknya."
    )
    summary_feedback: str = Field(
        ..., description="Ringkasan ringkas tentang kekuatan skrip dan area yang perlu ditingkatkan."
    )
    actionable_recommendations: List[str] = Field(
        ..., description="Rekomendasi spesifik (misalnya, 'Revisi CTA', 'Perpendek skrip', 'Lanjutkan ke variasi')."
    )
    is_approved_for_next_stage: bool = Field(
        ..., description="Menunjukkan apakah skrip memenuhi ambang batas kualitas untuk melanjutkan (misalnya, ke ulasan manusia atau generasi variasi)."
    )


class VariationRequest(BaseModel):
    """
    Permintaan untuk menghasilkan satu variasi uji A/B dengan perubahan spesifik.
    """
    variation_focus: str = Field(
        ...,
        description="Fokus utama dari variasi ini (misalnya, 'Hook + CTA + Emotional Tone')"
    )
    target_changes: List[str] = Field(
        ...,
        description="Perubahan spesifik yang akan dibuat: modifikasi hook, peningkatan CTA, pergeseran nada emosional"
    )


class SingleVariation(BaseModel):
    """
    Mewakili satu variasi uji A/B yang disempurnakan.
    """
    variation_name: str = Field(..., description="Nama/identifier untuk variasi ini")
    variation_type: str = Field(..., description="Jenis variasi (misalnya, 'Enhanced Hook + CTA + Tone')")
    base_script_comparison: str = Field(..., description="Perbandingan singkat dengan skrip dasar")
    ad_script_variation: ScriptDraft = Field(..., description="Skrip variasi yang disempurnakan")
    variation_evaluation_report: Optional[EvaluationReport] = Field(
        default=None, description="Laporan evaluasi akhir untuk variasi ini"
    )
    variation_iteration_count: int = Field(default=0, description="Jumlah iterasi penyempurnaan")
    notes: Optional[str] = Field(None, description="Catatan tambahan tentang variasi ini")


class AgentState(BaseModel):
    """
    Objek state inti yang dilewatkan antara node alur kerja, menangkap konteks utama untuk generasi kampanye.
    """
    campaign_goal: CampaignGoal = Field(
        ..., description="Tujuan utama kampanye iklan."
    )
    ad_platform: AdPlatform = Field(
        ..., description="Platform iklan yang akan digunakan."
    )
    product: Product = Field(
        ..., description="Detail tentang produk yang dipromosikan."
    )
    product_feature_focus: str = Field(
        ..., description="Fitur mana yang harus menjadi fokus iklan?"
    )
    audience_persona: AudiencePersona = Field(
        ..., description="Profil terperinci dari audiens target yang dimaksud"
    )
    creative_direction: CreativeDirection = Field(
        ..., description="sudut pesan iklan."
    )
    script_tone: ScriptTone = Field(
        ...,
        description="Suara atau nada brand yang diminta untuk skrip iklan."
    )
    # Workflow fields
    audience_insight: Optional[AudienceInsight] = Field(
        default=None,
        description="Detail psikografik dan perilaku dari persona pengguna."
    )
    brainstormed_hooks: Optional[List[str]] = Field(
        default=None,
        description="Daftar ide hook atau baris pembuka yang menarik perhatian yang dihasilkan dari brainstorming untuk skrip."
    )
    generated_ctas: Optional[List[str]] = Field(
        default=None,
        description="Daftar frasa ajakan bertindak yang dihasilkan untuk digunakan dalam skrip iklan."
    )
    core_message_pillars: Optional[List[str]] = Field(
        default=None,
        description="3 pesan paling penting yang harus disampaikan oleh iklan."
    )
    emotional_triggers: Optional[List[str]] = Field(
        default=None,
        description="Emosi spesifik yang akan ditimbulkan pada audiens."
    )
    primary_visual_concept: Optional[str] = Field(
        default=None,
        description="Deskripsi singkat dari gaya visual dan konsep yang direkomendasikan untuk iklan."
    )
    audio_strategy: Optional[str] = Field(
        default=None,
        description="Deskripsi singkat dari strategi audio yang direkomendasikan (misalnya, musik sedang tren, narator)."
    )
    script_draft: Optional[ScriptDraft] = Field(
        default=None,
        description="Draf kerja skrip iklan saat ini, yang dihasilkan atau diperbarui selama alur kerja."
    )
    evaluation_report: Optional[EvaluationReport] = Field(
        default=None,
        description="Laporan rinci berbagai kriteria dari Agen Penilai yang mengevaluasi draf skrip saat ini."
    )
    revision_feedback: Optional[str] = Field(
        default=None,
        description="Umpan balik evaluator atau pemeriksa dengan permintaan revisi spesifik untuk penulis skrip."
    )
    variation_request: Optional[VariationRequest] = Field(
        default=None,
        description="Detail permintaan untuk menghasilkan satu variasi"
    )
    variation_script_draft: Optional[ScriptDraft] = Field(
        default=None,
        description="Draf kerja skrip variasi saat ini"
    )
    variation_evaluation_report: Optional[EvaluationReport] = Field(
        default=None,
        description="Laporan evaluasi untuk skrip variasi"
    )
    variation_iteration_count: int = Field(
        default=0,
        description="Jumlah iterasi penyempurnaan untuk variasi"
    )
    single_variation_result: Optional[SingleVariation] = Field(
        default=None,
        description="Hasil variasi tunggal akhir dengan semua penyempurnaan"
    )
    is_variation_workflow: bool = Field(
        default=False,
        description="Tanda untuk menunjukkan apakah ini adalah alur kerja generasi variasi"
    )
    tool_calls_history: Optional[List[Dict]] = Field(
        default=None,
        description="Catatan kronologis panggilan alat atau agen yang dipanggil selama alur kerja, dengan input/output yang relevan."
    )
    script_iteration_history: Optional[List[Dict]] = Field(
        default=None,
        description="Riwayat iterasi penyempurnaan skrip, termasuk laporan evaluasi sebelumnya dan skrip yang disempurnakan."
    )
    iteration_count: int = Field(
        default=0,
        description="Jumlah iterasi penyempurnaan yang telah dilalui skrip."
    )
    total_llm_tokens: int = Field(
        default=0,
        description="Jumlah total token LLM (input + output) yang digunakan di semua panggilan."
    )
    timestamp: Optional[datetime] = Field(
        default=None,
        description="Timestamp yang menunjukkan kapan AgentState ini terakhir diperbarui atau diproses."
    )
    human_review_decision: Optional[str] = Field(
        default=None,
        description="Keputusan yang dibuat oleh pemeriksa manusia: 'approved', 'minor_revision', atau 'major_rework'."
    )
