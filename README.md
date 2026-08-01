# mazzagrp-mcp

[![MCP](https://img.shields.io/badge/MCP-Server-blue)](https://modelcontextprotocol.io)
[![x402](https://img.shields.io/badge/x402-Payments-purple)](https://x402.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue)](https://www.python.org)

MCP server wrapping 21 [mazzagrp.com](https://mazzagrp.com) AI API endpoints with x402 USDC micropayments on Base. Agents pay per call with crypto — no API keys, no signup.

## Install

```bash
pip install mazzagrp-mcp
```

## Configure

Add to your MCP client config (Claude Desktop, etc.):

```json
{
  "mcpServers": {
    "mazzagrp": {
      "command": "mazzagrp-mcp",
      "env": {
        "MAZZAGRP_WALLET_KEY": "0xYOUR_PRIVATE_KEY"
      }
    }
  }
}
```

Or use a wallet file:

```json
{
  "mcpServers": {
    "mazzagrp": {
      "command": "mazzagrp-mcp",
      "env": {
        "MAZZAGRP_WALLET_PATH": "/path/to/wallet.json"
      }
    }
  }
}
```

Wallet JSON format: `{"private_key": "0x...", "address": "0x..."}`

## 21 Tools

| Tool | Price | Description |
|------|-------|-------------|
| `recall` | $0.20 | Memory recall and context retrieval |
| `rag` | $1.50 | Retrieval-augmented generation pipeline |
| `sql` | $1.20 | AI-powered SQL query generation |
| `negotiator` | $1.50 | AI negotiation assistant |
| `design` | $0.80 | AI-assisted design recommendations |
| `simulation` | $2.00 | AI scenario simulation and modeling |
| `character` | $0.10 | AI character generation |
| `puzzles` | $0.80 | AI puzzle generation and solving |
| `arena` | $1.20 | AI model comparison and benchmarking |
| `storyforge` | $0.60 | AI creative story generation |
| `autoflow` | $1.50 | AI workflow orchestration |
| `worldbuilder` | $2.00 | AI worldbuilding for games and RPGs |
| `longqa` | $1.00 | Long-form question answering |
| `temporal` | $0.80 | Temporal workflow orchestration |
| `desktop` | $1.50 | Desktop application AI assistant |
| `mcp_eval` | $2.00 | MCP evaluation and scoring |
| `sheets` | $1.00 | AI spreadsheet automation |
| `webagent` | $1.80 | AI web agent for browsing |
| `consultation` | $5.00 | AI consultation with senior strategist |
| `chatbot` | $1.00 | Conversational AI chatbot |
| `automation` | $15.00 | AI workflow automation design |

## How it works

1. Agent calls an MCP tool (e.g., `recall`)
2. MCP server POSTs to `mazzagrp.com/api/recall`
3. Server returns HTTP 402 with x402 payment requirements
4. MCP server signs EIP-712 payment with your wallet
5. Retries with `PAYMENT-SIGNATURE` header
6. Returns AI response to the agent

## Payment

- **Protocol:** x402 v2
- **Network:** Base Sepolia (testnet)
- **Asset:** USDC
- **Facilitator:** x402.org/facilitator

Fund your wallet with USDC on Base Sepolia and the MCP server handles the rest.

## License

MIT
