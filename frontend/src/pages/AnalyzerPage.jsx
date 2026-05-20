import { useState } from "react";
import { Loader2, Sparkles } from "lucide-react";

import FileUpload from "../components/FileUpload.jsx";
import JobDescriptionInput from "../components/JobDescriptionInput.jsx";
import ResultCard from "../components/ResultCard.jsx";
import { analyzeResume } from "../services/api.js";

function AnalyzerPage() {
  const [resumeFile, setResumeFile] = useState(null);
  const [jobDescription, setJobDescription] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const canAnalyze = resumeFile && jobDescription.trim() && !isLoading;

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError("");
    setResult(null);

    if (!resumeFile) {
      setError("Please upload a PDF resume.");
      return;
    }

    if (!jobDescription.trim()) {
      setError("Please paste a job description.");
      return;
    }

    try {
      setIsLoading(true);
      const analysis = await analyzeResume({ resumeFile, jobDescription });
      setResult(analysis);
    } catch (apiError) {
      const message =
        apiError.response?.data?.detail ||
        "Something went wrong while analyzing the resume.";
      setError(message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-slate-50">
      <section className="border-b border-slate-200 bg-white">
        <div className="mx-auto flex max-w-6xl flex-col gap-4 px-4 py-8 sm:px-6 lg:px-8">
          <div className="inline-flex w-fit items-center gap-2 rounded-full border border-teal-200 bg-teal-50 px-3 py-1 text-xs font-semibold text-teal-700">
            <Sparkles className="h-4 w-4" aria-hidden="true" />
            AI Resume Screening
          </div>
          <div className="max-w-3xl">
            <h1 className="text-3xl font-bold text-slate-950 sm:text-5xl">
              ATS Resume Analyzer
            </h1>
            <p className="mt-4 text-base leading-7 text-slate-600">
              Compare a resume against a job description using keyword matching,
              skill detection, and semantic similarity.
            </p>
          </div>
        </div>
      </section>

      <section className="mx-auto grid max-w-6xl gap-6 px-4 py-8 sm:px-6 lg:grid-cols-[1fr_0.95fr] lg:px-8">
        <form
          className="space-y-6 rounded-lg border border-slate-200 bg-white p-6 shadow-soft"
          onSubmit={handleSubmit}
        >
          <FileUpload file={resumeFile} onFileChange={setResumeFile} />
          <JobDescriptionInput value={jobDescription} onChange={setJobDescription} />

          {error ? (
            <div className="rounded-lg border border-rose-200 bg-rose-50 px-4 py-3 text-sm font-medium text-rose-700">
              {error}
            </div>
          ) : null}

          <button
            type="submit"
            disabled={!canAnalyze}
            className="inline-flex w-full items-center justify-center gap-2 rounded-lg bg-slate-950 px-5 py-3 text-sm font-bold text-white transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:bg-slate-300"
          >
            {isLoading ? (
              <>
                <Loader2 className="h-5 w-5 animate-spin" aria-hidden="true" />
                Analyzing...
              </>
            ) : (
              <>
                <Sparkles className="h-5 w-5" aria-hidden="true" />
                Analyze Resume
              </>
            )}
          </button>
        </form>

        <ResultCard result={result} />
      </section>
    </main>
  );
}

export default AnalyzerPage;
