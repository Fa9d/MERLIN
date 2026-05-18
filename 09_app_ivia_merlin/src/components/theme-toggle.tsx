"use client";

import { useCallback, useSyncExternalStore } from "react";

type Theme = "light" | "dark";

function getSnapshot(): Theme | null {
  if (typeof document === "undefined") return null;
  const attr = document.documentElement.getAttribute("data-theme");
  if (attr === "dark" || attr === "light") return attr;
  const stored = localStorage.getItem("ivia-theme");
  if (stored === "dark" || stored === "light") return stored;
  return window.matchMedia("(prefers-color-scheme: dark)").matches
    ? "dark"
    : "light";
}

function getServerSnapshot(): Theme | null {
  return null;
}

function subscribe(callback: () => void) {
  if (typeof window === "undefined") return () => {};
  const observer = new MutationObserver(callback);
  observer.observe(document.documentElement, {
    attributes: true,
    attributeFilter: ["data-theme"],
  });
  const onStorage = (event: StorageEvent) => {
    if (event.key === "ivia-theme") callback();
  };
  window.addEventListener("storage", onStorage);
  return () => {
    observer.disconnect();
    window.removeEventListener("storage", onStorage);
  };
}

export function ThemeToggle({ className = "" }: { className?: string }) {
  const theme = useSyncExternalStore(subscribe, getSnapshot, getServerSnapshot);

  const toggle = useCallback(() => {
    const current = document.documentElement.getAttribute("data-theme");
    const next: Theme = current === "dark" ? "light" : "dark";
    localStorage.setItem("ivia-theme", next);
    document.documentElement.setAttribute("data-theme", next);
  }, []);

  // Placeholder identique côté SSR pour éviter un saut de layout.
  if (theme === null) {
    return (
      <span
        className={`theme-toggle theme-toggle--placeholder ${className}`}
        aria-hidden="true"
      />
    );
  }

  // En sombre, l'action est de passer en CLAIR ; et vice versa.
  const actionLabel = theme === "dark" ? "CLAIR" : "SOMBRE";
  const ariaLabel =
    theme === "dark" ? "Passer en mode clair" : "Passer en mode sombre";

  return (
    <button
      onClick={toggle}
      className={`theme-toggle ${className}`}
      aria-label={ariaLabel}
      title={ariaLabel}
      type="button"
    >
      <svg
        viewBox="0 0 20 20"
        width="16"
        height="16"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        aria-hidden="true"
      >
        {theme === "dark" ? (
          <>
            <circle cx="10" cy="10" r="4.25" stroke="currentColor" strokeWidth="1.5" />
            <line x1="10" y1="1.5" x2="10" y2="3.5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
            <line x1="10" y1="16.5" x2="10" y2="18.5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
            <line x1="1.5" y1="10" x2="3.5" y2="10" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
            <line x1="16.5" y1="10" x2="18.5" y2="10" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
            <line x1="4.1" y1="4.1" x2="5.5" y2="5.5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
            <line x1="14.5" y1="14.5" x2="15.9" y2="15.9" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
            <line x1="14.5" y1="5.5" x2="15.9" y2="4.1" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
            <line x1="4.1" y1="15.9" x2="5.5" y2="14.5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
          </>
        ) : (
          <path
            d="M 17 11.5 A 7.5 7.5 0 1 1 8.5 3 A 5.5 5.5 0 0 0 17 11.5 Z"
            stroke="currentColor"
            strokeWidth="1.5"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        )}
      </svg>
      <span className="theme-toggle__label">{actionLabel}</span>
    </button>
  );
}
