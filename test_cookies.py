#!/usr/bin/env python3
"""Quick script to test if yt-dlp can access Chrome cookies"""

import yt_dlp
import os

print("🔍 Testing Chrome cookie access...\n")

# Check if Chrome cookie file exists
chrome_cookies = os.path.expanduser('~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Cookies')
print(f"Chrome cookies file exists: {os.path.exists(chrome_cookies)}")

# Try to fetch one format with cookies
print("\n⏳ Fetching formats with Chrome cookies from a test video...\n")

opts = {
    'quiet': False,
    'no_warnings': False,
    'cookiesfrombrowser': ('firefox',),  # Try Firefox
    'skip_availability_check': True,
}

try:
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info('https://www.youtube.com/watch?v=gA-4fA_7kc8', download=False)
        
        if 'formats' in info:
            print(f"\n✅ SUCCESS! Found {len(info['formats'])} formats with Chrome cookies:\n")
            
            # Show high-quality formats
            quality_formats = [f for f in info['formats'] if f.get('height')]
            quality_formats.sort(key=lambda x: x.get('height', 0), reverse=True)
            
            print(f"{'format_id':10} {'ext':5} {'res':7} {'vcodec':12} {'acodec':12}")
            print("-" * 50)
            for f in quality_formats[:15]:  # Top 15
                fid = str(f.get('format_id',''))
                ext = f.get('ext','')
                height = f.get('height', '')
                res = f"{height}p" if height else ''
                vcodec = f.get('vcodec','')
                acodec = f.get('acodec','')
                print(f"{fid:10} {ext:5} {res:7} {vcodec:12} {acodec:12}")
        else:
            print("❌ No formats found")
except Exception as e:
    print(f"❌ Error: {e}\n")
    print("Possible solutions:")
    print("1. Make sure Chrome is COMPLETELY CLOSED (not running in background)")
    print("2. Check Task Manager and kill any 'chrome.exe' processes")
    print("3. Try Firefox instead if you have it logged in")
    print("4. Or use manual extraction from settings/cookies in YouTube")
