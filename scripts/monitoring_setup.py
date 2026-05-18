#!/usr/bin/env python3
"""
Automated monitoring for data removal and breach detection
"""

import json
from datetime import datetime
from pathlib import Path

class MonitoringSetup:
    """Set up automated monitoring for digital footprint"""
    
    def __init__(self, email, name):
        self.email = email
        self.name = name
        self.project_root = Path(__file__).parent.parent
        
    def create_monitoring_config(self):
        """Create monitoring configuration"""
        return {
            "email": self.email,
            "name": self.name,
            "setup_date": datetime.now().isoformat(),
            "google_alerts": [
                {"query": self.email, "frequency": "daily"},
                {"query": self.name, "frequency": "daily"},
            ],
            "breach_monitoring_services": [
                {"name": "Have I Been Pwned", "url": "https://haveibeenpwned.com/"},
                {"name": "Firefox Monitor", "url": "https://monitor.firefox.com/"},
                {"name": "Google Password Manager", "url": "https://passwords.google.com/"},
            ],
            "quarterly_checks": [
                "Search Google for your name",
                "Search Bing for your name", 
                "Check TrueCaller",
                "Check WhitePages",
                "Check MyLife",
                "Check Spokeo",
                "Verify breach databases",
            ]
        }
    
    def save_config(self):
        """Save monitoring configuration"""
        config = self.create_monitoring_config()
        config_file = self.project_root / "logs" / "monitoring_config.json"
        config_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        return config_file

if __name__ == "__main__":
    monitoring = MonitoringSetup("chaitanyajoshi15@gmail.com", "Chaitanya Prabhakar Joshi")
    config_file = monitoring.save_config()
    print(f"✓ Monitoring config saved to: {config_file}")

