import yt_dlp

print("Quick Resolution Test")
print("=" * 50)

# Simple test - no cookies, ios client
opts = {
    'quiet': True,
    'no_warnings': True,
    'extractor_args': {
        'youtube': {
            'player_client': ['ios', 'android']
        }
    }
}

test_url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'  # Rick Astley

try:
    print("Fetching formats...")
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(test_url, download=False)
        
        # Get all video formats
        video_formats = [f for f in info['formats'] if f.get('height')]
        resolutions = sorted(list(set([f.get('height') for f in video_formats])), reverse=True)
        
        print(f"\nAvailable resolutions: {resolutions}")
        
        if max(resolutions) >= 720:
            print("\n[SUCCESS] HD formats available!")
        else:
            print(f"\n[WARNING] Max resolution is {max(resolutions)}p")
            print("The player client fix may not have been applied correctly.")
            
except Exception as e:
    print(f"\nError: {e}")
