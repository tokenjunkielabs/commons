import { reconcileMatch } from "@/lib/match-actions"
import { supabaseAdmin } from "@/lib/supabase-admin"

type ReconcileOutcome = {
  matchId: string
  success: boolean
  error?: string
}

/**
 * Reconciles every match whose server-side deadline has passed.
 *
 * Candidate discovery is deliberately separate from reconcileMatch(): this
 * function finds all expired in-flight matches, while reconcileMatch remains
 * the single-match/idempotent authority for deciding whether settlement or a
 * stake-timeout refund is still required when each candidate is processed.
 */
export async function reconcileExpiredMatches() {
  try {
    const now = new Date().toISOString()

    const [activeResult, awaitingStakesResult] = await Promise.all([
      supabaseAdmin.from("matches").select("id").eq("status", "active").lt("ends_at", now),
      supabaseAdmin
        .from("matches")
        .select("id")
        .eq("status", "awaiting_stakes")
        .lt("stake_deadline_at", now),
    ])

    if (activeResult.error || awaitingStakesResult.error) {
      return {
        success: false,
        error:
          activeResult.error?.message ??
          awaitingStakesResult.error?.message ??
          "Failed to load expired matches",
      }
    }

    const matchIds = Array.from(
      new Set<string>([
        ...(activeResult.data ?? []).map((row) => row.id),
        ...(awaitingStakesResult.data ?? []).map((row) => row.id),
      ]),
    )

    const outcomes: ReconcileOutcome[] = []

    // Process sequentially so one cron invocation does not fan out a burst of
    // escrow/Supabase operations when many matches expire at the same time.
    for (const matchId of matchIds) {
      const result = await reconcileMatch(matchId)
      const error =
        "error" in result && typeof result.error === "string" ? result.error : "Unknown reconciliation error"

      outcomes.push({
        matchId,
        success: result.success,
        ...(result.success ? {} : { error }),
      })
    }

    const failed = outcomes.filter((outcome) => !outcome.success).length

    return {
      success: failed === 0,
      data: {
        candidates: matchIds.length,
        processed: outcomes.length,
        failed,
      },
      outcomes,
    }
  } catch (error) {
    console.error("Error in reconcileExpiredMatches:", error)
    return { success: false, error: "Failed to reconcile expired matches" }
  }
}
