#!/usr/bin/env python3
"""
Privacy Data Removal Framework - Main Entry Point
Orchestrates all privacy removal operations
"""

import argparse
import json
import logging
import os
import sys
from pathlib import Path
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/privacy_framework.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class PrivacyFramework:
    """Main orchestrator for privacy removal framework"""

    def __init__(self, config_file=None):
        """Initialize framework with optional config file"""
        self.config = self._load_config(config_file)
        self.identity = self._load_identity()
        self.logs_dir = Path("logs")
        self.logs_dir.mkdir(exist_ok=True)
        logger.info(f"Framework initialized for {self.identity.get('name', 'unknown')}")

    def _load_identity(self):
        """Load identity from environment or config"""
        return {
            "name": os.getenv("REMOVAL_NAME", self.config.get("identity", {}).get("name", "User")),
            "email": os.getenv("REMOVAL_EMAIL", self.config.get("identity", {}).get("email", "user@example.com")),
            "phone": os.getenv("REMOVAL_PHONE", self.config.get("identity", {}).get("phone", "")),
        }

    def _load_config(self, config_file):
        """Load configuration from file"""
        if config_file and Path(config_file).exists():
            try:
                with open(config_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Could not load config file: {e}")
        return {}

    def run_full_audit(self):
        """Run complete privacy audit"""
        logger.info("=" * 60)
        logger.info("FULL PRIVACY AUDIT")
        logger.info("=" * 60)

        try:
            from privacy_audit import PrivacyAudit
            audit = PrivacyAudit(self.identity)
            results = audit.run()
            self._save_results("privacy_audit", results)
            logger.info("✓ Privacy audit complete")
            return results
        except Exception as e:
            logger.error(f"Privacy audit failed: {e}")
            return None

    def generate_removal_plan(self):
        """Generate data broker removal plan"""
        logger.info("=" * 60)
        logger.info("GENERATING REMOVAL PLAN")
        logger.info("=" * 60)

        try:
            from data_broker_automation import DataBrokerAutomation
            automation = DataBrokerAutomation(self.identity)
            plan = automation.generate_removal_plan()
            self._save_results("removal_plan", plan)
            logger.info(f"✓ Removal plan generated with {plan['total_brokers']} brokers")
            logger.info(f"  Total estimated days: {plan.get('total_estimated_days', 'N/A')}")
            return plan
        except Exception as e:
            logger.error(f"Plan generation failed: {e}")
            return None

    def track_removals(self):
        """Track removal progress"""
        logger.info("=" * 60)
        logger.info("TRACKING REMOVALS")
        logger.info("=" * 60)

        try:
            from data_broker_automation import DataBrokerAutomation
            automation = DataBrokerAutomation(self.identity)
            summary = automation.get_summary()
            self._save_results("removal_summary", summary)

            # Display summary
            self._display_summary(summary)
            return summary
        except Exception as e:
            logger.error(f"Removal tracking failed: {e}")
            return None

    def setup_monitoring(self):
        """Setup continuous monitoring"""
        logger.info("=" * 60)
        logger.info("SETTING UP MONITORING")
        logger.info("=" * 60)

        try:
            from monitoring_orchestrator import MonitoringOrchestrator
            orchestrator = MonitoringOrchestrator(self.identity)
            config = orchestrator.setup_monitoring()
            self._save_results("monitoring_config", config)
            logger.info("✓ Monitoring setup complete")
            return config
        except Exception as e:
            logger.error(f"Monitoring setup failed: {e}")
            return None

    def run_diagnostic(self):
        """Run system diagnostic"""
        logger.info("=" * 60)
        logger.info("RUNNING DIAGNOSTICS")
        logger.info("=" * 60)

        try:
            from diagnostic_tool import DiagnosticTool
            diagnostic = DiagnosticTool()
            results = diagnostic.run_all_checks()
            self._save_results("diagnostic_results", results)

            # Display diagnostic results
            self._display_diagnostics(results)
            return results
        except Exception as e:
            logger.error(f"Diagnostic failed: {e}")
            return None

    def _save_results(self, filename, data):
        """Save results to JSON file"""
        try:
            filepath = self.logs_dir / f"{filename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            logger.info(f"Results saved to {filepath}")
        except Exception as e:
            logger.error(f"Failed to save results: {e}")

    def _display_summary(self, summary):
        """Display removal summary"""
        print("\n" + "=" * 60)
        print("REMOVAL SUMMARY")
        print("=" * 60)
        print(f"Identity: {summary.get('identity', 'Unknown')}")
        print(f"Total Brokers: {summary.get('total_brokers', 0)}")
        print(f"Completion: {summary.get('completion_percentage', 0):.1f}%")
        print("\nStatus Breakdown:")
        for status, count in summary.get('status_breakdown', {}).items():
            print(f"  {status}: {count}")
        print("=" * 60 + "\n")

    def _display_diagnostics(self, results):
        """Display diagnostic results"""
        print("\n" + "=" * 60)
        print("DIAGNOSTIC RESULTS")
        print("=" * 60)
        for check, result in results.items():
            status = "✓" if result.get("passed") else "✗"
            print(f"{status} {check}: {result.get('message', 'N/A')}")
        print("=" * 60 + "\n")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Privacy Data Removal Framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run full privacy audit
  python3 main.py --audit

  # Generate removal plan
  python3 main.py --plan

  # Track removal progress
  python3 main.py --track

  # Setup monitoring
  python3 main.py --monitor

  # Run diagnostics
  python3 main.py --diagnostic

  # Run everything (full setup)
  python3 main.py --full
        """
    )

    parser.add_argument("--config", help="Path to configuration file")
    parser.add_argument("--audit", action="store_true", help="Run privacy audit")
    parser.add_argument("--plan", action="store_true", help="Generate removal plan")
    parser.add_argument("--track", action="store_true", help="Track removal progress")
    parser.add_argument("--monitor", action="store_true", help="Setup monitoring")
    parser.add_argument("--diagnostic", action="store_true", help="Run diagnostics")
    parser.add_argument("--full", action="store_true", help="Run full setup (audit → plan → monitor)")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")

    args = parser.parse_args()

    # Ensure logs directory exists
    Path("logs").mkdir(exist_ok=True)

    try:
        # Initialize framework
        framework = PrivacyFramework(args.config)

        # Adjust log level if verbose
        if args.verbose:
            logging.getLogger().setLevel(logging.DEBUG)

        # Run requested operations
        if args.full:
            logger.info("Starting full setup...")
            framework.run_full_audit()
            framework.generate_removal_plan()
            framework.setup_monitoring()
            logger.info("✓ Full setup complete!")

        elif args.audit:
            framework.run_full_audit()

        elif args.plan:
            framework.generate_removal_plan()

        elif args.track:
            framework.track_removals()

        elif args.monitor:
            framework.setup_monitoring()

        elif args.diagnostic:
            framework.run_diagnostic()

        else:
            # Default: show summary
            framework.track_removals()

        logger.info("✓ Operation complete")
        sys.exit(0)

    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        sys.exit(1)

    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
