"use client";

export async function fetchWithAuth(
  url: RequestInfo,
  options?: RequestInit
): Promise<Response> {
  const token = localStorage.getItem("devpreplab_token");

  const headers: Record<string, string> = {
    ...(options?.headers as Record<string, string>),
  };

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  return fetch(url, {
    ...options,
    headers,
  });
}
