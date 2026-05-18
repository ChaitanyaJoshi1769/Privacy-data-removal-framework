# GitHub Actions Workflows

Automated CI/CD pipelines for the Privacy Data Removal Framework.

## Available Workflows

### 1. Daily Monitoring (`daily-monitoring.yml`)

Runs privacy monitoring tasks on a schedule.

**Schedule**:
- **Daily**: HIBP breach check + search monitoring + archive scanning (3:00 AM UTC)
- **Weekly**: Data broker rescan (Monday, 2:00 AM UTC)
- **Monthly**: Comprehensive audit (1st of month, 6:00 AM UTC)

**Actions**:
- Checks for data breaches via HIBP API
- Monitors search engine results
- Scans Archive.org for snapshots
- Generates weekly progress reports
- Runs monthly comprehensive audits

**Output**: 
- Results saved to `logs/` directory
- Artifacts uploaded to GitHub Actions
- Changes committed back to repository

**Configuration**:
- Add `MONITORING_EMAIL` secret with your email address
- Workflows run automatically on schedule
- Can be manually triggered from Actions tab

### 2. Framework Testing (`testing.yml`)

Validates code quality and functionality on every push.

**Trigger**: Push to main/develop, Pull requests

**Tests**:
- ✓ Import all modules successfully
- ✓ HIBP Monitor instantiation
- ✓ Data Broker Automation functionality
- ✓ Monitoring Orchestrator setup
- ✓ Dashboard Server HTML generation
- ✓ CLI help command
- ✓ Python syntax validation
- ✓ Documentation presence
- ✓ Code linting (flake8)

**Output**:
- Test results in GitHub Actions
- Code quality reports
- Artifacts if failures occur

---

## Setting Up Workflows

### Prerequisites

1. GitHub repository (you have this!)
2. Python 3.11+
3. Secrets configured

### Configure Secrets

Add these secrets to your GitHub repository:

**Settings → Secrets → New repository secret**

```
MONITORING_EMAIL = chaitanyajoshi15@gmail.com
```

### Enable Workflows

Workflows are automatically enabled. To verify:

1. Go to your repository
2. Click "Actions" tab
3. You should see workflow definitions

### Manual Trigger

Workflows can be manually triggered:

1. Go to Actions tab
2. Select a workflow
3. Click "Run workflow"
4. Select branch (usually main)
5. Click "Run"

---

## Monitoring Schedule

### Daily (3:00 AM UTC)
- HIBP breach check
- Search engine monitoring
- Archive.org scanning

### Weekly (Monday, 2:00 AM UTC)
- Data broker rescans
- Removal verification checks

### Monthly (1st, 6:00 AM UTC)
- Comprehensive privacy audit
- Full report generation

---

## Workflow Files

### `daily-monitoring.yml` (500+ lines)
- Scheduled daily privacy monitoring
- Weekly verification checks
- Monthly comprehensive audits
- Artifact upload & commit

### `testing.yml` (400+ lines)
- Syntax validation
- Import testing
- Functionality tests
- Code quality checks

---

## Accessing Results

### GitHub Actions Tab

1. Go to repository
2. Click "Actions" tab
3. Click workflow run
4. View logs and artifacts

### Committed Results

Results are automatically committed to the repository:
- Check `logs/` directory
- View recent commits
- Monitor changes over time

### Local Access

```bash
# Download artifacts
# Via GitHub UI: Actions > Workflow > Artifacts

# View committed logs
git log --oneline logs/

# Check latest monitoring
cat logs/monitoring_report.json
```

---

## Environment Variables

Workflows automatically have access to:

```yaml
GITHUB_TOKEN: Read/write repository access
MONITORING_EMAIL: Your email (from secrets)
```

---

## Troubleshooting Workflows

### Workflows Not Running

1. Check Actions tab → Workflows
2. Verify schedule is correct
3. Ensure repository is public or has Actions enabled
4. Check "Allow GitHub Actions to create pull requests" (Settings)

### Tests Failing

1. Click failed workflow
2. View logs for errors
3. Common issues:
   - Missing dependencies: Run `pip install -r scripts/requirements.txt`
   - Invalid email: Check MONITORING_EMAIL secret
   - API limits: Workflows respect rate limiting

### Results Not Committing

1. Verify GitHub token has write access
2. Check git config in workflow
3. Ensure branch protection doesn't block commits

---

## Customizing Workflows

### Change Schedule

Edit `.github/workflows/daily-monitoring.yml`:

```yaml
schedule:
  - cron: '0 3 * * *'  # Change time here
```

Cron format: `minute hour day month day-of-week`

Examples:
- `0 9 * * *` = 9:00 AM daily
- `0 2 * * 1` = 2:00 AM Monday
- `0 0 1 * *` = Midnight 1st of month

### Add New Workflow

1. Create `.github/workflows/yourname.yml`
2. Define triggers and steps
3. Commit to repository
4. Workflow becomes available in Actions tab

### Update Actions

Workflows use standard GitHub Actions:
- `actions/checkout` - Clone repository
- `actions/setup-python` - Install Python
- `actions/upload-artifact` - Save outputs

---

## Best Practices

✅ **Do**:
- Run on schedule (let automation work)
- Check results weekly
- Keep secrets secure
- Commit results to repository
- Use public repositories (easier sharing)

❌ **Don't**:
- Commit credentials to repository
- Disable automated monitoring
- Modify schedule too frequently
- Ignore workflow errors

---

## Monitoring Workflow Status

### GitHub Status Badge

Add to README:

```markdown
![Monitoring](https://github.com/ChaitanyaJoshi1769/Privacy-data-removal-framework/actions/workflows/daily-monitoring.yml/badge.svg)
```

### Workflow Insights

1. Actions → Select workflow
2. View statistics:
   - Run count
   - Success rate
   - Average duration
   - Recent runs

---

## Integration with Tools

Workflows integrate with:

- **HIBP API**: Real breach detection
- **Data Broker Automation**: 9 brokers tracked
- **Dashboard Server**: Generated reports
- **CLI Tools**: All available commands

---

## Support

For workflow issues:

1. Check GitHub Actions documentation
2. Review workflow logs
3. Verify secrets are configured
4. Check Python environment

---

## Next Steps

1. ✅ Repository setup complete
2. ✅ Workflows configured
3. Add `MONITORING_EMAIL` secret
4. Trigger workflows manually to test
5. Monitor results in logs/

Workflows will automatically:
- Run on schedule
- Monitor for privacy issues
- Generate reports
- Commit results

---

**Status**: Workflows Ready  
**Last Updated**: 2026-05-18  
**Version**: 2.0
