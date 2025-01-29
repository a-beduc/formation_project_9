
document.addEventListener("DOMContentLoaded", () => {
    const fileInput = document.querySelector(".formTicket__hidden");
    const customButton = document.querySelector(".formTicket__customBlock__upload");
    const fileName = document.querySelector(".formTicket__customBlock__fileName");
    const checkbox = document.querySelector('.formTicket__checkbox');
    const deleteButton = document.querySelector(".formTicket__customBlock__delete");

    customButton.addEventListener("click", () => {
        fileInput.click();
        if (checkbox) {
            checkbox.checked = false;
        }
    })

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

