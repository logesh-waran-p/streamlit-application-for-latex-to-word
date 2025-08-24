# LaTeX → Word (.docx) Converter (Streamlit)

Simple Streamlit app that converts a `.tex` file to `.docx` using **Pandoc**.

## Files
- `app.py` — Streamlit app
- `requirements.txt` — Python deps
- `packages.txt` — System packages for Streamlit Cloud (installs `pandoc`)

## Run locally
```bash
pip install -r requirements.txt
# Install Pandoc from https://pandoc.org/ (or your OS package manager)
streamlit run app.py
```

## Deploy on Streamlit Community Cloud
1. Push these files to a **public GitHub repo**.
2. Go to Streamlit Cloud → **New app** → select your repo/branch.
3. The build will install Python packages from `requirements.txt` and system packages from `packages.txt` (this installs `pandoc`).
4. Launch the app.

## Notes
- If your LaTeX project uses `\input`/`\include`, flatten it into a single `main.tex` before uploading (or extend the app to accept a zip).
- Toggle the **--mathml** checkbox if equation rendering looks off in Word.
