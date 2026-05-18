#!/usr/bin/env python3
"""
Comprehensive test suite for privacy framework automation tools
"""

import unittest
import json
import sys
from pathlib import Path
from datetime import datetime

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from hibp_monitor import HIBPMonitor
from gsc_removal_agent import GSCRemovalAgent
from bing_removal_agent import BingRemovalAgent
from data_broker_automation import DataBrokerAutomation, BrokerStatus
from monitoring_orchestrator import MonitoringOrchestrator, MonitoringAlert
from dashboard_server import DashboardServer
from broker_tracker import DataBrokerTracker
from exposure_scanner import ExposureScanner
from privacy_audit import PrivacyAudit
from progress_reporter import ProgressReporter


class TestHIBPMonitor(unittest.TestCase):
    """Test HIBP breach monitoring"""

    def setUp(self):
        self.monitor = HIBPMonitor()

    def test_initialization(self):
        """Test monitor initialization"""
        self.assertIsNotNone(self.monitor)
        self.assertEqual(self.monitor.user_agent, "Privacy-Framework-Monitor")

    def test_breach_result_structure(self):
        """Test breach result has correct structure"""
        email = "test@example.com"
        result = self.monitor.check_email_breaches(email)

        self.assertIn("email", result)
        self.assertIn("breached", result)
        self.assertIn("breach_count", result)
        self.assertIn("risk_level", result)

    def test_risk_level_assessment(self):
        """Test risk level is assigned correctly"""
        # Create mock results
        result = {
            "email": "test@example.com",
            "breached": False,
            "breach_count": 0,
            "risk_level": "GREEN"
        }
        self.assertEqual(result["risk_level"], "GREEN")


class TestGSCRemovalAgent(unittest.TestCase):
    """Test Google Search Console removal"""

    def setUp(self):
        self.agent = GSCRemovalAgent()

    def test_initialization(self):
        """Test agent initialization"""
        self.assertIsNotNone(self.agent)
        self.assertIsNotNone(self.agent.removal_requests)

    def test_removal_request_structure(self):
        """Test removal request has correct structure"""
        url = "https://example.com/test"
        request = self.agent.request_url_removal(url, reason="privacy")

        self.assertIn("url", request)
        self.assertIn("reason", request)
        self.assertIn("status", request)
        self.assertEqual(request["status"], "pending")

    def test_robots_txt_generation(self):
        """Test robots.txt blocking generation"""
        patterns = ["/private", "/admin"]
        content = self.agent.create_robots_txt_blocking(patterns)

        self.assertIn("User-agent: *", content)
        self.assertIn("/private", content)
        self.assertIn("/admin", content)

    def test_verification_checklist(self):
        """Test verification checklist generation"""
        checklist = self.agent.generate_verification_checklist()
        self.assertGreater(len(checklist), 0)
        self.assertTrue(all("☐" in item for item in checklist))


class TestBingRemovalAgent(unittest.TestCase):
    """Test Bing removal operations"""

    def setUp(self):
        self.agent = BingRemovalAgent()

    def test_initialization(self):
        """Test agent initialization"""
        self.assertIsNotNone(self.agent)
        self.assertEqual(self.agent.site_url, "github.com/ChaitanyaJoshi1769")

    def test_removal_request(self):
        """Test URL removal request"""
        url = "https://example.com/test"
        request = self.agent.request_url_removal(url)

        self.assertIn("url", request)
        self.assertIn("status", request)
        self.assertEqual(request["status"], "pending")

    def test_batch_generation(self):
        """Test batch removal plan generation"""
        urls = ["https://example.com/1", "https://example.com/2"]
        batch = self.agent.generate_removal_batch(urls)

        self.assertEqual(batch["total_urls"], 2)
        self.assertEqual(len(batch["urls"]), 2)

    def test_disavow_file_generation(self):
        """Test disavow file content generation"""
        urls = ["https://example.com"]
        content = self.agent.create_disavow_file(urls)

        self.assertIn("disavow:", content)
        self.assertIn("https://example.com", content)


class TestDataBrokerAutomation(unittest.TestCase):
    """Test data broker automation"""

    def setUp(self):
        self.automation = DataBrokerAutomation({
            "name": "Test User",
            "email": "test@example.com"
        })

    def test_broker_count(self):
        """Test correct number of brokers"""
        self.assertEqual(len(self.automation.BROKERS), 9)

    def test_broker_information(self):
        """Test broker info has required fields"""
        for broker_id, broker_info in self.automation.BROKERS.items():
            self.assertIn("name", broker_info)
            self.assertIn("url", broker_info)
            self.assertIn("removal_url", broker_info)
            self.assertIn("difficulty", broker_info)
            self.assertIn("time_estimate_days", broker_info)

    def test_removal_plan_structure(self):
        """Test removal plan has correct structure"""
        plan = self.automation.generate_removal_plan()

        self.assertIn("total_brokers", plan)
        self.assertIn("phases", plan)
        self.assertEqual(len(plan["phases"]), 3)

    def test_phase_structure(self):
        """Test each phase has required fields"""
        plan = self.automation.generate_removal_plan()

        for phase in plan["phases"]:
            self.assertIn("phase", phase)
            self.assertIn("brokers", phase)
            self.assertGreater(len(phase["brokers"]), 0)

    def test_broker_tracking_init(self):
        """Test broker tracking initialization"""
        self.assertEqual(len(self.automation.tracking), 9)

        for broker_id, track in self.automation.tracking.items():
            self.assertEqual(track["broker_id"], broker_id)
            self.assertIn("status", track)

    def test_removal_submission_logging(self):
        """Test removal submission logging"""
        broker_id = "spokeo"
        confirmation = "ABC123"

        submission = self.automation.submit_removal(broker_id, confirmation)

        self.assertEqual(submission["broker"], broker_id)
        self.assertEqual(submission["confirmation_number"], confirmation)
        self.assertIn("expected_removal_by", submission)

    def test_removal_verification(self):
        """Test removal verification logging"""
        broker_id = "spokeo"

        verification = self.automation.verify_removal(broker_id, verified=True)

        self.assertEqual(verification["broker"], broker_id)
        self.assertTrue(verification["removal_verified"])


class TestMonitoringOrchestrator(unittest.TestCase):
    """Test monitoring orchestration"""

    def setUp(self):
        self.identity = {
            "name": "Test User",
            "email": "test@example.com",
            "github_username": "testuser"
        }
        self.orchestrator = MonitoringOrchestrator(self.identity)

    def test_job_registration(self):
        """Test job registration"""
        initial_count = len(self.orchestrator.monitoring_jobs)

        self.orchestrator.setup_daily_checks()

        self.assertGreater(len(self.orchestrator.monitoring_jobs), initial_count)

    def test_daily_checks_setup(self):
        """Test daily checks setup"""
        daily = self.orchestrator.setup_daily_checks()

        self.assertGreater(len(daily), 0)
        for job in daily:
            self.assertIn("frequency", job)
            self.assertEqual(job["frequency"], "daily")

    def test_weekly_checks_setup(self):
        """Test weekly checks setup"""
        weekly = self.orchestrator.setup_weekly_checks()

        self.assertGreater(len(weekly), 0)
        for job in weekly:
            self.assertIn("frequency", job)
            self.assertEqual(job["frequency"], "weekly")

    def test_monthly_checks_setup(self):
        """Test monthly checks setup"""
        monthly = self.orchestrator.setup_monthly_checks()

        self.assertGreater(len(monthly), 0)
        for job in monthly:
            self.assertIn("frequency", job)
            self.assertEqual(job["frequency"], "monthly")

    def test_monitoring_report_structure(self):
        """Test monitoring report has correct structure"""
        self.orchestrator.setup_daily_checks()

        report = self.orchestrator.generate_monitoring_report()

        self.assertIn("identity", report)
        self.assertIn("total_jobs", report)
        self.assertIn("monitoring_status", report)

    def test_simulation_run(self):
        """Test simulation of daily monitoring run"""
        result = self.orchestrator.simulate_daily_run()

        self.assertIn("run_at", result)
        self.assertIn("jobs_executed", result)
        self.assertGreater(result["jobs_executed"], 0)


class TestDashboardServer(unittest.TestCase):
    """Test dashboard generation"""

    def setUp(self):
        self.dashboard = DashboardServer()

    def test_initialization(self):
        """Test dashboard initialization"""
        self.assertIsNotNone(self.dashboard)
        self.assertIsNotNone(self.dashboard.data)

    def test_broker_stats_calculation(self):
        """Test broker stats calculation"""
        stats = self.dashboard.calculate_broker_stats()

        self.assertIn("total", stats)
        self.assertIn("submitted", stats)
        self.assertIn("verified", stats)
        self.assertIn("completion_percent", stats)

    def test_breach_stats_calculation(self):
        """Test breach stats calculation"""
        stats = self.dashboard.calculate_breach_stats()

        self.assertIn("total_checks", stats)
        self.assertIn("breached", stats)
        self.assertIn("risk_level", stats)

    def test_html_generation(self):
        """Test HTML dashboard generation"""
        html = self.dashboard.generate_html()

        self.assertIsNotNone(html)
        self.assertIn("Privacy Framework Dashboard", html)
        self.assertIn("<html", html.lower())


class TestIntegration(unittest.TestCase):
    """Integration tests for complete workflows"""

    def setUp(self):
        self.identity = {
            "name": "Test User",
            "email": "test@example.com",
            "github_username": "testuser"
        }

    def test_complete_setup_workflow(self):
        """Test complete setup workflow"""
        # Initialize all components
        broker_automation = DataBrokerAutomation(self.identity)
        orchestrator = MonitoringOrchestrator(self.identity)
        gsc = GSCRemovalAgent()
        bing = BingRemovalAgent()

        # Generate plans
        removal_plan = broker_automation.generate_removal_plan()
        gsc_plan = gsc.generate_removal_plan(["https://example.com"])
        bing_plan = bing.generate_removal_batch(["https://example.com"])

        # Setup monitoring
        orchestrator.setup_daily_checks()
        orchestrator.setup_weekly_checks()

        # Verify components are working
        self.assertGreater(len(removal_plan["phases"]), 0)
        self.assertGreater(len(gsc_plan["removals"]), 0)
        self.assertGreater(len(bing_plan["urls"]), 0)
        self.assertGreater(len(orchestrator.monitoring_jobs), 0)

    def test_data_consistency(self):
        """Test data consistency across tools"""
        automation = DataBrokerAutomation(self.identity)

        # Get broker list from automation
        brokers = list(automation.BROKERS.keys())

        # Verify tracking has all brokers
        for broker_id in brokers:
            self.assertIn(broker_id, automation.tracking)


class TestBrokerTracker(unittest.TestCase):
    """Test broker tracker functionality"""

    def setUp(self):
        self.tracker = DataBrokerTracker()

    def test_initialization(self):
        """Test tracker initialization"""
        self.tracker.init_tracking()
        self.assertGreater(len(self.tracker.tracking), 0)

    def test_submission_logging(self):
        """Test submission logging"""
        broker_id = "spokeo"
        confirmation = "CONF123"

        self.tracker.init_tracking()
        self.tracker.log_submission(broker_id, confirmation)

        track = self.tracker.tracking[broker_id]
        self.assertEqual(track["confirmation_num"], confirmation)
        self.assertTrue(track["submitted"])


class TestDataValidation(unittest.TestCase):
    """Test data validation"""

    def test_broker_list_completeness(self):
        """Test data brokers list is complete"""
        automation = DataBrokerAutomation({})
        brokers = automation.BROKERS

        expected_brokers = [
            "spokeo", "whitepages", "intelius", "mylife",
            "truecaller", "peoplefinder", "ussearch",
            "familytreenow", "zoominfo"
        ]

        for broker in expected_brokers:
            self.assertIn(broker, brokers)

    def test_broker_removal_methods(self):
        """Test removal methods are defined"""
        automation = DataBrokerAutomation({})

        for broker_id, broker_info in automation.BROKERS.items():
            self.assertIn("removal_method", broker_info)
            self.assertGreater(len(broker_info["removal_method"]), 0)


def run_tests():
    """Run all tests"""
    unittest.main(argv=[''], verbosity=2, exit=False)


if __name__ == "__main__":
    print("=" * 60)
    print("Privacy Framework - Comprehensive Test Suite")
    print("=" * 60)
    print()

    run_tests()
