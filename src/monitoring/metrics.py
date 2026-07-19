from typing import Dict, Any
import time

class MetricsCollector:
    """Collects and provides performance metrics."""
    def __init__(self):
        self.queries_processed = 0
        self.fallbacks_triggered = 0
        self.total_processing_time = 0.0

    def record_query(self, processing_time: float, fallback: bool):
        self.queries_processed += 1
        self.total_processing_time += processing_time
        if fallback:
            self.fallbacks_triggered += 1

    def get_metrics(self) -> Dict[str, Any]:
        avg_time = self.total_processing_time / self.queries_processed if self.queries_processed > 0 else 0
        return {
            "queries_processed": self.queries_processed,
            "fallbacks_triggered": self.fallbacks_triggered,
            "average_processing_time_s": round(avg_time, 4)
        }

metrics_collector = MetricsCollector()
