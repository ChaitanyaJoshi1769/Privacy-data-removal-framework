# IMPLEMENTATION GUIDE

## Architecture Overview

```
footprint_ops/
├── footprint_ops.py          # Main CLI entry point
├── models.py                 # Database schema
│
├── footprint_ops/            # Main package (to create)
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py         # Configuration management
│   │   ├── database.py       # Database operations
│   │   └── logger.py         # Logging setup
│   │
│   ├── discovery/            # Phase 2 modules
│   │   ├── __init__.py
│   │   ├── search_engines.py # Google, Bing, etc.
│   │   ├── data_brokers.py   # Spokeo, Whitepages, etc.
│   │   ├── social_media.py   # LinkedIn, Twitter, GitHub, etc.
│   │   ├── metadata.py       # EXIF, PDF metadata
│   │   └── archive.py        # Internet Archive, caches
│   │
│   ├── removal/              # Phase 4 modules
│   │   ├── __init__.py
│   │   ├── account_deletion.py
│   │   ├── data_broker_optout.py
│   │   ├── privacy_requests.py (CCPA/GDPR)
│   │   └── search_removal.py
│   │
│   ├── monitoring/           # Phase 7 modules
│   │   ├── __init__.py
│   │   ├── search_monitor.py
│   │   ├── breach_monitor.py
│   │   └── alerting.py
│   │
│   └── utils/
│       ├── __init__.py
│       ├── browser.py        # Playwright automation
│       ├── correlation.py    # Identity correlation
│       └── reporting.py      # Report generation
│
├── scripts/                  # CLI scripts
│   ├── discover.py           # Discovery orchestration
│   ├── analyze.py            # Analysis & prioritization
│   ├── remove.py             # Removal orchestration
│   └── monitor.py            # Monitoring orchestration
│
├── tests/                    # Unit tests
└── docs/                     # Additional documentation
```

## Phase-by-Phase Implementation

### Phase 1: Database & Config (COMPLETE ✓)

**Status**: Database models and CLI framework ready

```python
# models.py - Already complete
# - 16 tables defined
# - Relationships configured
# - Enums for status tracking
```

### Phase 2: Discovery Implementation (IN PROGRESS)

**Module**: `footprint_ops/discovery/`

**Submodules to implement**:

1. **search_engines.py** (Google, Bing, DuckDuckGo, Yandex)
   ```python
   class SearchEngineDiscovery:
       def google_search(name, email, phone)
       def bing_search(name, email, phone)
       def extract_results(html)
       def get_cache_version(url)
   ```

2. **data_brokers.py** (Spokeo, Whitepages, Intelius, MyLife)
   ```python
   class DataBrokerDiscovery:
       def spokeo_search(name, email, phone)
       def whitepages_search(name, email, phone)
       def parse_listing(html)
       def extract_data_exposed(listing)
   ```

3. **social_media.py** (LinkedIn, Twitter, GitHub, Reddit, etc.)
   ```python
   class SocialMediaDiscovery:
       def linkedin_search(name, email)
       def twitter_search(username)
       def github_search(username)
       def reddit_search(username)
   ```

4. **metadata.py** (EXIF, PDF, document metadata)
   ```python
   class MetadataExtraction:
       def extract_exif(image_url)
       def extract_pdf_metadata(pdf_url)
       def reverse_image_search(image_url)
   ```

5. **archive.py** (Internet Archive, caches)
   ```python
   class ArchiveDiscovery:
       def wayback_machine_search(domain)
       def google_cache_search(url)
       def common_crawl_search(domain)
   ```

### Phase 3: Analysis (Planned)

**Module**: `footprint_ops/analysis/`

```python
class ExposureAnalysis:
    def classify_severity(exposure)  # critical/high/medium/low
    def calculate_risk_score(exposure)
    def build_correlation_graph(exposures)
    def generate_timeline(exposures)
```

### Phase 4: Removal (Planned)

**Module**: `footprint_ops/removal/`

1. **account_deletion.py**
   ```python
   class AccountDeletion:
       def delete_linkedin(credentials)
       def delete_facebook(credentials)
       def delete_old_email(credentials)
   ```

2. **data_broker_optout.py**
   ```python
   class DataBrokerOptout:
       def spokeo_optout(name, email)
       def whitepages_optout(name, email)
       def batch_optout(exposures)
   ```

3. **privacy_requests.py**
   ```python
   class PrivacyRequest:
       def generate_ccpa_request(name, email, company)
       def generate_gdpr_request(name, email, company)
       def send_requests(requests, method='email')
   ```

4. **search_removal.py**
   ```python
   class SearchRemoval:
       def google_removal_request(url)
       def bing_removal_request(url)
       def cache_removal_request(url)
   ```

### Phase 5: Search Suppression (Planned)

```python
class SearchSuppression:
    def request_url_removal(url)
    def request_cache_removal(url)
    def create_positive_profiles()
    def monitor_search_rank()
```

### Phase 7: Monitoring (Planned)

**Module**: `footprint_ops/monitoring/`

```python
class ContinuousMonitoring:
    def daily_search_scan()
    def weekly_data_broker_scan()
    def breach_monitoring()
    def image_monitoring()
    def generate_alerts()
```

## Implementation Priority

### Tier 1 (Essential)
1. Search engine discovery (Google, Bing)
2. Data broker discovery (Spokeo, Whitepages)
3. Basic removal (account deletion, data broker opt-out)

### Tier 2 (Important)
4. Social media enumeration
5. CCPA/GDPR request automation
6. Search console integration

### Tier 3 (Enhanced)
7. Metadata extraction
8. Archive searching
9. Continuous monitoring
10. Advanced correlation analysis

## Development Workflow

### 1. Create Feature Branch

```bash
git checkout -b feature/phase-2-discovery
```

### 2. Implement Module

```python
# footprint_ops/discovery/search_engines.py
import click
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

class GoogleDiscovery:
    """Google Search OSINT"""
    
    def __init__(self, headless=True):
        self.headless = headless
    
    def search(self, query: str, pages: int = 5) -> List[Dict]:
        """
        Search Google for query
        
        Args:
            query: Search query
            pages: Number of pages to search
        
        Returns:
            List of results: [{'title': '', 'url': '', 'snippet': ''}]
        """
        logger.info(f"Searching Google for: {query}")
        
        results = []
        # Implementation here (using Playwright)
        
        return results
```

### 3. Add Tests

```python
# tests/test_discovery.py
import pytest
from footprint_ops.discovery.search_engines import GoogleDiscovery

def test_google_search():
    discoverer = GoogleDiscovery()
    results = discoverer.search("test name")
    assert isinstance(results, list)
    assert len(results) >= 0
```

### 4. Integrate into CLI

```bash
# Update footprint_ops.py to call new modules
python footprint_ops.py discover --engine google --query "test"
```

### 5. Commit & Push

```bash
git add footprint_ops/ tests/
git commit -m "Feature: Google search discovery

- Implemented Google OSINT search
- Added page scraping and result extraction
- Integrated with CLI
- Added unit tests"
git push origin feature/phase-2-discovery
```

### 6. Create Pull Request (Optional)

```bash
gh pr create \
  --title "Feature: Phase 2 Discovery - Search Engines" \
  --body "Implements Google, Bing, DuckDuckGo search"
```

## Testing Strategy

### Unit Tests

```python
# tests/test_models.py
def test_identity_model():
    identity = Identity(legal_name="John Doe")
    assert identity.legal_name == "John Doe"
```

### Integration Tests

```python
# tests/test_discovery_integration.py
def test_full_discovery_workflow():
    profile = load_identity_profile()
    results = run_discovery(profile)
    assert results['total_exposures'] > 0
```

### Run Tests

```bash
pip install pytest pytest-cov
pytest tests/ -v --cov=footprint_ops/
```

## Code Quality

### Linting

```bash
pip install ruff black mypy
ruff check footprint_ops/
black footprint_ops/
mypy footprint_ops/
```

### Pre-commit Hook (Optional)

```bash
pip install pre-commit
# Create .pre-commit-config.yaml
pre-commit run --all-files
```

## Documentation

### Add Docstrings

```python
class GoogleDiscovery:
    """
    Google Search OSINT Discovery
    
    Performs systematic Google searches to discover public-facing
    personal data traces.
    
    Example:
        >>> discoverer = GoogleDiscovery()
        >>> results = discoverer.search("John Smith email")
        >>> for result in results:
        ...     print(result['url'])
    """
```

### API Documentation

```bash
# Generate API docs
pip install sphinx
sphinx-quickstart docs/
make -C docs/ html
```

## Performance Considerations

### Avoid Blocking

```python
# Bad
for broker in brokers:
    result = search_broker(broker)  # Blocks

# Good
import asyncio
async def search_all_brokers(brokers):
    tasks = [search_broker(b) for b in brokers]
    return await asyncio.gather(*tasks)
```

### Rate Limiting

```python
import time
time.sleep(2)  # Between requests to avoid blocking

# Or use:
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
```

### Caching

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def get_broker_listings(email: str):
    return search_broker(email)
```

## Database Integration

### Create Records

```python
from sqlalchemy.orm import Session
from models import Exposure, Identity

def save_exposure(session: Session, identity_id: str, exposure_data: Dict):
    exposure = Exposure(
        identity_id=identity_id,
        exposure_type="search_engine",
        platform="google",
        url=exposure_data['url'],
        severity="medium",
        data_exposed=exposure_data['data']
    )
    session.add(exposure)
    session.commit()
```

### Query Records

```python
from sqlalchemy import select
from models import Exposure

# Get all high-severity exposures
stmt = select(Exposure).where(Exposure.severity == "high")
results = session.execute(stmt).scalars().all()
```

## Deployment

### Package for Distribution

```bash
python setup.py sdist bdist_wheel
pip install dist/footprint_ops-0.1.0-py3-none-any.whl
footprint-ops --help
```

### GitHub Releases

```bash
git tag v0.1.0
git push origin v0.1.0
gh release create v0.1.0 --generate-notes
```

## Ongoing Maintenance

### Version Bumping

```bash
# Update version in:
# - pyproject.toml
# - setup.py
# - __init__.py

git tag v0.2.0
git push --tags
```

### Dependency Updates

```bash
pip list --outdated
pip install --upgrade requirement-name
```

### Security Updates

```bash
# Check for vulnerabilities
pip install bandit
bandit -r footprint_ops/
```

---

## Next Steps

1. **Create main package structure**
   ```bash
   mkdir -p footprint_ops/{core,discovery,removal,monitoring,utils}
   touch footprint_ops/__init__.py
   touch footprint_ops/core/__init__.py
   # etc.
   ```

2. **Implement Phase 2 Discovery**
   - Start with Google search
   - Add Bing search
   - Add data broker enumeration

3. **Add tests as you go**
   - Unit tests for each module
   - Integration tests for workflows

4. **Push progress regularly**
   - Commit after each feature
   - Update README with progress
   - Create GitHub Issues for tracking

5. **Document as you code**
   - Docstrings in every module
   - API documentation
   - Usage examples

---

**Begin with**: 
```bash
mkdir footprint_ops && cd footprint_ops && git init
```
