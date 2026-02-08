import yt_dlp
import sys
import json
import os
from datetime import datetime

def save_info_to_json(info, requested_res):
    json_filename = 'video_info.json'
    
    # The info we will save (will be expanded as needed)
    video_data = {
        'download_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'title': info.get('title'),
        'url': info.get('webpage_url'),
        'uploader': info.get('uploader'),
        'duration_seconds': info.get('duration'),
        'view_count': info.get('view_count'),
        'upload_date': info.get('upload_date'),
        'resolution_requested': requested_res if requested_res else "Best Available",
        'file_name': info.get('_filename') # Name of the downloaded file
    }

    # If file exists previously, read it and get the list
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

    # Add new video info to the list
    data_list.append(video_data)

    # Write back to file (Overwrite with new list)
    with open(json_filename, 'w', encoding='utf-8') as f:
        json.dump(data_list, f, ensure_ascii=False, indent=4)
    
    print(f"\n📄 Video info saved to '{json_filename}'")

def download_video(url, resolution=None):
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s',
        'merge_output_format': 'mp4',
        'quiet': False,
        'no_warnings': True,
        # Use TV client to bypass YouTube's SABR-only web client
        'extractor_args': {
            'youtube': {
                'player_client': ['tv', 'android']  # TV client first, fallback to android
            }
        },
        # Advanced headers
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.youtube.com/',
        },
        'socket_timeout': 30,
        'skip_unavailable_fragments': True,
    }

    if resolution:
        ydl_opts['format'] = f'bestvideo[height<={resolution}]+bestaudio/best[height<={resolution}]'

    try:
        print(f"\nDownloading & Extracting Info: {url}")
        print("Please wait...")
        
        max_retries = 2
        for attempt in range(max_retries):
            try:
                # 'extract_info' will download and also return info
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    
                    # After download is complete, save the info
                    save_info_to_json(info, resolution)
                    
                print("\n✅ Download & Data Save Complete!")
                break
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"\n⚠️  Download failed, retrying... (Attempt {attempt + 2}/{max_retries})")
                    import time
                    time.sleep(2)
                else:
                    raise e
        
    except Exception as e:
        print("\n❌ Error Occurred:")
        print(f"{str(e)}\n")
        print("Troubleshooting tips:")
        print("1. Make sure Chrome is closed (if using Chrome cookies)")
        print("2. Try a different video URL")
        print("3. Check your internet connection")
        print("4. Update yt-dlp: pip install --upgrade yt-dlp")

if __name__ == "__main__":
    print("=== YouTube Video Downloader with JSON Log ===")
    
    video_url = input("YouTube Video Link: ").strip()
    
    if not video_url:
        print("No link provided. Exiting.")
        sys.exit()

    print("\nResolution (e.g., 1080, 720) [Press Enter for Best]:")
    res_input = input("Resolution: ").strip()

    if res_input:
        download_video(video_url, resolution=res_input)
    else:
        print("\nSelecting Best Quality...")
        download_video(video_url)