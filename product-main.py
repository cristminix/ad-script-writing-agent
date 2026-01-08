import sys
import os 
import dotenv


from src.agent.state import (
    AgentState, Product, AudiencePersona, AudienceInsight, 
    CampaignGoal, AdPlatform, CreativeDirection, ScriptTone,
    Gender, Countries, IncomeRange, EducationLevel, SupportedPlatform
)
from src.agent.utils import build_audience_insight_message

def main():
    # Memuat variabel lingkungan dari file .env
    dotenv.load_dotenv()

    # Membuat objek Product
    product = Product(
        product_name="TechFix Pro",
        product_description="Jasa servis komputer profesional yang menyediakan perbaikan, pemeliharaan, dan dukungan teknis untuk semua jenis perangkat komputer dan laptop.",
        product_features={
            "Hardware Repair": "Perbaikan komponen keras seperti motherboard, RAM, hard drive, dan layar",
            "Software Troubleshooting": "Pemecahan masalah sistem operasi, driver, dan aplikasi",
            "Data Recovery": "Pemulihan data penting dari perangkat yang rusak atau mengalami kegagalan"
        },
        supported_platforms=[SupportedPlatform.desktop],
        unique_selling_point=[
            "Teknisi bersertifikat dengan pengalaman lebih dari 5 tahun",
            "Garansi perbaikan hingga 3 bulan",
            "Layanan antar-jemput gratis untuk wilayah Jakarta dan sekitarnya"
        ],
        problems_solved=[
            "Komputer lambat atau sering crash",
            "Gangguan perangkat keras seperti layar pecah atau keyboard rusak",
            "Kehilangan data penting akibat kerusakan perangkat"
        ]
    )

    # Membuat objek AudiencePersona
    audience_persona = AudiencePersona(
        # SIAPA mereka (usia, gender, lokasi)
        age_range="25-50",
        gender=Gender.all,
        location=[Countries.indonesia, Countries.usa, Countries.canada],
        income_range=IncomeRange.middle,
        education_level=EducationLevel.some_college,
        # BAGAIMANA mereka hidup
        lifestyle=["pengguna teknologi", "profesional sibuk", "menghargai efisiensi waktu"],
        # APA masalah mereka
        pain_points=[
            "Komputer yang lambat atau bermasalah",
            "Kehilangan data penting karena kerusakan perangkat",
            "Tidak memiliki waktu untuk memperbaiki perangkat sendiri"
        ],
        #  APA yang mereka inginkan
        aspiration=["memiliki perangkat yang berfungsi optimal", "menghemat waktu dengan layanan profesional", "mendapatkan solusi teknologi yang andal"]
    )

    # Membuat objek AgentState
    state = AgentState(
        campaign_goal=CampaignGoal.leads,
        ad_platform=AdPlatform.instagram_feeds,
        product=product,
        product_feature_focus="Hardware & Software Repair",
        audience_persona=audience_persona,
        creative_direction=CreativeDirection.testimonial,
        script_tone=ScriptTone.trustworthy,
        # audience_insight akan diisi oleh audience_insight_node
    )

    # Contoh pembuatan graph langgraph manual hanya dengan audience_insight_node
    from langgraph.graph import StateGraph, START, END
    from src.agent.nodes.audience_insight import audience_insight_node

    # Membuat graph dengan hanya audience_insight_node
    builder = StateGraph(AgentState)
    builder.add_node("audience_insight_node", audience_insight_node)
    builder.add_edge(START, "audience_insight_node")
    builder.add_edge("audience_insight_node", END)

    # Compile graph
    graph = builder.compile()

    # Menjalankan graph dengan state awal
    result = graph.invoke(state)

    # Menampilkan hasil dari graph
    print("Manual graph execution completed!")
    print(f"Final state contains audience insight: {'audience_insight' in result and result['audience_insight'] is not None}")
    print(f"Total tokens used: {result.get('total_llm_tokens', 0)}")

    # Jika ingin melihat hasil audience insight
    if 'audience_insight' in result and result['audience_insight']:
        print("\nAudience Insight Generated:")
        print(f"Common Interests: {result['audience_insight'].common_interests}")
        print(f"Media Consumption: {result['audience_insight'].media_consumption_habits}")
        print(f"Pain Points: {result['audience_insight'].elaborated_pain_points}")


if __name__ == "__main__":
    main()
