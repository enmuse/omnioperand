/**
 * src/mcp/server.ts
 * OmniOperand Remote Model Context Protocol (MCP) Server with SSE Transport
 * 
 * Exposes deterministic mathematical calculation tools to AI agents over SSE,
 * enforcing Bearer authentication and including Base EVM x402 micropayment pricing metadata.
 */

import express, { type Request, type Response, type NextFunction, type Application } from 'express';
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { SSEServerTransport } from '@modelcontextprotocol/sdk/server/sse.js';
import { z } from 'zod';
import {
  CALCULATOR_REGISTRY,
  solveOctagon,
  solveRegularPolygon,
  solveMortgage,
  solveCompoundInterest,
  solveCagr,
  solveAutoLoan,
  solveConcreteVolume,
  solveRoofPitch,
  solveCircleSector,
  solveRightTriangle
} from '../../api/solvers/index.js';
import { payment402Middleware } from '../middleware/payment402.ts';

/**
 * Standard pricing metadata attached to all tool schemas
 */
export function getToolPricingMetadata(calculatorName: string) {
  const recipient = process.env.MERCHANT_WALLET_ADDRESS ?? '';
  return {
    pricing: {
      price: '0.002 USDC',
      amount: '0.002',
      currency: 'USDC',
      chain: 'Base',
      chainId: 8453,
      recipient,
      tokenAddress: '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913',
      calculator: calculatorName
    }
  };
}

/**
 * Creates and registers all calculator tools on an McpServer instance
 */
export function createOmniOperandMcpServer(): McpServer {
  const server = new McpServer({
    name: 'OmniOperand High-Precision Math Engine',
    version: '1.0.0'
  });

  // 1. Regular Octagon Solver
  server.registerTool(
    'omni_octagon_solver',
    {
      title: 'Regular Octagon Solver',
      description: '[Price: 0.002 USDC on Base] Exact 8-variable regular octagon solver with radical closed-form geometry and bidirectional inversion.',
      inputSchema: {
        driver: z.enum([
          'side', 'a', 'area', 'a_poly', 'perimeter', 'p',
          'apothem', 'inradius', 'r_i', 'circumradius', 'r',
          'span', 's', 'short_diagonal', 'd_s', 'long_diagonal', 'd_l'
        ]).default('side').describe('The known reference parameter driving the calculation'),
        value: z.number().positive().describe('Numerical value of the known driver parameter'),
        precision: z.number().int().min(2).max(14).default(6).describe('Decimal places of precision (2-14)'),
        units: z.string().default('units').describe('Measurement unit identifier')
      },
      _meta: getToolPricingMetadata('octagon')
    },
    async (params) => {
      const result = solveOctagon(params);
      return {
        content: [{ type: 'text', text: JSON.stringify(result, null, 2) }]
      };
    }
  );

  // 2. Universal Regular Polygon Solver
  server.registerTool(
    'omni_regular_polygon_solver',
    {
      title: 'Universal Regular N-Gon Solver',
      description: '[Price: 0.002 USDC on Base] Universal regular n-sided polygon solver for any arbitrary n (3 to 1000). Resolves apothem, circumradius, area, perimeter, and internal angles.',
      inputSchema: {
        n: z.number().int().min(3).max(1000).default(8).describe('Number of polygon vertices/sides (3-1000)'),
        driver: z.enum(['side', 'a', 'area', 'perimeter', 'apothem', 'inradius', 'circumradius', 'span']).default('side'),
        value: z.number().positive().describe('Numerical value of the driving parameter'),
        precision: z.number().int().min(2).max(14).default(6)
      },
      _meta: getToolPricingMetadata('regular-polygon')
    },
    async (params) => {
      const result = solveRegularPolygon(params);
      return {
        content: [{ type: 'text', text: JSON.stringify(result, null, 2) }]
      };
    }
  );

  // 3. Mortgage Amortization Solver
  server.registerTool(
    'omni_mortgage_solver',
    {
      title: 'Mortgage Amortization Solver',
      description: '[Price: 0.002 USDC on Base] Exact mortgage amortization, monthly P&I, total interest, and early payoff acceleration calculator.',
      inputSchema: {
        principal: z.number().positive().describe('Total mortgage loan principal balance ($)'),
        annual_rate: z.number().min(0).max(100).describe('Fixed annual interest rate in percent (e.g. 6.5)'),
        term_years: z.number().min(1).max(50).describe('Loan amortization term in years'),
        extra_monthly: z.number().min(0).default(0).describe('Optional extra principal payment per month ($)')
      },
      _meta: getToolPricingMetadata('mortgage')
    },
    async (params) => {
      const result = solveMortgage(params);
      return {
        content: [{ type: 'text', text: JSON.stringify(result, null, 2) }]
      };
    }
  );

  // 4. Compound Interest Solver
  server.registerTool(
    'omni_compound_interest_solver',
    {
      title: 'Compound Interest Solver',
      description: '[Price: 0.002 USDC on Base] Deterministic compound interest and APY growth simulator with periodic contributions.',
      inputSchema: {
        principal: z.number().min(0).describe('Initial principal investment balance ($)'),
        annual_rate: z.number().min(0).describe('Annual interest rate in percent (e.g. 7.0)'),
        years: z.number().positive().describe('Investment horizon duration in years'),
        compound_frequency: z.number().int().default(12).describe('Frequency per year: 1=annual, 4=quarterly, 12=monthly, 365=daily'),
        monthly_contribution: z.number().min(0).default(0).describe('Recurring monthly deposit ($)')
      },
      _meta: getToolPricingMetadata('compound-interest')
    },
    async (params) => {
      const result = solveCompoundInterest(params);
      return {
        content: [{ type: 'text', text: JSON.stringify(result, null, 2) }]
      };
    }
  );

  // 5. CAGR Solver
  server.registerTool(
    'omni_cagr_solver',
    {
      title: 'Compound Annual Growth Rate (CAGR) Solver',
      description: '[Price: 0.002 USDC on Base] Calculates Compound Annual Growth Rate (CAGR), absolute return, and multiple on capital.',
      inputSchema: {
        initial_value: z.number().positive().describe('Starting portfolio or asset valuation ($)'),
        final_value: z.number().min(0).describe('Ending portfolio or asset valuation ($)'),
        years: z.number().positive().describe('Time elapsed in years')
      },
      _meta: getToolPricingMetadata('cagr')
    },
    async (params) => {
      const result = solveCagr(params);
      return {
        content: [{ type: 'text', text: JSON.stringify(result, null, 2) }]
      };
    }
  );

  // 6. Auto Loan Solver
  server.registerTool(
    'omni_auto_loan_solver',
    {
      title: 'Auto Loan Financing Solver',
      description: '[Price: 0.002 USDC on Base] Auto loan payment and interest analyzer with down payments, trade-in credits, and state sales tax adjustments.',
      inputSchema: {
        vehicle_price: z.number().positive().describe('Agreed vehicle purchase price ($)'),
        down_payment: z.number().min(0).default(0).describe('Cash down payment ($)'),
        trade_in: z.number().min(0).default(0).describe('Trade-in equity credit ($)'),
        interest_rate: z.number().min(0).default(5.9).describe('Annual loan interest rate (%)'),
        term_months: z.number().int().min(6).default(60).describe('Financing term in months'),
        sales_tax_pct: z.number().min(0).default(6.0).describe('State and local sales tax (%)')
      },
      _meta: getToolPricingMetadata('auto-loan')
    },
    async (params) => {
      const result = solveAutoLoan(params);
      return {
        content: [{ type: 'text', text: JSON.stringify(result, null, 2) }]
      };
    }
  );

  // 7. Concrete Volume Solver
  server.registerTool(
    'omni_concrete_volume_solver',
    {
      title: 'Concrete Volume & Structural Sizing Solver',
      description: '[Price: 0.002 USDC on Base] Structural concrete volume and bag estimation engine for slabs, footings, and cylindrical columns.',
      inputSchema: {
        shape: z.enum(['slab', 'footing', 'column']).default('slab'),
        length: z.number().positive().default(20).describe('Length in feet'),
        width: z.number().positive().default(10).describe('Width in feet'),
        depth: z.number().positive().default(4).describe('Thickness or depth in inches'),
        diameter: z.number().positive().optional().describe('Column diameter in inches'),
        height: z.number().positive().optional().describe('Column height in feet')
      },
      _meta: getToolPricingMetadata('concrete-volume')
    },
    async (params) => {
      const result = solveConcreteVolume(params);
      return {
        content: [{ type: 'text', text: JSON.stringify(result, null, 2) }]
      };
    }
  );

  // 8. Roof Pitch Solver
  server.registerTool(
    'omni_roof_pitch_solver',
    {
      title: 'Architectural Roof Pitch Solver',
      description: '[Price: 0.002 USDC on Base] Calculates architectural roof pitch ratio (x:12), angle in degrees, pitch multiplier, and full rafter length.',
      inputSchema: {
        rise: z.number().positive().describe('Vertical rise in inches'),
        run: z.number().positive().default(12).describe('Horizontal run in inches (default is 12)'),
        building_run_feet: z.number().positive().default(16).describe('Horizontal run of the building in feet')
      },
      _meta: getToolPricingMetadata('roof-pitch')
    },
    async (params) => {
      const result = solveRoofPitch(params);
      return {
        content: [{ type: 'text', text: JSON.stringify(result, null, 2) }]
      };
    }
  );

  // 9. Circle Sector Solver
  server.registerTool(
    'omni_circle_sector_solver',
    {
      title: 'Circle Sector & Arc Solver',
      description: '[Price: 0.002 USDC on Base] Circle sector analyzer computing arc length, chord length, sagitta height, and sector area.',
      inputSchema: {
        radius: z.number().positive().describe('Radius of the circle'),
        angle_deg: z.number().positive().max(360).describe('Central angle in degrees')
      },
      _meta: getToolPricingMetadata('circle-sector')
    },
    async (params) => {
      const result = solveCircleSector(params);
      return {
        content: [{ type: 'text', text: JSON.stringify(result, null, 2) }]
      };
    }
  );

  // 10. Right Triangle Solver
  server.registerTool(
    'omni_right_triangle_solver',
    {
      title: 'Right Triangle Pythagorean Solver',
      description: '[Price: 0.002 USDC on Base] Deterministic right triangle solver computing hypotenuse, area, altitude, inradius, and acute angles.',
      inputSchema: {
        leg_a: z.number().positive().describe('Length of leg a'),
        leg_b: z.number().positive().describe('Length of leg b')
      },
      _meta: getToolPricingMetadata('right-triangle')
    },
    async (params) => {
      const result = solveRightTriangle(params);
      return {
        content: [{ type: 'text', text: JSON.stringify(result, null, 2) }]
      };
    }
  );

  return server;
}

/**
 * Bearer Authentication Middleware for Remote MCP Server
 */
export function bearerAuthMiddleware(req: Request, res: Response, next: NextFunction): void {
  const authHeader = req.headers['authorization'];
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    res.status(401).json({
      error: 'Unauthorized',
      message: 'Bearer token required for remote MCP access. Header format: Authorization: Bearer <token>'
    });
    return;
  }

  const token = authHeader.slice(7).trim();
  const configuredToken = process.env.MCP_BEARER_TOKEN ?? process.env.BEARER_TOKEN;

  if (configuredToken && token !== configuredToken) {
    res.status(401).json({
      error: 'Unauthorized',
      message: 'Invalid bearer token'
    });
    return;
  }

  if (token.length === 0) {
    res.status(401).json({
      error: 'Unauthorized',
      message: 'Bearer token cannot be empty'
    });
    return;
  }

  next();
}

/**
 * Creates the complete Express application wiring SSE MCP server and HTTP 402 payment routes
 */
export function createRemoteMcpApp(): { app: Application; mcpServer: McpServer; transports: Map<string, SSEServerTransport> } {
  const app: Application = express();
  app.use(express.json());

  const mcpServer = createOmniOperandMcpServer();
  const transports = new Map<string, SSEServerTransport>();

  // Health and System Diagnostics
  app.get('/health', (_req: Request, res: Response) => {
    res.status(200).json({
      status: 'healthy',
      platform: 'OmniOperand Remote MCP Server',
      protocol: 'SSE + HTTP 402 / x402',
      pricing: '0.002 USDC on Base',
      solvers: Object.keys(CALCULATOR_REGISTRY).length,
      recipient: process.env.MERCHANT_WALLET_ADDRESS ?? 'unconfigured'
    });
  });

  // 1. MCP SSE Connection Endpoint (with Bearer Authentication)
  app.get('/sse', bearerAuthMiddleware, async (req: Request, res: Response) => {
    try {
      const transport = new SSEServerTransport('/message', res);
      const sessionId = transport.sessionId;
      transports.set(sessionId, transport);

      transport.onclose = () => {
        transports.delete(sessionId);
      };

      await mcpServer.connect(transport);
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : String(err);
      if (!res.headersSent) {
        res.status(500).json({ error: 'SSE Transport Initialization Failed', message: msg });
      }
    }
  });

  // 2. MCP Client Message POST Endpoint (with Bearer Authentication)
  app.post('/message', bearerAuthMiddleware, async (req: Request, res: Response) => {
    const sessionId = req.query.sessionId as string | undefined;
    if (!sessionId) {
      res.status(400).json({ error: 'Missing sessionId query parameter' });
      return;
    }

    const transport = transports.get(sessionId);
    if (!transport) {
      res.status(404).json({ error: 'Session not found or connection terminated' });
      return;
    }

    try {
      await transport.handlePostMessage(req, res, req.body);
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : String(err);
      if (!res.headersSent) {
        res.status(500).json({ error: 'Failed handling client message', message: msg });
      }
    }
  });

  // 3. HTTP 402 Micropayment Calculator Routes (Direct HTTP API)
  const handleCalculatorRequest = (req: Request, res: Response): void => {
    const rawCalc = req.params.calculator;
    const calcId = Array.isArray(rawCalc) ? rawCalc[0] : rawCalc;
    if (!calcId) {
      res.status(400).json({ error: 'Missing calculator parameter in path' });
      return;
    }
    const solver = (CALCULATOR_REGISTRY as Record<string, (params: unknown) => unknown>)[calcId];
    if (!solver) {
      res.status(404).json({
        error: 'Calculator Not Found',
        requested: calcId,
        available: Object.keys(CALCULATOR_REGISTRY)
      });
      return;
    }

    const params = req.method === 'POST' ? req.body : req.query;
    const result = solver(params ?? {});
    res.status(200).json({
      success: true,
      calculator: calcId,
      data: result,
      payment: (req as Request & { payment?: unknown }).payment
    });
  };

  app.post('/api/v1/solve/:calculator', payment402Middleware, handleCalculatorRequest);
  app.get('/api/v1/solve/:calculator', payment402Middleware, handleCalculatorRequest);

  return { app, mcpServer, transports };
}

/**
 * Starts the remote MCP server listening on specified port
 */
export function startRemoteMcpServer(port = Number(process.env.PORT ?? 3001)) {
  const { app } = createRemoteMcpApp();
  const server = app.listen(port, () => {
    console.log(`[OmniOperand MCP] Remote SSE Server listening on http://localhost:${port}`);
    console.log(`[OmniOperand MCP] SSE Endpoint: http://localhost:${port}/sse`);
    console.log(`[OmniOperand MCP] 402 Solver Gateway: http://localhost:${port}/api/v1/solve/:calculator`);
  });
  return server;
}

// Standalone execution check
if (process.argv[1] && (process.argv[1].endsWith('server.ts') || process.argv[1].endsWith('server.js'))) {
  startRemoteMcpServer();
}
