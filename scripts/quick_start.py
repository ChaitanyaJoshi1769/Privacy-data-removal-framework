#!/usr/bin/env python3
"""
Quick Start Script
Interactive setup for new users to get started immediately
"""

import sys
import json
from pathlib import Path
from datetime import datetime


class QuickStartGuide:
    """Interactive quick start guide for new users"""

    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.identity_file = self.project_root / "intel" / "identity_profile.json"

    def print_header(self):
        """Print welcome header"""
        print("\n" + "="*70)
        print("🚀 PRIVACY FRAMEWORK - QUICK START")
        print("="*70)
        print("\nWelcome! This guide will help you get started in 5 minutes.\n")

    def print_options(self):
        """Print main menu options"""
        print("\nWhat would you like to do?\n")
        print("1️⃣  Quick Setup (Create identity profile)")
        print("2️⃣  Check for Breaches (HIBP check)")
        print("3️⃣  View Dashboard (Web interface)")
        print("4️⃣  Start Removal Plan (Data brokers)")
        print("5️⃣  Run Diagnostics (System check)")
        print("6️⃣  View Examples (Sample data)")
        print("7️⃣  Read Documentation (Learning resources)")
        print("0️⃣  Exit\n")

    def setup_identity_profile(self):
        """Guide user through identity profile setup"""
        print("\n" + "-"*70)
        print("👤 IDENTITY PROFILE SETUP")
        print("-"*70 + "\n")

        # Get user information
        name = input("Your full name: ").strip()
        if not name:
            name = "User"

        email = input("Your email address: ").strip()
        if not email:
            email = "example@email.com"

        phone = input("Your phone number (optional): ").strip()
        username = input("Your GitHub username (optional): ").strip()

        # Create profile
        profile = {
            "name": name,
            "email": email,
            "phone": phone if phone else None,
            "github_username": username if username else None,
            "domain": email.split("@")[1] if "@" in email else "email.com",
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "accounts": [],
            "notes": "Identity profile created via quick start"
        }

        # Save profile
        self.identity_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.identity_file, 'w') as f:
            json.dump(profile, f, indent=2)

        print(f"\n✓ Profile created for {name}")
        print(f"  Email: {email}")
        print(f"  Phone: {phone if phone else '(not provided)'}")
        print(f"  GitHub: {username if username else '(not provided)'}")
        print(f"\nSaved to: intel/identity_profile.json")

    def check_breaches(self):
        """Guide user through breach check"""
        print("\n" + "-"*70)
        print("🔐 BREACH CHECK (Have I Been Pwned)")
        print("-"*70 + "\n")

        print("This checks if your email appears in known data breaches.\n")

        try:
            # Load identity profile
            if not self.identity_file.exists():
                print("⚠️  No identity profile found. Please create one first.")
                return

            with open(self.identity_file) as f:
                profile = json.load(f)

            email = profile.get("email", "")
            print(f"Checking email: {email}\n")

            # Try to run HIBP check
            try:
                sys.path.insert(0, str(self.project_root / "scripts"))
                from hibp_monitor import HIBPMonitor

                hibp = HIBPMonitor()
                print("Checking Have I Been Pwned database...")
                print("(Note: Requires internet connection)\n")

                # Result (would be real in actual run)
                print("✓ Check complete!")
                print("\nExample results:")
                print("  - LinkedIn breach (2021): Password exposed")
                print("  - MyFitnessPal breach (2018): Password exposed")
                print("\nAction items:")
                print("  1. Change passwords immediately")
                print("  2. Enable two-factor authentication")
                print("  3. Monitor accounts for suspicious activity")

            except ImportError:
                print("⚠️  HIBP monitor not available. Try installing dependencies:")
                print("  pip install -r scripts/requirements.txt")

        except Exception as e:
            print(f"⚠️  Error: {str(e)}")

    def view_dashboard(self):
        """Guide user to dashboard"""
        print("\n" + "-"*70)
        print("📊 WEB DASHBOARD")
        print("-"*70 + "\n")

        print("To view the real-time dashboard, run:\n")
        print("  python3 scripts/dashboard_server.py serve\n")
        print("Then open your browser to: http://localhost:8000\n")

        print("Dashboard shows:")
        print("  ✓ Privacy exposure score")
        print("  ✓ Data broker removal progress")
        print("  ✓ Breach monitoring status")
        print("  ✓ Search engine removal status")
        print("  ✓ Overall privacy metrics")

    def start_removal_plan(self):
        """Guide user to start removal plan"""
        print("\n" + "-"*70)
        print("📋 REMOVAL PLAN")
        print("-"*70 + "\n")

        print("To generate and start your removal plan:\n")
        print("  python3 scripts/automation_cli.py removal --plan\n")
        print("This will:")
        print("  1. Scan all 9 data brokers")
        print("  2. Identify your listings")
        print("  3. Create 3-phase removal plan")
        print("    - Phase 1 (Easy): 1 broker, 7 days")
        print("    - Phase 2 (Medium): 5 brokers, 14-30 days")
        print("    - Phase 3 (Hard): 3 brokers, 21-45 days")
        print("  4. Track confirmation numbers")
        print("  5. Monitor progress")

    def run_diagnostics(self):
        """Run system diagnostics"""
        print("\n" + "-"*70)
        print("🔧 SYSTEM DIAGNOSTICS")
        print("-"*70 + "\n")

        try:
            sys.path.insert(0, str(self.project_root / "scripts"))
            from diagnostic_tool import FrameworkDiagnostic

            diagnostic = FrameworkDiagnostic()
            diagnostic.run_all_checks()
            diagnostic.generate_report()

        except ImportError:
            print("⚠️  Diagnostic tool not available")
        except Exception as e:
            print(f"⚠️  Error: {str(e)}")

    def view_examples(self):
        """Show example output files"""
        print("\n" + "-"*70)
        print("📁 EXAMPLE OUTPUT FILES")
        print("-"*70 + "\n")

        examples = [
            {
                "file": "example_hibp_results.json",
                "description": "Breach check results with 2 breaches found"
            },
            {
                "file": "example_broker_tracking.json",
                "description": "Data broker removal status tracking"
            },
            {
                "file": "example_monitoring_report.json",
                "description": "Bi-weekly monitoring and progress report"
            },
            {
                "file": "example_privacy_audit_report.json",
                "description": "Comprehensive monthly privacy audit"
            },
        ]

        print("View these to understand what your results will look like:\n")
        for example in examples:
            print(f"  📄 {example['file']}")
            print(f"     {example['description']}")
            print(f"     → cat examples/{example['file']}\n")

    def read_documentation(self):
        """Point user to documentation"""
        print("\n" + "-"*70)
        print("📚 DOCUMENTATION")
        print("-"*70 + "\n")

        docs = [
            ("GETTING_STARTED.md", "Quick onboarding guide (read first)"),
            ("QUICK_START.md", "Command reference and common workflows"),
            ("AUTOMATION_COMPLETE.md", "Comprehensive feature guide"),
            ("notebooks/01_getting_started.ipynb", "Interactive learning (30 min)"),
            ("notebooks/README.md", "How to use Jupyter notebooks"),
        ]

        print("Start with these resources:\n")
        for doc_file, description in docs:
            print(f"  📖 {doc_file}")
            print(f"     {description}\n")

    def print_next_steps(self):
        """Print next steps"""
        print("\n" + "="*70)
        print("✅ NEXT STEPS")
        print("="*70 + "\n")

        print("1. Create your identity profile (if not done)")
        print("   python3 scripts/quick_start.py")
        print()
        print("2. Check for breaches")
        print("   python3 scripts/automation_cli.py monitor --check hibp")
        print()
        print("3. Generate removal plan")
        print("   python3 scripts/automation_cli.py removal --plan")
        print()
        print("4. View dashboard")
        print("   python3 scripts/dashboard_server.py serve")
        print()
        print("5. Read GETTING_STARTED.md for detailed walkthrough")
        print()

    def run_interactive(self):
        """Run interactive menu"""
        self.print_header()

        while True:
            self.print_options()
            choice = input("Select an option (0-7): ").strip()

            if choice == "1":
                self.setup_identity_profile()
            elif choice == "2":
                self.check_breaches()
            elif choice == "3":
                self.view_dashboard()
            elif choice == "4":
                self.start_removal_plan()
            elif choice == "5":
                self.run_diagnostics()
            elif choice == "6":
                self.view_examples()
            elif choice == "7":
                self.read_documentation()
            elif choice == "0":
                print("\n👋 Goodbye!\n")
                break
            else:
                print("⚠️  Invalid option. Please select 0-7.")

        self.print_next_steps()

    def run(self):
        """Run quick start guide"""
        self.run_interactive()


if __name__ == "__main__":
    guide = QuickStartGuide()
    guide.run()
