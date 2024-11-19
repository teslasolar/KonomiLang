"""
Flask API endpoints for the database monitoring system.
"""
from flask import Blueprint, jsonify, request
from . import utils
from .service import MonitoringService
from database.backup_manager import BackupManager

# Create Blueprint for monitoring API
monitor_api = Blueprint('monitor_api', __name__, url_prefix='/api/v1/monitor')

# Initialize services
monitoring_service = MonitoringService(interval=300)
backup_manager = BackupManager()
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

@monitor_api.route('/backups', methods=['GET'])
def list_backups():
    """List all available backups."""
    backups = backup_manager.list_backups()
    return jsonify({"backups": backups})

@monitor_api.route('/backups', methods=['POST'])
def create_backup():
    """Create a new backup."""
    data = request.get_json()
    databases = data.get('databases') if data else None
    
    try:
        backup_path = backup_manager.create_backup(databases)
        return jsonify({
            "message": "Backup created successfully",
            "backup_path": backup_path
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@monitor_api.route('/backups/restore', methods=['POST'])
def restore_backup():
    """Restore from a backup."""
    data = request.get_json()
    if not data or 'backup_path' not in data:
        return jsonify({"error": "backup_path is required"}), 400
        
    try:
        restored = backup_manager.restore_backup(
            data['backup_path'],
            data.get('databases')
        )
        return jsonify({
            "message": "Backup restored successfully",
            "restored_databases": restored
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
