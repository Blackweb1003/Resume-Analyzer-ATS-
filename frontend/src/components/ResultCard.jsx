import { CheckCircle2, Lightbulb, Target } from "lucide-react";

import ProgressBar from "./ProgressBar.jsx";
import SkillTags from "./SkillTags.jsx";

function ResultCard({ result }) {
  if (!result) {
    return (
      <div className="flex min-h-96 items-center justify-center rounded-lg border border-slate-200 bg-white p-8 text-center shadow-soft">
        <div>
          <Target className="mx-auto mb-4 h-10 w-10 text-slate-400" aria-hidden="true" />
          <h2 className="text-lg font-bold text-slate-900">Analysis will appear here</h2>
          <p className="mt-2 text-sm leading-6 text-slate-500">
            Upload a PDF resume and paste a job description to generate an ATS score.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6 rounded-lg border border-slate-200 bg-white p-6 shadow-soft">
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="text-sm font-semibold uppercase tracking-wide text-teal-700">
            Analysis Result
          </p>
          <h2 className="mt-1 text-2xl font-bold text-slate-950">
            {result.ats_score >= 75 ? "Strong Match" : "Needs Optimization"}
          </h2>
        </div>
        <div className="rounded-lg bg-slate-950 px-4 py-3 text-center text-white">
          <div className="text-3xl font-bold">{result.ats_score}</div>
          <div className="text-xs text-slate-300">score</div>
        </div>
      </div>

      <ProgressBar value={result.ats_score} />

      <div className="grid gap-5 md:grid-cols-2">
        <SkillTags title="Matched Skills" skills={result.matched_skills} />
        <SkillTags title="Missing Skills" skills={result.missing_skills} variant="missing" />
      </div>

      <SkillTags title="Detected Resume Skills" skills={result.detected_resume_skills} />

      <section className="space-y-3">
        <div className="flex items-center gap-2">
          <Lightbulb className="h-5 w-5 text-amber-500" aria-hidden="true" />
          <h3 className="text-sm font-semibold text-slate-800">Improvement Suggestions</h3>
        </div>
        <ul className="space-y-3">
          {result.suggestions.map((suggestion) => (
            <li
              key={suggestion}
              className="flex gap-3 rounded-lg bg-slate-50 px-4 py-3 text-sm leading-6 text-slate-700"
            >
              <CheckCircle2 className="mt-0.5 h-4 w-4 shrink-0 text-teal-600" aria-hidden="true" />
              <span>{suggestion}</span>
            </li>
          ))}
        </ul>
      </section>
    </div>
  );
}

export default ResultCard;
