import flet as ft
import os

def main(page: ft.Page):
    page.window.full_screen = True
    page.padding = 0
    
    def toggle_fullscreen(e):
        page.window.full_screen = not page.window.full_screen
        page.update()
    # Get all video files from assets/video directory
    video_dir = "assets/video"
    video_files = [f for f in os.listdir(video_dir) if f.endswith(('.mp4', '.avi', '.mov'))]
    
    # Create a playlist with all video files
    playlist = [ft.VideoMedia(os.path.join(video_dir, video)) for video in video_files]
    
    video = ft.Video(
        playlist=playlist,
        autoplay=True,
        show_controls=True,
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
            page.window.close()
        if e.key == "F":
            toggle_fullscreen(e)

    page.on_keyboard_event = on_keyboard
    page.add(
        video
        )

ft.app(target=main)