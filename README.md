# Betty AI Assistant 💁‍♀️

**Strategic Transformation Assistant powered by Outcome-Based Thinking (OBT)**

Betty is an AI-powered strategic transformation assistant designed to support organizations in implementing Outcome-Based Thinking, What/How Mapping, and cross-functional alignment for maximum business impact.

## 🚀 Latest Updates - Betty v4.3

**MODE System Implementation** - Concise, tool-like responses for maximum efficiency

- **38.8% Performance Improvement**: Overall score increased from 0.429 to 0.595
- **52% Faster Response Times**: Average response time reduced from 8.1s to 3.9s
- **89-98% Verbosity Reduction**: MODE 1 (outcome rewriting) and MODE 2 (classification) deliver ultra-concise responses
- **Upgraded to Claude Sonnet 4.5**: Latest model (claude-sonnet-4-20250514)
- **Production-Ready**: Validated with 50-question evaluation framework (0 errors, 100% success rate)

### MODE System

Betty v4.3 automatically detects question types and delivers appropriate response formats:

- **MODE 1 (CONCISE ANSWER)**: Outcome rewriting in ≤15 words total
- **MODE 2 (CLASSIFICATION)**: What/How classification in ≤5 words
- **MODE 3 (STANDARD)**: Comprehensive responses with context and evidence

See `evaluation/EVALUATION_COMPARISON_v4.2_vs_v4.3.md` for detailed performance analysis.

## 🎯 Features

### Strategic Transformation Support
- **Outcome-Based Thinking (OBT) Coaching**: Built-in instructional coaching for OBT methodology
- **MODE System**: Ultra-concise responses for outcome rewriting and classification
- **GPS Framework Navigation**: 288 strategic outcomes across 13 clusters
- **Multi-Domain Expertise**: 8 specialized knowledge domains with 53+ data files

### Technical Capabilities
- **RAG-Powered Intelligence**: Retrieval-Augmented Generation with ChromaDB vector storage (95% data completeness)
- **Advanced Document Processing**: PDF, DOCX, XLSX, CSV support with SharePoint integration
- **Knowledge Base Management**: Persistent storage with automatic updates across 8 domains
- **Evaluation Framework**: Automated testing with v4.3-optimized rubrics
- **Feedback Analytics**: Admin dashboard with user feedback analytics and improvement insights

### Knowledge Domains (8 Total)

1. **Change Control Management** - Change governance, ECO workflows, approval processes
2. **BOM & PIM Management** - Bill of Materials, Part Information Management, Master data governance
3. **Requirements Management** - Requirement capture, validation, traceability
4. **Design Management & Collaboration** - Design workflows, collaboration tools, handoff processes
5. **PD Framework Transformation** - Business process methodology, framework adoption
6. **Data & AI** - Data governance, AI strategy, predictive analytics
7. **Global PD** - Comprehensive Product Development oversight and strategic integration
8. **OBT Methodology** - Foundational Outcome-Based Thinking principles and GPS framework

## 🏗️ Architecture

```
Betty/
├── betty_app.py                  # Main application (v4.3 with MODE system)
├── system_prompt_v4.3.txt        # MODE system implementation (450 lines)
├── config/                       # Configuration management
│   ├── settings.py               # Claude Sonnet 4.5 configuration
│   └── __init__.py
├── utils/                        # Core utilities
│   ├── document_processor.py     # Multi-format text extraction
│   ├── vector_store.py           # ChromaDB interface
│   ├── feedback_manager.py       # User feedback analytics
│   └── __init__.py
├── evaluation/                   # Evaluation framework (NEW)
│   ├── run_evaluation.py         # v4.3-optimized rubric framework
│   ├── betty_testset_50q.csv     # 50-question test set
│   ├── results/                  # Evaluation results
│   ├── EVALUATION_COMPARISON_v4.2_vs_v4.3.md
│   ├── SYSTEM_PROMPT_IMPROVEMENTS_v4.3.md
│   └── EVALUATION_ANALYSIS_v4.2.md
├── pages/                        # Multi-page app components
│   └── admin_dashboard.py        # Analytics dashboard
├── chroma_db/                    # Vector database storage
│   └── chroma.sqlite3            # Persistent knowledge base
├── knowledge_files/              # 53+ source documents (8 domains)
│   ├── XLSX files                # Maturity matrices, project impacts
│   ├── DOCX files                # Stories, strategies, definitions
│   └── PDF files                 # Reference documentation
├── requirements.txt              # Python dependencies (updated for v4.3)
└── README.md                     # This file
```

## 🛠️ Technology Stack

- **Frontend**: Streamlit with multi-page support
- **AI Model**: Claude Sonnet 4.5 (claude-sonnet-4-20250514) - Production
- **Vector Database**: ChromaDB with persistent storage (95% completeness)
- **Embeddings**: SentenceTransformer (all-mpnet-base-v2) for 768-dimensional vectors
- **Document Processing**: PyPDF2, python-docx, openpyxl, pandas (XLSX support)
- **Evaluation**: scikit-learn, numpy (v4.3 testing framework)
- **Analytics**: SQLite with feedback tracking
- **Deployment**: Streamlit Cloud / AWS compatible

## 📋 Prerequisites

- Python 3.8+
- Anthropic API key (for Claude Sonnet 4.5)
- Git (for cloning)
- 2GB+ disk space (for vector database and knowledge files)

## 🚀 Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/tonybegum67/betty_for_molex.git
cd betty_for_molex
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Environment Variables
```bash
# Required
export ANTHROPIC_API_KEY="your_anthropic_api_key_here"

# Optional configurations
export CHROMA_DB_PATH="./chroma_db"
export CHUNK_SIZE="800"
export MAX_SEARCH_RESULTS="8"
```

### 4. Run Betty
```bash
streamlit run betty_app.py
```

Betty will be available at `http://localhost:8501`

**First Launch**: Knowledge base initialization takes ~2-3 minutes (one-time setup)

## 🎯 Betty's Core Competencies

### Strategic Transformation Support
- Strategic ideas and concept development
- Outcome statements with What/How classification (MODE system)
- GPS tier mapping (Destination → Highway → Main Street → County Road)
- Business capabilities and value stream alignment
- KPI goals and measurements
- Stakeholder roles and accountability mapping (RACI)
- Portfolio analysis and prioritization

### Instructional Coaching for OBT
- **Foundation Building**: Explains Outcome-Based Thinking principles
- **Practical Examples**: Provides outcome statement examples (10 words or less)
- **Classification Guidance**: Distinguishes between What outcomes vs How activities
- **Reframing Support**: Transforms vague goals into measurable outcomes
- **System Education**: Explains GPS tier system and capability alignment

### MODE System Responses

**MODE 1 Example - Outcome Rewriting**
```
User: "Rewrite 'implement ERP system' as an outcome (≤10 words)"
Betty: "Business operations are integrated across all functions"
(7 words, concise, metric-free)
```

**MODE 2 Example - Classification**
```
User: "Classify 'Decision speed improves measurably' — What or How?"
Betty: "What"
(1 word, perfect accuracy)
```

**MODE 3 Example - Comprehensive Analysis**
```
User: "Prioritize: Digital Twin, Advanced Analytics, Predictive Maintenance"
Betty: [Detailed analysis with impact scores, maturity levels, rationale,
       source citations, and confidence scores]
```

## 💬 Example Interactions

**Input**: "Create a metric-free outcome for customer onboarding"

**Betty's Response (MODE 1)**:
```
Customers seamlessly integrate into our product ecosystem immediately.
```
(8 words - concise, actionable, metric-free)

---

**Input**: "Is 'Deploy analytics dashboards' an acceptable outcome?"

**Betty's Response (MODE 2)**:
```
No.

**Reframed outcome:** Analytics insights drive operational decisions consistently.
```
(Brief classification + reframe)

---

**Input**: "State Change Control Management maturity"

**Betty's Response (Maturity Assessment)**:
```
Change Control Management — Current: Level 2 (Managed), Target: Level 4 (Quantitatively Managed)

Source: Change ControL Capability Definitions and Maturities.xlsx

Key context: Current state shows basic change workflows exist but lack
standardization across global operations. Target enables data-driven change
decisions with quantitative process controls.
```

## 🔧 Configuration

### Environment Variables
```bash
# Core Configuration
ANTHROPIC_API_KEY=your_api_key          # Required for Claude Sonnet 4.5

# Database Configuration
CHROMA_DB_PATH=./chroma_db              # Vector database path

# Processing Configuration
CHUNK_SIZE=800                          # Text chunk size in tokens
CHUNK_OVERLAP=100                       # Token overlap between chunks
MAX_SEARCH_RESULTS=8                    # Number of RAG search results (v4.3: increased to 8)
MAX_FILE_SIZE_MB=10                     # Maximum upload file size

# Model Configuration
EMBEDDING_MODEL=all-mpnet-base-v2       # Embedding model (768 dimensions)
TOKENIZER_MODEL=cl100k_base             # Tokenizer for chunking
```

### Streamlit Secrets (for cloud deployment)
Create `.streamlit/secrets.toml`:
```toml
ANTHROPIC_API_KEY = "your_anthropic_api_key_here"
```

## 📚 Usage Guide

### Adding Knowledge to Betty

Betty comes pre-loaded with 53+ knowledge files across 8 domains (95% completeness). To add more:

1. **Place files in knowledge_files/**: Supported formats: PDF, DOCX, XLSX, CSV, TXT
2. **Restart application**: Knowledge base auto-updates on startup
3. **Verify**: Check sidebar for "Knowledge Base Status: ✅ Ready"

### Betty's Response Standards (v4.3)

- **MODE 1 (Outcome Rewriting)**: ≤15 words total, metric-free, no How verbs
- **MODE 2 (Classification)**: ≤5 words, direct answer (What/How/Yes/No)
- **MODE 3 (Comprehensive)**: Full context with sources, confidence scores, structured analysis
- **RAG Integration**: Cites sources from knowledge base with file references
- **Confidence Scores**: HIGH (>90%), MODERATE (75-90%), LIMITED (<75%)

### Advanced Features

- **RAG Toggle**: Enable/disable knowledge base integration (default: enabled)
- **File Upload**: Temporary context for current session
- **Knowledge Refresh**: Automatic updates from knowledge_files/ directory
- **Admin Dashboard**: Access analytics and user feedback insights
- **Feedback System**: Thumbs up/down with detailed feedback collection
- **Evaluation Framework**: Run 50-question tests with `python evaluation/run_evaluation.py --full`

## 📊 Admin Dashboard

Access the admin dashboard to monitor Betty's performance:

### Features
- **Overview Metrics**: Total feedback, quality scores, satisfaction rates
- **Feedback Breakdown**: Positive vs negative feedback analysis
- **Trends Over Time**: Historical performance patterns
- **Quality Analysis**: OBT compliance and response quality metrics
- **Improvement Opportunities**: Areas for enhancement based on user feedback

### Access
Navigate to the Admin Dashboard page in the sidebar.

## 🧪 Evaluation Framework

Betty v4.3 includes a comprehensive evaluation framework:

```bash
# Run quick test (5 questions)
python evaluation/run_evaluation.py

# Run full evaluation (50 questions)
python evaluation/run_evaluation.py --full

# Run custom evaluation (N questions)
python evaluation/run_evaluation.py --questions 10
```

### Test Categories (50 Questions Total)
- Outcome Rewriting (18) - Convert activities to outcomes
- Classification (9) - What vs How determination
- Acceptance Criteria (5) - Structured criteria with owners/measures
- Portfolio Analysis (7) - Prioritization and RACI assignments
- Maturity Assessment (5) - Current and target maturity levels
- Domain Expertise (6) - Factual knowledge base queries

### Evaluation Results (v4.3)
- Overall Score: 0.595 (59.5%)
- Semantic Similarity: 0.614
- Rubric Precision: 0.940/3
- Rubric Adherence: 2.940/3
- Rubric Explanation: 2.440/3
- Average Response Time: 3.86 seconds

See `evaluation/EVALUATION_COMPARISON_v4.2_vs_v4.3.md` for detailed analysis.

## 🚀 Deployment

### Local Development
```bash
streamlit run betty_app.py --server.port 8501
```

### Streamlit Cloud
1. Connect GitHub repository to Streamlit Cloud
2. Add `ANTHROPIC_API_KEY` to Streamlit secrets
3. Set main file to `betty_app.py`
4. Deploy automatically on code changes

**Note**: Knowledge base rebuilds automatically on first deployment (~2-3 minutes)

### AWS Deployment
1. Push to GitHub main branch (already configured)
2. AWS pulls latest code automatically
3. Installs dependencies from `requirements.txt`
4. Loads `system_prompt_v4.3.txt` on startup
5. Rebuilds vector database from knowledge_files/

**Production Ready**: v4.3 deployment-ready with fail-fast validation

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "betty_app.py", "--server.address", "0.0.0.0"]
```

## 🔍 API Reference

### Document Processor
```python
from utils.document_processor import DocumentProcessor

processor = DocumentProcessor()

# Extract text from various formats
text = processor.extract_text_from_pdf(pdf_bytes)
text = processor.extract_text_from_docx(docx_bytes)
data = processor.extract_text_from_xlsx(xlsx_bytes)  # NEW in v4.3

# Process and chunk text
cleaned_text = processor.clean_text(raw_text)
chunks = processor.chunk_text(text, chunk_size=800, overlap=100)
```

### Vector Store
```python
from utils.vector_store import VectorStore

vector_store = VectorStore()

# Add documents to knowledge base
success = vector_store.add_documents(
    collection_name="betty_knowledge",
    documents=["Document text..."],
    metadatas=[{"source": "file.pdf"}]
)

# Search knowledge base (v4.3: n_results=8)
results = vector_store.search_collection(
    collection_name="betty_knowledge",
    query="outcome-based thinking",
    n_results=8
)
```

### Feedback Manager
```python
from utils.feedback_manager import FeedbackManager

feedback_manager = FeedbackManager()

# Record user feedback
feedback_manager.record_feedback(
    session_id="session_123",
    user_message="User question",
    betty_response="Betty's response",
    feedback_type="thumbs_up",
    feedback_text="Very helpful!"
)

# Get analytics
summary = feedback_manager.get_feedback_summary(days=30)
```

## 🐛 Troubleshooting

### Common Issues

**"system_prompt_v4.3.txt not found"**
- Ensure `system_prompt_v4.3.txt` exists in project root
- Check file permissions
- v4.3 uses fail-fast validation (no fallback to v4.2)

**"Please set your API key"**
- Verify `ANTHROPIC_API_KEY` in environment variables or Streamlit secrets
- Check API key has sufficient credits/quota
- v4.3 requires Claude Sonnet 4.5 access

**"Could not connect to ChromaDB"**
- Check database path permissions
- Clear corrupted database: `rm -rf chroma_db/`
- Restart application to rebuild knowledge base

**"No text could be extracted"**
- Verify file format is supported (PDF, DOCX, XLSX, CSV, TXT)
- Check file isn't password-protected or corrupted
- Ensure file size is under 10MB limit

**"Slow response times"**
- Check RAG is enabled (8 context chunks = ~2s overhead)
- Disable RAG for simple questions
- v4.3 averages 3.9s with RAG enabled (52% faster than v4.2)

**"Evaluation tests failing"**
- Install evaluation dependencies: `pip install scikit-learn numpy`
- Ensure `system_prompt_v4.3.txt` is loaded
- Check `evaluation/betty_testset_50q.csv` exists

## 📄 Documentation

- **[EVALUATION_COMPARISON_v4.2_vs_v4.3.md](evaluation/EVALUATION_COMPARISON_v4.2_vs_v4.3.md)**: Comprehensive v4.3 performance analysis
- **[SYSTEM_PROMPT_IMPROVEMENTS_v4.3.md](evaluation/SYSTEM_PROMPT_IMPROVEMENTS_v4.3.md)**: MODE system design rationale
- **[EVALUATION_ANALYSIS_v4.2.md](evaluation/EVALUATION_ANALYSIS_v4.2.md)**: Baseline v4.2 assessment
- **Knowledge Base**: 53+ files across 8 domains in knowledge_files/
- **API Reference**: Complete method documentation above

## 📊 Performance Metrics (v4.3)

### Evaluation Results (50-question validation)
- **Overall Score**: 0.595 (59.5%) - up 38.8% from v4.2
- **Classification Accuracy**: 0.667 (66.7%) - up 75.8% from v4.2
- **Outcome Rewriting**: 0.628 (62.8%) - up 65.5% from v4.2
- **Response Speed**: 3.86s average - 52% faster than v4.2
- **Success Rate**: 50/50 questions (100%), 0 errors

### MODE System Performance
- **MODE 1 Verbosity**: 89% reduction (69 words → 7.8 words avg)
- **MODE 2 Verbosity**: 98% reduction (145 words → 3.2 words avg)
- **Perfect Scores**: 4 classification questions (v4.2: 0)
- **Rubric Precision**: +571% improvement

### Knowledge Base Status
- **Data Completeness**: 95% (Production Ready)
- **Total Files**: 53+ documents
- **Domains**: 8 specialized knowledge areas
- **Vector Dimensions**: 768 (all-mpnet-base-v2)
- **RAG Context**: 8 chunks per query

## 📞 Support

- **GitHub Repository**: [tonybegum67/betty_for_molex](https://github.com/tonybegum67/betty_for_molex)
- **Issues**: Report bugs or request features via GitHub Issues
- **Documentation**: Comprehensive guides in evaluation/ directory
- **Development**: Follow contribution guidelines for code changes

## 👥 Credits

**Author**: Tony Begum, AI Architect
**Company**: BoldARC Advisors
**Project**: Betty for Molex - Strategic Transformation Platform

**Special Thanks**:
- Outcome-Based Thinking (OBT) methodology framework
- Molex stakeholders for domain expertise and validation
- Claude Sonnet 4.5 for MODE system capabilities

## 📜 License

Private repository - All rights reserved to BoldARC Advisors.

## 🏷️ Version History

**Betty v4.3 Production** (October 2025)
- MODE system implementation (concise responses)
- 38.8% performance improvement
- Claude Sonnet 4.5 upgrade
- 50-question evaluation framework
- 52% faster response times

**Betty v4.2 Production** (October 2025)
- SharePoint integration
- XLSX data support
- 8-domain knowledge expansion
- Enhanced RAG capabilities

**Betty v2.2 Beta** (January 2025)
- Initial OBT coaching system
- ChromaDB vector storage
- Multi-page Streamlit interface
- Admin dashboard analytics

---

**Built with ❤️ for strategic transformation and outcome-based thinking**
**Developed by BoldARC Advisors**

*Last updated: October 2025 (Betty v4.3)*
