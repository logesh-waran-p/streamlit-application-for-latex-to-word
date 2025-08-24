
FROM python:3.11-slim

# Install system dependencies (pandoc + fonts + minimal TeX utilities if needed)
RUN apt-get update && apt-get install -y --no-install-recommends \        pandoc \        && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy files
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py /app/

# Expose port (HF Spaces uses $PORT)
ENV PORT=7860
CMD streamlit run app.py --server.port $PORT --server.address 0.0.0.0
