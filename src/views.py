import flet as ft
from controller import divide_and_copy_files

def create_progress_callback(progress_bar):
    def _update_progress(value):
        progress_bar.value = value
        progress_bar.page.update()
    return _update_progress

def start_processing(e, source_folder, target_folders, parallel_copying, progress_bars, page, selected_file_type):
    if source_folder.value != "No folder selected" and all(f.value != "No folder selected" for f in target_folders):
        progress_callbacks = [create_progress_callback(pb) for pb in progress_bars]
        divide_and_copy_files(
            source_folder.value, 
            [f.value for f in target_folders], 
            parallel_copying.value,
            progress_callbacks,
            selected_file_type
        )
        page.add(ft.Text("Files have been successfully copied!"))
        page.update()
    else:
        page.add(ft.Text("Please select all folders before starting."))
        page.update()

def on_result(e: ft.FilePickerResultEvent, label: ft.Text):
    if e.path:
        folder_path = e.path
        label.value = folder_path
        label.update()

def on_number_of_folders_submit(e, page: ft.Page, input_field: ft.TextField, file_type_dropdown: ft.Dropdown ):
    try:
        target_folder_count = int(input_field.value)
        if target_folder_count <= 0:
            raise ValueError("Number of folders must be positive.")
    except ValueError:
        page.add(ft.Text("Please enter a valid positive integer for the number of target folders."))
        page.update()
        return
    
    selected_file_type = file_type_dropdown.value
    page.clean()
    view = create_window(page, target_folder_count, selected_file_type)
    page.add(view) 

def create_window(page: ft.Page, target_folder_count: int, selected_file_type: str):
    source_folder_label = ft.Text(value="No folder selected", width=400)

    target_folder_labels = []
    target_folder_buttons = []
    target_folder_pickers = []
    progress_bars = []

    for i in range(target_folder_count):
        target_folder_label = ft.Text(value="No folder selected", width=400)
        target_folder_button = ft.ElevatedButton(
            f"Select Target Folder {i + 1}", 
            on_click=lambda _, idx=i: target_folder_pickers[idx].get_directory_path(dialog_title=f"Select Target Folder {idx + 1}")
        )
        
        progress_bar = ft.ProgressBar(value=0, width=400)
        
        target_folder_labels.append(target_folder_label)
        target_folder_buttons.append(target_folder_button)
        progress_bars.append(progress_bar)

    source_folder_picker = ft.FilePicker(on_result=lambda e: on_result(e, source_folder_label))
    target_folder_pickers = [ft.FilePicker(on_result=lambda e, idx=i: on_result(e, target_folder_labels[idx])) for i in range(target_folder_count)]

    source_folder_button = ft.ElevatedButton(
        "Select Source Folder", 
        on_click=lambda _: source_folder_picker.get_directory_path(dialog_title="Select Source Folder")
    )

    parallel_copying_checkbox = ft.Checkbox(label="Enable Parallel Copying", value=False)

    start_button = ft.ElevatedButton(
        "Start Processing",
        on_click=lambda e: start_processing(e, source_folder_label, target_folder_labels, parallel_copying_checkbox, progress_bars, page, selected_file_type)
    )

    target_folder_views = []
    for i in range(target_folder_count):
        target_folder_views.append(ft.Column([
            target_folder_buttons[i],  
            target_folder_labels[i],   
            progress_bars[i]      
        ]))

    theme_switch = ft.Switch(label="Dark Mode", value=page.theme_mode == ft.ThemeMode.DARK, on_change=lambda e: toggle_theme(page, e.control))

    view = ft.Column(
        [
            theme_switch,
            ft.Text("Source Folder:", size=20),
            source_folder_button,
            source_folder_label,
            ft.Divider(),
            ft.Text("Target Folders:", size=20),
            *target_folder_views, 
            ft.Divider(),
            parallel_copying_checkbox,
            start_button
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    page.overlay.extend([source_folder_picker] + target_folder_pickers)

    return view

def toggle_theme(page: ft.Page, switch: ft.Switch):
    if switch.value:
        page.theme_mode = ft.ThemeMode.DARK
    else:
        page.theme_mode = ft.ThemeMode.LIGHT
    page.update()

def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.DARK
    page.title = "Folder Selector"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    theme_switch = ft.Switch(label="Dark Mode", value=page.theme_mode == ft.ThemeMode.DARK, on_change=lambda e: toggle_theme(page, e.control))
    
    input_field = ft.TextField(label="Enter number of target folders:", width=200)
    file_type_dropdown = ft.Dropdown(label="Select mode", options=[ft.dropdown.Option('.raw + .tgv'), ft.dropdown.Option('.jp2 + .json')], value=".raw + .tgv", width=200)
    submit_button = ft.ElevatedButton("Submit", on_click=lambda e: on_number_of_folders_submit(e, page, input_field, file_type_dropdown))

    page.add(ft.Column(
        [
            theme_switch,
            input_field,
            file_type_dropdown,
            submit_button,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    ))

# ft.app(target=main)
