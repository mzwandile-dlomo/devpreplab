"use client";

import { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { useAuth } from "../lib/hooks/useAuth"; // Import useAuth

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

const navLinks = [
  { href: "/", label: "Home" },
  { href: "/problems", label: "Problems" },
  { href: "/dashboard", label: "Dashboard" },
  { href: "/history", label: "History" },
];

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const pathname = usePathname();
  const { isLoggedIn, logout } = useAuth(); // Use the useAuth hook

  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased bg-zinc-50`}
      >
        <div className="min-h-screen flex flex-col">
          <header className="border-b border-zinc-200 bg-white/80 backdrop-blur sticky top-0 z-50">
            <div className="mx-auto flex max-w-5xl items-center justify-between px-4 py-4">
              <Link href="/" className="flex items-center gap-2">
                <span className="text-lg font-bold tracking-tight text-zinc-900">
                  DevPrepLab
                </span>
              </Link>
              
              {/* Desktop Navigation */}
              <nav className="hidden md:flex items-center gap-2 text-sm">
                {navLinks.map((link) => (
                  <Link
                    key={link.href}
                    href={link.href}
                    className={`px-4 py-2 rounded-md transition-colors ${
                      pathname === link.href
                        ? "bg-zinc-900 text-white"
                        : "text-zinc-600 hover:text-zinc-900"
                    }`}
                  >
                    {link.label}
                  </Link>
                ))}
              </nav>

              {/* Desktop Auth Buttons */}
              <div className="hidden md:flex items-center gap-3">
                {isLoggedIn ? (
                  <button
                    onClick={logout}
                    className="rounded-md bg-zinc-900 px-4 py-2 text-sm text-white hover:bg-zinc-800 transition-colors"
                  >
                    Sign Out
                  </button>
                ) : (
                  <>
                    <Link 
                      href="/login" 
                      className="text-sm text-zinc-600 hover:text-zinc-900 transition-colors"
                    >
                      Login
                    </Link>
                    <Link
                      href="/register"
                      className="rounded-md bg-zinc-900 px-4 py-2 text-sm text-white hover:bg-zinc-800 transition-colors"
                    >
                      Register
                    </Link>
                  </>
                )}
              </div>

              {/* Mobile Menu Button */}
              <button
                onClick={() => setIsMenuOpen(!isMenuOpen)}
                className="md:hidden text-zinc-900 p-2"
                aria-label="Toggle menu"
              >
                <svg
                  className="w-6 h-6"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d={isMenuOpen ? "M6 18L18 6M6 6l12 12" : "M4 6h16M4 12h16M4 18h16"}
                  />
                </svg>
              </button>
            </div>

            {/* Mobile Navigation */}
            {isMenuOpen && (
              <div className="md:hidden border-t border-zinc-200 bg-white">
                <nav className="flex flex-col px-4 py-3 gap-1">
                  {navLinks.map((link) => (
                    <Link
                      key={link.href}
                      href={link.href}
                      className={`px-3 py-2 rounded-md text-sm transition-colors ${
                        pathname === link.href
                          ? "bg-zinc-900 text-white"
                          : "text-zinc-600 hover:text-zinc-900"
                      }`}
                      onClick={() => setIsMenuOpen(false)}
                    >
                      {link.label}
                    </Link>
                  ))}
                  <div className="border-t border-zinc-200 pt-3 mt-2 flex flex-col gap-2">
                    {isLoggedIn ? (
                      <button
                        onClick={() => {
                          logout();
                          setIsMenuOpen(false);
                        }}
                        className="rounded-md bg-zinc-900 px-4 py-2 text-sm text-center text-white hover:bg-zinc-800"
                      >
                        Sign Out
                      </button>
                    ) : (
                      <>
                        <Link
                          href="/login"
                          className="text-sm text-center text-zinc-600 hover:text-zinc-900 py-2"
                          onClick={() => setIsMenuOpen(false)}
                        >
                          Login
                        </Link>
                        <Link
                          href="/register"
                          className="rounded-md bg-zinc-900 px-4 py-2 text-sm text-center text-white hover:bg-zinc-800"
                          onClick={() => setIsMenuOpen(false)}
                        >
                          Register
                        </Link>
                      </>
                    )}
                  </div>
                </nav>
              </div>
            )}
          </header>

          <main className="flex-1">{children}</main>

          <footer className="border-t border-zinc-200 bg-white/80">
            <div className="mx-auto max-w-5xl px-4 py-3 text-xs text-zinc-500">
              © {new Date().getFullYear()} DevPrepLab. All rights reserved.
            </div>
          </footer>
        </div>
      </body>
    </html>
  );
}
