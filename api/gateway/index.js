/**
 * api/gateway/index.js
 * OmniOperand API Gateway — Authentication, Tier Management, Rate Limiting & Metering
 */

// Universal crypto support (Web Crypto in Cloudflare Workers / Browser, crypto in Node)
async function sha256Hex(text) {
  if (typeof crypto !== 'undefined' && crypto.subtle) {
    const encoder = new TextEncoder();
    const data = encoder.encode(text);
    const hashBuffer = await crypto.subtle.digest('SHA-256', data);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
  } else {
    // Fallback for Node.js if crypto.subtle is not accessible
    const nodeCrypto = await import('crypto');
    return nodeCrypto.createHash('sha256').update(text).digest('hex');
  }
}

function generateSecureRandomHex(bytes = 24) {
  const arr = new Uint8Array(bytes);
  if (typeof crypto !== 'undefined' && crypto.getRandomValues) {
    crypto.getRandomValues(arr);
  } else {
    for (let i = 0; i < bytes; i++) {
      arr[i] = Math.floor(Math.random() * 256);
    }
  }
  return Array.from(arr).map(b => b.toString(16).padStart(2, '0')).join('');
}

// Tier Configurations
export const TIERS = {
  anonymous: {
    name: 'Anonymous',
    requestsPerMinute: 3,
    requestsPerMonth: 100
  },
  free: {
    name: 'Free',
    requestsPerMinute: 5,
    requestsPerMonth: 500
  },
  pro: {
    name: 'Pro',
    requestsPerMinute: 60,
    requestsPerMonth: 50000
  },
  enterprise: {
    name: 'Enterprise',
    requestsPerMinute: 300,
    requestsPerMonth: 1000000
  }
};

// In-Memory Key Registry & Pre-configured test keys
class ApiKeyRegistry {
  constructor() {
    this.keysByHash = new Map();
    this.keysByRaw = new Map();
    this.seedDefaultKeys();
  }

  seedDefaultKeys() {
    // Seed standard test keys for zero-config evaluation
    const demoKeys = [
      { raw: 'omni_live_free_demo_key_123', tier: 'free', consumerId: 'usr_demo_free', name: 'Demo Free Tier Key' },
      { raw: 'omni_live_pro_demo_key_456', tier: 'pro', consumerId: 'usr_demo_pro', name: 'Demo Pro Tier Key' },
      { raw: 'omni_live_enterprise_demo_key_789', tier: 'enterprise', consumerId: 'usr_demo_ent', name: 'Demo Enterprise Tier Key' }
    ];

    for (const k of demoKeys) {
      this.registerDirect(k.raw, k.tier, k.consumerId, k.name);
    }
  }

  registerDirect(rawKey, tier = 'free', consumerId = null, name = 'API Key') {
    const id = consumerId || `usr_${generateSecureRandomHex(8)}`;
    const record = {
      consumerId: id,
      tier: tier.toLowerCase(),
      name,
      createdAt: new Date().toISOString(),
      active: true,
      rawKeyPreview: `${rawKey.slice(0, 10)}...${rawKey.slice(-4)}`
    };
    this.keysByRaw.set(rawKey, record);
    return record;
  }

  async createKey(tier = 'free', name = 'Default API Key', email = null) {
    const randomPart = generateSecureRandomHex(24);
    const rawKey = `omni_${tier === 'enterprise' ? 'ent' : tier}_${randomPart}`;
    const keyHash = await sha256Hex(rawKey);
    const consumerId = `usr_${generateSecureRandomHex(8)}`;

    const record = {
      consumerId,
      tier: tier.toLowerCase(),
      name,
      email: email || null,
      keyHash,
      createdAt: new Date().toISOString(),
      active: true,
      rawKeyPreview: `${rawKey.slice(0, 10)}...${rawKey.slice(-4)}`
    };

    this.keysByRaw.set(rawKey, record);
    this.keysByHash.set(keyHash, record);

    return {
      apiKey: rawKey,
      keyHash,
      consumerId,
      tier: record.tier,
      name: record.name,
      createdAt: record.createdAt,
      quota: TIERS[record.tier] || TIERS.free
    };
  }

  async validateKey(rawKey) {
    if (!rawKey || typeof rawKey !== 'string') return null;
    const cleanKey = rawKey.trim();

    // Check direct memory cache
    if (this.keysByRaw.has(cleanKey)) {
      const rec = this.keysByRaw.get(cleanKey);
      if (rec.active) return rec;
    }

    // Check hash lookup
    const keyHash = await sha256Hex(cleanKey);
    if (this.keysByHash.has(keyHash)) {
      const rec = this.keysByHash.get(keyHash);
      if (rec.active) return rec;
    }

    return null;
  }
}

export const apiKeyRegistry = new ApiKeyRegistry();

// Sliding-Window Rate Limiter
class RateLimiter {
  constructor() {
    // Map of consumerId -> { minuteRequests: [timestamps], monthCount: number, monthResetTime: number }
    this.clients = new Map();
  }

  getClientState(consumerId) {
    const now = Date.now();
    let state = this.clients.get(consumerId);
    if (!state) {
      state = {
        minuteRequests: [],
        monthCount: 0,
        monthResetTime: now + 30 * 24 * 60 * 60 * 1000
      };
      this.clients.set(consumerId, state);
    }

    // Reset monthly bucket if 30 days passed
    if (now >= state.monthResetTime) {
      state.monthCount = 0;
      state.monthResetTime = now + 30 * 24 * 60 * 60 * 1000;
    }

    // Clean up timestamps older than 60 seconds
    const oneMinAgo = now - 60000;
    state.minuteRequests = state.minuteRequests.filter(ts => ts > oneMinAgo);

    return state;
  }

  checkRateLimit(consumerId, tierKey = 'free') {
    const now = Date.now();
    const tierConfig = TIERS[tierKey.toLowerCase()] || TIERS.free;
    const state = this.getClientState(consumerId);

    const minuteLimit = tierConfig.requestsPerMinute;
    const monthLimit = tierConfig.requestsPerMonth;

    const currentMinuteCount = state.minuteRequests.length;
    const currentMonthCount = state.monthCount;

    // Calculate reset time (when the oldest request in the current minute window expires)
    let resetSeconds = 60;
    if (state.minuteRequests.length > 0) {
      const oldest = state.minuteRequests[0];
      resetSeconds = Math.max(1, Math.ceil((oldest + 60000 - now) / 1000));
    }

    const remainingMinute = Math.max(0, minuteLimit - currentMinuteCount);

    if (currentMinuteCount >= minuteLimit) {
      return {
        allowed: false,
        reason: 'MINUTE_RATE_LIMIT_EXCEEDED',
        limit: minuteLimit,
        remaining: 0,
        resetSeconds,
        tier: tierKey,
        currentUsageMonth: currentMonthCount,
        monthLimit
      };
    }

    if (currentMonthCount >= monthLimit) {
      return {
        allowed: false,
        reason: 'MONTHLY_QUOTA_EXCEEDED',
        limit: minuteLimit,
        remaining: 0,
        resetSeconds,
        tier: tierKey,
        currentUsageMonth: currentMonthCount,
        monthLimit
      };
    }

    // Record request
    state.minuteRequests.push(now);
    state.monthCount++;

    return {
      allowed: true,
      limit: minuteLimit,
      remaining: Math.max(0, minuteLimit - (currentMinuteCount + 1)),
      resetSeconds,
      tier: tierKey,
      currentUsageMonth: state.monthCount,
      monthLimit
    };
  }

  reset(consumerId) {
    if (consumerId) {
      this.clients.delete(consumerId);
    } else {
      this.clients.clear();
    }
  }
}

export const rateLimiter = new RateLimiter();

// Usage Tracking & Billing Ledger
class UsageTracker {
  constructor(maxLogRetention = 5000) {
    this.maxRetention = maxLogRetention;
    this.logs = [];
    this.consumerStats = new Map();
  }

  recordRequest({ consumerId, tier, path, method, status, latencyMs, timestamp = new Date().toISOString() }) {
    const entry = {
      id: `req_${generateSecureRandomHex(12)}`,
      consumerId,
      tier,
      path,
      method,
      status,
      latencyMs: roundTo(latencyMs, 2),
      timestamp
    };

    this.logs.push(entry);
    if (this.logs.length > this.maxRetention) {
      this.logs.shift();
    }

    // Update aggregate stats
    let stats = this.consumerStats.get(consumerId);
    if (!stats) {
      stats = {
        consumerId,
        tier,
        totalRequests: 0,
        successfulRequests: 0,
        failedRequests: 0,
        totalLatencyMs: 0,
        endpoints: {}
      };
      this.consumerStats.set(consumerId, stats);
    }

    stats.totalRequests++;
    if (status >= 200 && status < 400) stats.successfulRequests++;
    else stats.failedRequests++;
    stats.totalLatencyMs += latencyMs;
    stats.endpoints[path] = (stats.endpoints[path] || 0) + 1;

    return entry;
  }

  getConsumerStats(consumerId) {
    const stats = this.consumerStats.get(consumerId);
    if (!stats) {
      return {
        consumerId,
        totalRequests: 0,
        successfulRequests: 0,
        failedRequests: 0,
        averageLatencyMs: 0,
        endpoints: {}
      };
    }
    return {
      ...stats,
      averageLatencyMs: stats.totalRequests > 0 ? roundTo(stats.totalLatencyMs / stats.totalRequests, 2) : 0
    };
  }

  getRecentLogs(limit = 100, consumerId = null) {
    let filtered = this.logs;
    if (consumerId) {
      filtered = filtered.filter(l => l.consumerId === consumerId);
    }
    return filtered.slice(-limit).reverse();
  }
}

function roundTo(val, dec = 2) {
  const f = Math.pow(10, dec);
  return Math.round(val * f) / f;
}

export const usageTracker = new UsageTracker();

// Standardized JSON Response Formatter
export function formatSuccessResponse({ calculator, inputs, result, units = {}, executionTimeMs = 0, meta = {} }) {
  return {
    success: true,
    calculator,
    inputs,
    result,
    execution_time_ms: roundTo(executionTimeMs, 2),
    units,
    ...(Object.keys(meta).length > 0 ? { meta } : {})
  };
}

export function formatErrorResponse({ code, message, executionTimeMs = 0, details = null }) {
  return {
    success: false,
    error: {
      code,
      message,
      ...(details ? { details } : {})
    },
    execution_time_ms: roundTo(executionTimeMs, 2)
  };
}

// Auth Header Parser
export function extractApiKey(requestOrHeaders) {
  let authHeader = null;
  let apiKeyHeader = null;

  if (typeof requestOrHeaders.headers?.get === 'function') {
    authHeader = requestOrHeaders.headers.get('Authorization') || requestOrHeaders.headers.get('authorization');
    apiKeyHeader = requestOrHeaders.headers.get('x-api-key') || requestOrHeaders.headers.get('X-API-Key');
  } else if (typeof requestOrHeaders === 'object') {
    authHeader = requestOrHeaders['authorization'] || requestOrHeaders['Authorization'];
    apiKeyHeader = requestOrHeaders['x-api-key'] || requestOrHeaders['X-API-Key'];
  }

  if (apiKeyHeader) {
    return apiKeyHeader.trim();
  }

  if (authHeader && authHeader.toLowerCase().startsWith('bearer ')) {
    return authHeader.slice(7).trim();
  }

  return null;
}
