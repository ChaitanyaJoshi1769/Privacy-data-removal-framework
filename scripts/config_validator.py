#!/usr/bin/env python3
"""
Configuration Validator and Migrator
Validates configuration files and handles version migrations
"""

import sys
import json
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime


class ConfigValidator:
    """Validate and migrate framework configurations"""

    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.config_dir = self.project_root / "intel"
        self.valid_config_version = "2.0"
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "validations": [],
            "errors": [],
            "warnings": [],
            "migrations": [],
            "recommendations": []
        }

    def validate_identity_profile(self) -> Tuple[bool, List[str]]:
        """Validate identity profile configuration"""
        profile_file = self.config_dir / "identity_profile.json"
        errors = []

        if not profile_file.exists():
            return False, ["Identity profile not found at intel/identity_profile.json"]

        try:
            with open(profile_file) as f:
                profile = json.load(f)
        except json.JSONDecodeError as e:
            return False, [f"Invalid JSON in identity profile: {str(e)}"]

        # Validate required fields
        required_fields = ["name", "email"]
        for field in required_fields:
            if field not in profile:
                errors.append(f"Missing required field: {field}")

        # Validate email format (basic)
        if "email" in profile and "@" not in profile["email"]:
            errors.append("Invalid email format in identity profile")

        # Validate phone format if present
        if "phone" in profile and profile["phone"]:
            phone = profile["phone"]
            if not any(c.isdigit() for c in phone):
                errors.append("Phone number should contain digits")

        # Validate accounts array if present
        if "accounts" in profile and isinstance(profile["accounts"], list):
            for i, account in enumerate(profile["accounts"]):
                if "platform" not in account:
                    errors.append(f"Account {i}: missing platform field")
                if "username" not in account:
                    errors.append(f"Account {i}: missing username field")

        return len(errors) == 0, errors

    def validate_privacy_config(self) -> Tuple[bool, List[str]]:
        """Validate privacy configuration"""
        config_file = self.project_root / ".privacy-config.json"
        errors = []

        if not config_file.exists():
            # Create from template if missing
            self.results["warnings"].append(
                "Privacy config not found - using defaults"
            )
            return True, errors

        try:
            with open(config_file) as f:
                config = json.load(f)
        except json.JSONDecodeError as e:
            return False, [f"Invalid JSON in privacy config: {str(e)}"]

        # Validate config structure
        if "monitoring" in config:
            monitoring = config["monitoring"]
            valid_frequencies = ["daily", "weekly", "monthly"]
            if "frequency" in monitoring:
                if monitoring["frequency"] not in valid_frequencies:
                    errors.append(
                        f"Invalid monitoring frequency: {monitoring['frequency']}"
                    )

        if "removal" in config:
            removal = config["removal"]
            valid_phases = ["easy", "medium", "hard"]
            if "phase" in removal:
                if removal["phase"] not in valid_phases:
                    errors.append(f"Invalid removal phase: {removal['phase']}")

        return len(errors) == 0, errors

    def validate_broker_tracking(self) -> Tuple[bool, List[str]]:
        """Validate broker tracking file"""
        tracking_file = self.config_dir / "broker_tracking.json"
        errors = []

        if not tracking_file.exists():
            return True, []  # Optional file

        try:
            with open(tracking_file) as f:
                tracking = json.load(f)
        except json.JSONDecodeError as e:
            return False, [f"Invalid JSON in broker tracking: {str(e)}"]

        # Validate broker entries if present
        if "brokers" in tracking and isinstance(tracking["brokers"], dict):
            valid_statuses = [
                "not_found", "found", "submitted", "removal_pending",
                "verified_removed", "removal_failed", "reappeared"
            ]
            for broker_id, broker_data in tracking["brokers"].items():
                if "status" in broker_data:
                    if broker_data["status"] not in valid_statuses:
                        errors.append(f"Invalid status for {broker_id}: {broker_data['status']}")

        return len(errors) == 0, errors

    def validate_github_actions(self) -> Tuple[bool, List[str]]:
        """Validate GitHub Actions workflows"""
        workflows_dir = self.project_root / ".github" / "workflows"
        errors = []

        if not workflows_dir.exists():
            self.results["warnings"].append(
                "GitHub workflows not configured - automated monitoring disabled"
            )
            return True, errors

        required_workflows = ["daily-monitoring.yml", "testing.yml"]
        for workflow in required_workflows:
            workflow_file = workflows_dir / workflow
            if not workflow_file.exists():
                errors.append(f"Missing workflow: {workflow}")

        return len(errors) == 0, errors

    def validate_directory_structure(self) -> Tuple[bool, List[str]]:
        """Validate required directories"""
        required_dirs = [
            "scripts",
            "intel",
            "logs",
            "templates",
            "notebooks",
            "tests",
            "examples",
            ".github/workflows"
        ]

        errors = []
        for directory in required_dirs:
            dir_path = self.project_root / directory
            if not dir_path.exists():
                errors.append(f"Missing directory: {directory}")

        return len(errors) == 0, errors

    def migrate_config_v1_to_v2(self) -> bool:
        """Migrate configuration from v1.0 to v2.0"""
        config_file = self.project_root / ".privacy-config.json"

        if not config_file.exists():
            return True  # Nothing to migrate

        try:
            with open(config_file) as f:
                config = json.load(f)
        except:
            return False

        # Check if already v2.0
        if config.get("version") == "2.0":
            return True

        # Add v2.0 fields if missing
        if "version" not in config:
            config["version"] = "2.0"
            self.results["migrations"].append("Added version field (v2.0)")

        if "monitoring_jobs" not in config:
            config["monitoring_jobs"] = {
                "daily": ["hibp_check", "search_monitoring", "archive_scan"],
                "weekly": ["broker_rescan", "social_audit", "removal_verification"],
                "monthly": ["credit_check", "dark_web_scan", "comprehensive_audit"]
            }
            self.results["migrations"].append("Added monitoring_jobs configuration")

        if "privacy_hardening" not in config:
            config["privacy_hardening"] = {
                "tier": "basic",
                "dns_privacy": False,
                "vpn_enabled": False,
                "duckduckgo_enabled": False
            }
            self.results["migrations"].append("Added privacy_hardening configuration")

        # Save migrated config
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)

        self.results["migrations"].append(f"Config migrated to v2.0")
        return True

    def check_template_files(self) -> Tuple[bool, List[str]]:
        """Check for required template files"""
        templates_dir = self.project_root / "templates"
        warnings = []

        if not templates_dir.exists():
            warnings.append("Templates directory not found")
            return True, warnings

        # Check for common template categories
        expected_subdirs = [
            "removal_workflows",
            "search_removal",
            "privacy_requests"
        ]

        for subdir in expected_subdirs:
            subdir_path = templates_dir / subdir
            if not subdir_path.exists():
                warnings.append(f"Template directory missing: {subdir}")

        return True, warnings

    def validate_all(self) -> None:
        """Run all validations"""
        print("\n" + "="*60)
        print("✓ CONFIGURATION VALIDATOR")
        print("="*60 + "\n")

        validations = [
            ("Directory Structure", self.validate_directory_structure),
            ("Identity Profile", self.validate_identity_profile),
            ("Privacy Config", self.validate_privacy_config),
            ("Broker Tracking", self.validate_broker_tracking),
            ("GitHub Actions", self.validate_github_actions),
            ("Templates", self.check_template_files),
        ]

        passed = 0
        failed = 0

        for check_name, check_func in validations:
            try:
                success, issues = check_func()
                self.results["validations"].append({
                    "name": check_name,
                    "status": "pass" if success else "fail",
                    "issues": issues
                })

                if success:
                    passed += 1
                    status = "✓"
                    detail = "OK"
                else:
                    failed += 1
                    status = "✗"
                    detail = f"{len(issues)} issues"

                print(f"{status} {check_name:30} {detail}")

                if issues and failed <= 3:
                    for issue in issues[:3]:
                        print(f"    └─ {issue}")

            except Exception as e:
                failed += 1
                print(f"✗ {check_name:30} ERROR: {str(e)[:40]}")
                self.results["errors"].append(f"{check_name}: {str(e)}")

        # Run migration
        print("\n" + "-"*60)
        print("📦 CONFIGURATION MIGRATION")
        print("-"*60 + "\n")

        if self.migrate_config_v1_to_v2():
            print("✓ Configuration migration: OK")
        else:
            print("✗ Configuration migration: FAILED")

        # Generate summary
        self.generate_summary(passed, failed)

    def generate_summary(self, passed: int, failed: int) -> None:
        """Generate validation summary"""
        print("\n" + "="*60)
        print("📊 VALIDATION SUMMARY")
        print("="*60)

        print(f"\nValidations: {passed} passed, {failed} failed")

        if self.results["migrations"]:
            print(f"\nMigrations Applied: {len(self.results['migrations'])}")
            for migration in self.results["migrations"][:3]:
                print(f"  ✓ {migration}")
            if len(self.results["migrations"]) > 3:
                print(f"  ... and {len(self.results['migrations']) - 3} more")

        if self.results["warnings"]:
            print(f"\n⚠️  Warnings ({len(self.results['warnings'])})")
            for warning in self.results["warnings"][:3]:
                print(f"  ⚠️  {warning}")

        if self.results["errors"]:
            print(f"\n🔴 Errors ({len(self.results['errors'])})")
            for error in self.results["errors"][:3]:
                print(f"  ✗ {error}")

        # Recommendations
        print(f"\n💡 RECOMMENDATIONS")
        if failed == 0:
            print("  ✓ Configuration is valid")
            print("  ✓ All validations passed")
            print("  ✓ Ready for deployment")
        else:
            print(f"  → Fix {failed} validation issue(s) above")
            print(f"  → Review error messages for details")
            print(f"  → See GETTING_STARTED.md for setup help")

        # Save results
        self.save_results()

    def save_results(self) -> None:
        """Save validation results"""
        report_file = self.project_root / "logs" / "config_validation_report.json"
        report_file.parent.mkdir(parents=True, exist_ok=True)

        with open(report_file, 'w') as f:
            json.dump(self.results, f, indent=2)

        print(f"\n✓ Report saved to logs/config_validation_report.json")

    def run(self) -> int:
        """Run validator and return status code"""
        self.validate_all()
        return 0 if not self.results["errors"] else 1


if __name__ == "__main__":
    validator = ConfigValidator()
    exit_code = validator.run()
    sys.exit(exit_code)
