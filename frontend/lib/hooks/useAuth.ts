"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api";

export function useAuth() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [isValidating, setIsValidating] = useState(true);
  const router = useRouter();

  useEffect(() => {
    async function validateToken() {
      const token = localStorage.getItem("devpreplab_token");

      if (!token) {
        setIsLoggedIn(false);
        setIsValidating(false);
        return;
      }

      // Validate token by calling /auth/me
      try {
        const res = await fetch(`${API_BASE}/auth/me`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (res.ok) {
          setIsLoggedIn(true);
        } else {
          // Token is invalid, clear it
          localStorage.removeItem("devpreplab_token");
          setIsLoggedIn(false);
        }
      } catch (err) {
        // Network error or other issue, assume logged out
        localStorage.removeItem("devpreplab_token");
        setIsLoggedIn(false);
      } finally {
        setIsValidating(false);
      }
    }

    validateToken();
  }, []);

  const login = (token: string) => {
    localStorage.setItem("devpreplab_token", token);
    setIsLoggedIn(true);
  };

  const logout = () => {
    localStorage.removeItem("devpreplab_token");
    setIsLoggedIn(false);
    router.push("/login");
  };

  return { isLoggedIn, isValidating, login, logout };
}
