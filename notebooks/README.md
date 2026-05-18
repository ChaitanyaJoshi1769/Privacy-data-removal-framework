# Interactive Jupyter Notebooks

Step-by-step interactive guides for using the Privacy Framework.

## Available Notebooks

### 1. **01_getting_started.ipynb** ⭐ START HERE
**Duration**: 30 minutes  
**What you'll do**:
- Set up your identity profile
- Check for data breaches (HIBP)
- Discover exposures
- Generate removal plan
- Set up de-indexing
- Configure monitoring
- View dashboard

**Best for**: First-time users, understanding workflow

### 2. **02_broker_removal.ipynb**
**Duration**: 45 minutes  
**Topics**:
- Deep dive into each data broker
- Understanding difficulty levels
- Step-by-step removal procedures
- Tracking confirmations
- Verification methods

**Best for**: Executing data broker removals

### 3. **03_search_deindexing.ipynb**
**Duration**: 20 minutes  
**Topics**:
- Google Search Console removal
- Bing Webmaster Tools removal
- Cache purging
- Robots.txt configuration
- Verification procedures

**Best for**: Setting up search engine removal

### 4. **04_monitoring_analysis.ipynb**
**Duration**: 15 minutes  
**Topics**:
- Monitoring job configuration
- Breach monitoring analysis
- Progress tracking
- Report generation
- Dashboard interpretation

**Best for**: Monitoring and analysis

## How to Use These Notebooks

### 1. Install Jupyter
```bash
pip install jupyter notebook
```

### 2. Start Jupyter
```bash
jupyter notebook
```

### 3. Open a Notebook
1. Navigate to `notebooks/` folder
2. Click on notebook file
3. Follow along with instructions
4. Edit cells with your information

### 4. Run Cells
- Click cell
- Press Shift + Enter to execute
- View results below

## Tips for Using Notebooks

✅ **Do**:
- Run cells in order
- Edit configuration cells with your info
- Take notes on results
- Save outputs

❌ **Don't**:
- Skip cells
- Run cells multiple times without clearing
- Change cell structure
- Run without editing configuration

## Configuration Cells

Each notebook has configuration cells where you should edit:

```python
identity = {
    "name": "Your Full Name",           # ← EDIT
    "email": "your@email.com",          # ← EDIT
    "phone": "+1-XXX-XXX-XXXX",        # ← EDIT
    "github_username": "your-username", # ← EDIT
}
```

## Output Files

Notebooks automatically save results to:
- `logs/` - JSON outputs
- `intel/` - Identity profiles
- `removal/` - Removal plans
- `discovery/` - Scan results

## Troubleshooting

### Module Import Error
```python
import sys
sys.path.insert(0, '../scripts')
```
This is already included in notebooks.

### API Connection Issues
Some cells require internet (HIBP, search engines). If offline:
- Results will show as 0/empty
- Continue with next cells
- Retry when connection is available

### File Not Found
Ensure notebooks are in `notebooks/` directory:
```
Privacy-data-removal-framework/
  notebooks/
    01_getting_started.ipynb     ← Here
    02_broker_removal.ipynb
    03_search_deindexing.ipynb
    04_monitoring_analysis.ipynb
  scripts/
  logs/
```

## Learning Path

### For Beginners
1. Read GETTING_STARTED.md
2. Run 01_getting_started.ipynb
3. Read QUICK_START.md
4. Run notebooks 2-4 as needed

### For Experienced Users
1. Review notebooks for reference
2. Use CLI directly
3. Customize as needed

### For Developers
1. Examine notebook structure
2. Review automation tools
3. Extend functionality

## Integration with CLI

Notebooks and CLI are complementary:

**Notebooks are best for**:
- Learning interactively
- One-time setup
- Exploring data
- Experimentation

**CLI is best for**:
- Automation
- Scripting
- Scheduling
- Production use

You can use either or both!

## Advanced Usage

### Running Notebooks from Command Line
```bash
# Convert to Python script
jupyter nbconvert --to python 01_getting_started.ipynb

# Run as Python script
python 01_getting_started.py
```

### Batch Execution
```python
# In a Python script
import nbformat
from nbconvert.preprocess import ExecutePreprocessor

notebook = nbformat.read('01_getting_started.ipynb', as_version=4)
ep = ExecutePreprocessor()
ep.preprocess(notebook)
```

## Support

For notebook issues:
1. Check your Python version (3.7+)
2. Verify dependencies installed
3. Check file paths
4. Review error messages

For tool questions:
- See AUTOMATION_GUIDE.md
- Check tool source code
- Review tool-specific documentation

## Contributing

Want to create more notebooks?

1. Follow naming convention: `NN_topic.ipynb`
2. Include markdown explanations
3. Add configuration cells
4. Save outputs to logs/
5. Add to this README

---

**Ready to start?** Open `01_getting_started.ipynb` in Jupyter!

```bash
jupyter notebook notebooks/01_getting_started.ipynb
```
