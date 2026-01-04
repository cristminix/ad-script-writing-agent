# Import libraries
import os
import json
import yaml
from typing import List, Optional, Dict
from langchain_core.messages import SystemMessage, HumanMessage, BaseMessage

from src.agent.state import AgentState
from src.agent.prompts import (audience_insight_system_prompt , creative_strategy_system_prompt,
                               script_generation_system_prompt, script_evaluation_system_prompt,
                               script_refinement_system_prompt, variation_generation_system_prompt)


def format_list(items: Optional[List[str]]) -> str:
    if not items:
        return "[not specified]"
    return "\n    - " + "\n    - ".join(items)


def format_dict_as_list(d: Dict[str, str]) -> str:
    if not d:
        return "[not specified]"
    return "\n    - " + "\n    - ".join([f"{k}: {v}" for k, v in d.items()])


def read_yaml_from_parent(filename):
    """
    Membaca dan mengurai file YAML yang terletak satu direktori di atas lokasi skrip.

    Args:
        filename (str): Nama file YAML (misalnya, 'your_file.yaml').

    Returns:
        dict or list: Konten yang telah diurai dari file YAML.
    """
    yaml_path = "/projects/ad_script_writing_agent/src/agent/copywriting_guideline.yaml"

    with open(yaml_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

guideline = read_yaml_from_parent('copywriting_guideline.yaml')

def build_audience_insight_message(state: AgentState) -> List[BaseMessage]:
    a = state.audience_persona
    p = state.product

    user_content_string = f"""\
### Profil Target Audiens  ###
{json.dumps(a.model_dump(), indent=2)}

### Detail Produk ###
{json.dumps(p.model_dump(), indent=2)}
"""

    return [
        SystemMessage(content=audience_insight_system_prompt),
        HumanMessage(content=user_content_string.strip())
    ]


def build_creative_strategy_message(state: AgentState) -> List[BaseMessage]:
    p = state.product
    a = state.audience_persona
    ai = state.audience_insight
    guideline = read_yaml_from_parent('copywriting_guideline.yaml')
    preferred_hook_examples = [
        "Kamera ponsel Anda sekarang menjadi koki pribadi Anda. Begini caranya.",
        "Bagaimana jika Anda bisa mengubah INI [tunjukkan foto hidangan lezat dengan keju dan lemak] menjadi makanan yang ramah penurunan berat badan ANDA?"
        "Bosan dengan resep yang mengabaikan alergi dan tujuan kebugaran Anda?",
        "Lelah dengan makanan yang tidak sesuai dengan diet Anda?",
        "Masih mencari ide makan malam 'keto, bebas kacang'? Tonton ini...",
        "Baru selesai latihan dan lapar? Biarkan aplikasi ini memilih makan malam Anda sambil Anda mendingin.",
        "Berpusing-pusing mencari hidangan yang pas dengan diet Anda?",
        "Lelah dengan persiapan makanan yang membosankan? Lihat bagaimana saya membuat keinginan saya bekerja untuk tujuan saya!",
        "Bagaimana jika Anda bisa makan INI dan tetap mencapai tujuan kebugaran Anda?",
        "Pernahkah Anda berharap bisa mengambil foto dan mendapatkan resep sehat yang dibuat untuk tujuan Anda?"
    ]
    preferred_cta_examples = [
        "Unduh Delisio dan personalisasi makanan Anda!"
        "Ketuk untuk membuat resep pertama Anda yang dipersonalisasi.",
        "Dapatkan Delisio dan selesaikan makan malam malam ini.",
        "Instal Delisio dan mulai memasak lebih pintar",
        "Instal dan ubah foto makanan apa pun menjadi hidangan ter-sehat Anda.",
        "Dapatkan koki pribadi AI Anda. Ketuk untuk menginstal sekarang!",
        "Unduh Delisio hari ini dan ambil alih perjalanan memasak sehat Anda."
        "Unduh Delisio dan masak lebih pintar dalam hitungan menit.",
    ]

    # Create a clean demographic profile by excluding redundant fields
    demographic_profile = {
        "age_range": a.age_range,
        "gender": a.gender.value,
        "location": [c.value for c in a.location],
        "income_range": a.income_range.value,
        "education_level": a.education_level.value if a.education_level else 'Not specified'
    }

    # Prepare a dictionary for the campaign brief and audience insights
    campaign_and_insights_dict = {
        "campaign_brief": {
            "campaign_goal": state.campaign_goal.value,
            "ad_platform": state.ad_platform.value,
            "creative_direction": state.creative_direction.value,
            "script_tone": state.script_tone,
            "product_details": {
                "name": p.product_name,
                "overview": p.product_description,
                "focused_feature": {
                    "name": state.product_feature_focus,
                    "description": p.product_features.get(state.product_feature_focus)
                },
                "unique_selling_points": p.unique_selling_point,
                "problems_solved": p.problems_solved,
                "supported_platforms": [sp.value for sp in p.supported_platforms]
            }
        },
        "demographic_profile": demographic_profile,
        "detailed_audience_insights": ai.model_dump(),
        "preferred_hook_examples": preferred_hook_examples,
        "preferred_cta_examples": preferred_cta_examples
    }

    # Use json.dumps to format the structured data for the LLM
    structured_data_str = json.dumps(campaign_and_insights_dict, indent=2)

    # Combine the structured data with the guidelines
    user_content_string = f"""\
    ### Brief Kampanye dan Wawasan Audiens ###
    {structured_data_str}

    ### Pedoman Copywriting Reels ###
    {yaml.dump(guideline, sort_keys=False)}

    ---
    Hasilkan strategi kreatif JSON berdasarkan informasi di atas.
    """

    return [
        SystemMessage(content=creative_strategy_system_prompt),
        HumanMessage(content=user_content_string.strip())
    ]


def build_script_generation_message(state: AgentState) -> List[BaseMessage]:
    p = state.product
    a = state.audience_persona
    ai = state.audience_insight
    guideline = read_yaml_from_parent('copywriting_guideline.yaml')

    # Prepare a single, comprehensive dictionary for all inputs
    inputs_dict = {
        "campaign_brief": {
            "campaign_goal": state.campaign_goal.value,
            "ad_platform": state.ad_platform.value,
            "creative_direction": state.creative_direction.value,
            "script_tone": state.script_tone.value,
            "product_details": {
                "name": p.product_name,
                "overview": p.product_description,
                "focused_feature": {
                    "name": state.product_feature_focus,
                    "description": p.product_features.get(state.product_feature_focus)
                },
                "unique_selling_points": p.unique_selling_point,
                "problems_solved": p.problems_solved,
                "supported_platforms": [sp.value for sp in p.supported_platforms]
            }
        },
        "creative_strategy": {
            "core_message_pillars": state.core_message_pillars,
            "brainstormed_hooks": state.brainstormed_hooks,
            "generated_ctas": state.generated_ctas,
            "emotional_triggers": state.emotional_triggers,
            "primary_visual_concept": state.primary_visual_concept,
            "audio_strategy": state.audio_strategy
        },
        "audience_insights": {
            "demographic_profile": {
                "age_range": a.age_range,
                "gender": a.gender.value,
                "location": [c.value for c in a.location],
                "income_range": a.income_range.value,
                "education_level": a.education_level.value if a.education_level else 'Not specified'
            },
            "detailed_insights": ai.model_dump()
        }
    }

    # Use json.dumps to format the entire dictionary
    structured_data_str = json.dumps(inputs_dict, indent=2)

    user_content_string = f"""\
    ### Ad Campaign Inputs ###
    {structured_data_str}

    ### Reels Copywriting Guideline ###
    {yaml.dump(guideline, sort_keys=False)}

    ---
    Hasilkan strategi kreatif JSON berdasarkan informasi di atas.
    """

    return [
        SystemMessage(content=script_generation_system_prompt),
        HumanMessage(content=user_content_string.strip())
    ]


def build_evaluation_message(state: AgentState) -> List[BaseMessage]:
    # Pre-check: Ensure script_draft exists before evaluation
    if not state.script_draft:
        raise ValueError("Script draft is missing for evaluation.")

    # Create a list of history entries for JSON serialization
    history_list = []
    if state.script_iteration_history:
        for entry in state.script_iteration_history:
            history_list.append({
                "timestamp": entry.get("timestamp", "N/A"),
                "recommendations_given": entry.get("previous_evaluation_report", {}).get("actionable_recommendations",
                                                                                         []),
                "script_produced_key_takeaway": entry.get("output_refined_script", {}).get("key_takeaway"),
                "script_produced_cta": entry.get("output_refined_script", {}).get("call_to_action_text"),
                # You can add more refined script details here if needed
            })

    # Prepare a single, comprehensive dictionary for all inputs
    evaluation_inputs_dict = {
        "campaign_brief": {
            "campaign_goal": state.campaign_goal.value,
            "ad_platform": state.ad_platform.value,
            "creative_direction": state.creative_direction.value,
            "script_tone": state.script_tone.value,
        },
        "product_details": {
            "name": state.product.product_name,
            "overview": state.product.product_description,
            "focused_feature": {
                "name": state.product_feature_focus,
                "description": state.product.product_features.get(state.product_feature_focus)
            },
            "unique_selling_points": state.product.unique_selling_point,
            "problems_solved": state.product.problems_solved,
        },
        "creative_strategy": {
            "core_message_pillars": state.core_message_pillars,
            "brainstormed_hooks": state.brainstormed_hooks,
            "generated_ctas": state.generated_ctas,
            "emotional_triggers": state.emotional_triggers,
        },
        "audience_insights": {
            "demographic_profile": {
                "age_range": state.audience_persona.age_range,
                "gender": state.audience_persona.gender.value,
                "location": [c.value for c in state.audience_persona.location],
                "income_range": state.audience_persona.income_range.value,
                "education_level": state.audience_persona.education_level.value if state.audience_persona.education_level else 'Not specified'
            },
            "detailed_insights": state.audience_insight.model_dump()
        },
        "script_refinement_history": history_list
    }

    # Use json.dumps to format the entire dictionary
    structured_data_str = json.dumps(evaluation_inputs_dict, indent=2)

    # Load the copywriting guidelines
    guideline = read_yaml_from_parent('copywriting_guideline.yaml')

    # Construct the final user message string
    user_content_string = f"""\
### Evaluation Context ###
{structured_data_str}

### Reels Copywriting Guideline ###
{yaml.dump(guideline, sort_keys=False)}

---
### Skrip untuk Dievaluasi (Versi Saat Ini) ###
Berikut adalah skrip iklan yang dihasilkan atau diperbaiki untuk ditinjau. Analisis berdasarkan semua konteks di atas, dan kriteria evaluasi yang disediakan dalam prompt sistem Anda.

```json
{state.script_draft.model_dump_json(indent=2)}
"""

    return [
        SystemMessage(content=script_evaluation_system_prompt),
        HumanMessage(content=user_content_string.strip())
    ]


def build_script_refinement_message(state: AgentState) -> List[BaseMessage]:
    # Ensure evaluation report exists before proceeding
    if not state.evaluation_report:
        raise ValueError("Evaluation Report is missing. Cannot build refinement message.")

    # Create a clean list of history entries for JSON serialization
    history_list = []
    if state.script_iteration_history:
        for entry in state.script_iteration_history:
            history_list.append(entry)

    # Create a clean demographic profile
    a = state.audience_persona
    demographic_profile = {
        "age_range": a.age_range,
        "gender": a.gender.value,
        "location": [c.value for c in a.location],
        "income_range": a.income_range.value,
        "education_level": a.education_level.value if a.education_level else 'Not specified'
    }

    # Prepare a single, comprehensive dictionary for all inputs
    refinement_inputs_dict = {
        "campaign_brief": {
            "campaign_goal": state.campaign_goal.value,
            "ad_platform": state.ad_platform.value,
            "creative_direction": state.creative_direction.value,
            "script_tone": state.script_tone.value,
        },
        "product_details": {
            "name": state.product.product_name,
            "overview": state.product.product_description,
            "focused_feature": {
                "name": state.product_feature_focus,
                "description": state.product.product_features.get(state.product_feature_focus)
            },
            "unique_selling_points": state.product.unique_selling_point,
            "problems_solved": state.product.problems_solved,
        },
        "creative_strategy": {
            "core_message_pillars": state.core_message_pillars,
            "brainstormed_hooks": state.brainstormed_hooks,
            "generated_ctas": state.generated_ctas,
            "emotional_triggers": state.emotional_triggers,
        },
        "audience_insights": {
            "demographic_profile": demographic_profile,
            "detailed_insights": state.audience_insight.model_dump()
        },
        "script_refinement_history": history_list,
        "current_script_draft": state.script_draft.model_dump(),
        "evaluation_feedback": state.evaluation_report.model_dump()
    }

    # Use json.dumps to format the entire dictionary
    structured_data_str = json.dumps(refinement_inputs_dict, indent=2)

    # Load the copywriting guidelines
    guideline = read_yaml_from_parent('copywriting_guideline.yaml')

    # Construct the final user message string
    user_content_string = f"""\
### Refinement Context ###
{structured_data_str}

### Reels Copywriting Guideline ###
{yaml.dump(guideline, sort_keys=False)}

---
Berdasarkan konteks di atas dan rekomendasi spesifik dalam bidang `evaluation_feedback`, hasilkan skrip iklan yang diperbaiki sebagai objek JSON.
"""
    return [
        SystemMessage(content=script_refinement_system_prompt),
        HumanMessage(content=user_content_string.strip())
    ]

def build_variation_generation_message(state: AgentState) -> List[BaseMessage]:
    # Ensure the script draft has been finalized or approved
    if not state.script_draft:
        raise ValueError("No approved script draft available for variation generation.")

    # Create a clean demographic profile
    a = state.audience_persona
    demographic_profile = {
        "age_range": a.age_range,
        "gender": a.gender.value,
        "location": [c.value for c in a.location],
        "income_range": a.income_range.value,
        "education_level": a.education_level.value if a.education_level else 'Not specified'
    }

    # Prepare a single, comprehensive dictionary for all inputs
    variation_inputs_dict = {
        "campaign_brief": {
            "campaign_goal": state.campaign_goal.value,
            "ad_platform": state.ad_platform.value,
            "creative_direction": state.creative_direction.value,
            "script_tone": state.script_tone.value,
        },
        "product_details": {
            "name": state.product.product_name,
            "overview": state.product.product_description,
            "focused_feature": {
                "name": state.product_feature_focus,
                "description": state.product.product_features.get(state.product_feature_focus)
            },
            "unique_selling_points": state.product.unique_selling_point,
            "problems_solved": state.product.problems_solved,
        },
        "audience_insights": {
            "demographic_profile": demographic_profile,
            "detailed_insights": state.audience_insight.model_dump()
        },
        "approved_base_script": state.script_draft.model_dump(),
    }

    # Use json.dumps to format the entire dictionary
    structured_data_str = json.dumps(variation_inputs_dict, indent=2)

    user_content_string = f"""\
### Ad Campaign Context ###
{structured_data_str}

---
Berdasarkan skrip yang disetujui di atas, konteks kampanye, dan wawasan audiens, hasilkan 3 varian berbeda yang dioptimalkan untuk pengujian A/B.
"""
    return [
        SystemMessage(content=variation_generation_system_prompt),
        HumanMessage(content=user_content_string.strip())
    ]
