#!/usr/bin/env python3
"""
Fix embedding dimension mismatch in Betty's knowledge base.

This script deletes the existing collection and recreates it with the correct
embedding dimensions to match the current configuration.
"""

import os
import sys
import shutil
from pathlib import Path

def fix_embedding_dimensions():
    """Delete the existing ChromaDB collection to force recreation with correct dimensions."""

    # Path to the ChromaDB directory
    chroma_path = Path("./data/betty_chroma_db")

    print("🔧 Fixing embedding dimension mismatch...")
    print(f"Target path: {chroma_path}")

    if chroma_path.exists():
        print(f"📁 Found existing ChromaDB at {chroma_path}")
        try:
            # Remove the entire ChromaDB directory
            shutil.rmtree(chroma_path)
            print("✅ Successfully deleted existing ChromaDB")
        except Exception as e:
            print(f"❌ Error deleting ChromaDB: {e}")
            return False
    else:
        print("ℹ️ No existing ChromaDB found")

    print("🎯 Next steps:")
    print("1. Start Betty with: streamlit run betty_app.py")
    print("2. The knowledge base will be recreated automatically with correct dimensions")
    print("3. All documents in docs/ folder will be reprocessed")

    return True

if __name__ == "__main__":
    success = fix_embedding_dimensions()
    if success:
        print("\n✨ Fix completed successfully!")
        print("You can now restart Betty and the embedding dimension issue should be resolved.")
    else:
        print("\n💥 Fix failed. Please check the error messages above.")
        sys.exit(1)