import "server-only";

declare global {
  var __merlinPrisma: unknown;
}

// The frontend app currently goes through the FastAPI backend rather than
// opening a direct Prisma connection during Next.js runtime.
export const db = global.__merlinPrisma;
