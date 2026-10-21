/**
 * tests/payment402.test.ts
 * Integration Test Suite for HTTP 402 / x402 Micropayment Verification & SSE Remote MCP Server
 * 
 * Verifies:
 * 1. HTTP 402 Payment Required interception when PAYMENT-SIGNATURE is missing
 * 2. Proper base64 encoding of PAYMENT-REQUIRED header (0.002 USDC on Base)
 * 3. HTTP 200 settlement path using mocked facilitator signature (anti-timeout mandate)
 * 4. HTTP 200 settlement path using real cryptographic Viem EVM signature verification
 * 5. Rejection of invalid/tampered signatures
 * 6. Remote MCP SSE endpoint Bearer authentication rejection (401) and acceptance (200 SSE)
 * 7. Inclusion of pricing metadata in MCP tool schemas
 */

import http from 'node:http';
import assert from 'node:assert';
import { privateKeyToAccount } from 'viem/accounts';
import { createRemoteMcpApp } from '../src/mcp/server.ts';
import { decodePaymentRequiredHeader } from '../src/middleware/payment402.ts';

// Setup Test Environment Variables
process.env.NODE_ENV = 'test';
process.env.MOCK_SETTLEMENT = 'true';
process.env.MERCHANT_WALLET_ADDRESS = process.env.MERCHANT_WALLET_ADDRESS || '0x2b8E141680d2A77dC6f5F31346387Fe559eb5681';
process.env.MCP_BEARER_TOKEN = process.env.MCP_BEARER_TOKEN || 'omni_test_mcp_token_xyz';

const MERCHANT_ADDRESS = process.env.MERCHANT_WALLET_ADDRESS;
const BEARER_TOKEN = process.env.MCP_BEARER_TOKEN;

async function runTests() {
  console.log('===============================================================');
  console.log('🚀 Running OmniOperand x402 & Remote MCP Server Integration Tests');
  console.log('===============================================================');

  const { app, mcpServer } = createRemoteMcpApp();
  const server = http.createServer(app);

  // Bind to dynamic ephemeral port on localhost
  await new Promise<void>((resolve, reject) => {
    server.once('error', reject);
    server.listen(0, '127.0.0.1', () => resolve());
  });

  const address = server.address();
  if (!address || typeof address === 'string') {
    throw new Error('Failed to obtain server listening port');
  }
  const baseUrl = `http://localhost:${address.port}`;
  console.log(`📡 Test server running at ${baseUrl}`);

  try {
    // -------------------------------------------------------------
    // Test 1: 402 Rejection Path - Missing PAYMENT-SIGNATURE Header
    // -------------------------------------------------------------
    console.log('\n[Test 1] Verifying HTTP 402 Rejection without PAYMENT-SIGNATURE...');
    const resNoSig = await fetch(`${baseUrl}/api/v1/solve/octagon?driver=side&value=10`, {
      method: 'GET'
    });

    assert.strictEqual(
      resNoSig.status,
      402,
      `Expected status 402 Payment Required, got ${resNoSig.status}`
    );

    const paymentRequiredHeader = resNoSig.headers.get('payment-required');
    assert.ok(
      paymentRequiredHeader,
      'PAYMENT-REQUIRED header must be returned on HTTP 402 response'
    );

    const decoded = decodePaymentRequiredHeader(paymentRequiredHeader);
    assert.ok(decoded, 'PAYMENT-REQUIRED header must be valid base64-encoded JSON');
    assert.strictEqual(decoded.price, '0.002 USDC', 'Header price must specify 0.002 USDC');
    assert.strictEqual(decoded.chain, 'Base', 'Header chain must specify Base');
    assert.strictEqual(decoded.chainId, 8453, 'Header chainId must specify 8453');
    assert.strictEqual(
      decoded.recipient.toLowerCase(),
      MERCHANT_ADDRESS.toLowerCase(),
      'Header recipient must match process.env.MERCHANT_WALLET_ADDRESS'
    );

    interface ErrorResponseBody {
      statusCode?: number;
      error?: string;
      message?: string;
    }

    interface SuccessResponseBody {
      success: boolean;
      calculator: string;
      data: {
        result: Record<string, number>;
      };
      payment: {
        settled: boolean;
        payerAddress?: string;
      };
    }

    const bodyNoSig = (await resNoSig.json()) as ErrorResponseBody;
    assert.strictEqual(bodyNoSig.statusCode, 402);
    assert.strictEqual(bodyNoSig.error, 'Payment Required');
    console.log('  ✅ HTTP 402 rejection path and PAYMENT-REQUIRED header verified successfully.');

    // -------------------------------------------------------------
    // Test 2: 200 Settlement Path - Mock Signature Verification
    // -------------------------------------------------------------
    console.log('\n[Test 2] Verifying HTTP 200 Settlement with Mocked Signature...');
    const resMockSig = await fetch(`${baseUrl}/api/v1/solve/octagon?driver=side&value=10`, {
      method: 'GET',
      headers: {
        'payment-signature': 'mock-valid-signature-unit-test-settled'
      }
    });

    assert.strictEqual(
      resMockSig.status,
      200,
      `Expected status 200 OK with valid mock signature, got ${resMockSig.status}`
    );

    const bodyMockSig = (await resMockSig.json()) as SuccessResponseBody;
    assert.strictEqual(bodyMockSig.success, true);
    assert.strictEqual(bodyMockSig.calculator, 'octagon');
    assert.ok(bodyMockSig.data.result.area > 0, 'Solver result must contain positive area');
    assert.ok(bodyMockSig.payment.settled, 'Settlement status must be true');
    console.log('  ✅ Mock signature settlement path returned 200 OK with verified calculation output.');

    // -------------------------------------------------------------
    // Test 3: 200 Settlement Path - Real Viem Cryptographic Signature
    // -------------------------------------------------------------
    console.log('\n[Test 3] Verifying HTTP 200 Settlement with Real Viem EVM Signature...');
    // Hardhat #0 deterministic test private key for EVM signatures
    const testAccount = privateKeyToAccount(
      '0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80'
    );
    const authMessage = `Pay 0.002 USDC on Base to ${MERCHANT_ADDRESS}`;
    const cryptographicSig = await testAccount.signMessage({ message: authMessage });

    const payload = {
      address: testAccount.address,
      signature: cryptographicSig,
      message: authMessage,
      amount: '0.002 USDC',
      chain: 'Base'
    };

    const resViemSig = await fetch(`${baseUrl}/api/v1/solve/mortgage`, {
      method: 'POST',
      headers: {
        'content-type': 'application/json',
        'payment-signature': JSON.stringify(payload)
      },
      body: JSON.stringify({
        principal: 400000,
        annual_rate: 6.5,
        term_years: 30
      })
    });

    assert.strictEqual(
      resViemSig.status,
      200,
      `Expected status 200 OK with real Viem signature, got ${resViemSig.status}`
    );

    const bodyViemSig = (await resViemSig.json()) as SuccessResponseBody;
    assert.strictEqual(bodyViemSig.success, true);
    assert.strictEqual(bodyViemSig.calculator, 'mortgage');
    assert.strictEqual(
      bodyViemSig.payment.payerAddress?.toLowerCase(),
      testAccount.address.toLowerCase(),
      'Payer address verified by Viem must match signer'
    );
    assert.ok(
      bodyViemSig.data.result.monthly_principal_and_interest > 0,
      'Mortgage P&I must be calculated'
    );
    console.log('  ✅ Viem cryptographic EVM signature verified on Base with 200 settlement.');

    // -------------------------------------------------------------
    // Test 4: 402 Rejection Path - Invalid / Tampered Signature
    // -------------------------------------------------------------
    console.log('\n[Test 4] Verifying Rejection with Invalid / Tampered Signature...');
    const resInvalidSig = await fetch(`${baseUrl}/api/v1/solve/octagon?driver=side&value=10`, {
      method: 'GET',
      headers: {
        'payment-signature': 'mock-invalid-signature-rejected'
      }
    });

    assert.strictEqual(
      resInvalidSig.status,
      402,
      `Expected status 402 for invalid signature, got ${resInvalidSig.status}`
    );

    const bodyInvalid = (await resInvalidSig.json()) as ErrorResponseBody;
    assert.strictEqual(bodyInvalid.error, 'Payment Required: Invalid Signature');
    console.log('  ✅ Invalid signature rejected with HTTP 402 and execution was blocked.');

    // -------------------------------------------------------------
    // Test 5: Remote MCP Server - Bearer Authentication Enforcement
    // -------------------------------------------------------------
    console.log('\n[Test 5] Verifying Remote MCP Server SSE Bearer Authentication...');
    // Without token -> 401
    const resNoToken = await fetch(`${baseUrl}/sse`);
    assert.strictEqual(
      resNoToken.status,
      401,
      `Expected status 401 Unauthorized without bearer token, got ${resNoToken.status}`
    );

    // With invalid token -> 401
    const resWrongToken = await fetch(`${baseUrl}/sse`, {
      headers: {
        authorization: 'Bearer wrong-secret-token'
      }
    });
    assert.strictEqual(
      resWrongToken.status,
      401,
      `Expected status 401 Unauthorized with wrong bearer token, got ${resWrongToken.status}`
    );

    // With valid token -> 200 with text/event-stream
    const controller = new AbortController();
    const resSseValid = await fetch(`${baseUrl}/sse`, {
      headers: {
        authorization: `Bearer ${BEARER_TOKEN}`
      },
      signal: controller.signal
    });

    assert.strictEqual(resSseValid.status, 200, `Expected 200 for valid SSE connection, got ${resSseValid.status}`);
    const contentType = resSseValid.headers.get('content-type');
    assert.ok(
      contentType && contentType.includes('text/event-stream'),
      `Content-Type must be text/event-stream, got ${contentType}`
    );
    controller.abort(); // Close client stream cleanly
    console.log('  ✅ Remote MCP Server SSE endpoint properly enforces Bearer authentication.');

    // -------------------------------------------------------------
    // Test 6: MCP Tool Schema Pricing Metadata Validation
    // -------------------------------------------------------------
    console.log('\n[Test 6] Verifying MCP Tool Schema Pricing Metadata...');
    // Inspect underlying registered tools from the McpServer instance
    const registeredTools = (mcpServer as unknown as { _registeredTools: Record<string, unknown> })._registeredTools;
    const toolNames = Object.keys(registeredTools);
    assert.ok(toolNames.length >= 10, `Must expose at least 10 calculator tools, found ${toolNames.length}`);

    const octagonTool = registeredTools['omni_octagon_solver'] as {
      description?: string;
      _meta?: { pricing?: { price?: string; chain?: string } };
    };
    assert.ok(octagonTool, 'omni_octagon_solver tool must be registered');
    assert.ok(
      octagonTool.description?.includes('0.002 USDC'),
      'Tool description must document 0.002 USDC pricing'
    );
    assert.ok(octagonTool._meta?.pricing, 'Tool must include _meta.pricing metadata');
    assert.strictEqual(octagonTool._meta?.pricing?.price, '0.002 USDC');
    assert.strictEqual(octagonTool._meta?.pricing?.chain, 'Base');
    console.log('  ✅ MCP Tool schemas successfully populated with pricing metadata (_meta.pricing).');

    console.log('\n===============================================================');
    console.log('🎉 ALL 6 INTEGRATION TESTS PASSED WITH 100% SUCCESS!');
    console.log('===============================================================');
  } finally {
    await new Promise<void>((resolve) => {
      server.close(() => resolve());
    });
    console.log('🧹 Test server shut down cleanly.');
  }
}

runTests().catch((err) => {
  console.error('❌ Test failed with error:', err);
  process.exit(1);
});
