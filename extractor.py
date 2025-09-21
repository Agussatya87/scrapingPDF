import pdfplumber
import pandas as pd
import re

# --- fungsi cleaning meta ---
def clean_meta(value: str):
    """Bersihkan metadata dari kode angka di depan dan karakter sisa"""
    if not value:
        return None
    value = value.strip()
    value = re.sub(r"^(Sekolah|Jurusan)\s*:\s*", "", value, flags=re.I)
    value = re.sub(r"^\d+\s*-\s*", "", value)
    value = re.sub(r"^\d+\s+", "", value)
    value = value.strip(" :-")
    return value

def extract_school_name(text: str):
    if not text:
        return None
    text = re.sub(r"^Sekolah\s*:?\s*", "", text, flags=re.I)
    text = re.sub(r"^\d+\s*-\s*", "", text)
    text = re.sub(r"^\d+\s+", "", text)
    return text.strip()

def extract_major_name(text: str):
    if not text:
        return None
    text = re.sub(r"^Jurusan\s*:?\s*", "", text, flags=re.I)
    text = re.sub(r"^\d+\s*-\s*", "", text)
    text = re.sub(r"^\d+\s+", "", text)
    return text.strip()

def extract_metadata_multiline(lines, start_idx, keyword):
    """Ekstrak metadata yang mungkin tersebar di beberapa baris"""
    if start_idx >= len(lines):
        return None, start_idx
    
    line = lines[start_idx]
    
    # Ambil bagian setelah keyword
    if ":" in line:
        content = line.split(":", 1)[1].strip()
    else:
        content = line.replace(keyword, "").strip()
    
    # JANGAN bersihkan prefix untuk Jenis Formasi karena P1, P2 dll adalah kode penting
    if keyword != "Jenis Formasi":
        # Bersihkan prefix angka hanya untuk metadata selain Jenis Formasi
        content = re.sub(r"^\d+\s*-\s*", "", content)
        content = re.sub(r"^\d+\s+", "", content)
    
    content = content.strip()
    
    # Cek baris berikutnya apakah masih bagian dari metadata yang sama
    next_idx = start_idx + 1
    while next_idx < len(lines):
        next_line = lines[next_idx].strip()
        
        # Stop jika bertemu keyword metadata lain atau informasi yang tidak diinginkan
        stop_keywords = ["Sekolah", "Jurusan", "Lokasi Formasi", "Jenis Formasi", "Jumlah Peserta", "Pendidikan"]
        if any(next_line.startswith(kw) for kw in stop_keywords):
            break
            
        # Stop jika bertemu format nomor urut (seperti "1 2023...")
        if re.match(r"^\d+\s+\d{4}", next_line):
            break
            
        # Stop jika bertemu header tabel
        if any(word in next_line.upper() for word in ["NO PESERTA", "NAMA", "TWK", "TIU", "TKP", "PENDIDIKAN"]):
            break
            
        # Stop jika baris kosong
        if not next_line:
            break
        
        # Stop jika terlihat seperti data peserta (format nomor peserta)
        if re.match(r"^\d+\s+\d{10,}", next_line):
            break
            
        # Stop jika baris mengandung format kode pendidikan seperti (3002000) atau angka dalam kurung
        if re.search(r"\(\d+\)", next_line):
            break
            
        # Stop jika baris terlalu panjang (kemungkinan bukan lanjutan metadata)
        if len(next_line) > 100:
            break
            
        # Jika baris ini tampak seperti lanjutan metadata, gabungkan
        if not re.match(r"^\d+\s", next_line) and len(next_line) > 3:
            # Untuk Jenis Formasi, jangan bersihkan prefix P1, P2 dll
            if keyword == "Jenis Formasi":
                clean_next = next_line.strip()
            else:
                # Bersihkan prefix angka dari baris lanjutan untuk metadata lain
                clean_next = re.sub(r"^\d+\s*-\s*", "", next_line)
                clean_next = re.sub(r"^\d+\s+", "", clean_next)
                clean_next = clean_next.strip()
            
            if clean_next:
                content += " " + clean_next
            next_idx += 1
        else:
            break
    
    return content.strip() if content else None, next_idx - 1

# --- fungsi cleaning hasil DataFrame ---
def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    # Buang baris tanpa peserta/nama
    df = df.dropna(subset=["No Peserta", "Nama"])
    df = df[df["No Peserta"].astype(str).str.strip() != ""]
    df = df[df["Nama"].astype(str).str.strip() != ""]

    # Buang baris header duplikat (TWK/TIU/TKP dsb)
    mask_header = (
        df["TWK"].astype(str).str.upper() == "TWK"
    ) | (
        df["Nama"].astype(str).str.upper() == "NAMA"
    )
    df = df[~mask_header]

    # Hapus kolom tidak penting
    drop_cols = [c for c in ["No", "Total Kompetisi"] if c in df.columns]
    df = df.drop(columns=drop_cols)

    # Trim spasi
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    return df.reset_index(drop=True)

# --- fungsi utama ---
def extract_kemenku_strong(pdf_path, excel_path):
    data_rows = []
    current_meta = {"Sekolah": None, "Jurusan": None, "Lokasi Formasi": None, "Jenis Formasi": None}
    total_kompetisi = None

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text() or ""
            lines = [ln.strip() for ln in text.split("\n") if ln.strip()]

            # --- cari metadata dengan penanganan multi-line ---
            i = 0
            while i < len(lines):
                ln = lines[i]
                
                # Skip baris yang mengandung "Pendidikan" karena bukan metadata utama
                if ln.startswith("Pendidikan"):
                    i += 1
                    continue
                
                if ln.startswith("Sekolah"):
                    content, next_i = extract_metadata_multiline(lines, i, "Sekolah")
                    current_meta["Sekolah"] = extract_school_name(content) if content else None
                    i = next_i
                    
                elif ln.startswith("Jurusan"):
                    content, next_i = extract_metadata_multiline(lines, i, "Jurusan")
                    current_meta["Jurusan"] = extract_major_name(content) if content else None
                    i = next_i
                    
                elif ln.startswith("Lokasi Formasi"):
                    content, next_i = extract_metadata_multiline(lines, i, "Lokasi Formasi")
                    current_meta["Lokasi Formasi"] = content
                    i = next_i
                    
                elif ln.startswith("Jenis Formasi"):
                    content, next_i = extract_metadata_multiline(lines, i, "Jenis Formasi")
                    current_meta["Jenis Formasi"] = content
                    i = next_i
                    
                elif "Jumlah Peserta" in ln:
                    m = re.search(r"Jumlah Peserta\s*:?\s*(\d+)", ln)
                    if m:
                        total_kompetisi = int(m.group(1))
                
                i += 1

            # --- ambil tabel peserta ---
            tables = page.extract_tables()
            for table in tables:
                if not table or len(table) < 2:
                    continue
                    
                header = [h if h is not None else "" for h in table[0]]
                if "No Peserta" in " ".join(header).title():
                    for row in table[1:]:
                        if not any(row):
                            continue
                        row = [r if r is not None else "" for r in row]
                        if "No Peserta" in " ".join(row).title():
                            continue
                        if len(row) >= 8:
                            if row[0] and not row[0].isdigit():
                                if "No" in row[0]:
                                    continue
                            data_rows.append({
                                "Sekolah": current_meta["Sekolah"],
                                "Jurusan": current_meta["Jurusan"],
                                "Lokasi Formasi": current_meta["Lokasi Formasi"],
                                "Jenis Formasi": current_meta["Jenis Formasi"],
                                "No": row[0],
                                "No Peserta": row[1],
                                "Kode Pendidikan": row[2],
                                "Nama": row[3],
                                "TWK": row[4],
                                "TIU": row[5],
                                "TKP": row[6],
                                "Total": row[7],
                                "Keterangan": row[8] if len(row) > 8 else "",
                                "Total Kompetisi": total_kompetisi
                            })

    df = pd.DataFrame(data_rows)

    # --- post-cleaning meta ---
    if not df.empty:
        # Untuk Sekolah dan Jurusan tetap dibersihkan karena memang ada prefix angka yang tidak diperlukan
        df['Sekolah'] = df['Sekolah'].apply(lambda x: extract_school_name(str(x)) if x else None)
        df['Jurusan'] = df['Jurusan'].apply(lambda x: extract_major_name(str(x)) if x else None)
        
        # Untuk Lokasi Formasi dan Jenis Formasi, hanya bersihkan prefix angka sederhana, jangan hapus kode formasi
        df['Lokasi Formasi'] = df['Lokasi Formasi'].apply(
            lambda x: re.sub(r"^\d+\s*-\s*", "", str(x)).strip() if x else None
        )
        # JANGAN bersihkan Jenis Formasi karena P1, P2 adalah kode penting
        # df['Jenis Formasi'] sudah bersih dari fungsi extract_metadata_multiline

    # --- cleaning tambahan (hapus sampah baris/kolom) ---
    df = clean_dataframe(df)

    df.to_excel(excel_path, index=False)
    print(f"Hasil ekstraksi: {len(df)} baris tersimpan di {excel_path}")
    
    # Debug: tampilkan metadata yang ditemukan
    if not df.empty:
        print("\nMetadata yang diekstrak:")
        sample = df.iloc[0]
        print(f"Sekolah: {sample['Sekolah']}")
        print(f"Jurusan: {sample['Jurusan']}")
        print(f"Lokasi Formasi: {sample['Lokasi Formasi']}")
        print(f"Jenis Formasi: {sample['Jenis Formasi']}")
    
    return df