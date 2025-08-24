import streamlit as st
import subprocess
import tempfile
import os
import shutil

st.set_page_config(page_title="LaTeX → Word (.docx) Converter", page_icon="📄", layout="centered")
st.title("📄 LaTeX → Word (.docx) Converter")
st.caption("Upload a **.tex** file, convert it with Pandoc, and download a Word document. Equations are preserved.")

def get_next_available_filename(base_path: str) -> str:
    directory, base_filename = os.path.split(base_path)
    filename, ext = os.path.splitext(base_filename)
    if not os.path.exists(base_path):
        return base_path
    counter = 1
    while True:
        new_filename = f"{filename}{counter}{ext}"
        new_path = os.path.join(directory, new_filename)
        if not os.path.exists(new_path):
            return new_path
        counter += 1

def pandoc_available() -> bool:
    return shutil.which("pandoc") is not None

st.sidebar.header("⚙️ Options")
output_basename: str = st.sidebar.text_input(
    "Output filename (no extension)",
    value="output",
    help="We'll append .docx automatically. If a name exists, a number is added to avoid overwrite.",
)
include_mathml = st.sidebar.checkbox(
    "Use --mathml flag",
    value=True,
    help=(
        "Keeps LaTeX equations as MathML during conversion. For DOCX, Pandoc typically emits Office Math; "
        "this flag usually doesn't hurt. You can uncheck if you prefer the default."
    ),
)

uploaded_tex = st.file_uploader("Upload your LaTeX file (.tex)", type=["tex"], accept_multiple_files=False)
convert_clicked = st.button("Convert to .docx", type="primary", use_container_width=True)

if convert_clicked:
    if not uploaded_tex:
        st.warning("Please upload a .tex file first.")
        st.stop()

    if not pandoc_available():
        st.error(
            "Pandoc is not installed on the server where this app runs. "
            "If you're on Streamlit Cloud, add 'pandoc' to packages.txt (included in this repo). "
            "If running locally, install from https://pandoc.org/."
        )
        st.stop()

    with st.status("Converting…", expanded=True) as status_box:
        st.write("① Saving uploaded file…")
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, uploaded_tex.name or "main.tex")
            tex_bytes = uploaded_tex.read()
            with open(input_path, "wb") as f:
                f.write(tex_bytes)

            out_name = (output_basename or "output").rstrip(". ") + ".docx"
            out_path = get_next_available_filename(os.path.join(tmpdir, out_name))

            cmd = ["pandoc", input_path, "-o", out_path]
            if include_mathml:
                cmd.append("--mathml")

            st.write("② Running Pandoc:")
            st.code(" ".join(cmd))

            try:
                subprocess.run(cmd, check=True)
                st.write("③ Reading output bytes…")
                with open(out_path, "rb") as f:
                    docx_data = f.read()
                status_box.update(label="✅ Conversion complete", state="complete")

                st.success("Your Word file is ready.")
                dl_name = os.path.basename(out_path)
                st.download_button(
                    label="Download .docx",
                    data=docx_data,
                    file_name=dl_name,
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True,
                )

            except subprocess.CalledProcessError as e:
                status_box.update(label="❌ Conversion failed", state="error")
                st.error(f"Pandoc returned an error. Details: {e}")

with st.expander("ℹ️ Tips for reliable conversion"):
    st.markdown(
        "- If your project uses multiple files (\\input/\\include), upload a single flattened `main.tex` that already resolves those, or host/deploy this app where it can access the project folder.\n"
        "- Image/figure paths must be valid relative to the uploaded file.\n"
        "- For bibliographies (`.bib`) and citations, Pandoc may need extra flags/filters; this simple app focuses on single-file conversions.\n"
        "- If equations look off in Word, try toggling the **--mathml** option above."
    )
