#!/usr/bin/env python3
"""
Privacy Hardening Module - Phase 6

Provides practical operational security and privacy hardening:
- Browser isolation and configuration
- Email segmentation strategy
- Device separation
- Metadata hygiene
- Password management
- VPN/DNS configuration
- Tracking prevention
- Financial privacy
- Communications security

This module generates personalized hardening guides.
"""

import logging
import json
from typing import Dict, List
from datetime import datetime
from pathlib import Path
from enum import Enum

logger = logging.getLogger(__name__)


class HardeningLevel(str, Enum):
    """Privacy hardening intensity levels"""
    BASIC = "basic"  # Essential protections
    ADVANCED = "advanced"  # Comprehensive
    PARANOID = "paranoid"  # Maximum isolation


class PrivacyHardeningGuide:
    """Generates personalized privacy hardening guides"""
    
    def __init__(self, level: HardeningLevel = HardeningLevel.ADVANCED):
        """
        Initialize hardening guide
        
        Args:
            level: Hardening intensity (basic, advanced, paranoid)
        """
        self.level = level
        self.recommendations = []
    
    def generate_comprehensive_guide(self, identity: Dict) -> Dict:
        """Generate complete privacy hardening guide"""
        
        guide = {
            "timestamp": datetime.now().isoformat(),
            "user": identity.get("name"),
            "level": self.level.value,
            "sections": {
                "browser_hardening": self._browser_hardening(),
                "email_segmentation": self._email_segmentation(),
                "device_separation": self._device_separation(),
                "metadata_hygiene": self._metadata_hygiene(),
                "password_security": self._password_security(),
                "network_privacy": self._network_privacy(),
                "financial_privacy": self._financial_privacy(),
                "communications": self._communications_security(),
                "monitoring": self._continuous_monitoring()
            },
            "implementation_timeline": self._get_timeline(),
            "tools_required": self._get_tools_list(),
            "estimated_cost": self._estimate_cost()
        }
        
        logger.info(f"Generated {self.level.value} privacy hardening guide")
        return guide
    
    def _browser_hardening(self) -> Dict:
        """Browser hardening recommendations"""
        
        base = {
            "objective": "Prevent tracking and data collection through browsers",
            "recommendations": [
                {
                    "priority": "critical",
                    "action": "Use privacy-focused browser",
                    "options": [
                        "Firefox (with hardening)",
                        "Brave (built-in protections)",
                        "Tor Browser (maximum anonymity)"
                    ],
                    "avoid": ["Chrome (Google tracking)", "Safari (Apple tracking)"],
                    "implementation_time": "1 hour"
                },
                {
                    "priority": "critical",
                    "action": "Install privacy extensions",
                    "recommended": [
                        "uBlock Origin (ad/tracker blocking)",
                        "Privacy Badger (tracker protection)",
                        "HTTPS Everywhere (encryption)",
                        "Decentraleyes (CDN protection)"
                    ],
                    "implementation_time": "30 minutes"
                },
                {
                    "priority": "high",
                    "action": "Configure browser settings",
                    "settings": [
                        "Disable 3rd party cookies",
                        "Block fingerprinting",
                        "Enable DNS-over-HTTPS",
                        "Disable autocomplete",
                        "Clear history on exit",
                        "Use private browsing by default"
                    ],
                    "implementation_time": "1 hour"
                },
                {
                    "priority": "medium",
                    "action": "Disable JavaScript from untrusted sites",
                    "tool": "NoScript extension",
                    "implementation_time": "30 minutes"
                }
            ]
        }
        
        if self.level == HardeningLevel.PARANOID:
            base["recommendations"].append({
                "priority": "critical",
                "action": "Use Tor Browser exclusively",
                "purpose": "Anonymize all traffic",
                "implementation_time": "2 hours"
            })
        
        return base
    
    def _email_segmentation(self) -> Dict:
        """Email segmentation strategy"""
        
        return {
            "objective": "Compartmentalize email to prevent correlation",
            "strategy": "Use multiple email addresses for different purposes",
            "implementation": {
                "tier_1_personal": {
                    "purpose": "Family, close friends only",
                    "provider": "ProtonMail (encrypted) or Tutanota",
                    "usage": "Never use for online services",
                    "forwarding": False,
                    "setup_time": "1 hour"
                },
                "tier_2_essential": {
                    "purpose": "Banking, critical accounts only",
                    "provider": "Temporary email service or ProtonMail alias",
                    "usage": "Highly sensitive transactions",
                    "forwarding": False,
                    "backup_emails": 2,
                    "setup_time": "1 hour"
                },
                "tier_3_general": {
                    "purpose": "Most online accounts",
                    "provider": "ProtonMail or Tutanota (encrypted preferred)",
                    "usage": "Primary online identity",
                    "forwarding": True,
                    "setup_time": "1 hour"
                },
                "tier_4_disposable": {
                    "purpose": "Sign-ups, untrustworthy sites",
                    "provider": "Temporary email (10minutemail, tempmail)",
                    "usage": "Sites you don't trust",
                    "self_destruct": "Auto-delete after 10 minutes",
                    "setup_time": "5 minutes"
                }
            },
            "total_setup_time": "4 hours"
        }
    
    def _device_separation(self) -> Dict:
        """Device separation recommendations"""
        
        base = {
            "objective": "Compartmentalize devices by trust level and purpose",
            "strategy": "Use separate devices/virtual machines for different activities",
            "basic_approach": {
                "device_1_work": {
                    "purpose": "Work accounts and professional",
                    "network": "VPN required",
                    "restrictions": "No personal data"
                },
                "device_2_personal": {
                    "purpose": "Personal accounts, finance",
                    "network": "VPN required",
                    "restrictions": "No work data"
                },
                "device_3_untrusted": {
                    "purpose": "New sites, shopping, experiments",
                    "network": "Tor or VPN",
                    "restrictions": "Assume compromised after use",
                    "reset_frequency": "Weekly"
                }
            },
            "virtual_machine_approach": {
                "benefit": "Isolate activities without multiple physical devices",
                "tools": [
                    "VirtualBox (free)",
                    "VMware Workstation",
                    "Qubes OS (security-focused)"
                ],
                "vms": [
                    "VM 1: General use",
                    "VM 2: Finance/banking",
                    "VM 3: Untrusted sites"
                ],
                "implementation_time": "8 hours"
            }
        }
        
        if self.level == HardeningLevel.PARANOID:
            base["extreme_approach"] = {
                "method": "Dedicated hardware + Tor",
                "devices": [
                    "Phone 1: Personal (iOS, no apps)",
                    "Phone 2: Work (Android, restricted)",
                    "Phone 3: Untrusted (Tor, disposable)",
                    "Laptop 1: Personal (Linux, full disk encryption)",
                    "Laptop 2: Work (Linux, isolated network)",
                    "Laptop 3: Tor-only (Tails OS)"
                ]
            }
        
        return base
    
    def _metadata_hygiene(self) -> Dict:
        """Metadata removal and hygiene"""
        
        return {
            "objective": "Remove identifying metadata from files and data",
            "metadata_types": [
                {
                    "type": "Document metadata (EXIF, IPTC)",
                    "risk": "High - contains location, device info, timestamps",
                    "removal_tools": [
                        "ExifTool (command-line)",
                        "ImageOptim (GUI)",
                        "MAT (Metadata Anonymization Toolkit)"
                    ],
                    "process": [
                        "1. Identify metadata",
                        "2. Strip metadata before sharing",
                        "3. Verify removal"
                    ]
                },
                {
                    "type": "Photo metadata (location, camera)",
                    "risk": "High - GPS coordinates, device identification",
                    "removal_tools": [
                        "ExifTool",
                        "Photos app (built-in on iOS/Android)",
                        "Verexif (online, use with caution)"
                    ],
                    "best_practice": "Disable location tracking in camera app"
                },
                {
                    "type": "Document metadata (author, creation date)",
                    "risk": "Medium - identifies creator and document history",
                    "removal_tools": [
                        "LibreOffice (remove metadata before save)",
                        "Microsoft Word (inspect & remove)",
                        "Mat2"
                    ]
                },
                {
                    "type": "Browser metadata (history, cookies)",
                    "risk": "High - tracks all activity",
                    "removal_tools": ["Browser privacy settings"],
                    "best_practice": "Clear history immediately after use"
                },
                {
                    "type": "File metadata (creation timestamp, author)",
                    "risk": "Medium",
                    "removal_tools": ["Touch command (Linux)", "Properties (Windows)"]
                }
            ],
            "implementation_checklist": [
                "□ Install ExifTool",
                "□ Set up automated metadata stripping",
                "□ Disable camera location tracking",
                "□ Clear browser history daily",
                "□ Check document metadata before sharing",
                "□ Use MAT for batch processing"
            ]
        }
    
    def _password_security(self) -> Dict:
        """Password management and security"""
        
        return {
            "objective": "Secure password management with strong, unique passwords",
            "strategy": "Use password manager with encryption",
            "recommended_tools": [
                {
                    "name": "Bitwarden",
                    "type": "Open-source password manager",
                    "encryption": "End-to-end encrypted",
                    "cost": "Free or $10/year",
                    "platforms": "All (desktop, mobile, browser)"
                },
                {
                    "name": "KeePass",
                    "type": "Offline password manager",
                    "encryption": "AES-256",
                    "cost": "Free",
                    "platforms": "Windows, Mac, Linux"
                },
                {
                    "name": "1Password",
                    "type": "Commercial password manager",
                    "encryption": "AES-256",
                    "cost": "$3-5/month",
                    "platforms": "All"
                }
            ],
            "best_practices": [
                "Use 20+ character passwords",
                "Include uppercase, lowercase, numbers, symbols",
                "Never reuse passwords",
                "Enable 2FA on all accounts",
                "Store password manager password in secure location",
                "Regular password audits"
            ],
            "password_strength_requirements": {
                "minimum_length": 20,
                "required_character_types": ["uppercase", "lowercase", "numbers", "symbols"],
                "entropy_minimum": 128,
                "example": "Tr0pic@lThund3r$torm#2024!"
            }
        }
    
    def _network_privacy(self) -> Dict:
        """Network and DNS privacy"""
        
        return {
            "objective": "Secure network traffic and DNS queries",
            "components": [
                {
                    "component": "VPN (Virtual Private Network)",
                    "purpose": "Encrypt and anonymize internet traffic",
                    "recommended_providers": [
                        {
                            "name": "Mullvad VPN",
                            "cost": "5 EUR/month or donation",
                            "no_logs": True,
                            "no_signup": True
                        },
                        {
                            "name": "ProtonVPN",
                            "cost": "Free or paid",
                            "no_logs": True,
                            "based_in": "Switzerland"
                        },
                        {
                            "name": "IVPN",
                            "cost": "$3.33/month",
                            "no_logs": True,
                            "transparency": "Regular audits"
                        }
                    ],
                    "avoid": ["Free VPNs (sell data)", "US-based VPNs (NSA cooperation)"]
                },
                {
                    "component": "DNS over HTTPS (DoH)",
                    "purpose": "Encrypt DNS queries",
                    "providers": [
                        "Quad9 (9.9.9.9)",
                        "Cloudflare (1.1.1.1) - privacy-focused",
                        "NextDNS (malware/adult content blocking)"
                    ],
                    "implementation": "Configure in browser or OS settings"
                },
                {
                    "component": "Tor Network",
                    "purpose": "Maximum anonymity",
                    "use_case": "Extremely sensitive activities",
                    "implementation": "Tor Browser (easiest)"
                }
            ],
            "setup_time": "2 hours"
        }
    
    def _financial_privacy(self) -> Dict:
        """Financial privacy measures"""
        
        return {
            "objective": "Protect financial transactions and data",
            "measures": [
                {
                    "measure": "Use separate bank accounts",
                    "purpose": "Compartmentalize financial activity",
                    "recommendation": [
                        "Account 1: Primary (minimal online)",
                        "Account 2: Online payments (limited funds)",
                        "Account 3: Privacy-focused banking"
                    ]
                },
                {
                    "measure": "Use privacy-focused payment methods",
                    "options": [
                        {
                            "method": "Cash",
                            "anonymity": "Maximum",
                            "limitations": "Not digital"
                        },
                        {
                            "method": "Cryptocurrency (Monero)",
                            "anonymity": "High",
                            "privacy_focus": "True"
                        },
                        {
                            "method": "Virtual card services",
                            "examples": ["Privacy.com", "Blur"],
                            "benefit": "Single-use cards, prevents tracking"
                        }
                    ]
                },
                {
                    "measure": "Disable financial marketing",
                    "actions": [
                        "Opt-out of credit card marketing",
                        "Unsubscribe from financial emails",
                        "Limit data sharing at financial institutions",
                        "Disable targeted ads"
                    ]
                }
            ]
        }
    
    def _communications_security(self) -> Dict:
        """Communications security"""
        
        return {
            "objective": "Secure all communications",
            "messaging": {
                "encrypted_options": [
                    {
                        "app": "Signal",
                        "encryption": "End-to-end (Signal Protocol)",
                        "open_source": True,
                        "trust_level": "Highest"
                    },
                    {
                        "app": "Wire",
                        "encryption": "End-to-end",
                        "open_source": True,
                        "features": "Video calls, file sharing"
                    },
                    {
                        "app": "Jami (formerly GNU Ring)",
                        "encryption": "Decentralized, end-to-end",
                        "open_source": True
                    }
                ],
                "avoid": ["WhatsApp (Facebook owned)", "Telegram (not private default)"]
            },
            "voice_calls": {
                "encrypted_options": [
                    "Signal (voice calls)",
                    "Wire (HD voice)",
                    "Jami (peer-to-peer)"
                ],
                "avoid": ["Google Meet (tracked)", "Zoom (privacy issues)"]
            },
            "email": {
                "encryption": "PGP/GPG or encrypted email provider",
                "providers": [
                    {
                        "name": "ProtonMail",
                        "encryption": "End-to-end",
                        "features": "Auto-delete, encrypted attachments"
                    },
                    {
                        "name": "Tutanota",
                        "encryption": "End-to-end",
                        "features": "Encrypted calendar, contacts"
                    }
                ]
            }
        }
    
    def _continuous_monitoring(self) -> Dict:
        """Continuous privacy monitoring"""
        
        return {
            "objective": "Maintain privacy posture over time",
            "monitoring_activities": [
                {
                    "activity": "Check for data breaches",
                    "frequency": "Monthly",
                    "tools": ["Have I Been Pwned", "Firefox Monitor"],
                    "action": "Change password if breached"
                },
                {
                    "activity": "Monitor credit reports",
                    "frequency": "Quarterly",
                    "tools": ["AnnualCreditReport.com"],
                    "action": "Check for fraud"
                },
                {
                    "activity": "Verify account security",
                    "frequency": "Monthly",
                    "checks": [
                        "Review login locations",
                        "Check 2FA is enabled",
                        "Review connected apps",
                        "Check recovery options"
                    ]
                },
                {
                    "activity": "Search for your name",
                    "frequency": "Monthly",
                    "tools": ["Google Search", "DuckDuckGo"],
                    "action": "Identify new exposures"
                },
                {
                    "activity": "Monitor dark web",
                    "frequency": "Monthly",
                    "tools": ["Have I Been Pwned", "Dark web monitoring services"]
                }
            ],
            "kpis": [
                "Number of compromised accounts: 0",
                "Number of new exposures: 0",
                "Negative search results: Decreasing",
                "Positive content ranking: Increasing"
            ]
        }
    
    def _get_timeline(self) -> Dict:
        """Implementation timeline"""
        
        timelines = {
            HardeningLevel.BASIC: {
                "week_1": ["Browser hardening", "Email segmentation setup"],
                "week_2": ["Password manager setup", "2FA enablement"],
                "week_3": ["VPN installation", "DNS configuration"],
                "total_weeks": 3
            },
            HardeningLevel.ADVANCED: {
                "week_1": ["Browser hardening", "Email segmentation"],
                "week_2": ["Password manager", "Device separation"],
                "week_3": ["Network privacy", "Financial hardening"],
                "week_4": ["Communications security", "Monitoring setup"],
                "total_weeks": 4
            },
            HardeningLevel.PARANOID: {
                "week_1": ["Tor Browser", "ProtonMail setup"],
                "week_2": ["VirtualBox VMs"],
                "week_3": ["Dedicated devices"],
                "week_4": ["Metadata tools"],
                "month_2": ["Advanced isolation"],
                "total_weeks": 8
            }
        }
        
        return timelines.get(self.level, timelines[HardeningLevel.ADVANCED])
    
    def _get_tools_list(self) -> List[Dict]:
        """Get required tools by level"""
        
        base_tools = [
            {"name": "Bitwarden", "type": "Password manager", "cost": "Free"},
            {"name": "Firefox", "type": "Browser", "cost": "Free"},
            {"name": "uBlock Origin", "type": "Extension", "cost": "Free"},
            {"name": "Mullvad VPN", "type": "VPN", "cost": "$60/year"},
            {"name": "Signal", "type": "Messaging", "cost": "Free"},
            {"name": "ProtonMail", "type": "Email", "cost": "Free or paid"}
        ]
        
        advanced_tools = base_tools + [
            {"name": "ExifTool", "type": "Metadata", "cost": "Free"},
            {"name": "VirtualBox", "type": "Virtualization", "cost": "Free"}
        ]
        
        paranoid_tools = advanced_tools + [
            {"name": "Tor Browser", "type": "Anonymity", "cost": "Free"},
            {"name": "Tails OS", "type": "Live OS", "cost": "Free"},
            {"name": "Qubes OS", "type": "Secure OS", "cost": "Free"}
        ]
        
        tools_by_level = {
            HardeningLevel.BASIC: base_tools,
            HardeningLevel.ADVANCED: advanced_tools,
            HardeningLevel.PARANOID: paranoid_tools
        }
        
        return tools_by_level.get(self.level, advanced_tools)
    
    def _estimate_cost(self) -> Dict:
        """Estimate total cost by level"""
        
        costs = {
            HardeningLevel.BASIC: {
                "one_time": 0,
                "monthly": 5,
                "annual": 60,
                "breakdown": "VPN ($5/mo), optional email upgrade"
            },
            HardeningLevel.ADVANCED: {
                "one_time": 20,
                "monthly": 10,
                "annual": 140,
                "breakdown": "VPN ($5/mo), email ($5/mo), one-time tools ($20)"
            },
            HardeningLevel.PARANOID: {
                "one_time": 500,
                "monthly": 20,
                "annual": 740,
                "breakdown": "Dedicated devices, VPN, email, advanced tools"
            }
        }
        
        return costs.get(self.level, costs[HardeningLevel.ADVANCED])
    
    def export_guide(self, guide: Dict, output_path: str = "hardening/guide.json"):
        """Export hardening guide"""
        try:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w') as f:
                json.dump(guide, f, indent=2, default=str)
            logger.info(f"Hardening guide exported to {output_path}")
        except Exception as e:
            logger.error(f"Failed to export guide: {e}")


if __name__ == "__main__":
    # Test hardening guide
    guide_gen = PrivacyHardeningGuide(level=HardeningLevel.ADVANCED)
    
    identity = {"name": "John Smith"}
    guide = guide_gen.generate_comprehensive_guide(identity)
    guide_gen.export_guide(guide)
    
    print(f"✓ Generated {guide['level']} privacy hardening guide")
    print(f"✓ Timeline: {guide['implementation_timeline']['total_weeks']} weeks")
    print(f"✓ Annual cost: ${guide['estimated_cost']['annual']}")
