"use client";

import * as React from "react";
import { fetchWithAuth } from "@/lib/utils/fetchWithAuth";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api";

interface Submission {
  id: string;
  problem_id: string;
  status: string;
  language: string;
  execution_time: number | null;
  memory_used: number | null;
  submitted_at: string;
}

interface Problem {
  id: string;
  title: string;
  difficulty: string;
}

export default function HistoryPage() {
  const [submissions, setSubmissions] = React.useState<Submission[]>([]);
  const [problems, setProblems] = React.useState<Map<string, Problem>>(new Map());
  const [loading, setLoading] = React.useState(true);
  const [error, setError] = React.useState<string | null>(null);

  React.useEffect(() => {
    async function load() {
      try {
        const res = await fetchWithAuth(`${API_BASE}/submissions/me`);
        if (!res.ok) {
          const text = await res.text();
          throw new Error(text || `Failed to load submissions (status ${res.status})`);
        }
        const data = await res.json();
        setSubmissions(data);

        // Fetch problem details for all unique problem IDs
        const uniqueProblemIds = Array.from(new Set<string>(data.map((s: Submission) => s.problem_id)));
        const problemMap = new Map<string, Problem>();

        await Promise.all(
          uniqueProblemIds.map(async (problemId) => {
            try {
              const pRes = await fetch(`${API_BASE}/problems/${problemId}`);
              if (pRes.ok) {
                const problem = await pRes.json();
                problemMap.set(problemId, problem);
              }
            } catch (err) {
              // Silently fail for individual problem fetches
            }
          })
        );

        setProblems(problemMap);
      } catch (err) {
        setError((err as Error).message ?? "Failed to load submissions");
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  const getStatusColor = (status: string) => {
    switch (status) {
      case "passed":
        return "text-emerald-400 bg-emerald-400/10 border-emerald-400/20";
      case "failed":
        return "text-amber-400 bg-amber-400/10 border-amber-400/20";
      case "error":
        return "text-rose-400 bg-rose-400/10 border-rose-400/20";
      case "timeout":
        return "text-sky-400 bg-sky-400/10 border-sky-400/20";
      default:
        return "text-zinc-400 bg-zinc-400/10 border-zinc-400/20";
    }
  };

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case "easy":
        return "text-emerald-400";
      case "medium":
        return "text-amber-400";
      case "hard":
        return "text-rose-400";
      default:
        return "text-zinc-400";
    }
  };
  

  return (
    <div className="mx-auto max-w-5xl px-4 py-8 space-y-6">
      <h1 className="text-2xl font-semibold text-white">Submission History</h1>

      {loading && <p className="text-sm text-zinc-400">Loading your submissions...</p>}

      {!loading && error && submissions.length === 0 && (
        <div className="rounded-lg border border-zinc-700 bg-zinc-800 px-6 py-8 text-center space-y-4">
          <p className="text-sm text-zinc-400">
            You need to be logged in to view your submission history.
          </p>
          {error && (
            <p className="text-xs font-medium text-rose-400 bg-rose-950/30 border border-rose-800 px-3 py-2 rounded-md">
              {error}
            </p>
          )}
          <div className="flex items-center justify-center gap-3">
            <a
              href="/login"
              className="inline-flex items-center justify-center rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 transition-colors"
            >
              Go to Login
            </a>
            <a
              href="/register"
              className="inline-flex items-center justify-center rounded-md border border-zinc-600 px-4 py-2 text-sm font-medium text-zinc-300 hover:bg-zinc-700 transition-colors"
            >
              Create Account
            </a>
          </div>
        </div>
      )}

      {!loading && !error && submissions.length === 0 && (
        <div className="rounded-lg border border-dashed border-zinc-700 bg-zinc-800/50 px-6 py-8 text-center">
          <p className="text-sm text-zinc-400">You have no submissions yet.</p>
          <a href="/problems" className="mt-3 inline-block text-sm text-blue-400 hover:text-blue-300 underline">
            Start Practicing
          </a>
        </div>
      )}

      {submissions.length > 0 && (
        <div className="space-y-3">
          {submissions.map((s) => {
            const problem = problems.get(s.problem_id);
            return (
              <div
                key={s.id}
                className="rounded-lg border border-zinc-700 bg-zinc-800 px-5 py-4 hover:border-zinc-600 transition-colors"
              >
                <div className="flex items-start justify-between gap-4">
                  <div className="flex-1 space-y-2">
                    <div className="flex items-center gap-3">
                      <span className={`inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-medium capitalize ${getStatusColor(s.status)}`}>
                        {s.status}
                      </span>
                      {problem && (
                        <span className={`text-xs font-medium capitalize ${getDifficultyColor(problem.difficulty)}`}>
                          {problem.difficulty}
                        </span>
                      )}
                      <span className="text-xs text-zinc-500 uppercase">
                        {s.language}
                      </span>
                    </div>

                    <div>
                      {problem ? (
                        <a
                          href={`/problems/${s.problem_id}`}
                          className="text-base font-medium text-white hover:text-blue-400 transition-colors"
                        >
                          {problem.title}
                        </a>
                      ) : (
                        <div className="text-base font-medium text-white">
                          Problem ID: {s.problem_id.slice(0, 8)}...
                        </div>
                      )}
                    </div>

                    <div className="flex items-center gap-4 text-xs text-zinc-500">
                      <span className="font-mono">{s.id.slice(0, 8)}</span>
                      <span>·</span>
                      <span>{new Date(s.submitted_at).toLocaleString()}</span>
                    </div>
                  </div>

                  <div className="flex flex-col items-end gap-1 text-right text-xs text-zinc-400">
                    {s.execution_time != null && (
                      <div className="flex items-center gap-1.5">
                        <span className="text-zinc-500">Time:</span>
                        <span className="font-mono font-medium text-white">{s.execution_time} ms</span>
                      </div>
                    )}
                    {s.memory_used != null && (
                      <div className="flex items-center gap-1.5">
                        <span className="text-zinc-500">Memory:</span>
                        <span className="font-mono font-medium text-white">{Math.round(s.memory_used)} KB</span>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
