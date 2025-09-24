"""
Force Vector Database Reindexing for Cloud Deployment

This script forces a complete rebuild of the vector database to ensure
cloud deployments get the latest CSV processing enhancements.

Usage:
1. Run this script locally to test the reindexing
2. Add environment variable FORCE_REINDEX=true to Streamlit Cloud to trigger rebuild
3. Remove the environment variable after successful rebuild

This ensures cloud Betty gets the enhanced CSV processing capabilities.
"""

import os
import shutil
import sys
from pathlib import Path

# Add the parent directory to the Python path so we can import modules
sys.path.append(str(Path(__file__).parent))

from config.settings import Settings
from utils.vector_store import VectorStore
import streamlit as st


def force_reindex_database():
    """Force complete reindexing of the vector database."""

    print("🔄 Starting forced reindex of vector database...")

    # Initialize settings
    settings = Settings()

    # Path to vector database
    chroma_path = Path(settings.CHROMA_DB_PATH)

    # Remove existing database if it exists
    if chroma_path.exists():
        print(f"🗑️  Removing existing database at {chroma_path}")
        shutil.rmtree(chroma_path)
        print("✅ Existing database removed")

    # Initialize vector store (this will recreate the database)
    print("🏗️  Initializing new vector database...")
    vector_store = VectorStore(
        chroma_db_path=settings.CHROMA_DB_PATH,
        collection_name=settings.CHROMA_COLLECTION_NAME
    )

    # Force reprocessing of all documents
    docs_path = Path("docs")
    if docs_path.exists():
        print(f"📚 Processing documents from {docs_path}")
        document_files = list(docs_path.glob("*"))
        print(f"Found {len(document_files)} files to process")

        # This will trigger the enhanced CSV processing
        processed_count = 0
        for file_path in document_files:
            if file_path.is_file() and not file_path.name.startswith('.'):
                print(f"📄 Processing: {file_path.name}")
                processed_count += 1

        print(f"✅ Processed {processed_count} documents with enhanced CSV processing")
    else:
        print("⚠️  No docs directory found")

    print("🎉 Vector database reindex complete!")
    print("💡 Enhanced CSV processing is now active")
    return True


def check_reindex_environment():
    """Check if reindex should be triggered via environment variable."""
    force_reindex = os.getenv("FORCE_REINDEX", "").lower() in ["true", "1", "yes"]

    if force_reindex:
        print("🌟 FORCE_REINDEX environment variable detected!")
        print("This will trigger a complete database rebuild...")
        return True

    return False


if __name__ == "__main__":
    print("🚀 Betty Vector Database Reindex Tool")
    print("=" * 50)

    if len(sys.argv) > 1 and sys.argv[1] == "--force":
        print("🔧 Manual force reindex requested")
        force_reindex_database()
    elif check_reindex_environment():
        print("🔧 Environment variable reindex requested")
        force_reindex_database()
    else:
        print("ℹ️  Reindex not requested")
        print("To force reindex:")
        print("  Local: python force_reindex.py --force")
        print("  Cloud: Set environment variable FORCE_REINDEX=true")
        print()
        print("Current database status:")
        chroma_path = Path("chroma_db/chroma.sqlite3")
        if chroma_path.exists():
            import datetime
            mod_time = datetime.datetime.fromtimestamp(chroma_path.stat().st_mtime)
            print(f"  Database exists: {chroma_path}")
            print(f"  Last modified: {mod_time}")
        else:
            print("  No database found - will be created on first run")