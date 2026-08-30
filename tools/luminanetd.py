#!/usr/bin/env python3
"""LuminaNet loopback node v0.1

Bindet nur 127.0.0.1. Wendet scene.set im Speicher an. Keine Hardware,
keine öffentliche Schnittstelle, keine Secrets.
"""

from __future__ import annotations

import json
import sys
import threading
import time
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any
from urllib.parse import urlparse

HOST = "127.0.0.1"
PORT = 8787
PROTO = "0.1"
NODE_ID = "loopback-atelier"
ZONE = "atelier"

FALLBACK_SCENE: dict[str, Any] = {
    "scene_id": "fallback-warm",
    "priority": 0,
    "hold_s": 0,
    "channels": {
        "ambient": {
            "mode": "rgb",
            "rgb": [255, 196, 140],
            "nits": 8,
            "ease_ms": 1200,
        }
    },
    "rhythm": {"kind": "none"},
}

ALLOWED_TOPICS = {
    "scene.set",
    "scene.get",
    "scene.clear",
    "node.hello",
    "node.caps",
    "sense.sample",
    "mesh.ping",
    "mesh.partition",
    "agent.hello",
    "agent.ask",
    "agent.say",
    "agent.nack",
}

lock = threading.Lock()
state: dict[str, Any] = {
    "started": time.time(),
    "scene": dict(FALLBACK_SCENE),
    "source": "boot",
    "applied_at": time.time(),
    "hold_until": None,
    "partition": False,
    "last_id": None,
    "seen_ids": {},
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def expire_scene() -> None:
    hold = state.get("hold_until")
    if hold is not None and time.time() > hold:
        state["scene"] = dict(FALLBACK_SCENE)
        state["source"] = "hold-expired"
        state["hold_until"] = None
        state["applied_at"] = time.time()


def seen_recently(msg_id: str) -> bool:
    now = time.time()
    cutoff = now - 600
    stale = [k for k, ts in state["seen_ids"].items() if ts < cutoff]
    for k in stale:
        del state["seen_ids"][k]
    if msg_id in state["seen_ids"]:
        return True
    state["seen_ids"][msg_id] = now
    state["last_id"] = msg_id
    return False


def reply(req: dict, topic: str, body: dict, ok: bool = True) -> dict:
    return {
        "v": PROTO,
        "id": f"{req.get('id', 'anon')}-ack",
        "ts": utc_now(),
        "ttl_s": 15,
        "in_reply_to": req.get("id"),
        "from": {"class": "lumina", "id": NODE_ID, "zone": ZONE, "topic": topic},
        "to": req.get("from", {"class": "operator"}),
        "body": {"ok": ok, **body},
    }


def nack(req: dict, code: str, detail: str) -> dict:
    return reply(req, "agent.nack", {"code": code, "detail": detail}, ok=False)


def apply_scene(scene: dict, source: str) -> dict:
    hold_s = int(scene.get("hold_s") or 0)
    applied = {
        "scene_id": scene.get("scene_id", "unnamed"),
        "priority": int(scene.get("priority", 0)),
        "hold_s": hold_s,
        "channels": scene.get("channels") or FALLBACK_SCENE["channels"],
        "rhythm": scene.get("rhythm") or {"kind": "none"},
    }
    state["scene"] = applied
    state["source"] = source
    state["applied_at"] = time.time()
    state["hold_until"] = (time.time() + hold_s) if hold_s > 0 else None
    return applied


def handle_envelope(req: dict) -> tuple[int, dict]:
    if not isinstance(req, dict):
        return 400, nack({}, "ambiguous", "kein objekt")
    if req.get("v") != PROTO:
        return 400, nack(req, "unknown-intent", "v muss 0.1 sein")
    msg_id = req.get("id")
    if not isinstance(msg_id, str) or len(msg_id) < 8:
        return 400, nack(req, "ambiguous", "id fehlt")
    to = req.get("to") if isinstance(req.get("to"), dict) else {}
    topic = to.get("topic")
    if topic not in ALLOWED_TOPICS:
        return 400, nack(req, "unknown-intent", f"topic nicht erlaubt: {topic}")
    ttl = req.get("ttl_s", 30)
    if not isinstance(ttl, int) or ttl < 1 or ttl > 86400:
        return 400, nack(req, "unsafe", "ttl_s ungültig")
    if seen_recently(msg_id):
        return 200, reply(req, topic, {"duplicate": True, "scene": state["scene"]})

    expire_scene()
    body = req.get("body") if isinstance(req.get("body"), dict) else {}

    if topic == "mesh.partition":
        state["partition"] = bool(body.get("partition", True))
        if state["partition"]:
            apply_scene(FALLBACK_SCENE, "partition")
        return 200, reply(req, "mesh.partition", {"partition": state["partition"]})

    if topic == "mesh.ping":
        return 200, reply(
            req,
            "mesh.pong",
            {
                "uptime_s": int(time.time() - state["started"]),
                "partition_hint": state["partition"],
                "node_id": NODE_ID,
            },
        )

    if topic in {"node.hello", "node.caps"}:
        return 200, reply(
            req,
            "node.hello",
            {
                "node_id": NODE_ID,
                "class": "lumina",
                "zone": ZONE,
                "caps": sorted(ALLOWED_TOPICS),
                "gamut": "rgb",
                "limits": {"max_nits": 120, "blackout_ok": False},
                "partition": state["partition"],
            },
        )

    if topic == "sense.sample":
        return 200, reply(
            req,
            "sense.sample",
            {"lux": None, "occupied": "unknown", "temp": None},
        )

    if topic == "scene.get":
        return 200, reply(
            req,
            "scene.get",
            {
                "scene": state["scene"],
                "source": state["source"],
                "partition": state["partition"],
            },
        )

    if topic == "scene.clear":
        applied = apply_scene(FALLBACK_SCENE, "clear")
        return 200, reply(req, "scene.clear", {"scene": applied})

    if topic == "scene.set":
        if state["partition"]:
            return 409, nack(req, "partition", "kein scene.set während partition")
        priority = int(body.get("priority", 0))
        if priority > 4 or priority < 0:
            return 400, nack(req, "unsafe", "priority außerhalb 0-4")
        rhythm = body.get("rhythm") if isinstance(body.get("rhythm"), dict) else {}
        period = rhythm.get("period_ms")
        if period is not None and int(period) < 2000:
            return 400, nack(req, "unsafe", "kein strobe: period_ms < 2000")
        if "channels" not in body:
            return 400, nack(req, "ambiguous", "channels fehlen")
        current_p = int(state["scene"].get("priority", 0))
        if priority < current_p:
            return 409, nack(
                req,
                "unsafe",
                f"priority {priority} verliert gegen lokale {current_p}",
            )
        applied = apply_scene(body, str((req.get("from") or {}).get("role") or "envelope"))
        return 200, reply(req, "scene.set", {"scene": applied})

    if topic == "agent.hello":
        return 200, reply(
            req,
            "agent.hello",
            {
                "role": "lumia",
                "proto": PROTO,
                "caps": ["scene.compose", "scene.set", "scene.get"],
                "availability": "local-mesh",
            },
        )

    if topic == "agent.ask":
        intent = body.get("intent")
        if intent != "scene.compose":
            return 400, nack(req, "unknown-intent", str(intent))
        if state["partition"]:
            return 409, nack(req, "partition", "ask während partition lokal begrenzt")
        mood = str((body.get("input") or {}).get("mood") or "dawn")
        scene = {
            "scene_id": f"{mood}-soft",
            "priority": int((body.get("input") or {}).get("priority") or 1),
            "hold_s": 1800,
            "channels": {
                "ambient": {
                    "mode": "rgb",
                    "rgb": [255, 214, 170],
                    "nits": 28,
                    "ease_ms": 4000,
                }
            },
            "rhythm": {"kind": "breathe", "period_ms": 12000, "depth": 0.08},
        }
        applied = apply_scene(scene, "lumia-ask")
        return 200, reply(req, "agent.say", {"intent": intent, "result": {"scene": applied}})

    return 400, nack(req, "unknown-intent", topic)


class Handler(BaseHTTPRequestHandler):
    server_version = "LuminaNet/0.1"

    def log_message(self, fmt: str, *args: Any) -> None:
        sys.stdout.write(f"[{utc_now()}] {self.address_string()} {fmt % args}\n")
        sys.stdout.flush()

    def _send(self, code: int, payload: dict) -> None:
        raw = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self) -> None:
        path = urlparse(self.path).path
        with lock:
            expire_scene()
            if path in {"/", "/health"}:
                self._send(
                    200,
                    {
                        "ok": True,
                        "service": "luminanetd",
                        "v": PROTO,
                        "bind": f"{HOST}:{PORT}",
                        "node_id": NODE_ID,
                        "uptime_s": int(time.time() - state["started"]),
                        "partition": state["partition"],
                        "scene_id": state["scene"].get("scene_id"),
                    },
                )
                return
            if path in {"/scene", "/v0.1/scene"}:
                self._send(
                    200,
                    {
                        "scene": state["scene"],
                        "source": state["source"],
                        "partition": state["partition"],
                    },
                )
                return
        self._send(404, {"ok": False, "code": "unknown-intent", "detail": path})

    def do_POST(self) -> None:
        path = urlparse(self.path).path
        if path != "/v0.1/envelope":
            self._send(404, {"ok": False, "code": "unknown-intent", "detail": path})
            return
        length = int(self.headers.get("Content-Length") or 0)
        if length > 16 * 1024:
            self._send(413, {"ok": False, "code": "unsafe", "detail": "payload > 16KiB"})
            return
        raw = self.rfile.read(length) if length else b"{}"
        try:
            req = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            self._send(400, {"ok": False, "code": "ambiguous", "detail": "kein json"})
            return
        with lock:
            code, payload = handle_envelope(req)
        self._send(code, payload)


def main() -> int:
    httpd = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"LuminaNet loopback v{PROTO} auf http://{HOST}:{PORT}")
    print("  GET  /health")
    print("  GET  /v0.1/scene")
    print("  POST /v0.1/envelope")
    print("Nur lokal. Ctrl+C beendet.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nKnoten gehalten.")
        httpd.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
