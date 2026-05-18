# GITHUB SETUP & DEPLOYMENT GUIDE

## 🔐 Step 1: Authenticate with GitHub

Choose ONE method:

### Method A: GitHub CLI (Recommended)

```bash
# Install GitHub CLI if needed
brew install gh  # macOS
# or
winget install GitHub.cli  # Windows
# or
sudo apt-get install gh  # Linux

# Authenticate
gh auth login

# Follow the prompts:
# - Choose: GitHub.com
# - Choose: HTTPS
# - Authenticate in browser
# - Authorize CLI
```

### Method B: Git + Personal Access Token

1. **Create GitHub Personal Access Token**
   - Go to: https://github.com/settings/tokens
   - Click "Generate new token" → "Generate new token (classic)"
   - Name: "footprint-ops"
   - Scope: ✓ repo ✓ workflow
   - Click "Generate token"
   - **Copy token immediately** (you won't see it again)

2. **Configure Git**
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
git config --global credential.helper store
```

3. **First Push**
   - Git will ask for username and password
   - Username: `your-github-username`
   - Password: `your-personal-access-token` (paste the token)

### Method C: SSH Key (if already set up)

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
# SSH keys should already be configured
```

---

## 📦 Step 2: Create Repository on GitHub

### Option A: Using GitHub CLI (Fastest)

```bash
cd /path/to/footprint_ops

# Create public repository
gh repo create footprint-ops \
  --public \
  --source=. \
  --remote=origin \
  --push \
  --description "Digital footprint remediation toolkit"
```

### Option B: Manual (via GitHub.com)

1. Go to https://github.com/new
2. **Repository name**: `footprint-ops`
3. **Description**: "Digital footprint remediation and privacy minimization toolkit"
4. **Public** (checked)
5. ✓ Initialize with `.gitignore` (Python)
6. Click "Create repository"

Then connect your local repo:
```bash
cd /path/to/footprint_ops
git remote add origin https://github.com/ChaitanyaJoshi1769/footprint-ops.git
git branch -M main
git push -u origin main
```

---

## 🚀 Step 3: Initial Push

```bash
cd /path/to/footprint_ops

# Stage all files
git add .

# Commit
git commit -m "Initial commit: Footprint Ops Phase 0

- Complete project structure
- Database schema (16 tables)
- CLI framework
- Configuration templates
- Identity intake questionnaire
- Operational documentation"

# Push to GitHub
git push -u origin master
# or
git push -u origin main
```

---

## 📝 Step 4: Ongoing Development & Progress

### Commit Convention

```bash
# After completing each phase:

git add .
git commit -m "Phase 2 Complete: Discovery Module

- Implemented OSINT discovery
- Added search engine integration
- Data broker enumeration
- Results storage

[Phase 2] [Discovery] [Feature Complete]"
```

### Push After Changes

```bash
# After making changes
git add .
git commit -m "Descriptive message"
git push origin main
```

### Check Status

```bash
git status          # See what's changed
git log --oneline   # See commit history
```

---

## 🔄 Step 5: Tracking Progress in GitHub

### Create Issues for Each Phase

```bash
# Create an issue for Phase 1
gh issue create \
  --title "Phase 1: Identity Intake" \
  --body "Complete identity intake questionnaire implementation"

# Create milestone for Phase 2
gh label create "phase-2-discovery" --color "0075ca"
```

### Use GitHub Projects

1. Go to your repo → "Projects" → "New"
2. Create board: "Footprint Ops Phases"
3. Add columns: To Do, In Progress, Done
4. Add cards for each phase

### Update README with Progress

Edit `README.md`:
```markdown
## Phase Progress

- [x] Phase 0: Setup & Infrastructure
- [ ] Phase 1: Identity Intake
- [ ] Phase 2: Discovery & Enumeration
- [ ] Phase 3: Exposure Analysis
- [ ] Phase 4: Removal Operations
- [ ] Phase 5: Search Suppression
- [ ] Phase 6: Privacy Hardening
- [ ] Phase 7: Continuous Monitoring
```

---

## 🐳 Step 6: Optional - CI/CD Setup

### Add GitHub Actions (Optional)

Create `.github/workflows/test.yml`:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.11, 3.12]

    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Run tests
      run: pytest tests/
    
    - name: Check code style
      run: |
        pip install ruff black mypy
        ruff check footprint_ops/
        black --check footprint_ops/
```

### Add Build Badge to README

After first successful workflow:

```markdown
![Tests](https://github.com/ChaitanyaJoshi1769/footprint-ops/workflows/Tests/badge.svg)
```

---

## 📊 Step 7: Document Implementation Progress

Create `IMPLEMENTATION_LOG.md`:

```markdown
# Implementation Progress Log

## Timeline

**2024-05-17**
- ✓ Phase 0 complete
- ✓ Database schema (16 tables)
- ✓ CLI framework (footprint_ops.py)
- ⏳ Phase 1 implementation in progress

**2024-05-18**
- ✓ Identity intake questionnaire
- ⏳ Discovery modules
- ⏳ Removal automation

## Completed Features

### Phase 0: Complete
- [x] Project structure
- [x] Database models
- [x] Configuration templates
- [x] CLI framework
- [x] Documentation

### Phase 1: In Progress
- [x] Questionnaire design
- [ ] Database integration
- [ ] Interactive CLI
- [ ] Identity correlation

### Phase 2: Planned
- [ ] Search engine discovery
- [ ] Data broker enumeration
- [ ] Social media scanning
- [ ] Archive crawling

## Known Issues

None yet.

## Next Steps

1. Complete Phase 1 implementation
2. Add discovery modules
3. Implement removal automation
4. Add monitoring system
```

---

## ✅ Quick Checklist

- [ ] GitHub CLI or SSH key configured
- [ ] Created repository on GitHub
- [ ] Initial commit pushed
- [ ] README updated with progress
- [ ] .gitignore applied (no sensitive data)
- [ ] Phase milestones created (optional)
- [ ] CI/CD configured (optional)
- [ ] Implementation log started

---

## 🚨 IMPORTANT: Never Commit

```
NEVER add these to git:

.env (contains API keys)
*.db (contains encrypted identity data)
config.yaml (contains sensitive settings)
intel/* (raw personal data)
discovery/* (OSINT results)
correlation/* (identity graphs)
logs/* (operational logs)
```

These are in `.gitignore` - verify:
```bash
git status  # Should NOT show above files
```

---

## 💬 Push After Each Phase

Example workflow:

```bash
# Phase 1 complete
git add footprint_ops/
git commit -m "Phase 1 Complete: Identity Intake

- Questionnaire with 8 sections
- Database integration
- Identity correlation analysis
- JSON export

[Phase 1][Feature Complete]"
git push

# Phase 2 complete  
git add footprint_ops/ scripts/
git commit -m "Phase 2 Complete: OSINT Discovery

- Google/Bing/DuckDuckGo search
- Data broker enumeration (10+ platforms)
- Social media scanning (15+ platforms)
- Metadata extraction
- Results storage

[Phase 2][Feature Complete]"
git push
```

---

## 🎯 Next Steps

1. **Authenticate with GitHub**
   ```bash
   gh auth login
   ```

2. **Create repository**
   ```bash
   cd /path/to/footprint_ops
   gh repo create footprint-ops --public --source=. --push
   ```

3. **Verify push**
   ```bash
   git log
   git remote -v
   ```

4. **Start Phase 1 implementation**
   ```bash
   python footprint_ops.py intake
   ```

5. **Track progress**
   - Create GitHub Issues
   - Update README with checkmarks
   - Push progress commits regularly

---

## 📚 Reference

- GitHub Docs: https://docs.github.com
- Git Docs: https://git-scm.com/doc
- GitHub CLI: https://cli.github.com
- Personal Access Tokens: https://github.com/settings/tokens

---

**Questions?** See `README.md` or `OPERATIONAL_PLAYBOOK.md`
