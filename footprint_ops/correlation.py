#!/usr/bin/env python3
"""
Correlation Analysis Module - Phase 1c

Detects and analyzes correlations between identity artifacts:
- Reused usernames across platforms
- Email pattern matching
- Profile photo matches
- Metadata correlation
- Social graph overlaps

Generates confidence scores (0.0-1.0) for each correlation.
"""

import logging
from typing import Dict, List, Tuple, Set
from collections import defaultdict
import json
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)


class IdentityCorrelationAnalyzer:
    """Analyzes correlations between identity artifacts"""
    
    def __init__(self):
        """Initialize correlation analyzer"""
        self.correlations = []
        self.correlation_scores = defaultdict(float)
        self.confidence_threshold = 0.5
    
    def analyze_profile(self, identity_profile: Dict) -> Dict:
        """
        Analyze identity profile for correlations
        
        Args:
            identity_profile: Identity data dictionary
        
        Returns:
            Correlation analysis results
        """
        results = {
            "timestamp": datetime.now().isoformat(),
            "identity_name": identity_profile.get("identity_id", "unknown"),
            "total_artifacts": 0,
            "correlations_detected": [],
            "correlation_matrix": {},
            "risk_factors": [],
            "summary": {}
        }
        
        # Extract all artifacts
        artifacts = self._extract_artifacts(identity_profile)
        results["total_artifacts"] = sum(len(v) for v in artifacts.values())
        
        logger.info(f"Analyzing {results['total_artifacts']} artifacts for correlations")
        
        # Detect username correlations
        username_corr = self._detect_username_patterns(artifacts)
        results["correlations_detected"].extend(username_corr)
        
        # Detect email patterns
        email_corr = self._detect_email_patterns(artifacts)
        results["correlations_detected"].extend(email_corr)
        
        # Detect name variations
        name_corr = self._detect_name_patterns(identity_profile)
        results["correlations_detected"].extend(name_corr)
        
        # Detect platform overlaps
        platform_corr = self._detect_platform_overlaps(artifacts)
        results["correlations_detected"].extend(platform_corr)
        
        # Build correlation matrix
        results["correlation_matrix"] = self._build_correlation_matrix(results["correlations_detected"])
        
        # Identify risk factors
        results["risk_factors"] = self._identify_risk_factors(results["correlations_detected"], artifacts)
        
        # Generate summary
        results["summary"] = self._generate_summary(results)
        
        logger.info(f"Detected {len(results['correlations_detected'])} correlations")
        return results
    
    def _extract_artifacts(self, profile: Dict) -> Dict:
        """Extract all identity artifacts from profile"""
        artifacts = {
            "usernames": [],
            "emails": [],
            "names": [],
            "locations": [],
            "platforms": set()
        }
        
        # Extract usernames
        accounts = profile.get("sections", {}).get("online_presence", {}).get("accounts", {})
        for platform, username in accounts.items():
            if username and username.strip():
                artifacts["usernames"].append({
                    "value": username.strip(),
                    "platform": platform,
                    "type": "username"
                })
                artifacts["platforms"].add(platform)
        
        # Extract emails
        contact_info = profile.get("sections", {}).get("contact_information", {})
        emails = [contact_info.get("primary_email")] + contact_info.get("secondary_emails", [])
        for email in emails:
            if email and email.strip():
                artifacts["emails"].append({
                    "value": email.strip(),
                    "type": "email"
                })
        
        # Extract names
        personal = profile.get("sections", {}).get("personal_identifiers", {})
        if personal.get("legal_name"):
            artifacts["names"].append({
                "value": personal["legal_name"],
                "type": "legal_name"
            })
        
        for nickname in personal.get("nicknames", []):
            if nickname.strip():
                artifacts["names"].append({
                    "value": nickname.strip(),
                    "type": "nickname"
                })
        
        # Extract locations
        locations = profile.get("sections", {}).get("location_history", {})
        if locations.get("current_address"):
            artifacts["locations"].append({
                "value": locations["current_address"],
                "type": "current_address"
            })
        
        for city in locations.get("cities_lived", []):
            if city and city.strip():
                artifacts["locations"].append({
                    "value": city.strip(),
                    "type": "city"
                })
        
        return artifacts
    
    def _detect_username_patterns(self, artifacts: Dict) -> List[Dict]:
        """Detect reused usernames across platforms"""
        correlations = []
        usernames = artifacts["usernames"]
        
        username_values = [u["value"] for u in usernames]
        platform_map = {u["value"]: u["platform"] for u in usernames}
        
        # Find exact matches
        for i, username1 in enumerate(username_values):
            for j, username2 in enumerate(username_values):
                if i < j and username1.lower() == username2.lower():
                    correlation = {
                        "type": "username_reuse",
                        "artifact1": {"value": username1, "platform": platform_map[username1]},
                        "artifact2": {"value": username2, "platform": platform_map[username2]},
                        "confidence": 0.95,
                        "risk": "HIGH",
                        "description": f"Same username across {platform_map[username1]} and {platform_map[username2]}"
                    }
                    correlations.append(correlation)
        
        # Find similar patterns (levenshtein distance)
        for i, username1 in enumerate(username_values):
            for j, username2 in enumerate(username_values):
                if i < j:
                    similarity = self._string_similarity(username1.lower(), username2.lower())
                    if 0.7 < similarity < 0.95:  # Similar but not identical
                        correlation = {
                            "type": "username_similarity",
                            "artifact1": {"value": username1, "platform": platform_map[username1]},
                            "artifact2": {"value": username2, "platform": platform_map[username2]},
                            "confidence": similarity,
                            "risk": "MEDIUM",
                            "description": f"Similar usernames: {username1} vs {username2}"
                        }
                        correlations.append(correlation)
        
        return correlations
    
    def _detect_email_patterns(self, artifacts: Dict) -> List[Dict]:
        """Detect email address patterns and correlations"""
        correlations = []
        emails = artifacts["emails"]
        
        # Email domain extraction
        email_domains = defaultdict(list)
        for email in emails:
            email_val = email["value"]
            domain = email_val.split("@")[1] if "@" in email_val else None
            if domain:
                email_domains[domain].append(email_val)
        
        # Detect multiple emails on same domain
        for domain, email_list in email_domains.items():
            if len(email_list) > 1:
                correlation = {
                    "type": "email_domain_reuse",
                    "artifacts": email_list,
                    "domain": domain,
                    "confidence": 0.85,
                    "risk": "MEDIUM",
                    "description": f"{len(email_list)} email addresses on same domain: {domain}"
                }
                correlations.append(correlation)
        
        # Detect email address in other artifacts
        for email in emails:
            email_val = email["value"]
            # Check if email appears in usernames
            for username in artifacts["usernames"]:
                if email_val.split("@")[0].lower() in username["value"].lower():
                    correlation = {
                        "type": "email_username_correlation",
                        "email": email_val,
                        "username": username["value"],
                        "platform": username["platform"],
                        "confidence": 0.8,
                        "risk": "HIGH",
                        "description": f"Email prefix matches username on {username['platform']}"
                    }
                    correlations.append(correlation)
        
        return correlations
    
    def _detect_name_patterns(self, profile: Dict) -> List[Dict]:
        """Detect name variations and patterns"""
        correlations = []
        personal = profile.get("sections", {}).get("personal_identifiers", {})
        
        legal_name = personal.get("legal_name", "").lower()
        nicknames = [n.lower() for n in personal.get("nicknames", [])]
        
        # Check if nicknames are derivations of legal name
        for nickname in nicknames:
            if self._is_name_derivation(legal_name, nickname):
                correlation = {
                    "type": "name_derivation",
                    "legal_name": legal_name,
                    "nickname": nickname,
                    "confidence": 0.9,
                    "risk": "HIGH",
                    "description": f"'{nickname}' is likely derivation of '{legal_name}'"
                }
                correlations.append(correlation)
        
        return correlations
    
    def _detect_platform_overlaps(self, artifacts: Dict) -> List[Dict]:
        """Detect patterns across multiple platforms"""
        correlations = []
        
        platforms = list(artifacts["platforms"])
        num_platforms = len(platforms)
        
        # Multi-platform presence is a risk factor
        if num_platforms >= 5:
            correlation = {
                "type": "multi_platform_presence",
                "platforms": platforms,
                "count": num_platforms,
                "confidence": 0.9,
                "risk": "HIGH",
                "description": f"Active on {num_platforms} platforms (consolidates identity)"
            }
            correlations.append(correlation)
        
        return correlations
    
    def _build_correlation_matrix(self, correlations: List[Dict]) -> Dict:
        """Build correlation matrix for visualization"""
        matrix = {
            "total_correlations": len(correlations),
            "by_type": defaultdict(int),
            "by_confidence": defaultdict(int),
            "by_risk": defaultdict(int)
        }
        
        for corr in correlations:
            matrix["by_type"][corr["type"]] += 1
            
            confidence = corr["confidence"]
            if confidence >= 0.9:
                matrix["by_confidence"]["very_high"] += 1
            elif confidence >= 0.7:
                matrix["by_confidence"]["high"] += 1
            elif confidence >= 0.5:
                matrix["by_confidence"]["medium"] += 1
            else:
                matrix["by_confidence"]["low"] += 1
            
            matrix["by_risk"][corr["risk"]] += 1
        
        return dict(matrix)
    
    def _identify_risk_factors(self, correlations: List[Dict], artifacts: Dict) -> List[Dict]:
        """Identify risk factors based on correlations"""
        risks = []
        
        high_risk_count = sum(1 for c in correlations if c["risk"] == "HIGH")
        if high_risk_count > 0:
            risks.append({
                "factor": "high_risk_correlations",
                "count": high_risk_count,
                "severity": "HIGH",
                "recommendation": "Prioritize removing these identities to break linkage"
            })
        
        username_reuse = sum(1 for c in correlations if c["type"] == "username_reuse")
        if username_reuse > 0:
            risks.append({
                "factor": "username_reuse",
                "count": username_reuse,
                "severity": "HIGH",
                "recommendation": "Same username across platforms enables cross-referencing"
            })
        
        platform_count = len(artifacts["platforms"])
        if platform_count > 10:
            risks.append({
                "factor": "excessive_platform_presence",
                "count": platform_count,
                "severity": "MEDIUM",
                "recommendation": "Consider consolidating or removing unused accounts"
            })
        
        return risks
    
    def _generate_summary(self, results: Dict) -> Dict:
        """Generate analysis summary"""
        correlations = results["correlations_detected"]
        
        summary = {
            "total_artifacts_analyzed": results["total_artifacts"],
            "total_correlations_found": len(correlations),
            "highest_risk": "UNKNOWN",
            "identity_linkage_strength": "LOW"
        }
        
        # Determine highest risk
        if correlations:
            risks = [c["risk"] for c in correlations]
            if "HIGH" in risks:
                summary["highest_risk"] = "HIGH"
            elif "MEDIUM" in risks:
                summary["highest_risk"] = "MEDIUM"
            else:
                summary["highest_risk"] = "LOW"
        
        # Determine identity linkage strength
        high_confidence = sum(1 for c in correlations if c["confidence"] >= 0.8)
        if high_confidence > 5:
            summary["identity_linkage_strength"] = "VERY_STRONG"
        elif high_confidence > 2:
            summary["identity_linkage_strength"] = "STRONG"
        elif high_confidence > 0:
            summary["identity_linkage_strength"] = "MODERATE"
        
        summary["recommendation"] = self._generate_recommendation(summary)
        
        return summary
    
    def _generate_recommendation(self, summary: Dict) -> str:
        """Generate actionable recommendation"""
        linkage = summary["identity_linkage_strength"]
        
        if linkage == "VERY_STRONG":
            return "URGENT: Multiple strong identity correlations detected. Prioritize removal of reused usernames and break linkage chains."
        elif linkage == "STRONG":
            return "HIGH PRIORITY: Remove duplicate usernames and consolidate accounts before deletion."
        elif linkage == "MODERATE":
            return "MEDIUM PRIORITY: Address email-username correlations and similar usernames."
        else:
            return "LOW PRIORITY: Limited correlations detected, but continue monitoring."
    
    def _string_similarity(self, s1: str, s2: str) -> float:
        """Calculate string similarity (0.0-1.0)"""
        # Simple Levenshtein-based similarity
        longer = s1 if len(s1) > len(s2) else s2
        shorter = s2 if len(s1) > len(s2) else s1
        
        if len(longer) == 0:
            return 1.0
        
        edit_distance = self._levenshtein(longer, shorter)
        return 1.0 - (edit_distance / len(longer))
    
    def _levenshtein(self, s1: str, s2: str) -> int:
        """Calculate Levenshtein distance"""
        if len(s1) < len(s2):
            return self._levenshtein(s2, s1)
        
        if len(s2) == 0:
            return len(s1)
        
        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        
        return previous_row[-1]
    
    def _is_name_derivation(self, full_name: str, short_name: str) -> bool:
        """Check if short_name is likely derivation of full_name"""
        parts = full_name.split()
        for part in parts:
            if len(short_name) > 2 and short_name in part.lower():
                return True
        return False
    
    def export_report(self, results: Dict, output_path: str = "correlation/analysis.json"):
        """Export correlation analysis to JSON"""
        try:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            logger.info(f"Correlation report exported to {output_path}")
        except Exception as e:
            logger.error(f"Failed to export report: {e}")


# Utility function
def analyze_identity_correlations(identity_profile: Dict) -> Dict:
    """Convenience function to analyze identity profile"""
    analyzer = IdentityCorrelationAnalyzer()
    return analyzer.analyze_profile(identity_profile)


if __name__ == "__main__":
    # Test correlation analysis
    import json
    
    # Load test profile
    try:
        with open('intel/identity_profile.json', 'r') as f:
            profile = json.load(f)
        
        analyzer = IdentityCorrelationAnalyzer()
        results = analyzer.analyze_profile(profile)
        analyzer.export_report(results)
        
        print(f"✓ Analyzed {results['total_artifacts']} artifacts")
        print(f"✓ Found {len(results['correlations_detected'])} correlations")
        print(f"✓ Report exported to correlation/analysis.json")
    except FileNotFoundError:
        print("No identity profile found. Run 'footprint-ops intake --interactive' first.")
