from collections import Counter, deque
from datetime import datetime, timezone
from threading import Lock

class RuntimeMonitor:
    def __init__(self, max_events: int = 500) -> None:
        self._events = deque(maxlen=max_events)
        self._lock = Lock()

    def record(self, event_type: str, severity: str, tenant_id: str, detail: str) -> None:
        event = {"timestamp": datetime.now(timezone.utc).isoformat(),
                 "event_type": event_type, "severity": severity,
                 "tenant_id": tenant_id, "detail": detail[:240]}
        with self._lock:
            self._events.append(event)

    def snapshot(self) -> dict:
        with self._lock:
            events = list(self._events)
        counts = Counter(event["severity"] for event in events)
        return {"total_events": len(events), "by_severity": dict(counts),
                "events": list(reversed(events[-100:]))}
