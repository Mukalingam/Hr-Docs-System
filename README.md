# 🔮 ResumeForge

Resume extraction and formatting tool built with Streamlit. Upload a candidate resume and a format template — the system automatically extracts, maps, and generates formatted CV documents.

---

## Features

- **Login System** — Role-based auth with admin and user roles
- **Upload & Preview** — Drag-and-drop for PDF / DOCX with in-app text preview
- **Smart Extraction** — Reads resume and maps data to the required template structure
- **Structured View** — Identification, Contact, Skills, Education, Work Experience
- **Download** — Generated Word (.docx) and PDF documents
- **History** — All past extractions saved and accessible from the sidebar
- **Admin Panel** — Manage users (add/view) from the sidebar
- **Dockerized** — Ready for AWS ECR + EC2 deployment

---

## Quick Start (Local)

```bash
# 1. Clone / copy files
cd resumeforge

# 2. Install deps
pip install -r requirements.txt

# 3. Add your API key
echo "ANTHROPIC_API_KEY=sk-ant-your-key-here" > .env

# 4. Run
streamlit run app.py
```

Open **http://localhost:8501**

---

## Default Login Credentials

| Username    | Password      | Role    |
|-------------|---------------|---------|
| `admin`     | `admin@123`   | Admin   |
| `recruiter` | `recruit@123` | User    |
| `manager`   | `manage@123`  | User    |

Admin users can add new users from the sidebar panel.

---

## Docker (Local)

```bash
# Build and run
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

---

## Deploy to AWS (ECR + EC2)

### Prerequisites
- AWS CLI configured (`aws configure`)
- Docker installed locally
- EC2 instance running with Docker + AWS CLI
- Security group allowing inbound on port **8501**

### Steps

1. **Edit `deploy.sh`** — fill in your AWS Account ID, EC2 host, and key path

2. **Set API key on EC2:**
   ```bash
   ssh -i your-key.pem ec2-user@your-ec2-ip
   echo 'export ANTHROPIC_API_KEY=sk-ant-your-key' >> ~/.bashrc
   source ~/.bashrc
   ```

3. **Run deploy:**
   ```bash
   chmod +x deploy.sh
   ./deploy.sh
   ```

4. **Access:** `http://your-ec2-ip:8501`

---

## Project Structure

```
resumeforge/
├── app.py              # Main Streamlit application
├── db.py               # SQLite database (auth + history)
├── requirements.txt    # Python dependencies
├── .env                # API key config (not committed)
├── Dockerfile          # Container image
├── docker-compose.yml  # Local Docker orchestration
├── deploy.sh           # AWS ECR/EC2 deploy script
├── .dockerignore       # Docker build exclusions
└── data/               # SQLite DB storage (auto-created)
```

---

## Tech Stack

- **Frontend:** Streamlit + Custom HTML/CSS (dark glassmorphism theme)
- **Backend:** Python, SQLite
- **Documents:** python-docx, fpdf2, PyPDF2
- **Container:** Docker, docker-compose
- **Cloud:** AWS ECR + EC2
