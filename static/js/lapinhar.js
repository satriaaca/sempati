let editorInformasi;
let editorTrend;

document.addEventListener(
    "DOMContentLoaded",
    async () => {
        try {
            editorInformasi = await ClassicEditor.create(
                document.querySelector("#informasiDiperoleh")
            );

            editorTrend = await ClassicEditor.create(
                document.querySelector("#trendPerkembangan")
            );
        } catch (error) {
            console.error("Gagal memuat CKEditor:", error);
        }

        const saveButton = document.getElementById("saveButton");
        if (saveButton) {
            saveButton.addEventListener("click", saveDocument);
        }

        const previewButton = document.getElementById("previewButton");
        if (previewButton) {
            previewButton.addEventListener("click", previewDocument);
        }
    }
);

async function saveDocument() {
    const payload = {
        nomorSurat: document.getElementById("nomorSurat").value,
        perihal: document.getElementById("perihalInput").value,
        tglInput: document.getElementById("tglInput").value,
        category: document.getElementById("categorySelect").value,
        kodeMasalah: document.getElementById("kodeMasalah").value,
        infoContent: editorInformasi ? editorInformasi.getData() : "",
        trendContent: editorTrend ? editorTrend.getData() : "",
        pejabat: document.getElementById("pejabat").value,
        jabatan: document.getElementById("jabatan").value,
        nip: document.getElementById("nip").value
    };

    try {
        const response = await fetch(
            "/api/save-form",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(payload)
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.message || "Gagal menyimpan ke server");
        }

        alert(data.message || "Berhasil disimpan");
        cleanText();

    } catch (err) {
        console.error(err);
        alert(err.message || "Gagal menyimpan laporan");
    }
}

function previewDocument() {
    console.log({
        informasi: editorInformasi ? editorInformasi.getData() : "",
        trend: editorTrend ? editorTrend.getData() : ""
    });

    alert("Preview belum dibuat");
}

function cleanText() {
    // Kosongkan input form standar
    document.getElementById("nomorSurat").value = "";
    document.getElementById("perihalInput").value = "";
    document.getElementById("tglInput").value = "";
    document.getElementById("categorySelect").value = "";
    document.getElementById("kodeMasalah").value = "";
    document.getElementById("pejabat").value = "";
    document.getElementById("jabatan").value = "";
    document.getElementById("nip").value = "";

    // Kosongkan CKEditor menggunakan method .setData()
    if (editorInformasi) {
        editorInformasi.setData("");
    }
    if (editorTrend) {
        editorTrend.setData("");
    }
}