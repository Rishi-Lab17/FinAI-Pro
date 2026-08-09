/*
=========================================================
FinAI Pro
Toast Notification
=========================================================
*/

function showToast(type, message) {

    const oldToast = document.getElementById("toast-container");

    if (oldToast) {
        oldToast.remove();
    }

    const toastContainer = document.createElement("div");

    toastContainer.id = "toast-container";

    toastContainer.className =
        "toast-container position-fixed top-0 end-0 p-3";

    const toast = document.createElement("div");

    toast.className =
        "toast align-items-center text-white border-0";

    switch (type) {

        case "success":
            toast.classList.add("bg-success");
            break;

        case "error":
            toast.classList.add("bg-danger");
            break;

        case "warning":
            toast.classList.add("bg-warning");
            toast.classList.add("text-dark");
            break;

        default:
            toast.classList.add("bg-primary");
            break;
    }

    toast.setAttribute("role", "alert");
    toast.setAttribute("aria-live", "assertive");
    toast.setAttribute("aria-atomic", "true");

    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                ${message}
            </div>

            <button
                type="button"
                class="btn-close btn-close-white me-2 m-auto"
                data-bs-dismiss="toast">
            </button>
        </div>
    `;

    toastContainer.appendChild(toast);

    document.body.appendChild(toastContainer);

    const bootstrapToast = new bootstrap.Toast(toast, {

        delay: 3000

    });

    bootstrapToast.show();

}


/*
=========================================================
Shortcut Functions
=========================================================
*/

function successToast(message) {

    showToast("success", message);

}


function errorToast(message) {

    showToast("error", message);

}


function warningToast(message) {

    showToast("warning", message);

}


function infoToast(message) {

    showToast("info", message);

}


/*
=========================================================
End of File
=========================================================
*/