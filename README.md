# 🚀 AI Resume Analyzer

An AI-powered web application that analyzes resumes and provides intelligent feedback using modern AI APIs. Built with Flask, containerized using Docker, and deployed on AWS EC2.

---

## 📌 Overview

This project allows users to upload their resume (PDF) and receive automated feedback such as skill evaluation, improvement suggestions, and role-based insights. It demonstrates full-stack development along with real-world DevOps deployment.

---

## 🧱 Architecture

```id="arch1"
Client (Browser)
        ↓
Frontend (HTML/CSS/JS)
        ↓
Flask Backend (API)
        ↓
AI Model (Google Generative AI / DeepSeek)
        ↓
Response → User
```

---

## ⚙️ Tech Stack

| Layer     | Technology                      |
| --------- | ------------------------------- |
| Frontend  | HTML, CSS, JavaScript           |
| Backend   | Flask (Python)                  |
| AI Engine | Google Generative AI / DeepSeek |
| Container | Docker                          |
| Cloud     | AWS EC2                         |

---

## 📁 Project Structure

```id="arch2"
resume_checker/
│
├── app.py                # Main Flask application
├── analyzer.py           # Resume processing logic
├── requirements.txt      # Dependencies
├── Dockerfile            # Docker configuration
├── .env                  # Environment variables
│
├── templates/
│   └── index.html        # Frontend UI
│
└── static/               # Static assets
```

---

## 🚀 Getting Started

### 1. Clone Repository

```bash id="cmd1"
git clone https://github.com/your-username/resume_checker.git
cd resume_checker
```

---

### 2. Install Dependencies

```bash id="cmd2"
pip install -r requirements.txt
```

---

### 3. Configure Environment Variables

Create a `.env` file:

```env id="env1"
GOOGLE_API_KEY=your_api_key
```

---

### 4. Run Application

```bash id="cmd3"
python app.py
```

Access:

```id="url1"
http://localhost:5000
```

---

## 🐳 Docker Setup

### Build Image

```bash id="cmd4"
docker build -t resume .
```

---

### Run Container

```bash id="cmd5"
docker run -d -p 5000:5000 --env-file .env resume
```

---

## ☁️ AWS Deployment (EC2)

### 1. Launch Instance

* OS: Ubuntu
* Open Ports:

  * `22` (SSH)
  * `5000` (Application)

---

### 2. Install Docker

```bash id="cmd6"
sudo apt update
sudo apt install docker.io -y
sudo systemctl start docker
sudo usermod -aG docker ubuntu
newgrp docker
```

---

### 3. Deploy Application

```bash id="cmd7"
git clone https://github.com/your-username/resume_checker.git
cd resume_checker

docker build -t resume .
docker run -d -p 5000:5000 --env-file .env resume
```

---

### 4. Access Application

```id="url2"
http://<EC2-PUBLIC-IP>:5000
```

---

## ⚠️ Configuration Notes

### Backend Configuration

Ensure Flask runs with:

```python id="code1"
app.run(host="0.0.0.0", port=5000)
```

---

### Frontend API Call (Important)

Use relative path:

```javascript id="code2"
fetch("/analyze")
```

Avoid:

```javascript id="code3"
http://localhost:5000
```
