import { NextRequest, NextResponse } from "next/server";

/**
 * Routes protégées — accès interdit sans authentification.
 * Tout sous-chemin de ces préfixes est également protégé.
 */
const PROTECTED_PREFIXES = [
  "/espace-praticien",
  "/operator",
  "/supervision",
  "/admin",
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
  "/suivi",
]);

function isProtected(pathname: string): boolean {
  if (PUBLIC_PATHS.has(pathname)) return false;
  return PROTECTED_PREFIXES.some(
    (prefix) => pathname === prefix || pathname.startsWith(prefix + "/")
  );
}

function redirectToLogin(request: NextRequest, pathname: string): NextResponse {
  const loginUrl = request.nextUrl.clone();
  loginUrl.pathname = "/acces-client";
  loginUrl.search = `?redirect=${encodeURIComponent(pathname)}`;
  return NextResponse.redirect(loginUrl);
}

function base64urlDecode(str: string): string {
  const padded = str + "=".repeat((4 - (str.length % 4)) % 4);
  const base64 = padded.replace(/-/g, "+").replace(/_/g, "/");
  return atob(base64);
}

async function hmacSha256Hex(secret: string, message: string): Promise<string> {
  const enc = new TextEncoder();
  const key = await crypto.subtle.importKey(
    "raw",
    enc.encode(secret),
    { name: "HMAC", hash: "SHA-256" },
    false,
    ["sign"]
  );
  const sig = await crypto.subtle.sign("HMAC", key, enc.encode(message));
  return Array.from(new Uint8Array(sig))
    .map((b) => b.toString(16).padStart(2, "0"))
    .join("");
}

async function verifyToken(token: string): Promise<boolean> {
  try {
    const secret = process.env.JWT_SECRET;
    if (!secret) return false;

    const dotIdx = token.lastIndexOf(".");
    if (dotIdx < 0) return false;

    const payloadB64 = token.slice(0, dotIdx);
    const signature = token.slice(dotIdx + 1);

    const expectedSig = await hmacSha256Hex(secret, payloadB64);
    if (expectedSig !== signature) return false;

    const payload = JSON.parse(base64urlDecode(payloadB64));
    const now = Math.floor(Date.now() / 1000);
    if (payload.exp && payload.exp < now) return false;

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
