# Kedinasan Student Selection Data Scraping (2023)

## Project Overview
This project is a web application designed to scrape and extract data from the 2023 Kedinasan student selection results. It allows users to upload PDF files containing selection results, processes them, and then provides the extracted data in an organized Excel format.

## Features
-   **PDF Upload:** Users can easily upload one or more PDF files containing the Kedinasan student selection results.
-   **Data Extraction:** Utilizes advanced techniques to accurately extract relevant information from the uploaded PDF documents.
-   **Excel Output:** Generates a structured Excel file (`.xlsx`) for each processed PDF, making the data easy to analyze and use.
-   **Web Interface:** A user-friendly web interface built with Flask for seamless interaction.

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
