#!/usr/bin/env python3
"""
Health Check - Verify Privacy Framework Installation and Configuration
"""

import json
import logging
import os
import sys
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class HealthCheck:
    """Performs comprehensive system health checks"""

    def __init__(self):
        self.results = {}
        self.checks_passed = 0
        self.checks_failed = 0

    def run_all_checks(self):
        """Run all health checks"""
        print("\n" + "=" * 60)
        print("PRIVACY FRAMEWORK HEALTH CHECK")
        print("=" * 60 + "\n")

        self.check_python_version()
        self.check_dependencies()
        self.check_directories()
        self.check_environment()
        self.check_configuration()
        self.check_logs()
        self.check_tracking_data()

        self.print_summary()
        return self.results

    def check_python_version(self):
        """Verify Python version"""
        check_name = "Python Version"
        try:
            version = sys.version_info
            if version.major >= 3 and version.minor >= 8:
                self.pass_check(check_name, f"Python {version.major}.{version.minor}.{version.micro}")
            else:
                self.fail_check(check_name, f"Python {version.major}.{version.minor} (requires 3.8+)")
        except Exception as e:
            self.fail_check(check_name, str(e))

    def check_dependencies(self):
        """Verify required dependencies are installed"""
        check_name = "Dependencies"
        required = ['requests', 'flask', 'pandas']
        missing = []

        for pkg in required:
            try:
                __import__(pkg.replace('-', '_'))
            except ImportError:
                missing.append(pkg)

        if not missing:
            self.pass_check(check_name, "All required packages installed")
        else:
            self.fail_check(check_name, f"Missing: {', '.join(missing)}")

    def check_directories(self):
        """Verify required directories exist"""
        check_name = "Directory Structure"
        required_dirs = ['logs', 'scripts', 'data']
        missing = []

        for directory in required_dirs:
            if not Path(directory).exists():
                missing.append(directory)
            else:
                Path(directory).mkdir(exist_ok=True)

        if not missing:
            self.pass_check(check_name, "All required directories present")
        else:
            self.fail_check(check_name, f"Missing: {', '.join(missing)}")

    def check_environment(self):
        """Verify environment variables are set"""
        check_name = "Environment Variables"
        required_vars = ['REMOVAL_NAME', 'REMOVAL_EMAIL']
        missing = []

        for var in required_vars:
            if not os.getenv(var):
                missing.append(var)

        if not missing:
            name = os.getenv('REMOVAL_NAME')
            email = os.getenv('REMOVAL_EMAIL')
            self.pass_check(check_name, f"{name} ({email})")
        else:
            self.fail_check(check_name, f"Missing: {', '.join(missing)}")

    def check_configuration(self):
        """Verify configuration files"""
        check_name = "Configuration Files"
        config_file = Path("scripts/config.json")
        example_file = Path("scripts/config.example.json")

        if example_file.exists():
            if config_file.exists():
                self.pass_check(check_name, "config.json exists and ready")
            else:
                self.fail_check(check_name, "config.json missing")
        else:
            self.fail_check(check_name, "config.example.json not found")

    def check_logs(self):
        """Verify logs directory and recent files"""
        check_name = "Logs Directory"
        logs_dir = Path("logs")

        if logs_dir.exists():
            log_files = list(logs_dir.glob("*.json"))
            if log_files:
                latest = max(log_files, key=lambda p: p.stat().st_mtime)
                self.pass_check(check_name, f"{len(log_files)} log files (latest: {latest.name})")
            else:
                self.pass_check(check_name, "Empty (no logs yet)")
        else:
            self.fail_check(check_name, "logs/ directory missing")

    def check_tracking_data(self):
        """Verify tracking data exists"""
        check_name = "Tracking Data"
        tracking_file = Path("logs/broker_tracking_complete.json")

        if tracking_file.exists():
            try:
                with open(tracking_file, 'r') as f:
                    data = json.load(f)
                count = len(data)
                self.pass_check(check_name, f"{count} brokers tracked")
            except Exception as e:
                self.fail_check(check_name, f"Error reading: {e}")
        else:
            self.fail_check(check_name, "No tracking data")

    def pass_check(self, name, message):
        """Record passed check"""
        self.results[name] = {"passed": True, "message": message}
        self.checks_passed += 1
        print(f"✓ {name}: {message}")

    def fail_check(self, name, message):
        """Record failed check"""
        self.results[name] = {"passed": False, "message": message}
        self.checks_failed += 1
        print(f"✗ {name}: {message}")

    def print_summary(self):
        """Print health check summary"""
        print("\n" + "=" * 60)
        print(f"SUMMARY: {self.checks_passed} passed, {self.checks_failed} failed")
        print("=" * 60 + "\n")

        if self.checks_failed == 0:
            print("✓ All checks passed! System is ready to use.")
        else:
            print(f"⚠ {self.checks_failed} issue(s) to resolve.")
        print()


def main():
    """Main entry point"""
    try:
        checker = HealthCheck()
        checker.run_all_checks()
        sys.exit(0 if checker.checks_failed == 0 else 1)
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
