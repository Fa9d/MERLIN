import { NextRequest, NextResponse } from "next/server";
import { jwtVerify } from "jose";

/**
 * Routes protégées — accès interdit sans authentification.
 * Tout sous-chemin de ces préfixes est également protégé.
 */
const PROTECTED_PREFIXES = [
  "/espace-praticien",
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
  if (PUBLIC_PATHS.has(pathname)) return false;
  return PROTECTED_PREFIXES.some(
    (prefix) => pathname === prefix || pathname.startsWith(prefix + "/")
  );
}

function redirectToLogin(request: NextRequest, pathname: string): NextResponse {
  const loginUrl = request.nextUrl.clone();
  loginUrl.pathname = "/login";
  loginUrl.search = `?redirect=${encodeURIComponent(pathname)}`;
  return NextResponse.redirect(loginUrl);
}

function getJwtSecret(): Uint8Array {
  const secret = process.env.JWT_SECRET;
  if (!secret) throw new Error("JWT_SECRET environment variable is not set");
  return new TextEncoder().encode(secret);
}

async function verifyToken(token: string): Promise<boolean> {
  try {
    await jwtVerify(token, getJwtSecret());
    return true;
  } catch {
    return false;
  }
}

export async function proxy(request: NextRequest) {
  const { pathname } = request.nextUrl;

  if (!isProtected(pathname)) {
    return NextResponse.next();
  }

  // 1. Cookie de session
  const sessionToken = request.cookies.get("session_token")?.value;
  if (sessionToken && (await verifyToken(sessionToken))) {
    return NextResponse.next();
  }

  // 2. Header Authorization: Bearer <token>
  const authHeader = request.headers.get("authorization") ?? "";
  if (authHeader.startsWith("Bearer ")) {
    const bearerToken = authHeader.slice(7).trim();
    if (bearerToken && (await verifyToken(bearerToken))) {
      return NextResponse.next();
    }
  }

  return redirectToLogin(request, pathname);
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
