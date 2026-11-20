import unittest
from app.runtime import RuntimeMonitor

class RuntimeMonitorTests(unittest.TestCase):
    def test_records_and_summarizes_events(self):
        monitor = RuntimeMonitor(max_events=2)
        monitor.record("request", "info", "tenant-a", "test")
        monitor.record("injection", "high", "tenant-a", "blocked")
        snapshot = monitor.snapshot()
        self.assertEqual(snapshot["total_events"], 2)
        self.assertEqual(snapshot["by_severity"]["high"], 1)

    def test_event_buffer_is_bounded(self):
        monitor = RuntimeMonitor(max_events=2)
        for index in range(3):
            monitor.record("request", "info", "tenant-a", str(index))
        self.assertEqual(monitor.snapshot()["total_events"], 2)

if __name__ == "__main__":
    unittest.main()
