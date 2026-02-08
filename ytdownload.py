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
    
    print(f"\n[Saved] Video info saved to '{json_filename}'")

def download_video(url, resolution=None, format_spec=None):
    download_folder = 'download'
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)
        print(f"[Created] '{download_folder}' folder")

    # Simple options - NO COOKIES, let yt-dlp auto-select best client
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best' if not format_spec else format_spec,
        'outtmpl': os.path.join(download_folder, '%(title)s.%(ext)s'),
        'merge_output_format': 'mp4',
        'quiet': False,
        'no_warnings': False,
    }

    if resolution and not format_spec:
        ydl_opts['format'] = f'bestvideo[height<={resolution}]+bestaudio/best[height<={resolution}]'

    try:
        print(f"\n[Downloading] {url}")
        print("Please wait...")
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            save_info_to_json(info, resolution)
            
        print("\n[SUCCESS] Download Complete!")
        
    except Exception as e:
        print("\n[ERROR] Download failed:")
        print(f"{str(e)}\n")

if __name__ == "__main__":
    print("=" * 60)
    print("YouTube Video Downloader - Simple & Fast")
    print("=" * 60)
    print("Gets all resolutions (144p to 4K) without any login!\n")

    while True:
        video_url = input("YouTube Video Link (or Enter to exit): ").strip()

        if not video_url:
            print("Goodbye!")
            break

        # Fetch formats (NO COOKIES - works better!)
        print("\n[Fetching] Getting available formats...")
        
        preview_opts = {
            'quiet': True,
            'no_warnings': False,
        }

        try:
            with yt_dlp.YoutubeDL(preview_opts) as ydl:
                info = ydl.extract_info(video_url, download=False)
        except Exception as e:
            print(f"[Warning] Could not fetch formats: {e}")
            print("Will try to download anyway...")
            info = None

        if info and 'formats' in info:
            print(f"\n{'='*70}")
            print(f"Video: {info.get('title', 'Unknown')}")
            print(f"{'='*70}")
            print(f"{'ID':10} {'Ext':5} {'Res':8} {'Video':20} {'Audio':15} {'Size':10}")
            print(f"{'-'*70}")
            
            # Filter and show only video formats (skip storyboards)
            shown = 0
            for f in info['formats']:
                # Skip useless formats
                if 'mhtml' in f.get('ext', ''):
                    continue
                if f.get('format_note') == 'storyboard':
                    continue
                if not f.get('vcodec') and not f.get('acodec'):
                    continue
                if f.get('vcodec') == 'none' and f.get('acodec') == 'none':
                    continue
                    
                fid = str(f.get('format_id', ''))
                ext = f.get('ext', '')
                height = f.get('height') or ''
                res = f"{height}p" if height else 'audio'
                vcodec = f.get('vcodec', 'none')[:19]
                acodec = f.get('acodec', 'none')[:14]
                fs = f.get('filesize') or f.get('filesize_approx') or ''
                if isinstance(fs, int):
                    fs = f"{round(fs/1024/1024,1)}MB"
                    
                print(f"{fid:10} {ext:5} {res:8} {vcodec:20} {acodec:15} {str(fs):10}")
                shown += 1
                
                if shown >= 35:
                    print("... (more formats available)")
                    break

            # Show available resolutions summary
            video_formats = [f for f in info['formats'] if f.get('height')]
            if video_formats:
                resolutions = sorted(set(f['height'] for f in video_formats), reverse=True)
                print(f"\n[Available Resolutions] {resolutions}")

        # Ask what to download
        print(f"\n{'='*70}")
        print("Options:")
        print("  - Type 'best' for best quality")
        print("  - Type a resolution number (e.g. 720, 1080, 1440)")
        print(f"{'='*70}")
        
        choice = input("Your choice: ").strip()

        if choice.lower() == 'best' or choice == '':
            download_video(video_url)
        elif choice.isdigit():
            download_video(video_url, resolution=choice)
        else:
            # Format ID provided
            download_video(video_url, format_spec=f"{choice}+bestaudio/best")

        print("\n" + "="*60)
        print("Ready for next download!")
        print("="*60 + "\n")
