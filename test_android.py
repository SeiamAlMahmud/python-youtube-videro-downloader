import yt_dlp

print("Quick test of ANDROID client fix...")

url = 'https://youtu.be/gA-4fA_7kc8'

opts = {
    'quiet': True,
    'extractor_args': {
        'youtube': {
            'player_client': ['android', 'web'],
            'skip': ['hls', 'dash'],
        }
    },
    'http_headers': {
        'User-Agent': 'com.google.android.youtube/19.09.37 (Linux; U; Android 11) gzip',
    },
}

try:
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=False)
        
        # Get video formats
        video_formats = [f for f in info['formats'] 
                        if f.get('vcodec') not in ('none', None) and f.get('height')]
        
        resolutions = sorted(set(f['height'] for f in video_formats), reverse=True)
        
        print(f"\nAvailable resolutions: {resolutions}")
        
        if len(resolutions) > 1 and max(resolutions) >= 720:
            print(f"\n[SUCCESS!] HD formats available! Max: {max(resolutions)}p")
        else:
            print(f"\n[ISSUE] Only {max(resolutions) if resolutions else 0}p available")
            
        print("\nTop formats:")
        video_formats.sort(key=lambda x: x.get('height', 0), reverse=True)
        for f in video_formats[:8]:
            print(f"  {f.get('format_id'):8} {f.get('ext'):5} {f.get('height')}p  {f.get('vcodec', '')[:20]}")
            
except Exception as e:
    print(f"Error: {e}")
