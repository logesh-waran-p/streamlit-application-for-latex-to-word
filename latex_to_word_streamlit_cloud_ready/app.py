
import streamlit as st
import subprocess, shutil, platform, sys, tempfile, os

st.set_page_config(page_title="LaTeX → DOCX (with diagnostics)", page_icon="🧪")
st.title("🧪 LaTeX → DOCX (with diagnostics)")

# --- Diagnostics panel ---
st.subheader("Environment diagnostics")
pandoc_path = shutil.which("pandoc")
st.write({"pandoc_path": pandoc_path, "python": sys.version, "platform": platform.platform()})
if pandoc_path:
    try:
        out = subprocess.check_output(["pandoc", "-v"], stderr=subprocess.STDOUT).decode("utf-8", "ignore").splitlines()[0]
    except Exception as e:
        out = f"pandoc -v failed: {e}"
    st.write({"pandoc_version": out})
else:
    st.error("Pandoc not found on PATH. Cloud should install it via packages.txt at repo root.")

st.divider()

st.caption("Upload a .tex file, convert via Pandoc, and download .docx")
output_basename = st.sidebar.text_input("Output filename (no extension)", "output")
use_mathml = st.sidebar.checkbox("Use --mathml", value=True)

uploaded_tex = st.file_uploader("Upload .tex", type=["tex"])
if st.button("Convert", type="primary"):
    if not uploaded_tex:
        st.warning("Please upload a .tex file first.")
        st.stop()
    if not pandoc_path:
        st.error("Pandoc still missing. See diagnostics above.")
        st.stop()

    with tempfile.TemporaryDirectory() as tmp:
        in_path = os.path.join(tmp, uploaded_tex.name or "main.tex")
        with open(in_path, "wb") as f:
            f.write(uploaded_tex.read())
        out_path = os.path.join(tmp, (output_basename or "output") + ".docx")

        cmd = ["pandoc", in_path, "-o", out_path]
        if use_mathml:
            cmd.append("--mathml")
        st.code(" ".join(cmd))

        try:
            subprocess.run(cmd, check=True)
            st.success("Done")
            with open(out_path, "rb") as f:
                st.download_button("Download .docx", f, file_name=os.path.basename(out_path),
                                   mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        except subprocess.CalledProcessError as e:
            st.error(f"Pandoc failed: {e}")
