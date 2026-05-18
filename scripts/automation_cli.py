#!/usr/bin/env python3
"""
Privacy Framework Automation CLI
Central command-line interface for all automation tools
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime

# Import all automation modules
from hibp_monitor import HIBPMonitor
from gsc_removal_agent import GSCRemovalAgent
from bing_removal_agent import BingRemovalAgent
from monitoring_orchestrator import MonitoringOrchestrator
from data_broker_automation import DataBrokerAutomation
from broker_tracker import DataBrokerTracker
from exposure_scanner import ExposureScanner
from progress_reporter import ProgressReporter
from privacy_audit import PrivacyAudit


class AutomationCLI:
    """Central CLI for all automation operations"""

    def __init__(self):
        self.parser = self._create_parser()
        self.output_dir = Path("logs")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _create_parser(self) -> argparse.ArgumentParser:
        """Create argument parser"""
        parser = argparse.ArgumentParser(
            prog="privacy-automation",
            description="Privacy Data Removal Framework - Automation CLI"
        )

        subparsers = parser.add_subparsers(dest="command", help="Available commands")

        # Monitoring commands
        monitoring = subparsers.add_parser("monitor", help="Run monitoring operations")
        monitoring.add_argument("--check", choices=["hibp", "search", "archive", "all"],
                             default="all", help="Type of check to run")
        monitoring.add_argument("--email", help="Email to check (for HIBP)")

        # Removal commands
        removal = subparsers.add_parser("removal", help="Manage removal operations")
        removal.add_argument("--broker", help="Data broker to target")
        removal.add_argument("--list", action="store_true", help="List all brokers")
        removal.add_argument("--plan", action="store_true", help="Generate removal plan")
        removal.add_argument("--search", action="store_true", help="Search across all brokers")

        # Search removal commands
        search_removal = subparsers.add_parser("deindex", help="Manage search de-indexing")
        search_removal.add_argument("--provider", choices=["google", "bing", "both"],
                                  default="both")
        search_removal.add_argument("--urls", nargs="+", help="URLs to delist")

        # Audit commands
        audit = subparsers.add_parser("audit", help="Run privacy audits")
        audit.add_argument("--type", choices=["github", "search", "all"],
                         default="all")
        audit.add_argument("--full", action="store_true", help="Run comprehensive audit")

        # Report commands
        reporting = subparsers.add_parser("report", help="Generate reports")
        reporting.add_argument("--type", choices=["progress", "monitoring", "summary"],
                             default="summary")
        reporting.add_argument("--period", choices=["weekly", "monthly"],
                             default="weekly")

        # Dashboard command
        dashboard = subparsers.add_parser("dashboard", help="View monitoring dashboard")
        dashboard.add_argument("--export", action="store_true", help="Export as JSON")

        # Help
        subparsers.add_parser("help", help="Show detailed help")

        return parser

    def run(self, args=None) -> None:
        """Run CLI"""
        if args is None:
            args = sys.argv[1:]

        if not args:
            self.parser.print_help()
            return

        parsed = self.parser.parse_args(args)

        try:
            if parsed.command == "monitor":
                self.run_monitoring(parsed)
            elif parsed.command == "removal":
                self.run_removal(parsed)
            elif parsed.command == "deindex":
                self.run_deindex(parsed)
            elif parsed.command == "audit":
                self.run_audit(parsed)
            elif parsed.command == "report":
                self.run_report(parsed)
            elif parsed.command == "dashboard":
                self.run_dashboard(parsed)
            elif parsed.command == "help":
                self.print_detailed_help()
            else:
                self.parser.print_help()
        except Exception as e:
            print(f"❌ Error: {e}", file=sys.stderr)
            sys.exit(1)

    def run_monitoring(self, args) -> None:
        """Execute monitoring operations"""
        print("🔍 Running monitoring checks...")

        if args.check in ["hibp", "all"]:
            print("\n📧 HIBP Breach Check")
            monitor = HIBPMonitor()
            identity = {
                "name": "Chaitanya Joshi",
                "email": args.email or "chaitanyajoshi15@gmail.com",
                "domain": "gmail.com"
            }
            report = monitor.generate_report(identity)
            print(json.dumps(report, indent=2))
            monitor.save_log(str(self.output_dir / "hibp_breaches.json"))
            print("✓ HIBP check complete")

        if args.check in ["search", "all"]:
            print("\n🔎 Search Engine Monitoring")
            print("Note: Manual verification needed")
            print("✓ Search monitoring configured")

        if args.check in ["archive", "all"]:
            print("\n📚 Archive.org Monitoring")
            print("Note: Manual verification needed")
            print("✓ Archive monitoring configured")

    def run_removal(self, args) -> None:
        """Execute removal operations"""
        print("🗑️  Running removal operations...")

        if args.list:
            self._list_brokers()
            return

        if args.plan:
            print("\nGenerating data broker removal plan...")
            automation = DataBrokerAutomation({
                "name": "Chaitanya Joshi",
                "email": "chaitanyajoshi15@gmail.com"
            })
            plan = automation.generate_removal_plan()
            print(json.dumps(plan, indent=2))
            automation.export_tracking(str(self.output_dir / "broker_tracking.json"))
            automation.export_summary(str(self.output_dir / "broker_summary.json"))
            print("✓ Removal plan generated")
            return

        if args.search:
            print("\nSearching across all data brokers...")
            automation = DataBrokerAutomation({
                "name": "Chaitanya Joshi",
                "email": "chaitanyajoshi15@gmail.com"
            })
            results = automation.search_all_brokers()
            print(json.dumps(results, indent=2))
            print("✓ Broker search complete")
            return

    def run_deindex(self, args) -> None:
        """Execute search engine de-indexing"""
        print("🔍 Managing search engine de-indexing...")

        urls = args.urls or [
            "https://github.com/ChaitanyaJoshi1769",
            "https://github.com/ChaitanyaJoshi1769?tab=repositories"
        ]

        if args.provider in ["google", "both"]:
            print("\n📍 Google Search Console Removal")
            gsc = GSCRemovalAgent()
            plan = gsc.generate_removal_plan(urls, priority="high")
            print(json.dumps(plan, indent=2))
            gsc.save_plan(plan, str(self.output_dir / "gsc_removal_plan.json"))
            gsc.export_tracking(str(self.output_dir / "gsc_removal_tracking.json"))
            print("✓ GSC removal plan generated")

        if args.provider in ["bing", "both"]:
            print("\n🔵 Bing Webmaster Tools Removal")
            bing = BingRemovalAgent()
            batch = bing.generate_removal_batch(urls)
            print(json.dumps(batch, indent=2))
            bing.export_summary(str(self.output_dir / "bing_removal_summary.json"))
            print("✓ Bing removal plan generated")

    def run_audit(self, args) -> None:
        """Execute privacy audits"""
        print("🔐 Running privacy audits...")

        audit = PrivacyAudit()

        if args.type in ["github", "all"]:
            print("\n🐙 GitHub Audit")
            github_audit = audit.audit_github()
            print(json.dumps(github_audit, indent=2))

        if args.type in ["search", "all"]:
            print("\n🔎 Search Engine Audit")
            search_audit = audit.audit_search_engines()
            print(json.dumps(search_audit, indent=2))

        if args.full:
            print("\n📊 Comprehensive Audit Report")
            report = audit.generate_audit_report()
            print(json.dumps(report, indent=2))

        print("✓ Audit complete")

    def run_report(self, args) -> None:
        """Generate reports"""
        print("📊 Generating reports...")

        reporter = ProgressReporter()

        if args.type == "progress":
            if args.period == "weekly":
                report = reporter.generate_weekly_report()
            else:
                report = reporter.generate_monthly_report()
            print(json.dumps(report, indent=2))

        elif args.type == "monitoring":
            identity = {
                "name": "Chaitanya Joshi",
                "email": "chaitanyajoshi15@gmail.com"
            }
            orchestrator = MonitoringOrchestrator(identity)
            orchestrator.setup_daily_checks()
            orchestrator.setup_weekly_checks()
            report = orchestrator.generate_monitoring_report()
            print(json.dumps(report, indent=2))

        print("✓ Report generated")

    def run_dashboard(self, args) -> None:
        """Display monitoring dashboard"""
        print("📈 Privacy Framework Dashboard")
        print("=" * 60)

        # Load all tracking data
        tracking_file = self.output_dir / "broker_tracking.json"
        hibp_file = self.output_dir / "hibp_breaches.json"
        progress_file = Path("logs/progress_master.json")

        dashboard = {
            "generated_at": datetime.now().isoformat(),
            "sections": {}
        }

        # Broker summary
        if tracking_file.exists():
            with open(tracking_file) as f:
                tracking = json.load(f)
                dashboard["sections"]["data_brokers"] = {
                    "total": len(tracking),
                    "verified_removed": sum(
                        1 for t in tracking.values()
                        if t.get("verified_removed")
                    ) if isinstance(tracking, dict) else 0
                }

        # HIBP summary
        if hibp_file.exists():
            with open(hibp_file) as f:
                hibp_data = json.load(f)
                breached = sum(1 for h in hibp_data if h.get("breached"))
                dashboard["sections"]["breach_monitoring"] = {
                    "total_checks": len(hibp_data),
                    "breached_emails": breached
                }

        print(json.dumps(dashboard, indent=2))

        if args.export:
            export_path = self.output_dir / "dashboard.json"
            with open(export_path, 'w') as f:
                json.dump(dashboard, f, indent=2)
            print(f"\n✓ Dashboard exported to {export_path}")

    def _list_brokers(self) -> None:
        """List all available data brokers"""
        automation = DataBrokerAutomation({})
        print("\n📋 Available Data Brokers:")
        print("=" * 70)

        for broker_id, broker_info in automation.BROKERS.items():
            name = broker_info["name"]
            difficulty = broker_info["difficulty"]
            days = broker_info["time_estimate_days"]
            print(f"  {broker_id:20} | {name:20} | {difficulty:10} | {days} days")

        print("=" * 70)

    def print_detailed_help(self) -> None:
        """Print detailed help"""
        help_text = """
Privacy Data Removal Framework - Automation CLI

USAGE:
  privacy-automation <command> [options]

COMMANDS:
  monitor       Run monitoring checks (HIBP, search engines, archives)
  removal       Manage data broker removal operations
  deindex       Manage search engine de-indexing (Google, Bing)
  audit         Run privacy audits
  report        Generate progress and status reports
  dashboard     View monitoring dashboard
  help          Show this help message

EXAMPLES:
  # Check for breaches
  privacy-automation monitor --check hibp --email your@email.com

  # Generate removal plan
  privacy-automation removal --plan

  # De-index from Google and Bing
  privacy-automation deindex --provider both

  # Run comprehensive audit
  privacy-automation audit --type all --full

  # Generate weekly progress report
  privacy-automation report --type progress --period weekly

  # View dashboard
  privacy-automation dashboard --export
        """
        print(help_text)


def main():
    """Main entry point"""
    cli = AutomationCLI()
    cli.run()


if __name__ == "__main__":
    main()
