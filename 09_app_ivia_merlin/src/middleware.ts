import { NextRequest, NextResponse } from "next/server";

/**
 * Routes protégées — accès interdit sans authentification.
 * Tout sous-chemin de ces préfixes est également protégé.
 */
const PROTECTED_PREFIXES = [
  "/praticien",
  "/operator",
  "/supervision",
  "/admin",
  "/suivi",
];

/**
 * Routes explicitement publiques — jamais interceptées.
 * Listées pour documentation ; le matcher config exclut déjà /api/auth/*.
 */
const PUBLIC_PATHS = new Set([
  "/",
  "/login",
  "/rendez-vous",
  "/rendez-vous/reserver",
  "/rendez-vous/confirmation",
  "/ressources",
  "/praticiens",
]);

function isProtected(pathname: string): boolean {
  // La liste publique est prioritaire
  if (PUBLIC_PATHS.has(pathname)) return false;

  return PROTECTED_PREFIXES.some(
    (prefix) => pathname === prefix || pathname.startsWith(prefix + "/")
  );
}

function hasValidCredentials(request: NextRequest): boolean {
  // 1. Cookie de session
  const sessionCookie = request.cookies.get("session_token");
  if (sessionCookie?.value) return true;

  // 2. Header Authorization: Bearer <token>
  const authHeader = request.headers.get("authorization") ?? "";
  if (authHeader.startsWith("Bearer ")) {
    const token = authHeader.slice(7).trim();
    // Vérification structurelle minimale : trois segments séparés par des points (JWT)
    if (token.split(".").length === 3) return true;
  }

  return false;
}

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  if (!isProtected(pathname)) {
    return NextResponse.next();
  }

  if (hasValidCredentials(request)) {
    return NextResponse.next();
  }

  // Redirection vers /login avec la destination originale en paramètre
  const loginUrl = request.nextUrl.clone();
  loginUrl.pathname = "/login";
  loginUrl.search = `?redirect=${encodeURIComponent(pathname)}`;

  return NextResponse.redirect(loginUrl);
}

export const config = {
  matcher: [
    /*
     * Intercepte toutes les routes sauf :
     *  - _next/static  (assets statiques)
     *  - _next/image   (optimisation d'images)
     *  - favicon.ico
     *  - /api/auth/*   (endpoints d'authentification eux-mêmes)
     */
    "/((?!_next/static|_next/image|favicon\\.ico|api/auth/).*)",
  ],
};
