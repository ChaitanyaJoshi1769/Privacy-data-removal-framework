#!/usr/bin/env python3
"""
Privacy Framework Initialization Script
One-command setup for new users
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime


class PrivacyFrameworkSetup:
    """Setup and initialize the privacy framework"""

    def __init__(self):
        self.project_root = Path(__file__).parent
        self.script_dir = self.project_root / "scripts"
        self.logs_dir = self.project_root / "logs"
        self.intel_dir = self.project_root / "intel"

    def create_directories(self) -> None:
        """Create necessary directories"""
        print("📁 Creating directories...")
        directories = [
            self.logs_dir,
            self.intel_dir,
            self.project_root / "removal",
            self.project_root / "discovery",
            self.project_root / "exposures",
            self.project_root / "suppression",
            self.project_root / "hardening",
            self.project_root / "monitoring",
        ]

        for directory in directories:
            directory.mkdir(exist_ok=True)
            print(f"  ✓ {directory.relative_to(self.project_root)}")

    def install_dependencies(self) -> None:
        """Install Python dependencies"""
        print("\n📦 Installing dependencies...")
        requirements_file = self.script_dir / "requirements.txt"

        if not requirements_file.exists():
            print("  ⚠️  requirements.txt not found")
            return

        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", "-r",
                str(requirements_file)
            ])
            print("  ✓ Dependencies installed")
        except subprocess.CalledProcessError as e:
            print(f"  ⚠️  Error installing dependencies: {e}")
            print("  Try: pip install -r scripts/requirements.txt")

    def create_identity_template(self) -> None:
        """Create identity profile template"""
        print("\n👤 Creating identity profile template...")
        identity_file = self.intel_dir / "identity_profile_template.json"

        template = {
            "name": "Your Name",
            "email": "your@email.com",
            "phone": "+1-XXX-XXX-XXXX",
            "github_username": "your-github-user",
            "domain": "example.com",
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "notes": "Edit this file with your information, then save as identity_profile.json"
        }

        with open(identity_file, 'w') as f:
            json.dump(template, f, indent=2)

        print(f"  ✓ Template created: intel/identity_profile_template.json")
        print("  📝 Edit this file with your information")

    def create_config_template(self) -> None:
        """Create configuration template"""
        print("\n⚙️  Creating configuration template...")
        config_file = self.project_root / ".privacy-config.json"

        config = {
            "version": "2.0",
            "user": {
                "email": "",
                "name": ""
            },
            "monitoring": {
                "daily_checks_enabled": True,
                "weekly_checks_enabled": True,
                "monthly_checks_enabled": True,
                "alert_email": ""
            },
            "removal": {
                "auto_track": True,
                "enable_notifications": True,
                "removal_brokers": [
                    "spokeo", "whitepages", "intelius", "mylife",
                    "truecaller", "peoplefinder", "ussearch",
                    "familytreenow", "zoominfo"
                ]
            },
            "privacy_hardening": {
                "level": "basic",
                "enable_vpn": False,
                "enable_2fa": True
            }
        }

        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)

        print(f"  ✓ Config template created: .privacy-config.json")
        print("  📝 Edit configuration as needed")

    def test_imports(self) -> None:
        """Test that all automation tools can be imported"""
        print("\n🧪 Testing automation tools...")

        tools = [
            "hibp_monitor",
            "gsc_removal_agent",
            "bing_removal_agent",
            "data_broker_automation",
            "monitoring_orchestrator",
            "broker_tracker",
            "exposure_scanner",
            "privacy_audit",
            "progress_reporter",
            "dashboard_server",
            "automation_cli"
        ]

        sys.path.insert(0, str(self.script_dir))
        failed = []

        for tool in tools:
            try:
                __import__(tool)
                print(f"  ✓ {tool}")
            except ImportError as e:
                # Some tools may fail if dependencies aren't installed
                print(f"  ⚠️  {tool} - {str(e)[:50]}")
                failed.append(tool)

        if failed:
            print(f"\n⚠️  {len(failed)} tools have import issues")
        else:
            print("\n✓ All automation tools ready!")

    def create_quick_start_guide(self) -> None:
        """Create quick start guide"""
        print("\n📖 Creating quick start guide...")
        guide_file = self.project_root / "QUICK_START.md"

        guide = """# Quick Start Guide

## 1. Initialize Framework (Done!)
```bash
python3 init.py
```

## 2. Edit Your Identity (First Time)
```bash
# Copy and edit the template
cp intel/identity_profile_template.json intel/identity_profile.json
# Edit with your information
```

## 3. Check for Breaches
```bash
python3 scripts/automation_cli.py monitor --check hibp --email your@email.com
```

## 4. Generate Removal Plan
```bash
python3 scripts/automation_cli.py removal --plan
```

## 5. View Results
```bash
cat logs/broker_summary.json
```

## 6. View Dashboard
```bash
python3 scripts/dashboard_server.py serve
# Open http://localhost:8000 in browser
```

## All Available Commands

### Monitoring
```bash
python3 scripts/automation_cli.py monitor --check hibp --email your@email.com
python3 scripts/automation_cli.py monitor --check all
python3 scripts/automation_cli.py monitor --check search
python3 scripts/automation_cli.py monitor --check archive
```

### Data Broker Removal
```bash
python3 scripts/automation_cli.py removal --list
python3 scripts/automation_cli.py removal --plan
python3 scripts/automation_cli.py removal --search
```

### Search De-indexing
```bash
python3 scripts/automation_cli.py deindex --provider google
python3 scripts/automation_cli.py deindex --provider bing
python3 scripts/automation_cli.py deindex --provider both
```

### Privacy Auditing
```bash
python3 scripts/automation_cli.py audit --type github
python3 scripts/automation_cli.py audit --type search
python3 scripts/automation_cli.py audit --type all --full
```

### Progress Reporting
```bash
python3 scripts/automation_cli.py report --type progress --period weekly
python3 scripts/automation_cli.py report --type monitoring
python3 scripts/automation_cli.py report --type summary
```

### Dashboard
```bash
python3 scripts/dashboard_server.py save     # Save as HTML
python3 scripts/dashboard_server.py serve    # Serve via HTTP
```

## Important Files
- **AUTOMATION_COMPLETE.md** - Full implementation guide
- **AUTOMATION_GUIDE.md** - Complete tool reference
- **EXECUTION_GUIDE.md** - Week-by-week procedures
- **OPERATIONAL_SUMMARY.md** - Deep reference

## Getting Help
```bash
python3 scripts/automation_cli.py help
```

## 4-Week Execution Plan

### Week 1: Discovery & Planning
- Run audit: `python3 scripts/automation_cli.py audit --type all --full`
- Generate removal plan: `python3 scripts/automation_cli.py removal --plan`

### Week 2: Easy Removals
- Execute TrueCaller removal (easiest broker)
- Track in: `logs/broker_tracking.json`

### Week 3: Medium Removals
- Execute WhitePages, MyLife, PeopleFinder, etc.
- Submit search removal requests

### Week 4: Difficult Removals & Verification
- Execute Spokeo, Intelius, US Search
- Verify all removals

## Output Files
All results are saved to `logs/`:
- `hibp_breaches.json` - Breach check results
- `broker_summary.json` - Removal status summary
- `broker_tracking.json` - Detailed tracking
- `gsc_removal_plan.json` - Google removal plan
- `bing_removal_summary.json` - Bing removal status
- `monitoring_report.json` - Monitoring status
- `dashboard.json` - Dashboard data

## Support
Questions? Check:
1. QUICK_START.md (this file)
2. AUTOMATION_GUIDE.md
3. AUTOMATION_COMPLETE.md
4. Run: `python3 scripts/automation_cli.py help`
"""

        with open(guide_file, 'w') as f:
            f.write(guide)

        print(f"  ✓ Quick start guide created: QUICK_START.md")

    def show_next_steps(self) -> None:
        """Show next steps for user"""
        print("\n" + "="*60)
        print("✅ INITIALIZATION COMPLETE!")
        print("="*60)

        next_steps = """
🚀 Next Steps:

1. 📝 Set up your identity profile:
   cp intel/identity_profile_template.json intel/identity_profile.json
   # Edit the file with your information

2. 🔍 Run your first check:
   python3 scripts/automation_cli.py monitor --check hibp --email your@email.com

3. 📋 Generate removal plan:
   python3 scripts/automation_cli.py removal --plan

4. 📊 View dashboard:
   python3 scripts/dashboard_server.py serve
   # Open http://localhost:8000 in your browser

5. 📖 Read the guides:
   cat QUICK_START.md              # Quick commands
   cat AUTOMATION_COMPLETE.md      # Full guide (START HERE)
   cat AUTOMATION_GUIDE.md         # Tool reference
   cat EXECUTION_GUIDE.md          # Step-by-step

📚 Documentation Structure:
   AUTOMATION_COMPLETE.md - Start here! Overview & quick start
   AUTOMATION_GUIDE.md - Tool reference with examples
   QUICK_START.md - Command cheat sheet
   EXECUTION_GUIDE.md - Week-by-week execution plan
   OPERATIONAL_SUMMARY.md - Complete reference (3500+ lines)

💡 Pro Tips:
   - All output goes to logs/ directory
   - Use 'logs/broker_summary.json' to track progress
   - Dashboard auto-refreshes every 60 seconds
   - Run 'python3 scripts/automation_cli.py help' for all commands

✨ You're ready! Start with:
   python3 scripts/automation_cli.py monitor --check hibp --email your@email.com
"""
        print(next_steps)

    def run(self) -> None:
        """Run complete setup"""
        print("\n" + "="*60)
        print("🔐 Privacy Data Removal Framework")
        print("Initialization Script")
        print("="*60)

        try:
            self.create_directories()
            self.install_dependencies()
            self.create_identity_template()
            self.create_config_template()
            self.test_imports()
            self.create_quick_start_guide()
            self.show_next_steps()

            print("\n✓ Setup complete! Ready to use the framework.\n")

        except Exception as e:
            print(f"\n❌ Setup error: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)


if __name__ == "__main__":
    setup = PrivacyFrameworkSetup()
    setup.run()
