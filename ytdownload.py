import yt_dlp
import sys
import json
import os
from datetime import datetime

def save_info_to_json(info, requested_res):
    json_filename = 'video_info.json'
    
    video_data = {
        'download_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'title': info.get('title'),
        'url': info.get('webpage_url'),
        'uploader': info.get('uploader'),
        'duration_seconds': info.get('duration'),
        'view_count': info.get('view_count'),
        'upload_date': info.get('upload_date'),
        'resolution_requested': requested_res if requested_res else "Best Available",
        'file_name': info.get('_filename')
    }

    if os.path.exists(json_filename):
        try:
            with open(json_filename, 'r', encoding='utf-8') as f:
                data_list = json.load(f)
                if not isinstance(data_list, list):
                    data_list = []
        except:
            data_list = []
    else:
        data_list = []

    data_list.append(video_data)

    with open(json_filename, 'w', encoding='utf-8') as f:
        json.dump(data_list, f, ensure_ascii=False, indent=4)
    
    print(f"\n[INFO] Video info saved to '{json_filename}'")

def download_video(url, resolution=None, format_spec=None, use_cookies=False):
    download_folder = 'download'
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)
        print(f"[INFO] Created '{download_folder}' folder")

    # Simplified approach: Let yt-dlp choose the best client automatically
    # Only specify cookies if user wants them
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best' if not format_spec else format_spec,
        'outtmpl': os.path.join(download_folder, '%(title)s.%(ext)s'),
        'merge_output_format': 'mp4',
        'quiet': False,
        'no_warnings': False,
        # Let yt-dlp auto-select the best client
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
        },
    }
    
    # Add cookie support if requested
    if use_cookies:
        try:
            ydl_opts['cookiesfrombrowser'] = ('firefox',)
            print("[INFO] Using Firefox cookies")
        except:
            try:
                ydl_opts['cookiesfrombrowser'] = ('chrome',)
                print("[INFO] Using Chrome cookies")
            except:
                print("[WARNING] Could not load browser cookies")

    if resolution and not format_spec:
        ydl_opts['format'] = f'bestvideo[height<={resolution}]+bestaudio/best[height<={resolution}]'

    try:
        print(f"\n[DOWNLOADING] {url}")
        print("Please wait...")
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            save_info_to_json(info, resolution)
            
        print("\n[SUCCESS] Download & Data Save Complete!")
        
    except Exception as e:
        print("\n[ERROR] Error Occurred:")
        print(f"{str(e)}\n")
        print("Troubleshooting tips:")
        print("1. Update yt-dlp: pip install --upgrade yt-dlp")
        print("2. Try using browser cookies (Firefox recommended)")
        print("3. Some videos require account login in browser first")

if __name__ == "__main__":
    print("=== YouTube Video Downloader (Fixed 2026) ===\n")

    # Check for available browser cookies
    firefox_path = os.path.expanduser('~\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles')
    chrome_path = os.path.expanduser('~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Cookies')
    
    has_firefox = os.path.exists(firefox_path)
    has_chrome = os.path.exists(chrome_path)
    
    if has_firefox:
        print("[INFO] Found Firefox browser")
    elif has_chrome:
        print("[INFO] Found Chrome browser")
    print()

    while True:
        video_url = input("YouTube Video Link (or press Enter to exit): ").strip()

        if not video_url:
            print("Exiting.")
            break

        # Ask about cookies
        print("\nFor HD quality (720p+), browser cookies are REQUIRED.")
        print("Make sure Firefox/Chrome is CLOSED before proceeding!")
        use_cookies_input = input("Use browser cookies? (Y/n): ").strip().lower()
        use_cookies = use_cookies_input != 'n'
        
        # Fetch formats with cookies if enabled
        preview_opts = {
            'quiet': True,
            'no_warnings': False,
            'listformats': True,
        }
        
        if use_cookies:
            try:
                preview_opts['cookiesfrombrowser'] = ('firefox',)
            except:
                try:
                    preview_opts['cookiesfrombrowser'] = ('chrome',)
                except:
                    pass

        try:
            print("\n[FETCHING] Getting available formats...")
            with yt_dlp.YoutubeDL(preview_opts) as ydl:
                info = ydl.extract_info(video_url, download=False)
        except Exception as e:
            print(f"[WARNING] Could not fetch formats: {e}")
            print("Will try to download anyway...")
            info = None

        if info and 'formats' in info:
            print(f"\nAvailable formats for: {info.get('title', 'Video')}")
            print(f"{'ID':10} {'Ext':5} {'Res':7} {'Video':15} {'Audio':15} {'Size':10}")
            print("-" * 70)
            
            # Show only useful formats
            shown = 0
            for f in info['formats']:
                # Skip storyboard and image-only formats
                if f.get('format_note') == 'storyboard':
                    continue
                if 'mhtml' in f.get('ext', ''):
                    continue
                    
                fid = str(f.get('format_id', ''))
                ext = f.get('ext', '')
                height = f.get('height') or ''
                res = f"{height}p" if height else f.get('resolution', 'audio')
                vcodec = f.get('vcodec', 'none')[:14]
                acodec = f.get('acodec', 'none')[:14]
                fs = f.get('filesize') or f.get('filesize_approx') or ''
                if isinstance(fs, int):
                    fs = f"{round(fs/1024/1024,1)}MB"
                    
                print(f"{fid:10} {ext:5} {res:7} {vcodec:15} {acodec:15} {str(fs):10}")
                shown += 1
                
                if shown >= 30:  # Limit output
                    print("... (more formats available)")
                    break

        # Ask user what to download
        print("\nOptions:")
        print("  - Type 'best' for best quality")
        print("  - Type a resolution (e.g., 720, 1080)")
        print("  - Type a format ID from the list above")
        choice = input("Your choice: ").strip()

        if choice.lower() == 'best' or choice == '':
            download_video(video_url, use_cookies=use_cookies)
        elif choice.isdigit():
            download_video(video_url, resolution=choice, use_cookies=use_cookies)
        else:
            # Format ID
            download_video(video_url, format_spec=choice, use_cookies=use_cookies)

        print("\nReady for next download.\n")