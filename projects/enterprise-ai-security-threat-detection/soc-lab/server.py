"""Loopback-only HTTP API for the synthetic AI security SOC lab."""
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Lock

from soc_core import ingest, update_incident

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
STATE_PATH = HERE / "state.json"
RULES_PATH = PROJECT / "config" / "detection-rules.json"
MAX_BODY = 1_000_000
LOCK = Lock()


def load_state():
    if STATE_PATH.exists():
        return json.loads(STATE_PATH.read_text(encoding="utf-8"))
    return {"events": [], "incidents": [], "audit": []}


def save_state(state):
    temporary = STATE_PATH.with_suffix(".tmp")
    temporary.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    temporary.replace(STATE_PATH)


def load_rules():
    return json.loads(RULES_PATH.read_text(encoding="utf-8"))


class Handler(BaseHTTPRequestHandler):
    server_version = "AISOC-Lab/1.0"

    def log_message(self, fmt, *args):
        print("SOC-LAB", self.address_string(), fmt % args)

    def _send(self, status, payload):
        body = json.dumps(payload, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _body(self):
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            raise ValueError("Invalid Content-Length")
        if length < 1 or length > MAX_BODY:
            raise ValueError("Request body must be between 1 byte and 1 MB")
        raw = self.rfile.read(length)
        try:
            return json.loads(raw)
        except (UnicodeDecodeError, json.JSONDecodeError):
            raise ValueError("Request body must be valid JSON")

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            body = (HERE / "index.html").read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)
        elif self.path == "/api/state":
            with LOCK:
                self._send(200, load_state())
        elif self.path == "/api/playbooks":
            self._send(200, json.loads((HERE / "playbooks.json").read_text(encoding="utf-8")))
        elif self.path == "/api/health":
            self._send(200, {"status": "ok", "mode": "synthetic-local-only"})
        else:
            self._send(404, {"error": "Not found"})

    def do_POST(self):
        if self.path not in ("/api/events", "/api/demo-ingest"):
            self._send(404, {"error": "Not found"})
            return
        try:
            if self.path == "/api/demo-ingest":
                events = json.loads((PROJECT / "scenarios" / "sample-events.json").read_text(encoding="utf-8"))
            else:
                payload = self._body()
                events = payload if isinstance(payload, list) else [payload]
            with LOCK:
                state = load_state()
                result = ingest(state, events, load_rules())
                save_state(state)
            self._send(201, result)
        except (ValueError, KeyError) as error:
            self._send(400, {"error": str(error)})

    def do_PATCH(self):
        prefix = "/api/incidents/"
        if not self.path.startswith(prefix):
            self._send(404, {"error": "Not found"})
            return
        incident_id = self.path[len(prefix):]
        if not incident_id or "/" in incident_id:
            self._send(404, {"error": "Not found"})
            return
        try:
            payload = self._body()
            actor = payload.pop("actor", "soc-analyst")
            with LOCK:
                state = load_state()
                incident = update_incident(state, incident_id, payload, actor=actor)
                save_state(state)
            self._send(200, incident)
        except KeyError as error:
            self._send(404, {"error": str(error)})
        except ValueError as error:
            self._send(400, {"error": str(error)})


def main():
    # Bind only to loopback: this demo is intentionally not network-exposed.
    server = ThreadingHTTPServer(("127.0.0.1", 8765), Handler)
    print("Synthetic AI SOC lab: http://127.0.0.1:8765")
    print("API: GET /api/state, POST /api/events, PATCH /api/incidents/{incident_id}")
    print("Stop with Ctrl+C. Local JSON state is stored in soc-lab/state.json.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping SOC lab.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
