## New User-der Jonno Setup Guide

### Step 1: Termux App Install Korun

Prothome phone-e Termux app (F-Droid ba GitHub theke updated version) install korte hobe (Google Play Store-er version-ti ekhon outdated).

### Step 2: Storage Permission & Packages Install Korun

Termux open kore nicher command-gulo ekta ekta kore run korun:

```bash
# 1. Termux update and upgrade korun
pkg update && pkg upgrade -y

# 2. Phone storage permission din (Jate video Download folder-e save hoy)
termux-setup-storage

# 3. Python ebong FFmpeg (Video processing-er jonno mandatory) install korun
pkg install python ffmpeg -y
```

(Storage command dile phone theke permission chaibe, seta Allow kore dite hobe).

### Step 3: Required Python Libraries Install Korun

Ebar python-er server ebong downloader libraries-gulo install korte hobe:

```bash
pip install flask yt-dlp
```

### Step 4: app.py File Toiri Korun

* Termux-e ekta notun file open korun:
  ```bash
  nano app.py
  ```

* Apnar kache thaka full code-ti (jei code-ti ekhon amra use korchi) copy kore oi Nano editor-e paste kore din.
* Save korar jonno: Keyboard theke **Ctrl + x** chapaun, tarpor **y** din, shese **Enter** press korun.

### Step 5: Server Run Korun

File save howar por server start korar jonno run korun:

```bash
python app.py
```

(Server start hole ekti local link show korbe: http://localhost:5000)

### Step 6: Browser theke Use Korun

* Apnar phone-er jekono web browser (jemon Google Chrome) open korun.
* Address bar-e likhun: **http://localhost:5000**
* Besh! Ebar samne sundor UI chole asbe jekhan theke Single Download ba Multiple Batch Download (0%-100% live animation soho) use kore direct phone-er Download folder-e video namiye nite parben.

---

Ei steps-gulo follow korlei jekono new user khub sahajjei eta nijer phone-e chaliye nite parbe!

---

## Apnar ei project-ti ekdom complete ebong darun ekta application hoyeche! 🚀

Kono new user jodi apnar ei Instagram Downloader-ti nijer phone-e setup kore use korte chay, tahole take prothome Termux-er maddhome kichu basic setup kore nite hobe. Niche new user-der jonno ekta complete step-by-step guide deya holo, apnake jara eta use korte chaibe tader apni eta dite paren:

### New User-der Jonno Setup Guide:

#### Step 1: Termux App Install Korun

Prothome phone-e Termux app (F-Droid ba GitHub theke updated version) install korte hobe (Google Play Store-er version-ti ekhon outdated).

#### Step 2: Storage Permission & Packages Install Korun

Termux open kore nicher command-gulo ekta ekta kore run korun:

```bash
# 1. Termux update and upgrade korun
pkg update && pkg upgrade -y

# 2. Phone storage permission din (Jate video Download folder-e save hoy)
termux-setup-storage

# 3. Python ebong FFmpeg (Video processing-er jonno mandatory) install korun
pkg install python ffmpeg -y
```

(Storage command dile phone theke permission chaibe, seta Allow kore dite hobe).

#### Step 3: Required Python Libraries Install Korun

Ebar python-er server ebong downloader libraries-gulo install korte hobe:

```bash
pip install flask yt-dlp
```

#### Step 4: app.py File Toiri Korun

- Termux-e ekta notun file open korun:
  ```bash
  nano app.py
  ```
- Apnar kache thaka full code-ti (jei code-ti ekhon amra use korchi) copy kore oi Nano editor-e paste kore din.
- Save korar jonno: Keyboard theke **Ctrl + x** chapaun, tarpor **y** din, shese **Enter** press korun.

#### Step 5: Server Run Korun

File save howar por server start korar jonno run korun:

```bash
python app.py
```

(Server start hole ekti local link show korbe: http://localhost:5000)

#### Step 6: Browser theke Use Korun

- Apnar phone-er jekono web browser (jemon Google Chrome) open korun.
- Address bar-e likhun: **http://localhost:5000**
- Besh! Ebar samne sundor UI chole asbe jekhan theke Single Download ba Multiple Batch Download (0%-100% live animation soho) use kore direct phone-er Download folder-e video namiye nite parben.

---

Ei steps-gulo follow korlei jekono new user khub sahajjei eta nijer phone-e chaliye nite parbe!
