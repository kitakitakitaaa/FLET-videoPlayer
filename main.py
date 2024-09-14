import flet as ft

def main(page: ft.Page):
    page.window_full_screen = True
    page.padding = 0
    
    def toggle_fullscreen(e):
        page.window_full_screen = not page.window_full_screen
        page.update()

    video = ft.Video(
        playlist=[
            ft.VideoMedia("assets/video/video.mp4"),
        ],
        autoplay=True,
        show_controls=True ,
        
        # width=640,
        # height=360,
        expand=True,
        on_completed=lambda _: video.play()
    )
    def play_video(e):
        video.play()
        page.update()

    def pause_video(e):
        video.pause()
        page.update()

    def stop_video(e):
        video.pause()
        video.seek(0)
        page.update()

    # Escキーで終了
    def on_keyboard(e: ft.KeyboardEvent):
        if e.key == "Escape":
            print("Escape key pressed!")
            page.window_close()

    page.on_keyboard_event = on_keyboard
    page.add(
        # ft.AppBar(title=ft.Text("動画再生"), bgcolor=ft.colors.SURFACE_VARIANT),
        video,
        # ft.Row([
        #     ft.ElevatedButton("再生", on_click=play_video),
        #     ft.ElevatedButton("一時停止", on_click=pause_video),
        #     ft.ElevatedButton("停止", on_click=stop_video),
        #     ft.ElevatedButton("フルスクリーン切替", on_click=toggle_fullscreen),
        # ])
    )

ft.app(target=main)