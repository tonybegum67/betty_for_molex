# Cloud Deployment Fix - CSV Processing Enhancement

## Problem
Streamlit Cloud Betty can't access CSV numerical data because it has a stale vector database that was built before our CSV processing enhancements.

**Symptoms:**
- Local Betty: Provides detailed CSV scores like "13% capability impact vs 55% target"
- Cloud Betty: Says "I don't have the exact total impact score calculation"

## Root Cause
Cloud deployment is using an old vector database that doesn't include the enhanced CSV processing that creates searchable entries like:
```
"PROJECT: [project_name] has impact scores: [score1], [score2], [score3]"
```

## Solution

### Option 1: Environment Variable Force Reindex (Recommended)

1. **Go to Streamlit Cloud Dashboard**
   - Navigate to your Betty app settings
   - Go to "Environment variables"

2. **Add Force Reindex Variable**
   ```
   Variable Name: FORCE_REINDEX
   Variable Value: true
   ```

3. **Deploy Changes**
   - Save the environment variable
   - The app will restart automatically
   - Betty will detect `FORCE_REINDEX=true` and rebuild the entire vector database
   - You'll see a message: "🔄 Force reindex requested - rebuilding knowledge base with latest enhancements..."

4. **Remove Variable After Success**
   - Once Betty is working correctly, remove the `FORCE_REINDEX` variable
   - This prevents unnecessary rebuilds on future restarts

### Option 2: Manual Cache Clear

1. **Clear Streamlit Cache**
   - In Streamlit Cloud, go to app settings
   - Use "Clear cache" option
   - Restart the app

2. **Trigger Reprocessing**
   - The app should detect missing data and reprocess automatically
   - May take 2-3 minutes to rebuild the vector database

## Verification

After applying the fix, test with this question:
**"What is the current project impact score for BOM-PIM pain points?"**

**Expected Response (Fixed):**
- Specific numerical scores and percentages
- References to CSV files in Sources section
- Detailed breakdown like local Betty provides

**Problem Response (Broken):**
- Generic response without specific numbers
- "I don't have the exact total impact score calculation"

## Technical Details

The fix adds this code to Betty's initialization:
```python
# Check for forced reindex (for cloud deployment updates)
force_reindex = os.getenv("FORCE_REINDEX", "").lower() in ["true", "1", "yes"]
if force_reindex:
    st.info("🔄 Force reindex requested - rebuilding knowledge base...")
    # Remove existing collection to force complete rebuild
    collections = betty_vector_store.list_collections()
    if collection_name in collections:
        betty_vector_store.delete_collection(collection_name)
```

This ensures cloud deployments can trigger a complete database rebuild to get the latest CSV processing enhancements.

## Files Modified
- `betty_app.py` - Added force reindex capability
- `force_reindex.py` - Standalone reindex script (for local testing)
- `CLOUD_DEPLOYMENT_FIX.md` - This documentation

## Next Steps
After fixing the cloud deployment, both local and cloud Betty should provide identical responses with full CSV data access.