# FOOTPRINT REMEDIATION OPERATIONAL PLAYBOOK

## Quick Start

```bash
# 1. Initialize project
make init

# 2. Complete identity intake (30-60 min)
make intake

# 3. Run discovery (automated OSINT)
make discover

# 4. Review findings
make expose

# 5. Execute removals
make remove  # Will show dry-run first
```

---

## PHASE 0: OPERATIONAL SETUP ✓

### What's Been Created

```
✓ Project structure (16 directories)
✓ Python environment (pyproject.toml, requirements.txt)
✓ Database schema (SQLAlchemy models)
✓ Configuration templates (.env.example)
✓ CLI framework (Makefile, cli.py placeholder)
✓ Audit & logging infrastructure
✓ Identity intake questionnaire
```

### Next Steps

1. **Install dependencies**
   ```bash
   python -m pip install -r requirements.txt
   ```

2. **Initialize database**
   ```bash
   python models.py  # Creates SQLite database
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

---

## PHASE 1: IDENTITY INGESTION & CORRELATION

### Objective
Build a master identity graph showing all aliases, accounts, emails, phones, and correlation vectors.

### Execution

1. **Complete Questionnaire**
   - Run interactive intake: `python identity_intake_questionnaire.py`
   - Or: `make intake`
   - Takes 30-60 minutes
   - Covers 8 sections (personal, contact, location, education, accounts, artifacts, security, priorities)

2. **Data Entry** - Answer comprehensively:
   - All legal names, nicknames, aliases
   - All emails (current, historical, variations)
   - All phone numbers
   - All locations you've lived
   - Education & employment history
   - Every online account (LinkedIn, Twitter, GitHub, Reddit, Discord, etc.)
   - Domains you own/owned
   - Websites, blogs, repositories
   - Known breaches affecting you

3. **Correlation Analysis** - System will:
   - Detect reused usernames across platforms
   - Find profile photo matches
   - Identify email correlations
   - Find phone number linkages
   - Build relationship graph
   - Score correlation confidence (0.0-1.0)
   - Generate correlation report

### Output
- `intel/identity_profile.json` - Complete identity profile
- `correlation/identity_graph.json` - Relationship graph
- `correlation/correlation_report.html` - Visual analysis
- Database entries in: identities, aliases, contacts, accounts tables

### Key Insights Generated
```
Identity Graph:
- 1 primary identity
- 15-50+ aliases/correlations
- Correlation confidence scores
- Platform overlap analysis
- Risk vectors identified
```

---

## PHASE 2: MAXIMUM DISCOVERY & ENUMERATION

### Objective
Exhaustively search for all discoverable traces using lawful OSINT methods only.

### Coverage

**Search Engines**
- Google (site: and specific queries)
- Bing
- DuckDuckGo
- Yandex

**Archive & Cached Content**
- Internet Archive (archive.org)
- Google Cache
- Bing Cache
- Archive.is

**AI Indexing**
- Common Crawl
- AI dataset mirrors
- Training data exposures

**Data Brokers**
- Whitepages, Spokeo, PeopleFinder, Intelius, MyLife
- FastPeopleSearch, ZoomInfo, Pipl
- TrueCaller (phone lookups)

**Social Media**
- LinkedIn (profiles, posts, resume data)
- Twitter (tweets, location data, photos)
- Facebook (pages, photo tags)
- Instagram (tagged photos, story mentions)
- Reddit (posts, comments, deleted content archives)
- GitHub (public repos, commits, profile info)
- Stack Overflow (answers, user profiles)

**Public Records & Registries**
- WHOIS records (current & historical)
- Business registrations (LLC, sole prop)
- Professional licenses
- Court records (if accessible)
- Property records
- Voter registration records

**Metadata & Technical**
- EXIF data in photos
- Metadata in PDFs
- DNS records
- Historical domain registrations
- Git commit history
- Package registry profiles

**Content Archives**
- Paste sites (Pastebin, Paste.ee, Hastebin)
- Code repositories (public GitHub, GitLab)
- Document repositories (Scribd, SlideShare)
- Image sharing (Imgur, Flickr)
- Dead links (Wayback Machine)

### Execution

```bash
# Full discovery (2-4 hours)
make discover

# Or run components individually:
python scripts/discover_search_engines.py --engines google,bing
python scripts/discover_data_brokers.py --targets whitepages,spokeo
python scripts/discover_social_media.py --platforms linkedin,twitter,github
python scripts/discover_archives.py --include-wayback --include-cache
python scripts/discover_metadata.py --extract-exif --extract-pdf
```

### What Gets Discovered
- URLs containing your name, email, phone
- Profile photos and image matches
- Old website snapshots
- Resume/CV copies
- Leaked data references
- Breach mentions
- Forum posts
- Code commits
- Public records

### Output
- `discovery/search_engine_results.json`
- `discovery/data_broker_profiles.json`
- `discovery/social_media_inventory.json`
- `discovery/archive_snapshots.json`
- `discovery/metadata_findings.json`
- Database entries in: exposures table

### Risk Signals Identified
```
[CRITICAL] Address exposed on Whitepages
[HIGH] Phone number on Spokeo
[HIGH] Facebook photos with location tags
[MEDIUM] Old LinkedIn resume with phone
[MEDIUM] GitHub profile links to Twitter
[LOW] Name mentioned in 5-year-old blog post
```

---

## PHASE 3: EXPOSURE PRIORITIZATION

### Objective
Classify and risk-rank all discovered exposures.

### Classification Framework

**CRITICAL** - Immediate safety/financial risk:
- Home address publicly exposed
- Phone number in data broker
- Government ID exposed
- Financial accounts compromised
- Ongoing harassment/safety threat

**HIGH** - Significant identity/privacy risk:
- Email in breach database
- Account credentials compromised
- Employer/school linkage
- Profile photos with metadata
- Search result prominence (position 1-5)

**MEDIUM** - Moderate exposure:
- Social media visibility
- Old archived content
- Less critical location data
- Generic mentions (no address/phone)

**LOW** - Minimal impact:
- Very old content (5+ years)
- Generic name matches
- Minimal personal data
- No search visibility

### Execution

```bash
make expose        # Generates exposure analysis
make prioritize    # Risk-ranks all exposures
```

### Analysis Generated
```
PRIORITY MATRIX:

[CRITICAL - REMOVE IMMEDIATELY]
□ jsmith@example.com on Spokeo.com
□ 123 Main St, City, State on Whitepages
□ Phone: +1-555-0123 on Intelius
□ Driver's License # on PasteBin

[HIGH - REMOVE URGENTLY]
□ LinkedIn profile with sensitive info (Google position 2)
□ GitHub profile links to Twitter
□ Facebook photos with geolocation
□ Resume.pdf in public Google Drive

[MEDIUM - MONITOR & REMOVE]
□ Old blog posts with work experience
□ Reddit comments with location hints
□ Stack Overflow profile with email
□ YouTube channel with real name

[LOW - MONITOR]
□ 10-year-old forum posts
□ Cached pages (no search rank)
□ Archive.org snapshots
```

### Key Metrics
- Total exposures discovered: X
- Critical severity: X (Y%)
- High severity: X (Y%)
- Search-visible: X
- Data broker presence: X
- Breach mentions: X

### Output
- `exposures/exposure_inventory.json`
- `exposures/risk_matrix.html`
- `exposures/severity_breakdown.json`
- `reports/exposure_summary.html`

---

## PHASE 4: AGGRESSIVE REMOVAL OPERATIONS

### Objective
Execute coordinated removals across all vectors.

### Removal Types

**Type 1: Account Deletion**
- Delete/disable account on platform
- Example: Deactivate Facebook, delete old LinkedIn
- Impact: Removes all content and profile
- Success rate: High (you control the account)

**Type 2: Data Broker Opt-Out**
- Submit opt-out requests to data brokers
- Platforms: Spokeo, Whitepages, Intelius, MyLife, etc.
- Impact: Removes listing (though they re-ingest)
- Success rate: High (automated workflows)
- Persistence: 30-90 days before they re-list you

**Type 3: CCPA/GDPR Privacy Request**
- Submit legal privacy request for data removal
- Applies: Whitepages, Spokeo, ZoomInfo, etc.
- Impact: Legal obligation to remove
- Success rate: High (legally binding)
- Persistence: Blocks re-listing for 45 days (may need annual re-request)

**Type 4: Search Engine Removal**
- Submit removal requests to Google, Bing
- Example: Remove cached page, URL de-index
- Impact: Page disappears from search results
- Success rate: Variable (may take weeks)

**Type 5: Platform Takedown**
- Report non-consensual content
- File DMCA for copyright/misuse
- Platforms: Reddit, Facebook, paste sites
- Impact: Content removal
- Success rate: Variable

**Type 6: Content Replacement**
- Replace old content with bland placeholder
- Example: Replace resume with "no longer available"
- Impact: De-ranks in search, less useful
- Success rate: High

### Execution Strategy

**Phase 4A: Approval & Dry-Run**

```bash
# See what will be removed (no changes)
make remove  # Runs with --dry-run by default

# Output:
# [DRY RUN] Would delete LinkedIn account (affects 45 connections)
# [DRY RUN] Would submit opt-out to Spokeo (70% success rate)
# [DRY RUN] Would submit CCPA request to Whitepages
# [DRY RUN] Would request Google removal for 5 URLs
#
# Total impact: Remove X exposures, suppress Y more
# Estimated persistence: Z-A months before re-listing
```

**Phase 4B: Approval**

```bash
# Review dry-run output
# Get explicit approval for destructive actions
# Document rationale (safety, privacy, etc.)

python scripts/removal_approval.py --review-all
# or
python footprint_ops/cli.py removal --confirm-all
```

**Phase 4C: Execute**

```bash
# Execute approved removals
make remove  # Removes --dry-run flag

# Tracks:
# - Submitted requests
# - Confirmation emails received
# - Platform responses
# - Status of each removal
```

### Specific Workflows

**Remove from Data Brokers**

```bash
python scripts/data_broker_optout.py \
    --targets spokeo,whitepages,intelius,mylife \
    --email your_email \
    --mode batch
```

Automates:
- Finding your listing on each site
- Navigating opt-out form
- Submitting removal request
- Tracking confirmation

**Submit CCPA/GDPR Requests**

```bash
python scripts/privacy_requests.py \
    --regulation ccpa,gdpr \
    --targets whitepages,spokeo,zoominfo \
    --method batch
```

Generates:
- Signed privacy request emails
- Required documentation
- Submission tracking

**Google/Bing Removal**

```bash
python scripts/search_engine_removal.py \
    --search-console-key <key> \
    --urls removal_urls.txt \
    --request-type cache_removal,url_removal
```

Submits:
- Cache removal requests
- URL removal requests
- Outdated content requests

**Account Deletions**

```bash
python scripts/account_deletion_workflows.py \
    --platforms linkedin,facebook,twitter \
    --accounts accounts.json \
    --confirm
```

Executes:
- Account deactivation
- Final data download (if available)
- Deletion confirmation

### Removal Tracking Database

All operations logged with:
- Operation type
- Target platform
- Submission date
- Status (pending, submitted, verified removed, failed, reappeared)
- Verification date
- Retry count
- Estimated completion

### Output
- `removal/operations_log.json`
- `removal/removal_tracker.html` (live dashboard)
- `reports/removal_status.json`

---

## PHASE 5: SEARCH ENGINE SUPPRESSION

### Objective
Suppress remaining discoverable content from search rankings.

### Strategies

**Strategy 1: URL De-Indexing**
- Remove specific URLs from Google/Bing index
- Via: Search Console
- Impact: URL no longer appears in search results
- Persistence: Permanent (unless page is re-indexed)

**Strategy 2: Cached Page Removal**
- Remove cached version of pages
- Via: Search Console cache removal request
- Impact: Cached version unavailable
- Persistence: Weeks to months

**Strategy 3: Outdated Content Removal**
- Flag pages with outdated personal info
- Via: Search Console "remove outdated content"
- Impact: May suppress ranking
- Persistence: Days to weeks

**Strategy 4: Snippet Suppression**
- Prevent preview text in search results
- Via: meta robots tag, robots.txt
- Impact: No preview snippet shown (still in index)
- Persistence: Permanent (if you control site)

**Strategy 5: Negative SEO / Content Flooding**
- Create positive content to dilute search visibility
- Create profiles on professional sites (clean GitHub, LinkedIn)
- Rank positive content above problematic content
- Impact: Negative results pushed down in ranking
- Persistence: Ongoing (requires maintaining positive content)

### Execution

```bash
make deindex

# Or specifically:
python scripts/google_removal_requests.py \
    --method bulk \
    --urls removal_urls.txt

python scripts/search_dilution.py \
    --create-profiles professional \
    --platforms github,linkedin,medium
```

### Example: Remove Search Result

```
Before:
  Position 1: "John Smith - Address: 123 Main St, City"
  
After:
  (URL no longer in index)
  Position 1: "John Smith - GitHub Profile"
  Position 2: "John Smith - Stack Overflow"
```

### Output
- `deindex/removal_requests.json`
- `deindex/search_suppression_status.html`
- `reports/search_visibility_before_after.json`

---

## PHASE 6: ATTRIBUTION FRAGMENTATION

### Objective
Future-proof: Break identity linkage chains and reduce correlation vectors.

### Strategies

**Email Segmentation**
- Create separate "work" email (professional)
- Keep separate "personal" email (minimal exposure)
- Use separate "privacy" email for random signups
- Never cross-pollinate email address usage

**Device Separation**
- Maintain separate device for financial/sensitive
- Different device for public/social use
- Different browser profiles for each use case

**Browser Isolation**
- Firefox profile 1: Work/professional
- Firefox profile 2: Personal/private
- Chrome profile: Temporary/public
- Containers (Multi-Account Containers extension) for account separation

**Metadata Hygiene**
- Strip EXIF from photos before uploading
- Remove metadata from PDFs
- Use VPN/proxy to avoid IP tracking
- Use DuckDuckGo, Brave, or privacy-focused browser

**Account Practices**
- Don't reuse usernames across platforms
- Use unique, randomized usernames when possible
- Avoid profile photos that match across accounts
- Use different phone numbers for accounts (Google Voice, etc.)

**DNS & Network Privacy**
- Use DNS-over-HTTPS (DOH) or DNS-over-TLS (DOT)
- Pi-hole locally or NextDNS for ad blocking
- VPN for public WiFi
- Tor for maximum anonymity when needed

**Password Management**
- Use unique passwords for every account
- Password manager (1Password, Bitwarden, KeePass)
- Enable 2FA/MFA everywhere
- Use passkeys where supported

### Implementation

```bash
python scripts/privacy_hardening.py --recommend

# Generates:
# - Browser setup guide
# - Email segmentation template
# - VPN/DNS recommendations
# - Device isolation checklist
# - Password manager setup
```

### Output
- `templates/privacy_playbook.md` - Customized for your situation
- `templates/browser_config.json`
- `templates/device_isolation_guide.md`

---

## PHASE 7: CONTINUOUS MONITORING

### Objective
Long-term surveillance for re-exposures and new data leaks.

### Monitoring Types

**Type 1: Search Engine Re-appearance**
- Daily/weekly Google/Bing searches for your name
- Check search rankings
- Alert if new results appear
- Check for cached versions

**Type 2: Data Broker Re-listing**
- Weekly scans of major data brokers
- Check if you've been re-listed
- Automated opt-out submission
- Re-submit CCPA requests if needed

**Type 3: Breach Monitoring**
- Monitor Have I Been Pwned for your email
- Set up alerts on Breach Database
- Check Dark Web monitoring services
- Monitor credit reports

**Type 4: Social Media Monitoring**
- Alerts for mentions of your name
- Alerts for photos containing you
- Monitor for impersonation accounts
- Check old platforms for re-activation

**Type 5: Metadata/Image Leaks**
- Reverse image search for profile photos
- EXIF data extraction monitoring
- PDF metadata monitoring
- Metadata in any publicly shared files

### Execution

```bash
make monitor

# Runs daily scans:
python scripts/search_monitoring.py --frequency daily
python scripts/data_broker_monitoring.py --frequency weekly
python scripts/breach_monitoring.py --frequency daily
python scripts/social_media_monitoring.py --frequency daily
```

### Alerting

Alerts trigger on:
- New search results (unknown exposures)
- Re-listing by data broker
- New breach involving your email/phone
- New mentions on social media
- New image matches

### Dashboard

```
MONITORING DASHBOARD
====================
Last scans: 2 hours ago
Data brokers scanned: 8
New exposures detected: 0
Re-exposures: 0
Breach alerts: 0

Timeline:
- 2024-05-17 12:00: Google scan completed (0 new)
- 2024-05-17 10:30: Spokeo scan completed (reappeared: 1)
- 2024-05-16 12:00: Breach monitoring (no new)
```

### Output
- `monitoring/daily_report.json`
- `monitoring/weekly_summary.html`
- `monitoring/reappearance_log.json`
- Alert emails (if configured)

---

## PHASE 8: EXECUTION CYCLE

### Iterative Process

1. **Discover** - Find all exposures
2. **Correlate** - Identify linkages
3. **Prioritize** - Rank by severity
4. **Recommend** - Suggest removal strategy
5. **Approve** - Get explicit approval
6. **Execute** - Perform removals
7. **Verify** - Confirm removal succeeded
8. **Monitor** - Watch for re-exposure
9. **Report** - Generate findings
10. **Iterate** - Repeat for new exposures

### Full Cycle Command

```bash
python footprint_ops/cli.py full-cycle \
    --identity-file intel/identity.json \
    --auto-discover \
    --skip-high-risk \
    --dry-run-first
```

---

## IMPORTANT NOTES

### Persistence & Re-Indexing

**Critical Reality**: Data brokers continuously re-ingest data from public sources. Your removal is not permanent.

- **First removal**: 40-80% success rate
- **Without ongoing monitoring**: 60-70% re-list within 3-6 months
- **Without address protection**: Home address will re-appear
- **Solution**: Ongoing monitoring + annual re-submission

### Address Protection

Most critical vector. Strategies:
- Virtual mailbox services (UMail, VirtualMailbox)
- Family trust property (if possible)
- P.O. Box (limits effectiveness)
- Address suppression services

### Legal Protections

- **CCPA** (California): Right to deletion, opt-out
- **GDPR** (EU): Right to erasure, data subject rights
- **SORN**: US government databases
- **State laws**: Various state data broker laws

### Safety Considerations

If you're removing due to:
- Stalking/harassment → Also file police report
- Abusive ex → Consider protective order
- Professional threat → Document & report
- Identity theft → Credit freeze + monitoring

---

## RESOURCES

- Have I Been Pwned: https://haveibeenpwned.com
- Internet Archive Removal: https://help.archive.org/hc/en-us/articles/360004651732
- CCPA Removal Request Template: See templates/ccpa_request.txt
- GDPR Removal Request: See templates/gdpr_request.txt
- Google Search Console: https://search.google.com/search-console
- Bing Webmaster Tools: https://www.bing.com/webmasters

---

## SUPPORT & TROUBLESHOOTING

Common issues:

**Data broker doesn't have opt-out form**
→ Use CCPA/GDPR removal request instead

**Google won't remove cached page**
→ Wait 2-3 weeks for cache expiry

**Page keeps re-appearing after removal**
→ Contact source (site owner) for removal

**Don't know your LinkedIn password**
→ Use password recovery; if old account, may need ID

---

**Next Steps**: Complete Phase 1 (Identity Intake) → Run Phase 2 (Discovery)
