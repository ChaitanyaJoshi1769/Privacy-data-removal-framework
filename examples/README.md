# Example Outputs

This directory contains realistic example outputs from the Privacy Framework. Use these to understand what data structures and metrics you'll see when running the framework.

## Files

### 1. example_identity_profile.json

**Purpose**: Template for identity profile configuration

```bash
cat examples/example_identity_profile.json
```

**Contains**:
- Name, email, phone number
- GitHub username and domain
- Account information structure
- Timestamps

**When Generated**: Created during framework initialization

**Used By**: All framework tools for identification

---

### 2. example_config.json

**Purpose**: Framework configuration template

```bash
cat examples/example_config.json
```

**Contains**:
- Monitoring settings
- Removal preferences
- API keys (if applicable)
- Notification settings

**When Generated**: During setup

**Used By**: Global framework configuration

---

### 3. example_hibp_results.json (NEW)

**Purpose**: Have I Been Pwned breach check results

```bash
python3 scripts/hibp_monitor.py example@email.com
```

**Size**: ~3.2 KB

**Contains**:
- **Breaches Found**: 2 breaches (LinkedIn 2021, MyFitnessPal 2018)
- **Risk Assessment**: Score 75/100, HIGH severity
- **Password Status**: Compromised (present in databases)
- **Data Classes**: Email, passwords, usernames, phone numbers
- **Remediation Plan**: Immediate, 24-hour, 1-week actions
- **Accounts Affected**: Specific services with remediation URLs

**Key Fields**:
```json
{
  "email": "example@email.com",
  "breaches_found": 2,
  "password_compromised": true,
  "risk_assessment": {
    "score": 75,
    "level": "HIGH"
  },
  "breaches": [...],
  "remediation_plan": {...}
}
```

**What It Tells You**:
- ✓ Which services compromised your email
- ✓ When the breach occurred
- ✓ What data was exposed
- ✓ Whether password was compromised
- ✓ Steps to take immediately

**What To Do**:
1. Change passwords for affected accounts IMMEDIATELY
2. Enable two-factor authentication
3. Monitor accounts for suspicious activity

**Generated When**:
- Running HIBP monitor manually
- Daily automated monitoring (3 AM UTC)
- Weekly updates
- On-demand checks

---

### 4. example_broker_tracking.json (NEW)

**Purpose**: Data broker removal status tracking

```bash
python3 scripts/automation_cli.py removal --list
```

**Size**: ~8.5 KB

**Contains**:
- **Broker Status**: All 9 brokers with removal status
- **Phased Tracking**: Easy/Medium/Hard phases
- **Confirmation Numbers**: For each submission
- **Timeline**: Week-by-week progress
- **Statistics**: Success rates and timelines
- **Verification**: What's been confirmed removed
- **Next Actions**: What to do next

**Key Sections**:
- Phase 1 (Easy): 1 broker
  - TrueCaller: ✓ VERIFIED REMOVED
  
- Phase 2 (Medium): 5 brokers
  - WhitePages: ⏳ In progress (8 days left)
  - MyLife: ⏳ In progress (18 days left)
  - PeopleFinder: ✓ VERIFIED REMOVED
  - FamilyTreeNow: ⏳ In progress (18 days left)
  - ZoomInfo: Not yet submitted
  
- Phase 3 (Hard): 3 brokers
  - Spokeo: Not yet submitted
  - Intelius: Not yet submitted
  - USSearch: Not yet submitted

**Statistics**:
```json
{
  "total_submissions": 5,
  "removals_verified": 2,
  "removals_in_progress": 3,
  "success_rate": "40% verified",
  "estimated_completion_date": "2026-06-22",
  "reappearance_rate": "0%"
}
```

**What It Tells You**:
- ✓ Which brokers have your data
- ✓ Current removal status
- ✓ When removals will complete
- ✓ Which have been verified removed
- ✓ Any reappearances detected

**What To Do**:
- Monitor progress weekly
- Submit Phase 3 removals
- Verify completed removals
- Resubmit if reappears

**Updated When**:
- Manual submission
- Weekly broker rescan (Monday 2 AM UTC)
- Removal verification (Friday 2 PM UTC)

---

### 5. example_monitoring_report.json (NEW)

**Purpose**: Bi-weekly or monthly monitoring summary

```bash
python3 scripts/automation_cli.py report --type monitoring
```

**Size**: ~12 KB

**Contains**:
- **Job Status**: All 9 automated monitoring jobs
  - Daily: HIBP check, search monitoring, archive scan
  - Weekly: Broker rescan, social audit, removal verification
  - Monthly: Credit check, dark web scan, comprehensive audit

- **Results**: What each job found
  - 0 new breaches
  - 0 new search results
  - 2 removals verified
  - 0 reappearances detected

- **Alerts**: Notifications sent
  - MEDIUM: PeopleFinder removal verified
  - LOW: WhitePages processing update
  - LOW: Monthly credit check complete

- **Metrics**: Privacy progress
  - Exposure score: 52/100 (was 85)
  - Improvement: 33 points (38.8%)
  - Search results: 0 (was 4)
  - Brokers removed: 2 (was 0)

**What It Tells You**:
- ✓ Overall privacy improvement
- ✓ Status of each monitoring job
- ✓ What's been completed
- ✓ What's in progress
- ✓ Alerts and issues
- ✓ Trend over time

**What To Do**:
- Review weekly for progress
- Act on any alerts
- Plan next phase
- Update removal submissions

**Generated When**:
- End of week (Friday)
- End of month (30th)
- On-demand report request

---

### 6. example_privacy_audit_report.json (NEW)

**Purpose**: Comprehensive monthly privacy audit

```bash
python3 scripts/automation_cli.py audit --type all --full
```

**Size**: ~13 KB

**Contains**:
- **7 Audit Sections**:
  1. GitHub: Public profile, 5 public repos, no sensitive data
  2. Search Engines: 0 results in Google/Bing (removed)
  3. Data Brokers: 5 brokers have data, 2 removed, 3 in progress
  4. Social Media: 1 LinkedIn profile (public, acceptable)
  5. Breaches: 2 breaches on record, password compromised
  6. Password Security: Change ALL breached account passwords
  7. Privacy Settings: Email/phone hidden, address removed

- **Risk Assessment**:
  - Critical: Password exposed in breaches
  - High: 5 data brokers still active
  - Medium: Archive snapshots exist
  - Low: LinkedIn profile public (normal)

- **Action Items**:
  - Immediate: Change passwords
  - This week: Verify removals
  - This month: Submit Phase 3 brokers
  - Ongoing: Automated monitoring

- **Historical Comparison**:
  - Started: 85/100 (Very High Risk)
  - Previous: 63/100 (Medium)
  - Current: 52/100 (Medium, Improving)
  - Improvement: 33 points (38.8%)
  - Projection: Reach low risk by end of July

**What It Tells You**:
- ✓ Overall privacy score and trend
- ✓ Detailed findings in each area
- ✓ Risk levels and priorities
- ✓ Specific action items
- ✓ Progress since starting
- ✓ Expected completion date

**What To Do**:
- Review all 7 audit sections
- Act on critical issues first
- Follow action item timeline
- Plan for next month

**Generated When**:
- Monthly (20th of month, 9 AM UTC)
- On-demand audit request
- After major changes

---

## How To Use These Examples

### 1. Understand Data Structures

Review these files to understand what data your framework will generate:

```bash
# Look at structure of breach results
jq . examples/example_hibp_results.json | head -50

# Examine broker tracking format
jq '.brokers | keys' examples/example_broker_tracking.json

# Check monitoring job outputs
jq '.daily_monitoring_jobs' examples/example_monitoring_report.json
```

### 2. Set Expectations

These examples show realistic progress:
- Week 1: Submit Phase 1 and some Phase 2
- Week 2: Verify Phase 1 complete
- Week 3-4: Phase 2 in progress, plan Phase 3
- Month 2: Phase 2 complete, Phase 3 processing
- Month 3+: All removals complete, continuous monitoring

### 3. Compare Your Results

When you run the framework, compare your outputs to these examples:

```bash
# Your results vs example
python3 scripts/automation_cli.py removal --list > my_brokers.json
diff examples/example_broker_tracking.json my_brokers.json

# Check if monitoring looks similar
python3 scripts/automation_cli.py report --type monitoring > my_report.json
jq .statistics my_report.json
```

### 4. Extract Templates

Use these as templates for custom reports:

```bash
# Create your own monitoring summary
cp examples/example_monitoring_report.json my_monitoring_summary.json
# Edit with your actual data
```

### 5. Integration Examples

Use these for API/programmatic access:

```python
import json

# Load example to understand structure
with open('examples/example_hibp_results.json') as f:
    example = json.load(f)

# Use as template for your implementation
print(example['breaches_found'])
print(example['risk_assessment']['level'])
```

---

## Example Timeline

These examples represent this timeline:

```
2026-05-18: Framework started
  ↓ Week 1: Submit Phase 1 & early Phase 2
2026-05-25: Phase 1 complete (TrueCaller)
  ↓ Week 2: More Phase 2 submissions
2026-06-01: Weekly monitoring starts
  ↓ Week 3: Phase 2 processing, verify removals
2026-06-15: Bi-weekly report, Phase 3 planning
  ↓ Week 4-5: Phase 2 completing, Phase 3 submissions
2026-06-22: Most removals complete
  ↓ Month 2: Ongoing monitoring, reappearance checks
2026-07-15: Month 2 audit report
```

---

## Key Metrics in Examples

### Exposure Score
- Started: 85/100 (Very High Risk)
- Current: 52/100 (Medium Risk)
- Goal: <30/100 (Low Risk)
- Timeline: 1-2 months to goal

### Broker Status
- Total: 9 brokers
- Phase 1 (Easy): 1 broker, 100% complete
- Phase 2 (Medium): 5 brokers, 40% complete
- Phase 3 (Hard): 3 brokers, 0% started
- Overall: 22% removal rate

### Search Presence
- Started: Multiple pages
- Current: 0 search results
- Status: Successfully deindexed
- Duration: Removal + 6-month temporary

### Breach Status
- Total breaches: 2
- Password compromised: Yes
- New breaches (this month): 0
- Status: Requires immediate password change

---

## Questions?

Refer to these files when you have questions about:

- **Data Structure**: "What does a removal look like?" → See example_broker_tracking.json
- **Progress**: "How long until done?" → See example_monitoring_report.json
- **Risk**: "What's my exposure score?" → See example_privacy_audit_report.json
- **Breaches**: "What if I'm in a breach?" → See example_hibp_results.json

---

**Last Updated**: 2026-05-18  
**Format Version**: 2.0  
**Examples Are**: Realistic, achievable, based on actual framework output
