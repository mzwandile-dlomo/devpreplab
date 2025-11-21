"use client";

import dynamic from "next/dynamic";
import * as React from "react";

const MonacoEditor = dynamic(() => import("@monaco-editor/react"), { ssr: false });

export interface CodeEditorProps {
  language: string;
  value: string;
  onChange: (value: string) => void;
  height?: string | number;
}

export function CodeEditor({ language, value, onChange, height = 400 }: CodeEditorProps) {
  const handleChange = (val: string | undefined) => {
    onChange(val ?? "");
  };

  return (
    <div className="rounded-md border border-zinc-200 overflow-hidden bg-zinc-950">
      <MonacoEditor
        language={language}
        value={value}
        onChange={handleChange}
        height={height}
        theme="vs-dark"
        options={{
          minimap: { enabled: false },
          fontSize: 13,
          scrollBeyondLastLine: false,
          automaticLayout: true,
        }}
      />
    </div>
  );
}
