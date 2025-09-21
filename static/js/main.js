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

    fileInfo.classList.add("show");
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
            progressText.textContent = "Selesai";

            statusMessage.className = "status-message success";
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
            statusMessage.className = "status-message error";
            statusMessage.textContent = "❌ " + data.message;
        }
    } catch (err) {
        statusMessage.className = "status-message error";
        statusMessage.textContent = "❌ Error server: " + err;
    }
}

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
