# Data Collection for Civil Servant Student Candidate Selection (2023)

## Deskripsi

Aplikasi ini dibuat untuk mengekstrak data dari file PDF hasil seleksi calon mahasiswa kedinasan tahun 2023. Pengguna dapat mengunggah satu atau beberapa file PDF melalui interface web, kemudian aplikasi akan memproses dokumen tersebut dan menghasilkan file Excel (.xlsx) yang berisi data hasil ekstraksi. Tujuan agar data lebih mudah dianalisis dan diolah lebih lanjut.

## Fitur

- Upload file PDF hasil seleksi kedinasan  
- Ekstraksi data teks / tabel dari PDF secara otomatis
- Overview dalam tabel beberapa data yang sudah di ekstrak  
- Output dalam format Excel (.xlsx)  
- Interface web yang user‐friendly menggunakan Flask  

## 📑 Kolom Hasil Ekstraksi
Aplikasi akan mengekstrak data dari PDF ke dalam file Excel dengan struktur kolom berikut:
| Kolom              | Deskripsi                                                                                                           |
| ------------------ | ------------------------------------------------------------------------------------------------------------------- |
| **Sekolah**        | Nama sekolah atau instansi penyelenggara (contoh: *POLITEKNIK STATISTIKA STIS*)                                     |
| **Jurusan**        | Program studi / jurusan yang dipilih (contoh: *D-III STATISTIKA*)                                                   |
| **Lokasi Formasi** | Lokasi tempat formasi / penempatan (contoh: *Aceh*)                                                                 |
| **Jenis Formasi**  | Keterangan jenis formasi seleksi (contoh: *P1 – Calon Mahasiswa STIS Program Studi Statistika Program Diploma III*) |
| **No**             | Nomor urut peserta dalam daftar                                                                                     |
| **No Peserta**     | Nomor peserta ujian seleksi (ID unik)                                                                               |
| **Kode Pend**      | Kode pendidikan / formasi (misalnya: *3001000*, *3002000*)                                                          |
| **Nama**           | Nama lengkap peserta                                                                                                |
| **TWK**            | Nilai *Tes Wawasan Kebangsaan*                                                                                      |
| **TIU**            | Nilai *Tes Intelegensi Umum*                                                                                        |
| **TKP**            | Nilai *Tes Karakteristik Pribadi*                                                                                   |
| **Total**          | Jumlah total skor (TWK + TIU + TKP)                                                                                 |
| **Keterangan**     | Status atau catatan hasil (contoh: *P/L*, *L*, dsb.)                                              |


## Installation

To set up and run this project locally, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Agussatya87/scrapingPDF.git
    cd scrapingPDF
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment:**
    -   **Windows:**
        ```bash
        .\venv\Scripts\activate
        ```
    -   **macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```

4.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  **Run the Flask application:**
    ```bash
    python app.py
    ```

2.  **Access the application:**
    Open your web browser and navigate to `http://127.0.0.1:5000/`.

3.  **Upload PDF files:**
    Use the provided interface to upload your Kedinasan student selection PDF files.

4.  **Download Extracted Data:**
    After processing, the extracted data will be available as Excel files in the `outputs/` directory. You will also be able to download them directly from the web interface.

## Project Structure

```
.
├── app.py                  # Main Flask application file
├── extractor.py            # Core logic for PDF data extraction
├── requirements.txt        # Python dependencies
├── .gitignore              # Specifies intentionally untracked files to ignore
├── outputs/                # Directory to store generated Excel files
├── uploads/                # Directory to temporarily store uploaded PDF files
├── static/
│   ├── css/
│   │   └── style.css       # Stylesheets for the web interface
│   └── js/
│       └── main.js         # JavaScript for client-side functionalities
└── templates/
    └── index.html          # HTML template for the main page
```
