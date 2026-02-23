# Video Downloader

A Python-based desktop application for downloading videos and audio from social media platforms including YouTube, TikTok, Instagram, and more.

## Features

- **Multi-platform Support**: Download videos from YouTube, TikTok, Instagram, and hundreds of other platforms
- **Dual Format Support**:
  - Download complete videos with audio
  - Extract and save audio as MP3
- **Quality Selection**: Choose from available video qualities (1080p, 720p, 480p, 360p, etc.)
- **Progress Tracking**: Real-time download progress display
- **Easy to Use**: Simple GUI with intuitive controls
- **Automatic Storage**: Downloaded files are saved directly to your Windows Downloads folder

## System Requirements

- **Python**: 3.6 or higher (tested with Python 3.13)
- **Operating System**: Windows 7 or higher
- **Internet**: Active internet connection for downloading videos

## Installation

### Step 1: Install Dependencies

Open Command Prompt or PowerShell and run:

```bash
cd "C:\Users\강주혁\Desktop\03_APP\04_Downloader\VideoDownloader"
pip install -r requirements.txt
```

This will install the required packages:
- **yt-dlp**: Universal video downloader

**Note**: `yt-dlp` may require FFmpeg for MP3 conversion. If you get an error about FFmpeg, install it using:
```bash
pip install yt-dlp[default]
```

### Step 2: Run the Application

#### Option A: Using the batch file (Recommended for Windows)
Double-click the `run.bat` file in the project folder.

#### Option B: Using Command Line
```bash
python video_downloader.py
```

## Usage Guide

### Basic Download Process

1. **Launch the application** using `run.bat` or `python video_downloader.py`

2. **Paste the video URL** into the input field
   - Supported URLs include:
     - YouTube videos: https://www.youtube.com/watch?v=...
     - YouTube Shorts: https://youtube.com/shorts/...
     - TikTok videos: https://www.tiktok.com/@user/video/...
     - Instagram videos: https://www.instagram.com/p/...
     - And many more platforms

3. **Click the "Download" button**

4. **Select download type**:
   - **Video (with audio)**: Download the full video
   - **MP3 (audio only)**: Extract and download just the audio as MP3

5. **For video downloads**:
   - The app will fetch available qualities
   - Select your preferred quality (higher numbers = better quality, larger file size)
   - Click "Download" to start

6. **Monitor progress**:
   - Watch the progress bar to see download status
   - Check the status log for detailed messages

7. **Find your file**:
   - Completed downloads are automatically saved to your Downloads folder
   - A notification will appear when the download is complete

### Quality Selection

When downloading videos, you'll see quality options like:
- **1080p (MP4)**: Full HD, largest file size, highest quality
- **720p (MP4)**: HD quality, recommended for most users
- **480p (WebM)**: Standard definition, smaller file size
- **360p (WebM)**: Low quality, smallest file size

**Tip**: Choose 720p for a good balance between quality and file size.

## Features Explained

### URL Input Field
- Paste any supported video URL
- The app will validate the URL format before attempting download

### Progress Bar
- Shows real-time download progress
- Percentage display updates during download
- Reaches 100% when download is complete

### Status Log
- Displays detailed messages about the download process
- Shows errors or warnings if something goes wrong
- Helpful for troubleshooting

## Troubleshooting

### "Invalid URL" Error
- Make sure you're copying the full URL from the browser address bar
- Ensure the URL starts with `http://` or `https://`
- Check if the URL contains the full video link (not a shortened URL)

### "No video formats available"
- The video might be age-restricted or private
- Try a different video
- Check if the video is available in your region

### Download fails with network error
- Check your internet connection
- Wait a moment and try again
- Some videos may have download restrictions

### Slow download speed
- This depends on:
  - Your internet connection speed
  - The video server's speed
  - The video quality (higher quality = slower download)
- Nothing can be done in the app to improve this

### FFmpeg error (for MP3 downloads)
- The app uses FFmpeg to convert audio to MP3
- Install FFmpeg manually from: https://ffmpeg.org/download.html
- Or reinstall with: `pip install yt-dlp[default]`

### No sound in downloaded video
- This sometimes happens with certain platforms
- Try downloading at a lower quality
- Try a different video to verify the app works

## File Structure

```
VideoDownloader/
├── video_downloader.py       # Main application file
├── requirements.txt          # Python dependencies
├── README.md                 # This file
└── run.bat                   # Windows batch file to run the app
```

## Supported Platforms

The application supports 100+ video platforms including:

- ✓ YouTube (videos, shorts, playlists)
- ✓ TikTok
- ✓ Instagram (Reels, videos)
- ✓ Facebook
- ✓ Twitter/X
- ✓ Reddit
- ✓ Twitch
- ✓ Vimeo
- ✓ Dailymotion
- ✓ And many more...

See the [yt-dlp documentation](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md) for a complete list.

## Technical Details

### How It Works

1. **URL Validation**: The app validates the URL format
2. **Format Detection**: When you select "Video", it queries the video server for available formats
3. **Download**: Uses yt-dlp to download the selected format
4. **Conversion** (MP3 only): Uses FFmpeg to convert audio to MP3 format
5. **Storage**: Saves files to `C:\Users\YourUsername\Downloads\`

### Output Format

- **Videos**: Saved as MP4 or WebM (depending on availability)
- **Audio**: Converted to MP3 format (192 kbps quality)
- **Filename**: Original video title is used as filename

## Security & Privacy

- The app only downloads publicly available videos
- It does not modify, analyze, or store any personal data
- Downloaded files are stored locally on your computer
- No internet connection is required after the download completes

## Known Limitations

- Age-restricted videos may require authentication
- Private videos cannot be downloaded
- Some platforms may block automated downloads
- Geographic restrictions apply as per the content owner's settings

## Tips & Best Practices

1. **Check available space**: Videos can be large, ensure you have enough disk space
2. **Use reasonable quality**: 720p is a good balance for most videos
3. **Legal usage**: Only download content you have permission to download
4. **Large files**: Very long videos (hours) will take significant time and space to download
5. **Interrupted downloads**: The app will overwrite partial downloads if you retry the same video

## License

This application uses yt-dlp, which is licensed under the Unlicense.

## Support

For issues or feature requests, please check:
- The troubleshooting section above
- The [yt-dlp GitHub repository](https://github.com/yt-dlp/yt-dlp)

## Version History

- **v1.0** (2026-02-15): Initial release
  - Video and MP3 download support
  - Quality selection dialog
  - Progress tracking
  - Status logging
  - Windows integration

## Future Enhancements

Potential features for future versions:
- Batch downloading (multiple URLs at once)
- Download history/favorites
- Thumbnail preview
- Subtitle downloading
- Custom output folder selection
- Download queue management
# youtube_downloader-
# youtube_downloader-
