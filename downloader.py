import yt_dlp
import sys

def download_video(url, resolution=None):
    # Set default options
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best', # Download video and audio separately and merge them
        'outtmpl': '%(title)s.%(ext)s',        # File name will be according to video title
        'merge_output_format': 'mp4',          # Output will always be MP4
    }

    # If user specifies resolution
    if resolution:
        # Logic to select specified resolution or best quality below it
        ydl_opts['format'] = f'bestvideo[height<={resolution}]+bestaudio/best[height<={resolution}]'

    try:
        print(f"\nDownloading: {url}")
        print("Please wait, we are processing...")
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
        print("\n✅ Download Done!")
        
    except Exception as e:
        print("\n❌ got an error:")
        print(e)

if __name__ == "__main__":
    print("=== YouTube Video Downloader ===")
    
    # 1. Get link input
    video_url = input("Provide your YouTube Link: ").strip()
    
    if not video_url:
        print("did not get any link, program is clossing।")
        sys.exit()

    # 2. Get resolution input
    print("\nGive resoulution? (ex: 1080, 720, 480)")
    print("Note: If you don't type any resolution, 'Best Quality' will download.")
    res_input = input("Type your resoultion then enter: ").strip()

    # 3. Start download
    if res_input:
        download_video(video_url, resolution=res_input)
    else:
        print("\nWe are chooosing Best Quality for you...")
        download_video(video_url)