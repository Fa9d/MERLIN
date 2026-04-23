import "server-only";

import type { PrismaClient } from "@/generated/prisma/client";

declare global {
  var __merlinPrisma: PrismaClient | undefined;
}

// The frontend app currently goes through the FastAPI backend rather than
// opening a direct Prisma connection during Next.js runtime.
export const db = global.__merlinPrisma;
