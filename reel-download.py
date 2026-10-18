import json
import re
import time
from flask import Flask, Response, jsonify, render_template_string, request
import yt_dlp

app = Flask(__name__)

# Single-file HTML & CSS Interface with Real-time Progress Bar & Smooth Animation
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Insta Video Downloader</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Roboto, sans-serif; }
        body { background: #0f172a; color: #f8fafc; display: flex; justify-content: center; align-items: center; min-height: 100vh; padding: 20px; }
        .card { background: #1e293b; padding: 25px; border-radius: 16px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); width: 100%; max-width: 520px; }
        h1 { font-size: 24px; margin-bottom: 6px; color: #f43f5e; text-align: center; }
        p.subtitle { font-size: 13px; color: #94a3b8; margin-bottom: 20px; text-align: center; }
        
        /* Tab Switcher */
        .tabs { display: flex; background: #0f172a; border-radius: 8px; padding: 4px; margin-bottom: 20px; border: 1px solid #334155; }
        .tab-btn { flex: 1; padding: 10px; border: none; background: transparent; color: #94a3b8; font-size: 14px; font-weight: 600; cursor: pointer; border-radius: 6px; transition: 0.2s; }
        .tab-btn.active { background: #f43f5e; color: #fff; }

        .form-section { display: none; }
        .form-section.active { display: block; }

        label { display: block; font-size: 13px; font-weight: 600; color: #cbd5e1; margin-bottom: 6px; }
        input[type="text"], textarea { width: 100%; padding: 12px; border-radius: 8px; border: 1px solid #334155; background: #0f172a; color: #fff; font-size: 14px; outline: none; margin-bottom: 16px; }
        input[type="text"]:focus, textarea:focus { border-color: #f43f5e; }
        textarea { height: 110px; resize: vertical; line-height: 1.4; }
        
        button.action-btn { width: 100%; padding: 14px; border: none; border-radius: 8px; background: #f43f5e; color: #fff; font-size: 16px; font-weight: bold; cursor: pointer; transition: 0.2s; }
        button.action-btn:hover { background: #e11d48; }
        button.action-btn:disabled { background: #475569; cursor: not-allowed; }

        /* Progress Bar Styling */
        .progress-container { background: #0f172a; border-radius: 10px; border: 1px solid #334155; overflow: hidden; height: 22px; position: relative; margin-top: 12px; }
        .progress-bar { height: 100%; width: 0%; background: linear-gradient(90deg, #f43f5e, #e11d48); transition: width 0.2s ease-in-out; }
        .progress-text { position: absolute; top: 0; left: 0; width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: bold; color: #fff; text-shadow: 0 0 4px rgba(0,0,0,0.8); }

        /* Status & Logs */
        .status-box { margin-top: 20px; display: none; background: #0f172a; padding: 15px; border-radius: 10px; border: 1px solid #334155; }
        .status-header { font-size: 14px; font-weight: bold; margin-bottom: 8px; color: #38bdf8; display: flex; justify-content: space-between; }
        .log-list { max-height: 160px; overflow-y: auto; font-size: 12px; line-height: 1.5; margin-top: 10px; }
        .log-item { margin-bottom: 6px; border-bottom: 1px solid #1e293b; padding-bottom: 4px; }
        .success { color: #4ade80; }
        .error { color: #f87171; }
        .loading { color: #fba124; }
        .folder-info { margin-top: 12px; background: #1e293b; padding: 10px; border-radius: 8px; font-size: 12px; color: #cbd5e1; border-left: 4px solid #f43f5e; word-break: break-all; }
    </style>
</head>
<body>
    <div class="card">
        <h1>📸 Insta Downloader</h1>
        <p class="subtitle">Select your download mode</p>
        
        <!-- Tab Buttons -->
        <div class="tabs">
            <button class="tab-btn active" onclick="switchTab('single')">1. Single Download</button>
            <button class="tab-btn" onclick="switchTab('batch')">2. Multiple Download</button>
        </div>

        <!-- SECTION 1: Single Download -->
        <div id="single-section" class="form-section active">
            <form id="singleForm">
                <label for="singleUrl">Instagram Video / Reel Link:</label>
                <input type="text" id="singleUrl" placeholder="https://www.instagram.com/reel/..." required autocomplete="off">
                <button type="submit" id="singleBtn" class="action-btn">Download Single Video</button>
            </form>
            <div id="single-status" class="status-box">
                <div id="singleMsg" class="loading">⏳ Connecting...</div>
                
                <div class="progress-container" id="singleProgressContainer">
                    <div class="progress-bar" id="singleProgressBar"></div>
                    <div class="progress-text" id="singleProgressText">0%</div>
                </div>

                <div id="singleFolder" class="folder-info" style="display:none;">
                    📍 <strong>Saved Location:</strong><br><code id="singlePath"></code>
                </div>
            </div>
        </div>

        <!-- SECTION 2: Multiple Download -->
        <div id="batch-section" class="form-section">
            <form id="batchForm">
                <label for="batchUrls">Multiple Links (Newline or Comma separated):</label>
                <textarea id="batchUrls" placeholder="Link 1\nLink 2, Link 3..." required></textarea>
                <button type="submit" id="batchBtn" class="action-btn">Start Batch Queue</button>
            </form>
            <div id="batch-status" class="status-box">
                <div class="status-header">
                    <span id="batchCount">Processing...</span>
                    <span id="batchOverall">0%</span>
                </div>

                <div id="batchCurrentVideo" style="font-size: 12px; color: #fba124; margin-top: 5px; font-weight: 600;">Starting queue...</div>

                <div class="progress-container" id="batchProgressContainer">
                    <div class="progress-bar" id="batchProgressBar"></div>
                    <div class="progress-text" id="batchProgressText">0%</div>
                </div>

                <div id="batchLogList" class="log-list"></div>

                <div id="batchFolderBox" class="folder-info" style="display:none;">
                    📍 <strong>Saved Location:</strong><br><code id="batchPath"></code>
                </div>
            </div>
        </div>
    </div>

    <script>
        function switchTab(tab) {
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.form-section').forEach(s => s.classList.remove('active'));
            
            if(tab === 'single') {
                document.querySelectorAll('.tab-btn')[0].classList.add('active');
                document.getElementById('single-section').classList.add('active');
            } else {
                document.querySelectorAll('.tab-btn')[1].classList.add('active');
                document.getElementById('batch-section').classList.add('active');
            }
        }

        function setProgressBar(barEl, textEl, percent) {
            const p = Math.min(100, Math.max(0, percent));
            barEl.style.width = p + '%';
            textEl.innerText = p.toFixed(1) + '%';
        }

        // Single Download Handler (SSE for Progress)
        document.getElementById('singleForm').addEventListener('submit', function(e) {
            e.preventDefault();
            const urlInput = document.getElementById('singleUrl');
            const btn = document.getElementById('singleBtn');
            const statusBox = document.getElementById('single-status');
            const msg = document.getElementById('singleMsg');
            const bar = document.getElementById('singleProgressBar');
            const text = document.getElementById('singleProgressText');
            const folderBox = document.getElementById('singleFolder');
            const folderPath = document.getElementById('singlePath');

            const url = urlInput.value.trim();
            if(!url) return;

            btn.disabled = true;
            btn.innerText = "Downloading...";
            statusBox.style.display = "block";
            folderBox.style.display = "none";
            msg.className = "loading";
            msg.innerText = "⏳ Connecting to Instagram...";
            setProgressBar(bar, text, 0);

            const eventSource = new EventSource('/stream-single?url=' + encodeURIComponent(url));

            eventSource.onmessage = function(event) {
                const data = JSON.parse(event.data);
                
                if (data.status === 'downloading') {
                    msg.innerText = "⚡ Downloading Video...";
                    setProgressBar(bar, text, data.percent);
                } else if (data.status === 'finished') {
                    setProgressBar(bar, text, 100);
                    msg.className = "success";
                    msg.innerText = "✅ Video Download Completed!";
                    folderPath.innerText = data.save_path;
                    folderBox.style.display = "block";
                    urlInput.value = "";
                    eventSource.close();
                    btn.disabled = false;
                    btn.innerText = "Download Single Video";
                } else if (data.status === 'error') {
                    msg.className = "error";
                    msg.innerText = "❌ Error: " + data.message;
                    eventSource.close();
                    btn.disabled = false;
                    btn.innerText = "Download Single Video";
                }
            };

            eventSource.onerror = function() {
                msg.className = "error";
                msg.innerText = "❌ Download failed or server disconnected!";
                eventSource.close();
                btn.disabled = false;
                btn.innerText = "Download Single Video";
            };
        });

        // Batch Download Handler (SSE for Sequential Animated Progress)
        document.getElementById('batchForm').addEventListener('submit', function(e) {
            e.preventDefault();
            const urlsInput = document.getElementById('batchUrls');
            const btn = document.getElementById('batchBtn');
            const statusBox = document.getElementById('batch-status');
            const count = document.getElementById('batchCount');
            const currentVideo = document.getElementById('batchCurrentVideo');
            const bar = document.getElementById('batchProgressBar');
            const text = document.getElementById('batchProgressText');
            const logList = document.getElementById('batchLogList');
            const folderBox = document.getElementById('batchFolderBox');
            const folderPath = document.getElementById('batchPath');

            const rawText = urlsInput.value.trim();
            if(!rawText) return;

            btn.disabled = true;
            btn.innerText = "Processing Queue...";
            statusBox.style.display = "block";
            folderBox.style.display = "none";
            logList.innerHTML = "";
            setProgressBar(bar, text, 0);

            const eventSource = new EventSource('/stream-batch?raw_text=' + encodeURIComponent(rawText));

            eventSource.onmessage = function(event) {
                const data = JSON.parse(event.data);

                if (data.status === 'start_video') {
                    count.innerText = `Downloading Video (${data.index}/${data.total})`;
                    currentVideo.innerText = `⏳ Video ${data.index}: Downloading (0%)`;
                    setProgressBar(bar, text, 0);
                } else if (data.status === 'downloading') {
                    currentVideo.innerText = `⚡ Video ${data.index}: Downloading (${data.percent.toFixed(1)}%)`;
                    setProgressBar(bar, text, data.percent);
                } else if (data.status === 'video_complete') {
                    setProgressBar(bar, text, 100);
                    currentVideo.innerText = `✅ Video ${data.index}: Download Complete!`;
                    
                    const logItem = document.createElement('div');
                    logItem.className = 'log-item success';
                    logItem.innerHTML = `✅ <strong>Video ${data.index}</strong> download complete (100%)`;
                    logList.appendChild(logItem);
                    logList.scrollTop = logList.scrollHeight;
                } else if (data.status === 'video_error') {
                    const logItem = document.createElement('div');
                    logItem.className = 'log-item error';
                    logItem.innerHTML = `❌ <strong>Video ${data.index}</strong> failed: ${data.message}`;
                    logList.appendChild(logItem);
                    logList.scrollTop = logList.scrollHeight;
                } else if (data.status === 'finished') {
                    count.innerText = `Finished (${data.success_count}/${data.total} Completed)`;
                    currentVideo.innerText = "🎉 All Downloads Completed!";
                    folderPath.innerText = data.save_path;
                    folderBox.style.display = "block";
                    urlsInput.value = "";
                    eventSource.close();
                    btn.disabled = false;
                    btn.innerText = "Start Batch Queue";
                } else if (data.status === 'error') {
                    currentVideo.innerText = "❌ Error occurred";
                    const logItem = document.createElement('div');
                    logItem.className = 'log-item error';
                    logItem.innerHTML = `❌ ${data.message}`;
                    logList.appendChild(logItem);
                    eventSource.close();
                    btn.disabled = false;
                    btn.innerText = "Start Batch Queue";
                }
            };

            eventSource.onerror = function() {
                currentVideo.innerText = "❌ Connection Error!";
                eventSource.close();
                btn.disabled = false;
                btn.innerText = "Start Batch Queue";
            };
        });
    </script>
</body>
</html>
"""


@app.route("/")
def index():
  return render_template_string(HTML_TEMPLATE)


@app.route("/stream-single")
def stream_single():
  url = request.args.get("url", "").strip()

  def generate():
    if not url:
      yield f"data: {json.dumps({'status': 'error', 'message': 'URL is required!'})}\n\n"
      return

    download_folder = "/sdcard/Download"

    def progress_hook(d):
      if d["status"] == "downloading":
        total = d.get("total_bytes") or d.get("total_bytes_estimate") or 0
        downloaded = d.get("downloaded_bytes", 0)
        percent = (downloaded / total * 100) if total > 0 else 0
        progress_data = {"status": "downloading", "percent": round(percent, 1)}
        yield_data = f"data: {json.dumps(progress_data)}\n\n"
        # store in non-local variable or send directly via yield trick
        progress_hook.last_data = yield_data

    progress_hook.last_data = None

    def my_hook(d):
      if d["status"] == "downloading":
        total = d.get("total_bytes") or d.get("total_bytes_estimate") or 0
        downloaded = d.get("downloaded_bytes", 0)
        percent = (downloaded / total * 100) if total > 0 else 0
        progress_hook.last_data = f"data: {json.dumps({'status': 'downloading', 'percent': round(percent, 1)})}\n\n"

    ydl_opts = {
        "format": "best",
        "outtmpl": f"{download_folder}/%(title)s.%(ext)s",
        "quiet": True,
        "no_warnings": True,
        "progress_hooks": [my_hook],
    }

    try:
      with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # We run download in thread-like sequence yielding updates
        def run_dl():
          ydl.download([url])

        import threading

        t = threading.Thread(target=run_dl)
        t.start()

        while t.is_alive():
          if progress_hook.last_data:
            yield progress_hook.last_data
            progress_hook.last_data = None
          time.sleep(0.2)

        t.join()

      yield (
          f"data:"
          f" {json.dumps({'status': 'finished', 'save_path': download_folder + ' (Phone Internal Storage/Download)'})}\n\n"
      )
    except Exception as e:
      yield f"data: {json.dumps({'status': 'error', 'message': str(e)})}\n\n"

  return Response(generate(), mimetype="text/event-stream")


@app.route("/stream-batch")
def stream_batch():
  raw_text = request.args.get("raw_text", "").strip()

  def generate():
    if not raw_text:
      yield f"data: {json.dumps({'status': 'error', 'message': 'No links provided!'})}\n\n"
      return

    urls = re.findall(r"https?://[^\s,]+", raw_text)
    if not urls:
      yield f"data: {json.dumps({'status': 'error', 'message': 'No valid URLs found!'})}\n\n"
      return

    download_folder = "/sdcard/Download"
    total_videos = len(urls)
    success_count = 0

    for idx, url in enumerate(urls, 1):
      yield f"data: {json.dumps({'status': 'start_video', 'index': idx, 'total': total_videos})}\n\n"

      progress_data_holder = {"last": None}

      def my_hook(d):
        if d["status"] == "downloading":
          total = d.get("total_bytes") or d.get("total_bytes_estimate") or 0
          downloaded = d.get("downloaded_bytes", 0)
          percent = (downloaded / total * 100) if total > 0 else 0
          progress_data_holder["last"] = f"data: {json.dumps({'status': 'downloading', 'index': idx, 'percent': round(percent, 1)})}\n\n"

      ydl_opts = {
          "format": "best",
          "outtmpl": f"{download_folder}/%(title)s.%(ext)s",
          "quiet": True,
          "no_warnings": True,
          "progress_hooks": [my_hook],
      }

      try:

        def run_dl():
          yt_dlp.YoutubeDL(ydl_opts).download([url])

        import threading

        t = threading.Thread(target=run_dl)
        t.start()

        while t.is_alive():
          if progress_data_holder["last"]:
            yield progress_data_holder["last"]
            progress_data_holder["last"] = None
          time.sleep(0.2)

        t.join()

        success_count += 1
        yield f"data: {json.dumps({'status': 'video_complete', 'index': idx})}\n\n"
      except Exception as e:
        yield f"data: {json.dumps({'status': 'video_error', 'index': idx, 'message': str(e)})}\n\n"

    yield (
        f"data:"
        f" {json.dumps({'status': 'finished', 'total': total_videos, 'success_count': success_count, 'save_path': download_folder + ' (Phone Internal Storage/Download)'})}\n\n"
    )

  return Response(generate(), mimetype="text/event-stream")


if __name__ == "__main__":
  print("\n🚀 Server running on http://localhost:5000\n")
  app.run(host="0.0.0.0", port=5000, debug=False)