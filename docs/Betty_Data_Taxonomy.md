# Betty AI Assistant - Data Taxonomy & Pipeline Specification

**Version**: 1.0
**Date**: January 2025
**Author**: BoldARC - Chief AI Officer
**Purpose**: Comprehensive data taxonomy for Betty's training data, RAG capabilities, and future pipeline development

---

## Executive Summary

This document defines the complete data taxonomy for Betty AI Assistant, establishing standardized classifications, validation rules, and pipeline requirements to ensure Betty only trains on data compatible with her RAG (Retrieval-Augmented Generation) model capabilities.

**Key Objectives**:
- Document all current data sources and structures
- Define data compatibility requirements for RAG model
- Establish validation rules for future data ingestion
- Provide pipeline specifications for automated data processing

---

## Table of Contents

1. [Data Architecture Overview](#data-architecture-overview)
2. [Primary Data Categories](#primary-data-categories)
3. [Data Format Specifications](#data-format-specifications)
4. [RAG Model Requirements](#rag-model-requirements)
5. [Data Processing Pipeline](#data-processing-pipeline)
6. [Validation Rules & Quality Gates](#validation-rules--quality-gates)
7. [Future Pipeline Recommendations](#future-pipeline-recommendations)

---

## Data Architecture Overview

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                    Betty AI System                           │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  Input Layer         Processing Layer      Storage Layer     │
│  ───────────────    ──────────────────    ───────────────   │
│  • Documents        • Text Extraction     • ChromaDB        │
│  • Structured Data  • Chunking           • Vector Store     │
│  • Metadata         • Embedding          • Metadata DB      │
│                     • Validation                             │
│                                                               │
│  Retrieval Layer    Generation Layer     Output Layer        │
│  ───────────────    ──────────────────   ───────────────    │
│  • Semantic Search  • Claude/GPT-4o      • Responses        │
│  • Reranking        • Context Assembly   • Citations        │
│  • Filtering        • Prompt Engineering • Feedback         │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow Architecture

```
Raw Data → Validation → Extraction → Cleaning → Chunking →
Embedding → Vector Storage → Retrieval → Generation → Response
```

---

## Primary Data Categories

### Category 1: Strategic Framework Documents

**Description**: Documents defining Outcome-Based Thinking (OBT), GPS methodology, and strategic frameworks

**Purpose**: Enable Betty to coach users on OBT principles and strategic transformation

**Subcategories**:

#### 1.1 OBT & GPS Foundation
- **Examples**:
  - `OBT and GPS Construction Rules.docx`
  - `OBT GPS Definitions.docx`
  - `GPS-OBT Talking Points.docx`
  - `THE GPS_OBT Story.docx`
- **Content Type**: Instructional, definitional, methodological
- **Key Concepts**: Outcome statements, What/How classification, GPS tiers (Destination, Highway, Main Street, County Road)
- **RAG Capability**: High (text-based, structured concepts, clear definitions)

#### 1.2 Strategic Transformation Guides
- **Examples**:
  - `Molex - Becoming and Outcomes Based Organization.docx`
  - `Betty for Molex GPS.docx`
- **Content Type**: Organizational transformation, change management
- **Key Concepts**: Cultural transformation, strategic alignment, organizational outcomes
- **RAG Capability**: High (narrative structure, contextual guidance)

#### 1.3 Reference Architecture
- **Examples**:
  - `Molex Manufacturing BA Reference Architecture.docx`
- **Content Type**: Technical architecture, business capabilities
- **Key Concepts**: Business capabilities, value streams, system architecture
- **RAG Capability**: High (structured information, hierarchical relationships)

### Category 2: Project Impact Data

**Description**: Structured data showing project impacts on capabilities and pain points

**Purpose**: Enable Betty to provide data-driven insights on project effectiveness and strategic alignment

**Subcategories**:

#### 2.1 Current Project Impact (CSV)
- **Examples**:
  - `BOM-PIM_total-project-impact.csv`
  - `BOM-PIM_current_project_impact_to_capabilities.csv`
  - `BOM-PIM_current-project-impact-to-pain-points.csv`
  - `Change Management_total-project-impact.csv`
  - `Change Management_current-project-impact-to-pain-points.csv`
  - `Change Management_current-project-impact-to-capabilities.csv`
- **Content Type**: Quantitative metrics, project scores, impact assessments
- **Data Structure**:
  - Project names (columns)
  - Impact dimensions (rows): Pain Points, Capability Features, Impact Index, Z-Score
  - Percentage values (cells)
- **Key Metrics**: Impact Index, Z-Score, weighted pain points, capability features
- **RAG Capability**: Medium-High (structured, requires enhanced CSV processing for search)

#### 2.2 Future Project Impact (CSV)
- **Examples**:
  - `BOM-PIM_future_project_impact_to_capabilities.csv`
  - `BOM-PIM_future_project_impact_to_pain_points.csv`
  - `Change Management_future-project-impact-to-capabilities.csv`
  - `Change Management_future-project-impact-to-pain-points.csv`
- **Content Type**: Predictive metrics, planned project assessments
- **Data Structure**: Same as current projects
- **RAG Capability**: Medium-High (requires cross-referencing with current data)

#### 2.3 Project Descriptions & Details
- **Examples**:
  - `DESCRIPTION OF CURRENT BOM PIM PROJECTS (082825).docx`
  - `DESCRIPTION OF FUTURE BOM PIM PROJECT (082825).docx`
  - `Potential Future Change Control Management Projects (O82225).docx`
- **Content Type**: Project specifications, objectives, scope
- **RAG Capability**: High (detailed text, contextual information)

### Category 3: Domain-Specific Knowledge

**Description**: Specialized knowledge for specific business domains (BOM/PIM, Change Management, Design Management)

**Subcategories**:

#### 3.1 BOM & PIM (Bill of Materials / Product Information Management)
- **Examples**:
  - `BOM and PIM GPS Outcomes (082625).docx`
  - `BOM PIM Capabilities Definitions and Maturity.docx`
  - `Impact of Future BOM PIM Projects on Pain Points 072825.docx`
  - `BOM PIM CURRENT PROJECT IMPACT TO PAIN POINTS with Explanations - Final 072225.docx`
- **Content Type**: Domain definitions, capability maturity models, pain points
- **Key Concepts**: Product data management, engineering BOMs, manufacturing BOMs, master data
- **RAG Capability**: High (domain-specific terminology, structured knowledge)

#### 3.2 Change Management & Change Control
- **Examples**:
  - `Product Change Control Management GPS Outcomes.docx`
  - `CHANGE CONTROL MANAGEMENT CAPABILITIES AND MATURITY LEVELS.docx`
  - `Change Control Management Roadmap Mile Marker Definitions.docx`
  - `Change_Control_Roadmap_MileMarkers_ClosedLoopMerged.docx`
  - `The Change Managment Story v2.0 (2).docx`
  - `Change Management Pain Point - August 15, 2025.docx`
- **Content Type**: Process definitions, maturity models, roadmaps, pain points
- **Key Concepts**: Engineering change orders (ECOs), change workflows, governance
- **RAG Capability**: High (process-oriented, sequential information)

#### 3.3 Design Management & Collaboration
- **Examples**:
  - `DESIGN MGMT and COLLABORATION CAPABILITIES DEFINITION and MATURITY (090125).docx`
  - `DESIGN MGMT & COLLABORATION OUTCOMES (090125).docx`
  - `The Future of Design at Molex_ Sarah_s Complete Journey - BOM and PIM (Revised August 7, 2025) (1).docx`
- **Content Type**: Capability definitions, user journey narratives, collaboration frameworks
- **Key Concepts**: Design workflows, collaboration tools, design-to-manufacturing handoff
- **RAG Capability**: High (narrative structure, scenario-based information)

### Category 4: GPS Outcomes Master Data

**Description**: Structured JSON data containing the complete GPS outcomes hierarchy

**Subcategories**:

#### 4.1 GPS Outcomes Database
- **Examples**:
  - `GPS_Outcomes_Master.json`
  - `GPS_Outcomes_Master_backup.json`
- **Content Type**: Hierarchical outcome structures, cluster-based organization
- **Data Structure**:
  ```json
  {
    "outcome_id": "ACQ-001",
    "cluster": "Acquire Customer",
    "cluster_id": "ACQ",
    "highest_order_outcome": "The most desired companies eagerly become our customers",
    "tier_level": 1,
    "outcome_text": "Our brand is immediately recognized and revered",
    "parent_id": null,
    "children_ids": ["ACQ-002", "ACQ-003"]
  }
  ```
- **Key Attributes**:
  - `outcome_id`: Unique identifier (cluster_id + number)
  - `cluster`: Business cluster name
  - `highest_order_outcome`: Top-level strategic outcome
  - `tier_level`: Hierarchical level (1-3)
  - `outcome_text`: Specific outcome statement
  - `parent_id`: Parent outcome reference
  - `children_ids`: Child outcomes array
- **Total Records**: 288 outcomes across multiple clusters
- **Clusters**: Acquire Customer, Build Product, Produce & Fulfill, Grow Customer, Enable the Business
- **RAG Capability**: Medium (requires JSON parsing and relationship mapping; current implementation may need enhancement for deep hierarchical queries)

---

## Data Format Specifications

### Supported File Formats

| Format | Extension | Processing Method | RAG Compatibility | Current Status | Use Cases |
|--------|-----------|-------------------|-------------------|----------------|-----------|
| **PDF** | `.pdf` | PyPDF2 extraction | High | ✅ Active (3 files) | Published documents, reports, presentations |
| **DOCX** | `.docx` | python-docx with structure preservation | High | ✅ Active (24 files) | Working documents, specifications, guidelines |
| **TXT** | `.txt` | Direct UTF-8/Latin-1 decoding | High | ⚠️ Supported but no files currently | Plain text notes, simple documentation |
| **CSV** | `.csv` | Enhanced CSV parsing with context | Medium-High | ❌ NOT in vector DB (10 files exist) | Quantitative data, project metrics, impact scores |
| **JSON** | `.json` | *Currently not processed for RAG* | Low (needs enhancement) | ❌ NOT in vector DB (2 files exist) | Structured data, hierarchical relationships |
| **MD** | `.md` | Treated as TXT | High | ⚠️ Supported but no files currently | Markdown documentation |

### Processing Capabilities by Format

#### PDF (.pdf)
- **Extraction**: Page-by-page text extraction
- **Limitations**: Cannot extract from scanned PDFs (no OCR), complex layouts may lose structure
- **Chunking**: Token-based with overlap
- **Metadata Preserved**: Filename, chunk index
- **Recommended Use**: Final documents, presentations, published reports

#### DOCX (.docx)
- **Extraction**: Advanced structure preservation
  - Heading hierarchy (H1-H6)
  - List formatting (bullet points)
  - Table extraction (row/column structure)
- **Limitations**: Complex formatting, embedded objects, charts not extracted
- **Chunking**: Semantic chunking respects document structure
- **Metadata Preserved**: Filename, chunk index, structure information
- **Recommended Use**: Primary knowledge base documents

#### TXT (.txt) & MD (.md)
- **Extraction**: Direct text decoding (UTF-8 primary, Latin-1 fallback)
- **Limitations**: No structure information
- **Chunking**: Token-based or semantic
- **Metadata Preserved**: Filename, chunk index
- **Recommended Use**: Simple notes, code documentation, plain text guides

#### CSV (.csv)
- **Current RAG Status**: ❌ **NOT PROCESSED** - CSV files exist but are NOT in ChromaDB vector database
- **Files in Repository**: 10 CSV files (BOM-PIM and Change Management project impact data)
- **Code Capability**: Enhanced CSV parsing implemented in `document_processor.py`
  - Automatic delimiter detection (`,`, `;`, `\t`, `|`)
  - Header identification
  - Row-by-row structured text formatting
  - Project reference detection
  - Searchable entries for known projects
- **Potential Processing Output**:
  ```
  Row 1: Column1: Value1, Column2: Value2, Column3: Value3
  PROJECT: Digital Twin Implementation has impact scores: 65.6%, 37.0%
  ```
- **Why Not in RAG**: CSV files in docs/ folder are not being picked up by knowledge base initialization
- **Impact**: Betty cannot retrieve project impact scores, Z-scores, or capability/pain point percentages via RAG
- **Workaround**: Data may be embedded in system prompt or referenced in DOCX files
- **Recommended Action**: Add CSV files to knowledge base update process
- **Limitations**: Large tables may be chunked mid-row; complex multi-line cells may lose context
- **Metadata Preserved**: Filename, chunk index, column headers

#### JSON (.json)
- **Current RAG Status**: ❌ **NOT PROCESSED** - JSON files exist but are NOT in ChromaDB vector database
- **Files in Repository**: 2 JSON files (`GPS_Outcomes_Master.json`, `GPS_Outcomes_Master_backup.json`)
- **Data Content**: 288 GPS outcomes with hierarchical relationships (outcome_id, cluster, tier_level, parent_id, children_ids)
- **Code Capability**: ❌ **NOT IMPLEMENTED** - No JSON extraction method in `document_processor.py`
- **Current Workaround**:
  - GPS outcomes data available via DOCX files (e.g., `BOM and PIM GPS Outcomes (082625).docx`)
  - JSON structure knowledge embedded in Betty's system prompt
  - Betty knows the framework but cannot semantically search individual outcome records
- **Data Loss**: DOCX files may not have complete 288 outcomes with full hierarchical relationships
- **Impact**:
  - Cannot retrieve specific outcomes by outcome_id
  - Cannot navigate parent-child relationships dynamically
  - Cannot search by cluster, tier_level, or highest_order_outcome efficiently
  - Updates to JSON file don't automatically update RAG knowledge
- **Required Enhancement**:
  - Implement `extract_text_from_json()` method in document_processor
  - JSON parsing and flattening for text extraction
  - Relationship mapping (parent-child, hierarchical)
  - Searchable text generation from nested structures
  - Metadata preservation of JSON paths and relationships
- **Use Cases**: GPS outcomes hierarchy, structured knowledge graphs, complex data relationships
- **Priority**: MEDIUM-HIGH (GPS data exists in DOCX form, but JSON would provide richer structure)

---

## RAG Model Requirements

### Embedding Model Specifications

**Current Model**: `sentence-transformers/all-mpnet-base-v2`

**Alternative Models** (for performance optimization):
- `all-MiniLM-L6-v2` (faster, smaller)
- `paraphrase-MiniLM-L3-v2` (fallback)

**Embedding Dimensions**: 768 (all-mpnet-base-v2)

**Compatibility Requirements**:
- All documents must be convertible to plain text
- Text must be semantically meaningful when chunked
- Chunk size: 1000 tokens (configurable: 800-1200)
- Chunk overlap: 200 tokens (configurable: 100-300)

### Text Chunking Requirements

#### Token-Based Chunking (Default)
- **Tokenizer**: tiktoken (`cl100k_base`)
- **Chunk Size**: 1000 tokens
- **Overlap**: 200 tokens
- **Use Case**: General documents, mixed content

#### Semantic Chunking (Optional)
- **Method**: NLTK sentence tokenization
- **Boundary**: Sentence boundaries respected
- **Chunk Size Target**: 1000 tokens (flexible to complete sentences)
- **Overlap**: Sentence-level overlap
- **Use Case**: Narrative documents, instructional content
- **Limitation**: Requires NLTK punkt tokenizer

### Vector Search Requirements

**Search Method**: Semantic similarity (cosine distance)

**Search Parameters**:
- **Max Results**: 8 (configurable: 3-20)
- **Distance Metric**: Cosine distance (lower = more similar)
- **Reranking**: Optional (disabled for consistency)
- **Reranker Model**: `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Result Formatting**:
```python
{
    "content": "Text chunk content",
    "metadata": {
        "filename": "source_document.docx",
        "chunk_index": 5
    },
    "distance": 0.234,  # Optional: similarity score
    "relevance_score": 0.87  # Optional: reranker score
}
```

### Data Compatibility Matrix

| Data Type | Code Support | RAG Status | Current Usage | Priority |
|-----------|--------------|------------|---------------|----------|
| Plain text narrative | ✅ Implemented | ✅ Active (27 files, 102 chunks) | Primary knowledge source | Baseline |
| Structured documents (DOCX with headings) | ✅ Implemented | ✅ Active (24 DOCX files) | GPS outcomes, capabilities, pain points | High |
| Tables (in DOCX) | ✅ Implemented | ✅ Active (extracted in DOCX files) | Maturity models, roadmaps | Medium |
| CSV data | ✅ Implemented | ❌ **NOT IN USE** (10 files not processed) | Project impact scores unavailable | **HIGH** |
| JSON hierarchical data | ❌ Not implemented | ❌ **NOT IN USE** (2 files not processed) | GPS outcomes master data unavailable | **MEDIUM-HIGH** |
| Images, charts | ❌ Not compatible | ❌ Not supported | OCR required (not planned) | Low |
| Scanned PDFs | ❌ Not compatible | ❌ Not supported | OCR required (not planned) | Low |
| Binary formats | ❌ Not compatible | ❌ Not supported | N/A | N/A |

---

## Data Processing Pipeline

### Current Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│ Stage 1: File Validation                                         │
├─────────────────────────────────────────────────────────────────┤
│ • Check file extension (.pdf, .docx, .txt, .csv)                │
│ • Validate file size (< 10MB default)                           │
│ • Verify file accessibility                                     │
│ • Detect file encoding (UTF-8, Latin-1)                         │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│ Stage 2: Text Extraction                                         │
├─────────────────────────────────────────────────────────────────┤
│ • PDF: PyPDF2 page-by-page extraction                           │
│ • DOCX: python-docx with structure preservation                 │
│ • TXT: Direct decoding                                          │
│ • CSV: Enhanced parsing with project detection                  │
│ • JSON: *NOT IMPLEMENTED* (future enhancement)                  │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│ Stage 3: Text Cleaning & Normalization                          │
├─────────────────────────────────────────────────────────────────┤
│ • Fix spacing issues (punctuation, line breaks)                 │
│ • Remove excessive whitespace                                   │
│ • Normalize line endings                                        │
│ • Preserve meaningful structure                                 │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│ Stage 4: Chunking                                                │
├─────────────────────────────────────────────────────────────────┤
│ • Method 1: Token-based chunking (default)                      │
│   - Chunk size: 1000 tokens                                     │
│   - Overlap: 200 tokens                                         │
│ • Method 2: Semantic chunking (optional)                        │
│   - Sentence boundary preservation                              │
│   - Target size: 1000 tokens                                    │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│ Stage 5: Embedding Generation                                    │
├─────────────────────────────────────────────────────────────────┤
│ • Model: all-mpnet-base-v2 (768 dimensions)                     │
│ • Batch processing for efficiency                               │
│ • Progress tracking available                                   │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│ Stage 6: Vector Storage                                          │
├─────────────────────────────────────────────────────────────────┤
│ • Database: ChromaDB (persistent or in-memory)                  │
│ • Collection: betty_knowledge                                   │
│ • Metadata: filename, chunk_index                               │
│ • Unique IDs: doc_{offset}_chunk_{index}                        │
│ • Duplicate detection: filename-based                           │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│ Stage 7: Retrieval & Generation                                 │
├─────────────────────────────────────────────────────────────────┤
│ • Query embedding generation                                    │
│ • Semantic similarity search (cosine distance)                  │
│ • Optional reranking with cross-encoder                         │
│ • Context assembly for LLM                                      │
│ • Response generation (Claude 3.5 Sonnet or GPT-4o)            │
└─────────────────────────────────────────────────────────────────┘
```

### Pipeline Processing Times

| Stage | Typical Time | Factors |
|-------|--------------|---------|
| File Validation | <1 second | File size, filesystem speed |
| Text Extraction | 1-30 seconds | File type, size, complexity |
| Text Cleaning | <1 second | Text length |
| Chunking | 1-5 seconds | Text length, method (token vs semantic) |
| Embedding Generation | 5-60 seconds | Number of chunks, batch size, model speed |
| Vector Storage | 1-10 seconds | Number of chunks, database type |
| Retrieval | <1 second | Collection size, number of results |
| Generation | 2-20 seconds | LLM provider, response length, context size |

### Memory & Resource Requirements

**Embedding Model**:
- RAM: ~500MB for all-mpnet-base-v2
- Disk: ~420MB model files
- GPU: Optional (CPU fallback available)

**Vector Database**:
- Persistent: ~50-100MB per 1000 chunks
- In-memory: ~100-200MB per 1000 chunks
- Recommended: 2GB+ RAM for production

**Processing**:
- Peak RAM: ~1-2GB during embedding generation
- Concurrent processing: Limited by available RAM
- Recommended: 4GB+ RAM for production

---

## Validation Rules & Quality Gates

### Pre-Ingestion Validation

#### File-Level Validation

**Rule V1.1: File Format Compliance**
- **Check**: File extension in [.pdf, .docx, .txt, .csv, .md, .json]
- **Action**: Reject unsupported formats
- **Error Message**: "Unsupported file type: {filename}. Supported types: PDF, DOCX, TXT, CSV, MD, JSON"

**Rule V1.2: File Size Limit**
- **Check**: File size ≤ 10MB (configurable)
- **Action**: Reject oversized files
- **Error Message**: "File {filename} is too large (max 10MB)"
- **Rationale**: Prevent memory overflow and processing timeouts

**Rule V1.3: File Accessibility**
- **Check**: File can be opened and read
- **Action**: Skip inaccessible files
- **Error Message**: "Cannot access file: {filename}"

**Rule V1.4: File Encoding**
- **Check**: File encoding is UTF-8 or Latin-1 compatible
- **Action**: Attempt fallback encoding
- **Error Message**: "Cannot decode file: {filename}"

#### Content-Level Validation

**Rule V2.1: Non-Empty Content**
- **Check**: Extracted text length > 0
- **Action**: Reject empty files
- **Error Message**: "No text extracted from {filename}"
- **Rationale**: Empty documents add no value to knowledge base

**Rule V2.2: Minimum Content Length**
- **Check**: Extracted text length ≥ 50 characters
- **Action**: Warn and allow (with user confirmation)
- **Warning**: "File {filename} has very little content ({length} chars)"
- **Rationale**: Very short documents may lack context

**Rule V2.3: Text Quality**
- **Check**: Text has reasonable word/character ratio (not just symbols)
- **Action**: Warn if ratio < 0.3
- **Warning**: "File {filename} may contain low-quality text"

**Rule V2.4: Language Detection**
- **Check**: Text is primarily English (Betty's current capability)
- **Action**: Warn if non-English detected (future enhancement)
- **Status**: *Not implemented* (future consideration)

### Post-Processing Validation

#### Chunking Validation

**Rule V3.1: Chunk Count**
- **Check**: Number of chunks > 0
- **Action**: Reject if no valid chunks created
- **Error Message**: "Failed to create chunks from {filename}"

**Rule V3.2: Chunk Size Range**
- **Check**: Chunk size between 100-2000 tokens
- **Action**: Warn if outside range (but allow)
- **Rationale**: Very small chunks lack context; very large chunks reduce precision

**Rule V3.3: Chunk Overlap Validation**
- **Check**: Overlap < chunk_size
- **Action**: Auto-adjust overlap if invalid
- **Warning**: "Overlap adjusted to {new_value}"

#### Embedding Validation

**Rule V4.1: Embedding Generation Success**
- **Check**: All chunks have valid embeddings
- **Action**: Reject entire document if embedding fails
- **Error Message**: "Failed to generate embeddings for {filename}"

**Rule V4.2: Embedding Dimension Match**
- **Check**: Embedding dimensions match model (768 for all-mpnet-base-v2)
- **Action**: Reject mismatched embeddings
- **Rationale**: Dimension mismatch causes vector search failures

### Duplicate Detection

**Rule V5.1: Filename Uniqueness**
- **Check**: Filename not already in collection
- **Action**: Skip duplicate files (don't re-add)
- **Info Message**: "File {filename} already in knowledge base"
- **Rationale**: Prevent duplicate content and maintain database efficiency

**Rule V5.2: Content Hash Uniqueness** *(Future Enhancement)*
- **Check**: Document content hash not in database
- **Action**: Skip duplicate content even with different filenames
- **Status**: *Not implemented*

### Knowledge Base Integrity

**Rule V6.1: Collection Exists**
- **Check**: Target collection exists or can be created
- **Action**: Auto-create if missing
- **Info Message**: "Creating new collection: {collection_name}"

**Rule V6.2: Database Accessibility**
- **Check**: ChromaDB client connection successful
- **Action**: Fail gracefully with error message
- **Error Message**: "Cannot connect to vector database"

**Rule V6.3: Database Size Limits**
- **Check**: Database size < maximum limit (if configured)
- **Action**: Warn if approaching limit
- **Status**: *Not implemented* (future consideration for large deployments)

### CSV-Specific Validation

**Rule V7.1: CSV Structure**
- **Check**: CSV has valid header row
- **Action**: Warn if header missing (use column indices)
- **Warning**: "CSV {filename} has no header row"

**Rule V7.2: CSV Delimiter Detection**
- **Check**: Delimiter can be automatically detected or fallback to comma
- **Action**: Use fallback delimiter if detection fails
- **Info**: "Using comma delimiter for {filename}"

**Rule V7.3: CSV Row Consistency**
- **Check**: Most rows have same number of columns as header
- **Action**: Handle inconsistent rows with warning
- **Warning**: "Row {n} in {filename} has inconsistent columns"

### JSON-Specific Validation *(Future Implementation)*

**Rule V8.1: JSON Syntax Validation**
- **Check**: Valid JSON syntax
- **Action**: Reject malformed JSON
- **Error Message**: "Invalid JSON syntax in {filename}"
- **Status**: *To be implemented*

**Rule V8.2: JSON Structure Validation**
- **Check**: JSON has expected schema (for GPS outcomes)
- **Action**: Validate required fields
- **Status**: *To be implemented*

**Rule V8.3: JSON Relationship Integrity**
- **Check**: Parent-child relationships are valid
- **Action**: Warn of orphaned nodes
- **Status**: *To be implemented*

---

## Future Pipeline Recommendations

### Priority 1: CSV Data Integration (HIGH - CRITICAL GAP)

**Objective**: Add existing CSV project impact data to RAG vector database

**Current Situation**:
- 10 CSV files exist in docs/ folder with critical project impact data
- CSV extraction code is implemented and ready
- Files are NOT being processed during knowledge base initialization
- Betty cannot retrieve project scores, Z-scores, or impact percentages via RAG

**Implementation Requirements**:

1. **Update Knowledge Base Initialization**
   - Modify `betty_app.py` initialization to include .csv files
   - Add CSV files to processing queue in `initialize_knowledge_base()`

2. **Verify CSV Processing**
   - Test CSV extraction with project impact files
   - Validate row-based chunking preserves relationships
   - Ensure project references are searchable

3. **Force Reindex**
   - Set `FORCE_REINDEX=true` to rebuild knowledge base with CSV data
   - Verify all 10 CSV files are processed and indexed

**Expected Impact**:
- Enable Betty to answer project impact queries with actual data
- Support data-driven recommendations based on impact scores
- Provide quantitative analysis capabilities

**Implementation Timeline**: 1-2 days

**Estimated Chunks Added**: 50-100 (depending on CSV size and chunking)

---

### Priority 2: JSON Data Processing (MEDIUM-HIGH)

**Objective**: Enable Betty to understand and retrieve structured GPS outcomes from JSON

**Current Situation**:
- GPS outcomes available in DOCX files (partial coverage)
- Full 288-outcome hierarchy with relationships only in JSON
- JSON extraction not implemented

**Implementation Requirements**:

1. **JSON Parser Module**
   ```python
   def process_json_for_rag(json_file: io.BytesIO, schema_type: str) -> List[str]:
       """
       Parse JSON and convert to searchable text chunks.

       Args:
           json_file: BytesIO containing JSON data
           schema_type: Type of JSON schema ('gps_outcomes', 'hierarchical', 'flat')

       Returns:
           List of text chunks with preserved relationships
       """
   ```

2. **GPS Outcomes Specific Processing**
   - Flatten hierarchical structure while preserving relationships
   - Create searchable text entries:
     ```
     Outcome ID: ACQ-001
     Cluster: Acquire Customer
     Highest Order Outcome: The most desired companies eagerly become our customers
     Tier Level: 1
     Outcome Text: Our brand is immediately recognized and revered
     Parent: None
     Children: ACQ-002, ACQ-003

     [Full relationship context for semantic search]
     ```
   - Generate multiple search variations:
     - By outcome ID
     - By cluster
     - By outcome text
     - By highest order outcome
     - By tier level

3. **Metadata Preservation**
   ```python
   metadata = {
       "filename": "GPS_Outcomes_Master.json",
       "chunk_index": 0,
       "outcome_id": "ACQ-001",
       "cluster": "Acquire Customer",
       "tier_level": 1,
       "parent_id": null,
       "children_ids": ["ACQ-002", "ACQ-003"],
       "data_type": "gps_outcome"
   }
   ```

4. **Validation Rules**
   - Required fields: `outcome_id`, `cluster`, `outcome_text`, `tier_level`
   - Relationship integrity checks
   - Duplicate outcome ID detection

**Expected Impact**:
- Enable Betty to answer questions about GPS outcomes hierarchy
- Support navigation through outcome relationships
- Provide context-aware outcome recommendations

**Implementation Timeline**: 2-3 weeks

### Priority 3: Enhanced CSV Processing (MEDIUM - AFTER INTEGRATION)

**Objective**: Improve retrieval accuracy for project impact data

**Implementation Requirements**:

1. **Table-Aware Chunking**
   - Preserve full rows in chunks
   - Include header context in every chunk
   - Maintain column relationships

2. **Cross-Reference Generation**
   - Link projects to impact scores
   - Create searchable project summaries:
     ```
     Project: Digital Twin Implementation
     Current Capability Impact: 65.6%
     Current Pain Point Impact: 37.0%
     Impact Index: 102.6%
     Z-Score: -0.07
     Domain: BOM-PIM
     ```

3. **Multi-File Aggregation**
   - Combine current and future project data
   - Create comparative views
   - Enable cross-domain queries

**Expected Impact**:
- More accurate project impact queries
- Better support for comparative analysis
- Enhanced data-driven recommendations

**Implementation Timeline**: 1-2 weeks

### Priority 4: Content Quality Monitoring (MEDIUM)

**Objective**: Track and improve knowledge base quality over time

**Implementation Requirements**:

1. **Usage Analytics**
   - Track which documents are most retrieved
   - Measure retrieval success rates
   - Identify knowledge gaps

2. **Quality Metrics Dashboard**
   - Document coverage by domain
   - Average chunk relevance scores
   - User feedback correlation

3. **Automated Quality Reports**
   - Weekly knowledge base health reports
   - Recommendations for content updates
   - Identification of outdated content

**Expected Impact**:
- Data-driven knowledge base improvements
- Identification of content gaps
- Better understanding of Betty's knowledge utilization

**Implementation Timeline**: 2-3 weeks

### Priority 5: Advanced Semantic Search (LOW-MEDIUM)

**Objective**: Improve retrieval precision for complex queries

**Implementation Requirements**:

1. **Query Classification**
   - Detect query intent (factual, procedural, strategic)
   - Route to appropriate search strategy

2. **Multi-Vector Search**
   - Generate multiple query variations
   - Combine results with weighted scoring

3. **Context-Aware Reranking**
   - Enable reranking for complex queries
   - Use conversation context for relevance scoring

**Expected Impact**:
- Higher quality responses for complex queries
- Better handling of multi-part questions
- Improved context understanding

**Implementation Timeline**: 3-4 weeks

### Priority 6: Incremental Knowledge Updates (LOW)

**Objective**: Support continuous knowledge base updates without full reprocessing

**Implementation Requirements**:

1. **Change Detection**
   - File modification timestamps
   - Content hash comparisons
   - Selective reprocessing

2. **Version Control**
   - Track document versions
   - Maintain change history
   - Enable rollback capability

3. **Hot Reload**
   - Add new documents without restart
   - Update existing documents in place
   - Minimal disruption to live system

**Expected Impact**:
- Faster knowledge base updates
- Reduced processing overhead
- Better version management

**Implementation Timeline**: 2-3 weeks

---

## Data Governance & Best Practices

### Data Quality Standards

1. **Document Naming Convention**
   - Use descriptive filenames
   - Include domain identifier: `[DOMAIN]_[DESCRIPTION]_[VERSION].ext`
   - Example: `BOM-PIM_Current_Project_Impact_v2.0.csv`

2. **Version Control**
   - Maintain version numbers in filenames
   - Keep backup copies of critical documents
   - Track change history in metadata

3. **Documentation Requirements**
   - Every data source should have a README
   - Document data structure and relationships
   - Maintain glossary of domain terms

### Data Maintenance Schedule

| Activity | Frequency | Owner | Priority |
|----------|-----------|-------|----------|
| Review knowledge base contents | Monthly | Knowledge Manager | High |
| Update outdated documents | Quarterly | Domain Experts | High |
| Validate data integrity | Weekly | System Admin | Critical |
| Optimize chunking parameters | Quarterly | Data Scientist | Medium |
| Review retrieval quality | Monthly | Product Manager | High |
| Clean up duplicate content | Quarterly | Knowledge Manager | Medium |

### Security & Privacy Considerations

1. **Sensitive Data Handling**
   - Identify and flag sensitive documents
   - Implement access controls (if multi-user)
   - Ensure compliance with data regulations

2. **PII Detection** *(Future Enhancement)*
   - Scan for personally identifiable information
   - Redact or flag sensitive content
   - Maintain audit trail

3. **Data Retention**
   - Define retention policies
   - Archive outdated but valuable content
   - Secure deletion of deprecated data

---

## Appendix A: Current Data Inventory

### Actual ChromaDB Vector Database Contents

**Current State**: 102 chunks from 27 files (24 DOCX + 3 PDF)

**Files in RAG (from ChromaDB analysis)**:

| File | Type | Chunks | Category | Status |
|------|------|--------|----------|--------|
| Molex Manufacturing BA Reference Architecture.docx | DOCX | 20 | Reference Arch | ✅ Active |
| BOM PIM CURRENT PROJECT IMPACT TO PAIN POINTS with Explanations - Final 072225.docx | DOCX | 15 | BOM-PIM | ✅ Active |
| Impact of Future BOM PIM Projects on Pain Points 072825.docx | DOCX | 15 | BOM-PIM | ✅ Active |
| Molex - Becoming and Outcomes Based Organization.docx | DOCX | 6 | Strategic | ✅ Active |
| Change_Control_Roadmap_MileMarkers_ClosedLoopMerged.docx | DOCX | 6 | Change Mgmt | ✅ Active |
| Potential Future Change Control Management Projects (O82225).docx | DOCX | 4 | Change Mgmt | ✅ Active |
| THE GPS_OBT Story.docx | DOCX | 4 | OBT Foundation | ✅ Active |
| The Future of Design at Molex_ Sarah_s Complete Journey - BOM and PIM (Revised August 7, 2025) (1).docx | DOCX | 4 | Design Mgmt | ✅ Active |
| DESCRIPTION OF FUTURE BOM PIM PROJECT (082825).docx | DOCX | 3 | BOM-PIM | ✅ Active |
| The Change Managment Story v2.0 (2).docx | DOCX | 3 | Change Mgmt | ✅ Active |
| BOM and Part Information Management Pain Points - Commercial Parts.pdf | PDF | 2 | BOM-PIM | ✅ Active |
| DESCRIPTION OF CURRENT BOM PIM PROJECTS (082825).docx | DOCX | 2 | BOM-PIM | ✅ Active |
| DESIGN MGMT and COLLABORATION CAPABILITIES DEFINITION and MATURITY (090125).docx | DOCX | 2 | Design Mgmt | ✅ Active |
| GPS-OBT Talking Points.docx | DOCX | 2 | OBT Foundation | ✅ Active |
| Venture Summary - PCN Revamp (1).pdf | PDF | 2 | Projects | ✅ Active |
| BOM and PIM GPS Outcomes (082625).docx | DOCX | 1 | GPS Outcomes | ✅ Active |
| BOM PIM Capabilities Definitions and Maturity(1).docx | DOCX | 1 | BOM-PIM | ✅ Active |
| BOM PIM Capabilities Definitions and Maturity.docx | DOCX | 1 | BOM-PIM | ✅ Active |
| CHANGE CONTROL MANAGEMENT CAPABILITIES AND MATURITY LEVELS(1).docx | DOCX | 1 | Change Mgmt | ✅ Active |
| CHANGE CONTROL MANAGEMENT CAPABILITIES AND MATURITY LEVELS.docx | DOCX | 1 | Change Mgmt | ✅ Active |
| Change Control Management Roadmap Mile Marker Definitions.docx | DOCX | 1 | Change Mgmt | ✅ Active |
| Change Management Pain Point - August 15, 2025 (1).pdf | PDF | 1 | Change Mgmt | ✅ Active |
| Change Management Pain Point - August 15, 2025.docx | DOCX | 1 | Change Mgmt | ✅ Active |
| DESIGN MGMT & COLLABORATION OUTCOMES (090125).docx | DOCX | 1 | Design Mgmt | ✅ Active |
| OBT and GPS Construction Rules.docx | DOCX | 1 | OBT Foundation | ✅ Active |
| OBT GPS Definitions.docx | DOCX | 1 | OBT Foundation | ✅ Active |
| Product Change Control Management GPS Outcomes.docx | DOCX | 1 | GPS Outcomes | ✅ Active |

**Total in RAG**: 27 files, 102 chunks

### Files NOT in RAG (Critical Gap)

#### Project Impact CSV Data (10 CSV files - NOT PROCESSED)

| File | Category | Domain | Priority | RAG Status |
|------|----------|--------|----------|------------|
| BOM-PIM_total-project-impact.csv | Current Impact | BOM-PIM | High | ❌ NOT IN RAG |
| BOM-PIM_current_project_impact_to_capabilities.csv | Current Impact | BOM-PIM | High | ❌ NOT IN RAG |
| BOM-PIM_current-project-impact-to-pain-points.csv | Current Impact | BOM-PIM | High | ❌ NOT IN RAG |
| BOM-PIM_future_project_impact_to_capabilities.csv | Future Impact | BOM-PIM | Medium | ❌ NOT IN RAG |
| BOM-PIM_future_project_impact_to_pain_points.csv | Future Impact | BOM-PIM | Medium | ❌ NOT IN RAG |
| Change Management_total-project-impact.csv | Current Impact | Change Mgmt | High | ❌ NOT IN RAG |
| Change Management_current-project-impact-to-pain-points.csv | Current Impact | Change Mgmt | High | ❌ NOT IN RAG |
| Change Management_current-project-impact-to-capabilities.csv | Current Impact | Change Mgmt | High | ❌ NOT IN RAG |
| Change Management_future-project-impact-to-capabilities.csv | Future Impact | Change Mgmt | Medium | ❌ NOT IN RAG |
| Change Management_future-project-impact-to-pain-points.csv | Future Impact | Change Mgmt | Medium | ❌ NOT IN RAG |

**Impact**: Betty cannot retrieve project impact scores, Z-scores, or quantitative metrics via RAG search

#### GPS Outcomes Master Data (2 JSON files - NOT PROCESSED)

| File | Records | Priority | RAG Status |
|------|---------|----------|------------|
| GPS_Outcomes_Master.json | 288 outcomes | Critical | ❌ NOT IN RAG |
| GPS_Outcomes_Master_backup.json | 288 outcomes | Critical | ❌ NOT IN RAG |

**Impact**: Full GPS outcomes hierarchy with relationships not searchable via RAG. Betty relies on DOCX files for GPS outcomes (partial data) and system prompt knowledge.

---

### Summary Statistics

**Total Files in Repository**: 49 files
- ✅ **In RAG**: 27 files (24 DOCX + 3 PDF) = 102 chunks
- ❌ **NOT in RAG**: 22 files (10 CSV + 2 JSON + 10 DOCX not yet processed)

**Critical Gaps**:
1. **CSV Project Impact Data**: 10 files with quantitative metrics NOT accessible
2. **JSON GPS Master Data**: 2 files with full outcome hierarchy NOT accessible

**RAG Coverage**: 55% of files (27/49)

---

### Domain-Specific Knowledge (Files by Domain)

**BOM & PIM**:
- ✅ In RAG: 7 DOCX files
- ❌ NOT in RAG: 5 CSV files (project impact data)

**Change Management**:
- ✅ In RAG: 8 DOCX files, 2 PDF files
- ❌ NOT in RAG: 5 CSV files (project impact data)

**Design Management**:
- ✅ In RAG: 3 DOCX files

**GPS Outcomes**:
- ✅ In RAG: 2 DOCX files (partial outcomes)
- ❌ NOT in RAG: 2 JSON files (complete 288-outcome hierarchy)

**Strategic/OBT Foundation**:
- ✅ In RAG: 6 DOCX files

---

## Appendix B: Technical Configuration Reference

### Environment Variables

```bash
# API Configuration
AI_PROVIDER=claude  # or "openai"
ANTHROPIC_API_KEY=your_anthropic_key
OPENAI_API_KEY=your_openai_key

# Database Configuration
CHROMA_DB_PATH=./data/betty_chroma_db

# Processing Configuration
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
MAX_SEARCH_RESULTS=8

# Embedding Configuration
EMBEDDING_MODEL=sentence-transformers/all-mpnet-base-v2
TOKENIZER_MODEL=cl100k_base

# File Processing
MAX_FILE_SIZE_MB=10

# RAG Enhancement
USE_RERANKING=False
USE_SEMANTIC_CHUNKING=False
RERANKER_MODEL=cross-encoder/ms-marco-MiniLM-L-6-v2

# Deployment
FORCE_REINDEX=false  # Set to "true" to rebuild knowledge base
```

### ChromaDB Collections

**Primary Collection**: `betty_knowledge`
- **Purpose**: Main knowledge base for Betty
- **Documents**: All processed docs, DOCX, TXT, CSV files
- **Estimated Size**: 2000-5000 chunks (varies by content)

**Metadata Schema**:
```python
{
    "filename": str,         # Source filename
    "chunk_index": int,      # Chunk number within document
    # Future: Add data_type, domain, version, date
}
```

**Unique ID Pattern**: `doc_{doc_offset}_chunk_{chunk_index}`

### Model Specifications

**Embedding Model** (all-mpnet-base-v2):
- Dimensions: 768
- Max sequence length: 384 tokens
- Performance: ~1000 docs/sec on CPU
- Memory: ~500MB

**LLM Models**:
- Claude 3.5 Sonnet (primary): Context window 200K tokens
- GPT-4o (secondary): Context window 128K tokens

---

## Appendix C: Glossary

**RAG (Retrieval-Augmented Generation)**: AI technique combining information retrieval with text generation

**Embedding**: Numerical vector representation of text for semantic similarity

**Chunking**: Splitting documents into smaller, manageable pieces for processing

**Token**: Basic unit of text for language models (roughly 0.75 words)

**Vector Database**: Database optimized for storing and searching high-dimensional vectors

**Semantic Search**: Search based on meaning rather than keyword matching

**OBT (Outcome-Based Thinking)**: Molex methodology for defining and measuring strategic outcomes

**GPS (Global Positioning System)**: Molex strategic framework with tiered outcomes (Destination, Highway, Main Street, County Road)

**BOM (Bill of Materials)**: Comprehensive list of components and materials

**PIM (Product Information Management)**: System for managing product data

**ECO (Engineering Change Order)**: Formal process for product changes

---

## Appendix D: Change Log

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | January 2025 | BoldARC | Initial taxonomy creation |

---

**Document Status**: Living Document
**Next Review**: March 2025
**Owner**: BoldARC - Chief AI Officer
**Contact**: [Add contact information]

---

*End of Betty Data Taxonomy & Pipeline Specification v1.0*
