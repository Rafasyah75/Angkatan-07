import flet as ft
from supabase import create_client, Client
import os
import time

# --- KONFIGURASI SUPABASE (WAJIB DIGANTI AGAR ONLINE) ---
# Dapatkan di Project Settings > API pada dashboard Supabase
SUPABASE_URL = "https://avsbllgczhxsfbaulihk.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImF2c2JsbGdjemh4c2ZiYXVsaWhrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzMwMTQ5NDQsImV4cCI6MjA4ODU5MDk0NH0.e4CIApB5UMB2Sh9NnOThV2RK-zDcfOU0dhCPyS2djnA"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
BUCKET_NAME = "galeri" # Nama bucket yang kamu buat di Supabse Storage

# --- DATaABASE ADMIN ---
ADMINS = {
    "Hilbraaaam": "Ketua Angkatan 24-26",
    "Hudzaifahh": "Wakil ketua Angkatan 24-26",
    "Rafasyahh": "Humas Kesayangan",
    "Elazzam": "Eos 800 D",
    "Azzam Diq": "Shidiq",
    "Dzikrii": "Bayar woe",
    "Yusupp": "Bangun",
    "Azzam JR": "Saturn",
    "MK Azzam": "Aneka Gold",
    "Sami abd": "TamTam"
}

def main(page: ft.Page):
    page.title = "Galeri Angkatan Online"
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO
    page.padding = 20

    # Notifikasi SnackBar
    def notify(text, color="blue"):
        page.snack_bar = ft.SnackBar(ft.Text(text), bgcolor=color)
        page.snack_bar.open = True
        page.update()

    # --- LOGIKA UPLOAD KE SUPABASE ---
    def on_upload_result(e: ft.FilePickerResultEvent):
        if e.files:
            tipe = page.session.get("current_type")
            notify(f"Sedang mengunggah {len(e.files)} file...", "blue")
            
            for file in e.files:
                try:
                    with open(file.path, 'rb') as f:
                        # Upload ke folder 'foto' atau 'video' di dalam bucket
                        cloud_path = f"{tipe}/{file.name}"
                        supabase.storage.from_(BUCKET_NAME).upload(
                            path=cloud_path,
                            file=f,
                            file_options={"cache-control": "3600", "upsert": "true"}
                        )
                    notify(f"Berhasil: {file.name}", "green")
                except Exception as ex:
                    notify(f"Gagal upload {file.name}: {ex}", "red")
            
            # Refresh galeri setelah selesai
            show_gallery(tipe, admin=True)

    file_picker = ft.FilePicker(on_result=on_upload_result)
    page.overlay.append(file_picker)

    # --- MENU UTAMA ---
    def go_menu(e=None):
        page.clean()
        page.add(
            ft.Container(
                content=ft.Column([
                    ft.Icon(ft.icons.CLOUD_DONE_ROUNDED, size=80, color=ft.colors.BLUE_400),
                    ft.Text("GALERI ANGKATAN", size=28, weight="bold"),
                    ft.Text("Xativa 1 | 2024 - 2026", size=16, color=ft.colors.BLUE_200),
                    ft.Divider(height=30, color="transparent"),
                    ft.ElevatedButton("Galeri Foto", icon=ft.icons.PHOTO_LIBRARY, width=280, height=50, on_click=lambda _: show_gallery("foto")),
                    ft.ElevatedButton("Galeri Video", icon=ft.icons.VIDEO_LIBRARY, width=280, height=50, on_click=lambda _: show_gallery("video")),
                    ft.Divider(height=20, color="transparent"),
                    ft.TextButton("Login Admin", icon=ft.icons.LOCK_PERSON, on_click=go_login),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=40
            )
        )

    # --- LOGIN ---
    def go_login(e):
        page.clean()
        user_input = ft.TextField(label="Username Admin", prefix_icon=ft.icons.PERSON, width=300)
        pass_input = ft.TextField(label="Password", password=True, can_reveal_password=True, prefix_icon=ft.icons.LOCK, width=300)
        
        def cek_login(e):
            if user_input.value in ADMINS and ADMINS[user_input.value] == pass_input.value:
                notify(f"Selamat datang, {user_input.value}!", "green")
                admin_panel()
            else:
                notify("Login Gagal! Akun tidak terdaftar.", "red")

        page.add(
            ft.Text("LOGIN ADMIN", size=25, weight="bold"),
            user_input, pass_input,
            ft.ElevatedButton("Masuk", on_click=cek_login, width=300),
            ft.TextButton("Kembali", on_click=go_menu)
        )

    # --- PANEL ADMIN ---
    def admin_panel():
        page.clean()
        page.add(
            ft.Text("PANEL KONTROL ADMIN", size=25, weight="bold", color="blue"),
            ft.ElevatedButton("Kelola Foto (Upload/Hapus)", icon=ft.icons.EDIT, width=280, on_click=lambda _: show_gallery("foto", admin=True)),
            ft.ElevatedButton("Kelola Video (Upload/Hapus)", icon=ft.icons.VIDEO_SETTINGS, width=280, on_click=lambda _: show_gallery("video", admin=True)),
            ft.OutlinedButton("Logout", icon=ft.icons.LOGOUT, width=280, on_click=go_menu)
        )

    # --- TAMPILAN GALERI (CLOUD) ---
    def show_gallery(tipe, admin=False):
        page.clean()
        page.session.set("current_type", tipe)
        
        # Ambil daftar file dari Supabase Storage
        try:
            res = supabase.storage.from_(BUCKET_NAME).list(tipe)
            # Filter file (abaikan file sistem jika ada)
            files = [item['name'] for item in res if item['name'] != '.emptyFolderPlaceholder']
        except:
            files = []

        list_files = ft.ListView(expand=True, spacing=10, padding=10)

        if not files:
            list_files.controls.append(ft.Text("Belum ada file di Cloud.", italic=True, text_align="center"))

        for f in files:
            # Ambil URL Publik untuk setiap file
            file_url = supabase.storage.from_(BUCKET_NAME).get_public_url(f"{tipe}/{f}")
            
            list_files.controls.append(
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.icons.IMAGE if tipe == "foto" else ft.icons.PLAY_CIRCLE_FILL, color="blue"),
                        ft.Text(f, expand=True, overflow=ft.TextOverflow.ELLIPSIS),
                        ft.IconButton(ft.icons.VISIBILITY, tooltip="Lihat", on_click=lambda _, url=file_url: page.launch_url(url)),
                        ft.IconButton(
                            ft.icons.DELETE_FOREVER, 
                            icon_color="red", 
                            visible=admin, 
                            on_click=lambda e, name=f: (
                                supabase.storage.from_(BUCKET_NAME).remove([f"{tipe}/{name}"]),
                                notify(f"Terhapus: {name}", "orange"),
                                show_gallery(tipe, admin)
                            )
                        )
                    ]),
                    padding=10, border=ft.border.all(1, ft.colors.GREY_800), border_radius=10, bgcolor=ft.colors.BLACK12
                )
            )

        # Header Galeri
        header = ft.Row([
            ft.Text(f"GALERI {tipe.upper()}", size=22, weight="bold"),
            ft.ElevatedButton("Upload", icon=ft.icons.ADD_A_PHOTO, visible=admin, 
                              on_click=lambda _: file_picker.pick_files(allow_multiple=True))
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

        page.add(
            header,
            ft.Divider(),
            ft.Container(content=list_files, expand=True),
            ft.FloatingActionButton(icon=ft.icons.ARROW_BACK, on_click=lambda _: admin_panel() if admin else go_menu())
        )
        page.update()

    # Splash Screen
    page.add(ft.ProgressRing(), ft.Text("Menghubungkan ke Cloud..."))
    page.update()
    time.sleep(1)
    go_menu()

if __name__ == "__main__":
    # Menjalankan sebagai Web App
    port_env = int(os.environ.get("PORT", 8550))
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, host="0.0.0.0", port=port_env)
