# Fix for Streamlit Cloud SQLite3 compatibility - MUST be at the very top
import sys
if 'sqlite3' in sys.modules:
    del sys.modules['sqlite3']

try:
    import pysqlite3 as sqlite3
    sys.modules['sqlite3'] = sqlite3
except ImportError:
    import sqlite3

import streamlit as st
import openai
import anthropic
import os
import io
import re
from typing import Generator, List

# Mermaid diagram support
try:
    from streamlit_mermaid import st_mermaid
    MERMAID_AVAILABLE = True
except ImportError:
    MERMAID_AVAILABLE = False

# Import configuration and utilities
from config.settings import AppConfig
from utils.document_processor import document_processor
from utils.vector_store import betty_vector_store
from utils.feedback_manager import feedback_manager
from utils.clipboard_helper import create_inline_copy_button

# ChromaDB compatibility check
try:
    print(f"Using SQLite version: {sqlite3.sqlite_version}")
except Exception as e:
    print(f"SQLite setup warning: {e}")

# Initialize configuration
AppConfig.init_environment()


# Set page config
st.set_page_config(
    page_title=AppConfig.PAGE_TITLE,
    page_icon=AppConfig.PAGE_ICON,
    layout="wide"
)

# Enhanced knowledge base initialization with better persistence handling
def initialize_knowledge_base():
    """Initialize knowledge base with enhanced persistence and change detection."""
    if "knowledge_base_initialized" not in st.session_state:
        with st.spinner("🔄 Initializing Betty's knowledge base..."):
            try:
                collection_name = AppConfig.KNOWLEDGE_COLLECTION_NAME
                docs_path = "docs"

                # Check for forced reindex (for cloud deployment updates)
                force_reindex = os.getenv("FORCE_REINDEX", "").lower() in ["true", "1", "yes"]
                if force_reindex:
                    st.info("🔄 Force reindex requested - rebuilding knowledge base with latest enhancements...")
                    # Remove existing collection to force complete rebuild
                    collections = betty_vector_store.list_collections()
                    if collection_name in collections:
                        betty_vector_store.delete_collection(collection_name)
                        st.success("✅ Existing database cleared for complete rebuild")

                # Check if collection exists and get current state
                collections = betty_vector_store.list_collections()
                collection_exists = collection_name in collections
                current_doc_count = 0
                
                if collection_exists:
                    collection = betty_vector_store.get_or_create_collection(collection_name)
                    current_doc_count = collection.count()
                
                # Get current documents in docs folder and subdirectories
                doc_files = []
                if os.path.exists(docs_path):
                    # Walk through all subdirectories
                    for root, dirs, files in os.walk(docs_path):
                        for file in files:
                            if file.lower().endswith(('.pdf', '.docx', '.txt', '.md', '.csv', '.xlsx')):
                                doc_files.append(os.path.join(root, file))
                
                # Check if we need to update (new files or no existing collection)
                needs_update = not collection_exists or current_doc_count == 0

                # For local deployment, also check for file changes
                is_local = not (os.getenv("STREAMLIT_SHARING") or
                               os.getenv("STREAMLIT_CLOUD") or
                               os.getenv("STREAMLIT_RUNTIME_ENV") == "cloud")

                # PRE-POPULATED VECTOR DATABASE STRATEGY
                # Check if we have a pre-populated vector database
                if collection_exists and current_doc_count > 50:
                    # Use existing pre-populated vector database
                    needs_update = False
                    env_type = "☁️ Cloud" if not is_local else "💾 Local"
                    st.info(f"📚 Using pre-populated knowledge base ({current_doc_count} documents) - {env_type}")
                elif is_local and doc_files:
                    # Only rebuild locally if no substantial database exists
                    stored_files = getattr(st.session_state, 'knowledge_files_count', 0)
                    if len(doc_files) != stored_files or current_doc_count < 50:
                        needs_update = True
                        st.info(f"🔄 Building vector database from {len(doc_files)} documents...")
                else:
                    # Cloud deployment without pre-populated database - graceful fallback
                    needs_update = False
                    st.warning("⚠️ No pre-populated vector database found. Betty will use embedded knowledge.")
                
                if needs_update and doc_files:
                    st.info(f"📚 Loading {len(doc_files)} documents into knowledge base...")
                    success = betty_vector_store.add_documents_from_files(
                        collection_name, 
                        doc_files, 
                        show_progress=True
                    )
                    
                    if success:
                        updated_collection = betty_vector_store.get_or_create_collection(collection_name)
                        final_count = updated_collection.count()
                        st.session_state.knowledge_base_initialized = True
                        st.session_state.knowledge_files_count = len(doc_files)
                        st.success(f"✅ Knowledge base updated with {final_count} document chunks!")
                        
                        # Display environment info
                        env_type = "☁️ Cloud (In-Memory)" if not is_local else "💾 Local (Persistent)"
                        st.info(f"Environment: {env_type}")
                    else:
                        st.error("❌ Failed to update knowledge base")
                        
                elif collection_exists and current_doc_count > 0:
                    # Collection exists and has data
                    st.session_state.knowledge_base_initialized = True
                    st.session_state.knowledge_files_count = len(doc_files)
                    env_type = "☁️ Cloud (In-Memory)" if not is_local else "💾 Local (Persistent)"
                    st.success(f"✅ Knowledge base ready with {current_doc_count} chunks! ({env_type})")
                    
                else:
                    # No documents found
                    st.warning("⚠️ No documents found in docs folder")
                    st.session_state.knowledge_base_initialized = True
                    st.session_state.knowledge_files_count = 0
                    
            except Exception as e:
                st.error(f"❌ Error initializing knowledge base: {e}")
                st.session_state.knowledge_base_initialized = True
                
def force_knowledge_base_refresh():
    """Force a complete refresh of the knowledge base."""
    if "knowledge_base_initialized" in st.session_state:
        del st.session_state.knowledge_base_initialized
    if "knowledge_files_count" in st.session_state:
        del st.session_state.knowledge_files_count
    
    # Clear existing collection
    try:
        collection_name = AppConfig.KNOWLEDGE_COLLECTION_NAME
        collections = betty_vector_store.list_collections()
        if collection_name in collections:
            betty_vector_store.client.delete_collection(name=collection_name)
            st.info("🗑️ Cleared existing knowledge base for refresh")
    except Exception as e:
        st.warning(f"Note: Could not clear existing collection: {e}")
    
    # Re-initialize
    initialize_knowledge_base()

# Initialize session state early
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize session ID for feedback tracking
if "session_id" not in st.session_state:
    import uuid
    st.session_state.session_id = str(uuid.uuid4())

# Initialize feedback state
if "feedback_given" not in st.session_state:
    st.session_state.feedback_given = set()

# Initialize knowledge base for cloud deployment
initialize_knowledge_base()

# Enhanced Navigation Header
col1, col2, col3 = st.columns([3, 1, 1])

with col1:
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    ">
        <h1 style="
            color: white;
            margin: 0;
            font-size: 2.2rem;
            font-weight: 600;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
        ">
            {AppConfig.PAGE_ICON} {AppConfig.PAGE_TITLE}
        </h1>
        <p style="
            color: rgba(255, 255, 255, 0.9);
            margin: 0.5rem 0 0 0;
            font-size: 1rem;
            font-weight: 300;
        ">
            Strategic Transformation Assistant powered by AI
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="padding-top: 1rem;">
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🏠 Betty Chat", 
                 use_container_width=True, 
                 type="primary",
                 help="Main chat interface"):
        st.rerun()

with col3:
    st.markdown("""
    <div style="padding-top: 1rem;">
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("📊 Admin Dashboard", 
                 use_container_width=True, 
                 type="secondary",
                 help="Access analytics and admin features"):
        st.switch_page("pages/admin_dashboard.py")

# Betty's Introduction and Sample Prompts
if not st.session_state.messages:
    st.markdown("---")
    
    # Betty's Description
    st.markdown("""
    ### 👋 Welcome! I'm Betty
    
    I'm an AI assistant designed to facilitate strategic transformation through **Outcome-Based Thinking (OBT)** and **What/How Mapping**. My role is to help organizations like Molex activate, measure, and align strategic outcomes with business structures for maximum impact.
    
    I assist in developing strategic ideas, creating measurable outcome statements, mapping these to the GPS tier framework, aligning them with business capabilities, and defining relevant KPIs. Additionally, I provide instructional coaching to enhance understanding and application of OBT methodology, building organizational capability while delivering strategic value.
    """)
    
    # Sample Prompts
    st.markdown("### 🚀 Try these sample prompts:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Transform Strategy", use_container_width=True):
            sample_prompt = "Help me transform 'improve customer satisfaction' into a measurable outcome statement with KPIs and GPS tier mapping"
            st.session_state.messages.append({"role": "user", "content": sample_prompt})
            st.rerun()
        
        st.caption("Transform vague goals into measurable outcomes")
    
    with col2:
        if st.button("🎯 Outcome Analysis", use_container_width=True):
            sample_prompt = "Analyze this statement: 'implement agile methodologies across development teams' - is this a What or How? Help me reframe it."
            st.session_state.messages.append({"role": "user", "content": sample_prompt})
            st.rerun()
        
        st.caption("Learn What vs How classification")
    
    with col3:
        if st.button("🏗️ GPS Mapping", use_container_width=True):
            sample_prompt = "Map the outcome 'product defect rates reduced by 50%' to the appropriate GPS tier and identify supporting business capabilities"
            st.session_state.messages.append({"role": "user", "content": sample_prompt})
            st.rerun()
        
        st.caption("Align outcomes with organizational structure")
    
    st.markdown("---")
    st.markdown("💬 **Or ask me anything about strategic transformation, OBT methodology, or Molex operations!**")

# --- Configuration ---
# Get the API key based on provider
if AppConfig.AI_PROVIDER == "claude":
    AppConfig.ANTHROPIC_API_KEY = st.secrets.get("ANTHROPIC_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
    if not AppConfig.ANTHROPIC_API_KEY:
        st.error("Please set your Anthropic API key in Streamlit secrets (e.g., .streamlit/secrets.toml) or as an environment variable.")
        st.stop()
    client = anthropic.Anthropic(api_key=AppConfig.ANTHROPIC_API_KEY)
else:
    AppConfig.OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
    if not AppConfig.OPENAI_API_KEY:
        st.error("Please set your OpenAI API key in Streamlit secrets (e.g., .streamlit/secrets.toml) or as an environment variable.")
        st.stop()
    client = openai.OpenAI(api_key=AppConfig.OPENAI_API_KEY)

# Validate configuration
if not AppConfig.validate_config():
    st.error("Invalid configuration. Please check your settings.")
    st.stop()

# --- RAG and Vector DB Setup ---
# Use the configured vector store
vector_store = betty_vector_store

# Document processing functions now use the shared utilities
# These wrapper functions maintain compatibility with existing code
def extract_text_from_pdf(file: io.BytesIO) -> str:
    """Extracts text from an in-memory PDF file."""
    return document_processor.extract_text_from_pdf(file)

def extract_text_from_docx(file: io.BytesIO) -> str:
    """Extracts text from an in-memory DOCX file."""
    return document_processor.extract_text_from_docx(file)

def chunk_text(text: str, chunk_size: int = None, overlap: int = None) -> List[str]:
    """Splits text into overlapping chunks based on token count."""
    return document_processor.chunk_text(
        text, 
        chunk_size or AppConfig.CHUNK_SIZE, 
        overlap or AppConfig.CHUNK_OVERLAP
    )

def add_files_to_collection(collection_name: str, file_paths: List[str]):
    """Processes and adds a list of files from disk to a ChromaDB collection."""
    return vector_store.add_documents_from_files(collection_name, file_paths)

# --- Duplicate functions removed - using implementations above ---

def search_knowledge_base(query: str, collection_name: str, n_results: int = None):
    """Searches the knowledge base for relevant context with optional reranking."""
    n_results = n_results or AppConfig.MAX_SEARCH_RESULTS
    if AppConfig.USE_RERANKING:
        return vector_store.search_collection_with_reranking(collection_name, query, n_results)
    else:
        return vector_store.search_collection(collection_name, query, n_results)

def detect_and_render_mermaid(content: str) -> bool:
    """
    Detect Mermaid diagrams in content and render them.
    Returns True if Mermaid diagrams were found and rendered.
    """
    if not MERMAID_AVAILABLE:
        st.warning("⚠️ Mermaid rendering not available. Install streamlit-mermaid to enable diagram visualization.")
        return False
    
    # Pattern to match standard Mermaid diagram blocks
    mermaid_pattern = r'```mermaid\s*\n(.*?)\n```'
    
    diagrams_found = False
    remaining_parts = []
    last_end = 0
    
    # Find all mermaid code blocks
    matches = list(re.finditer(mermaid_pattern, content, re.DOTALL | re.IGNORECASE))
    
    if not matches:
        # No mermaid diagrams found
        return False
    
    for match in matches:
        # Add content before this diagram
        if match.start() > last_end:
            text_before = content[last_end:match.start()].strip()
            if text_before:
                remaining_parts.append(text_before)
        
        # Extract and render the diagram
        diagram_code = match.group(1).strip()
        
        if diagram_code:  # Only render if there's actual content
            try:
                # Render the diagram with streamlit-mermaid
                st_mermaid(diagram_code, height=400)
                diagrams_found = True
                
                # Add a small expander with the code for reference
                with st.expander("📊 View Mermaid Code", expanded=False):
                    st.code(diagram_code, language="mermaid")
                    
            except Exception as e:
                st.error(f"❌ Error rendering Mermaid diagram: {e}")
                # Show the code as fallback
                with st.expander("⚠️ Mermaid Code (Failed to Render)", expanded=True):
                    st.code(diagram_code, language="mermaid")
                    st.info("💡 Try copying this code to a Mermaid live editor: https://mermaid.live/")
                diagrams_found = True  # Still count as found even if rendering failed
        
        last_end = match.end()
    
    # Add any remaining content after the last diagram
    if last_end < len(content):
        text_after = content[last_end:].strip()
        if text_after:
            remaining_parts.append(text_after)
    
    # Display remaining content as markdown if any
    for part in remaining_parts:
        if part.strip():
            st.markdown(part)
    
    return diagrams_found


# --- Betty's Personality & Knowledge ---
# Betty for Molex v4.2 Production System - Enhanced SharePoint Integration
SYSTEM_PROMPT = """Betty for Molex v4.2 Production System - Enhanced SharePoint Integration

Strategic Transformation Assistant with Professional Standards

Developer: Tony Begum, AI Architect, BoldARC Advisors
Version: 4.2 Production (SharePoint Integration)
Last Updated: October 2025

Core Identity & Mission

You are Betty for Molex 4.2, an AI assistant for strategic transformation using Outcome-Based Thinking (OBT), What/How Mapping, and cross-functional alignment. You help organizations activate, measure, and align strategic outcomes to business structures for maximum impact while maintaining professional boundaries and user wellbeing.

Betty navigates strategic outcomes using a cluster-based GPS with 288 outcomes organized across 13 strategic clusters. Each cluster has variable depth (1-6 tiers) based on strategic complexity. The destination remains: "Customers always choose Molex first."

Data Context & Quality Standards

Current Portfolio State
- Total Knowledge Files: 53+ files (DOCX, PDF, XLSX, CSV across 8 domains)
- Data Completeness: 95% (Production Ready - Enhanced with SharePoint data)
- Confidence Framework:
  - HIGH (>90%): All domain analysis with XLSX maturity data
  - MODERATE (75-90%): Cross-domain integration analysis
  - LIMITED (<75%): Emerging data patterns

Critical Data Facts
- Impact Scoring: 0-3 integers only (2s and 3s count in totals)
- Maturity Scale: 1-5 (Initial, Managed, Defined, Quantitatively Managed, Optimized)
- CRITICAL: Never confuse maturity levels (1-5) with impact scores (0-3)

Core Competencies

1. Strategic Transformation Support
Provide deep reasoning across:
- Strategic ideas and concept development
- Outcome statements with What/How classification
- Business capabilities and value stream alignment
- KPI goals and measurements
- Information concepts and dependencies
- Stakeholder roles and accountability mapping
- Project portfolio analysis with impact scores

2. Multi-Domain Expertise (ENHANCED - 8 Domains)

**Domain 1: Change Control Management**
- Capabilities: Change governance, ECO workflows, approval processes
- Data Sources: Change ControL Capability Definitions and Maturities.xlsx, Project impact data, Pain point definitions
- KPIs: Change cycle time, approval efficiency, compliance rates
- Use For: Change process optimization, governance questions, ECO workflow analysis

**Domain 2: BOM & PIM Management**
- Capabilities: Bill of Materials, Part Information Management, Master data governance
- Data Sources: BOM PIM Capability Definitions and Maturities.xlsx, Project impacts, Pain points
- Use For: Product data management, engineering BOMs, manufacturing BOMs
- Story Reference: "The Future of Design at Molex: Sarah's Journey"

**Domain 3: Requirements Management (NEW)**
- Capabilities: Requirement capture, validation, traceability, stakeholder management
- Data Sources: Requirements Management Capability Definitions and Maturities.xlsx, Project impacts
- Pain Points: Requirements Management Pain Points (092325)
- KPIs: Potential KPIs for Requirements Management.docx
- Use For: Requirements engineering, validation processes, traceability matrices

**Domain 4: Design Management & Collaboration (EXPANDED)**
- Capabilities: Design workflows, collaboration tools, design-to-manufacturing handoff
- Data Sources: Design Management and Collaboration Capability Definitions and Maturities.xlsx
- Project Impacts: Design Mgmt and Collaboration Project Impacts (100625).xlsx
- Story Reference: "The Future of Design Management and Collaboration: A Molex Innovation Story"
- Use For: Design process optimization, collaboration tooling, workflow automation

**Domain 5: PD Framework Transformation (NEW)**
- Capabilities: Business process methodology, framework adoption, transformation roadmaps
- Data Sources: Business Process Methodology Features Description.docx
- Use For: Product development framework questions, methodology transformation

**Domain 6: Data & AI (NEW)**
- Capabilities: Data governance, AI strategy, predictive analytics, decision support
- Data Sources: Data and AI Capability Definitions and Maturities.xlsx, Project impacts
- Pain Points: DATA and AI Pain Points (092225).docx
- Story Reference: "The Future of Confident Decision-Making at Molex"
- Agentic Strategy: AI Agentic Strategy for Data & AI.docx
- Use For: Data strategy, AI implementation, analytics capabilities

**Domain 7: Global PD (NEW)**
- Comprehensive Product Development oversight and strategic integration
- Data Sources:
  * Mini GPS Outcomes Master (XLSX with hierarchical relationships)
  * GPD KPI Outcomes-Based Summary.xlsx
  * Value of Outcomes 080425.xlsx
  * Global PD Dependency Diagram Stage Definitions
  * PD Capability Definitions (101025).docx
  * Master Product Development Story (all capabilities integrated)
- AI Agentic Strategies: 5 domain-specific strategy documents
  * BOM & PIM Management Agentic Strategy
  * Change Control Management Agentic Strategy
  * Design Management & Collaboration Agentic Strategy
  * Requirements Management Agentic Strategy
  * Data & AI Agentic Strategy
- Use For: Enterprise PD strategy, cross-domain integration, KPI frameworks, AI automation roadmaps

**Domain 8: OBT Methodology (ENHANCED)**
- Foundational Outcome-Based Thinking principles and GPS framework
- Data Sources:
  * Five Things to Know About OBT.docx
  * Molex - Becoming and Outcomes Based Organization.docx
  * OBT and GPS Construction Rules.docx
  * OBT GPS Definitions.docx
  * THE GPS_OBT Story.docx
- Use For: OBT education, GPS construction, transformation methodology

3. Project-Capability Alignment
Key capability mappings remain consistent with v4.1

4. Instructional Coaching for OBT
Enhanced with expanded domain examples and cross-domain coaching scenarios

5. Data-Driven Analysis (ENHANCED)
Always:
- State confidence level based on data completeness (now >95% with XLSX data)
- Use exact values from XLSX capability matrices (1-5 maturity scale)
- Use exact percentages from project impact XLSX files (0-3 impact scores)
- Distinguish between maturity levels and impact scores
- Explain capability gaps as intentional sequencing

6. Maturity Assessment Analysis (MULTI-DOMAIN - ENHANCED)
When responding to maturity questions:
- Primary Sources: Domain-specific XLSX maturity matrices:
  * Change Control: Change ControL Capability Definitions and Maturities.xlsx
  * BOM/PIM: BOM PIM Capability Definitions and Maturities.xlsx
  * Requirements: Requirements Management Capability Definitions and Maturities.xlsx
  * Design: Design Management and Collaboration Capability Definitions and Maturities.xlsx
  * Data & AI: Data and AI Capability Definitions and Maturities.xlsx
- Maturity Scale: 1-5 (Initial, Managed, Defined, Quantitatively Managed, Optimized)
- Response Format: State Current Level (1-5) and Target Level (1-5) with domain context
- Cross-Domain Analysis: Now available across 5 domains with structured XLSX data
- NEVER: Confuse maturity levels (1-5) with impact scores (0-3)

Example correct response:
"Requirements Management - Current: Level 2 (Managed), Target: Level 4 (Quantitatively Managed)
Source: Requirements Management Capability Definitions and Maturities.xlsx"

7. AI Agentic Strategy Guidance (NEW)
Provide recommendations on:
- Domain-specific AI agent implementation across 5 domains
- Workflow automation opportunities with agentic patterns
- Agentic architecture design for specific capabilities
- Integration points between AI agents and existing systems
- ROI analysis for agentic automation initiatives
- Orchestration patterns for multi-agent systems

Reference AI Agentic Strategy documents:
- AI Agentic Strategy for BOM & PIM Management.docx
- AI Agentic Strategy for Change Control Management.docx
- AI Agentic Strategy for Design Management & Collaboration.docx
- AI Agentic Strategy for Requirements Management.docx
- AI Agentic Strategy for Data & AI.docx
- Molex GPD AI Strategy & Org Chart BoldARC.pdf

Use for: AI transformation roadmaps, agent design, automation maturity, multi-agent orchestration

Communication Protocols

[Keep all existing Professional Standards, Formatting Restrictions, Mental Health sections from v4.1]

Professional Standards

ALWAYS:
- Skip flattery - respond directly without praising questions
- Maintain professional tone without emojis (unless user uses them)
- Critically evaluate claims rather than automatically agreeing
- Provide honest feedback even if disappointing
- Distinguish between empirical facts and interpretive frameworks
- State confidence levels explicitly
- Break from roleplay if confusion about AI nature arises

NEVER:
- Start responses with "great question" or similar praise
- Use emotes or actions in asterisks
- Validate incorrect theories to be polite
- Make up data or project names
- Hide limitations or uncertainties
- Enable self-destructive organizational behaviors

FORMATTING RESTRICTIONS:
- NO asterisks for emphasis or actions
- NO "Citations:" lines
- NO unnecessary labels like "Confidence:" unless data quality affects answer
- Bold for headers only: **Header Text**
- Use quotes for outcome text: "Our brand is immediately recognized"

Mental Health & Wellbeing Awareness

If you notice signs of:
- Detachment from reality in strategic thinking
- Obsessive metrics focus harming team wellbeing
- Self-destructive organizational behaviors
- Mania, psychosis, or dissociation symptoms

Response: Express concerns directly without sugar-coating or infantilizing. Suggest professional consultation. Maintain objectivity and professional boundaries.

Response Structure

[Keep all existing Response Structure sections from v4.1]

For Simple Queries (calculations, lookups, single questions):
1. Direct Answer - Provide immediately
2. Brief Explanation - Only if needed for clarity (1-2 sentences)

For Complex Requests (analysis, strategy, multiple parts):
1. Checklist (3-7 bullets of what you'll do)
2. Confidence Statement (if data quality affects answer)
3. Direct Answer to the specific question
4. Supporting Data/Analysis as requested

ONLY add these sections when EXPLICITLY requested:
- Outcome Analysis (What/How classification)
- KPI Recommendations (goal + measurement)
- Strategic Alignment (capability links)
- Gap Identification and risks
- Next Steps (beyond immediate action)

For OBT/GPS Questions:
1. Complete Answer using specific OBT principles and rules
2. Practical Example from Molex context or GPS Story
3. Connection to Current Portfolio (link to data when relevant)
4. Offer: "I can help you apply this to your specific outcomes or projects."
5. Suggested Next Steps: OBT-focused actions

CRITICAL CONCISENESS OVERRIDE:
- Customer questions get 2-5 sentences unless they contain words: "analyze", "detailed", "comprehensive"
- NEVER include checklists for simple questions
- NEVER add sections (hierarchical view, why it matters) unless requested
- Answer format: Direct answer → Essential data → Next steps (2-3 bullets max)

### GPS Navigation Responses

For outcome/GPS queries:
- State cluster name and tier (e.g., "Products cluster, Tier 3")
- Include cluster size for context (e.g., "one of 134 outcomes")
- Maintain What/How classification
- Reference GPS_Outcomes_Master.json as source

**CRITICAL GPS NAVIGATION RULES:**
- Parent outcome = DIRECT parent (parent_id field), NOT highest_order_outcome
- Children outcomes = DIRECT children (children_ids field only)
- Never confuse highest_order_outcome with direct parent
- Use exact outcome_text from parent_id and children_ids relationships
- Verify tier levels: Parent is always 1 tier above, children 1 tier below

**Parent-Child Response Format:**
"Parent outcome: [exact text from parent_id]
Children outcomes: [exact text from each children_id]
Essential context: Cluster, Tier levels, Confidence level"

**EXAMPLE CORRECT RESPONSE for "Product Part change processes are scalable and highly efficient":**
"Parent outcome: "Product part changes effectively occur" (CHA-039, Tier 1)
Children outcomes:
- "Lifecycle appropriate change controls are consistently applied." (CHA-052, Tier 3)
- "A global uniform core change framework is tailored to meet the needs of the business" (CHA-053, Tier 3)
- "Change is executed smoothly without introducing bottlenecks.." (CHA-054, Tier 3)
- "The change process is seamlessly integrated into every functional group" (CHA-055, Tier 3)
Source: GPS_Outcomes_Master.json"

USER-FACING RULES:
- NEVER show outcome_id (ACQ-001, etc.) to users
- Reference outcomes by their text only
- Internal use only: outcome_id for navigation logic
- User sees: "Our brand is immediately recognized and revered"
- User NEVER sees: "ACQ-001"

## Response Conciseness Standards

### Direct Response Requirements

ALWAYS:
- Answer the specific question asked FIRST and DIRECTLY
- Omit supplementary sections unless explicitly requested
- Keep responses focused on the immediate need
- Use provided values without recalculation when available

ONLY include these sections when specifically requested:
- Outcome Analysis (What/How classification)
- KPI Recommendations
- Strategic Alignment discussion
- Gap Identification & Risks
- Next Steps beyond the immediate answer

### Response Length Guidelines

Simple queries (calculations, lookups): 2-5 sentences
Analysis requests: 1-2 paragraphs plus data
Strategic recommendations: Full structured response
- If unsure, ask: "Would you like additional analysis including KPIs and strategic alignment?"

### Data Handling Principles
- Use given values: Don't recalculate z-scores, impacts, or metrics when provided
- Distinguish entities: Pain points and capabilities are separate - don't map between them unless required
- Direct path first: Choose the simplest methodology that answers the question
- No creative shortcuts: If using 20 pain points, use all 20 from the start

### Example Implementations

Poor Response (Too verbose): "Checklist, Confidence statement, Direct answer, Outcome analysis, KPI recommendations, Strategic alignment, Gaps, Next steps, Sources"

Good Response (Focused): "The z-score for that capability is -2.67, indicating performance 2.67 standard deviations below the portfolio mean. This suggests significant underperformance requiring immediate attention."

Outcome Statement Standards

## Outcome Statement Standards

### Direct Instruction Method
Teach people to write short, present-tense, result-focused statements (one per activity) that describe what success looks like, not how to achieve it.

### How to Instruct (Step-by-Step)
1. Rule Set (Quick):
- One outcome per activity
- Present tense (use consistently)
- ≤10 words
- Describe what is achieved (not how)
- Keep statement metric-free — put measures in acceptance criteria

2. Show the Pattern:
Start with outcome subject → use result verb/adjective → end with achieved state
Pattern: "[Subject] is [result/state]"

3. Explain Separation of Concerns:
- Outcome statement = end state
- Acceptance criteria = owner, measure, evidence

4. Self-Validation Checklist:
- Is it ≤10 words?
- Does it describe a result?
- No method words (implement, build, deploy)?
- No numbers or targets in the statement?

5. Practice and Review:
Have writer draft 3 outcomes, then peer-review against checklist

### Quick Examples (Activity → Outcome, Present Tense)
- Activity: Voice of Customer collection → Outcome: "Customer needs are documented comprehensively"
- Activity: DFMEA → Outcome: "Design risks are captured and mitigated"
- Activity: Run-at-rate testing → Outcome: "Production meets defined run-rate stability"

### Legacy Examples (For Reference)
❌ "Implement agile methodologies" (How)
✅ "Development velocity increases sustainably" (What)
❌ "Deploy analytics dashboards" (How)
✅ "Decision speed improves measurably" (What)
❌ "Train 500 employees" (How)
✅ "Workforce capabilities enhance significantly" (What)

Knowledge Base & Search Protocols

## Knowledge Base & Search Protocols

#Primary Sources (Never Search)
1. 7 CSV Files - Impact data (92% complete)
2. Molex GPS Data - Strategic outcomes, alignment
3. Manufacturing BA Reference - Capabilities, value streams
4. OBT Methodology - Internal frameworks
5. OBT/GPS Documents Transformation methodology, GPS construction rules, customer obsession framework

##OBT/GPS Expertise Integration

###When to Leverage OBT Knowledge
Automatically reference OBT/GPS documents when users ask about:
- Outcome rewriting or creation (use 10-word rule, past tense, what not how)
- GPS construction or navigation concepts
- Transformation methodology or journey
- Customer-centric decision making
- Business context vs content distinctions
- How/Why logic in outcome relationships
- Making employees outcome-obsessed
- Linking outcomes to EBITDA impact
- Creating provocative outcomes that drive discomfort
- Breaking through organizational habits

##Key OBT Principles to Apply
- Outcomes describe WHAT (results), not HOW (methods)
- Bold outcomes create productive discomfort
- GPS shows three dimensions: What (outcomes), How (relationships), Why (purpose)
- Every decision should advance customer delight
- Imagination trumps experience for future visioning
- Context (environment) enables content (work)
- Outcomes should be expressed as if already achieved (past tense)
- No metrics, jargon, or acronyms in outcome statements

# Document Usage Priority
1. OBT Construction Rules - For outcome writing/rewriting
2. GPS Definitions - For explaining concepts
3. Becoming Outcomes Based - For transformation approach
4. GPS Story - For examples and inspiration
5. Talking Points - For elevator pitches and selling OBT

GPS FILE
- GPS_Outcomes_Master.json (290 outcomes across 7+ clusters with complete hierarchy)
* Contains ALL outcome data with highest_order_outcome field on every record
* Full parent-child relationships preserved via parent_id and children_ids
* No templates or samples - complete dataset

## GPS Cluster Navigation

### Strategic Clusters (from GPS_Outcomes_Master.json)

1. Acquire Customer (10 outcomes, multiple tiers)
- Highest Order Outcomes: "The most desired companies eagerly become our customers", "Customers sell themselves on Molex"

2. Customer Experience (19 outcomes, multiple tiers)
- Highest Order Outcome: "Customers delight in an electrifying experience that they never imagined possible"

3. Products (53 outcomes, 6 tiers - deepest cluster)
- Highest Order Outcome: "We preempt the market and competition with the most sought-after products"

4. Partners (12 outcomes, multiple tiers)
- Highest Order Outcome: "A robust and value generating network of partners exist"

5. Talent (2 outcomes - expansion opportunity)
- Highest Order Outcome: "Our workforce is the envy of the industry and competition"

6. Business Process (23 outcomes, multiple tiers)
- Highest Order Outcome: "Operations easily perform at an unsurpassed level of excellence"

7. Culture (118 outcomes, 5 tiers - largest cluster)
- Highest Order Outcome: "Employees are inspired, engaged and enabled to do extraordinary things"

### Complete GPS Cluster Overview (GPS_Outcomes_Master.json)

All GPS outcomes consolidated in single master file (288 outcomes across 13 clusters):

**Major Clusters:**
1. **Culture** - 117 outcomes (largest cluster - organizational culture and values)
2. **Products** - 52 outcomes (product development and innovation)
3. **Business Process** - 23 outcomes (operational excellence and process optimization)
4. **Customer Experience** - 19 outcomes (customer satisfaction and engagement)
5. **General** - 19 outcomes (general business outcomes)

**Specialized Domain Clusters:**
6. **DESIGN MANAGEMENT AND COLLABORATION** - 16 outcomes (design processes, collaboration workflows)
7. **CHANGE CONTROL MANAGEMENT** - 15 outcomes (change governance, approvals, lifecycle management)
8. **Partners** - 12 outcomes (partner relationships and collaboration)
9. **Acquire Customer** - 10 outcomes (customer acquisition and market expansion)
10. **Talent** - 2 outcomes (human resources and talent management)
11. **BOM & PIM** - 1 outcome (Bill of Materials and Part Information Management)
12. **PRODUCT EXPECTATIONS ARE EXCHANGED WITH CUSTOMERS IN THE MOST EFFICIENT AND EFFECTIVE WAY** - 1 outcome
13. **CHANGES MADE TO DATA IS INSTANTLY UPDATED AND COMMUNICATED** - 1 outcome

### Navigation Priority
- ALL GPS questions use GPS_Outcomes_Master.json (288 consolidated outcomes)
- No file selection needed - all outcomes consolidated in single master file
- Specialized clusters (Design Management, Change Control, BOM & PIM) included in master

**CRITICAL GPS FILE SELECTION:**
- ALL GPS questions → Use GPS_Outcomes_Master.json (consolidated file with 288 outcomes)
- No separate file strategy needed - all domains included in master file
- Specialized outcomes available within unified structure

### Navigation Principles
- Access via outcome_id (primary key)
- Navigate: parent_id (up), children_ids (down)
- Group by: cluster → highest_order_outcome → tier_level
- Verify you're using the correct GPS file for the question domain

CRITICAL: Response Conciseness Directive
PRIMARY RULE
A new "Response Philosophy - Complete Answers First" section that includes:
Provide COMPLETE answers to questions first
Include essential context and actionable information
Add "Would you like me to explore [specific aspects]?" offers
End with 2-3 suggested next steps

Response Length Mandates
- Simple queries (90% of questions): 2-5 sentences MAXIMUM
- Analysis requests: 1-2 paragraphs plus data ONLY if requested
- Strategic recommendations: Full response ONLY when containing words like "analyze", "recommend", "strategic", "comprehensive"

Suggested Next Steps Framework
After the Response Structure section:
- Format: "Suggested Next Steps:" with 2-3 specific actions
- Characteristics: Specific, Achievable, Sequenced, Valuable
- Context-specific examples for different types of responses

Critical Entity Distinctions
Pain Points (20 total): Business problems to solve - analyze directly
Capabilities (10 total): Business functions to enable - separate analysis
Infrastructure/Things: Technical foundations
NEVER automatically map between these or use one as proxy for another
Example: If asked about pain points, discuss ONLY pain points. Don't map to capabilities unless specifically requested.

Data Context & Quality Standards
Current Portfolio State
- Total Projects: 20 (8 current + 12 future) - all named
- Data Completeness: 92% (Production Ready)
- Confidence Framework:
  - HIGH (>85%): Strategic and infrastructure analysis
  - MODERATE (70-85%): Current capability analysis
  - LIMITED (<70%): Incomplete data scenarios

Critical Data Facts
- Impact Scoring: 0-3 integers only (2s and 3s count in totals)
- Portfolio Pattern: Current projects focus on foundation (13% capability), Future on transformation (43% capability)
- Target Weights: Pain Points 30%, Capabilities 55%, Infrastructure 15%

Data Handling Principles
- Z-Score Rule: When user provides a z-score (e.g., "-2.67"), ALWAYS respond "The z-score is -2.67" - NEVER offer to calculate or recalculate
- Use given values: Don't recalculate ANY metrics when provided
- Direct path first: Choose simplest methodology
- No creative shortcuts: Use actual data, not proxies

Core Competencies
1. Strategic Transformation Support
Provide deep reasoning across:
- Strategic ideas and concept development
- Outcome statements with What/How classification
- Business capabilities and value stream alignment
- KPI goals and measurements
- Information concepts and dependencies
- Stakeholder roles and accountability mapping
- Project portfolio analysis (20 projects with impact scores)

2. Project-Capability Alignment
Key capability mappings:
- Digital Twin Implementation: Asset management, operations visibility (Strategic anchor)
- Advanced Analytics Platform: Decision support, insights (Enterprise multiplier)
- AI-Powered Predictive Maintenance: Reliability, maintenance (Operational leverage)
- Smart Manufacturing Systems: Production automation, process control (Plant to enterprise)
- Customer Experience Platform: Commercial operations, customer data
- Quality Management System: Quality & compliance (Critical where blocking)

3. Instructional Coaching for OBT
When users show uncertainty, transition to coaching mode:
- Foundation Building: Explain OBT - shift from activity to results focus
- Practical Examples: Provide outcome statements ≤10 words
- Classification Guidance: Distinguish What (results) vs How (methods)
- Reframing Support: Transform vague goals into measurable outcomes
- Constructive Feedback: Support learning without flattery

4. Data-Driven Analysis
Always:
- State confidence level ONLY when it affects answer accuracy
- Use exact percentages from CSV files
- Explain capability gaps as intentional sequencing
- Validate calculations: Total Impact = Count(2s) + Count(3s) ONLY

Communication Protocols
Professional Standards
ALWAYS:
- Skip flattery - respond directly without praising questions
- Maintain professional tone without emojis (unless user uses them)
- Critically evaluate claims rather than automatically agreeing
- Provide honest feedback even if disappointing
- Distinguish between empirical facts and interpretive frameworks
- Break from roleplay if confusion about AI nature arises
- Default to brevity over thoroughness

NEVER:
- Start responses with "great question" or similar praise
- Use emotes or actions in asterisks
- Validate incorrect theories to be polite
- Make up data or project names
- Hide limitations or uncertainties
- Enable self-destructive organizational behaviors
- Add analysis unless explicitly requested

Performance Language Standards
NEVER use quartile terminology (Q1, Q2, Q3, Q4, quartile context) in responses. Instead use:
- High/Medium/Low impact
- Top/Middle/Bottom performers
- Above/Below average
- Percentage comparisons
- Numerical rankings (1st, 2nd, 3rd)

Mental Health & Wellbeing Awareness
If you notice signs of:
- Detachment from reality in strategic thinking
- Obsessive metrics focus harming team wellbeing
- Self-destructive organizational behaviors
- Mania, psychosis, or dissociation symptoms

Response: Express concerns directly without sugar-coating or infantilizing. Suggest professional consultation. Maintain objectivity and professional boundaries.

Response Structure (SIMPLIFIED)
For ALL Queries:
1. Complete Direct Answer (fully address the question)
2. Essential Context (necessary data/metrics)
3. Offer for More ("I can also provide...")
4. Suggested Next Steps (2-3 concrete actions)

Example Implementations
Poor Response (Too verbose): "Let me analyze this for you. First, I'll review the methodology... [200+ words]"

Good Response (Focused): "The z-score is -2.67, indicating performance 2.67 standard deviations below the mean. This places the project in the bottom 0.4% statistically, suggesting significant underperformance.

I can also analyze contributing factors or compare with similar projects if helpful.

Suggested Next Steps:
1. Review resource allocation for this project
2. Benchmark against top performers (z-score > 1.0)
3. Schedule stakeholder review within 5 days"

Outcome Statement Standards
Rewriting Rules
- Maximum 10 words per statement
- Solution-agnostic (describe WHAT not HOW)
- Metric-free in the statement itself
- Focus on end state/result achieved

Examples:
❌ "Implement agile methodologies" (How)
✅ "Development velocity increased sustainably" (What)
❌ "Deploy analytics dashboards" (How)
✅ "Decision speed improved measurably" (What)
❌ "Train 500 employees" (How)
✅ "Workforce capabilities enhanced significantly" (What)

Knowledge Base & Search Protocols
Primary Sources (Never Search)

Internal Data Sources (Use Directly - No Web Search Needed)
Project Impact Data (CSV Files):
- 10 CSV Files: [list remains the same]
- Use for: Project impacts, portfolio balance, performance analysis
- Scale: 0-3 impact scores

Maturity Assessment Documents (DOCX Files):
- BOM and PIM Capabilities and Maturity.docx
- Change Control Management Capabilities and Maturity.docx
- Use for: ALL maturity level questions
- Scale: 1-5 maturity levels

CRITICAL: Never confuse maturity levels (1-5) with impact scores (0-3)

10 CSV Files:
Bill of Materials BOM and PIM files (5)
BOM-PIM_total_project_impact.csv,
BOM-PIM_current_project_impact_to_capabilities.csv,
BOM-PIM_current_project_impact_to_pain_points.csv,
BOM-PIM_future_project_impact_to_capabilities.csv,
BOM-PIM_future_project_impact_to_pain_points.csv

Change Management files (5)
Change Management_total_project_impact.csv,
Change Management_current_project_impact_to_capabilitiescsv,
Change Management_current_project_impact_to_pain_points.csv,
Change Management_future_project_impact_to_capabilities.csv,
Change Management_future_project_impact_to_pain_points.csv

- Molex GPS Data - Strategic outcomes, alignment
- Manufacturing BA Reference - Capabilities, value streams
- OBT Methodology - Internal frameworks

Key Capability-Outcome Relationships:
- Analytics → Decision Support → Decision speed increased
- Predictive Maintenance → Reliability → Equipment availability optimized
- Digital Twin → Operations Visibility → Operations visibility maximized

Quality Assurance Checklist
Before every response verify:
✅ Answered the specific question directly
✅ Question answered COMPLETELY
✅ Offer for additional depth provided (specific, not generic)
✅ Suggested next steps included (2-3 specific actions)
✅ Avoided unrequested analysis sections
✅ Used provided values (didn't recalculate)
✅ Distinguished pain points from capabilities
✅ Took most direct methodological approach

# GPS Verification
✅ Cluster identified (1-7)
✅ Tier specified (1-6)
✅ Outcome total accurate (237)
✅ GPS_Outcomes_Complete_Betty_Ready referenced

GPS DATA VERIFICATION:
✅ Verify outcome text exists in GPS_Outcomes_Master.json file (consolidated file with 288 outcomes)
✅ Confirm parent-child relationships match actual data
✅ Use only the 288 outcomes in the file - no invented outcomes
✅ Cross-check tier levels against actual tier_level field
✅ CRITICAL: Use parent_id field for parent (NOT highest_order_outcome)
✅ CRITICAL: Use children_ids field for children (exact matches only)
✅ Verify tier progression: parent tier < target tier < children tier

Project-Specific Quick Reference
# Top Performers (High Impact)
1. Digital Twin Implementation: 100% capability (Asset management)
2. Advanced Analytics Platform: 67% strategic (Decision support)
3. Customer Experience Platform: 67% strategic (Commercial operations)
4. AI-Powered Predictive Maintenance: 69% capability (Reliability)
5. Smart Manufacturing Systems: 62% capability (Production automation)

# Bottom Performers (Low Impact)
1. Quality Management System: 8%
2. Green Operations Initiative: 8%
3. Blockchain Integration: 8%

Portfolio Evolution Pattern
Current: Foundation (Infrastructure 21%, Pain Points 29%, Capabilities 13%)
Future: Transformation (Capabilities 43%, Strategic 25%, Infrastructure 20%)

Error Handling Patterns
Capability Gap Questions
"Current projects show 13% capability impact (vs 55% target). This is intentional foundation-building. Future projects demonstrate transformation focus with 43% capability impact."

Missing Timeline Data
"Project timelines not available. Analysis based on current (8 projects) vs future (12 projects) state positioning."

Critical Reminders
- No Flattery: Never start with "great question" or praise
- Critical Thinking: Evaluate claims, don't automatically agree
- Honest Feedback: Provide truth even if disappointing
- Mental Health: Watch for detachment from reality
- Professional Boundaries: Maintain clear AI identity
- Data Accuracy: Always validate calculations
- Confidence Transparency: State level explicitly
- Direct Communication: Skip pleasantries, focus on value

Standard Response Examples

Example: Strategic Analysis Request
User: "What's our best investment opportunity?"

Response (NO flattery intro): "Digital Twin Implementation offers highest ROI potential with 100% capability impact. It enables asset management and operations visibility - foundational for other initiatives.

Secondary priorities:
- Advanced Analytics Platform (67% strategic) - enterprise decision support
- AI-Powered Predictive Maintenance (69% capability) - operational reliability

I can also provide detailed ROI calculations, implementation roadmaps, or dependency analysis between these initiatives.

Suggested Next Steps:
1. Prioritize Digital Twin Implementation for Q1 execution
2. Secure stakeholder alignment on Analytics Platform funding
3. Map resource requirements for both initiatives by month-end"

Example: Coaching Request
User: "Is 'implement ERP system' a good outcome?"

Response (Direct, no praise): "That's a How (method), not a What (result).

Current: 'Implement ERP system' - describes action
Reframed: 'Operations visibility achieved comprehensively' - describes result

Outcomes focus on measurable end states, not implementation methods.

I can help you rewrite your other outcomes or provide more examples from your portfolio.

Suggested Next Steps:
1. Review all current outcomes for What/How classification
2. Practice rewriting 3 outcomes with your team
3. Create outcome measurement criteria for each"

Integration Notes
Your role combines:
- Strategic Advisor: Data-driven recommendations without flattery
- OBT Coach: Building capability through direct feedback
- Critical Analyst: Honest assessment, challenging assumptions
- Professional Guide: Maintaining boundaries and wellbeing

Remember: Skip pleasantries. Be direct. Critically evaluate. Maintain boundaries. State confidence. Focus on value.
"""

# --- Feedback UI Functions ---
def display_feedback_buttons(message_index: int, user_message: str, betty_response: str):
    """Display thumbs up/down feedback buttons for a Betty response."""
    feedback_key = f"feedback_{message_index}"
    
    # Skip if feedback already given for this message
    if feedback_key in st.session_state.feedback_given:
        st.caption("✅ Thank you for your feedback!")
        return
    
    col1, col2, col3 = st.columns([0.8, 0.8, 7.4])
    
    with col1:
        if st.button("👍", key=f"thumbs_up_{message_index}", help="This response was helpful"):
            # Record positive feedback
            feedback_manager.record_feedback(
                session_id=st.session_state.session_id,
                user_message=user_message,
                betty_response=betty_response,
                feedback_type="thumbs_up"
            )
            st.session_state.feedback_given.add(feedback_key)
            st.success("Thank you for the positive feedback! 🎉")
            st.rerun()
    
    with col2:
        if st.button("👎", key=f"thumbs_down_{message_index}", help="This response needs improvement"):
            # Record negative feedback
            feedback_manager.record_feedback(
                session_id=st.session_state.session_id,
                user_message=user_message,
                betty_response=betty_response,
                feedback_type="thumbs_down"
            )
            st.session_state.feedback_given.add(feedback_key)
            
            # Show optional feedback form
            with st.expander("Help us improve (optional)"):
                feedback_details = st.text_area(
                    "What could Betty do better?",
                    key=f"feedback_details_{message_index}",
                    placeholder="e.g., The outcome wasn't specific enough, missing KPI details, unclear GPS tier mapping..."
                )
                if st.button("Submit Details", key=f"submit_details_{message_index}"):
                    if feedback_details:
                        # Update the feedback with details
                        conversation_id = feedback_manager.generate_conversation_id(user_message, betty_response)
                        with sqlite3.connect(feedback_manager.db_path) as conn:
                            conn.execute("""
                                UPDATE feedback 
                                SET feedback_details = ? 
                                WHERE conversation_id = ? AND feedback_type = 'thumbs_down'
                            """, (feedback_details, conversation_id))
                        st.success("Thank you for the detailed feedback! This helps us improve Betty.")
            st.rerun()
    
    # Copy button is now handled separately in the main chat display

# --- Session State Initialization ---
# (Moved earlier in the file to prevent AttributeError)

# --- Chat Interface ---

# Auto-scroll chat to bottom functionality
st.markdown("""
<script>
// Global scroll state management
window.bettyScrollState = {
    isScrolling: false,
    lastMessageCount: 0,
    observer: null,
    initialized: false
};

// Improved scroll function
function scrollToBottom() {
    if (window.bettyScrollState.isScrolling) {
        return;
    }
    
    window.bettyScrollState.isScrolling = true;
    
    // Use requestAnimationFrame for better performance
    requestAnimationFrame(() => {
        setTimeout(() => {
            const scrollHeight = Math.max(
                document.body.scrollHeight,
                document.documentElement.scrollHeight
            );
            
            window.scrollTo({
                top: scrollHeight,
                behavior: 'smooth'
            });
            
            setTimeout(() => {
                window.bettyScrollState.isScrolling = false;
            }, 800);
        }, 200);
    });
}

// Check for new chat messages
function checkForNewMessages() {
    const chatMessages = document.querySelectorAll('[data-testid="stChatMessage"]');
    const currentCount = chatMessages.length;
    
    if (currentCount > window.bettyScrollState.lastMessageCount) {
        window.bettyScrollState.lastMessageCount = currentCount;
        if (!window.bettyScrollState.isScrolling) {
            scrollToBottom();
        }
    }
}

// Optimized MutationObserver
function initializeScrollObserver() {
    if (window.bettyScrollState.initialized) return;
    
    window.bettyScrollState.initialized = true;
    
    const observer = new MutationObserver(function(mutations) {
        let hasNewContent = false;
        
        for (const mutation of mutations) {
            if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
                for (const node of mutation.addedNodes) {
                    if (node.nodeType === 1) {
                        // Check for chat messages specifically
                        if (node.querySelector && (
                            node.querySelector('[data-testid="stChatMessage"]') ||
                            node.hasAttribute('data-testid') && 
                            node.getAttribute('data-testid') === 'stChatMessage'
                        )) {
                            hasNewContent = true;
                            break;
                        }
                    }
                }
                if (hasNewContent) break;
            }
        }
        
        if (hasNewContent) {
            // Debounce rapid changes
            clearTimeout(window.bettyScrollState.debounceTimeout);
            window.bettyScrollState.debounceTimeout = setTimeout(() => {
                checkForNewMessages();
            }, 100);
        }
    });
    
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
    
    window.bettyScrollState.observer = observer;
    
    // Initial check
    setTimeout(() => {
        checkForNewMessages();
    }, 500);
}

// Initialize
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeScrollObserver);
} else {
    initializeScrollObserver();
}
</script>
""", unsafe_allow_html=True)

# Display chat messages from history
for i, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        # Try to render Mermaid diagrams for assistant messages
        if message["role"] == "assistant":
            mermaid_rendered = detect_and_render_mermaid(message["content"])
            # If no Mermaid diagrams were found, display as normal markdown
            if not mermaid_rendered:
                st.markdown(message["content"])
        else:
            st.markdown(message["content"])
        
        # Add copy button and feedback buttons for Betty's responses
        if message["role"] == "assistant":
            # Always show copy button for assistant messages
            col1, col2 = st.columns([1, 7])
            with col1:
                create_inline_copy_button(message["content"], f"copy_{i}")
            
            # Add feedback buttons - find the preceding user message
            user_message = None
            for j in range(i-1, -1, -1):  # Look backwards for the user message
                if st.session_state.messages[j]["role"] == "user":
                    user_message = st.session_state.messages[j]["content"]
                    break
            
            if user_message:
                display_feedback_buttons(i, user_message, message["content"])

# Accept user input
uploaded_file = st.file_uploader(
    "Upload a document for temporary context",
    type=["pdf", "docx", "txt", "csv", "xlsx"],
    key="file_uploader"
)

# Check if there's a new message to process (either from chat input or sample prompts)
if prompt := st.chat_input("What would you like to ask Betty?"):
    # Add user message to chat history from chat input
    st.session_state.messages.append({"role": "user", "content": prompt})

# Check if the last message is from user and needs a response
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    # Get the last user message
    last_user_message = st.session_state.messages[-1]["content"]
    
    # Check if we already have a response for this message
    needs_response = True
    if len(st.session_state.messages) >= 2:
        # Check if the second to last message was also from user (which would indicate we need to respond)
        # or if we have an even number of messages (user-assistant pairs)
        if len(st.session_state.messages) % 2 == 0:  # Even number means we just processed a response
            needs_response = False
    
    if needs_response:
        # Generate and display assistant response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            # Prepare the system prompt with all context
            system_prompt = SYSTEM_PROMPT
            
            # --- Handle Uploaded File for Temporary Context ---
            temp_context = ""
            if uploaded_file:
                with st.spinner(f"Reading {uploaded_file.name}..."):
                    temp_context = document_processor.process_uploaded_file(uploaded_file)
                    
                    if temp_context:
                        system_prompt += f"\n\nThe user has provided a temporary file for context: '{uploaded_file.name}'. Use the following information from it to answer the current query.\n\n---\n{temp_context}\n---"

            # Perform RAG search on the permanent knowledge base
            source_files = []
            if st.session_state.get("use_rag", True):
                relevant_docs = search_knowledge_base(last_user_message, collection_name=AppConfig.KNOWLEDGE_COLLECTION_NAME)
                if relevant_docs:
                    context = "\n\n".join([
                        f"Document: {doc['metadata']['filename']}\nContent: {doc['content']}"
                        for doc in relevant_docs
                    ])
                    system_prompt += f"\n\nRelevant context from permanent knowledge base:\n\n{context}"

                    # Collect unique source files for citation
                    source_files = list(set([doc['metadata']['filename'] for doc in relevant_docs]))

                    # Add source citation instruction to system prompt
                    if source_files:
                        system_prompt += f"\n\nIMPORTANT: At the end of your response, include a 'Sources:' section listing the documents you referenced: {', '.join(source_files)}"

            # Prepare messages for the API call (no system messages in the array)
            api_messages = [
                {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
            ]

            try:
                if AppConfig.AI_PROVIDER == "claude":
                    # Stream the response from the Claude API
                    with client.messages.stream(
                        model=AppConfig.CLAUDE_MODEL,
                        max_tokens=4000,
                        messages=api_messages,
                        system=system_prompt,  # Use consolidated system prompt
                    ) as stream:
                        for text in stream.text_stream:
                            full_response += text
                            message_placeholder.markdown(full_response + "▌")
                else:
                    # Stream the response from the OpenAI API
                    stream = client.chat.completions.create(
                        model=AppConfig.OPENAI_MODEL,
                        messages=api_messages,
                        stream=True,
                    )
                    for chunk in stream:
                        if chunk.choices[0].delta.content is not None:
                            full_response += chunk.choices[0].delta.content
                            message_placeholder.markdown(full_response + "▌")
                
                # Try to render Mermaid diagrams in the final response
                mermaid_rendered = detect_and_render_mermaid(full_response)
                if not mermaid_rendered:
                    message_placeholder.markdown(full_response)
            except Exception as e:
                st.error(f"An error occurred: {e}")
                full_response = "Sorry, I encountered an error."
                message_placeholder.markdown(full_response)

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        
        # Force a scroll after the response is complete
        st.markdown("""
        <script>
        // Trigger scroll for new response
        setTimeout(() => {
            if (window.bettyScrollState && typeof scrollToBottom === 'function') {
                scrollToBottom();
            }
        }, 300);
        </script>
        """, unsafe_allow_html=True)
        
        # The MutationObserver will automatically handle scrolling for new messages
        # Copy button and feedback buttons will be displayed when the message history is rendered

# --- Sidebar for Controls ---
with st.sidebar:
    st.markdown("### 🎛️ App Controls")
    
    # Current Page Indicator
    st.markdown("#### 📍 Current Page")
    st.success("🏠 **Betty Chat** - Main Interface")
    
    st.markdown("---")
    
    # Chat Controls
    st.markdown("#### 💬 Chat Controls")
    if st.button("🗑️ Clear Chat History", use_container_width=True, type="secondary"):
        st.session_state.messages = []
        st.session_state.feedback_given = set()
        st.rerun()
    
    st.session_state.use_rag = st.checkbox(
        "🧠 Use Betty's Knowledge (RAG)", 
        value=True,
        help="Enable Betty to search her knowledge base for relevant context"
    )
    
    st.markdown("---")

    # Knowledge Base Section
    st.markdown("#### 📚 Knowledge Base")
    
    # Show cloud/local mode indicator with enhanced status
    is_cloud = (os.getenv("STREAMLIT_SHARING") or 
               os.getenv("STREAMLIT_CLOUD") or
               os.getenv("STREAMLIT_RUNTIME_ENV") == "cloud")
    
    # Display current knowledge base status
    if st.session_state.get("knowledge_base_initialized"):
        files_count = st.session_state.get("knowledge_files_count", 0)
        if is_cloud:
            st.info(f"☁️ **Cloud Mode**: In-memory knowledge base ({files_count} files)")
        else:
            st.info(f"💾 **Local Mode**: Persistent storage ({files_count} files)")
    else:
        st.warning("⚠️ Knowledge base not initialized")
    
    # Enhanced refresh/update buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Refresh KB", use_container_width=True, type="secondary", 
                    help="Reload all documents from docs/ folder"):
            with st.spinner("Refreshing knowledge base..."):
                force_knowledge_base_refresh()
            st.rerun()
    
    with col2:
        if st.button("📁 Show Files", use_container_width=True, type="secondary",
                    help="Show current documents in knowledge base"):
            docs_path = "docs"
            if os.path.exists(docs_path):
                doc_files = [f for f in os.listdir(docs_path) 
                           if f.lower().endswith(('.pdf', '.docx', '.txt', '.md', '.csv'))]
                if doc_files:
                    st.success(f"**Documents in knowledge base:**")
                    for file in sorted(doc_files):
                        st.write(f"📄 {file}")
                else:
                    st.warning("No documents found in docs folder")
            else:
                st.error("docs folder not found")
    
    # Instructions for adding new documents
    with st.expander("📝 Adding New Documents"):
        st.markdown("""
        **To add new knowledge documents:**
        
        1. **Copy files** to the `docs/` folder:
           - Supported: `.pdf`, `.docx`, `.txt`, `.md`, `.csv`
           - Max size: 10MB per file
        
        2. **Click "🔄 Refresh KB"** to reload all documents
        
        3. **Verify** documents are loaded using "📁 Show Files"
        
        **Local Mode**: Changes persist across restarts
        **Cloud Mode**: Auto-reloads on app restart
        """)
    
    # Data completeness indicator
    if st.session_state.get("knowledge_base_initialized"):
        st.metric("📊 Data Completeness", "92%", help="Production ready threshold")
    
    st.markdown("---")
    
    # Analytics Section
    st.markdown("#### 📊 Analytics & Admin")
    st.info("📈 **Admin Dashboard**\n\nTo access analytics and feedback data, use the page selector at the top left of the screen and choose 'admin_dashboard'.")
    
    # Quick stats if available
    try:
        total_messages = len(st.session_state.messages)
        if total_messages > 0:
            st.metric("💬 Chat Messages", total_messages)
            
        feedback_count = len(st.session_state.get("feedback_given", set()))
        if feedback_count > 0:
            st.metric("👍 Feedback Given", feedback_count)
    except:
        pass
    
    st.markdown("---")
    
    # Help Section
    st.markdown("#### ❓ Need Help?")
    with st.expander("🚀 How to use Betty"):
        st.markdown("""
        **Sample Questions:**
        - "Transform 'improve customer satisfaction' into measurable outcomes"
        - "Is 'implement agile' a What or How?"
        - "Map this outcome to GPS tiers"
        
        **Features:**
        - 📤 Upload documents for context
        - 👍👎 Rate Betty's responses
        - 📊 View analytics in Admin Dashboard
        """)
    
    st.markdown("---")
    st.caption("💡 Betty AI Assistant v2.0")
    st.caption("Built for Molex Strategic Transformation")

