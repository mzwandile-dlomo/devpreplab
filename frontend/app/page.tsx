import Link from "next/link";

export default function Home() {
  return (
    <div className="mx-auto flex max-w-5xl flex-col gap-10 px-4 py-10">
      <section className="grid gap-8 md:grid-cols-[2fr,1.2fr] md:items-center">
        <div className="space-y-4">
          <h1 className="text-3xl text-white font-semibold tracking-tight md:text-4xl">
            Practice coding interviews with focused, timed challenges.
          </h1>
          <p className="text-sm leading-relaxed text-zinc-600">
            DevPrepLab helps you prepare for technical interviews with curated problems,
            an integrated editor, automated test runs, and progress tracking so you can
            see exactly how you are improving over time.
          </p>
          <div className="flex flex-wrap gap-3">
            <Link
              href="/problems"
              className="inline-flex items-center rounded-md bg-black px-4 py-2 text-sm font-medium text-white hover:bg-zinc-800"
            >
              Browse problems
            </Link>
            <button
              type="button"
              className="inline-flex items-center rounded-md border border-zinc-300 px-4 py-2 text-sm font-medium text-zinc-700 hover:bg-zinc-50"
              disabled
            >
              Start timed session (coming soon)
            </button>
          </div>
        </div>

        <div className="space-y-3 rounded-lg border border-zinc-200 bg-white p-4 shadow-sm">
          <h2 className="text-sm font-semibold text-zinc-900">Why DevPrepLab?</h2>
          <ul className="space-y-2 text-sm text-zinc-600">
            <li>
              • Curated problems by difficulty and topic.
            </li>
            <li>
              • Real execution against hidden test cases.
            </li>
            <li>
              • Track your success rate and history over time.
            </li>
          </ul>
        </div>
      </section>

      <section className="grid gap-4 md:grid-cols-3">
        <div className="rounded-lg border border-zinc-200 bg-white p-4">
          <h3 className="text-sm font-semibold text-zinc-900">Problem sets</h3>
          <p className="mt-1 text-xs text-zinc-600">
            Browse problems by difficulty and category to target your weak spots.
          </p>
        </div>
        <div className="rounded-lg border border-zinc-200 bg-white p-4">
          <h3 className="text-sm font-semibold text-zinc-900">Execution sandbox</h3>
          <p className="mt-1 text-xs text-zinc-600">
            Run your code safely in an isolated environment with real test cases.
          </p>
        </div>
        <div className="rounded-lg border border-zinc-200 bg-white p-4">
          <h3 className="text-sm font-semibold text-zinc-900">Progress tracking</h3>
          <p className="mt-1 text-xs text-zinc-600">
            Review your history, see trends, and measure improvement over time.
          </p>
        </div>
      </section>
    </div>
  );
}
