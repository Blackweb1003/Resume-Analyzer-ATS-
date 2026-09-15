# ATS Resume Analyzer

Complete full-stack hybrid ATS Resume Analyzer built with FastAPI, React, Tailwind CSS, PyMuPDF, scikit-learn, sentence-transformers, and the OpenAI Responses API.

## 1. What This Project Does

The app lets a user upload a PDF resume and paste a job description. The backend extracts resume text, runs the existing deterministic ATS analysis, optionally adds an LLM contextual analysis layer, calculates the final score in Python, and returns improvement suggestions. The frontend displays the final score, objective score breakdown, contextual breakdown when available, skills, strengths, weaknesses, evidence, and suggestions.

## 2. Folder Structure

```text
resume-analyzer/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── routes/
│   │   │   └── resume_routes.py
│   │   ├── services/
│   │   │   ├── analysis_service.py
│   │   │   ├── pdf_service.py
│   │   │   ├── scoring_service.py
│   │   │   ├── skill_service.py
│   │   │   └── suggestion_service.py
│   │   ├── utils/
│   │   │   ├── config.py
│   │   │   └── text_cleaner.py
│   │   ├── models/
│   │   │   └── resume_model.py
│   │   └── schemas/
│   │       └── analysis_schema.py
│   ├── requirements.txt
│   ├── render.yaml
│   └── .env
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── FileUpload.jsx
│   │   │   ├── JobDescriptionInput.jsx
│   │   │   ├── ProgressBar.jsx
│   │   │   ├── ResultCard.jsx
│   │   │   └── SkillTags.jsx
│   │   ├── pages/
│   │   │   └── AnalyzerPage.jsx
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── styles.css
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   └── .env.example
└── README.md
```

## 3. Why This Architecture Matters

`main.py` creates the FastAPI app, enables CORS, and connects routers. It should stay small because application startup and API wiring are different concerns from resume analysis.

`routes/resume_routes.py` owns HTTP behavior: file upload validation, form input validation, and returning API responses.

`services/` owns business logic. PDF extraction, skill extraction, scoring, LLM communication, and suggestions are separate so each piece can be tested and improved independently.

`schemas/` defines Pydantic response contracts. This keeps backend responses predictable for the React frontend.

`frontend/src/services/api.js` owns API calls. Components should not know Axios details.

`frontend/src/components/` contains reusable UI pieces. The page composes them into the full analyzer workflow.

## 4. Backend Setup

Use Python 3.11 or 3.12 for the smoothest local setup. The project includes `backend/runtime.txt` so Render uses Python 3.12.8 in production.

From the project root:

```bash
cd resume-analyzer/backend
python -m venv .venv
```

Activate the virtual environment on Windows PowerShell:

```bash
.\.venv\Scripts\Activate.ps1
```

Activate on macOS/Linux:

```bash
source .venv/bin/activate
```

Install backend dependencies:

```bash
pip install -r requirements.txt
```

Run the backend:

```bash
uvicorn app.main:app --reload
```

Open:

```text
http://localhost:8000
http://localhost:8000/docs
```

The first run may take longer because `sentence-transformers` downloads the `all-MiniLM-L6-v2` model.

## 5. Backend Data Flow

1. React sends `resume` and `job_description` to `POST /api/v1/analyze`.
2. `resume_routes.py` validates that the file is a PDF and the job description is not empty.
3. `pdf_service.py` uses PyMuPDF to extract text from the PDF.
4. `analysis_service.py` coordinates the analysis.
5. `skill_service.py` extracts known technical skills and finds matched/missing skills.
6. `scoring_service.py` calculates keyword similarity, semantic similarity, skill match score, and the final Python-controlled score.
7. `llm_service.py` optionally calls OpenAI once for structured contextual analysis.
8. `suggestion_service.py` creates fallback rule-based improvement suggestions.
9. FastAPI returns JSON to the frontend.

Example response:

```json
{
  "ats_score": 84,
  "base_score": 82,
  "skill_score": 75,
  "keyword_score": 68,
  "semantic_score": 91,
  "matched_skills": ["python", "fastapi", "sql"],
  "missing_skills": ["docker", "aws"],
  "detected_resume_skills": ["python", "fastapi", "react", "sql"],
  "llm_analysis_available": true,
  "experience_relevance": 80,
  "project_relevance": 70,
  "contextual_skill_alignment": 85,
  "strengths": ["Backend API experience is relevant to the job."],
  "weaknesses": ["Cloud deployment evidence is limited."],
  "suggestions": [
    "Make existing API project impact more measurable."
  ],
  "llm_error": null
}
```

## 6. Frontend Setup

Open a second terminal:

```bash
cd resume-analyzer/frontend
npm install
```

Create your local frontend environment file:

```bash
copy .env.example .env
```

On macOS/Linux:

```bash
cp .env.example .env
```

Run the frontend:

```bash
npm run dev
```

Open:

```text
http://localhost:5173
```

## 7. Frontend Data Flow

1. `AnalyzerPage.jsx` stores the selected PDF, job description, loading state, errors, and result.
2. `FileUpload.jsx` captures the resume PDF.
3. `JobDescriptionInput.jsx` captures the job description.
4. `api.js` sends both fields as `multipart/form-data` to FastAPI.
5. `ResultCard.jsx` displays the score, matched skills, missing skills, detected skills, and suggestions.

## 8. Manual Testing Steps

Start backend:

```bash
cd resume-analyzer/backend
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload
```

Start frontend:

```bash
cd resume-analyzer/frontend
npm run dev
```

Test in the browser:

1. Open `http://localhost:5173`.
2. Upload a readable PDF resume.
3. Paste a real job description.
4. Click `Analyze Resume`.
5. Confirm that score, objective breakdown, skills, and suggestions appear.
6. If `OPENAI_API_KEY` is configured, confirm the contextual breakdown appears.
7. If `OPENAI_API_KEY` is missing, confirm the app still returns the base score with contextual analysis marked unavailable.

Test API directly in Swagger:

1. Open `http://localhost:8000/docs`.
2. Expand `POST /api/v1/analyze`.
3. Upload a PDF and enter a job description.
4. Execute the request.

## 9. How ATS Scoring Works

The existing objective score is preserved:

```text
45% skill match
25% keyword similarity
30% semantic similarity
```

Skill match checks how many required skills from the job description are present in the resume.

Keyword similarity uses `CountVectorizer` and cosine similarity to compare shared terms and phrases.

Semantic similarity uses `sentence-transformers` to compare meaning, not just exact words.

When the LLM succeeds, the backend computes a contextual score from structured LLM dimensions:

```text
LLM contextual score =
  (contextual skill alignment * 50%)
  + (experience relevance * 30%)
  + (project relevance * 20%)
```

The final hybrid score is still calculated by Python, not by the LLM:

```text
final ATS score =
  (existing objective score * 70%)
  + (LLM contextual score * 30%)
```

If the LLM is unavailable, times out, returns malformed data, or `OPENAI_API_KEY` is missing, the app falls back to the existing objective score and returns:

```json
{
  "llm_analysis_available": false,
  "llm_error": "Contextual analysis temporarily unavailable"
}
```

The LLM does not produce the final score. It only returns structured context such as required skills, preferred skills, evidence, strengths, weaknesses, relevance dimensions, and suggestions.

The LLM was added to improve context that fixed dictionaries and keyword overlap miss: synonyms, related responsibilities, project relevance, skill evidence, strengths, weaknesses, and personalized wording suggestions. It does not replace PDF extraction, deterministic skill matching, keyword similarity, semantic similarity, or the backend scoring engine. All OpenAI communication lives in `backend/app/services/llm_service.py`, and the response is validated with Pydantic before it can influence scoring.

## 10. Environment Variables

Backend `.env`:

```env
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
EMBEDDING_MODEL_NAME=all-MiniLM-L6-v2
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4.1-mini
OPENAI_TIMEOUT_SECONDS=30
```

Frontend `.env`:

```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

In production, `CORS_ORIGINS` must contain your Vercel frontend URL, and `VITE_API_BASE_URL` must contain your Render backend API URL with `/api/v1`. Never expose `OPENAI_API_KEY` in frontend code or Vercel frontend environment variables.

## 11. Deploy Backend to Render

1. Push this repository to GitHub.
2. Go to Render and create a new Web Service.
3. Connect the GitHub repository.
4. Set root directory:

```text
resume-analyzer/backend
```

5. Set build command:

```bash
pip install -r requirements.txt
```

6. Set start command:

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

7. Add environment variables:

```env
CORS_ORIGINS=https://your-vercel-app.vercel.app
EMBEDDING_MODEL_NAME=all-MiniLM-L6-v2
OPENAI_API_KEY=your-backend-only-key
OPENAI_MODEL=gpt-4.1-mini
```

8. Deploy and copy the Render backend URL.

## 12. Deploy Frontend to Vercel

1. Import the GitHub repository in Vercel.
2. Set framework preset to `Vite`.
3. Set root directory:

```text
resume-analyzer/frontend
```

4. Set build command:

```bash
npm run build
```

5. Set output directory:

```text
dist
```

6. Add environment variable:

```env
VITE_API_BASE_URL=https://your-render-service.onrender.com/api/v1
```

7. Deploy.
8. Copy the Vercel URL and add it to Render `CORS_ORIGINS`.
9. Redeploy the Render service after updating CORS.

## 13. Common Bugs and Fixes

`CORS error`: Add the exact Vercel URL to backend `CORS_ORIGINS`. Include `https://` and do not add a trailing slash.

`Only PDF resume files are supported`: Upload a real PDF. Some browsers may send unusual MIME types for renamed files.

`Could not extract readable text`: The PDF may be scanned image-only. Add OCR later with Tesseract or a cloud OCR API.

`First request is slow`: The sentence-transformer model loads on first use. This is normal.

`Render memory issue`: Sentence-transformers can be heavy on small instances. Upgrade Render plan or switch to a smaller embedding approach.

`Frontend cannot connect`: Check `VITE_API_BASE_URL` and confirm it ends with `/api/v1`.

`Contextual analysis temporarily unavailable`: Confirm `OPENAI_API_KEY` is configured on the backend and that the selected `OPENAI_MODEL` supports the Responses API with structured output.

## 14. Future Improvements

Add OCR support for scanned resumes.

Expand the dynamic LLM analysis with calibrated evaluation data.

Store analysis history with PostgreSQL.

Add authentication for saved analyses.

Add downloadable PDF reports.

Add resume section checks for summary, work experience, education, skills, projects, and certifications.

## 15. Resume-Ready Project Description

Built a full-stack hybrid ATS Resume Analyzer using FastAPI, React, Tailwind CSS, PyMuPDF, scikit-learn, sentence-transformers, and the OpenAI Responses API. Implemented PDF resume parsing, deterministic ATS scoring, contextual LLM analysis with fallback behavior, skill gap detection, semantic similarity scoring, personalized suggestions, responsive UI, and deployment-ready configuration for Render and Vercel.
