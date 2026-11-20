"""Send synthetic EKS signals to the loopback-only AI SOC lab."""
import argparse
import json
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from adapter import normalize_batch

HERE = Path(__file__).resolve().parent


def load_events(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def ensure_loopback(url):
    parsed = urlparse(url)
    if parsed.scheme != "http" or parsed.hostname not in {"127.0.0.1", "localhost"}:
        raise ValueError("For safety, the simulator can send only to an HTTP localhost/127.0.0.1 URL")
    if parsed.path != "/api/events":
        raise ValueError("Target path must be /api/events")
    return url


def send_events(events, url):
    ensure_loopback(url)
    body = json.dumps(events).encode("utf-8")
    request = Request(url, data=body, headers={"Content-Type": "application/json"}, method="POST")
    with urlopen(request, timeout=5) as response:
        return json.loads(response.read().decode("utf-8"))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", default=str(HERE / "scenarios" / "eks-events.json"))
    parser.add_argument("--batch-id", default="eks-demo-001")
    parser.add_argument("--url", default="http://127.0.0.1:8765/api/events")
    parser.add_argument("--dry-run", action="store_true", help="Print normalized events without sending")
    args = parser.parse_args()
    events = normalize_batch(load_events(args.input), args.batch_id)
    if args.dry_run:
        print(json.dumps(events, indent=2))
        print(f"\nDry run: {len(events)} normalized synthetic events; nothing sent.")
        return
    result = send_events(events, args.url)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
