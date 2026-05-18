#!/usr/bin/env python3
"""
Removal Submission Dashboard
Real-time tracking of removal submissions and progress
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List

sys.path.insert(0, str(Path(__file__).parent))


class RemovalDashboard:
    """Track and display removal progress"""

    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.submissions_file = self.project_root / "logs" / "removal_submissions.json"
        self.phases = {
            1: {"name": "Easy", "days": 7, "brokers": ["truecaller"]},
            2: {
                "name": "Medium",
                "days": 30,
                "brokers": ["whitepages", "mylife", "peoplefinder", "familytreenow", "zoominfo"]
            },
            3: {
                "name": "Hard",
                "days": 45,
                "brokers": ["spokeo", "intelius", "ussearch"]
            }
        }

    def load_submissions(self) -> List[Dict]:
        """Load submission data"""
        if not self.submissions_file.exists():
            return []

        with open(self.submissions_file) as f:
            return json.load(f)

    def calculate_stats(self, submissions: List[Dict]) -> Dict:
        """Calculate statistics"""
        total = 9
        submitted = len(submissions)
        remaining = total - submitted

        # Group by phase
        phase_stats = {}
        for phase in [1, 2, 3]:
            phase_brokers = self.phases[phase]["brokers"]
            phase_submitted = len([s for s in submissions if s["broker_id"] in phase_brokers])
            phase_total = len(phase_brokers)
            phase_stats[phase] = {
                "submitted": phase_submitted,
                "total": phase_total,
                "percent": (phase_submitted / phase_total * 100) if phase_total > 0 else 0
            }

        return {
            "total": total,
            "submitted": submitted,
            "remaining": remaining,
            "percent_complete": (submitted / total * 100) if total > 0 else 0,
            "by_phase": phase_stats,
            "submissions": submissions
        }

    def print_dashboard(self):
        """Print dashboard display"""
        submissions = self.load_submissions()
        stats = self.calculate_stats(submissions)

        print("\n" + "="*70)
        print("📊 REMOVAL SUBMISSION DASHBOARD")
        print("="*70)
        print(f"\nLastUpdated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Submissions: {stats['submissions_file'] if 'submissions_file' in stats else self.submissions_file}\n")

        # Overall progress
        print("OVERALL PROGRESS")
        print("-" * 70)
        total = stats["total"]
        submitted = stats["submitted"]
        percent = stats["percent_complete"]

        # Progress bar
        bar_length = 40
        filled = int(bar_length * submitted / total) if total > 0 else 0
        bar = "█" * filled + "░" * (bar_length - filled)
        print(f"{bar} {submitted}/{total} ({percent:.0f}%)")
        print()

        # Phase breakdown
        print("PHASE BREAKDOWN")
        print("-" * 70)
        for phase in [1, 2, 3]:
            phase_data = self.phases[phase]
            phase_stats = stats["by_phase"][phase]
            submitted = phase_stats["submitted"]
            total = phase_stats["total"]
            percent = phase_stats["percent"]

            status = "✓" if submitted == total else "⏳" if submitted > 0 else "○"
            bar_filled = int(15 * submitted / total) if total > 0 else 0
            bar = "█" * bar_filled + "░" * (15 - bar_filled)

            print(f"{status} Phase {phase} ({phase_data['name']:6}) {bar} {submitted}/{total} ({percent:.0f}%)")
            print(f"   Est. completion: ~{phase_data['days']} days")
            print()

        # Submitted brokers
        if submissions:
            print("SUBMITTED BROKERS")
            print("-" * 70)
            for sub in submissions:
                days_ago = (datetime.now() - datetime.fromisoformat(sub["timestamp"])).days
                time_str = f"{days_ago}d ago" if days_ago > 0 else "today"
                print(f"✓ {sub['broker_name']:20} | Conf: {sub['confirmation_number']:20} | {time_str}")
            print()

        # Timeline estimate
        print("TIMELINE ESTIMATE")
        print("-" * 70)
        print(f"Phase 1 (Easy):      ~7 days   (1 broker)")
        print(f"Phase 2 (Medium):    ~30 days  (5 brokers, overlapping)")
        print(f"Phase 3 (Hard):      ~45 days  (3 brokers, may need ID)")
        print(f"TOTAL:               ~4-6 weeks (all phases)")
        print()

        # Next actions
        print("NEXT ACTIONS")
        print("-" * 70)
        if submitted == 0:
            print("→ Start with Phase 1: TrueCaller (easiest, ~10 minutes)")
            print("→ Then move to Phase 2: WhitePages, MyLife, etc.")
        elif submitted < 6:
            print(f"→ Continue Phase 2: {6 - submitted} remaining")
            print("→ Begin Phase 3 prep: Gather ID documents")
        else:
            print("→ Move to Phase 3: Spokeo, Intelius, USSearch")
            print("→ Have photo ID ready for verification")

        print(f"\nMonitoring:")
        print(f"→ Check email for confirmations")
        print(f"→ Save all confirmation numbers")
        print(f"→ Verify removals after ~{self.phases[max([s for s in stats['by_phase'] if stats['by_phase'][s]['submitted'] > 0], default=1)]['days']} days")
        print(f"→ Watch for reappearances (check monthly)")
        print()

    def export_json(self):
        """Export stats to JSON"""
        submissions = self.load_submissions()
        stats = self.calculate_stats(submissions)

        output_file = self.project_root / "logs" / "removal_dashboard.json"
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w') as f:
            json.dump(stats, f, indent=2)

        print(f"✓ Dashboard exported to: {output_file}")

    def run(self):
        """Run dashboard"""
        self.print_dashboard()
        self.export_json()


if __name__ == "__main__":
    dashboard = RemovalDashboard()
    dashboard.run()
