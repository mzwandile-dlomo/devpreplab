"use client";

import Link from "next/link";
import * as React from "react";
import { useRouter } from "next/navigation";
import { CodeEditor } from "@/components/editor/CodeEditor";
import { CountdownTimer } from "@/components/timer/CountdownTimer";
import { TestResults, SubmissionResultProps } from "@/components/results/TestResults";
import { fetchWithAuth } from "@/lib/utils/fetchWithAuth";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api";

interface Problem {
  id: string;
  title: string;
  description: string;
  difficulty: string;
  category: string;
  time_limit: number;
  memory_limit: number;
  starter_code?: string;
}

async function fetchProblem(id: string): Promise<Problem> {
  const res = await fetch(`${API_BASE}/problems/${id}`);
  if (!res.ok) {
    throw new Error("Failed to fetch problem");
  }
  return res.json();
}

const PYTHON_STARTER = `def solution(x):\n    """Example solution function. Adjust parameters to match the problem."""\n    # TODO: implement your solution here\n    return x\n`;

export default function PracticePage({ params }: { params: Promise<{ id: string }> }) {
  const router = useRouter();
  // Unwrap the params Promise
  const { id } = React.use(params);
  
  const [problem, setProblem] = React.useState<Problem | null>(null);
  const [loading, setLoading] = React.useState(true);
  const [error, setError] = React.useState<string | null>(null);

  const [code, setCode] = React.useState(PYTHON_STARTER);
  const [isSubmitting, setIsSubmitting] = React.useState(false);
  const [result, setResult] = React.useState<SubmissionResultProps | null>(null);

  React.useEffect(() => {
    let cancelled = false;

    async function load() {
      try {
        setLoading(true);
        const data = await fetchProblem(id);
        if (!cancelled) {
          setProblem(data);
          // Use problem's starter code if available, otherwise use default
          if (data.starter_code) {
            setCode(data.starter_code);
          }
        }
      } catch (err) {
        if (!cancelled) {
          setError((err as Error).message ?? "Failed to load problem");
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    load();

    return () => {
      cancelled = true;
    };
  }, [id]);

  const handleSubmit = async () => {
    if (!problem) return;

    setIsSubmitting(true);
    setResult(null);

    try {
      // Check if user is logged in
      const token = localStorage.getItem("devpreplab_token");
      let userId: string | null = null;

      if (token) {
        // Validate token and get user ID
        try {
          const userRes = await fetchWithAuth(`${API_BASE}/auth/me`);
          if (userRes.ok) {
            const userData = await userRes.json();
            userId = userData.id;
          }
        } catch (err) {
          // Token invalid, continue as anonymous
        }
      }

      // Choose endpoint based on authentication status
      const endpoint = userId ? `${API_BASE}/submissions/` : `${API_BASE}/submissions/preview`;
      const payload = userId
        ? { user_id: userId, problem_id: problem.id, code, language: "python" }
        : { problem_id: problem.id, code, language: "python" };

      const res = await fetchWithAuth(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!res.ok) {
        const text = await res.text();
        setResult({
          status: "error",
          stdout: "",
          stderr: text || `Submission failed with status ${res.status}`,
          execution_time_ms: null,
          memory_kb: null,
        });
        return;
      }

      const data = await res.json();

      // Handle different response formats
      if (userId) {
        // Saved submission response (SubmissionInDB)
        setResult({
          status: data.status,
          stdout: data.status === "passed" ? "All test cases passed!" : "Some test cases failed",
          stderr: "",
          execution_time_ms: data.execution_time ?? null,
          memory_kb: data.memory_used ?? null,
        });
      } else {
        // Preview response (SubmissionResult)
        setResult({
          status: data.status,
          stdout: data.stdout ?? "",
          stderr: data.stderr ?? "",
          execution_time_ms: data.execution_time_ms ?? null,
          memory_kb: data.memory_kb ?? null,
        });
      }
    } catch (err) {
      setResult({
        status: "error",
        stdout: "",
        stderr: (err as Error).message ?? "Unexpected error during submission",
        execution_time_ms: null,
        memory_kb: null,
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="mx-auto max-w-5xl px-4 py-8 text-sm text-zinc-400">
        Loading problem...
      </div>
    );
  }

  if (error || !problem) {
    return (
      <div className="mx-auto max-w-5xl px-4 py-8 space-y-3 text-sm text-zinc-400">
        <p className="font-medium text-zinc-100">Unable to load problem.</p>
        <p>{error}</p>
        <button
          type="button"
          className="rounded-md border border-zinc-700 bg-zinc-800 px-3 py-1 text-xs text-zinc-100 hover:bg-zinc-700"
          onClick={() => router.push("/problems")}
        >
          Back to problems
        </button>
      </div>
    );
  }

  return (
    <div className="mx-auto flex max-w-5xl flex-col gap-6 px-4 py-8">
      <Link
        href="/problems"
        className="inline-flex w-fit items-center gap-1 rounded-md bg-zinc-800 px-3 py-1.5 text-sm font-medium text-zinc-100 hover:bg-zinc-700 transition-colors"
      >
        <span>←</span>
        <span>Back</span>
      </Link>

      <header className="flex flex-col justify-between gap-3 border-b border-zinc-800 pb-4 md:flex-row md:items-center">
        <div>
          <h1 className="text-xl font-semibold text-zinc-100">{problem.title}</h1>
          <p className="mt-1 text-xs text-zinc-400">
            {problem.category} · {problem.difficulty}
          </p>
        </div>
        <div className="flex flex-col items-start gap-2 text-xs text-zinc-400 md:items-end">
          <div>
            Time limit: {problem.time_limit}s · Memory limit: {problem.memory_limit}MB
          </div>
          <CountdownTimer initialSeconds={problem.time_limit * 2} />
        </div>
      </header>

      <main className="grid gap-6 md:grid-cols-[minmax(0,2fr)_minmax(0,1fr)]">
        <section className="space-y-3">
          <div className="rounded-md border border-zinc-800 bg-zinc-900 px-4 py-3 text-sm text-zinc-300">
            <div className="mb-1 font-semibold text-zinc-100">Description</div>
            <p className="text-xs text-zinc-300">{problem.description}</p>
          </div>

          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-xs font-medium text-zinc-100">Code editor</span>
              <span className="text-[11px] text-zinc-400">Language: Python</span>
            </div>
            <CodeEditor language="python" value={code} onChange={setCode} height={420} />
          </div>

          <div className="flex justify-end pt-2">
            <button
              type="button"
              onClick={handleSubmit}
              disabled={isSubmitting}
              className="inline-flex items-center rounded-md bg-zinc-800 px-4 py-2 text-sm font-medium text-zinc-100 hover:bg-zinc-700 disabled:opacity-60 transition-colors"
            >
              {isSubmitting ? "Running..." : "Run code"}
            </button>
          </div>
        </section>

        <aside className="space-y-3">
          <div className="rounded-md border border-zinc-800 bg-zinc-900 px-4 py-3">
            <div className="mb-2 text-xs font-semibold text-zinc-100">Results</div>
            <TestResults result={result} isSubmitting={isSubmitting} />
          </div>
        </aside>
      </main>
    </div>
  );
}