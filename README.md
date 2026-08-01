# MazzaGroup MCP Server

21 mazzagrp.com AI API endpoints exposed as MCP tools. Pay-per-request via x402 USDC micropayments on Base. No API keys.

## Quick start

```bash
pip install mazzagrp-mcp
```

### Claude Desktop / Cursor

```json
{
  "mcpServers": {
    "mazzagrp": {
      "command": "mazzagrp-mcp",
      "env": {
        "MAZZAGRP_WALLET_KEY": "<your-evm-private-key>"
      }
    }
  }
}
```

### Environment variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `MAZZAGRP_WALLET_KEY` | yes | — | EVM private key (hex, 0x-prefixed) for signing x402 payments |
| `MAZZAGRP_WALLET_PATH` | no | — | Path to wallet JSON file with `private_key` field (alternative to `MAZZAGRP_WALLET_KEY`) |
| `MAZZAGRP_BASE_URL` | no | `https://api.mazzagrp.com` | API base URL |

Fund your wallet address with USDC on Base before calling paid endpoints.

## Tools (21)

| Tool | Cost | Description |
|------|------|-------------|
| `demo` | $0.01 | Test endpoint |
| `scrape` | $0.05 | Scrape a URL |
| `gigs_search` | $0.15 | GigRadar freelance gig search |
| `lighthouse` | $0.12 | Lighthouse performance audit |
| `a11y_audit` | $0.08 | Accessibility audit |
| `crawl_judge` | $0.03 | Crawlability assessment |
| `doc_extract` | $0.25 | Document content extraction (PDF/URL) |
| `sentiment` | $0.10 | Sentiment analysis |
| `summarize` | $0.10 | Text summarization |
| `translate` | $0.12 | Text translation |
| `classify` | $0.08 | Text classification |
| `ner` | $0.10 | Named entity recognition |
| `embeddings` | $0.05 | Vector embeddings |
| `code_review` | $0.15 | AI code review |
| `sql_generate` | $0.12 | Text-to-SQL generation |
| `rag_query` | $0.20 | RAG with citations |
| `web_agent` | $0.50 | Browser automation agent |
| `sheets_automation` | $0.30 | Google Sheets automation |
| `roleplay` | $0.10 | Character engine roleplay |
| `negotiation` | $0.15 | Negotiation training |
| `knowledge_recall` | $0.25 | Zero-hallucination knowledge recall |

## How it works

1. Agent calls an MCP tool → server forwards request to `https://api.mazzagrp.com/v1/{endpoint}`
2. API returns HTTP 402 with x402 payment requirements
3. Server signs an EIP-3009 TransferWithAuthorization message with your wallet key
4. Server retries with the `X-PAYMENT` header containing the signed payment
5. API settles the USDC payment on Base and returns the result
6. Server returns the result to the agent

## License

MIT
