#!/usr/bin/env python3
"""
Performance Benchmarking Suite
Measures execution time and resource usage of framework operations
"""

import sys
import time
import json
from pathlib import Path
from datetime import datetime
from memory_profiler import profile
import timeit

sys.path.insert(0, str(Path(__file__).parent))


class PerformanceBenchmark:
    """Benchmark framework performance"""

    def __init__(self):
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "benchmarks": {},
            "system_info": {},
            "performance_summary": {}
        }
        self.project_root = Path(__file__).parent.parent

    def benchmark_hibp_monitor(self) -> dict:
        """Benchmark HIBP monitor operations"""
        try:
            from hibp_monitor import HIBPMonitor

            hibp = HIBPMonitor()

            # Measure initialization
            start = time.time()
            hibp_instance = HIBPMonitor()
            init_time = time.time() - start

            # Measure mock check (doesn't hit API)
            start = time.time()
            result = hibp.check_breaches_mock("example@email.com")
            check_time = time.time() - start

            return {
                "name": "HIBP Monitor",
                "status": "pass",
                "initialization_ms": round(init_time * 1000, 2),
                "check_operation_ms": round(check_time * 1000, 2),
                "total_time_ms": round((init_time + check_time) * 1000, 2)
            }
        except Exception as e:
            return {
                "name": "HIBP Monitor",
                "status": "error",
                "error": str(e)[:100]
            }

    def benchmark_data_broker_automation(self) -> dict:
        """Benchmark data broker automation"""
        try:
            from data_broker_automation import DataBrokerAutomation

            start = time.time()
            broker_auto = DataBrokerAutomation()
            init_time = time.time() - start

            start = time.time()
            plan = broker_auto.generate_removal_plan()
            plan_time = time.time() - start

            start = time.time()
            summary = broker_auto.get_summary()
            summary_time = time.time() - start

            return {
                "name": "Data Broker Automation",
                "status": "pass",
                "initialization_ms": round(init_time * 1000, 2),
                "plan_generation_ms": round(plan_time * 1000, 2),
                "summary_generation_ms": round(summary_time * 1000, 2),
                "total_time_ms": round((init_time + plan_time + summary_time) * 1000, 2),
                "brokers_processed": len(broker_auto.brokers)
            }
        except Exception as e:
            return {
                "name": "Data Broker Automation",
                "status": "error",
                "error": str(e)[:100]
            }

    def benchmark_gsc_removal(self) -> dict:
        """Benchmark Google Search Console removal"""
        try:
            from gsc_removal_agent import GSCRemovalAgent

            start = time.time()
            gsc = GSCRemovalAgent()
            init_time = time.time() - start

            start = time.time()
            robots = gsc.generate_robots_txt()
            robots_time = time.time() - start

            start = time.time()
            checklist = gsc.get_verification_checklist()
            checklist_time = time.time() - start

            return {
                "name": "GSC Removal Agent",
                "status": "pass",
                "initialization_ms": round(init_time * 1000, 2),
                "robots_generation_ms": round(robots_time * 1000, 2),
                "checklist_generation_ms": round(checklist_time * 1000, 2),
                "total_time_ms": round((init_time + robots_time + checklist_time) * 1000, 2)
            }
        except Exception as e:
            return {
                "name": "GSC Removal Agent",
                "status": "error",
                "error": str(e)[:100]
            }

    def benchmark_bing_removal(self) -> dict:
        """Benchmark Bing removal operations"""
        try:
            from bing_removal_agent import BingRemovalAgent

            start = time.time()
            bing = BingRemovalAgent()
            init_time = time.time() - start

            start = time.time()
            disavow = bing.generate_disavow_file()
            disavow_time = time.time() - start

            start = time.time()
            verification = bing.get_verification_methods()
            verification_time = time.time() - start

            return {
                "name": "Bing Removal Agent",
                "status": "pass",
                "initialization_ms": round(init_time * 1000, 2),
                "disavow_generation_ms": round(disavow_time * 1000, 2),
                "verification_generation_ms": round(verification_time * 1000, 2),
                "total_time_ms": round((init_time + disavow_time + verification_time) * 1000, 2)
            }
        except Exception as e:
            return {
                "name": "Bing Removal Agent",
                "status": "error",
                "error": str(e)[:100]
            }

    def benchmark_monitoring_orchestrator(self) -> dict:
        """Benchmark monitoring orchestrator"""
        try:
            from monitoring_orchestrator import MonitoringOrchestrator

            start = time.time()
            orchestrator = MonitoringOrchestrator()
            init_time = time.time() - start

            start = time.time()
            orchestrator.setup_daily_checks()
            daily_setup_time = time.time() - start

            start = time.time()
            report = orchestrator.generate_monitoring_report()
            report_time = time.time() - start

            return {
                "name": "Monitoring Orchestrator",
                "status": "pass",
                "initialization_ms": round(init_time * 1000, 2),
                "daily_setup_ms": round(daily_setup_time * 1000, 2),
                "report_generation_ms": round(report_time * 1000, 2),
                "total_time_ms": round((init_time + daily_setup_time + report_time) * 1000, 2),
                "jobs_configured": len(orchestrator.jobs)
            }
        except Exception as e:
            return {
                "name": "Monitoring Orchestrator",
                "status": "error",
                "error": str(e)[:100]
            }

    def benchmark_dashboard_server(self) -> dict:
        """Benchmark dashboard server operations"""
        try:
            from dashboard_server import DashboardServer

            start = time.time()
            dashboard = DashboardServer()
            init_time = time.time() - start

            start = time.time()
            stats = dashboard.calculate_broker_stats()
            stats_time = time.time() - start

            start = time.time()
            html = dashboard.generate_html()
            html_time = time.time() - start

            return {
                "name": "Dashboard Server",
                "status": "pass",
                "initialization_ms": round(init_time * 1000, 2),
                "stats_calculation_ms": round(stats_time * 1000, 2),
                "html_generation_ms": round(html_time * 1000, 2),
                "total_time_ms": round((init_time + stats_time + html_time) * 1000, 2),
                "html_size_bytes": len(html) if html else 0
            }
        except Exception as e:
            return {
                "name": "Dashboard Server",
                "status": "error",
                "error": str(e)[:100]
            }

    def benchmark_broker_tracker(self) -> dict:
        """Benchmark broker tracker operations"""
        try:
            from broker_tracker import DataBrokerTracker

            start = time.time()
            tracker = DataBrokerTracker()
            init_time = time.time() - start

            start = time.time()
            tracker.init_tracking()
            init_track_time = time.time() - start

            start = time.time()
            summary = tracker.get_summary()
            summary_time = time.time() - start

            return {
                "name": "Broker Tracker",
                "status": "pass",
                "initialization_ms": round(init_time * 1000, 2),
                "tracking_init_ms": round(init_track_time * 1000, 2),
                "summary_generation_ms": round(summary_time * 1000, 2),
                "total_time_ms": round((init_time + init_track_time + summary_time) * 1000, 2)
            }
        except Exception as e:
            return {
                "name": "Broker Tracker",
                "status": "error",
                "error": str(e)[:100]
            }

    def run_all_benchmarks(self) -> None:
        """Run all performance benchmarks"""
        print("\n" + "="*70)
        print("🏃 PERFORMANCE BENCHMARK SUITE")
        print("="*70 + "\n")

        benchmarks = [
            ("HIBP Monitor", self.benchmark_hibp_monitor),
            ("Data Broker Automation", self.benchmark_data_broker_automation),
            ("GSC Removal Agent", self.benchmark_gsc_removal),
            ("Bing Removal Agent", self.benchmark_bing_removal),
            ("Monitoring Orchestrator", self.benchmark_monitoring_orchestrator),
            ("Dashboard Server", self.benchmark_dashboard_server),
            ("Broker Tracker", self.benchmark_broker_tracker),
        ]

        total_time = 0
        passed = 0
        failed = 0

        for name, benchmark_func in benchmarks:
            try:
                result = benchmark_func()
                self.results["benchmarks"][result["name"]] = result

                if result["status"] == "pass":
                    passed += 1
                    total_ms = result.get("total_time_ms", 0)
                    total_time += total_ms
                    status = "✓"
                    print(f"{status} {name:35} {total_ms:8.2f} ms")
                else:
                    failed += 1
                    print(f"✗ {name:35} ERROR")
            except Exception as e:
                failed += 1
                print(f"✗ {name:35} {str(e)[:40]}")

        # Generate summary
        self.generate_summary(passed, failed, total_time)

    def generate_summary(self, passed: int, failed: int, total_time: float) -> None:
        """Generate benchmark summary"""
        print("\n" + "="*70)
        print("📊 BENCHMARK SUMMARY")
        print("="*70)

        print(f"\nResults: {passed} passed, {failed} failed")
        print(f"Total time: {total_time:.2f} ms ({total_time/1000:.2f} seconds)")
        print(f"Average per tool: {total_time/max(passed, 1):.2f} ms")

        performance_targets = {
            "HIBP Monitor": {"target": 500, "critical": 2000},
            "Data Broker Automation": {"target": 200, "critical": 1000},
            "GSC Removal Agent": {"target": 100, "critical": 500},
            "Bing Removal Agent": {"target": 100, "critical": 500},
            "Monitoring Orchestrator": {"target": 300, "critical": 1500},
            "Dashboard Server": {"target": 200, "critical": 1000},
            "Broker Tracker": {"target": 150, "critical": 500},
        }

        print("\n" + "-"*70)
        print("Performance vs Targets:")
        print("-"*70)

        for tool_name, targets in performance_targets.items():
            if tool_name in self.results["benchmarks"]:
                result = self.results["benchmarks"][tool_name]
                if result["status"] == "pass":
                    actual = result.get("total_time_ms", 0)
                    target = targets["target"]
                    critical = targets["critical"]

                    if actual <= target:
                        status = "🟢 EXCELLENT"
                    elif actual <= critical:
                        status = "🟡 ACCEPTABLE"
                    else:
                        status = "🔴 SLOW"

                    print(f"{status} {tool_name:35} {actual:8.2f}ms (target: {target}ms)")

        self.results["performance_summary"] = {
            "tools_passed": passed,
            "tools_failed": failed,
            "total_time_ms": round(total_time, 2),
            "average_time_ms": round(total_time / max(passed, 1), 2),
            "status": "✅ HEALTHY" if failed == 0 else f"⚠️  {failed} failures"
        }

        # Save results
        self.save_results()

    def save_results(self) -> None:
        """Save benchmark results to file"""
        report_file = self.project_root / "logs" / "performance_benchmark.json"
        report_file.parent.mkdir(parents=True, exist_ok=True)

        with open(report_file, 'w') as f:
            json.dump(self.results, f, indent=2)

        print(f"\n✓ Results saved to logs/performance_benchmark.json")

    def run(self) -> int:
        """Run all benchmarks and return status code"""
        self.run_all_benchmarks()
        return 0 if self.results["performance_summary"].get("tools_failed", 0) == 0 else 1


if __name__ == "__main__":
    benchmark = PerformanceBenchmark()
    exit_code = benchmark.run()
    sys.exit(exit_code)
