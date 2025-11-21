import Link from "next/link";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api";

interface Problem {
  id: string;
  title: string;
  difficulty: string;
  category: string;
}

async function fetchProblems(): Promise<Problem[]> {
  const res = await fetch(`${API_BASE}/problems`, { next: { revalidate: 30 } });
  if (!res.ok) {
    throw new Error("Failed to fetch problems");
  }
  return res.json();
}

export default async function ProblemsPage() {
  const problems = await fetchProblems();

  return (
    <div className="mx-auto max-w-4xl px-4 py-8">
      <div className="mb-6 flex items-center justify-between gap-3">
        <div>
          <h1 className="text-2xl font-semibold">Problems</h1>
          <span className="text-sm text-zinc-500">{problems.length} problems</span>
        </div>
        <a
          href="/problems/random"
          className="inline-flex items-center rounded-md border border-zinc-300 px-3 py-1 text-xs font-medium text-white hover:bg-zinc-50"
        >
          Random problem
        </a>
      </div>

      <div className="space-y-3">
        {problems.map((p) => (
          <Link
            key={p.id}
            href={`/problems/${p.id}`}
            className="flex items-start justify-between rounded-lg border border-zinc-200 bg-white px-4 py-3 shadow-sm hover:bg-zinc-50"
          >
            <div>
              <h2 className="text-sm font-medium text-zinc-900">{p.title}</h2>
              <p className="mt-1 text-xs text-zinc-500">{p.category}</p>
            </div>
            <span
              className={`inline-flex rounded-full px-2 py-0.5 text-xs font-semibold capitalize ${
                p.difficulty === "easy"
                  ? "bg-emerald-50 text-emerald-700"
                  : p.difficulty === "medium"
                  ? "bg-amber-50 text-amber-700"
                  : "bg-rose-50 text-rose-700"
              }`}
            >
              {p.difficulty}
            </span>
          </Link>
        ))}

        {problems.length === 0 && (
          <p className="text-sm text-zinc-500">No problems available yet.</p>
        )}
      </div>
    </div>
  );
}
