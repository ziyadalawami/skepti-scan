# 🤨 Skepti-Scan

**Trust nothing. Verify everything.**

Skepti-Scan is a ruthlessly analytical RAG-based fact-checking API built with FastAPI, LangChain, and PostgreSQL. It operates on a simple premise: raw claims without sources are useless. Instead of relying on an LLM's hallucinated memory, this system cross-references user claims against live web data to determine a definitive verdict.

---

## 🚀 API Endpoint Map

```text
/api/v1
└── /verify/
    ├── POST /                 # Submit a single claim for aggressive fact-checking
└── /claims/
    ├── GET  /                 # Retrieve a paginated list of historical investigations
    └── GET  /{id}             # Fetch the detailed verdict of a specific claim
```

---

## 🛠️ Requirements

* Python 3.11 (Slim)
* Docker Desktop installed and running
* Miniconda (Recommended for local backend development)

---

## 💻 Local Development Setup

Use this method if you are actively writing code and want the FastAPI server or Streamlit frontend to hot-reload when you save files.

**1. Create a clean environment using Miniconda:**

```bash
conda create -n skeptiscan-env python=3.11 -y
```

**2. Activate the environment:**

```bash
conda activate skeptiscan-env
```

**3. Install the required packages:**

```bash
pip install -r requirements.txt
```

**4. Configure your environment variables:**<br>
Copy the provided template to create your local environment file:

```bash
cp .env.example .env
```

Open the newly created `.env` file and set your secure credentials:

```env
# REQUIRED CREDENTIALS
DB_PASSWORD=your_secure_database_password
OPENROUTER_API_KEY=your_openrouter_api_key_here
```
*(Note: Other values in the env file are optional to change.)*

**5. Spin up the Database Container:**<br>
*(Note: This starts only the isolated PostgreSQL database.)*

```bash
docker compose up -d db
```

**6. Run the API (Backend):**

```bash
uvicorn app.main:app --reload --port 8000
```

*The API interactive documentation will be available at `http://localhost:8000/docs`.*

**7. Run the Dashboard (Frontend):**<br>
Open a new terminal, ensure your conda environment is activated, and run:

```bash
streamlit run frontend/app.py
```

*The UI will be available at `http://localhost:8501`.*

---

## 🐳 Docker Deployment

Use this method if you want to deploy the entire application (Database, API, and Frontend) in completely isolated, lightweight containers without touching a local Python environment.

**1. Setup the environment variables:**<br>
Ensure your `.env` file is populated with your database credentials and OpenRouter API key.

**2. Build and start all services:**

```bash
docker compose up --build -d
```

> **Tip:** The `-d` flag runs the containers in the background so you can keep using your terminal.

* **Frontend UI:** `http://localhost:8501`
* **Backend API Docs:** `http://localhost:8000/docs`

---

## 💡 Usage Examples

You can test the API functionalities using the Swagger UI, the Streamlit frontend, or via standard cURL/Postman requests.

### 1. Submit a Claim for Verification

The system requires a strict JSON payload. It will search the web, format the context, and return a cold, hard JSON verdict.

**POST** `/api/v1/verify`

**Request:**

```json
{
  "claim_text": "The Great Wall of China is visible from space with the naked eye."
}
```

**Response:**

```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "claim_text": "The Great Wall of China is visible from space with the naked eye.",
  "status": "debunked",
  "confidence": 0.95,
  "justification": "Multiple space agencies and astronauts confirm the Great Wall is not visible from low Earth orbit without optical aid.",
  "sources": [
    "[https://www.nasa.gov/vision/space/workinginspace/great_wall.html](https://www.nasa.gov/vision/space/workinginspace/great_wall.html)"
  ],
  "created_at": "2026-07-01T10:00:00Z"
}
```

### 2. Retrieve Investigation History

Fetch a paginated list of all previously scrutinized claims.

**GET** `/api/v1/claims?skip=0&limit=10`<br>
*(No payload required. Use query parameters to control pagination.)*

### 3. Fetch a Specific Verdict

Retrieve the full details of a past investigation.

**GET** `/api/v1/claims/{id}`<br>
*(No payload required. Pass the investigation's UUID in the URL path.)*

