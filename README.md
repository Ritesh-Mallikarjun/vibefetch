# ⚡ VibeFetch — Deployment Guide
### By Ritesh Mallikarjun | github.com/Ritesh-Mallikarjun

---

## 📁 Files in this repo

| File | Purpose |
|------|---------|
| `index.html` | The frontend website |
| `server.py` | The Python backend (handles downloads) |
| `requirements.txt` | Python packages |
| `Procfile` | Tells Railway how to start the server |
| `runtime.txt` | Python version |
| `nixpacks.toml` | Tells Railway to install FFmpeg |

---

## 🚀 STEP 1 — Upload to GitHub

1. Go to https://github.com/Ritesh-Mallikarjun
2. Click **"New repository"**
3. Name it: `vibefetch`
4. Set it to **Public**
5. Click **"Create repository"**
6. Upload ALL files from this folder (drag & drop them)
7. Click **"Commit changes"**

---

## 🖥️ STEP 2 — Deploy Backend on Railway

1. Go to https://railway.app
2. Click **"Start a New Project"**
3. Sign in with your **GitHub account** (Ritesh-Mallikarjun)
4. Click **"Deploy from GitHub repo"**
5. Select your **vibefetch** repository
6. Railway will auto-detect Python and start building
7. Wait ~2 minutes for the build to complete
8. Once live, click your project → **Settings** → **Networking** → **Generate Domain**
9. Copy your Railway URL — it looks like:
   `https://vibefetch-production-xxxx.up.railway.app`

---

## ✏️ STEP 3 — Update Your Frontend URL

1. Open `index.html` in any text editor (Notepad is fine)
2. Find this line (near the bottom in the script):
   ```
   const API_BASE = 'https://YOUR-RAILWAY-URL.up.railway.app';
   ```
3. Replace `YOUR-RAILWAY-URL` with your actual Railway URL
4. Save the file
5. Go back to GitHub → your vibefetch repo → click `index.html` → Edit → paste updated content → Commit

---

## 🌐 STEP 4 — Deploy Frontend on Netlify

1. Go to https://netlify.com
2. Sign up free (use GitHub login)
3. Click **"Add new site"** → **"Deploy manually"**
4. Drag and drop ONLY the `index.html` file
5. Netlify gives you a random URL — click **"Site settings"** → **"Change site name"**
6. Type: `ritesh-mallikarjun` → Save
7. Your site is now live at:
   🎉 **https://ritesh-mallikarjun.netlify.app**

---

## ✅ Final Check

Visit your Netlify URL, paste a YouTube link, and test a download.
If it works — you're live for the whole world! 🌍

---

## 🆘 Troubleshooting

**Download fails / CORS error:**
→ Make sure Railway backend is running (check Railway dashboard logs)
→ Make sure `API_BASE` in index.html matches your Railway URL exactly

**FFmpeg not found error on Railway:**
→ The `nixpacks.toml` file handles this automatically. If issues persist, go to Railway → Variables → add: `NIX_PACKAGES = ffmpeg`

**Railway server sleeping:**
→ Railway free tier stays awake. If you ever switch to Render, note it sleeps after 15min.
