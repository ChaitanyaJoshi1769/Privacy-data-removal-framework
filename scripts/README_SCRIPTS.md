# Privacy Data Removal Framework - Scripts Guide

## Overview

This directory contains production-ready Python scripts for automating data broker removal tracking, monitoring, and privacy management.

## Core Scripts

### `data_broker_automation.py`
**Purpose:** Tracks data broker removal submissions and generates removal plans  
**Key Features:**
- Manages 9 major data brokers (Spokeo, WhitePages, Intelius, MyLife, TrueCaller, PeopleFinder, US Search, FamilyTreeNow, ZoomInfo)
- Tracks removal status from submission through verification
- Generates phased removal plans (Easy → Medium → Hard)
- Exports tracking data to JSON for monitoring dashboards

**Usage:**
```bash
# Set identity via environment variables
export REMOVAL_NAME="Your Name"
export REMOVAL_EMAIL="your.email@example.com"

# Run automation
python3 scripts/data_broker_automation.py
```

**Output:**
- `logs/broker_tracking_complete.json` - Complete tracking data for all brokers
- `logs/broker_summary.json` - Summary with completion percentages

### `monitoring_orchestrator.py`
**Purpose:** Orchestrates continuous monitoring for data reappearance  
**Key Features:**
- Google Alerts integration for name/email/phone monitoring
- HIBP (Have I Been Pwned) breach monitoring
- Firefox Monitor integration
- Quarterly verification checklists
- Automated notification system

**Usage:**
```bash
python3 scripts/monitoring_orchestrator.py --setup
```

### `dashboard_server.py`
**Purpose:** Real-time web dashboard for removal tracking  
**Key Features:**
- Live progress visualization
- Phase-by-phase breakdown
- Timeline tracking with expected removal dates
- Status indicators for each broker

**Usage:**
```bash
python3 scripts/dashboard_server.py
# Access at http://localhost:8080
```

### `privacy_audit.py`
**Purpose:** Performs comprehensive privacy audit  
**Checks:**
- Data exposure across brokers
- Search engine visibility
- Social media presence
- Email breaches

**Usage:**
```bash
python3 scripts/privacy_audit.py
```

### `diagnostic_tool.py`
**Purpose:** Diagnoses removal process issues  
**Troubleshooting:**
- Broker URL validation
- Network connectivity checks
- Configuration validation
- Log analysis

**Usage:**
```bash
python3 scripts/diagnostic_tool.py
```

## Supporting Scripts

### `broker_tracker.py`
Core broker tracking functionality with status management and confirmation logging

### `hibp_monitor.py`
Monitors Have I Been Pwned for breach notifications

### `config_validator.py`
Validates configuration files and environment setup

### `performance_benchmark.py`
Benchmarks removal speeds across different brokers

### `progress_reporter.py`
Generates progress reports for removal campaigns

## Configuration

### Environment Variables
```bash
export REMOVAL_NAME="Your Full Name"
export REMOVAL_EMAIL="your.email@example.com"
export REMOVAL_PHONE="555-555-5555"
export MONITORING_EMAIL="alerts@example.com"
```

### Configuration File (Optional)
Copy `config.example.json` to `config.json` and customize:
```bash
cp scripts/config.example.json scripts/config.json
# Edit config.json with your settings
```

## Workflow

### Phase 1: Initial Removal (Week 1-2)
```bash
# Generate removal plan
python3 scripts/data_broker_automation.py

# Start easy brokers (TrueCaller, etc.)
# Monitor progress with dashboard
python3 scripts/dashboard_server.py
```

### Phase 2: Medium Removal (Week 2-4)
```bash
# Continue with medium difficulty brokers
# Track submissions and confirmations
python3 scripts/monitoring_orchestrator.py --track
```

### Phase 3: Difficult Removal (Week 4-8)
```bash
# Complete hard difficulty brokers
# Verify removal completion
python3 scripts/data_broker_automation.py --verify
```

### Phase 4: Continuous Monitoring (Ongoing)
```bash
# Run monthly monitoring
python3 scripts/monitoring_orchestrator.py --check

# Quarterly full audit
python3 scripts/privacy_audit.py
```

## Output Files

All scripts export data to `logs/` directory:

- `broker_tracking_complete.json` - Full tracking data
- `broker_summary.json` - Completion summary
- `monitoring_config.json` - Monitoring configuration
- `privacy_audit_report.json` - Privacy audit results
- `benchmark_results.json` - Performance metrics

## Error Handling

All scripts include comprehensive error logging. Check logs for troubleshooting:

```bash
# View recent logs
tail -f logs/*.log

# Run diagnostic tool if issues occur
python3 scripts/diagnostic_tool.py
```

## Requirements

- Python 3.8+
- Dependencies in `requirements.txt`:
  - requests
  - httpx
  - beautifulsoup4
  - lxml
  - python-dotenv

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Copy example config
cp scripts/config.example.json scripts/config.json

# Set environment variables
export REMOVAL_NAME="Your Name"
export REMOVAL_EMAIL="your.email@example.com"
```

## Security Considerations

1. **Never commit PII** - Use environment variables, not hardcoded credentials
2. **Secure logs** - Keep `logs/` directory with restricted permissions
3. **Backup tracking** - Archive `broker_tracking_complete.json` regularly
4. **Monitor alerts** - Set up email notifications for completion alerts
5. **Review manually** - Verify each removal completion before marking done

## Monitoring Checklist

**Weekly (10 minutes):**
- ✓ Check dashboard progress
- ✓ Verify no new submissions needed
- ✓ Review pending confirmations

**Monthly (15 minutes):**
- ✓ Run privacy audit
- ✓ Check HIBP for breaches
- ✓ Review monitoring alerts
- ✓ Update tracking logs

**Quarterly (30 minutes):**
- ✓ Full privacy audit
- ✓ Verify all removals remain
- ✓ Check for reappearances
- ✓ Update removal plan

## Support

For issues or questions:
1. Run `diagnostic_tool.py` for system check
2. Review logs in `logs/` directory
3. Consult individual script docstrings
4. Check [PROJECT_MANIFEST.md](../PROJECT_MANIFEST.md) for project overview

## License

This framework is part of the Privacy Data Removal Framework project.
