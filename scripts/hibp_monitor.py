#!/usr/bin/env python3
"""
Have I Been Pwned (HIBP) Breach Monitoring
Integrates with HIBP API for automated breach detection
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path

class HIBPMonitor:
    """Monitor for data breaches using Have I Been Pwned API"""

    BASE_URL = "https://haveibeenpwned.com/api/v3"

    def __init__(self, user_agent: str = "Privacy-Framework-Monitor"):
        """
        Initialize HIBP monitor

        Args:
            user_agent: Required for HIBP API access
        """
        self.user_agent = user_agent
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": user_agent})
        self.breaches_log = []

    def check_email_breaches(self, email: str) -> Dict:
        """
        Check if email appears in known data breaches

        Args:
            email: Email address to check

        Returns:
            Dict with breach info and risk assessment
        """
        try:
            # Add rate limiting to respect HIBP API limits (1 req per 1.5 seconds)
            time.sleep(1.5)

            url = f"{self.BASE_URL}/breachedaccount/{email}"
            resp = self.session.get(url, timeout=10)

            result = {
                "email": email,
                "checked_at": datetime.now().isoformat(),
                "breached": False,
                "breach_count": 0,
                "breaches": [],
                "risk_level": "GREEN",
                "action_required": False
            }

            if resp.status_code == 200:
                breaches = resp.json()
                result["breached"] = True
                result["breach_count"] = len(breaches)
                result["breaches"] = [{
                    "name": b.get("Name"),
                    "breach_date": b.get("BreachDate"),
                    "data_classes": b.get("DataClasses", []),
                    "is_verified": b.get("IsVerified"),
                    "is_sensitive": b.get("IsSensitive")
                } for b in breaches]

                # Risk assessment
                if len(breaches) > 3:
                    result["risk_level"] = "RED"
                    result["action_required"] = True
                elif len(breaches) > 0:
                    result["risk_level"] = "YELLOW"
                    result["action_required"] = True

            elif resp.status_code == 404:
                result["risk_level"] = "GREEN"

            else:
                result["error"] = f"API error: {resp.status_code}"

            self.breaches_log.append(result)
            return result

        except requests.exceptions.RequestException as e:
            return {
                "email": email,
                "error": str(e),
                "checked_at": datetime.now().isoformat()
            }

    def check_password_pwned(self, password: str) -> Dict:
        """
        Check if password appears in pwned password database (k-anonymity)

        Args:
            password: Password to check

        Returns:
            Dict with breach count for password
        """
        try:
            import hashlib

            sha1_hash = hashlib.sha1(password.encode()).hexdigest().upper()
            prefix = sha1_hash[:5]
            suffix = sha1_hash[5:]

            time.sleep(1.5)
            url = f"{self.BASE_URL}/pwnedpassword/{prefix}"
            resp = self.session.get(url, timeout=10)

            result = {
                "checked_at": datetime.now().isoformat(),
                "is_pwned": False,
                "breach_count": 0,
                "risk_level": "GREEN"
            }

            if resp.status_code == 200:
                for line in resp.text.split('\n'):
                    if line:
                        hash_suffix, count = line.split(':')
                        if hash_suffix == suffix:
                            result["is_pwned"] = True
                            result["breach_count"] = int(count)
                            result["risk_level"] = "RED" if int(count) > 1 else "YELLOW"
                            break

            return result

        except Exception as e:
            return {"error": str(e), "checked_at": datetime.now().isoformat()}

    def check_domain_breaches(self, domain: str) -> Dict:
        """
        Check all breaches for a domain

        Args:
            domain: Domain to check

        Returns:
            Dict with all breaches for domain
        """
        try:
            time.sleep(1.5)
            url = f"{self.BASE_URL}/breaches?domain={domain}"
            resp = self.session.get(url, timeout=10)

            result = {
                "domain": domain,
                "checked_at": datetime.now().isoformat(),
                "breach_count": 0,
                "breaches": []
            }

            if resp.status_code == 200:
                breaches = resp.json()
                result["breach_count"] = len(breaches)
                result["breaches"] = [{
                    "name": b.get("Name"),
                    "breach_date": b.get("BreachDate"),
                    "affected_count": b.get("PwnCount")
                } for b in breaches]

            return result

        except Exception as e:
            return {"domain": domain, "error": str(e)}

    def generate_report(self, identity: Dict) -> Dict:
        """
        Generate comprehensive breach report for identity

        Args:
            identity: Identity profile with email, username, phone

        Returns:
            Comprehensive breach assessment
        """
        report = {
            "generated_at": datetime.now().isoformat(),
            "identity": identity.get("name"),
            "email_breaches": None,
            "domain_breaches": None,
            "critical_findings": [],
            "recommendations": []
        }

        if "email" in identity:
            report["email_breaches"] = self.check_email_breaches(identity["email"])
            if report["email_breaches"].get("breach_count", 0) > 0:
                report["critical_findings"].append(
                    f"Email found in {report['email_breaches']['breach_count']} breaches"
                )

        if "domain" in identity:
            report["domain_breaches"] = self.check_domain_breaches(identity["domain"])

        # Recommendations
        if report["critical_findings"]:
            report["recommendations"].extend([
                "Change passwords for all accounts",
                "Enable 2FA on critical accounts",
                "Monitor credit reports via AnnualCreditReport.com",
                "Consider identity theft monitoring service",
                "Set fraud alerts with credit bureaus"
            ])
        else:
            report["recommendations"].append("No breaches detected - maintain current security practices")

        return report

    def save_log(self, filepath: str = "logs/hibp_breaches.json"):
        """Save breach log to file"""
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(self.breaches_log, f, indent=2)


if __name__ == "__main__":
    # Example usage
    monitor = HIBPMonitor()

    identity = {
        "name": "Chaitanya Joshi",
        "email": "chaitanyajoshi15@gmail.com",
        "domain": "gmail.com"
    }

    print("Running HIBP breach check...")
    report = monitor.generate_report(identity)
    print(json.dumps(report, indent=2))

    monitor.save_log()
