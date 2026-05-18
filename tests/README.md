# Automated Testing Suite

Comprehensive test coverage for all automation tools.

## Running Tests

### Run All Tests
```bash
python -m pytest tests/ -v
```

### Run Specific Test File
```bash
python -m pytest tests/test_automation_tools.py -v
```

### Run Specific Test Class
```bash
python -m pytest tests/test_automation_tools.py::TestHIBPMonitor -v
```

### Run Specific Test
```bash
python -m pytest tests/test_automation_tools.py::TestHIBPMonitor::test_initialization -v
```

### Run with Coverage
```bash
pip install pytest-cov
python -m pytest tests/ --cov=scripts --cov-report=html
```

### Run Using unittest (Alternative)
```bash
python tests/test_automation_tools.py
```

## Test Structure

### Test Classes

1. **TestHIBPMonitor**
   - HIBP monitor initialization
   - Breach result structure validation
   - Risk assessment logic

2. **TestGSCRemovalAgent**
   - Google Search Console agent initialization
   - Removal request structure
   - robots.txt generation
   - Verification checklist

3. **TestBingRemovalAgent**
   - Bing agent initialization
   - URL removal requests
   - Batch removal generation
   - Disavow file generation

4. **TestDataBrokerAutomation**
   - Broker count and information
   - Removal plan structure
   - Phase organization
   - Removal tracking
   - Verification logging

5. **TestMonitoringOrchestrator**
   - Job registration and setup
   - Daily/weekly/monthly checks
   - Monitoring report generation
   - Simulation execution

6. **TestDashboardServer**
   - Dashboard initialization
   - Stats calculation
   - HTML generation

7. **TestIntegration**
   - Complete workflow integration
   - Data consistency across tools

8. **TestBrokerTracker**
   - Tracker initialization
   - Submission logging
   - Verification tracking

9. **TestDataValidation**
   - Broker list completeness
   - Required field validation

## Test Coverage

### What's Tested

✅ **Initialization**: All classes instantiate correctly  
✅ **Data Structure**: Output has required fields  
✅ **Logic**: Calculations produce expected results  
✅ **Integration**: Components work together  
✅ **Validation**: Required data is present  

### Coverage by Tool

| Tool | Tests | Coverage |
|------|-------|----------|
| HIBP Monitor | 3 | ✓ |
| GSC Agent | 4 | ✓ |
| Bing Agent | 4 | ✓ |
| Data Broker | 8 | ✓ |
| Monitoring | 6 | ✓ |
| Dashboard | 3 | ✓ |
| Integration | 2 | ✓ |
| Validation | 2 | ✓ |

**Total**: 32+ test cases

## Continuous Integration

Tests run automatically on:
- Every push to repository
- Pull requests
- Scheduled daily

See `.github/workflows/testing.yml` for CI/CD configuration.

## Test Failures

### Common Issues

**Import Error**
```
ModuleNotFoundError: No module named 'hibp_monitor'
```
**Solution**: Ensure scripts/ is in Python path (already done in test file)

**API Failures**
```
RequestException: Connection timeout
```
**Solution**: Tests mock API responses, internet not required

**File Not Found**
```
FileNotFoundError: logs/
```
**Solution**: Test automatically creates directories

### Debugging Tests

```bash
# Run with detailed output
python -m pytest tests/ -vv

# Run with print statements shown
python -m pytest tests/ -s

# Run with debugging on failure
python -m pytest tests/ --pdb
```

## Adding New Tests

### Test Template
```python
import unittest

class TestNewTool(unittest.TestCase):
    """Test new automation tool"""
    
    def setUp(self):
        """Initialize before each test"""
        # Setup code here
        pass
    
    def test_basic_functionality(self):
        """Test basic functionality"""
        # Arrange
        input_data = {}
        
        # Act
        result = function(input_data)
        
        # Assert
        self.assertIsNotNone(result)
        self.assertEqual(result["key"], "expected_value")
    
    def tearDown(self):
        """Clean up after each test"""
        # Cleanup code here
        pass
```

### Add to Test Suite
1. Create test class inheriting from `unittest.TestCase`
2. Add test methods prefixed with `test_`
3. Use assertions to verify behavior
4. Add to appropriate test file

## Running Tests in CI/CD

GitHub Actions automatically runs tests:

```yaml
- name: Run tests
  run: python -m pytest tests/ -v
```

Tests must pass before merging to main.

## Performance Benchmarks

Expected test execution times:

| Test Class | Time |
|-----------|------|
| HIBP Monitor | <100ms |
| GSC Agent | <50ms |
| Bing Agent | <50ms |
| Data Broker | <200ms |
| Monitoring | <150ms |
| Dashboard | <100ms |
| Integration | <300ms |
| **Total** | **~1 second** |

## Dependencies

Required for testing:
```bash
pip install pytest pytest-cov
```

All tools tested have minimal external dependencies.

## Best Practices

✅ **Do**:
- Run tests before committing
- Add tests for new features
- Keep tests independent
- Use descriptive test names
- Test both success and failure cases

❌ **Don't**:
- Skip failing tests
- Hardcode values
- Rely on external services
- Share state between tests
- Use sleep() for timing

## Continuous Monitoring

Tests also serve as health checks:

- **Daily**: Run to verify functionality
- **Weekly**: Extended test suite with external APIs
- **Monthly**: Performance benchmarks

See `.github/workflows/daily-monitoring.yml`

## Test Reports

Generate test coverage reports:

```bash
# HTML coverage report
python -m pytest tests/ --cov=scripts --cov-report=html

# Open report
open htmlcov/index.html
```

## Contributing Tests

When adding new functionality:

1. Write test first (TDD)
2. Implement feature
3. Verify test passes
4. Add documentation

## Support

For test issues:
1. Check test output for specific error
2. Review test code
3. Check tool source code
4. Review tool documentation

---

**Status**: All tests passing ✓

To run tests:
```bash
python -m pytest tests/ -v
```
