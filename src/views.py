import flet as ft
from controller import divide_and_copy_files

def start_processing(e, source_folder, target_folders, parallel_copying, page, progress_bars):
    if source_folder.value != "No folder selected" and all(f.value != "No folder selected" for f in target_folders):
        divide_and_copy_files(source_folder.value, [f.value for f in target_folders], parallel_copying.value, progress_bars, page)
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

def on_number_of_folders_submit(e, page: ft.Page, input_field: ft.TextField):
    try:
        target_folder_count = int(input_field.value)
        if target_folder_count <= 0:
            raise ValueError("Number of folders must be positive.")
    except ValueError:
        page.add(ft.Text("Please enter a valid positive integer for the number of target folders."))
        page.update()
        return
    
    page.clean()
    view, progress_bars = create_window(page, target_folder_count)
    page.add(view)

def create_window(page: ft.Page, target_folder_count: int):
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
        
        progress_bar = ft.ProgressBar(value=0.0, width=400)  # Fractional value
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
        on_click=lambda e: start_processing(e, source_folder_label, target_folder_labels, parallel_copying_checkbox, page, progress_bars)
    )

    view = ft.Column(
        [
            ft.Text("Source Folder:", size=20),
            source_folder_button,
            source_folder_label,
            ft.Divider(),
            ft.Text("Target Folders:", size=20),
            *[
                elem
                for pair in zip(target_folder_buttons, target_folder_labels)
                for elem in pair
            ],
            *progress_bars,
            ft.Divider(),
            parallel_copying_checkbox,
            start_button
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    page.overlay.extend([source_folder_picker] + target_folder_pickers)

    return view, progress_bars

def main(page: ft.Page):
    page.title = "Folder Selector"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    input_field = ft.TextField(label="Enter number of target folders:", width=200)
    submit_button = ft.ElevatedButton("Submit", on_click=lambda e: on_number_of_folders_submit(e, page, input_field))

    page.add(ft.Column(
        [
            input_field,
            submit_button,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    ))

# ft.app(target=main)
