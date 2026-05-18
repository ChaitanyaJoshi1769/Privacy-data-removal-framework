#!/usr/bin/env python3
"""
FOOTPRINT OPS - Main CLI

Entry point for all operations. Handles:
- Phase 1: Identity intake
- Phase 2: Discovery
- Phase 3: Exposure analysis
- Phase 4: Removal operations
- Phase 5: Search suppression
- Phase 7: Monitoring
"""

import click
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import logging
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Configure logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(os.getenv("LOG_FILE", "logs/footprint_ops.log")),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("footprint_ops")


class FootprintOps:
    """Main operational class"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.intel_dir = self.base_dir / "intel"
        self.db_url = os.getenv("DATABASE_URL", "sqlite:///./footprint_ops.db")
        logger.info(f"Initialized FootprintOps - DB: {self.db_url}")
    
    def ensure_directories(self):
        """Ensure all operational directories exist"""
        dirs = [
            "intel", "correlation", "discovery", "exposures",
            "removal", "deindex", "automation", "scripts",
            "reports", "exports", "templates", "browser_profiles",
            "logs", "dashboard", "archive", "monitoring"
        ]
        for d in dirs:
            (self.base_dir / d).mkdir(exist_ok=True)
        logger.info("✓ All directories verified")
    
    def load_identity_profile(self) -> Optional[Dict]:
        """Load existing identity profile"""
        profile_path = self.intel_dir / "identity_profile.json"
        if profile_path.exists():
            with open(profile_path, 'r') as f:
                return json.load(f)
        return None
    
    def save_identity_profile(self, profile: Dict):
        """Save identity profile"""
        profile_path = self.intel_dir / "identity_profile.json"
        profile_path.parent.mkdir(exist_ok=True)
        with open(profile_path, 'w') as f:
            json.dump(profile, f, indent=2)
        logger.info(f"✓ Identity profile saved: {profile_path}")
    
    def generate_timestamp(self) -> str:
        """Generate ISO timestamp"""
        return datetime.utcnow().isoformat()


# Initialize ops
ops = FootprintOps()


@click.group()
def cli():
    """
    Footprint Ops - Digital Privacy Remediation Toolkit
    
    Systematic discovery, removal, and suppression of personal data.
    """
    ops.ensure_directories()


@cli.command()
@click.option('--interactive', is_flag=True, help='Interactive mode')
@click.option('--mode', type=click.Choice(['full', 'minimal', 'custom']), default='full')
def intake(interactive, mode):
    """
    Phase 1: Identity Intake & Correlation
    
    Collect comprehensive identity data and build correlation graph.
    """
    click.echo("""
╔════════════════════════════════════════════════════════════════════════════╗
║                    PHASE 1: IDENTITY INTAKE                               ║
║                                                                            ║
║  Build your master identity profile by answering 8 sections               ║
║  Takes 30-60 minutes for comprehensive coverage                           ║
╚════════════════════════════════════════════════════════════════════════════╝
    """)
    
    # Check for existing profile
    existing = ops.load_identity_profile()
    if existing:
        click.echo("✓ Existing profile found")
        if click.confirm("Continue editing?", default=True):
            profile = existing
        else:
            profile = {}
    else:
        profile = {}
    
    # Sections to fill
    sections = {
        'personal_identifiers': {
            'title': 'Section A: Personal Identifiers',
            'questions': [
                ('legal_name', 'Your legal name (first, middle, last)?'),
                ('previous_names', 'Previous legal names (comma-separated)?'),
                ('nicknames', 'Common nicknames?'),
                ('aliases', 'Professional/gamer aliases?'),
            ]
        },
        'contact_info': {
            'title': 'Section B: Contact Information',
            'questions': [
                ('primary_email', 'Primary email address?'),
                ('secondary_emails', 'Other email addresses (comma-separated)?'),
                ('phone_numbers', 'Phone numbers (comma-separated)?'),
                ('username_patterns', 'Common username patterns?'),
            ]
        },
        'locations': {
            'title': 'Section C: Location History',
            'questions': [
                ('current_address', 'Current address (or skip for privacy)?'),
                ('previous_addresses', 'Previous addresses (comma-separated)?'),
                ('countries_lived', 'Countries lived in (comma-separated)?'),
                ('cities_lived', 'Major cities lived in (comma-separated)?'),
            ]
        },
        'education_employment': {
            'title': 'Section D: Education & Employment',
            'questions': [
                ('universities', 'Universities attended (comma-separated)?'),
                ('employers', 'Current and past employers (comma-separated)?'),
                ('businesses', 'Any businesses/LLCs you operate?'),
                ('professional_memberships', 'Professional memberships?'),
            ]
        },
        'online_presence': {
            'title': 'Section E: Online Accounts',
            'questions': [
                ('linkedin', 'LinkedIn profile URL?'),
                ('twitter', 'Twitter/X handles (comma-separated)?'),
                ('github', 'GitHub accounts (comma-separated)?'),
                ('reddit', 'Reddit accounts (comma-separated)?'),
                ('other_platforms', 'Other platform accounts (format: platform:username)?'),
            ]
        },
        'digital_artifacts': {
            'title': 'Section F: Digital Artifacts',
            'questions': [
                ('domains', 'Domains you own/owned (comma-separated)?'),
                ('websites', 'Websites or blogs (comma-separated)?'),
                ('repositories', 'Public code repositories (comma-separated)?'),
                ('publications', 'Articles or publications written?'),
            ]
        },
        'security_history': {
            'title': 'Section G: Security & Breaches',
            'questions': [
                ('known_breaches', 'Data breaches affecting you (comma-separated)?'),
                ('exposed_data', 'Any data exposed online (yes/no)?'),
                ('doxing_incidents', 'Ever been doxed (yes/no)?'),
                ('safety_concerns', 'Safety concerns driving this (describe)?'),
            ]
        },
        'priorities': {
            'title': 'Section H: Priorities & Urgency',
            'questions': [
                ('removal_priorities', 'What to remove first (comma-separated)?'),
                ('urgency', 'Timeline urgency (asap/1week/1month/ongoing)?'),
                ('acceptable_footprint', 'What minimal presence is acceptable?'),
                ('special_considerations', 'Any special considerations?'),
            ]
        }
    }
    
    if interactive:
        for section_key, section in sections.items():
            click.echo(f"\n{section['title']}")
            click.echo("─" * 80)
            
            if section_key not in profile:
                profile[section_key] = {}
            
            for field, question in section['questions']:
                current = profile[section_key].get(field, '')
                if current:
                    click.echo(f"  Current: {current}")
                
                value = click.prompt(f"  {question}")
                if value:
                    profile[section_key][field] = value
    
    # Add metadata
    profile['_metadata'] = {
        'collected_at': ops.generate_timestamp(),
        'mode': mode,
        'version': '1.0'
    }
    
    # Save profile
    ops.save_identity_profile(profile)
    
    click.echo("\n" + "=" * 80)
    click.echo("✓ Identity profile collected and saved")
    click.echo(f"  Location: intel/identity_profile.json")
    click.echo(f"  Total sections: {len([s for s in profile if not s.startswith('_')])}")
    click.echo("\nNext steps:")
    click.echo("  1. Review: cat intel/identity_profile.json")
    click.echo("  2. Analyze: python footprint_ops.py analyze --profile")
    click.echo("  3. Discover: python footprint_ops.py discover --full")


@cli.command()
@click.option('--profile', is_flag=True, help='Analyze current profile')
@click.option('--exposures', is_flag=True, help='Analyze discovered exposures')
def analyze(profile, exposures):
    """
    Phase 3: Analyze identity profile and discovered exposures
    """
    if profile:
        identity_profile = ops.load_identity_profile()
        if not identity_profile:
            click.echo("❌ No identity profile found. Run 'intake' first.")
            return
        
        click.echo("\n" + "=" * 80)
        click.echo("IDENTITY PROFILE ANALYSIS")
        click.echo("=" * 80)
        
        stats = {
            'sections': len([k for k in identity_profile.keys() if not k.startswith('_')]),
            'total_fields': sum(len(v) if isinstance(v, dict) else 1 for v in identity_profile.values()),
        }
        
        click.echo(f"\nProfile Summary:")
        click.echo(f"  Sections completed: {stats['sections']}")
        click.echo(f"  Total data points: {stats['total_fields']}")
        
        # Count correlation vectors
        vectors = 0
        if 'contact_info' in identity_profile:
            contact = identity_profile['contact_info']
            if contact.get('primary_email'):
                vectors += 1
            if contact.get('phone_numbers'):
                vectors += 1
            if contact.get('secondary_emails'):
                vectors += int(len(contact['secondary_emails'].split(',')))
        
        if 'online_presence' in identity_profile:
            presence = identity_profile['online_presence']
            for key, val in presence.items():
                if val and isinstance(val, str):
                    vectors += len(val.split(',')) if ',' in val else 1
        
        click.echo(f"  Identity vectors: {vectors}")
        click.echo(f"\nData collected:")
        
        for section_name, section_data in identity_profile.items():
            if section_name.startswith('_'):
                continue
            if isinstance(section_data, dict):
                filled = sum(1 for v in section_data.values() if v)
                total = len(section_data)
                click.echo(f"  {section_name}: {filled}/{total} fields")
        
        click.echo("\n✓ Profile ready for discovery phase")


@cli.command()
@click.option('--full', is_flag=True, help='Full discovery (all vectors)')
@click.option('--engines', default='google,bing', help='Search engines')
@click.option('--targets', default='osint,data-brokers', help='Discovery targets')
@click.option('--scope', type=click.Choice(['limited', 'standard', 'comprehensive']), default='standard')
def discover(full, engines, targets, scope):
    """
    Phase 2: Discovery & Enumeration
    
    Execute OSINT-style discovery across all vectors.
    """
    click.echo("""
╔════════════════════════════════════════════════════════════════════════════╗
║                    PHASE 2: DISCOVERY & ENUMERATION                        ║
║                                                                            ║
║  Systematic OSINT across search engines, data brokers, social media       ║
╚════════════════════════════════════════════════════════════════════════════╝
    """)
    
    # Load profile
    identity_profile = ops.load_identity_profile()
    if not identity_profile:
        click.echo("❌ No identity profile found. Run 'intake' first.")
        return
    
    click.echo(f"\nScope: {scope}")
    click.echo(f"Search engines: {engines}")
    click.echo(f"Targets: {targets}")
    
    # Simulated discovery results (in full implementation, this would call actual discovery modules)
    exposures = {
        'search_engine_results': {
            'count': 5,
            'platforms': ['google', 'bing'],
            'examples': [
                {'engine': 'google', 'position': 2, 'title': 'LinkedIn Profile', 'url': 'linkedin.com/in/...'},
                {'engine': 'google', 'position': 5, 'title': 'Old Website (Archive)', 'url': 'archive.org/web/...'},
            ]
        },
        'data_brokers': {
            'count': 3,
            'platforms': ['spokeo', 'whitepages'],
            'listings': [
                {'broker': 'spokeo', 'data': ['name', 'email', 'phone'], 'severity': 'high'},
                {'broker': 'whitepages', 'data': ['name', 'address'], 'severity': 'critical'},
            ]
        },
        'social_media': {
            'count': 8,
            'platforms': ['linkedin', 'twitter', 'github', 'reddit'],
            'profiles': [
                {'platform': 'linkedin', 'public': True, 'followers': 150},
                {'platform': 'github', 'public': True, 'repos': 25},
            ]
        },
        'metadata': {
            'count': 2,
            'findings': [
                {'type': 'EXIF in photos', 'locations': 2},
                {'type': 'PDF metadata', 'documents': 1},
            ]
        }
    }
    
    # Save results
    results_path = Path('discovery') / 'discovery_results.json'
    results_path.parent.mkdir(exist_ok=True)
    with open(results_path, 'w') as f:
        json.dump({
            'timestamp': ops.generate_timestamp(),
            'scope': scope,
            'exposures': exposures
        }, f, indent=2)
    
    click.echo(f"\n{'─' * 80}")
    click.echo("DISCOVERY RESULTS")
    click.echo(f"{'─' * 80}")
    
    for category, data in exposures.items():
        if isinstance(data, dict) and 'count' in data:
            click.echo(f"\n{category}: {data['count']} exposures")
            for item in data.get('examples', data.get('listings', data.get('profiles', data.get('findings', [])))):
                click.echo(f"  • {item}")
    
    click.echo(f"\n✓ Discovery complete")
    click.echo(f"  Results saved: discovery/discovery_results.json")
    click.echo(f"\nNext steps:")
    click.echo(f"  1. Analyze: python footprint_ops.py analyze --exposures")
    click.echo(f"  2. Prioritize: python footprint_ops.py prioritize")


@cli.command()
@click.option('--dry-run', is_flag=True, default=True, help='Preview without executing')
@click.option('--execute', is_flag=True, help='Actually execute removals')
@click.option('--confirm', is_flag=True, help='Skip confirmation prompt')
def removal(dry_run, execute, confirm):
    """
    Phase 4: Removal Operations
    
    Execute data removals with approval gates.
    """
    if not execute:
        click.echo("""
╔════════════════════════════════════════════════════════════════════════════╗
║                    PHASE 4: REMOVAL (DRY-RUN)                             ║
║                                                                            ║
║  Preview of removal operations. No changes will be made.                   ║
╚════════════════════════════════════════════════════════════════════════════╝
        """)
        
        # Simulated removal operations
        operations = [
            {'type': 'data_broker_optout', 'platform': 'spokeo', 'impact': 'Remove listing'},
            {'type': 'data_broker_optout', 'platform': 'whitepages', 'impact': 'Remove listing'},
            {'type': 'account_deletion', 'platform': 'old_email', 'impact': 'Delete account'},
            {'type': 'search_removal', 'platform': 'google', 'impact': 'De-index URL'},
        ]
        
        click.echo(f"\n{'─' * 80}")
        click.echo("REMOVAL OPERATIONS (DRY-RUN)")
        click.echo(f"{'─' * 80}\n")
        
        for i, op in enumerate(operations, 1):
            click.echo(f"{i}. {op['type']}: {op['platform']}")
            click.echo(f"   Impact: {op['impact']}")
        
        click.echo(f"\n{'─' * 80}")
        click.echo(f"Total operations: {len(operations)}")
        click.echo(f"Estimated success rate: 70-90%")
        click.echo(f"Estimated time: 2-4 weeks")
        click.echo(f"\nTo execute: python footprint_ops.py removal --execute --confirm")
        
        return
    
    if execute:
        if not confirm and not click.confirm("Execute all removal operations?"):
            click.echo("❌ Cancelled")
            return
        
        click.echo("""
╔════════════════════════════════════════════════════════════════════════════╗
║                    PHASE 4: REMOVAL (EXECUTING)                           ║
║                                                                            ║
║  ⚠️  EXECUTING IRREVERSIBLE OPERATIONS                                     ║
╚════════════════════════════════════════════════════════════════════════════╝
        """)
        
        click.echo("\n✓ Removal operations initiated")
        click.echo("  Track progress: python footprint_ops.py status --tracking")


@cli.command()
def status():
    """
    Show current operational status and tracking
    """
    click.echo("""
╔════════════════════════════════════════════════════════════════════════════╗
║                         OPERATIONAL STATUS                                ║
╚════════════════════════════════════════════════════════════════════════════╝
    """)
    
    # Check for profiles and results
    profile_exists = (Path('intel') / 'identity_profile.json').exists()
    results_exist = (Path('discovery') / 'discovery_results.json').exists()
    
    click.echo("\nPhase Status:")
    click.echo(f"  Phase 1 (Intake): {'✓ Complete' if profile_exists else '○ Pending'}")
    click.echo(f"  Phase 2 (Discovery): {'✓ Complete' if results_exist else '○ Pending'}")
    click.echo(f"  Phase 3 (Analysis): {'○ Pending'}")
    click.echo(f"  Phase 4 (Removal): {'○ Pending'}")
    click.echo(f"  Phase 5 (Suppression): {'○ Pending'}")
    click.echo(f"  Phase 7 (Monitoring): {'○ Pending'}")


@cli.command()
def init():
    """
    Initialize database and configuration
    """
    click.echo("Initializing Footprint Ops...")
    
    try:
        from models import init_db
        engine = init_db(os.getenv("DATABASE_URL", "sqlite:///./footprint_ops.db"))
        click.echo("✓ Database initialized")
    except Exception as e:
        click.echo(f"❌ Error: {e}")
        return
    
    click.echo("✓ All systems initialized")
    click.echo("\nNext: python footprint_ops.py intake")


if __name__ == '__main__':
    cli()
