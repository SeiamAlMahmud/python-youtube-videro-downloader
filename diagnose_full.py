import yt_dlp
import os

print("=== DIAGNOSTIC TEST ===\n")

# Check Node.js
import subprocess
try:
    result = subprocess.run(['node', '--version'], capture_output=True, text=True)
    print(f"✓ Node.js installed: {result.stdout.strip()}")
except:
    print("✗ Node.js NOT found!")

# Check Firefox
firefox_path = os.path.expanduser('~\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles')
print(f"✓ Firefox profiles exist: {os.path.exists(firefox_path)}")

# Try to extract cookies
print("\n--- Testing Cookie Extraction ---")
try:
    from yt_dlp.cookies import extract_cookies_from_browser
    jar = extract_cookies_from_browser('firefox')
    youtube_cookies = [c for c in jar if 'youtube.com' in c.domain]
    print(f"✓ Found {len(youtube_cookies)} YouTube cookies from Firefox")
    
    # Check for login cookies
    important_cookies = ['SID', 'SAPISID', 'SSID', '__Secure-3PSID']
    found_cookies = [c.name for c in youtube_cookies if c.name in important_cookies]
    print(f"✓ Login cookies found: {found_cookies}")
    
    if not found_cookies:
        print("\n✗ NO LOGIN COOKIES! You are NOT logged into YouTube in Firefox!")
        print("   Please:")
        print("   1. Open Firefox")
        print("   2. Go to youtube.com")
        print("   3. Click 'Sign In' and login")
        print("   4. Close Firefox")
        print("   5. Run this script again")
    else:
        print("\n✓ You ARE logged into YouTube in Firefox!")
        
except Exception as e:
    print(f"✗ Error extracting cookies: {e}")

# Try simple extraction
print("\n--- Testing Video Extraction (without cookies) ---")
opts = {
    'quiet': True,
    'no_warnings': True,
}

try:
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info('https://www.youtube.com/watch?v=dQw4w9WgXcQ', download=False)
        formats = [f for f in info.get('formats', []) if f.get('height')]
        if formats:
            resolutions = sorted(set(f['height'] for f in formats), reverse=True)
            print(f"✓ WITHOUT cookies - Resolutions: {resolutions}")
        else:
            print("✗ WITHOUT cookies - No video formats found!")
except Exception as e:
    print(f"✗ Error: {e}")

# Try with cookies
print("\n--- Testing Video Extraction (WITH Firefox cookies) ---")
opts_cookies = {
    'quiet': True,
    'no_warnings': True,
    'cookiesfrombrowser': ('firefox',),
}

try:
    with yt_dlp.YoutubeDL(opts_cookies) as ydl:
        info = ydl.extract_info('https://www.youtube.com/watch?v=dQw4w9WgXcQ', download=False)
        formats = [f for f in info.get('formats', []) if f.get('height')]
        if formats:
            resolutions = sorted(set(f['height'] for f in formats), reverse=True)
            print(f"✓ WITH cookies - Resolutions: {resolutions}")
        else:
            print("✗ WITH cookies - No video formats found!")
except Exception as e:
    print(f"✗ Error: {e}")

print("\n=== DIAGNOSIS COMPLETE ===")
