import streamlit as st
from src.agent.state import VideoScriptDraft, StaticAdDraft, EvaluationReport


def display_video_script(script: VideoScriptDraft):
    """Menampilkan skrip video dengan format yang rapi."""
    st.subheader("📹 Skrip Iklan Video")

    # Basic info
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Platform", script.ad_platform_target.replace('_', ' ').title())
    with col2:
        st.metric("Durasi", f"{script.duration_estimate_seconds}s")
    with col3:
        st.metric("Adegan", len(script.scenes))

    st.markdown("---")

    # Scenes
    st.subheader("🎬 Adegan")
    for scene in script.scenes:
        with st.expander(f"Scene {scene.scene_number} ({scene.duration_seconds}s)", expanded=True):
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**Deskripsi Visual:**")
                st.write(scene.visual_description)

                if scene.on_screen_text:
                    st.markdown("**Teks di Layar:**")
                    st.info(scene.on_screen_text)

            with col2:
                st.markdown("**Deskripsi Audio:**")
                st.write(scene.audio_description)

                if scene.voiceover_dialogue:
                    st.markdown("**Sulih Suara/Dialog:**")
                    st.write(scene.voiceover_dialogue)

    # CTA and hashtags
    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🎯 Ajakan Bertindak")
        st.success(script.call_to_action_text)

    with col2:
        st.subheader("🏷️ Hashtag yang Disarankan")
        hashtag_text = " ".join([f"#{tag}" for tag in script.suggested_hashtags])
        st.code(hashtag_text)

    # Key takeaway
    st.subheader("💡 Poin Penting")
    st.info(script.key_takeaway)


def display_static_script(script: StaticAdDraft):
    """Menampilkan skrip iklan statis dengan format yang rapi."""
    st.subheader("📱 Skrip Iklan Statis")

    # Basic info
    st.metric("Platform", script.ad_platform_target.replace('_', ' ').title())

    st.markdown("---")

    # Main content
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("📝 Salinan Iklan")

        st.markdown("**Judul:**")
        st.markdown(f"# {script.headline}")

        st.markdown("**Isi:**")
        st.write(script.body_copy)

        st.markdown("**Ajakan Bertindak:**")
        st.success(script.call_to_action_text)

    with col2:
        st.subheader("🖼️ Elemen Visual")

        st.markdown("**Deskripsi Gambar:**")
        st.write(script.image_description)

        if script.on_image_text:
            st.markdown("**Teks pada Gambar:**")
            st.info(script.on_image_text)

        st.markdown("**Hashtag:**")
        hashtag_text = " ".join([f"#{tag}" for tag in script.suggested_hashtags])
        st.code(hashtag_text)

    # Key takeaway
    st.markdown("---")
    st.subheader("💡 Poin Penting")
    st.info(script.key_takeaway)


def display_evaluation_scores(evaluation: EvaluationReport):
    """Menampilkan skor evaluasi dengan format yang rapi."""
    st.subheader("📊 Evaluasi Kualitas")

    # Overall score
    col1, col2 = st.columns([1, 2])
    with col1:
        score_color = "green" if evaluation.overall_score >= 4.0 else "orange" if evaluation.overall_score >= 3.0 else "red"
        st.metric("Skor Keseluruhan", f"{evaluation.overall_score:.1f}/5.0")

    with col2:
        approval_status = "✅ Disetujui" if evaluation.is_approved_for_next_stage else "🔄 Perlu Penyempurnaan"
        st.success(approval_status) if evaluation.is_approved_for_next_stage else st.warning(approval_status)

    st.markdown("---")

    # Detailed scores
    st.subheader("📋 Skor Terperinci")

    # Create score grid
    criteria_items = list(evaluation.detailed_scores.items())
    num_cols = 2

    for i in range(0, len(criteria_items), num_cols):
        cols = st.columns(num_cols)

        for j, col in enumerate(cols):
            if i + j < len(criteria_items):
                criterion, metric = criteria_items[i + j]

                with col:
                    # Score with color coding
                    score = metric.score
                    score_color = "🟢" if score >= 4 else "🟡" if score >= 3 else "🔴"

                    st.markdown(f"**{criterion.value.replace('_', ' ').title()}**")
                    st.markdown(f"{score_color} {score}/5")

                    with st.expander("Lihat Umpan Balik"):
                        st.write(metric.feedback)

    # Summary feedback
    st.markdown("---")
    st.subheader("📝 Umpan Balik Ringkasan")
    st.info(evaluation.summary_feedback)

    # Recommendations
    if evaluation.actionable_recommendations:
        st.subheader("🔧 Rekomendasi")
        for i, rec in enumerate(evaluation.actionable_recommendations, 1):
            st.write(f"{i}. {rec}")


def display_iteration_history(history):
    """Menampilkan riwayat iterasi skrip."""
    if not history:
        st.info("Tidak ada riwayat iterasi tersedia.")
        return

    st.subheader("🔄 Riwayat Penyempurnaan")

    for i, entry in enumerate(history):
        with st.expander(f"Iteration {i + 1} - {entry.get('timestamp', 'Unknown time')}"):
            if 'previous_evaluation_report' in entry:
                prev_eval = entry['previous_evaluation_report']
                st.write(f"**Skor Sebelumnya:** {prev_eval.get('overall_score', 'N/A')}/5.0")

                if 'actionable_recommendations' in prev_eval:
                    st.write("**Rekomendasi yang Diterapkan:**")
                    for rec in prev_eval['actionable_recommendations']:
                        st.write(f"• {rec}")
