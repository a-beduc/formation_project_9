/**
 * Script to manage image upload through a custom button.
 */
document.addEventListener("DOMContentLoaded", () => {
    const fileInput = document.querySelector(".formTicket__hidden");
    const customButton = document.querySelector(".formTicket__customBlock__upload");
    const fileName = document.querySelector(".formTicket__customBlock__fileName");
    const checkbox = document.querySelector('.formTicket__checkbox');
    const deleteButton = document.querySelector(".formTicket__customBlock__delete");

    /**
     * When user clicks the "custom" button. Trigger a click on the hidden file input.
     */
    customButton.addEventListener("click", () => {
        fileInput.click();
    })

    /**
     * Display the name of the file selected before upload.
     */
    fileInput.addEventListener("change", () => {
        if (fileName) {
            fileName.style.display = "inline-block";
        }
        if (fileInput.files.length > 0) {
            fileName.textContent = fileInput.files[0].name;
        } else {
            fileName.textContent = "Ajouter une image";
        }
    });

    /**
     * Check the hidden checkbox when clicking on the custom delete button.
     */
    if (deleteButton) {
        deleteButton.addEventListener("click", () => {
            if (checkbox) {
                checkbox.checked = true;
            }
            if (fileName) {
                fileName.style.display = "none";
            }
        })
    }
})
