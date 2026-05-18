#!/usr/bin/env python3
"""
Privacy Framework Diagnostic Tool
Checks system setup, validates configurations, and identifies issues
"""

import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime


class FrameworkDiagnostic:
    """Diagnostic tool for framework health checks"""

    def __init__(self):
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "checks": {},
            "warnings": [],
            "errors": [],
            "recommendations": []
        }
        self.project_root = Path(__file__).parent.parent

    def check_python_version(self) -> bool:
        """Check Python version compatibility"""
        version = sys.version_info
        check = {
            "name": "Python Version",
            "status": "pass" if version.major >= 3 and version.minor >= 7 else "fail",
            "details": f"Python {version.major}.{version.minor}.{version.micro}",
            "required": "3.7+"
        }

        if check["status"] == "fail":
            self.results["errors"].append("Python 3.7+ required")

        self.results["checks"]["python_version"] = check
        return check["status"] == "pass"

    def check_dependencies(self) -> bool:
        """Check required Python packages"""
        try:
            import requests
            check = {
                "name": "Python Dependencies",
                "status": "pass",
                "packages": {
                    "requests": "installed"
                }
            }
        except ImportError:
            check = {
                "name": "Python Dependencies",
                "status": "fail",
                "packages": {
                    "requests": "MISSING"
                }
            }
            self.results["errors"].append("Missing: requests library")
            self.results["recommendations"].append(
                "Install: pip install -r scripts/requirements.txt"
            )

        self.results["checks"]["dependencies"] = check
        return check["status"] == "pass"

    def check_directory_structure(self) -> bool:
        """Check if all required directories exist"""
        required_dirs = [
            "scripts",
            "logs",
            "intel",
            "templates",
            "notebooks",
            "tests",
            ".github/workflows"
        ]

        missing = []
        for directory in required_dirs:
            path = self.project_root / directory
            if not path.exists():
                missing.append(directory)

        check = {
            "name": "Directory Structure",
            "status": "pass" if not missing else "fail",
            "directories_found": len(required_dirs) - len(missing),
            "directories_total": len(required_dirs),
            "missing": missing if missing else None
        }

        if missing:
            self.results["errors"].append(f"Missing directories: {', '.join(missing)}")
            self.results["recommendations"].append("Run: python3 init.py")

        self.results["checks"]["directories"] = check
        return check["status"] == "pass"

    def check_scripts(self) -> bool:
        """Check if all automation scripts exist"""
        required_scripts = [
            "hibp_monitor.py",
            "gsc_removal_agent.py",
            "bing_removal_agent.py",
            "data_broker_automation.py",
            "monitoring_orchestrator.py",
            "automation_cli.py",
            "dashboard_server.py",
            "broker_tracker.py",
            "exposure_scanner.py",
            "privacy_audit.py",
            "progress_reporter.py"
        ]

        scripts_dir = self.project_root / "scripts"
        found = []
        missing = []

        for script in required_scripts:
            if (scripts_dir / script).exists():
                found.append(script)
            else:
                missing.append(script)

        check = {
            "name": "Automation Scripts",
            "status": "pass" if not missing else "fail",
            "scripts_found": len(found),
            "scripts_total": len(required_scripts),
            "missing": missing if missing else None
        }

        if missing:
            self.results["errors"].append(f"Missing scripts: {', '.join(missing)}")

        self.results["checks"]["scripts"] = check
        return check["status"] == "pass"

    def check_documentation(self) -> bool:
        """Check if all documentation files exist"""
        required_docs = [
            "README.md",
            "GETTING_STARTED.md",
            "QUICK_START.md",
            "AUTOMATION_COMPLETE.md",
            "AUTOMATION_GUIDE.md",
            "FRAMEWORK_COMPLETE.md"
        ]

        found = []
        missing = []

        for doc in required_docs:
            if (self.project_root / doc).exists():
                found.append(doc)
            else:
                missing.append(doc)

        check = {
            "name": "Documentation",
            "status": "pass" if not missing else "warn",
            "docs_found": len(found),
            "docs_total": len(required_docs),
            "missing": missing if missing else None
        }

        if missing:
            self.results["warnings"].append(f"Missing docs: {', '.join(missing)}")
            self.results["recommendations"].append("Review documentation in root directory")

        self.results["checks"]["documentation"] = check
        return check["status"] != "fail"

    def check_identity_profile(self) -> bool:
        """Check if identity profile exists"""
        profile_file = self.project_root / "intel" / "identity_profile.json"
        template_file = self.project_root / "intel" / "identity_profile_template.json"

        has_profile = profile_file.exists()
        has_template = template_file.exists()

        status = "pass" if has_profile else "warn" if has_template else "fail"

        check = {
            "name": "Identity Profile",
            "status": status,
            "profile_exists": has_profile,
            "template_exists": has_template
        }

        if not has_profile:
            self.results["warnings"].append("Identity profile not configured")
            self.results["recommendations"].append(
                "Create identity profile: cp intel/identity_profile_template.json intel/identity_profile.json"
            )

        self.results["checks"]["identity_profile"] = check
        return status != "fail"

    def check_git_setup(self) -> bool:
        """Check if git repository is configured"""
        git_dir = self.project_root / ".git"

        check = {
            "name": "Git Repository",
            "status": "pass" if git_dir.exists() else "warn",
            "configured": git_dir.exists()
        }

        if not git_dir.exists():
            self.results["warnings"].append("Not a git repository")

        self.results["checks"]["git"] = check
        return check["status"] != "fail"

    def check_github_actions(self) -> bool:
        """Check if GitHub Actions workflows are configured"""
        workflows_dir = self.project_root / ".github" / "workflows"

        required_workflows = [
            "daily-monitoring.yml",
            "testing.yml"
        ]

        found = []
        missing = []

        if workflows_dir.exists():
            for workflow in required_workflows:
                if (workflows_dir / workflow).exists():
                    found.append(workflow)
                else:
                    missing.append(workflow)
        else:
            missing = required_workflows

        check = {
            "name": "GitHub Actions",
            "status": "pass" if not missing else "warn",
            "workflows_found": len(found),
            "workflows_total": len(required_workflows),
            "missing": missing if missing else None
        }

        if missing:
            self.results["warnings"].append(f"Missing workflows: {', '.join(missing)}")

        self.results["checks"]["github_actions"] = check
        return check["status"] != "fail"

    def test_imports(self) -> bool:
        """Test if all automation tools can be imported"""
        sys.path.insert(0, str(self.project_root / "scripts"))

        tools = [
            "hibp_monitor",
            "gsc_removal_agent",
            "bing_removal_agent",
            "data_broker_automation",
            "monitoring_orchestrator",
            "automation_cli"
        ]

        results = {}
        failed = []

        for tool in tools:
            try:
                __import__(tool)
                results[tool] = "OK"
            except ImportError as e:
                results[tool] = f"FAILED: {str(e)[:50]}"
                failed.append(tool)

        check = {
            "name": "Tool Imports",
            "status": "pass" if not failed else "fail",
            "tools_working": len(tools) - len(failed),
            "tools_total": len(tools),
            "results": results
        }

        if failed:
            self.results["errors"].append(f"Import failures: {', '.join(failed)}")
            self.results["recommendations"].append(
                "Install dependencies: pip install -r scripts/requirements.txt"
            )

        self.results["checks"]["imports"] = check
        return check["status"] == "pass"

    def run_all_checks(self) -> None:
        """Run all diagnostic checks"""
        print("\n" + "="*60)
        print("🔧 Privacy Framework Diagnostic")
        print("="*60 + "\n")

        checks = [
            ("Python Version", self.check_python_version),
            ("Dependencies", self.check_dependencies),
            ("Directory Structure", self.check_directory_structure),
            ("Automation Scripts", self.check_scripts),
            ("Documentation", self.check_documentation),
            ("Identity Profile", self.check_identity_profile),
            ("Git Setup", self.check_git_setup),
            ("GitHub Actions", self.check_github_actions),
            ("Tool Imports", self.test_imports)
        ]

        for check_name, check_func in checks:
            try:
                result = check_func()
                status_emoji = "✓" if result else "⚠"
                print(f"{status_emoji} {check_name}")
            except Exception as e:
                print(f"✗ {check_name}: {str(e)[:50]}")
                self.results["errors"].append(f"{check_name} check failed: {str(e)[:50]}")

    def generate_report(self) -> None:
        """Generate diagnostic report"""
        print("\n" + "="*60)
        print("📊 Diagnostic Summary")
        print("="*60)

        total_checks = len(self.results["checks"])
        passed_checks = sum(1 for c in self.results["checks"].values() if c.get("status") == "pass")
        warned_checks = sum(1 for c in self.results["checks"].values() if c.get("status") == "warn")
        failed_checks = sum(1 for c in self.results["checks"].values() if c.get("status") == "fail")

        print(f"\nChecks: {passed_checks} passed, {warned_checks} warned, {failed_checks} failed")
        print(f"Status: ", end="")

        if failed_checks > 0:
            print("❌ FAILED - Critical issues detected")
        elif warned_checks > 0:
            print("⚠️  WARNING - Some issues detected")
        else:
            print("✅ HEALTHY - All systems operational")

        if self.results["errors"]:
            print(f"\n🔴 Errors ({len(self.results['errors'])}):")
            for error in self.results["errors"]:
                print(f"  - {error}")

        if self.results["warnings"]:
            print(f"\n🟡 Warnings ({len(self.results['warnings'])}):")
            for warning in self.results["warnings"]:
                print(f"  - {warning}")

        if self.results["recommendations"]:
            print(f"\n💡 Recommendations ({len(self.results['recommendations'])}):")
            for rec in self.results["recommendations"]:
                print(f"  - {rec}")

        # Save report
        report_file = self.project_root / "logs" / "diagnostic_report.json"
        report_file.parent.mkdir(parents=True, exist_ok=True)

        with open(report_file, 'w') as f:
            json.dump(self.results, f, indent=2)

        print(f"\n✓ Report saved to logs/diagnostic_report.json")

    def run(self) -> int:
        """Run all diagnostics and return status code"""
        self.run_all_checks()
        self.generate_report()

        # Return status code
        if self.results["errors"]:
            return 1
        elif self.results["warnings"]:
            return 0  # Still operational
        else:
            return 0


if __name__ == "__main__":
    diagnostic = FrameworkDiagnostic()
    exit_code = diagnostic.run()
    sys.exit(exit_code)
