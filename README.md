# Agen Penulisan Iklan (Ads Copywriting Agent)

> Tujuan utama proyek ini adalah mengotomatisasi pembuatan konten iklan media sosial yang berkualitas tinggi dan efektif.

Dalam penulisan iklan berbasis AI, LLM tentu dapat membantu, namun respons mereka hampir **tidak pernah siap untuk diterapkan di dunia nyata pada percobaan pertama**. Saya berusaha mengatasi ini dengan membuat orkestrasi canggih dari berbagai LLM. Sistem ini secara strategis merencanakan, melakukan brainstorming, menulis, dan mengoreksi konten, memastikan kualitas dan efektivitas tercapai secara otomatis. Tujuannya adalah membuat AI lebih efisien untuk pembuatan konten pemasaran media sosial.

---

## Daftar Isi

- [Orkestrasi Sistem](#orkestrasi-sistem)
- [Prasyarat](#prasyarat)
- [Instalasi](#instalasi)
- [Masalah dan Keterbatasan yang Diketahui](#masalah-dan-keterbatasan-yang-diketahui)

---

## Orkestrasi Sistem

Dalam sistem multi-agent ini, proses kompleks penulisan iklan yang efektif telah dimodularisasi. Dengan menetapkan setiap langkah kepada LLM yang berbeda, kita dapat memiliki kendali lebih besar atas proses penalaran dan kreatif. Orkestrasi strategis ini memastikan standar kualitas yang lebih tinggi dan output yang lebih andal dibandingkan dengan model tunggal yang umum. Alur kerja disusun sebagai berikut:

![Diagram Alur Kerja](diagram/graph_diagram.png)

1.  **Pengumpulan Input:** Pengguna memberikan detail kampanye yang penting, termasuk:

    - **Tujuan kampanye**
    - **Platform iklan**
    - **Detail produk:** nama, deskripsi, fitur, unique selling points, dan masalah yang dipecahkan oleh produk
    - **Target audiens:** rentang usia, gender, lokasi, rentang pendapatan, pendidikan, gaya hidup, pain points, dan aspirasi menggunakan produk
    - **Pendekatan kreatif:** sudut pesan untuk iklan
    - **Nada skrip**

2.  **Node Wawasan Audiens (Market Researcher):** Node ini berperan sebagai **peneliti pasar** dan **profiler audiens** ahli. Tanggung jawab utamanya adalah **mensintesis** input awal pengguna untuk menciptakan pemahaman audiens yang lebih mendalam dan dapat ditindaklanjuti. Node ini melampaui demografi sederhana untuk menyimpulkan psikografi mereka, termasuk rutinitas harian, perilaku online, nilai inti, dan proses pengambilan keputusan.

3.  **Node Strategi Kreatif (Marketing Strategist):** Berperan sebagai **Marketing Strategist** dan **Creative Director** yang terampil, node ini mengambil wawasan audiens yang mendalam dan detail kampanye untuk membangun rencana kreatif yang komprehensif. Tugas utamanya adalah mengubah data mentah menjadi strategi iklan yang dapat ditindaklanjuti. Node ini mendefinisikan pilar pesan inti, melakukan brainstorming untuk hook, menghasilkan CTA yang menarik, dan mengidentifikasi pemicu emosional spesifik yang akan digunakan dalam iklan. Output strategis ini berfungsi sebagai cetak biru untuk node berikutnya, memastikan salinan iklan akhir memiliki tujuan dan selaras dengan tujuan pemasaran.

4.  **Node Generasi Skrip (Ad Scriptwriter):** Node ini beroperasi sebagai **Scriptwriter** ahli. Perannya adalah mengambil cetak biru strategis dari node sebelumnya dan input awal pengguna untuk menghasilkan skrip iklan lengkap yang siap digunakan. Output node ini bersifat kondisional berdasarkan platform iklan: menghasilkan skrip video terperinci, adegan demi adegan, untuk platform dinamis (seperti Instagram Reels atau TikTok) dan salinan teks singkat dengan detail gambar untuk platform statis (seperti Facebook atau Instagram feed). Node ini memastikan konten akhir disesuaikan dengan platform, nada, dan strategi kreatif tertentu, termasuk pesan kunci, hook, dan CTA.

5.  **Node Evaluasi Skrip (Ad Script Evaluator):** Node ini berfungsi sebagai **Ad Script Evaluator**. Peran utamanya adalah menilai draf skrip yang dihasilkan terhadap semua input sebelumnya, termasuk brief kampanye asli, strategi kreatif, dan wawasan audiens yang terperinci. Evaluasi ini memberikan skor pada skrip berdasarkan berbagai kriteria seperti **efektivitas hook**, **kejelasan**, **daya tarik emosional**, dan **kepatuhan platform**. Tanggung jawab inti node ini adalah menentukan apakah skrip siap untuk tahap selanjutnya dari alur kerja. Jika skrip tidak memenuhi standar kualitas tinggi (misalnya, skor terlalu rendah), node ini memberikan umpan balik dan rekomendasi yang sangat spesifik dan dapat ditindaklanjuti dalam format "ubah INI menjadi ITU". Umpan balik ini dirancang sebagai panduan langsung untuk node berikutnya, memastikan skrip dapat direvisi hingga mencapai kualitas siap produksi.

6.  **Node Penyempurnaan Skrip (Ad Script Refiner):** Node ini adalah **Ad Script Refiner** ahli. Tujuan tunggalnya adalah mengambil skrip dan umpan balik yang dapat ditindaklanjuti dari **Node Evaluasi Skrip** dan meningkatkannya secara iteratif. Node ini beroperasi dengan logika "ubah INI menjadi ITU", dengan teliti mengimplementasikan rekomendasi yang tepat yang diberikan untuk meningkatkan kualitas skrip. Node ini berfokus secara eksklusif pada revisi, bukan pada generasi kreatif baru. Node ini secara langsung memodifikasi konten skrip—seperti teks tubuh, teks di layar, atau deskripsi visual—hingga memenuhi standar tinggi untuk persetujuan akhir, memastikan output akhir adalah skrip iklan yang dipoles dan siap produksi.

---

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
