import streamlit as st
import subprocess, shutil, tempfile, os

st.set_page_config(page_title="LaTeX → Word (.docx)", page_icon="📄", layout="centered")
st.title("📄 LaTeX → Word (.docx)")
st.caption("Upload a .tex file, convert with Pandoc, and download a .docx.")

def get_next_available_filename(base_path: str) -> str:
    d, b = os.path.split(base_path)
    name, ext = os.path.splitext(b)
    if not os.path.exists(base_path):
        return base_path
    i = 1
    while True:
        p = os.path.join(d, f"{name}{i}{ext}")
        if not os.path.exists(p):
            return p
        i += 1

def pandoc_available() -> bool:
    return shutil.which("pandoc") is not None

st.sidebar.header("⚙️ Options")
output_basename = st.sidebar.text_input("Output filename (no extension)", "output")
use_mathml = st.sidebar.checkbox("Use --mathml", value=True)

st.write({"pandoc_path": shutil.which("pandoc")})

uploaded_tex = st.file_uploader("Upload .tex", type=["tex"])
if st.button("Convert", type="primary"):
    if not uploaded_tex:
        st.warning("Please upload a .tex file first.")
        st.stop()
    if not pandoc_available():
        st.error("Pandoc is not installed in this container.")
        st.stop()

    with tempfile.TemporaryDirectory() as tmp:
        in_path = os.path.join(tmp, uploaded_tex.name or "main.tex")
        with open(in_path, "wb") as f:
            f.write(uploaded_tex.read())
        out_path = get_next_available_filename(os.path.join(tmp, (output_basename or "output") + ".docx"))
        cmd = ["pandoc", in_path, "-o", out_path]
        if use_mathml:
            cmd.append("--mathml")
        st.code(" ".join(cmd))
        try:
            subprocess.run(cmd, check=True)
            with open(out_path, "rb") as f:
                st.download_button("Download .docx", f, file_name=os.path.basename(out_path),
                                   mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
            st.success("Done")
        except subprocess.CalledProcessError as e:
            st.error(f"Pandoc failed: {e}")
