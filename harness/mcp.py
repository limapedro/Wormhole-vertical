# Minimal stdio JSON-RPC client for the external OBS-MCP server.
# Copyright (C) 2026 Wormhole-vertical contributors
# SPDX-License-Identifier: GPL-2.0-or-later
from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


class ObsMcp:
    def __init__(self, exe: Path, config: Path, root: Path):
        cfg = config if config.is_absolute() else root / config
        self._proc = subprocess.Popen(
            [str(exe), "--config", str(cfg)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            bufsize=1,
        )
        self._id = 0
        self.call_raw("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "wormhole-vertical-harness", "version": "1"},
        })

    def call_raw(self, method: str, params: dict[str, Any]) -> dict[str, Any]:
        self._id += 1
        request = {"jsonrpc": "2.0", "id": self._id, "method": method, "params": params}
        assert self._proc.stdin is not None and self._proc.stdout is not None
        self._proc.stdin.write(json.dumps(request) + "\n")
        self._proc.stdin.flush()
        while True:
            line = self._proc.stdout.readline()
            if not line:
                raise RuntimeError("OBS-MCP closed stdout")
            response = json.loads(line)
            if response.get("id") == self._id:
                return response

    def tool(self, name: str, arguments: dict[str, Any]) -> str:
        response = self.call_raw("tools/call", {"name": name, "arguments": arguments})
        if "error" in response:
            raise RuntimeError(f"OBS-MCP tool {name} failed: {response['error']}")
        content = response["result"]["content"]
        return content[0]["text"] if content else ""

    def ws(self, instance: str, request_type: str, request_id: int,
           request_data: dict[str, Any] | None = None) -> dict[str, Any]:
        payload = json.dumps({
            "op": 6,
            "d": {
                "requestType": request_type,
                "requestId": request_id,
                **({"requestData": request_data} if request_data else {}),
            },
        })
        text = self.tool("obs_ws_call", {"name": instance, "request": payload})
        outer = json.loads(text)
        status = outer["d"]["requestStatus"]
        if not status["result"]:
            raise RuntimeError(f"OBS WS {request_type} failed: {status}")
        return outer["d"].get("responseData", {})

    def close(self) -> None:
        if self._proc.stdin:
            self._proc.stdin.close()
        try:
            self._proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self._proc.terminate()
