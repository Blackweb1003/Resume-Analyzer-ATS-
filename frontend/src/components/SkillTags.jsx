function SkillTags({ title, skills, variant = "matched" }) {
  const colorClass =
    variant === "missing"
      ? "border-rose-200 bg-rose-50 text-rose-700"
      : "border-teal-200 bg-teal-50 text-teal-700";

  return (
    <section className="space-y-3">
      <h3 className="text-sm font-semibold text-slate-800">{title}</h3>
      {skills.length > 0 ? (
        <div className="flex flex-wrap gap-2">
          {skills.map((skill) => (
            <span
              key={skill}
              className={`rounded-full border px-3 py-1 text-xs font-semibold ${colorClass}`}
            >
              {skill}
            </span>
          ))}
        </div>
      ) : (
        <p className="rounded-lg bg-slate-50 px-4 py-3 text-sm text-slate-500">
          No skills found in this category.
        </p>
      )}
    </section>
  );
}

export default SkillTags;
