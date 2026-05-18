#!/usr/bin/env python3
"""
Privacy Request Generation - Phase 4b

Generates legally compliant privacy requests for:
- CCPA (California Consumer Privacy Act)
- GDPR (EU General Data Protection Regulation)
- DPIA (Data Protection Impact Assessment)
- PIPEDA (Canada)

Features:
- Template generation
- Personalization
- Email formatting
- Document export
- Tracking
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime
from enum import Enum
from pathlib import Path
import json

logger = logging.getLogger(__name__)


class PrivacyLaw(str, Enum):
    """Privacy regulations"""
    CCPA = "ccpa"  # California Consumer Privacy Act
    GDPR = "gdpr"  # EU General Data Protection Regulation
    PIPEDA = "pipeda"  # Canada Personal Information Protection Act
    DPIA = "dpia"  # Data Protection Impact Assessment


class PrivacyRequestGenerator:
    """Generates privacy requests for data removal"""
    
    def __init__(self):
        """Initialize privacy request generator"""
        self.requests = []
    
    def generate_ccpa_request(self, name: str, email: str, phone: Optional[str] = None, 
                            platform: str = "Unknown Company") -> Dict:
        """
        Generate CCPA (California Consumer Privacy Act) request
        
        Args:
            name: User name
            email: User email
            phone: User phone (optional)
            platform: Company/platform name
        
        Returns:
            CCPA request document
        """
        
        request = {
            "type": "CCPA_REQUEST",
            "law": "California Consumer Privacy Act (CCPA)",
            "date": datetime.now().isoformat(),
            "user_name": name,
            "user_email": email,
            "user_phone": phone,
            "platform": platform,
            "subject_line": "Consumer Request for Deletion of Personal Information (CCPA)",
            "body": f"""
Dear {platform} Data Privacy Team,

I am a California resident and am submitting this request pursuant to the California Consumer Privacy Act (CCPA), 
specifically California Civil Code Section 1798.100.

I request that you delete all personal information collected from me and retained in your system, including:

PERSONAL INFORMATION TO BE DELETED:
- Full Name: {name}
- Email Address(es): {email}
{f"- Phone Number: {phone}" if phone else ""}
- Any aliases or usernames associated with the above
- Account IDs or unique identifiers
- Browsing and purchase history
- Geolocation data
- Biometric data (if applicable)
- Inferred preferences and characteristics
- All other personal information as defined under CCPA

REQUIREMENT:
You must delete or direct your service providers to delete the personal information I have provided 
in this request, except where an exception under CCPA Section 1798.105(d) applies.

VERIFICATION:
I declare under penalty of perjury under the laws of the State of California that the information 
I have provided in this request is true and correct.

Please confirm receipt and processing of this request within 10 business days and provide written 
confirmation of deletion within 45 days of receipt of this request.

Thank you,
{name}
{email}
{f"{phone}" if phone else ""}

Date: {datetime.now().strftime("%B %d, %Y")}
            """
        }
        
        self.requests.append(request)
        logger.info(f"Generated CCPA request for {platform}")
        return request
    
    def generate_gdpr_request(self, name: str, email: str, phone: Optional[str] = None,
                            platform: str = "Unknown Company") -> Dict:
        """
        Generate GDPR (EU General Data Protection Regulation) request
        
        Args:
            name: User name
            email: User email
            phone: User phone (optional)
            platform: Company/platform name
        
        Returns:
            GDPR request document
        """
        
        request = {
            "type": "GDPR_REQUEST",
            "law": "General Data Protection Regulation (GDPR)",
            "date": datetime.now().isoformat(),
            "user_name": name,
            "user_email": email,
            "user_phone": phone,
            "platform": platform,
            "subject_line": "Data Subject Access Request and Right to Erasure (GDPR Articles 17 & 21)",
            "body": f"""
Dear {platform} Data Protection Officer / Privacy Team,

I am writing to exercise my rights as a data subject under the General Data Protection Regulation (GDPR), 
specifically Articles 17 (Right to Erasure) and 21 (Right to Object).

REQUEST FOR ERASURE OF PERSONAL DATA:

Pursuant to GDPR Article 17, I request the erasure of all personal data you hold concerning me, including:

PERSONAL DATA SUBJECT TO ERASURE:
- Full Name: {name}
- Email Address(es): {email}
{f"- Phone Number: {phone}" if phone else ""}
- Any aliases or alternative identifiers
- Account numbers and user IDs
- Transaction history and payment information
- Communications and support tickets
- Cookies and tracking data
- IP addresses and device identifiers
- Location history
- Behavioral and preference data
- Any other personal data as defined under GDPR Article 4

LEGAL BASIS FOR ERASURE:
- Article 17(1)(a): The personal data is no longer necessary
- Article 17(1)(b): Withdrawal of consent
- Article 17(1)(c): Objection to processing

REQUIREMENTS:
1. Confirm receipt within 10 working days
2. Erase all personal data within 30 days of receipt
3. Inform all recipients of the erasure request
4. Confirm completion in writing

CONSEQUENCES:
Please note that failure to comply with this request within the specified timeframe may result in:
- Formal complaint to the relevant Data Protection Authority
- Potential fines under GDPR Article 83

I reserve the right to lodge a complaint with my national Data Protection Authority if this request 
is not honored within the specified timeframe.

Yours faithfully,
{name}
{email}
{f"{phone}" if phone else ""}

Date: {datetime.now().strftime("%d %B %Y")}
            """
        }
        
        self.requests.append(request)
        logger.info(f"Generated GDPR request for {platform}")
        return request
    
    def generate_pipeda_request(self, name: str, email: str, phone: Optional[str] = None,
                               platform: str = "Unknown Company") -> Dict:
        """
        Generate PIPEDA (Canada) request
        
        Args:
            name: User name
            email: User email
            phone: User phone (optional)
            platform: Company/platform name
        
        Returns:
            PIPEDA request document
        """
        
        request = {
            "type": "PIPEDA_REQUEST",
            "law": "Personal Information Protection and Electronic Documents Act (PIPEDA)",
            "date": datetime.now().isoformat(),
            "user_name": name,
            "user_email": email,
            "user_phone": phone,
            "platform": platform,
            "subject_line": "Request for Deletion of Personal Information (PIPEDA Principle 4.3)",
            "body": f"""
Dear {platform} Privacy Officer,

I am submitting a request for deletion of personal information under the Personal Information Protection 
and Electronic Documents Act (PIPEDA), specifically Principle 4.3 regarding Accuracy of Personal Information.

REQUEST FOR DELETION:

I request the deletion of all personal information you maintain about me, including:

PERSONAL INFORMATION TO BE DELETED:
- Full Name: {name}
- Email Address(es): {email}
{f"- Phone Number: {phone}" if phone else ""}
- Account identifiers
- Transaction records
- Communications
- Device and location data
- Usage patterns and preferences
- Any related personal information

BASIS FOR REQUEST:
Under PIPEDA Principle 4.3, organizations must ensure personal information is as accurate, 
complete, and current as possible. Deletion of unnecessary information is necessary for compliance.

TIMELINE:
Please acknowledge receipt within 30 days and complete deletion within 60 days of receipt.

Thank you,
{name}
{email}
{f"{phone}" if phone else ""}

Date: {datetime.now().strftime("%B %d, %Y")}
            """
        }
        
        self.requests.append(request)
        logger.info(f"Generated PIPEDA request for {platform}")
        return request
    
    def generate_batch_requests(self, identity: Dict, platforms: List[str], 
                               laws: List[str] = None) -> Dict:
        """
        Generate batch privacy requests for multiple platforms
        
        Args:
            identity: Identity profile with name, email, phone
            platforms: List of platforms to request
            laws: List of privacy laws to use (default: all)
        
        Returns:
            Batch request summary
        """
        
        if laws is None:
            laws = ["ccpa", "gdpr"]
        
        batch = {
            "timestamp": datetime.now().isoformat(),
            "identity_name": identity.get("name"),
            "identity_email": identity.get("email"),
            "platforms": platforms,
            "laws": laws,
            "requests_generated": [],
            "total_requests": 0
        }
        
        name = identity.get("name", "User")
        email = identity.get("email", "user@example.com")
        phone = identity.get("phone")
        
        # Generate requests for each platform and law
        for platform in platforms:
            for law in laws:
                if law == "ccpa":
                    req = self.generate_ccpa_request(name, email, phone, platform)
                elif law == "gdpr":
                    req = self.generate_gdpr_request(name, email, phone, platform)
                elif law == "pipeda":
                    req = self.generate_pipeda_request(name, email, phone, platform)
                else:
                    continue
                
                batch["requests_generated"].append({
                    "platform": platform,
                    "law": law,
                    "subject": req["subject_line"]
                })
        
        batch["total_requests"] = len(batch["requests_generated"])
        logger.info(f"Generated {batch['total_requests']} privacy requests")
        return batch
    
    def export_requests(self, output_dir: str = "templates/privacy_requests"):
        """
        Export all generated requests to files
        
        Args:
            output_dir: Directory to save requests
        """
        try:
            Path(output_dir).mkdir(parents=True, exist_ok=True)
            
            for i, request in enumerate(self.requests):
                filename = f"{request['type'].lower()}_{i+1}_{request['platform'].lower().replace(' ', '_')}.txt"
                filepath = Path(output_dir) / filename
                
                # Write body to file
                with open(filepath, 'w') as f:
                    f.write(f"Subject: {request['subject_line']}\n\n")
                    f.write(request['body'])
                
                logger.info(f"Exported request to {filepath}")
            
            # Export JSON summary
            summary = {
                "timestamp": datetime.now().isoformat(),
                "total_requests": len(self.requests),
                "requests": [
                    {
                        "type": r["type"],
                        "law": r["law"],
                        "platform": r["platform"],
                        "user_email": r["user_email"],
                        "subject": r["subject_line"]
                    }
                    for r in self.requests
                ]
            }
            
            summary_path = Path(output_dir) / "summary.json"
            with open(summary_path, 'w') as f:
                json.dump(summary, f, indent=2)
            
            logger.info(f"Privacy requests exported to {output_dir}")
        
        except Exception as e:
            logger.error(f"Failed to export requests: {e}")


class DataBrokerOptOutGenerator:
    """Generates data broker opt-out requests"""
    
    def __init__(self):
        """Initialize opt-out generator"""
        self.optouts = []
    
    def generate_optout_template(self, name: str, email: str, phone: str,
                                broker: str) -> Dict:
        """Generate broker-specific opt-out template"""
        
        optout = {
            "type": "OPTOUT_REQUEST",
            "broker": broker,
            "date": datetime.now().isoformat(),
            "user_name": name,
            "user_email": email,
            "user_phone": phone,
            "instructions": self._get_broker_instructions(broker),
            "notes": f"Opt-out request for {name} from {broker}"
        }
        
        self.optouts.append(optout)
        logger.info(f"Generated opt-out template for {broker}")
        return optout
    
    def _get_broker_instructions(self, broker: str) -> Dict:
        """Get broker-specific opt-out instructions"""
        
        instructions = {
            "spokeo": {
                "url": "https://www.spokeo.com/optout",
                "method": "online_form",
                "difficulty": "easy",
                "time_estimate_days": 3,
                "steps": [
                    "1. Visit https://www.spokeo.com/optout",
                    "2. Enter your name and email",
                    "3. Click 'Remove My Information'",
                    "4. Verify via email",
                    "5. Confirm removal"
                ]
            },
            "whitepages": {
                "url": "https://www.whitepages.com/suppression_requests",
                "method": "online_form",
                "difficulty": "easy",
                "time_estimate_days": 3,
                "steps": [
                    "1. Visit https://www.whitepages.com/suppression_requests",
                    "2. Submit suppression request",
                    "3. Provide name and email",
                    "4. Verify request",
                    "5. Monitor for removal"
                ]
            },
            "intelius": {
                "url": "https://www.intelius.com/opt-out",
                "method": "online_form",
                "difficulty": "medium",
                "time_estimate_days": 7,
                "steps": [
                    "1. Go to https://www.intelius.com/opt-out",
                    "2. Enter personal information",
                    "3. Submit opt-out request",
                    "4. Wait for processing",
                    "5. Verify removal"
                ]
            },
            "mylife": {
                "url": "https://www.mylife.com/optout",
                "method": "online_form",
                "difficulty": "medium",
                "time_estimate_days": 7,
                "steps": [
                    "1. Visit https://www.mylife.com/optout",
                    "2. Search for your profile",
                    "3. Click 'Remove My Profile'",
                    "4. Verify your identity",
                    "5. Confirm removal"
                ]
            }
        }
        
        return instructions.get(broker.lower(), {
            "url": f"https://{broker.lower()}.com/optout",
            "method": "manual",
            "difficulty": "unknown",
            "time_estimate_days": 7,
            "steps": ["Visit the site's privacy/opt-out page", "Follow their removal process"]
        })


def generate_privacy_requests(name: str, email: str, phone: Optional[str] = None,
                             platforms: List[str] = None) -> Dict:
    """Convenience function to generate privacy requests"""
    
    if platforms is None:
        platforms = ["Spokeo", "Whitepages", "MyLife", "Intelius"]
    
    generator = PrivacyRequestGenerator()
    
    identity = {
        "name": name,
        "email": email,
        "phone": phone
    }
    
    batch = generator.generate_batch_requests(identity, platforms, ["ccpa", "gdpr"])
    generator.export_requests()
    
    return batch


if __name__ == "__main__":
    # Test privacy request generation
    generator = PrivacyRequestGenerator()
    
    # Generate CCPA request
    ccpa_req = generator.generate_ccpa_request(
        name="John Smith",
        email="john.smith@example.com",
        phone="+1-555-0123",
        platform="Spokeo"
    )
    
    # Generate GDPR request
    gdpr_req = generator.generate_gdpr_request(
        name="John Smith",
        email="john.smith@example.com",
        platform="Whitepages"
    )
    
    # Export all requests
    generator.export_requests()
    
    print(f"✓ Generated {len(generator.requests)} privacy requests")
    print(f"✓ Requests exported to templates/privacy_requests/")
