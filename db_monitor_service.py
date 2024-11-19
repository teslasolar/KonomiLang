import time
import threading
from db_monitor import DatabaseMonitor

class MonitoringService:
    def __init__(self, interval=300):  # Default 5 minutes
        self.interval = interval
        self.monitor = DatabaseMonitor()
        self.running = False
        self.thread = None
        self.last_results = None
        
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
                self.last_results = self.monitor.monitor_databases()
                total_dbs = len(self.last_results)
                healthy_dbs = sum(1 for metrics in self.last_results.values() 
                                if metrics["connection_status"] and metrics["integrity_check"])
                
                print(f"\nMonitoring Update ({time.strftime('%Y-%m-%d %H:%M:%S')})")
                print(f"Healthy databases: {healthy_dbs}/{total_dbs}")
                
                # Sleep for the specified interval
                time.sleep(self.interval)
                
            except Exception as e:
                print(f"Error in monitoring loop: {str(e)}")
                time.sleep(60)  # Wait a minute before retrying on error
                
    def get_status(self):
        """Get the latest monitoring results."""
        return self.last_results

def main():
    service = MonitoringService(interval=300)  # 5 minutes interval
    try:
        service.start()
        # Keep the main thread running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        service.stop()

if __name__ == "__main__":
    main()
