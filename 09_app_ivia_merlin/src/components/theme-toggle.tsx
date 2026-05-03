"use client";

import { useEffect, useState } from "react";

export function ThemeToggle({ className = "" }: { className?: string }) {
  const [theme, setTheme] = useState<"light" | "dark" | null>(null);

  useEffect(() => {
    const stored = localStorage.getItem("ivia-theme") as "light" | "dark" | null;
    const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
    const initial = stored ?? (prefersDark ? "dark" : "light");
    setTheme(initial);
  }, []);

  function toggle() {
    const next = theme === "dark" ? "light" : "dark";
    setTheme(next);
    localStorage.setItem("ivia-theme", next);
    document.documentElement.setAttribute("data-theme", next);
  }

  if (theme === null) return <span style={{ width: "2.2rem", height: "2.2rem", display: "inline-block" }} />;

  return (
    <button
      onClick={toggle}
      className={`theme-toggle ${className}`}
      aria-label={theme === "dark" ? "Passer en mode clair" : "Passer en mode sombre"}
      title={theme === "dark" ? "Mode clair" : "Mode sombre"}
    >
      {theme === "dark" ? (
        <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
          <circle cx="10" cy="10" r="4.25" stroke="currentColor" strokeWidth="1.5"/>
          <line x1="10" y1="1.5" x2="10" y2="3.5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
          <line x1="10" y1="16.5" x2="10" y2="18.5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
          <line x1="1.5" y1="10" x2="3.5" y2="10" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
          <line x1="16.5" y1="10" x2="18.5" y2="10" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
          <line x1="4.1" y1="4.1" x2="5.5" y2="5.5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
          <line x1="14.5" y1="14.5" x2="15.9" y2="15.9" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
          <line x1="14.5" y1="5.5" x2="15.9" y2="4.1" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
          <line x1="4.1" y1="15.9" x2="5.5" y2="14.5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
        </svg>
      ) : (
        <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
          <path
            d="M 17 11.5 A 7.5 7.5 0 1 1 8.5 3 A 5.5 5.5 0 0 0 17 11.5 Z"
            stroke="currentColor"
            strokeWidth="1.5"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </svg>
      )}
    </button>
  );
}
