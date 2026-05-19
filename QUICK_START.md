# Quick Start Guide - Privacy Data Removal Framework

## Installation (5 minutes)

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/Privacy-data-removal-framework.git
cd Privacy-data-removal-framework
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set your identity
```bash
export REMOVAL_NAME="Your Full Name"
export REMOVAL_EMAIL="your.email@example.com"
export REMOVAL_PHONE="555-555-5555"
```

### 4. (Optional) Copy configuration
```bash
cp scripts/config.example.json scripts/config.json
# Edit config.json with your details
```

## First Run (10 minutes)

### Option A: Run Everything (Recommended for first time)
```bash
python3 scripts/main.py --full
```

This will:
1. ✓ Run privacy audit
2. ✓ Generate removal plan
3. ✓ Setup monitoring

### Option B: Run Step-by-Step

**Step 1: Audit your privacy exposure**
```bash
python3 scripts/main.py --audit
```

**Step 2: Generate removal plan**
```bash
python3 scripts/main.py --plan
```

**Step 3: Setup monitoring**
```bash
python3 scripts/main.py --monitor
```

## Daily Operations

### Check Removal Progress
```bash
python3 scripts/main.py --track
```

### Launch Dashboard
```bash
python3 scripts/dashboard_server.py
# Open http://localhost:8080
```

### Run Monthly Check
```bash
python3 scripts/main.py --audit
```

## Key Files

- **data_broker_automation.py** - Removal tracking engine
- **monitoring_orchestrator.py** - Continuous monitoring
- **dashboard_server.py** - Real-time progress dashboard
- **main.py** - Unified entry point (recommended)

## Output Files

All results are saved to `logs/` directory:
- `removal_plan_*.json` - Your removal strategy
- `removal_summary_*.json` - Current progress
- `privacy_audit_*.json` - Your privacy exposure
- `monitoring_config_*.json` - Monitoring setup

## Monitoring Schedule

**Weekly (10 minutes):**
```bash
python3 scripts/main.py --track
```

**Monthly (15 minutes):**
```bash
python3 scripts/main.py --audit
```

**Quarterly (30 minutes):**
```bash
python3 scripts/main.py --full
```

## Manual Removal Process

### For Each Data Broker:
1. Note the broker info from the removal plan
2. Visit the removal URL
3. Complete the removal form
4. Save the confirmation number
5. Log in the dashboard or update `logs/broker_tracking_complete.json`

### Phase Timeline:
- **Phase 1 (Easy):** TrueCaller, etc. - Complete in Week 1
- **Phase 2 (Medium):** WhitePages, PeopleFinder, etc. - Weeks 2-3
- **Phase 3 (Hard):** Spokeo, Intelius, US Search - Weeks 4-6

## Troubleshooting

**Issue: "REMOVAL_NAME not set"**
```bash
export REMOVAL_NAME="Your Name"
export REMOVAL_EMAIL="your.email@example.com"
```

**Issue: Scripts not found**
```bash
cd scripts/
# Or use full path: python3 scripts/main.py --track
```

**Issue: Permission errors**
```bash
chmod +x scripts/*.py
```

**Issue: Module not found**
```bash
pip install -r requirements.txt
```

**Run diagnostics:**
```bash
python3 scripts/main.py --diagnostic
```

## Security Tips

1. **Never commit PII** - Use environment variables
2. **Backup logs** - Archive `logs/` directory
3. **Secure emails** - Use encrypted email for confirmations
4. **Monitor alerts** - Setup email notifications
5. **Verify removals** - Check each site after removal

## Next Steps

1. ✅ Run `python3 scripts/main.py --full`
2. ✅ Check your removal plan in `logs/removal_plan_*.json`
3. ✅ Follow Phase 1 brokers to start removal
4. ✅ Update dashboard as you complete removals
5. ✅ Monitor for reappearances monthly

## Support

For issues:
1. Run `python3 scripts/main.py --diagnostic`
2. Check `logs/privacy_framework.log`
3. Review `scripts/README_SCRIPTS.md`
4. Check `PROJECT_MANIFEST.md` for full documentation

## Resources

- **Main Entry Point:** `scripts/main.py`
- **Scripts Guide:** `scripts/README_SCRIPTS.md`
- **Security Guides:** `GITHUB_SECURITY_HARDENING.md`, `EMAIL_SECURITY_SETUP.md`, `PRIVACY_HARDENING.md`
- **Removal Guide:** `COMPREHENSIVE_ACTION_PLAN.md`

---

**Ready to remove your digital footprint?**
```bash
python3 scripts/main.py --full
```

**Need detailed info?**
See [PROJECT_MANIFEST.md](PROJECT_MANIFEST.md) or [scripts/README_SCRIPTS.md](scripts/README_SCRIPTS.md)
