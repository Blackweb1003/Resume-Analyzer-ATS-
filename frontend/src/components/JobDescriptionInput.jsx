function JobDescriptionInput({ value, onChange }) {
  return (
    <div className="space-y-3">
      <label className="text-sm font-semibold text-slate-800" htmlFor="jobDescription">
        Job Description
      </label>
      <textarea
        id="jobDescription"
        value={value}
        onChange={(event) => onChange(event.target.value)}
        className="min-h-72 w-full resize-y rounded-lg border border-slate-300 bg-white px-4 py-3 text-sm leading-6 text-slate-800 outline-none transition placeholder:text-slate-400 focus:border-teal-500 focus:ring-4 focus:ring-teal-100"
        placeholder="Paste the full job description here..."
      />
    </div>
  );
}

export default JobDescriptionInput;
