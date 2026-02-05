FROM python:3.11-slim

# --- Metadata ---
LABEL maintainer="ResumeForge"
LABEL description="ResumeForge - Resume Extraction & Formatting Tool"

# --- System deps ---
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# --- Working directory ---
WORKDIR /app

# --- Install Python deps (cached layer) ---
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- Copy app code ---
COPY app.py .
COPY db.py .

# --- Create persistent data directory ---
RUN mkdir -p /app/data

# --- Streamlit config (headless, no browser, CORS) ---
RUN mkdir -p /root/.streamlit
RUN echo '\
[server]\n\
headless = true\n\
port = 8501\n\
address = "0.0.0.0"\n\
enableCORS = false\n\
enableXsrfProtection = false\n\
maxUploadSize = 50\n\
\n\
[browser]\n\
gatherUsageStats = false\n\
\n\
[theme]\n\
base = "dark"\n\
' > /root/.streamlit/config.toml

# --- Expose port ---
EXPOSE 8501

# --- Health check ---
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# --- Run ---
ENTRYPOINT ["streamlit", "run", "app.py"]