import flet as ft

from controller import divide_and_copy_files

def start_processing(e, source_folder, target_folders, parallel_copying, page):
    if source_folder.value != "No folder selected" and all(f.value != "No folder selected" for f in target_folders):
        divide_and_copy_files(source_folder.value, [f.value for f in target_folders], parallel_copying.value)
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

def update_folder_labels(target_folders, container):
    for idx, (button, label, delete_button) in enumerate(target_folders):
        button.text = f"Select Target Folder {idx + 1}"
        button.on_click = lambda _, idx=idx: target_folders[idx][2].get_directory_path(dialog_title=f"Select Target Folder {idx + 1}")
        button.update()

def add_target_folder(page: ft.Page, target_folders, target_folder_pickers, container):
    idx = len(target_folders)
    target_folder_label = ft.Text(value="No folder selected", width=400)
    target_folder_picker = ft.FilePicker(on_result=lambda e, idx=idx: on_result(e, target_folder_label))
    target_folder_pickers.append(target_folder_picker)
    
    target_folder_button = ft.ElevatedButton(
        f"Select Target Folder {idx + 1}",
        on_click=lambda _, idx=idx: target_folder_picker.get_directory_path(dialog_title=f"Select Target Folder {idx + 1}")
    )

    delete_button = ft.IconButton(
        icon=ft.icons.DELETE, 
        on_click=lambda e, idx=idx: delete_target_folder(idx, target_folders, target_folder_pickers, container, page)
    )

    target_folders.append((target_folder_button, target_folder_label, target_folder_picker))
    container.controls.append(ft.Row([target_folder_button, target_folder_label, delete_button]))
    
    page.overlay.append(target_folder_picker)
    page.update()

def delete_target_folder(idx, target_folders, target_folder_pickers, container, page):
    # Remove the selected folder, picker, and UI elements
    del target_folders[idx]
    del target_folder_pickers[idx]
    del container.controls[idx]
    
    # Update the text and on_click events for the remaining folders to have correct indices
    for new_idx, (button, label, picker) in enumerate(target_folders):
        button.text = f"Select Target Folder {new_idx + 1}"
        button.on_click = lambda e, new_idx=new_idx: picker.get_directory_path(dialog_title=f"Select Target Folder {new_idx + 1}")
        button.update()
    
    # Refresh the UI
    page.update()

def create_window(page: ft.Page):
    source_folder_label = ft.Text(value="No folder selected", width=400)
    
    target_folders = []
    target_folder_pickers = []
    
    container = ft.Column()

    # Add default target folders
    for _ in range(2):
        add_target_folder(page, target_folders, target_folder_pickers, container)
    
    source_folder_picker = ft.FilePicker(on_result=lambda e: on_result(e, source_folder_label))
    source_folder_button = ft.ElevatedButton(
        "Select Source Folder",
        on_click=lambda _: source_folder_picker.get_directory_path(dialog_title="Select Source Folder")
    )

    parallel_copying_checkbox = ft.Checkbox(label="Enable Parallel Copying", value=False)

    add_folder_button = ft.ElevatedButton(
        "Add Target Folder",
        on_click=lambda e: add_target_folder(page, target_folders, target_folder_pickers, container)
    )

    start_button = ft.ElevatedButton(
        "Start Processing",
        on_click=lambda e: start_processing(e, source_folder_label, [label for _, label, _ in target_folders], parallel_copying_checkbox, page)
    )

    view = ft.Column(
        [
            ft.Text("Source Folder:", size=20),
            source_folder_button,
            source_folder_label,
            ft.Divider(),
            ft.Text("Target Folders:", size=20),
            container,
            add_folder_button,
            ft.Divider(),
            parallel_copying_checkbox,
            start_button
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    page.overlay.append(source_folder_picker)

    return view

def main(page: ft.Page):
    page.title = "Folder Selector"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    view = create_window(page)
    page.add(view)

# ft.app(target=main)
