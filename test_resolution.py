#!/usr/bin/env python3
"""Test script to verify high-resolution format availability"""

import yt_dlp
import os
import sys

# Force UTF-8 encoding for Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

print("Testing High-Resolution Format Availability\n")
print("=" * 60)

# Test URL
test_url = 'https://www.youtube.com/watch?v=gA-4fA_7kc8'

# Check for Firefox browser
firefox_path = os.path.expanduser('~\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles')
has_firefox = os.path.exists(firefox_path)
print(f"Firefox cookies available: {has_firefox}")

# Test different player client configurations
test_configs = [
    {
        'name': 'With Cookies - WEB client (BEST FOR HIGH QUALITY)',
        'clients': ['web', 'ios', 'tv_embedded'],
        'use_cookies': True
    },
    {
        'name': 'With Cookies - IOS client',
        'clients': ['ios', 'android', 'tv'],
        'use_cookies': True
    },
    {
        'name': 'Without Cookies - IOS client',
        'clients': ['ios', 'android', 'tv'],
        'use_cookies': False
    },
]

for i, config in enumerate(test_configs, 1):
    print(f"\n\n{'='*60}")
    print(f"TEST {i}: {config['name']}")
    print(f"Player clients: {', '.join(config['clients'])}")
    print('='*60)
    
    opts = {
        'quiet': True,
        'no_warnings': True,
        'extractor_args': {
            'youtube': {
                'player_client': config['clients']
            }
        },
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.youtube.com/',
        },
    }
    
    if config['use_cookies'] and has_firefox:
        opts['cookiesfrombrowser'] = ('firefox',)
    
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(test_url, download=False)
            
            if 'formats' in info:
                # Filter video formats only (has height)
                video_formats = [f for f in info['formats'] if f.get('height')]
                video_formats.sort(key=lambda x: x.get('height', 0), reverse=True)
                
                # Show available resolutions
                resolutions = list(set([f.get('height') for f in video_formats if f.get('height')]))
                resolutions.sort(reverse=True)
                
                print(f"\n[SUCCESS] Found {len(video_formats)} video formats")
                print(f"Available Resolutions: {resolutions}")
                
                # Highlight high-quality formats
                high_quality = [r for r in resolutions if r >= 720]
                if high_quality:
                    print(f"[HIGH QUALITY] Available: {high_quality}")
                else:
                    print(f"[WARNING] No HD formats found! Max resolution: {max(resolutions) if resolutions else 'N/A'}p")
                
                # Show top 10 formats
                print(f"\n{'='*70}")
                print(f"{'ID':8} {'Ext':6} {'Res':8} {'FPS':5} {'Codec':15} {'Filesize':12}")
                print(f"{'='*70}")
                for f in video_formats[:10]:
                    fid = str(f.get('format_id', ''))
                    ext = f.get('ext', '')
                    height = f.get('height', '')
                    res = f"{height}p" if height else ''
                    fps = str(f.get('fps', '')) if f.get('fps') else ''
                    vcodec = f.get('vcodec', '')[:14]
                    fs = f.get('filesize') or f.get('filesize_approx') or ''
                    if isinstance(fs, int):
                        fs = f"{round(fs/1024/1024, 1)}MB"
                    
                    print(f"{fid:8} {ext:6} {res:8} {fps:5} {vcodec:15} {str(fs):12}")
                    
    except Exception as e:
        print(f"[ERROR] {e}")
        continue

print("\n\n" + "="*60)
print("RECOMMENDATION:")
print("="*60)
print("[1] Use the configuration that shows the highest resolutions")
print("[2] Make sure Firefox is installed and you're logged into YouTube")
print("[3] The 'web' client with cookies should give you 1080p, 1440p, 4K")
print("\nIf you only see low resolutions (360p max):")
print("  1. Install Firefox and login to YouTube")
print("  2. Close all Firefox windows before running the script")
print("  3. Make sure you're using 'web' or 'ios' clients (NOT 'mweb')")
