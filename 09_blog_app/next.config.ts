import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Sert le blog sous le sous-chemin https://ivia.quebec/ressources/blog
  basePath: "/ressources/blog",
  // Export 100% statique (HTML/CSS/JS) -> déposé dans le site statique existant
  output: "export",
  // Requis pour l'export statique (pas d'optimiseur d'images côté serveur)
  images: { unoptimized: true },
  // URLs en /dossier/index.html -> compatibles avec un service Nginx statique
  trailingSlash: true,
};

export default nextConfig;
