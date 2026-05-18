#!/usr/bin/env python3
"""
Automated Removal Helper
Opens broker removal pages and guides user through submissions
Tracks confirmations and progress
"""

import sys
import json
import webbrowser
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List

sys.path.insert(0, str(Path(__file__).parent))

try:
    from broker_tracker import DataBrokerTracker
except:
    print("Warning: broker_tracker not available")


class RemovalHelper:
    """Guide user through broker removals with automation"""

    def __init__(self, email: str):
        self.email = email
        self.name = email.split("@")[0]
        self.project_root = Path(__file__).parent.parent
        self.tracker = DataBrokerTracker()
        self.submissions = []

        # Broker information with removal URLs
        self.brokers = {
            "truecaller": {
                "name": "TrueCaller",
                "url": "https://www.truecaller.com/unlist",
                "phase": 1,
                "difficulty": "easy",
                "instructions": [
                    "1. Enter your phone number",
                    "2. Verify via SMS (check your phone)",
                    "3. Confirm removal request",
                    "4. You'll get a confirmation - SAVE IT"
                ]
            },
            "whitepages": {
                "name": "White Pages",
                "url": "https://www.whitepages.com/suppression",
                "phase": 2,
                "difficulty": "medium",
                "instructions": [
                    "1. Enter your name and phone/email",
                    "2. Review all listings",
                    "3. Submit removal for each listing",
                    "4. Confirm via email (check inbox)",
                    "5. Save confirmation numbers"
                ]
            },
            "mylife": {
                "name": "MyLife",
                "url": "https://www.mylife.com/privacy",
                "phase": 2,
                "difficulty": "medium",
                "instructions": [
                    "1. Click 'Remove My Profile'",
                    "2. Create account (required)",
                    "3. Find your profile",
                    "4. Verify email and phone",
                    "5. Confirm removal request"
                ]
            },
            "peoplefinder": {
                "name": "PeopleFinder",
                "url": "https://www.peoplefinder.com/removal",
                "phase": 2,
                "difficulty": "medium",
                "instructions": [
                    "1. Find your listing",
                    "2. Click 'Remove this person'",
                    "3. Verify identity",
                    "4. Confirm removal"
                ]
            },
            "familytreenow": {
                "name": "FamilyTreeNow",
                "url": "https://www.familytreenow.com/user/delete",
                "phase": 2,
                "difficulty": "medium",
                "instructions": [
                    "1. Create account (required)",
                    "2. Find your person record",
                    "3. Click 'Remove this person'",
                    "4. Verify via email",
                    "5. Confirm deletion"
                ]
            },
            "zoominfo": {
                "name": "ZoomInfo",
                "url": "https://www.zoominfo.com/d/update-profile",
                "phase": 2,
                "difficulty": "medium",
                "instructions": [
                    "1. Search for your business profile",
                    "2. Click 'Remove Profile'",
                    "3. Provide business verification",
                    "4. Submit removal request"
                ]
            },
            "spokeo": {
                "name": "Spokeo",
                "url": "https://www.spokeo.com/optout",
                "phase": 3,
                "difficulty": "hard",
                "instructions": [
                    "1. Find your listing",
                    "2. Click 'Report' or 'Remove'",
                    "3. Upload photo ID (required)",
                    "4. Submit removal request",
                    "5. Wait for email confirmation"
                ]
            },
            "intelius": {
                "name": "Intelius",
                "url": "https://www.intelius.com/optout",
                "phase": 3,
                "difficulty": "hard",
                "instructions": [
                    "1. Find your profile",
                    "2. Phone verification (they'll call)",
                    "3. Upload government ID photo",
                    "4. May require certified mail letter",
                    "5. Allow 45 days for processing"
                ]
            },
            "ussearch": {
                "name": "US Search",
                "url": "https://www.ussearch.com/privacy",
                "phase": 3,
                "difficulty": "hard",
                "instructions": [
                    "1. Search for your profile",
                    "2. Upload identity document (required)",
                    "3. Verify email",
                    "4. Submit removal request",
                    "5. Wait for confirmation"
                ]
            }
        }

    def print_header(self):
        """Print welcome header"""
        print("\n" + "="*70)
        print("🚀 AUTOMATED REMOVAL HELPER")
        print("="*70)
        print(f"\nEmail: {self.email}")
        print(f"Starting: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    def show_broker(self, broker_id: str):
        """Show broker removal page"""
        if broker_id not in self.brokers:
            print(f"❌ Unknown broker: {broker_id}")
            return

        broker = self.brokers[broker_id]
        print("\n" + "="*70)
        print(f"📍 {broker['name'].upper()}")
        print("="*70)
        print(f"Difficulty: {broker['difficulty'].upper()}")
        print(f"Phase: {broker['phase']}\n")

        print("Steps:")
        for step in broker['instructions']:
            print(f"  {step}")

        print(f"\nOpening removal page...")
        print(f"URL: {broker['url']}\n")

        # Open in browser
        try:
            webbrowser.open(broker['url'])
            print(f"✓ Opened {broker['name']} removal page in browser")
        except Exception as e:
            print(f"⚠️  Could not open browser: {e}")
            print(f"Please visit manually: {broker['url']}")

        return broker

    def log_submission(self, broker_id: str, confirmation: str):
        """Log broker submission"""
        submission = {
            "broker_id": broker_id,
            "broker_name": self.brokers[broker_id]['name'],
            "confirmation_number": confirmation,
            "timestamp": datetime.now().isoformat(),
            "status": "submitted"
        }

        self.submissions.append(submission)

        # Save to tracking file
        tracking_file = self.project_root / "logs" / "removal_submissions.json"
        tracking_file.parent.mkdir(parents=True, exist_ok=True)

        submissions = []
        if tracking_file.exists():
            with open(tracking_file) as f:
                submissions = json.load(f)

        submissions.append(submission)

        with open(tracking_file, 'w') as f:
            json.dump(submissions, f, indent=2)

        print(f"✓ Logged: {self.brokers[broker_id]['name']}")
        print(f"  Confirmation: {confirmation}")

        return submission

    def run_interactive_removal(self):
        """Run interactive removal wizard"""
        self.print_header()

        phases = {
            1: "EASY REMOVALS (Week 1)",
            2: "MEDIUM REMOVALS (Weeks 2-4)",
            3: "HARD REMOVALS (Weeks 4+)"
        }

        current_phase = 1
        completed = []

        while True:
            print(f"\n{'='*70}")
            print(f"📋 {phases[current_phase]}")
            print(f"{'='*70}\n")

            # Get brokers for this phase
            phase_brokers = {
                bid: b for bid, b in self.brokers.items()
                if b['phase'] == current_phase
            }

            for i, (broker_id, broker) in enumerate(phase_brokers.items(), 1):
                status = "✓ DONE" if broker_id in completed else "⏳ TODO"
                print(f"{i}. {status:10} {broker['name']}")

            print(f"\nOptions:")
            print("  [1-{0}] Submit removal for broker".format(len(phase_brokers)))
            print("  [N] Next phase")
            print("  [P] Previous phase")
            print("  [S] Summary")
            print("  [Q] Quit")
            print()

            choice = input("Choose option: ").strip().lower()

            if choice == 'q':
                print("\n✓ Removal helper closed")
                self.show_summary(completed)
                break
            elif choice == 'n':
                if current_phase < 3:
                    current_phase += 1
                else:
                    print("⚠️  Already at final phase")
            elif choice == 'p':
                if current_phase > 1:
                    current_phase -= 1
                else:
                    print("⚠️  Already at first phase")
            elif choice == 's':
                self.show_summary(completed)
            elif choice.isdigit():
                idx = int(choice) - 1
                broker_list = list(phase_brokers.items())
                if 0 <= idx < len(broker_list):
                    broker_id, broker = broker_list[idx]
                    self.process_broker(broker_id, broker, completed)

    def process_broker(self, broker_id: str, broker: dict, completed: list):
        """Process single broker removal"""
        print(f"\n{'='*70}")
        print(f"📍 {broker['name']}")
        print(f"{'='*70}\n")

        # Show instructions
        print("Instructions:")
        for step in broker['instructions']:
            print(f"  {step}")

        print(f"\nNow opening {broker['name']} removal page...")
        print(f"URL: {broker['url']}\n")

        # Open browser
        try:
            webbrowser.open(broker['url'])
            print(f"✓ Opened in browser\n")
        except:
            print(f"❌ Could not open browser")
            print(f"Please visit: {broker['url']}\n")

        # Wait for user to complete
        print("Complete the removal process in the browser window.")
        print("Then come back here and enter your confirmation number.\n")

        confirmation = input("Confirmation number (or 'skip'): ").strip()

        if confirmation.lower() == 'skip':
            print("⏭️  Skipped")
            return

        if confirmation:
            self.log_submission(broker_id, confirmation)
            completed.append(broker_id)
            print(f"✓ {broker['name']} removal logged!")
            print(f"✓ Progress: {len(completed)} brokers processed\n")

            # Show estimated completion time
            if len(completed) > 0:
                print(f"Estimated removals complete:")
                if broker_id == "truecaller":
                    print("  → TrueCaller: 7 days")
                elif broker['phase'] == 2:
                    print("  → Medium brokers: 14-30 days")
                else:
                    print("  → Hard brokers: 21-45 days")

    def show_summary(self, completed: list):
        """Show completion summary"""
        print("\n" + "="*70)
        print("📊 REMOVAL PROGRESS SUMMARY")
        print("="*70)

        total = len(self.brokers)
        done = len(completed)
        percent = (done / total * 100) if total > 0 else 0

        print(f"\nCompleted: {done}/{total} ({percent:.0f}%)")
        print(f"Remaining: {total - done}")

        if completed:
            print(f"\nCompleted Brokers:")
            for broker_id in completed:
                broker = self.brokers[broker_id]
                print(f"  ✓ {broker['name']} (Phase {broker['phase']})")

        print(f"\nTimeline:")
        print(f"  Phase 1: ~7 days")
        print(f"  Phase 2: ~14-30 days")
        print(f"  Phase 3: ~21-45 days")
        print(f"  TOTAL: ~4-6 weeks")

        print(f"\nWhat to do now:")
        if done == 0:
            print(f"  → Start with Phase 1 (easiest: TrueCaller)")
        elif done < 6:
            print(f"  → Continue with Phase 2 brokers")
        else:
            print(f"  → Move to Phase 3 (requires ID verification)")

        print(f"\nMonitor removals:")
        print(f"  → Check email for confirmations")
        print(f"  → Google your name in 1-2 weeks")
        print(f"  → Verify removal completion on broker sites")

    def run(self):
        """Run removal helper"""
        self.run_interactive_removal()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        email = sys.argv[1]
    else:
        email = input("Enter your email address: ").strip()
        if not email:
            print("❌ Email required")
            sys.exit(1)

    helper = RemovalHelper(email)
    helper.run()
