import flet
from flet import (
    Page, Column, Row, Text, TextField, IconButton, icons, ListView,
    FilePicker, FilePickerResultEvent, ElevatedButton, AlertDialog, Container
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
    page.title = "File Manager"
    page.window_width = 900
    page.window_height = 600
    page.padding = 10
    page.bgcolor = "#1E1E2F"
    
    current_path = os.getcwd()
    
    # قائمة الملفات
    file_list = ListView(expand=True, spacing=5, padding=5, bgcolor="#2E2E3E", border_radius=10)
    
    path_label = Text(value=current_path, color="white", size=16)
    
    folder_input = TextField(hint_text="New folder name", expand=True, color="white", bgcolor="#3E3E50")
    
    def refresh_list():
        file_list.controls.clear()
        for name, full_path, icon in list_files(current_path):
            btn_row = Row(
                controls=[
                    Text(name, expand=True, color="white"),
                    IconButton(icons.DELETE, on_click=lambda e, p=full_path: delete_file_click(p)),
                ]
            )
            file_list.controls.append(btn_row)
        page.update()
    
    def delete_file_click(path_to_delete):
        delete_file(path_to_delete)
        refresh_list()
    
    def create_folder_click(e):
        name = folder_input.value.strip()
        if name:
            create_folder(current_path, name)
            folder_input.value = ""
            refresh_list()
    
    # رفع الملفات
    file_picker = FilePicker(on_result=lambda e: upload_file(e))
    page.overlay.append(file_picker)
    
    def upload_file(e: FilePickerResultEvent):
        if e.files:
            for f in e.files:
                shutil.copy(f.path, current_path)
        refresh_list()
    
    # زر فتح FilePicker
    upload_btn = ElevatedButton("Upload File", on_click=lambda e: file_picker.pick_files())
    
    # تصميم واجهة حديثة
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
