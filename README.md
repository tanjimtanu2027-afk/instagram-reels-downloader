# Instagram Reel Downloader

A Flask-based web app with a beautiful dark-themed UI for downloading Instagram Reels. Supports single and batch (multiple) downloads with real-time progress bars via Server-Sent Events (SSE). Videos are saved to your phone's Download folder using yt-dlp.

## Features

- **Single Download**: Paste one Instagram Reel link and download instantly
- **Batch Download**: Paste multiple links (newline or comma separated) and download them all at once
- **Live Progress**: Real-time percentage progress bars with smooth animation
- **Zero Config**: Works out of the box on Android via Termux

## Setup Guide (New Users)

If you want to run this on your Android phone, follow the steps below:

### Step 1: Install Termux App
Install Termux from **F-Droid** or GitHub (the Google Play Store version is outdated).

### Step 2: Grant Storage Permission & Install Packages
Open Termux and run these commands one by one:

```bash
# 1. Update and upgrade Termux
pkg update && pkg upgrade -y

# 2. Grant storage permission (so videos save to your Download folder)
termux-setup-storage

# 3. Install Git, Python, and FFmpeg (required for repository cloning and video processing)
pkg install git python ffmpeg -y
```

*(After running the storage command, your phone will ask for permission — tap Allow.)*

### Step 3: Install Required Python Libraries
```bash
pip install flask yt-dlp
```

### Step 4: Clone the Repository
- Clone the project files from GitHub:
  ```bash
  git clone https://github.com/tanjimtanu2027-afk/instagram-reels-downloader
  ```

### Step 5: Run the Server
- Enter the project directory:
  ```bash
  cd instagram-reels-downloader
  ```
- Start the server:
  ```bash
  python reel-download..py
  ```

(Once started, you will see a local link: http://localhost:5000)

### Step 6: Open in Browser
- Open any web browser on your phone (e.g., Chrome).
- Go to: **http://localhost:5000**
- The app will load with a clean UI. Choose between **Single Download** or **Multiple Batch Download** (both show live 0–100% progress animations). Videos are saved directly to your phone's **Download** folder.

---

Enjoy! 🎉
