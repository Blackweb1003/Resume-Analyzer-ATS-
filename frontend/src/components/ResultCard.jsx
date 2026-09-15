import {
  AlertCircle,
  Brain,
  CheckCircle2,
  Info,
  Lightbulb,
  Target,
} from "lucide-react";

import ProgressBar from "./ProgressBar.jsx";
import SkillTags from "./SkillTags.jsx";

function MetricBar({ label, value }) {
  if (value === null || value === undefined) {
    return null;
  }

  const safeValue = Math.max(0, Math.min(100, Number(value) || 0));

  return (
    <div className="space-y-2">
      <div className="flex items-center justify-between gap-3 text-sm">
        <span className="font-medium text-slate-600">{label}</span>
        <span className="shrink-0 font-bold text-slate-950">{safeValue}%</span>
      </div>
      <div className="h-2 overflow-hidden rounded-full bg-slate-200">
        <div
          className="h-full rounded-full bg-teal-600"
          style={{ width: `${safeValue}%` }}
        />
      </div>
    </div>
  );
}

function TextList({ title, items, icon: Icon, variant = "neutral" }) {
  if (!items?.length) {
    return null;
  }

  const iconClass = variant === "warning" ? "text-rose-500" : "text-teal-600";

  return (
    <section className="space-y-3">
      <div className="flex items-center gap-2">
        <Icon className={`h-5 w-5 ${iconClass}`} aria-hidden="true" />
        <h3 className="text-sm font-semibold text-slate-800">{title}</h3>
      </div>
      <ul className="space-y-2">
        {items.map((item) => (
          <li
            key={item}
            className="rounded-lg bg-slate-50 px-4 py-3 text-sm leading-6 text-slate-700"
          >
            {item}
          </li>
        ))}
      </ul>
    </section>
  );
}

function SkillEvidenceList({ evidence }) {
  if (!evidence?.length) {
    return null;
  }

  return (
    <section className="space-y-3">
      <div className="flex items-center gap-2">
        <Info className="h-5 w-5 text-slate-500" aria-hidden="true" />
        <h3 className="text-sm font-semibold text-slate-800">Skill Evidence</h3>
      </div>
      <div className="space-y-3">
        {evidence.map((item) => (
          <div
            key={`${item.skill}-${item.evidence_strength}`}
            className="rounded-lg border border-slate-200 bg-white px-4 py-3"
          >
            <div className="flex flex-wrap items-center gap-2">
              <span className="text-sm font-bold text-slate-900">{item.skill}</span>
              <span className="rounded-full bg-slate-100 px-2 py-1 text-[11px] font-semibold uppercase text-slate-600">
                {item.evidence_strength}
              </span>
            </div>
            <p className="mt-2 text-sm leading-6 text-slate-600">{item.evidence}</p>
          </div>
        ))}
      </div>
    </section>
  );
}

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
          <p className="mt-2 text-sm text-slate-500">
            Base score: {result.base_score ?? result.ats_score}
          </p>
        </div>
        <div className="rounded-lg bg-slate-950 px-4 py-3 text-center text-white">
          <div className="text-3xl font-bold">{result.ats_score}</div>
          <div className="text-xs text-slate-300">score</div>
        </div>
      </div>

      <ProgressBar value={result.ats_score} />

      {!result.llm_analysis_available ? (
        <div className="flex gap-3 rounded-lg border border-amber-200 bg-amber-50 px-4 py-3 text-sm leading-6 text-amber-800">
          <AlertCircle className="mt-0.5 h-4 w-4 shrink-0" aria-hidden="true" />
          <span>
            {result.llm_error || "Contextual analysis temporarily unavailable."}
          </span>
        </div>
      ) : null}

      <section className="space-y-4">
        <h3 className="text-sm font-semibold text-slate-800">Objective Breakdown</h3>
        <div className="grid gap-4 md:grid-cols-3">
          <MetricBar label="Skill Match" value={result.skill_score} />
          <MetricBar label="Keyword Match" value={result.keyword_score} />
          <MetricBar label="Semantic Match" value={result.semantic_score} />
        </div>
      </section>

      {result.llm_analysis_available ? (
        <section className="space-y-4">
          <div className="flex items-center gap-2">
            <Brain className="h-5 w-5 text-teal-600" aria-hidden="true" />
            <h3 className="text-sm font-semibold text-slate-800">
              Contextual Breakdown
            </h3>
          </div>
          <div className="grid gap-4 md:grid-cols-3">
            <MetricBar label="Experience" value={result.experience_relevance} />
            <MetricBar label="Projects" value={result.project_relevance} />
            <MetricBar
              label="Skill Alignment"
              value={result.contextual_skill_alignment}
            />
          </div>
        </section>
      ) : null}

      <div className="grid gap-5 md:grid-cols-2">
        <SkillTags title="Matched Skills" skills={result.matched_skills} />
        <SkillTags title="Missing Skills" skills={result.missing_skills} variant="missing" />
      </div>

      <SkillTags title="Detected Resume Skills" skills={result.detected_resume_skills} />

      {result.llm_analysis_available ? (
        <>
          <div className="grid gap-5 md:grid-cols-2">
            <SkillTags title="Required Skills" skills={result.required_skills || []} />
            <SkillTags title="Preferred Skills" skills={result.preferred_skills || []} />
          </div>

          <div className="grid gap-5 md:grid-cols-2">
            <SkillTags
              title="Contextual Matches"
              skills={result.contextual_matched_skills || []}
            />
            <SkillTags
              title="Contextual Gaps"
              skills={result.contextual_missing_skills || []}
              variant="missing"
            />
          </div>
        </>
      ) : null}

      <TextList
        title="Strengths"
        items={result.strengths}
        icon={CheckCircle2}
      />

      <TextList
        title="Weaknesses"
        items={result.weaknesses}
        icon={AlertCircle}
        variant="warning"
      />

      <SkillEvidenceList evidence={result.skill_evidence} />

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

      {result.llm_explanation ? (
        <section className="space-y-3">
          <h3 className="text-sm font-semibold text-slate-800">Score Explanation</h3>
          <p className="rounded-lg bg-slate-50 px-4 py-3 text-sm leading-6 text-slate-700">
            {result.llm_explanation}
          </p>
        </section>
      ) : null}
    </div>
  );
}

export default ResultCard;
