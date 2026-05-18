#!/usr/bin/env python3
"""
Monitoring Orchestrator
Coordinates all automated monitoring tasks and generates alerts
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from pathlib import Path
from dataclasses import dataclass, asdict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class MonitoringEvent:
    """Represents a monitoring event"""
    event_id: str
    event_type: str
    severity: str
    source: str
    description: str
    detected_at: str
    action_required: bool
    action_taken: Optional[str] = None


class MonitoringOrchestrator:
    """Orchestrates all monitoring operations"""

    def __init__(self, identity: Dict):
        """
        Initialize monitoring orchestrator

        Args:
            identity: Identity profile to monitor
        """
        self.identity = identity
        self.monitoring_jobs = []
        self.events = []
        self.alerts = []

    def register_job(self, job: Dict) -> None:
        """
        Register a monitoring job

        Args:
            job: Job configuration
        """
        job_with_meta = {
            **job,
            "registered_at": datetime.now().isoformat(),
            "last_run": None,
            "next_run": self._calculate_next_run(job["frequency"]),
            "run_count": 0,
            "last_status": None
        }
        self.monitoring_jobs.append(job_with_meta)

    def setup_daily_checks(self) -> List[Dict]:
        """Setup daily monitoring jobs"""
        jobs = [
            {
                "job_id": "daily_hibp_check",
                "name": "HIBP Breach Monitoring",
                "frequency": "daily",
                "time": "03:00 UTC",
                "module": "hibp_monitor",
                "check_items": [self.identity.get("email")],
                "timeout": 30,
                "on_alert": "CRITICAL if new breach, HIGH if >3 breaches, MEDIUM if new password compromised"
            },
            {
                "job_id": "daily_search_check",
                "name": "Search Engine Monitoring",
                "frequency": "daily",
                "time": "06:00 UTC",
                "engines": ["google", "bing", "duckduckgo"],
                "search_terms": [
                    self.identity.get("name"),
                    self.identity.get("email"),
                    self.identity.get("github_username")
                ],
                "timeout": 60,
                "on_alert": "HIGH if removed URL appears, MEDIUM if new results"
            },
            {
                "job_id": "daily_archive_check",
                "name": "Archive.org Monitoring",
                "frequency": "daily",
                "time": "09:00 UTC",
                "sites": ["github.com/ChaitanyaJoshi1769"],
                "check_method": "Archive.org API",
                "timeout": 30,
                "on_alert": "MEDIUM if new snapshots added"
            }
        ]

        for job in jobs:
            self.register_job(job)

        return jobs

    def setup_weekly_checks(self) -> List[Dict]:
        """Setup weekly monitoring jobs"""
        jobs = [
            {
                "job_id": "weekly_data_broker_scan",
                "name": "Data Broker Rescan",
                "frequency": "weekly",
                "day": "Monday",
                "time": "02:00 UTC",
                "brokers": [
                    "spokeo", "whitepages", "intelius", "mylife",
                    "truecaller", "peoplefinder", "ussearch", "familytreenow"
                ],
                "timeout": 300,
                "on_alert": "HIGH if new listings found, CRITICAL if removal reverted"
            },
            {
                "job_id": "weekly_social_audit",
                "name": "Social Media Audit",
                "frequency": "weekly",
                "day": "Wednesday",
                "time": "10:00 UTC",
                "platforms": ["github", "linkedin", "twitter", "facebook"],
                "timeout": 60,
                "on_alert": "HIGH if unauthorized profile found"
            },
            {
                "job_id": "weekly_removal_verification",
                "name": "Removal Verification Check",
                "frequency": "weekly",
                "day": "Friday",
                "time": "14:00 UTC",
                "verify_urls": self._get_urls_to_verify(),
                "timeout": 120,
                "on_alert": "MEDIUM if URL still indexed, HIGH if re-indexed"
            }
        ]

        for job in jobs:
            self.register_job(job)

        return jobs

    def setup_monthly_checks(self) -> List[Dict]:
        """Setup monthly monitoring jobs"""
        jobs = [
            {
                "job_id": "monthly_credit_report",
                "name": "Credit Report Monitoring",
                "frequency": "monthly",
                "day": 1,
                "time": "06:00 UTC",
                "services": ["experian", "equifax", "transunion"],
                "timeout": 60,
                "on_alert": "CRITICAL if fraud detected, HIGH if suspicious inquiries"
            },
            {
                "job_id": "monthly_dark_web_scan",
                "name": "Dark Web Monitoring",
                "frequency": "monthly",
                "day": 15,
                "time": "03:00 UTC",
                "search_terms": [
                    self.identity.get("email"),
                    self.identity.get("phone")
                ],
                "services": ["haveibeenpwned", "dehashed"],
                "timeout": 120,
                "on_alert": "CRITICAL if credentials found, HIGH if PII found"
            },
            {
                "job_id": "monthly_comprehensive_audit",
                "name": "Comprehensive Privacy Audit",
                "frequency": "monthly",
                "day": 20,
                "time": "12:00 UTC",
                "modules": [
                    "exposure_scanner",
                    "privacy_audit",
                    "progress_reporter"
                ],
                "timeout": 300,
                "on_alert": "Generate comprehensive report"
            }
        ]

        for job in jobs:
            self.register_job(job)

        return jobs

    def log_event(self, event: MonitoringEvent) -> None:
        """Log a monitoring event"""
        self.events.append(asdict(event))
        logger.info(f"Event logged: {event.event_id} - {event.description}")

        if event.action_required:
            self.create_alert(event)

    def create_alert(self, event: MonitoringEvent) -> Dict:
        """
        Create alert from event

        Args:
            event: Monitoring event

        Returns:
            Alert record
        """
        alert = {
            "alert_id": f"alert_{int(datetime.now().timestamp())}",
            "from_event": event.event_id,
            "severity": event.severity,
            "title": f"{event.source}: {event.description}",
            "details": asdict(event),
            "created_at": datetime.now().isoformat(),
            "acknowledged": False,
            "action_required": True,
            "sla_minutes": self._get_sla(event.severity)
        }

        self.alerts.append(alert)
        return alert

    def simulate_daily_run(self) -> Dict:
        """Simulate a daily monitoring run and return results"""
        results = {
            "run_at": datetime.now().isoformat(),
            "jobs_executed": 0,
            "events_detected": 0,
            "alerts_raised": 0,
            "job_results": []
        }

        # Simulate HIBP check
        hibp_result = {
            "job": "daily_hibp_check",
            "status": "completed",
            "duration_seconds": 5,
            "findings": {
                "email_breached": False,
                "breach_count": 0,
                "action_needed": False
            }
        }
        results["job_results"].append(hibp_result)
        results["jobs_executed"] += 1

        # Simulate search check
        search_result = {
            "job": "daily_search_check",
            "status": "completed",
            "duration_seconds": 12,
            "findings": {
                "google_results": 42,
                "removed_urls": 0,
                "new_urls": 0,
                "action_needed": False
            }
        }
        results["job_results"].append(search_result)
        results["jobs_executed"] += 1

        # Simulate archive check
        archive_result = {
            "job": "daily_archive_check",
            "status": "completed",
            "duration_seconds": 3,
            "findings": {
                "snapshots": 5,
                "new_snapshots": 0,
                "action_needed": False
            }
        }
        results["job_results"].append(archive_result)
        results["jobs_executed"] += 1

        return results

    def generate_monitoring_report(self) -> Dict:
        """Generate comprehensive monitoring report"""
        report = {
            "generated_at": datetime.now().isoformat(),
            "identity": self.identity.get("name"),
            "monitoring_status": "active",
            "total_jobs": len(self.monitoring_jobs),
            "jobs_by_frequency": self._count_by_frequency(),
            "recent_events": self.events[-10:] if self.events else [],
            "active_alerts": [a for a in self.alerts if not a["acknowledged"]],
            "event_summary": self._get_event_summary(),
            "recommendations": self._generate_recommendations()
        }
        return report

    def export_all_data(self, output_dir: str = "logs") -> None:
        """Export all monitoring data"""
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        # Export jobs
        with open(f"{output_dir}/monitoring_jobs.json", 'w') as f:
            json.dump(self.monitoring_jobs, f, indent=2)

        # Export events
        with open(f"{output_dir}/monitoring_events.json", 'w') as f:
            json.dump(self.events, f, indent=2)

        # Export alerts
        with open(f"{output_dir}/monitoring_alerts.json", 'w') as f:
            json.dump(self.alerts, f, indent=2)

        # Export report
        report = self.generate_monitoring_report()
        with open(f"{output_dir}/monitoring_report.json", 'w') as f:
            json.dump(report, f, indent=2)

    def _calculate_next_run(self, frequency: str) -> str:
        """Calculate next run time"""
        now = datetime.now()
        if frequency == "daily":
            next_run = now + timedelta(days=1)
        elif frequency == "weekly":
            next_run = now + timedelta(weeks=1)
        elif frequency == "monthly":
            next_run = now + timedelta(days=30)
        else:
            next_run = now + timedelta(hours=1)
        return next_run.isoformat()

    def _get_urls_to_verify(self) -> List[str]:
        """Get list of URLs to verify for removal"""
        return [
            "https://github.com/ChaitanyaJoshi1769",
            "https://github.com/ChaitanyaJoshi1769?tab=repositories"
        ]

    def _get_sla(self, severity: str) -> int:
        """Get SLA minutes for alert severity"""
        slas = {
            "CRITICAL": 5,
            "HIGH": 60,
            "MEDIUM": 1440,
            "LOW": 10080
        }
        return slas.get(severity, 1440)

    def _count_by_frequency(self) -> Dict:
        """Count jobs by frequency"""
        counts = {}
        for job in self.monitoring_jobs:
            freq = job.get("frequency", "unknown")
            counts[freq] = counts.get(freq, 0) + 1
        return counts

    def _get_event_summary(self) -> Dict:
        """Get summary of events"""
        summary = {
            "total_events": len(self.events),
            "by_severity": {},
            "by_source": {}
        }

        for event in self.events:
            severity = event.get("severity", "unknown")
            source = event.get("source", "unknown")
            summary["by_severity"][severity] = summary["by_severity"].get(severity, 0) + 1
            summary["by_source"][source] = summary["by_source"].get(source, 0) + 1

        return summary

    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations based on monitoring data"""
        recs = []

        if any(a for a in self.alerts if a["severity"] == "CRITICAL"):
            recs.append("⚠️  CRITICAL: Immediate action required on alerts")

        if not any(j for j in self.monitoring_jobs if j["frequency"] == "daily"):
            recs.append("Enable daily monitoring for early breach detection")

        if not any(j for j in self.monitoring_jobs if j["frequency"] == "monthly"):
            recs.append("Setup monthly comprehensive audits")

        if not recs:
            recs.append("✓ Monitoring system healthy - continue current schedule")

        return recs


if __name__ == "__main__":
    identity = {
        "name": "Chaitanya Joshi",
        "email": "chaitanyajoshi15@gmail.com",
        "github_username": "ChaitanyaJoshi1769",
        "phone": "+1-XXXXXXXXX"
    }

    orchestrator = MonitoringOrchestrator(identity)

    print("Setting up monitoring jobs...")
    orchestrator.setup_daily_checks()
    orchestrator.setup_weekly_checks()
    orchestrator.setup_monthly_checks()

    print(f"Total jobs registered: {len(orchestrator.monitoring_jobs)}")

    print("\nSimulating daily run...")
    daily_result = orchestrator.simulate_daily_run()
    print(json.dumps(daily_result, indent=2))

    print("\nGenerating report...")
    report = orchestrator.generate_monitoring_report()
    print(json.dumps(report, indent=2))

    orchestrator.export_all_data()
    print("\n✓ Monitoring data exported to logs/")
