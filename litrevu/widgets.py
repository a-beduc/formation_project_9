from django.forms import ClearableFileInput


class CustomFileInput(ClearableFileInput):
    template_name = "widgets/custom_file_input.html"

    clear_checkbox_label = "Supprimer l'image"
    initial_text = "Image actuelle"
    input_text = "Téléverser une nouvelle image"
