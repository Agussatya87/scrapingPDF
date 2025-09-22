const fileInput = document.getElementById("fileInput");
const uploadArea = document.getElementById("uploadArea");
const fileInfo = document.getElementById("fileInfo");
const fileName = document.getElementById("fileName");
const progressFill = document.getElementById("progressFill");
const progressText = document.getElementById("progressText");
const statusMessage = document.getElementById("statusMessage");
const resultsSection = document.getElementById("resultsSection");
const previewTable = document.getElementById("previewTable");
const downloadBtn = document.getElementById("downloadBtn");
const newFileBtn = document.getElementById("newFileBtn");
const extractBtn = document.getElementById("extractBtn"); // New element

let currentFileId = null;

uploadArea.addEventListener("click", () => fileInput.click());
fileInput.addEventListener("change", handleFile);

// Drag and Drop functionality
uploadArea.addEventListener("dragover", (e) => {
    e.preventDefault();
    uploadArea.classList.add("dragover");
});

uploadArea.addEventListener("dragleave", () => {
    uploadArea.classList.remove("dragover");
});

uploadArea.addEventListener("drop", (e) => {
    e.preventDefault();
    uploadArea.classList.remove("dragover");
    fileInput.files = e.dataTransfer.files;
    handleFile();
});

async function handleFile() {
    const file = fileInput.files[0];
    if (!file) return;

    // Reset UI for new upload
    fileInfo.classList.add("show");
    resultsSection.classList.remove("show");
    statusMessage.classList.remove("show");
    extractBtn.style.display = "none";

    fileName.textContent = file.name;
    progressFill.style.width = "0%";
    progressText.textContent = "Mengupload...";

    const formData = new FormData();
    formData.append("file", file);

    try {
        const res = await fetch("/upload", { method: "POST", body: formData });
        const data = await res.json();

        if (data.status === "success") {
            currentFileId = data.file_id;
            progressFill.style.width = "100%";
            progressText.textContent = "Upload Selesai";

            statusMessage.className = "status-message success show"; // Add 'show' class
            statusMessage.textContent = data.message + " Silakan klik tombol 'Mulai Ekstraksi' di bawah.";
            extractBtn.style.display = "block";

            // Reset results section until extraction is complete
            document.getElementById("totalRows").textContent = "0";
            document.getElementById("totalSchools").textContent = "0";
            document.getElementById("totalMajors").textContent = "0";
            document.getElementById("totalPages").textContent = "0";
            previewTable.innerHTML = "";

            // Old extraction logic removed here

            downloadBtn.onclick = () => window.location.href = `/download/${currentFileId}`;
            newFileBtn.onclick = () => window.location.reload();
        } else {
            statusMessage.className = "status-message error show"; // Add 'show' class
            statusMessage.textContent = "❌ Error server: " + err;
        }
    } catch (err) {
        statusMessage.className = "status-message error show"; // Add 'show' class
        statusMessage.textContent = "❌ Error server: " + err;
    }
}

// New function to handle extraction
extractBtn.addEventListener("click", async () => {
    if (!currentFileId) {
        statusMessage.className = "status-message error show";
        statusMessage.textContent = "❌ Tidak ada file yang diupload untuk diekstrak.";
        return;
    }

    extractBtn.disabled = true;
    extractBtn.textContent = "Mengekstrak...";
    statusMessage.className = "status-message processing show";
    statusMessage.textContent = "⏳ Sedang mengekstrak data dari PDF...";
    progressText.textContent = "Mengekstrak...";
    progressFill.style.width = "50%"; // Simulate progress

    try {
        const res = await fetch(`/extract/${currentFileId}`, { method: "POST" });
        const data = await res.json();

        if (data.status === "success") {
            progressFill.style.width = "100%";
            progressText.textContent = "Ekstraksi Selesai";

            statusMessage.className = "status-message success show";
            statusMessage.textContent = "✅ Ekstraksi berhasil!";

            document.getElementById("totalRows").textContent = data.stats.totalRows;
            document.getElementById("totalSchools").textContent = data.stats.totalSchools;
            document.getElementById("totalMajors").textContent = data.stats.totalMajors;
            document.getElementById("totalPages").textContent = data.stats.totalPages;

            renderPreview(data.preview);

            resultsSection.classList.add("show");
            downloadBtn.onclick = () => window.location.href = `/download/${currentFileId}`;
            newFileBtn.onclick = () => window.location.reload();
        } else {
            statusMessage.className = "status-message error show";
            statusMessage.textContent = "❌ " + data.message;
            progressFill.style.width = "0%";
            progressText.textContent = "Gagal";
        }
    } catch (err) {
        statusMessage.className = "status-message error show";
        statusMessage.textContent = "❌ Error server saat ekstraksi: " + err;
        progressFill.style.width = "0%";
        progressText.textContent = "Gagal";
    } finally {
        extractBtn.disabled = false;
        extractBtn.textContent = "Mulai Ekstraksi";
    }
});

function renderPreview(rows) {
    if (!rows.length) {
        previewTable.innerHTML = "<p>Tidak ada data untuk ditampilkan</p>";
        return;
    }

    let table = "<table><thead><tr>";
    Object.keys(rows[0]).forEach(col => {
        table += `<th>${col}</th>`;
    });
    table += "</tr></thead><tbody>";

    rows.forEach(row => {
        table += "<tr>";
        Object.values(row).forEach(val => {
            table += `<td>${val ?? ""}</td>`;
        });
        table += "</tr>";
    });

    table += "</tbody></table>";
    previewTable.innerHTML = table;
}
