import { FileText, UploadCloud, X } from "lucide-react";

function FileUpload({ file, onFileChange }) {
  const handleChange = (event) => {
    const selectedFile = event.target.files?.[0];
    if (selectedFile) {
      onFileChange(selectedFile);
    }
  };

  return (
    <div className="space-y-3">
      <label className="text-sm font-semibold text-slate-800" htmlFor="resume">
        Resume PDF
      </label>
      <label
        className="flex min-h-44 cursor-pointer flex-col items-center justify-center rounded-lg border border-dashed border-slate-300 bg-white px-5 py-6 text-center transition hover:border-teal-500 hover:bg-teal-50"
        htmlFor="resume"
      >
        <UploadCloud className="mb-3 h-9 w-9 text-teal-600" aria-hidden="true" />
        <span className="text-sm font-semibold text-slate-900">
          Upload your resume
        </span>
        <span className="mt-1 text-xs text-slate-500">PDF only, readable text works best</span>
        <input
          id="resume"
          type="file"
          accept="application/pdf"
          className="hidden"
          onChange={handleChange}
        />
      </label>

      {file ? (
        <div className="flex items-center justify-between rounded-lg border border-slate-200 bg-slate-50 px-4 py-3">
          <div className="flex min-w-0 items-center gap-3">
            <FileText className="h-5 w-5 shrink-0 text-teal-700" aria-hidden="true" />
            <span className="truncate text-sm font-medium text-slate-700">{file.name}</span>
          </div>
          <button
            type="button"
            className="rounded-md p-1 text-slate-500 transition hover:bg-slate-200 hover:text-slate-900"
            onClick={() => onFileChange(null)}
            aria-label="Remove resume file"
          >
            <X className="h-4 w-4" aria-hidden="true" />
          </button>
        </div>
      ) : null}
    </div>
  );
}

export default FileUpload;
