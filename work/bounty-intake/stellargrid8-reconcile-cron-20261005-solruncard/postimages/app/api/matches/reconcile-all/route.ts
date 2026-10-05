import { type NextRequest, NextResponse } from "next/server"
import { reconcileExpiredMatches } from "@/lib/reconcile-expired-matches"

export const dynamic = "force-dynamic"
export const runtime = "nodejs"

// Vercel Cron includes `Authorization: Bearer <CRON_SECRET>` when CRON_SECRET
// is configured for the deployment. Fail closed rather than expose a public
// endpoint that can trigger money-adjacent settlement/refund operations.
export async function GET(request: NextRequest) {
  const secret = process.env.CRON_SECRET
  if (!secret) {
    return NextResponse.json({ success: false, error: "CRON_SECRET is not configured" }, { status: 500 })
  }

  if (request.headers.get("authorization") !== `Bearer ${secret}`) {
    return NextResponse.json({ success: false, error: "Unauthorized" }, { status: 401 })
  }

  const result = await reconcileExpiredMatches()
  return NextResponse.json(result, { status: result.success ? 200 : 500 })
}
