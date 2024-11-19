"""
Flask API endpoints for the database monitoring system.
"""
from flask import Blueprint, jsonify
from . import utils
from .service import MonitoringService

# Create Blueprint for monitoring API
monitor_api = Blueprint('monitor_api', __name__, url_prefix='/api/v1/monitor')

# Initialize monitoring service
monitoring_service = MonitoringService(interval=300)
monitoring_service.start()

@monitor_api.route('/status', methods=['GET'])
def get_status():
    """Get overall grid status."""
    results = monitoring_service.get_status()
    if not results:
        return jsonify({"error": "No monitoring data available"}), 404
        
    status = utils.aggregate_status(results)
    return jsonify(status)

@monitor_api.route('/database/<position>', methods=['GET'])
def get_database_status(position):
    """Get status for a specific database."""
    results = monitoring_service.get_status()
    if not results:
        return jsonify({"error": "No monitoring data available"}), 404
        
    if position not in results:
        return jsonify({"error": f"Database {position} not found"}), 404
        
    metrics = results[position]
    formatted_metrics = utils.format_metrics(metrics)
    health_status = utils.check_database_health(metrics)
    
    response = {
        "position": position,
        "metrics": formatted_metrics,
        "health_status": health_status
    }
    
    return jsonify(response)

@monitor_api.route('/metrics', methods=['GET'])
def get_metrics():
    """Get performance metrics for all databases."""
    results = monitoring_service.get_status()
    if not results:
        return jsonify({"error": "No monitoring data available"}), 404
        
    metrics = {}
    for position, data in results.items():
        metrics[position] = {
            "query_performance": data.get("query_performance", {}),
            "error_stats": data.get("error_stats", {}),
            "connection_pool": data.get("connection_pool", {}),
            "size_bytes": data.get("size_bytes", 0),
            "size_formatted": utils.format_size(data.get("size_bytes", 0))
        }
        
    return jsonify(metrics)

@monitor_api.route('/check', methods=['POST'])
def trigger_check():
    """Manually trigger a monitoring check."""
    status = monitoring_service.trigger_check()
    return jsonify(status)
