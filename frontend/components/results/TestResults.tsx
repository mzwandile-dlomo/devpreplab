"use client";

import * as React from "react";

export type SubmissionStatus = "passed" | "failed" | "error" | "timeout";

export interface SubmissionResultProps {
  status: SubmissionStatus;
  stdout: string;
  stderr: string;
  execution_time_ms?: number | null;
  memory_kb?: number | null;
}

export interface TestResultsProps {
  result: SubmissionResultProps | null;
  isSubmitting: boolean;
}

export function TestResults({ result, isSubmitting }: TestResultsProps) {
  if (isSubmitting) {
    return (
      <div className="rounded-md border border-zinc-200 bg-white px-4 py-3 text-sm text-zinc-700">
        Running code against test cases...
      </div>
    );
  }

  if (!result) {
    return (
      <div className="rounded-md border border-dashed border-zinc-200 bg-zinc-50 px-4 py-3 text-sm text-zinc-500">
        Run your code to see results.
      </div>
    );
  }

  const statusColor =
    result.status === "passed"
      ? "bg-emerald-50 text-emerald-700 border-emerald-200"
      : result.status === "failed"
      ? "bg-amber-50 text-amber-700 border-amber-200"
      : result.status === "timeout"
      ? "bg-sky-50 text-sky-700 border-sky-200"
      : "bg-rose-50 text-rose-700 border-rose-200";

  return (
    <div className="space-y-3">
      <div className={`inline-flex items-center gap-2 rounded-full border px-3 py-1 text-xs font-medium ${statusColor}`}>
        <span>Status:</span>
        <span className="capitalize">{result.status}</span>
        {typeof result.execution_time_ms === "number" && (
          <span className="text-[11px] text-zinc-600">
            · {result.execution_time_ms} ms
          </span>
        )}
        {typeof result.memory_kb === "number" && (
          <span className="text-[11px] text-zinc-600">
            · {Math.round(result.memory_kb)} KB
          </span>
        )}
      </div>

      {result.stdout && (
        <div className="rounded-md border border-zinc-200 bg-white px-3 py-2 text-xs">
          <div className="mb-1 font-semibold text-zinc-800">Output</div>
          <pre className="whitespace-pre-wrap break-words text-zinc-800">{result.stdout}</pre>
        </div>
      )}

      {result.stderr && (
        <div className="rounded-md border border-zinc-200 bg-white px-3 py-2 text-xs">
          <div className="mb-1 font-semibold text-zinc-800">Errors</div>
          <pre className="whitespace-pre-wrap break-words text-rose-800">{result.stderr}</pre>
        </div>
      )}
    </div>
  );
}
