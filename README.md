# Kedinasan Student Selection Data Scraping (2023)

## Deskripsi

Aplikasi ini dibuat untuk mengekstrak data dari file PDF hasil seleksi calon mahasiswa kedinasan tahun 2023. Pengguna dapat mengunggah satu atau beberapa file PDF melalui interface web, kemudian aplikasi akan memproses dokumen tersebut dan menghasilkan file Excel (.xlsx) yang berisi data hasil ekstraksi. Tujuan agar data lebih mudah dianalisis dan diolah lebih lanjut.

## Fitur

- Upload file PDF hasil seleksi kedinasan  
- Ekstraksi data teks / tabel dari PDF secara otomatis
- overview dalam tabel beberapa data yang sudah di ekstrak  
- Output dalam format Excel (.xlsx)  
- Interface web yang user‐friendly menggunakan Flask  


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
