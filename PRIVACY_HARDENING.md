# Privacy Hardening Guide

**Email**: chaitanyajoshi15@gmail.com  
**Priority**: HIGH - Do after removal process begins

---

## 🔐 Password Security

### Create Strong Unique Passwords

**Requirements**:
- Minimum 16 characters
- Mix: uppercase, lowercase, numbers, symbols
- No dictionary words or personal info
- Unique for each account

**Example Format**: `Tr0pic@lSunset#2026$Jazz`

**Tools**: 
- 1Password (recommended)
- Bitwarden (open source, free)
- KeePass (local storage)
- LastPass (though recently compromised, improving)

### Password Manager Setup

1. **Choose a manager** (recommend Bitwarden)
2. **Create strong master password** (20+ characters)
3. **Enable 2FA on password manager account**
4. **Migrate passwords**:
   - Export from browser
   - Import into manager
   - Delete browser-stored passwords
   - Change passwords for high-risk accounts

### High-Risk Accounts to Change First
- [ ] Gmail
- [ ] GitHub
- [ ] Banking
- [ ] PayPal/Financial
- [ ] Amazon
- [ ] Apple ID

---

## 🌐 DNS Privacy

### Switch from ISP DNS to Private DNS

**Current DNS** (default, tracks you):
- Your ISP (Comcast, AT&T, etc.) logs all DNS queries
- Used to profile your browsing

**Private DNS Options**:

**Option 1: Quad9** (best for security)
- IP: 9.9.9.9
- Blocks malware/phishing
- No logging
- DNSSEC enabled

**Option 2: Cloudflare** (fast)
- IP: 1.1.1.1
- Privacy focused
- Fast speeds
- No logging

**Option 3: NextDNS** (customizable)
- IP: 45.90.28.0
- Parental controls
- Ad blocking
- Custom filtering

**Mac Setup**:
1. System Settings → Network → WiFi → Details
2. Click "DNS" tab
3. Add: 9.9.9.9 (or your choice)
4. Remove 8.8.8.8, ISP DNS
5. Test: `nslookup google.com` should use new DNS

**Windows Setup**:
1. Settings → Network & Internet → Change adapter options
2. Right-click → Properties
3. IPv4 Properties → Use custom DNS
4. Primary: 9.9.9.9
5. Secondary: 149.112.122.112

---

## 🔒 VPN Recommendations

### Why VPN Matters
- Hides your IP address
- Encrypts all browsing
- Prevents ISP from seeing websites
- Prevents websites from seeing your location

### VPN Comparison

**Mullvad** (Recommended - No-logs, audited)
- Cost: Free or €5/month
- No account needed
- Audited security
- Based in Sweden (good privacy laws)

**Proton VPN** (Good - Swiss company)
- Cost: Free tier or €120/year
- Swiss jurisdiction
- No-logs verified
- Own infrastructure

**Windscribe** (Budget option)
- Cost: Free or CAD$4.08/month
- Canadian company
- No-logs
- Large server network

### VPN Setup
1. Download app from official website
2. Install and launch
3. Connect to a server
4. Verify: Visit whatismyipaddress.com
5. Your location should be VPN server location

### When to Use VPN
- **Always**: Public WiFi (coffee shops, airports)
- **Recommended**: Home browsing
- **Essential**: Accessing sensitive accounts

---

## 📧 Email Aliases (Privacy Layer)

### Create Secondary Emails for Services

**Gmail Alias Method**:
- Instead of: chaitanyajoshi15@gmail.com
- Use: chaitanyajoshi15+facebook@gmail.com
- Or: chaitanyajoshi15+shopping@gmail.com
- All go to your main inbox
- Can set rules to filter them

**Benefits**:
- Identify which service leaked your email
- Quickly disable compromised aliases
- Reduce exposure of main email

### Implementation
1. Go to: mail.google.com/mail/u/0/#settings/accounts
2. "Add another email address"
3. Format: `chaitanyajoshi15+[service]@gmail.com`
4. Verify with code
5. Use different suffix for each service

### Suggested Aliases
- `+banking` for financial sites
- `+shopping` for e-commerce
- `+social` for social media
- `+games` for gaming
- `+newsletters` for subscriptions

---

## 🔐 Two-Factor Authentication (2FA)

### Accounts to Enable 2FA On (Priority Order)

1. **Email** (Gmail/Outlook)
2. **GitHub**
3. **Banking**
4. **PayPal/Financial**
5. **Amazon**
6. **Apple ID**
7. **Important subscriptions**
8. **Social media** (Facebook, LinkedIn, Twitter)

### 2FA Methods (Best to Worst)

**1. Authenticator Apps** (Best - Recommended)
- Google Authenticator
- Authy (syncs across devices)
- Microsoft Authenticator
- How: Scan QR code, enter 6-digit code
- Backup: Save recovery codes in password manager

**2. Security Keys** (Best - If available)
- Yubikey
- Titan Key
- Backup: Have 2 keys
- Most secure method

**3. SMS** (Acceptable but risky)
- Receives code via text
- Vulnerable to SIM swapping
- Better than nothing

**4. Email** (Least preferred)
- Code sent to email
- Requires email access
- Slowest option

---

## 🛡️ Browser Privacy Settings

### Chrome Privacy
- Settings → Privacy → Close all tabs when closing browser
- Settings → Privacy → Delete cookies/site data on exit
- Install: uBlock Origin, Privacy Badger
- Settings → Site Settings → Block cookies (3rd party)

### Firefox Privacy
- Settings → Privacy → Enhanced Tracking Protection
- Enable: Strict mode
- Extensions → Privacy Badger, uBlock Origin
- about:config → privacy.trackingprotection → true

### Safari Privacy
- Preferences → Privacy → Prevent cross-site tracking
- Preferences → Privacy → Block all cookies
- Preferences → Websites → Don't Auto-Play

---

## 📊 Data Minimization

### Reduce Data You Share

**Don't Provide**:
- Phone number (unless essential)
- Date of birth (unless legal requirement)
- Address (use PO Box if available)
- Social Security number (only for financial/tax)

**Do Provide**:
- Email (use alias)
- Name (can use nickname legally)
- Minimal address info

### Subscription Audits

Quarterly, review:
- [ ] Email subscriptions you signed up for
- [ ] Unsubscribe from unused newsletters
- [ ] Check app permissions
- [ ] Review social media privacy settings

---

## 🔍 Privacy-First Tools

### Alternative Services

**Search Engine**:
- Google → DuckDuckGo (no tracking)
- Or: Startpage (Google results, no tracking)

**Email Client**:
- Outlook/Gmail → Proton Mail (encrypted)
- Or: Tutanota (Swiss, encrypted)

**Messaging**:
- WhatsApp → Signal (open source, no-logs)
- iMessage → Signal (more secure)

**Cloud Storage**:
- Google Drive → Sync.com (encrypted)
- Dropbox → Tresorit (encrypted)

---

## ✅ Privacy Hardening Checklist

- [ ] Password manager set up with strong passwords
- [ ] High-risk accounts password changed
- [ ] DNS switched to private service (Quad9)
- [ ] VPN installed and tested
- [ ] Email aliases created for new services
- [ ] 2FA enabled on top 5 accounts
- [ ] Browser privacy settings hardened
- [ ] Data minimization review completed
- [ ] Monthly calendar reminder set for privacy checks

---

## 📅 Ongoing Privacy Maintenance

### Monthly
- [ ] Check for new data breaches (haveibeenpwned.com)
- [ ] Review browser cookies and cached data
- [ ] Check installed extensions/apps for updates
- [ ] Verify VPN is still working

### Quarterly
- [ ] Review 2FA settings and recovery codes
- [ ] Audit email subscriptions
- [ ] Check app permissions
- [ ] Verify no compromised passwords

### Annually
- [ ] Review all online accounts
- [ ] Update privacy settings across platforms
- [ ] Review VPN/DNS provider changes
- [ ] Assess new privacy threats

