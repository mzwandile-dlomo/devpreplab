"use client";

import * as React from "react";

export interface CountdownTimerProps {
  initialSeconds: number;
  onComplete?: () => void;
}

export function CountdownTimer({ initialSeconds, onComplete }: CountdownTimerProps) {
  const [secondsLeft, setSecondsLeft] = React.useState(initialSeconds);
  const [isRunning, setIsRunning] = React.useState(false);

  React.useEffect(() => {
    if (!isRunning || secondsLeft <= 0) return;

    const id = window.setInterval(() => {
      setSecondsLeft((prev) => {
        if (prev <= 1) {
          window.clearInterval(id);
          setIsRunning(false);
          onComplete?.();
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => window.clearInterval(id);
  }, [isRunning, secondsLeft, onComplete]);

  const minutes = Math.floor(secondsLeft / 60)
    .toString()
    .padStart(2, "0");
  const seconds = (secondsLeft % 60).toString().padStart(2, "0");

  const reset = () => {
    setSecondsLeft(initialSeconds);
    setIsRunning(false);
  };

  return (
    <div className="inline-flex items-center gap-3 rounded-md border border-zinc-200 bg-white px-3 py-2 text-xs text-zinc-800">
      <span className="font-mono text-sm tabular-nums">
        {minutes}:{seconds}
      </span>
      <div className="flex gap-2">
        <button
          type="button"
          className="rounded border border-zinc-300 px-2 py-1 text-[11px] hover:bg-zinc-50"
          onClick={() => setIsRunning((v) => !v)}
        >
          {isRunning ? "Pause" : "Start"}
        </button>
        <button
          type="button"
          className="rounded border border-zinc-300 px-2 py-1 text-[11px] hover:bg-zinc-50"
          onClick={reset}
        >
          Reset
        </button>
      </div>
    </div>
  );
}
