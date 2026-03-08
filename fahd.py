import flet
from flet import (
    Page, Column, Row, Text, TextField, IconButton, icons, ListView,
    ElevatedButton, FilePicker, FilePickerResultEvent, Container, Image
)
import os
import shutil

# --- وظائف إدارة الملفات ---
def list_files(path):
    items = []
    try:
        for f in os.listdir(path):
            full_path = os.path.join(path, f)
            icon = icons.FOLDER if os.path.isdir(full_path) else icons.DESCRIPTION
            items.append((f, full_path, icon))
    except Exception as e:
        print("Error listing files:", e)
    return items

def delete_file(path):
    if os.path.isdir(path):
        shutil.rmtree(path)
    else:
        os.remove(path)

def create_folder(path, name):
    os.makedirs(os.path.join(path, name), exist_ok=True)

# --- واجهة Flet ---
def main(page: Page):
    page.title = "Advanced File Manager"
    page.window_width = 1000
    page.window_height = 650
    page.padding = 10
    page.bgcolor = "#1E1E2F"

    current_path = os.getcwd()
    
    file_list = ListView(expand=True, spacing=5, padding=5, bgcolor="#2E2E3E", border_radius=10)
    path_label = Text(value=current_path, color="white", size=16)
    folder_input = TextField(hint_text="New folder name", expand=True, color="white", bgcolor="#3E3E50")
    
    def refresh_list():
        file_list.controls.clear()
        for name, full_path, icon in list_files(current_path):
            def delete_click(e, p=full_path):
                delete_file(p)
                refresh_list()
            def preview_click(e, p=full_path):
                if os.path.isfile(p):
                    ext = os.path.splitext(p)[1].lower()
                    if ext in [".png", ".jpg", ".jpeg", ".gif"]:
                        page.dialog = Container(
                            content=Image(src=p, width=500, height=500),
                            padding=10
                        )
                        page.dialog.open = True
                        page.update()
                    else:
                        page.snack_bar = flet.SnackBar(Text(f"Cannot preview {ext}"))
                        page.snack_bar.open = True
                        page.update()
            
            btn_row = Row(
                controls=[
                    IconButton(icon=icon, on_click=lambda e, p=full_path: preview_click(e, p)),
                    Text(name, expand=True, color="white"),
                    IconButton(icons.DELETE, on_click=delete_click),
                ]
            )
            file_list.controls.append(btn_row)
        page.update()
    
    def create_folder_click(e):
        name = folder_input.value.strip()
        if name:
            create_folder(current_path, name)
            folder_input.value = ""
            refresh_list()
    
    file_picker = FilePicker(on_result=lambda e: upload_file(e))
    page.overlay.append(file_picker)
    
    def upload_file(e: FilePickerResultEvent):
        if e.files:
            for f in e.files:
                shutil.copy(f.path, current_path)
        refresh_list()
    
    upload_btn = ElevatedButton("Upload File", on_click=lambda e: file_picker.pick_files())
    
    page.add(
        Column(
            controls=[
                Row([path_label]),
                Row([folder_input, ElevatedButton("Create Folder", on_click=create_folder_click), upload_btn]),
                file_list
            ],
            expand=True,
            spacing=10
        )
    )
    
    refresh_list()

if __name__ == "__main__":
    flet.app(target=main)
