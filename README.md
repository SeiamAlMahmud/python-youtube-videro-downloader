# YouTube Downloader - How to Get HD Quality (2026)

## ⚠️ IMPORTANT: YouTube Changed in 2026!

**Browser cookies are NOW REQUIRED for HD quality (720p, 1080p, etc.)**

YouTube now blocks HD downloads unless you're logged in through a browser.

## 🚀 Quick Setup (DO THIS FIRST)

### 1. Install Firefox Browser
Download: https://www.mozilla.org/firefox/

### 2. Login to YouTube in Firefox
1. Open Firefox
2. Go to youtube.com
3. **Login with your Google account**
4. Watch any video to test
5. **CLOSE all Firefox windows**

### 3. Run the Downloader
```bash
python ytdownload.py
```

### 4. Answer YES to cookies
```
Use browser cookies? (RECOMMENDED for HD - Y/n): y
```

## ✅ That's It!

You'll now see HD formats (720p, 1080p, etc.) available for download!

## 📖 Full Example

```bash
python ytdownload.py

# Output:
=== YouTube Video Downloader (2026 Updated) ===
[INFO] Found Firefox browser

YouTube Video Link: https://youtube.com/watch?v=gA-4fA_7kc8
Use browser cookies? (RECOMMENDED for HD - Y/n): y

[FETCHING] Getting available formats...
[INFO] Using Firefox cookies

Available formats for: Master AI Coding...
format_id  ext   res     vcodec       acodec       filesize
22         mp4   720p    avc1.64001F  mp4a.40.2    95.4MB
18         mp4   360p    avc1.42001E  mp4a.40.2    35.2MB

Enter format id, max resolution (e.g., 1080), or type 'best':
Choice: 720

[DOWNLOADING] ...
[SUCCESS] Download & Data Save Complete!
```

## ❓ Troubleshooting

### Q: Still showing only 360p?

**A: Make sure:**
1. Firefox is installed ✓
2. You're logged into YouTube in Firefox ✓
3. Firefox is COMPLETELY closed (check Task Manager) ✓
4. You answered 'y' to "Use browser cookies?" ✓

### Q: "Could not load browser cookies" error?

**A:**
1. Close ALL Firefox windows
2. Check Task Manager and end any Firefox processes
3. Restart your terminal
4. Try again

### Q: Can I use Chrome instead of Firefox?

**A:** Yes, but Firefox works better. If you want Chrome:
1. Make sure Chrome is completely closed
2. The script will auto-detect and use Chrome cookies

### Q: Do I need to be logged in every time?

**A:** No! Once you login to YouTube in Firefox, you stay logged in. Just:
1. Close Firefox before running the script
2. Answer 'y' to cookies
3. That's it!

### Q: Why does it need my login?

**A:** The script uses your browser cookies to prove to YouTube that you're a real person, not a bot. It's the same as if you were watching in your browser. Your login info is NOT sent anywhere - it just uses the cookies already saved by Firefox.

## 🎯 Summary

| Without Firefox Cookies | With Firefox Cookies |
|------------------------|---------------------|
| ❌ Only 360p or lower | ✅ 720p, 1080p, 1440p, 4K |
| ❌ Many errors | ✅ Works reliably |
| ❌ "Sign in" errors | ✅ Authenticated |

**Bottom line:** Install Firefox, login to YouTube, close Firefox, run the script with cookies = HD downloads! 🎉

---

For technical details, see: [`RESOLUTION_FIX.md`](RESOLUTION_FIX.md)
