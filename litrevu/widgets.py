from django.forms import ClearableFileInput


class CustomFileInput(ClearableFileInput):
    """
    Custom file input widget rendering a file upload input with a template suited to the application design.
    Overrides default ClearableFileInput labels and template.
    """
    template_name = "widgets/custom_file_input.html"

    clear_checkbox_label = "Supprimer l'image"
    initial_text = "Image actuelle"
    input_text = "Téléverser une nouvelle image"
