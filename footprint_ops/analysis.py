#!/usr/bin/env python3
"""
Exposure Analysis Module - Phase 3

Analyzes all discovered exposures and generates risk matrices.

Functions:
- Severity classification (CRITICAL/HIGH/MEDIUM/LOW)
- Risk scoring algorithm
- Correlation analysis
- Search visibility ranking
- Data broker prevalence analysis
- Breach impact assessment
- Removal difficulty estimation
- Timeline generation
- Prioritization matrix

Output:
- Risk matrix JSON
- HTML visualization
- Removal priority list
- Detailed exposure report
"""

import logging
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
from collections import defaultdict
import json
from pathlib import Path
import statistics

logger = logging.getLogger(__name__)


@dataclass
class ExposureAnalysis:
    """Comprehensive exposure analysis result"""
    exposure_id: str
    type: str  # search_engine, data_broker, social_media, archive, etc
    source: str  # specific platform
    url: Optional[str]
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW
    risk_score: float  # 0.0-100.0
    correlation_risk: float  # 0.0-1.0 (how unique is this?)
    search_visibility: Optional[int]  # position in search results
    removal_feasibility: str  # EASY, MEDIUM, HARD
    removal_cost: Optional[int]  # estimated days
    data_exposed: List[str]  # [address, phone, email, etc]
    discovered_date: str
    impact_summary: str
    recommendation: str
    priority: int  # 1-5 (1 = highest)


class ExposureAnalyzer:
    """Analyzes and prioritizes exposures"""
    
    def __init__(self):
        """Initialize exposure analyzer"""
        self.exposures = []
        self.risk_matrix = {}
        
        # Risk factor weights
        self.risk_weights = {
            'address': 0.95,
            'phone': 0.90,
            'ssn': 1.0,
            'credit_card': 1.0,
            'email': 0.70,
            'employment': 0.50,
            'education': 0.40,
            'social_profile': 0.55,
            'photo': 0.45
        }
    
    def analyze_discoveries(self, search_results: List[Dict], data_brokers: List[Dict], social_media: List[Dict]) -> Dict:
        """
        Analyze all discovered exposures
        
        Args:
            search_results: From Phase 2a
            data_brokers: From Phase 2b
            social_media: From Phase 2c
        
        Returns:
            Analysis results
        """
        all_analyses = []
        
        # Analyze search results
        for result in search_results:
            analysis = self._analyze_search_result(result)
            if analysis:
                all_analyses.append(analysis)
        
        # Analyze data brokers
        for broker in data_brokers:
            if broker.get('found'):
                analysis = self._analyze_data_broker(broker)
                if analysis:
                    all_analyses.append(analysis)
        
        # Analyze social media
        for profile in social_media:
            if profile.get('found'):
                analysis = self._analyze_social_profile(profile)
                if analysis:
                    all_analyses.append(analysis)
        
        self.exposures = all_analyses
        
        # Generate matrix
        matrix = self._build_risk_matrix(all_analyses)
        
        return {
            "timestamp": datetime.now().isoformat(),
            "total_exposures": len(all_analyses),
            "exposures_by_severity": self._count_by_severity(all_analyses),
            "exposures_by_source": self._count_by_source(all_analyses),
            "risk_matrix": matrix,
            "exposures": [asdict(a) for a in all_analyses],
            "summary": self._generate_summary(all_analyses),
            "recommendations": self._generate_recommendations(all_analyses)
        }
    
    def _analyze_search_result(self, result: Dict) -> Optional[ExposureAnalysis]:
        """Analyze a search result exposure"""
        import uuid
        
        risk_score = self._calculate_risk_score(result.get('risk_level', 'LOW'))
        severity = self._classify_severity(risk_score)
        
        data_exposed = []
        if 'address' in result.get('snippet', '').lower():
            data_exposed.append('address')
        if 'phone' in result.get('snippet', '').lower():
            data_exposed.append('phone')
        if 'email' in result.get('snippet', '').lower():
            data_exposed.append('email')
        
        analysis = ExposureAnalysis(
            exposure_id=str(uuid.uuid4()),
            type='search_engine',
            source=result.get('engine', 'unknown'),
            url=result.get('url'),
            severity=severity,
            risk_score=risk_score,
            correlation_risk=self._assess_correlation_risk(result.get('snippet', '')),
            search_visibility=result.get('position', 999),
            removal_feasibility='MEDIUM',
            removal_cost=7,  # weeks
            data_exposed=data_exposed,
            discovered_date=result.get('found_date', datetime.now().isoformat()),
            impact_summary=f"Found in {result.get('engine')} results at position {result.get('position', 999)}",
            recommendation=self._recommend_action(severity, 'search_engine'),
            priority=self._assign_priority(severity)
        )
        
        return analysis
    
    def _analyze_data_broker(self, broker: Dict) -> Optional[ExposureAnalysis]:
        """Analyze a data broker exposure"""
        import uuid
        
        risk_score = self._calculate_broker_risk(broker.get('risk_level', 'MEDIUM'))
        severity = self._classify_severity(risk_score)
        
        data_exposed = broker.get('data_exposed', [])
        
        # Determine removal feasibility
        removal_difficulty = broker.get('removal_difficulty', 'MEDIUM')
        if removal_difficulty == 'EASY':
            removal_feasibility = 'EASY'
            removal_cost = 1  # days
        elif removal_difficulty == 'MEDIUM':
            removal_feasibility = 'MEDIUM'
            removal_cost = 7
        else:
            removal_feasibility = 'HARD'
            removal_cost = 30
        
        analysis = ExposureAnalysis(
            exposure_id=str(uuid.uuid4()),
            type='data_broker',
            source=broker.get('broker', 'unknown'),
            url=broker.get('url'),
            severity=severity,
            risk_score=risk_score,
            correlation_risk=0.9,  # Data brokers are highly correlating
            search_visibility=None,
            removal_feasibility=removal_feasibility,
            removal_cost=removal_cost,
            data_exposed=data_exposed if isinstance(data_exposed, list) else [],
            discovered_date=broker.get('last_checked', datetime.now().isoformat()),
            impact_summary=f"Listed on {broker.get('broker')} with {len(data_exposed) if data_exposed else 'personal'} data exposed",
            recommendation=self._recommend_action(severity, 'data_broker'),
            priority=self._assign_priority(severity)
        )
        
        return analysis
    
    def _analyze_social_profile(self, profile: Dict) -> Optional[ExposureAnalysis]:
        """Analyze a social media profile exposure"""
        import uuid
        
        exposure_level = profile.get('exposure_level', 'MEDIUM')
        risk_score = self._calculate_exposure_risk(exposure_level)
        severity = self._classify_severity(risk_score)
        
        data_exposed = profile.get('profile_info', {}).get('exposure', '').split(', ') if profile.get('profile_info') else []
        
        analysis = ExposureAnalysis(
            exposure_id=str(uuid.uuid4()),
            type='social_media',
            source=profile.get('platform', 'unknown'),
            url=profile.get('profile_url'),
            severity=severity,
            risk_score=risk_score,
            correlation_risk=0.7,  # Social profiles contain personal info
            search_visibility=None,
            removal_feasibility='EASY',
            removal_cost=1,  # You can delete your own account
            data_exposed=data_exposed,
            discovered_date=profile.get('last_updated', datetime.now().isoformat()),
            impact_summary=f"Active {exposure_level.lower()} exposure on {profile.get('platform')}",
            recommendation=self._recommend_action(severity, 'social_media'),
            priority=self._assign_priority(severity)
        )
        
        return analysis
    
    def _calculate_risk_score(self, risk_level: str) -> float:
        """Calculate numeric risk score from level"""
        scores = {
            'CRITICAL': 95.0,
            'HIGH': 75.0,
            'MEDIUM': 50.0,
            'LOW': 25.0
        }
        return scores.get(risk_level, 50.0)
    
    def _calculate_broker_risk(self, risk_level: str) -> float:
        """Calculate data broker risk score"""
        scores = {
            'CRITICAL': 90.0,
            'HIGH': 70.0,
            'MEDIUM': 40.0,
            'LOW': 20.0
        }
        return scores.get(risk_level, 40.0)
    
    def _calculate_exposure_risk(self, exposure_level: str) -> float:
        """Calculate social media exposure risk"""
        scores = {
            'HIGH': 70.0,
            'MEDIUM': 45.0,
            'LOW': 20.0
        }
        return scores.get(exposure_level, 45.0)
    
    def _classify_severity(self, risk_score: float) -> str:
        """Classify severity from risk score"""
        if risk_score >= 80:
            return 'CRITICAL'
        elif risk_score >= 60:
            return 'HIGH'
        elif risk_score >= 40:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    def _assess_correlation_risk(self, snippet: str) -> float:
        """Assess how unique this exposure is (correlation risk)"""
        # Lower uniqueness = higher correlation risk
        # If snippet contains identifying info, higher risk
        unique_indicators = ['email', 'phone', 'address', 'ssn']
        count = sum(1 for ind in unique_indicators if ind in snippet.lower())
        return min(count * 0.25, 1.0)
    
    def _assign_priority(self, severity: str) -> int:
        """Assign priority (1 = highest)"""
        priorities = {
            'CRITICAL': 1,
            'HIGH': 2,
            'MEDIUM': 3,
            'LOW': 4
        }
        return priorities.get(severity, 4)
    
    def _recommend_action(self, severity: str, exposure_type: str) -> str:
        """Generate removal recommendation"""
        base_recommendation = {
            'CRITICAL': 'REMOVE IMMEDIATELY',
            'HIGH': 'REMOVE URGENTLY',
            'MEDIUM': 'REMOVE (MEDIUM PRIORITY)',
            'LOW': 'MONITOR & REMOVE'
        }
        
        method_recommendation = {
            'search_engine': ' via Search Console',
            'data_broker': ' via CCPA/opt-out',
            'social_media': ' delete account'
        }
        
        base = base_recommendation.get(severity, 'REVIEW')
        method = method_recommendation.get(exposure_type, '')
        
        return f"{base}{method}"
    
    def _build_risk_matrix(self, exposures: List[ExposureAnalysis]) -> Dict:
        """Build risk vs removal difficulty matrix"""
        matrix = defaultdict(lambda: defaultdict(list))
        
        for exp in exposures:
            matrix[exp.severity][exp.removal_feasibility].append(exp.exposure_id)
        
        return dict(matrix)
    
    def _count_by_severity(self, exposures: List[ExposureAnalysis]) -> Dict[str, int]:
        """Count exposures by severity"""
        counts = defaultdict(int)
        for exp in exposures:
            counts[exp.severity] += 1
        return dict(counts)
    
    def _count_by_source(self, exposures: List[ExposureAnalysis]) -> Dict[str, int]:
        """Count exposures by source"""
        counts = defaultdict(int)
        for exp in exposures:
            counts[exp.source] += 1
        return dict(counts)
    
    def _generate_summary(self, exposures: List[ExposureAnalysis]) -> Dict:
        """Generate analysis summary"""
        severity_counts = self._count_by_severity(exposures)
        avg_risk = statistics.mean([e.risk_score for e in exposures]) if exposures else 0
        
        summary = {
            "total_exposures": len(exposures),
            "critical_count": severity_counts.get('CRITICAL', 0),
            "high_count": severity_counts.get('HIGH', 0),
            "medium_count": severity_counts.get('MEDIUM', 0),
            "low_count": severity_counts.get('LOW', 0),
            "average_risk_score": round(avg_risk, 2),
            "urgency": self._assess_urgency(severity_counts),
            "estimated_removal_time_days": self._estimate_removal_time(exposures)
        }
        
        return summary
    
    def _assess_urgency(self, severity_counts: Dict) -> str:
        """Assess overall urgency"""
        critical = severity_counts.get('CRITICAL', 0)
        high = severity_counts.get('HIGH', 0)
        
        if critical >= 5 or high >= 10:
            return 'CRITICAL - ACT NOW'
        elif critical > 0 or high >= 5:
            return 'URGENT - START REMOVAL TODAY'
        elif high > 0:
            return 'HIGH - START THIS WEEK'
        else:
            return 'MODERATE - ONGOING REMOVAL'
    
    def _estimate_removal_time(self, exposures: List[ExposureAnalysis]) -> int:
        """Estimate total removal time in days"""
        # Sum removal costs (weighted by priority)
        total_days = sum(exp.removal_cost or 7 for exp in exposures if exp.removal_feasibility != 'HARD')
        hard_removals = len([e for e in exposures if e.removal_feasibility == 'HARD'])
        total_days += hard_removals * 30  # Hard removals take longer
        return total_days
    
    def _generate_recommendations(self, exposures: List[ExposureAnalysis]) -> Dict:
        """Generate prioritized action recommendations"""
        critical = sorted([e for e in exposures if e.severity == 'CRITICAL'], key=lambda x: x.risk_score, reverse=True)
        high = sorted([e for e in exposures if e.severity == 'HIGH'], key=lambda x: x.risk_score, reverse=True)
        
        recommendations = {
            "phase_1_immediate": [
                {
                    "priority": i + 1,
                    "source": e.source,
                    "action": e.recommendation,
                    "estimated_days": e.removal_cost
                }
                for i, e in enumerate(critical[:5])  # Top 5 critical
            ],
            "phase_2_this_week": [
                {
                    "priority": i + 6,
                    "source": e.source,
                    "action": e.recommendation,
                    "estimated_days": e.removal_cost
                }
                for i, e in enumerate(high[:10])  # Top 10 high
            ],
            "phase_3_ongoing": f"Monitor and continue removal of {len([e for e in exposures if e.severity in ['MEDIUM', 'LOW']])} medium/low exposures"
        }
        
        return recommendations
    
    def export_analysis(self, analysis: Dict, output_path: str = "exposures/analysis.json"):
        """Export analysis to JSON"""
        try:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w') as f:
                json.dump(analysis, f, indent=2, default=str)
            logger.info(f"Analysis exported to {output_path}")
        except Exception as e:
            logger.error(f"Failed to export analysis: {e}")


if __name__ == "__main__":
    # Test analysis
    analyzer = ExposureAnalyzer()
    
    # Mock data for testing
    mock_search_results = [
        {
            "url": "https://example.com",
            "engine": "google",
            "position": 1,
            "risk_level": "HIGH",
            "snippet": "John Smith address phone number email",
            "found_date": datetime.now().isoformat()
        }
    ]
    
    mock_brokers = [
        {
            "found": True,
            "broker": "Spokeo",
            "url": "https://spokeo.com/john-smith",
            "risk_level": "CRITICAL",
            "removal_difficulty": "EASY",
            "data_exposed": ["name", "phone", "address"],
            "last_checked": datetime.now().isoformat()
        }
    ]
    
    mock_profiles = [
        {
            "found": True,
            "platform": "LinkedIn",
            "profile_url": "https://linkedin.com/in/johnsmith",
            "exposure_level": "HIGH",
            "profile_info": {"exposure": "name, email, work history"},
            "last_updated": datetime.now().isoformat()
        }
    ]
    
    analysis = analyzer.analyze_discoveries(mock_search_results, mock_brokers, mock_profiles)
    analyzer.export_analysis(analysis)
    
    print(f"✓ Analyzed {analysis['total_exposures']} exposures")
    print(f"✓ Analysis exported to exposures/analysis.json")
