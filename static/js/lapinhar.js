let editorInformasi;
let editorTrend;

document.addEventListener(
    "DOMContentLoaded",
    async () => {

        editorInformasi = await ClassicEditor.create(
            document.querySelector("#informasiDiperoleh")
        );

        editorTrend = await ClassicEditor.create(
            document.querySelector("#trendPerkembangan")
        );

        const saveButton =
            document.getElementById("saveButton");

        if (saveButton) {
            saveButton.addEventListener(
                "click",
                saveDocument
            );
        }

        const previewButton =
            document.getElementById("previewButton");

        if (previewButton) {
            previewButton.addEventListener(
                "click",
                previewDocument
            );
        }

    }
);

async function saveDocument() {

    const payload = {
        nomorSurat:
            document.getElementById(
                "nomorSurat"
            ).value,

        perihal:
            document.getElementById(
                "perihalInput"
            ).value,

        tglInput:
            document.getElementById(
                "tglInput"
            ).value,

        category:
            document.getElementById(
                "categorySelect"
            ).value,

        kodeMasalah:
            document.getElementById(
                "kodeMasalah"
            ).value,

        infoContent:
            editorInformasi.getData(),

        trendContent:
            editorTrend.getData()
    };

    try {

        const response = await fetch(
            "/api/save-form",
            {
                method: "POST",
                headers: {
                    "Content-Type":
                        "application/json"
                },
                body:
                    JSON.stringify(payload)
            }
        );

        const data =
            await response.json();

        alert(
            data.message ||
            "Berhasil disimpan"
        );

    } catch (err) {

        console.error(err);

        alert(
            "Gagal menyimpan laporan"
        );
    }
}

function previewDocument() {

    console.log({
        informasi:
            editorInformasi.getData(),

        trend:
            editorTrend.getData()
    });

    alert(
        "Preview belum dibuat"
    );
}