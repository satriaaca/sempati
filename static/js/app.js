const themeToggle = document.getElementById("themeToggle");

if (themeToggle) {

    themeToggle.addEventListener("click", () => {

        const html = document.documentElement;

        const currentTheme = html.getAttribute("data-bs-theme");

        const nextTheme =
            currentTheme === "dark"
                ? "light"
                : "dark";

        html.setAttribute(
            "data-bs-theme",
            nextTheme
        );

        localStorage.setItem(
            "theme",
            nextTheme
        );

    });

    const savedTheme =
        localStorage.getItem("theme");

    if (savedTheme) {
        document.documentElement.setAttribute(
            "data-bs-theme",
            savedTheme
        );
    }

}

document.addEventListener(
    "DOMContentLoaded",
    () => {

        const sidebar =
            document.getElementById(
                "sidebar"
            );

        const toggleBtn =
            document.getElementById(
                "sidebarToggle"
            );

        const overlay =
            document.getElementById(
                "sidebarOverlay"
            );

        if (toggleBtn) {

            toggleBtn.addEventListener(
                "click",
                () => {
                    sidebar.classList.toggle(
                        "show"
                    );

                    overlay.classList.toggle(
                        "show"
                    );
                }
            );

        }

        if (overlay) {

            overlay.addEventListener(
                "click",
                () => {
                    sidebar.classList.remove(
                        "show"
                    );

                    overlay.classList.remove(
                        "show"
                    );
                }
            );

        }

    }
);