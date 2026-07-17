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
            editorTrend.getData(),
        
        pejabat: document.getElementById( "pejabat").value,
        jabatan: document.getElementById("jabatan").value,
        nip: document.getElementById("nip").value,
        pejabatTar: document.getElementById( "pejabatTar").value,
        jabatanTar: document.getElementById("jabatanTar").value,
        nipTar: document.getElementById("nipTar").value,
        nomorTar:
            document.getElementById(
                "nomorTar"
            ).value,
    };

    try {

        const response = await fetch(
            "/api/save-lapinsus",
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
