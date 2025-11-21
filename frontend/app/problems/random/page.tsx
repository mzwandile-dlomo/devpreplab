import { redirect } from "next/navigation";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api";

interface Problem {
  id: string;
}

async function fetchRandomProblem(): Promise<Problem> {
  const res = await fetch(`${API_BASE}/problems/random`, {
    cache: "no-store",
  });

  if (!res.ok) {
    throw new Error("Failed to fetch random problem");
  }

  return res.json();
}

export default async function RandomProblemPage() {
  const problem = await fetchRandomProblem();

  redirect(`/problems/${problem.id}`);
}
