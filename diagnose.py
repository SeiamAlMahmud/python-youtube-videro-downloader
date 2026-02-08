import yt_dlp
import sys

test_url = 'https://youtu.be/gA-4fA_7kc8'

print("Testing Different Player Clients...")
print("=" * 60)

# Test different client combinations
clients_to_test = [
    ['web'],
    ['ios'],
    ['android'],
    ['tv'],
    ['web', 'ios'],
    ['ios', 'android'],
    ['android', 'web'],
]

for clients in clients_to_test:
    print(f"\nTesting: {clients}")
    print("-" * 60)
    
    opts = {
        'quiet': True,
        'no_warnings': True,
        'extractor_args': {
            'youtube': {
                'player_client': clients,
                'skip': ['hls', 'dash']  # Skip streaming formats
            }
        },
    }
    
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(test_url, download=False)
            
            # Get video formats only
            video_formats = [f for f in info.get('formats', []) 
                           if f.get('vcodec') != 'none' and f.get('height')]
            
            if video_formats:
                resolutions = sorted(set(f['height'] for f in video_formats), reverse=True)
                print(f"Resolutions found: {resolutions}")
                
                # Show details of top formats
                video_formats.sort(key=lambda x: x.get('height', 0), reverse=True)
                for fmt in video_formats[:5]:
                    print(f"  {fmt.get('format_id'):8} {fmt.get('ext'):5} {fmt.get('height')}p")
            else:
                print("  NO VIDEO FORMATS FOUND!")
                
    except Exception as e:
        print(f"  ERROR: {str(e)[:80]}")

print("\n" + "=" * 60)
print("DIAGNOSIS COMPLETE")
