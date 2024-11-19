"""
Monitoring service for continuous database monitoring.
"""
import time
import threading
from typing import Dict, Any, Optional
from .core import DatabaseMonitor
from . import utils

class MonitoringService:
    def __init__(self, interval: int = 300):  # Default 5 minutes
        self.interval = interval
        self.monitor = DatabaseMonitor()
        self.running = False
        self.thread = None
        self.last_results: Optional[Dict[str, Dict[str, Any]]] = None
        self._lock = threading.Lock()
        
    def start(self):
        """Start the monitoring service."""
        if self.running:
            return
            
        self.running = True
        self.thread = threading.Thread(target=self._monitoring_loop)
        self.thread.daemon = True
        self.thread.start()
        print("Monitoring service started.")
        
    def stop(self):
        """Stop the monitoring service."""
        self.running = False
        if self.thread:
            self.thread.join()
        print("Monitoring service stopped.")
        
    def _monitoring_loop(self):
        """Main monitoring loop."""
        while self.running:
            try:
                with self._lock:
                    self.last_results = self.monitor.monitor_databases()
                
                # Generate status summary
                status = utils.aggregate_status(self.last_results)
                print(f"\nMonitoring Update ({status['timestamp']})")
                print(f"Healthy databases: {status['healthy_databases']}/{status['total_databases']}")
                
                # Check for issues and generate alerts
                self._check_for_alerts()
                
                # Sleep for the specified interval
                time.sleep(self.interval)
                
            except Exception as e:
                print(f"Error in monitoring loop: {str(e)}")
                time.sleep(60)  # Wait a minute before retrying on error
                
    def _check_for_alerts(self):
        """Check monitoring results for issues and generate alerts."""
        if not self.last_results:
            return
            
        for position, metrics in self.last_results.items():
            health_status = utils.check_database_health(metrics)
            
            # Generate alerts for issues
            for issue in health_status["issues"]:
                alert = utils.generate_alert(issue, "error", position)
                print(f"ALERT: {alert['severity'].upper()} - {alert['database']}: {alert['issue']}")
            
            # Generate alerts for warnings
            for warning in health_status["warnings"]:
                alert = utils.generate_alert(warning, "warning", position)
                print(f"ALERT: {alert['severity'].upper()} - {alert['database']}: {alert['issue']}")
    
    def get_status(self) -> Optional[Dict[str, Dict[str, Any]]]:
        """Get the latest monitoring results."""
        with self._lock:
            return self.last_results if self.last_results else None
            
    def trigger_check(self) -> Dict[str, Any]:
        """Manually trigger a monitoring check."""
        with self._lock:
            self.last_results = self.monitor.monitor_databases()
            return utils.aggregate_status(self.last_results)
