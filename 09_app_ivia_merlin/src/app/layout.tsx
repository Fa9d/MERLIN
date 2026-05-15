import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "IVIA — La maison du vivant | Québec",
  description:
    "IVIA — In Vivo In Actu. Un espace pour déposer, comprendre et remettre en relation ce qui agit en nous : corps, liens, mémoire, territoire. Au Québec, sous consentement, sans diagnostic.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="fr-CA" suppressHydrationWarning>
      <head>
        {/* Theme flash prevention — must run before paint */}
        <script
          dangerouslySetInnerHTML={{
            __html: `(function(){var t=localStorage.getItem('ivia-theme');var d=window.matchMedia('(prefers-color-scheme:dark)').matches;document.documentElement.setAttribute('data-theme',t||(d?'dark':'light'));})();`,
          }}
        />
        <link rel="preconnect" href="https://api.fontshare.com" />
        <link
          href="https://api.fontshare.com/v2/css?f[]=zodiak@400,700&f[]=satoshi@400,500,700&display=swap"
          rel="stylesheet"
        />
      </head>
      <body>{children}</body>
    </html>
  );
}
