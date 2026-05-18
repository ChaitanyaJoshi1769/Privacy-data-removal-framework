#!/usr/bin/env python3
"""
Privacy Framework Web Dashboard
Real-time visualization of monitoring and removal progress
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any


class DashboardServer:
    """Generates dashboard HTML with real-time data"""

    def __init__(self, data_dir: str = "logs"):
        """
        Initialize dashboard server

        Args:
            data_dir: Directory containing JSON data files
        """
        self.data_dir = Path(data_dir)
        self.data = {}
        self.load_all_data()

    def load_all_data(self) -> None:
        """Load all JSON data files from logs directory"""
        if not self.data_dir.exists():
            self.data_dir.mkdir(parents=True, exist_ok=True)
            return

        # Load broker tracking
        broker_file = self.data_dir / "broker_tracking.json"
        if broker_file.exists():
            try:
                with open(broker_file) as f:
                    self.data["brokers"] = json.load(f)
            except:
                self.data["brokers"] = {}

        # Load HIBP data
        hibp_file = self.data_dir / "hibp_breaches.json"
        if hibp_file.exists():
            try:
                with open(hibp_file) as f:
                    self.data["hibp"] = json.load(f)
            except:
                self.data["hibp"] = []

        # Load monitoring report
        monitoring_file = self.data_dir / "monitoring_report.json"
        if monitoring_file.exists():
            try:
                with open(monitoring_file) as f:
                    self.data["monitoring"] = json.load(f)
            except:
                self.data["monitoring"] = {}

    def calculate_broker_stats(self) -> Dict:
        """Calculate broker removal statistics"""
        brokers = self.data.get("brokers", {})
        if not brokers:
            return {
                "total": 0,
                "submitted": 0,
                "verified": 0,
                "pending": 0,
                "failed": 0,
                "completion_percent": 0
            }

        total = len(brokers)
        submitted = sum(1 for b in brokers.values() if b.get("submission_date"))
        verified = sum(1 for b in brokers.values() if b.get("verified_removed"))
        pending = sum(1 for b in brokers.values() if b.get("status") == "removal_pending")
        failed = sum(1 for b in brokers.values() if b.get("status") == "removal_failed")

        return {
            "total": total,
            "submitted": submitted,
            "verified": verified,
            "pending": pending,
            "failed": failed,
            "completion_percent": round((verified / total * 100) if total > 0 else 0, 1)
        }

    def calculate_breach_stats(self) -> Dict:
        """Calculate breach monitoring statistics"""
        hibp = self.data.get("hibp", [])
        if not hibp:
            return {
                "total_checks": 0,
                "breached": 0,
                "safe": 0,
                "risk_level": "UNKNOWN"
            }

        total = len(hibp)
        breached = sum(1 for h in hibp if h.get("breached"))
        safe = total - breached

        risk = "GREEN"
        if breached > 3:
            risk = "RED"
        elif breached > 0:
            risk = "YELLOW"

        return {
            "total_checks": total,
            "breached": breached,
            "safe": safe,
            "risk_level": risk
        }

    def get_broker_list(self) -> List[Dict]:
        """Get detailed broker list with status"""
        brokers = self.data.get("brokers", {})
        broker_list = []

        for broker_id, data in brokers.items():
            broker_list.append({
                "id": broker_id,
                "name": data.get("broker_info", {}).get("name", broker_id),
                "status": data.get("status", "unknown"),
                "submitted": bool(data.get("submission_date")),
                "verified": data.get("verified_removed", False),
                "submitted_date": data.get("submission_date"),
                "verification_date": data.get("verification_date"),
                "confirmation_num": data.get("confirmation_number")
            })

        return sorted(broker_list, key=lambda x: (x["status"], x["name"]))

    def generate_html(self) -> str:
        """Generate dashboard HTML"""
        broker_stats = self.calculate_broker_stats()
        breach_stats = self.calculate_breach_stats()
        broker_list = self.get_broker_list()

        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Privacy Framework Dashboard</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}

        header {{
            background: white;
            padding: 30px;
            border-radius: 8px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}

        h1 {{
            color: #333;
            margin-bottom: 10px;
            font-size: 28px;
        }}

        .timestamp {{
            color: #666;
            font-size: 14px;
        }}

        .dashboard {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}

        .card {{
            background: white;
            padding: 25px;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}

        .card h2 {{
            color: #333;
            font-size: 18px;
            margin-bottom: 20px;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }}

        .stat {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 1px solid #eee;
        }}

        .stat:last-child {{
            border-bottom: none;
            margin-bottom: 0;
        }}

        .stat-label {{
            color: #666;
            font-weight: 500;
        }}

        .stat-value {{
            color: #333;
            font-size: 24px;
            font-weight: bold;
        }}

        .progress {{
            width: 100%;
            height: 30px;
            background: #eee;
            border-radius: 15px;
            overflow: hidden;
            margin-top: 15px;
        }}

        .progress-bar {{
            height: 100%;
            background: linear-gradient(90deg, #667eea, #764ba2);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 12px;
            font-weight: bold;
        }}

        .status-badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
        }}

        .status-green {{
            background: #d4edda;
            color: #155724;
        }}

        .status-yellow {{
            background: #fff3cd;
            color: #856404;
        }}

        .status-red {{
            background: #f8d7da;
            color: #721c24;
        }}

        .broker-list {{
            background: white;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }}

        .broker-list h2 {{
            padding: 25px;
            border-bottom: 2px solid #667eea;
            color: #333;
            font-size: 18px;
            margin: 0;
        }}

        .broker-item {{
            display: grid;
            grid-template-columns: 2fr 1fr 1fr 1fr 1fr;
            align-items: center;
            padding: 15px 25px;
            border-bottom: 1px solid #eee;
        }}

        .broker-item:last-child {{
            border-bottom: none;
        }}

        .broker-item:nth-child(even) {{
            background: #f8f9fa;
        }}

        .broker-name {{
            color: #333;
            font-weight: 500;
        }}

        .broker-status {{
            text-align: center;
        }}

        .broker-submitted {{
            text-align: center;
        }}

        .broker-verified {{
            text-align: center;
        }}

        .broker-date {{
            text-align: center;
            font-size: 12px;
            color: #666;
        }}

        .checkmark {{
            color: #28a745;
            font-weight: bold;
            font-size: 16px;
        }}

        .x-mark {{
            color: #dc3545;
            font-weight: bold;
            font-size: 16px;
        }}

        .footer {{
            text-align: center;
            color: white;
            font-size: 12px;
            margin-top: 30px;
        }}

        .alert {{
            padding: 15px 20px;
            border-radius: 8px;
            margin-bottom: 20px;
        }}

        .alert-info {{
            background: #d1ecf1;
            color: #0c5460;
            border-left: 4px solid #17a2b8;
        }}

        .alert-warning {{
            background: #fff3cd;
            color: #856404;
            border-left: 4px solid #ffc107;
        }}

        .alert-danger {{
            background: #f8d7da;
            color: #721c24;
            border-left: 4px solid #dc3545;
        }}

        @media (max-width: 768px) {{
            .dashboard {{
                grid-template-columns: 1fr;
            }}

            .broker-item {{
                grid-template-columns: 1fr;
                gap: 10px;
            }}

            .broker-item > * {{
                padding: 5px 0;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🔐 Privacy Framework Dashboard</h1>
            <div class="timestamp">Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}</div>
        </header>

        <div class="dashboard">
            <!-- Broker Removal Progress -->
            <div class="card">
                <h2>📋 Data Broker Removal</h2>
                <div class="stat">
                    <span class="stat-label">Total Brokers</span>
                    <span class="stat-value">{broker_stats['total']}</span>
                </div>
                <div class="stat">
                    <span class="stat-label">Submitted</span>
                    <span class="stat-value">{broker_stats['submitted']}</span>
                </div>
                <div class="stat">
                    <span class="stat-label">Verified Removed</span>
                    <span class="stat-value">{broker_stats['verified']}</span>
                </div>
                <div class="stat">
                    <span class="stat-label">Pending</span>
                    <span class="stat-value">{broker_stats['pending']}</span>
                </div>
                <div class="progress">
                    <div class="progress-bar" style="width: {broker_stats['completion_percent']}%">
                        {broker_stats['completion_percent']}%
                    </div>
                </div>
            </div>

            <!-- Breach Monitoring -->
            <div class="card">
                <h2>🔍 Breach Monitoring (HIBP)</h2>
                <div class="stat">
                    <span class="stat-label">Total Checks</span>
                    <span class="stat-value">{breach_stats['total_checks']}</span>
                </div>
                <div class="stat">
                    <span class="stat-label">Breached</span>
                    <span class="stat-value">{breach_stats['breached']}</span>
                </div>
                <div class="stat">
                    <span class="stat-label">Safe</span>
                    <span class="stat-value">{breach_stats['safe']}</span>
                </div>
                <div class="stat">
                    <span class="stat-label">Risk Level</span>
                    <span class="status-badge status-{'green' if breach_stats['risk_level'] == 'GREEN' else 'yellow' if breach_stats['risk_level'] == 'YELLOW' else 'red'}">
                        {breach_stats['risk_level']}
                    </span>
                </div>
            </div>

            <!-- Monitoring Status -->
            <div class="card">
                <h2>📊 Monitoring Status</h2>
                <div class="stat">
                    <span class="stat-label">Daily Jobs</span>
                    <span class="stat-value">3</span>
                </div>
                <div class="stat">
                    <span class="stat-label">Weekly Jobs</span>
                    <span class="stat-value">3</span>
                </div>
                <div class="stat">
                    <span class="stat-label">Monthly Jobs</span>
                    <span class="stat-value">3</span>
                </div>
                <div class="stat">
                    <span class="stat-label">Status</span>
                    <span class="status-badge status-green">ACTIVE</span>
                </div>
            </div>
        </div>

        <!-- Broker Details Table -->
        <div class="broker-list">
            <h2>📌 Detailed Broker Status</h2>
            <div class="broker-item" style="font-weight: bold; background: #f0f0f0;">
                <div>Broker</div>
                <div class="broker-status">Status</div>
                <div class="broker-submitted">Submitted</div>
                <div class="broker-verified">Verified</div>
                <div class="broker-date">Submission Date</div>
            </div>
"""

        for broker in broker_list:
            status_class = (
                "status-green" if broker["status"] == "verified_removed"
                else "status-yellow" if broker["status"] in ["removal_pending", "submitted"]
                else "status-red"
            )
            status_text = broker["status"].replace("_", " ").title()

            submitted_symbol = "✓" if broker["submitted"] else "✗"
            verified_symbol = "✓" if broker["verified"] else "✗"
            submitted_color = "checkmark" if broker["submitted"] else "x-mark"
            verified_color = "checkmark" if broker["verified"] else "x-mark"

            date_display = broker["submitted_date"][:10] if broker["submitted_date"] else "—"

            html += f"""
            <div class="broker-item">
                <div class="broker-name">{broker['name']}</div>
                <div class="broker-status"><span class="status-badge {status_class}">{status_text}</span></div>
                <div class="broker-submitted"><span class="{submitted_color}">{submitted_symbol}</span></div>
                <div class="broker-verified"><span class="{verified_color}">{verified_symbol}</span></div>
                <div class="broker-date">{date_display}</div>
            </div>
"""

        html += """
        </div>

        <div class="footer">
            <p>Privacy Data Removal Framework | Automated Monitoring & Remediation</p>
            <p>Refresh page to see updated data</p>
        </div>
    </div>

    <script>
        // Auto-refresh every 60 seconds
        setTimeout(function() {
            location.reload();
        }, 60000);
    </script>
</body>
</html>
"""
        return html

    def save_dashboard(self, filepath: str = "dashboard.html") -> None:
        """Save dashboard HTML to file"""
        html = self.generate_html()
        with open(filepath, 'w') as f:
            f.write(html)
        print(f"✓ Dashboard saved to {filepath}")

    def serve_dashboard(self, port: int = 8000) -> None:
        """Serve dashboard via HTTP"""
        try:
            from http.server import HTTPServer, SimpleHTTPRequestHandler
            import webbrowser

            class DashboardHandler(SimpleHTTPRequestHandler):
                def do_GET(self):
                    if self.path == "/" or self.path == "/dashboard.html":
                        self.send_response(200)
                        self.send_header("Content-type", "text/html")
                        self.end_headers()

                        dashboard = DashboardServer()
                        html = dashboard.generate_html()
                        self.wfile.write(html.encode())
                    else:
                        super().do_GET()

            server = HTTPServer(("localhost", port), DashboardHandler)
            print(f"🌐 Dashboard server running at http://localhost:{port}")
            print("Press Ctrl+C to stop")

            webbrowser.open(f"http://localhost:{port}")
            server.serve_forever()

        except Exception as e:
            print(f"Error starting server: {e}")
            print("Falling back to HTML file generation...")
            self.save_dashboard()


if __name__ == "__main__":
    import sys

    dashboard = DashboardServer()

    if len(sys.argv) > 1 and sys.argv[1] == "serve":
        port = int(sys.argv[2]) if len(sys.argv) > 2 else 8000
        dashboard.serve_dashboard(port)
    else:
        dashboard.save_dashboard()
        print("\nTo view dashboard:")
        print("  1. Open dashboard.html in a browser")
        print("  2. Or run: python3 scripts/dashboard_server.py serve")
