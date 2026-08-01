"""MCP server wrapping 21 mazzagrp.com AI API endpoints with x402 USDC payments."""

from __future__ import annotations

import asyncio
import json
import os
import sys
import typing as t

from mcp.server import MCPServer

sys.path.insert(0, "/root/mazzagrp-python")
from mazzagrp.client import MazzaClient  # noqa: E402

DEFAULT_WALLET_PATH = "/root/.openclaw/workspace/x402-cashclaw/wallet.json"

# 21 endpoints: (tool_name, price, description, client_method)
ENDPOINTS = [
    ("recall", "$0.20", "Memory recall and context retrieval", "recall"),
    ("rag", "$1.50", "Retrieval-augmented generation pipeline", "rag"),
    ("sql", "$1.20", "AI-powered SQL query generation and optimization", "sql"),
    ("negotiator", "$1.50", "AI negotiation assistant and strategy advisor", "negotiator"),
    ("design", "$0.80", "AI-assisted design recommendations and mockups", "design"),
    ("simulation", "$2.00", "AI scenario simulation and modeling", "simulation"),
    ("character", "$0.10", "AI character generation and development", "character"),
    ("puzzles", "$0.80", "AI puzzle generation and solving", "puzzles"),
    ("arena", "$1.20", "AI model comparison and benchmarking arena", "arena"),
    ("storyforge", "$0.60", "AI-powered creative story generation and worldbuilding", "storyforge"),
    ("autoflow", "$1.50", "AI-powered automated workflow orchestration", "autoflow"),
    ("worldbuilder", "$2.00", "AI worldbuilding for fiction, games, and RPGs", "worldbuilder"),
    ("longqa", "$1.00", "Long-form question answering with deep analysis", "longqa"),
    ("temporal", "$0.80", "Temporal workflow orchestration assistant", "temporal"),
    ("desktop", "$1.50", "Desktop application AI assistant", "desktop"),
    ("mcp_eval", "$2.00", "MCP (Model Context Protocol) evaluation and scoring", "mcp_eval"),
    ("sheets", "$1.00", "AI spreadsheet formula generation and data analysis", "sheets"),
    ("webagent", "$1.80", "AI web agent for autonomous browsing and task execution", "webagent"),
    ("consultation", "$5.00", "AI consultation with a senior strategist", "consultation"),
    ("chatbot", "$1.00", "Conversational AI chatbot interaction", "chatbot"),
    ("automation", "$15.00", "AI-powered workflow automation design and implementation", "automation"),
]


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
        base_url=os.environ.get("MAZZAGRP_BASE_URL", "https://mazzagrp.com"),
    )


def create_server() -> MCPServer:
    client = _create_client()
    server = MCPServer(
        name="mazzagrp",
        title="MazzaGroup AI APIs",
        description="21 AI API endpoints with x402 USDC micropayments on Base.",
        version="0.1.0",
    )

    for tool_name, price, desc, method_name in ENDPOINTS:
        client_method = getattr(client, method_name)

        def make_func(m):
            def tool_func(prompt: str) -> str:
                return json.dumps(m(prompt=prompt), default=str)
            return tool_func

        full_desc = f"{desc} ({price})"
        server.tool(name=tool_name, description=full_desc)(make_func(client_method))

    return server


def main():
    server = create_server()
    asyncio.run(server.run_stdio_async())


if __name__ == "__main__":
    main()
