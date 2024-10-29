import flet as ft
import os
import xml.etree.ElementTree as ET
import sys
import pyautogui
import json
import socket
import threading
import screeninfo

# フェイルセーフを無効化
pyautogui.FAILSAFE = False

def hide_cursor():
    # マウスカーソルを画面外に移動して非表示にする
    screen_width, screen_height = pyautogui.size()
    pyautogui.moveTo(screen_width + 100, screen_height + 100)

def get_config():
    try:
        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.xml')
        tree = ET.parse(config_path)
        root = tree.getroot()
        return {
            'settings_json_path': root.find('settings_json_path').text,
            'monitor_index': int(root.find('monitor_index').text)
        }
    except Exception as e:
        print(f"設定ファイルの読み込みエラー: {e}")
        sys.exit(1)

def get_playlist_from_settings(settings_path):
    try:
        with open(settings_path, 'r', encoding='utf-8') as f:
            settings = json.load(f)
            return settings.get('file_order', [])
    except Exception as e:
        print(f"設定ファイルの読み込みエラー: {e}")
        sys.exit(1)

def main(page: ft.Page):
    # モニター情報を取得
    monitors = screeninfo.get_monitors()
    
    # 設定ファイルから情報を取得
    config = get_config()
    MONITOR_INDEX = config['monitor_index']
    
    if len(monitors) > MONITOR_INDEX:
        target_monitor = monitors[MONITOR_INDEX]
        # ウィンドウを指定したモニターに配置
        page.window.top = target_monitor.y
        page.window.left = target_monitor.x
        page.update()
    
    page.window.full_screen = True
    page.padding = 0
    
    hide_cursor()
    
    def toggle_fullscreen(e):
        page.window.full_screen = not page.window.full_screen
        page.update()

    # 設定ファイルから情報を取得
    config = get_config()
    
    def reload_playlist():
        # settings.jsonからプレイリストを取得
        video_files = get_playlist_from_settings(config['settings_json_path'])
        print("Reloading playlist:", video_files)
        
        # Create a new video component with the updated playlist
        new_playlist = [ft.VideoMedia(video_path) for video_path in video_files]
        new_video = ft.Video(
            playlist=new_playlist,
            autoplay=True,
            show_controls=False,
            expand=True,
            on_completed=lambda _: new_video.play()
        )
        
        # Remove old video and add new one
        page.controls.clear()
        page.add(new_video)
        page.update()
        
        # Update the global video reference
        global video
        video = new_video

    # 初期プレイリストの読み込み
    video_files = get_playlist_from_settings(config['settings_json_path'])
    playlist = [ft.VideoMedia(video_path) for video_path in video_files]
    
    video = ft.Video(
        playlist=playlist,
        autoplay=True,
        show_controls=False,
        expand=True,
        on_completed=lambda _: video.play()
    )

    def udp_listener():
        UDP_IP = "127.0.0.1"  # localhost
        UDP_PORT = 12345
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((UDP_IP, UDP_PORT))
        
        while True:
            data, addr = sock.recvfrom(1024)
            message = data.decode('utf-8')
            if message == "video_reload":
                print("Received reload command")
                reload_playlist()

    # UDP受信用スレッドの開始
    threading.Thread(target=udp_listener, daemon=True).start()

    def on_keyboard(e: ft.KeyboardEvent):
        if e.key == "Escape":
            page.window.close()
        if e.key == "F":
            toggle_fullscreen(e)

    page.on_keyboard_event = on_keyboard
    page.add(video)

ft.app(target=main)