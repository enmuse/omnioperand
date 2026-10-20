/**
 * functions/api/v1/usage.js
 * Usage Telemetry & Billing Ledger Endpoint
 * GET /api/v1/usage -> Inspect request volume, latency, and tier limits
 */

import { usageTracker, formatSuccessResponse } from '../../../api/gateway/index.js';

export async function onRequestGet(context) {
  const start = performance.now();
  const consumerId = context.data?.consumerId || 'usr_anonymous';
  const tier = context.data?.tier || 'free';

  const stats = usageTracker.getConsumerStats(consumerId);
  const recentLogs = usageTracker.getRecentLogs(20, consumerId);

  const execMs = performance.now() - start;

  return new Response(JSON.stringify(formatSuccessResponse({
    calculator: "usage_telemetry",
    inputs: { consumer_id: consumerId, tier },
    result: {
      consumer_id: consumerId,
      tier,
      total_requests: stats.totalRequests,
      successful_requests: stats.successfulRequests,
      failed_requests: stats.failedRequests,
      average_latency_ms: stats.averageLatencyMs,
      endpoint_breakdown: stats.endpoints,
      recent_transactions: recentLogs,
      billing_integration: {
        meter_event_name: "calculator_invocations",
        currency: "USD",
        status: "ready_for_stripe_webhooks"
      }
    },
    executionTimeMs: execMs
  }), null, 2), {
    status: 200,
    headers: { "Content-Type": "application/json" }
  });
}
