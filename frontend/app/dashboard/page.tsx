"use client";

import * as React from "react";
import { fetchWithAuth } from "@/lib/utils/fetchWithAuth";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api";

interface User {
  id: string;
  email: string;
  created_at: string;
}

interface Submission {
  id: string;
  problem_id: string;
  status: string;
  language: string;
  execution_time: number | null;
  memory_used: number | null;
  submitted_at: string;
}

export default function DashboardPage() {
  const [user, setUser] = React.useState<User | null>(null);
  const [submissions, setSubmissions] = React.useState<Submission[]>([]);
  const [loading, setLoading] = React.useState(true);
  const [error, setError] = React.useState<string | null>(null);

  React.useEffect(() => {
    async function load() {
      try {
        const res = await fetchWithAuth(`${API_BASE}/auth/me`);
        if (!res.ok) {
          const text = await res.text();
          throw new Error(text || `Failed to load user (status ${res.status})`);
        }
        const data = await res.json();
        setUser(data);

        // Load submissions for stats
        const subRes = await fetchWithAuth(`${API_BASE}/submissions/me`);
        if (subRes.ok) {
          const subData = await subRes.json();
          setSubmissions(subData);
        }
      } catch (err) {
        setError((err as Error).message ?? "Failed to load user");
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  const stats = React.useMemo(() => {
    const totalAttempts = submissions.length;
    const passed = submissions.filter(s => s.status === "passed").length;
    const failed = submissions.filter(s => s.status === "failed").length;
    const errors = submissions.filter(s => s.status === "error" || s.status === "timeout").length;
    const successRate = totalAttempts > 0 ? Math.round((passed / totalAttempts) * 100) : 0;

    const uniqueProblems = new Set(submissions.filter(s => s.status === "passed").map(s => s.problem_id));
    const problemsSolved = uniqueProblems.size;

    const avgTime = submissions
      .filter(s => s.execution_time != null)
      .reduce((acc, s) => acc + (s.execution_time || 0), 0) / submissions.filter(s => s.execution_time != null).length || 0;

    return {
      totalAttempts,
      passed,
      failed,
      errors,
      successRate,
      problemsSolved,
      avgTime: Math.round(avgTime),
    };
  }, [submissions]);

  return (
    <div className="mx-auto max-w-5xl px-4 py-8 space-y-6">
      <h1 className="text-2xl font-semibold text-white">Dashboard</h1>

      {loading && <p className="text-sm text-zinc-400">Loading your data...</p>}

      {!loading && !user && (
        <div className="rounded-lg border border-zinc-700 bg-zinc-800 px-6 py-8 text-center space-y-4">
          <p className="text-sm text-zinc-400">
            You need to be logged in to view your dashboard.
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

      {user && (
        <div className="space-y-6">
          <div className="rounded-lg border border-zinc-700 bg-zinc-800 px-6 py-4">
            <p className="text-sm text-zinc-400">
              Signed in as <span className="font-medium text-white">{user.email}</span>
            </p>
            <p className="text-xs text-zinc-500 mt-1">
              Member since {new Date(user.created_at).toLocaleDateString()}
            </p>
          </div>

          <div>
            <h2 className="text-lg font-semibold text-white mb-4">Your Statistics</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              <div className="rounded-lg border border-zinc-700 bg-zinc-800 px-5 py-4">
                <div className="text-3xl font-bold text-white">{stats.problemsSolved}</div>
                <div className="text-sm text-zinc-400 mt-1">Problems Solved</div>
              </div>

              <div className="rounded-lg border border-zinc-700 bg-zinc-800 px-5 py-4">
                <div className="text-3xl font-bold text-white">{stats.totalAttempts}</div>
                <div className="text-sm text-zinc-400 mt-1">Total Attempts</div>
              </div>

              <div className="rounded-lg border border-zinc-700 bg-zinc-800 px-5 py-4">
                <div className="text-3xl font-bold text-emerald-400">{stats.successRate}%</div>
                <div className="text-sm text-zinc-400 mt-1">Success Rate</div>
              </div>

              <div className="rounded-lg border border-zinc-700 bg-zinc-800 px-5 py-4">
                <div className="text-3xl font-bold text-white">{stats.avgTime}</div>
                <div className="text-sm text-zinc-400 mt-1">Avg Time (ms)</div>
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="rounded-lg border border-zinc-700 bg-zinc-800 px-5 py-4">
              <div className="text-2xl font-bold text-emerald-400">{stats.passed}</div>
              <div className="text-sm text-zinc-400 mt-1">Passed</div>
            </div>

            <div className="rounded-lg border border-zinc-700 bg-zinc-800 px-5 py-4">
              <div className="text-2xl font-bold text-amber-400">{stats.failed}</div>
              <div className="text-sm text-zinc-400 mt-1">Failed</div>
            </div>

            <div className="rounded-lg border border-zinc-700 bg-zinc-800 px-5 py-4">
              <div className="text-2xl font-bold text-rose-400">{stats.errors}</div>
              <div className="text-sm text-zinc-400 mt-1">Errors</div>
            </div>
          </div>

          {submissions.length === 0 && (
            <div className="rounded-lg border border-dashed border-zinc-700 bg-zinc-800/50 px-6 py-8 text-center">
              <p className="text-sm text-zinc-400">No submissions yet. Start practicing!</p>
              <a href="/problems" className="mt-3 inline-block text-sm text-blue-400 hover:text-blue-300 underline">
                Browse Problems
              </a>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
