import yt_dlp
import os
import subprocess

print("DIAGNOSTIC TEST")
print("=" * 50)

# Check Node.js
try:
    result = subprocess.run(['node', '--version'], capture_output=True, text=True)
    print(f"Node.js: {result.stdout.strip()}")
except:
    print("Node.js: NOT FOUND")

# Check Firefox
firefox_path = os.path.expanduser('~\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles')
print(f"Firefox profiles exist: {os.path.exists(firefox_path)}")

# Check cookies
print("\nChecking Firefox cookies...")
try:
    opts = {
        'quiet': True,
        'cookiesfrombrowser': ('firefox',),
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        # Just try to load cookies
        print("Firefox cookies loaded successfully!")
except Exception as e:
    print(f"Cookie error: {str(e)[:100]}")

# Test WITHOUT cookies
print("\nTest 1: WITHOUT cookies")
opts1 = {'quiet': True}
try:
    with yt_dlp.YoutubeDL(opts1) as ydl:
        info = ydl.extract_info('https://www.youtube.com/watch?v=dQw4w9WgXcQ', download=False)
        video_formats = [f for f in info.get('formats', []) if f.get('height')]
        if video_formats:
            resolutions = sorted(set(f['height'] for f in video_formats), reverse=True)
            print(f"Resolutions available: {resolutions}")
            if max(resolutions) >= 720:
                print("Status: HD AVAILABLE!")
            else:
                print(f"Status: Limited to {max(resolutions)}p")
        else:
            print("Status: NO VIDEO FORMATS")
except Exception as e:
    print(f"Error: {str(e)[:100]}")

# Test WITH cookies  
print("\nTest 2: WITH Firefox cookies")
opts2 = {
    'quiet': True,
    'cookiesfrombrowser': ('firefox',),
}
try:
    with yt_dlp.YoutubeDL(opts2) as ydl:
        info = ydl.extract_info('https://www.youtube.com/watch?v=dQw4w9WgXcQ', download=False)
        video_formats = [f for f in info.get('formats', []) if f.get('height')]
        if video_formats:
            resolutions = sorted(set(f['height'] for f in video_formats), reverse=True)
            print(f"Resolutions available: {resolutions}")
            if max(resolutions) >= 720:
                print("Status: HD AVAILABLE!")
            else:
                print(f"Status: Limited to {max(resolutions)}p")
        else:
            print("Status: NO VIDEO FORMATS")
except Exception as e:
    print(f"Error: {str(e)[:100]}")

print("\n" + "=" * 50)
print("DIAGNOSIS COMPLETE")
