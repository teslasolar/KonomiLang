"""
Utility functions for the database monitoring system.
"""
import json
from datetime import datetime
from typing import Dict, List, Any, Optional

def format_size(size_bytes: int) -> str:
    """Format byte size to human readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} TB"

def format_metrics(metrics: Dict[str, Any]) -> Dict[str, Any]:
    """Format raw metrics into human-readable format."""
    formatted = metrics.copy()
    if "size_bytes" in formatted:
        formatted["size_formatted"] = format_size(formatted["size_bytes"])
    if "timestamp" in formatted:
        formatted["timestamp_formatted"] = datetime.fromisoformat(formatted["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")
    return formatted

def aggregate_status(results: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    """Aggregate monitoring results into overall status."""
    total_dbs = len(results)
    healthy_dbs = sum(1 for metrics in results.values() 
                     if metrics["connection_status"] and metrics["integrity_check"])
    total_size = sum(metrics["size_bytes"] for metrics in results.values())
    
    return {
        "total_databases": total_dbs,
        "healthy_databases": healthy_dbs,
        "health_percentage": (healthy_dbs / total_dbs * 100) if total_dbs > 0 else 0,
        "total_size_bytes": total_size,
        "total_size_formatted": format_size(total_size),
        "timestamp": datetime.now().isoformat(),
    }

def check_database_health(metrics: Dict[str, Any]) -> Dict[str, Any]:
    """Evaluate database health based on metrics."""
    health_status = {
        "is_healthy": False,
        "issues": [],
        "warnings": [],
    }
    
    # Check connection
    if not metrics["connection_status"]:
        health_status["issues"].append("Database connection failed")
    
    # Check integrity
    if not metrics["integrity_check"]:
        health_status["issues"].append("Database integrity check failed")
    
    # Check size (warn if over 1GB)
    if metrics["size_bytes"] > 1_000_000_000:
        health_status["warnings"].append("Database size exceeds 1GB")
    
    # Set overall health status
    health_status["is_healthy"] = len(health_status["issues"]) == 0
    
    return health_status

def generate_alert(issue: str, severity: str, db_position: str) -> Dict[str, Any]:
    """Generate a standardized alert object."""
    return {
        "timestamp": datetime.now().isoformat(),
        "severity": severity,
        "database": db_position,
        "issue": issue,
        "alert_id": f"{db_position}_{int(datetime.now().timestamp())}"
    }
