#!/usr/bin/env python3
"""
PATH Framework CLI - Artifact Generation
Wrapper script to generate PATH-compliant artifacts using the Software Engineering Methodology

Usage:
    uv run python path_generate.py --project "My API" --domain "business"
    
    # Or run directly from the phase directory:
    uv run python -m path_framework.phases.arch.generate_artifacts --project "My API"
"""

import sys
import os
from pathlib import Path

# Add framework to path
framework_root = Path(__file__).parent
sys.path.insert(0, str(framework_root))

# Import and run the artifact generator
if __name__ == "__main__":
    try:
        from path_framework.phases.arch.generate_artifacts import main
        main()
    except ImportError as e:
        print(f"❌ Error importing PATH Framework: {e}")
        print("💡 Make sure you're running with UV from the PATH Framework root directory:")
        print("   uv run python path_generate.py --project 'Your Project'")
        sys.exit(1)
