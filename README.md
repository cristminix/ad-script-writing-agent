# Agen Penulisan Iklan (Ads Copywriting Agent)

> Tujuan utama proyek ini adalah mengotomatisasi pembuatan konten iklan media sosial yang berkualitas tinggi dan efektif.

Dalam penulisan iklan berbasis AI, LLM tentu dapat membantu, namun respons mereka hampir **tidak pernah siap untuk diterapkan di dunia nyata pada percobaan pertama**. Saya berusaha mengatasi ini dengan membuat orkestrasi canggih dari berbagai LLM. Sistem ini secara strategis merencanakan, melakukan brainstorming, menulis, dan mengoreksi konten, memastikan kualitas dan efektivitas tercapai secara otomatis. Tujuannya adalah membuat AI lebih efisien untuk pembuatan konten pemasaran media sosial.

[Baca Artikel di medium](https://medium.com/me/stats/post/05712e3a0a46?statsForAllStoriesUrl=https%3A%2F%2Fmedium.com%2Fme%2Fstats&source=stats_homepage--------------------------------------------)

## Prasyarat

- **Python 3.11+**
- **Git**
- **Kunci API Gemini atau OpenAI**: Proyek ini bergantung pada kunci API dari model **Gemini** milik Google dan **GPT** milik OpenAI. Jika Anda hanya memiliki salah satu kunci ini, Anda dapat mengedit kode di dalam `src/agent/nodes` untuk menggunakan model pilihan Anda untuk setiap node.\*\*\*

## Instalasi

Untuk menyiapkan dan menjalankan proyek Anda, Anda perlu mengikuti beberapa langkah sederhana.

1.  **Clone repositori:**

    ```bash
    git clone https://github.com/cristminix/ad-script-writing-agent
    cd ad-script-writing-agent
    ```

2.  **Instal dependensi:**
    Anda perlu menginstal semua pustaka Python yang diperlukan.

    ```bash
    pip install -r requirements.txt
    ```

3.  **Siapkan variabel lingkungan:**
    Proyek ini memerlukan berbagai kunci API dan pengaturan konfigurasi. Anda harus membuat file `.env` dan mengisinya dengan kunci pribadi Anda.

    ```bash
    cp .env.example .env
    ```

    Buka file `.env` yang baru dibuat dan ganti nilai placeholder dengan kunci API aktual Anda. Anda perlu memberikan kunci API dari Google dan OpenAI untuk menjalankan aplikasi. Atau Anda dapat mengubah kode di dalam `src/agent/nodes` untuk menggunakan model pilihan Anda untuk setiap node.

4.  **Jalankan aplikasi:**
    Aplikasi berjalan melalui antarmuka web Streamlit. Gunakan perintah berikut untuk memulainya.
    ```bash
    streamlit run app.py
    ```
    Setelah perintah dijalankan, tab baru akan terbuka di browser Anda yang menunjukkan aplikasi.

---

## Masalah dan Keterbatasan yang Diketahui

> **Status MVP**: Sistem ini saat ini berada dalam tahap MVP (Minimum Viable Product) dan **belum siap produksi**. Beberapa peningkatan arsitektur diperlukan sebelum menerapkannya di lingkungan produksi.

### 1. Implementasi Human-in-the-Loop Manual

**Masalah Saat Ini**: Fungsi human-in-the-loop diimplementasikan secara manual, bukan menggunakan kemampuan API native LangGraph.

**Masalah**: Pendekatan ini kurang memiliki ketangguhan dan fitur persistensi yang disediakan oleh sistem `interrupt()` dan `Command` bawaan LangGraph, termasuk status eksekusi persisten dan titik integrasi yang fleksibel.

**Pendekatan yang Lebih Baik**: Implementasi pola human-in-the-loop native LangGraph menggunakan:

- `interrupt()` untuk pemberhentian dinamis berdasarkan skor kualitas skrip
- `Command(resume=...)` untuk alur kerja persetujuan/penolakan manusia
- Interupsi statis (`interrupt_before`/`interrupt_after`) pada node kunci seperti Script Evaluation

### 2. Masalah Loop Penyempurnaan Tak Terbatas

**Masalah Saat Ini**: Proses penyempurnaan otomatis sering masuk ke dalam loop tak terbatas di mana LLM terus-menerus menyempurnakan skrip tanpa mencapai ambang batas kualitas yang dapat diterima.

**Solusi Sementara Saat Ini**: Batas keras 3 siklus tinjauan, yang sering menghasilkan kualitas output suboptimal.

**Keterbatasan Pendekatan Saat Ini**:

- Skrip mungkin masih di bawah kualitas produksi setelah 3 iterasi
- Tidak ada mekanisme untuk intervensi manusia ketika penyempurnaan otomatis gagal
- Membuang sumber daya komputasi pada siklus penyempurnaan yang tidak produktif

**Solusi yang Diusulkan** (Memerlukan Penelitian):

- **Penyesuaian ambang batas adaptif**: Menurunkan ambang batas kualitas setelah setiap iterasi yang gagal
- **Eskalasi manusia**: Memicu human-in-the-loop ketika siklus penyempurnaan melebihi 2 iterasi
- **Pendekatan multi-model**: Beralih ke model LLM yang berbeda untuk penyempurnaan setelah upaya gagal
- **Pemeriksaan kesamaan semantik**: Menghentikan penyempurnaan ketika perubahan menjadi minimal antar iterasi

### 3. Kesenjangan Kesiapan Produksi

**Area Tambahan yang Memerlukan Pengembangan**:

- **Penanganan kesalahan**: Mekanisme pemulihan kesalahan terbatas untuk kegagalan API
- **Optimalisasi kinerja**: Tidak ada caching atau pemrosesan paralel untuk pembuatan beberapa kampanye
- **Validasi kualitas**: Kurang kerangka kerja pengujian komprehensif untuk penilaian kualitas output
- **Skalabilitas**: Arsitektur saat ini tidak mendukung sesi pengguna bersamaan secara efektif

### 4. Peluang Penelitian

<details>
<summary>Area untuk Pengembangan Masa Depan</summary>

**Integrasi Human-in-the-Loop**: Mengimplementasi pola `interrupt` LangGraph untuk alur kerja persetujuan, khususnya pada tahap Script Evaluation.

**Optimalisasi Penyempurnaan**: Mengembangkan kriteria penghentian yang lebih cerdas dan algoritma penilaian kualitas untuk mencegah loop tak terbatas sambil mempertahankan standar output tinggi.

**Metrik Kualitas**: Penelitian ke dalam sistem penilaian kualitas otomatis yang lebih baik berkorelasi dengan evaluasi manusia terhadap efektivitas salinan iklan.

</details>
