from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status

from app.schemas.analysis_schema import AnalysisResponse
from app.services.analysis_service import analyze_resume
from app.services.pdf_service import extract_text_from_pdf


router = APIRouter()


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_resume_endpoint(
    resume: UploadFile = File(...),
    job_description: str = Form(...),
) -> AnalysisResponse:
    if resume.content_type != "application/pdf":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF resume files are supported.",
        )

    if not job_description.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Job description cannot be empty.",
        )

    resume_bytes = await resume.read()

    if not resume_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded resume file is empty.",
        )

    try:
        resume_text = extract_text_from_pdf(resume_bytes)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    if not resume_text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not extract readable text from this PDF.",
        )

    return analyze_resume(resume_text=resume_text, job_description=job_description)
