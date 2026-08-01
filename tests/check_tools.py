#!/usr/bin/env python3
"""Self-check: verify 21 tools registered with correct schemas."""
import asyncio
from mazzagrp_mcp.server import create_server, ENDPOINTS

async def main():
    server = create_server()
    tools = await server.list_tools()
    assert len(tools) == 21, f"expected 21 tools, got {len(tools)}"
    names = {t.name for t in tools}
    expected = {e[0] for e in ENDPOINTS}
    assert names == expected, f"mismatch: {names ^ expected}"
    # demo and crawl_judge have no required params (only optional `options`)
    demo = next(t for t in tools if t.name == "demo")
    assert "options" in demo.input_schema.get("properties", {})
    # translate requires text + target_lang
    translate = next(t for t in tools if t.name == "translate")
    assert set(translate.input_schema.get("required", [])) == {"text", "target_lang"}
    print(f"OK — {len(tools)} tools registered, schemas valid")

asyncio.run(main())
