import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "IVIA — La maison du vivant | Québec",
  description:
    "IVIA — In Vivo In Actu. Un espace pour déposer, comprendre et remettre en relation ce qui agit en nous : corps, liens, mémoire, territoire. Au Québec, sous consentement, sans diagnostic.",
};

// Doit s'exécuter avant la peinture pour éviter le flash clair/sombre.
const themeFlashScript = `(function(){try{var t=localStorage.getItem('ivia-theme');var d=window.matchMedia('(prefers-color-scheme:dark)').matches;document.documentElement.setAttribute('data-theme',t||(d?'dark':'light'));}catch(e){document.documentElement.setAttribute('data-theme','light');}})();`;

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="fr-CA" suppressHydrationWarning>
      <head>
        <script
          id="ivia-theme-flash"
          dangerouslySetInnerHTML={{ __html: themeFlashScript }}
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
