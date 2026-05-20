function ProgressBar({ value }) {
  const safeValue = Math.max(0, Math.min(100, Number(value) || 0));

  return (
    <div className="space-y-2">
      <div className="flex items-center justify-between text-sm">
        <span className="font-medium text-slate-600">ATS Match</span>
        <span className="font-bold text-slate-950">{safeValue}%</span>
      </div>
      <div className="h-3 overflow-hidden rounded-full bg-slate-200">
        <div
          className="h-full rounded-full bg-teal-600 transition-all duration-700"
          style={{ width: `${safeValue}%` }}
        />
      </div>
    </div>
  );
}

export default ProgressBar;
