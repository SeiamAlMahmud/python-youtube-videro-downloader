import yt_dlp

print("Testing IOS client with cookies support...")

url = 'https://youtu.be/gA-4fA_7kc8'

opts = {
    'quiet': True,
    'no_warnings': False,
    'extractor_args': {
        'youtube': {
            'player_client': ['ios', 'web'],
        }
    },
    'http_headers': {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15',
    },
}

# Try with Firefox cookies
try:
    opts['cookiesfrombrowser'] = ('firefox',)
    print("Attempting with Firefox cookies...")
except:
    print("No Firefox cookies")

try:
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=False)
        
        # Get video formats
        video_formats = [f for f in info.get('formats', [])
                        if f.get('vcodec') not in ('none', None) and f.get('height')]
        
        if video_formats:
            resolutions = sorted(set(f['height'] for f in video_formats), reverse=True)
            print(f"\n[SUCCESS] Available resolutions: {resolutions}")
            
            if max(resolutions) >= 720:
                print(f"[HD AVAILABLE] Maximum: {max(resolutions)}p")
            else:
                print(f"[LIMITED] Maximum: {max(resolutions)}p")
                
            print("\nTop formats:")
            video_formats.sort(key=lambda x: x.get('height', 0), reverse=True)
            for f in video_formats[:10]:
                fid = f.get('format_id', '')
                ext = f.get('ext', '')
                height = f.get('height', '')
                print(f"  {fid:8} {ext:5} {height}p")
        else:
            print("[ERROR] No video formats found!")
            
except Exception as e:
    print(f"[ERROR] {e}")
