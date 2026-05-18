# Privacy Framework Automation Guide

Complete reference for all automated tools and scripts in the privacy remediation framework.

## Quick Start

### 1. Install Dependencies
```bash
pip install requests
```

### 2. Run Monitoring
```python
python automation_cli.py monitor --check all
```

### 3. Generate Removal Plan
```python
python automation_cli.py removal --plan
```

## Available Automation Tools

### 1. HIBP Breach Monitor (`hibp_monitor.py`)

**Purpose**: Automated checking for data breaches using Have I Been Pwned API

**Key Functions**:
- `check_email_breaches(email)` - Check if email appears in breaches
- `check_password_pwned(password)` - Check if password is compromised
- `check_domain_breaches(domain)` - Check all breaches for domain
- `generate_report(identity)` - Comprehensive breach assessment

**Usage**:
```python
from hibp_monitor import HIBPMonitor

monitor = HIBPMonitor()
identity = {
    "name": "Chaitanya Joshi",
    "email": "chaitanyajoshi15@gmail.com",
    "domain": "gmail.com"
}

report = monitor.generate_report(identity)
monitor.save_log("logs/hibp_breaches.json")
```

**Key Features**:
- Rate limiting (respects HIBP API limits: 1 request per 1.5 seconds)
- Risk assessment (GREEN/YELLOW/RED)
- Action recommendations
- JSON export for tracking

**Output**: 
```json
{
  "email": "chaitanyajoshi15@gmail.com",
  "breached": true/false,
  "breach_count": 0,
  "risk_level": "GREEN|YELLOW|RED",
  "action_required": false,
  "breaches": []
}
```

### 2. Google Search Console Removal (`gsc_removal_agent.py`)

**Purpose**: Automate URL removal requests from Google Search results

**Key Functions**:
- `request_url_removal(url, reason)` - Submit URL for removal
- `request_cache_purge(url)` - Request cache purge
- `generate_removal_plan(urls, priority)` - Prioritized removal plan
- `create_robots_txt_blocking(patterns)` - Generate robots.txt content
- `generate_verification_checklist()` - Removal verification steps

**Usage**:
```python
from gsc_removal_agent import GSCRemovalAgent

agent = GSCRemovalAgent()
urls = ["https://github.com/ChaitanyaJoshi1769"]
plan = agent.generate_removal_plan(urls, priority="high")
agent.save_plan(plan)
```

**Timeline**: 3-6 months for full removal from search results

**Verification**:
1. Check Google Search results (should show zero results)
2. Check Google Cache (should return 404)
3. Verify robots.txt blocking
4. Monitor GSC removal request status

### 3. Bing Webmaster Tools (`bing_removal_agent.py`)

**Purpose**: Automate URL removal from Bing Search

**Key Functions**:
- `request_url_removal(url)` - Submit disavow request
- `generate_removal_batch(urls)` - Batch removal plan
- `create_disavow_file(urls)` - Generate disavow file content
- `generate_verification_guide()` - Verification procedures

**Usage**:
```python
from bing_removal_agent import BingRemovalAgent

agent = BingRemovalAgent()
batch = agent.generate_removal_batch(urls)
agent.export_summary()
```

**Timeline**: 1-4 weeks for removal

**Verification**:
1. Bing Search: site:github.com/ChaitanyaJoshi1769
2. Bing Webmaster Tools: URL Inspection
3. Search Traffic reports

### 4. Monitoring Orchestrator (`monitoring_orchestrator.py`)

**Purpose**: Centralized coordination of all monitoring jobs

**Key Functions**:
- `setup_daily_checks()` - Register daily monitoring jobs
- `setup_weekly_checks()` - Register weekly checks
- `setup_monthly_checks()` - Register monthly audits
- `simulate_daily_run()` - Test monitoring pipeline
- `generate_monitoring_report()` - Comprehensive report

**Monitoring Schedule**:

**Daily**:
- HIBP breach check (3:00 AM UTC)
- Search engine monitoring (6:00 AM UTC)
- Archive.org scanning (9:00 AM UTC)

**Weekly**:
- Data broker rescan (Monday, 2:00 AM UTC)
- Social media audit (Wednesday, 10:00 AM UTC)
- Removal verification (Friday, 2:00 PM UTC)

**Monthly**:
- Credit report monitoring (1st day)
- Dark web scanning (15th day)
- Comprehensive privacy audit (20th day)

**Usage**:
```python
from monitoring_orchestrator import MonitoringOrchestrator

identity = {
    "name": "Chaitanya Joshi",
    "email": "chaitanyajoshi15@gmail.com",
    "github_username": "ChaitanyaJoshi1769"
}

orchestrator = MonitoringOrchestrator(identity)
orchestrator.setup_daily_checks()
orchestrator.setup_weekly_checks()
orchestrator.setup_monthly_checks()

report = orchestrator.generate_monitoring_report()
orchestrator.export_all_data()
```

### 5. Data Broker Automation (`data_broker_automation.py`)

**Purpose**: Automate searches and removal tracking across 9 major data brokers

**Supported Brokers** (9 total):
1. Spokeo (14 days, hard)
2. White Pages (14 days, medium)
3. Intelius (21 days, hard)
4. MyLife (30 days, medium)
5. TrueCaller (7 days, easy)
6. PeopleFinder (14 days, medium)
7. US Search (21 days, hard)
8. FamilyTreeNow (30 days, medium)
9. ZoomInfo (14 days, medium)

**Key Functions**:
- `search_all_brokers()` - Search for identity across all brokers
- `search_broker(broker_id)` - Search specific broker
- `submit_removal(broker_id, confirmation_num)` - Log removal submission
- `verify_removal(broker_id, verified)` - Track removal completion
- `generate_removal_plan(prioritize_by)` - Phased removal plan
- `get_summary()` - Status summary

**Usage**:
```python
from data_broker_automation import DataBrokerAutomation

automation = DataBrokerAutomation({
    "name": "Chaitanya Joshi",
    "email": "chaitanyajoshi15@gmail.com"
})

# Generate phased plan
plan = automation.generate_removal_plan(prioritize_by="difficulty")

# Search all brokers
results = automation.search_all_brokers()

# Track removal
automation.submit_removal("spokeo", confirmation_num="ABC123")
automation.verify_removal("spokeo", verified=True)

# Get status
summary = automation.get_summary()
```

**Removal Phases**:
- Phase 1: Easy removals (7 days) - TrueCaller
- Phase 2: Medium removals (14 days) - Spokeo, White Pages, PeopleFinder, MyLife, ZoomInfo
- Phase 3: Hard removals (21 days) - Intelius, US Search, FamilyTreeNow

### 6. Automation CLI (`automation_cli.py`)

**Purpose**: Central command-line interface for all automation operations

**Commands**:
```bash
# Monitoring
python automation_cli.py monitor --check hibp --email your@email.com
python automation_cli.py monitor --check all

# Removal operations
python automation_cli.py removal --list          # List brokers
python automation_cli.py removal --plan          # Generate plan
python automation_cli.py removal --search        # Search all brokers

# Search de-indexing
python automation_cli.py deindex --provider google
python automation_cli.py deindex --provider bing
python automation_cli.py deindex --provider both

# Auditing
python automation_cli.py audit --type github
python automation_cli.py audit --type search
python automation_cli.py audit --type all --full

# Reporting
python automation_cli.py report --type progress --period weekly
python automation_cli.py report --type monitoring
python automation_cli.py report --type summary

# Dashboard
python automation_cli.py dashboard
python automation_cli.py dashboard --export
```

### 7. Supporting Tools

**broker_tracker.py** - Track removal status across all 9 brokers
```python
from broker_tracker import DataBrokerTracker

tracker = DataBrokerTracker()
tracker.init_tracking()
tracker.log_submission("spokeo", "ABC123")
tracker.log_verification("spokeo", True)
summary = tracker.get_summary()
tracker.export_to_csv("broker_tracking.csv")
```

**exposure_scanner.py** - Automated exposure discovery
```python
from exposure_scanner import ExposureScanner

scanner = ExposureScanner()
report = scanner.generate_report()
```

**progress_reporter.py** - Progress tracking and reporting
```python
from progress_reporter import ProgressReporter

reporter = ProgressReporter()
weekly = reporter.generate_weekly_report()
monthly = reporter.generate_monthly_report()
```

**privacy_audit.py** - Privacy configuration auditing
```python
from privacy_audit import PrivacyAudit

audit = PrivacyAudit()
github_audit = audit.audit_github()
search_audit = audit.audit_search_engines()
report = audit.generate_audit_report()
```

## Workflow Examples

### Complete Privacy Remediation Workflow

```bash
# Day 1: Audit and Planning
python automation_cli.py audit --type all --full
python automation_cli.py removal --plan
python automation_cli.py deindex --provider both

# Days 2-28: Execution
# Manually execute removals according to phased plan
# Track progress using broker_tracker.py

# Daily: Monitor for breaches and changes
python automation_cli.py monitor --check all

# Weekly: Verify removals and track progress
python automation_cli.py report --type progress --period weekly

# Monthly: Comprehensive review
python automation_cli.py report --type monitoring
python automation_cli.py dashboard --export
```

### Quick Breach Check

```bash
python automation_cli.py monitor --check hibp --email your@email.com
```

### Weekly Progress Review

```bash
python automation_cli.py report --type progress --period weekly
python automation_cli.py dashboard
```

## Automation Architecture

```
automation_cli.py (Main Interface)
├── hibp_monitor.py (Breach Detection)
├── gsc_removal_agent.py (Google Removal)
├── bing_removal_agent.py (Bing Removal)
├── monitoring_orchestrator.py (Job Coordination)
├── data_broker_automation.py (9 Brokers)
└── Supporting Tools
    ├── broker_tracker.py
    ├── exposure_scanner.py
    ├── progress_reporter.py
    └── privacy_audit.py
```

## Output Files

All automation tools save results to `logs/` directory:

```
logs/
├── hibp_breaches.json              # Breach check results
├── gsc_removal_plan.json           # Google removal plan
├── gsc_removal_tracking.json       # Google removal status
├── bing_removal_summary.json       # Bing removal status
├── broker_tracking.json            # Data broker status
├── broker_summary.json             # Broker summary
├── broker_tracking.csv             # CSV export
├── monitoring_jobs.json            # Scheduled jobs
├── monitoring_events.json          # Monitoring events
├── monitoring_alerts.json          # Active alerts
├── monitoring_report.json          # Monitoring report
└── dashboard.json                  # Dashboard data
```

## Scheduling Recommendations

**Daily** (Early Morning):
- HIBP breach checks
- Search engine monitoring
- Archive.org scanning

**Weekly** (Monday):
- Data broker rescans
- Removal verification

**Monthly** (1st, 15th, 20th):
- Credit monitoring
- Dark web scanning
- Comprehensive audits

## Error Handling

All tools include error handling for:
- Network timeouts
- API rate limiting
- Invalid inputs
- File I/O errors

Check `logs/` directory for error details and retry information.

## Troubleshooting

### HIBP API Errors
- Ensure rate limiting is respected (1.5s between requests)
- Check API status at haveibeenpwned.com
- Verify email format

### GSC/Bing Removal
- URLs must be fully indexed first
- Removal takes 3-6 months
- Verify property ownership in respective tools

### Data Broker Issues
- Some brokers may not find matches
- Manual verification often needed
- Keep confirmation numbers

## Next Steps

1. Review monitoring schedule
2. Execute data broker removals in phased approach
3. Submit search engine removal requests
4. Monitor daily for changes
5. Weekly progress reviews
6. Monthly comprehensive audits
