"""MCP server wrapping 21 mazzagrp.com AI API endpoints with x402 USDC payments."""

from __future__ import annotations

import asyncio
import json
import os
import sys
import typing as t

from mcp.server import MCPServer

# Reuse the existing SDK — don't rewrite the x402 payment logic.
sys.path.insert(0, "/root/mazzagrp-python")
from mazzagrp.client import MazzaClient  # noqa: E402

DEFAULT_WALLET_PATH = "/root/.openclaw/workspace/x402-cashclaw/wallet.json"


def _load_private_key() -> str:
    key = os.environ.get("MAZZAGRP_WALLET_KEY")
    if key:
        return key
    path = os.environ.get("MAZZAGRP_WALLET_PATH", DEFAULT_WALLET_PATH)
    with open(path) as f:
        return json.load(f)["private_key"]


def _create_client() -> MazzaClient:
    return MazzaClient(
        private_key=_load_private_key(),
        base_url=os.environ.get("MAZZAGRP_BASE_URL", "https://api.mazzagrp.com"),
    )


# 21 endpoint specs: (method_name, cost, description, required_params, client_method)
# required_params: list of (name, type) — the rest are passed as **kwargs
ENDPOINTS: list[tuple[str, str, str, list[tuple[str, type]], str]] = [
    ("demo", "$0.01", "Test endpoint — verify connectivity and payment flow.", [], "demo"),
    ("scrape", "$0.05", "Scrape content from a URL.", [("url", str)], "scrape"),
    ("gigs_search", "$0.15", "GigRadar: search freelance gigs across platforms.", [("query", str)], "gigs_search"),
    ("lighthouse", "$0.12", "Run a Lighthouse performance audit on a URL.", [("url", str)], "lighthouse"),
    ("a11y_audit", "$0.08", "Run an accessibility audit on a URL.", [("url", str)], "a11y_audit"),
    ("crawl_judge", "$0.03", "Assess crawlability of a URL (robots, sitemaps, meta tags).", [("url", str)], "crawl_judge"),
    ("doc_extract", "$0.25", "Extract content from a document (PDF URL or text).", [("document", str)], "doc_extract"),
    ("sentiment", "$0.10", "Analyze sentiment of text (positive/negative/neutral + score).", [("text", str)], "sentiment"),
    ("summarize", "$0.10", "Summarize text into a concise summary.", [("text", str)], "summarize"),
    ("translate", "$0.12", "Translate text to a target language.", [("text", str), ("target_lang", str)], "translate"),
    ("classify", "$0.08", "Classify text into categories.", [("text", str)], "classify"),
    ("ner", "$0.10", "Named Entity Recognition — extract entities from text.", [("text", str)], "ner"),
    ("embeddings", "$0.05", "Generate vector embeddings for text.", [("text", str)], "embeddings"),
    ("code_review", "$0.15", "AI-powered code review.", [("code", str)], "code_review"),
    ("sql_generate", "$0.12", "Generate SQL from natural language query.", [("query", str)], "sql_generate"),
    ("rag_query", "$0.20", "RAG query with citations.", [("question", str)], "rag_query"),
    ("web_agent", "$0.50", "Browser automation agent — executes a web task.", [("task", str)], "web_agent"),
    ("sheets_automation", "$0.30", "Google Sheets automation — execute a sheets task.", [("task", str)], "sheets_automation"),
    ("roleplay", "$0.10", "Character engine roleplay — interact with a character.", [("character", str), ("message", str)], "roleplay"),
    ("negotiation", "$0.15", "Negotiation training — practice negotiation scenarios.", [("scenario", str)], "negotiation"),
    ("knowledge_recall", "$0.25", "Zero-hallucination knowledge recall — factual Q&A.", [("question", str)], "knowledge_recall"),
]


def _build_tool_func(client: MazzaClient, method_name: str, required_params: list[tuple[str, type]]):
    """Build a tool function that calls the corresponding MazzaClient method.

    Required params become explicit typed parameters; optional params go through an `options` dict.
    """
    client_method = getattr(client, method_name)

    # Build the function with explicit params — MCP uses annotations for the JSON schema.
    param_names = [name for name, _ in required_params]
    param_decls = ", ".join([f"{name}: {typ.__name__}" for name, typ in required_params])
    if param_decls:
        param_decls += ", options: dict | None = None"
    else:
        param_decls = "options: dict | None = None"

    code = f"def tool_func({param_decls}) -> str:\n"
    code += f"    _kwargs = {{}}\n"
    code += f"    for p in {param_names!r}:\n"
    code += f"        _kwargs[p] = locals()[p]\n"
    code += f"    if options:\n"
    code += f"        _kwargs.update({{k: v for k, v in options.items() if v is not None}})\n"
    code += f"    return json.dumps(client_method(**_kwargs), default=str)\n"

    ns: dict[str, t.Any] = {"client_method": client_method, "json": json}
    exec(code, ns)
    return ns["tool_func"]


def create_server() -> MCPServer:
    client = _create_client()
    server = MCPServer(
        name="mazzagrp",
        title="MazzaGroup AI APIs",
        description="21 AI API endpoints with x402 USDC micropayments on Base.",
        version="0.1.0",
    )

    for method_name, cost, desc, required_params, _ in ENDPOINTS:
        tool_func = _build_tool_func(client, method_name, required_params)
        full_desc = f"{desc} ({cost})"
        server.tool(name=method_name, description=full_desc)(tool_func)

    return server


def main():
    server = create_server()
    asyncio.run(server.run_stdio_async())


if __name__ == "__main__":
    main()
