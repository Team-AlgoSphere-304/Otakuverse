#!/usr/bin/env python3
"""
OtakuVerse Startup Script
Run the FastAPI server for the backend
"""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

def main():
    """Start the OtakuVerse API server."""
    import uvicorn
    from dotenv import load_dotenv
    
    # Load environment variables
    load_dotenv()
    
    # Get configuration from environment
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8000"))
    debug = os.getenv("API_DEBUG", "True").lower() == "true"
    
    print(f"""
    ╔══════════════════════════════════════════════════════════╗
    ║                   🎌 OtakuVerse API 🎌                   ║
    ║     Multi-Agent Entertainment Recommendation System      ║
    ╚══════════════════════════════════════════════════════════╝
    
    Starting server...
    - Host: {host}
    - Port: {port}
    - Debug: {debug}
    
    📍 API will be available at: http://{host if host != '0.0.0.0' else 'localhost'}:{port}
    📚 Swagger UI: http://localhost:{port}/docs
    📖 ReDoc: http://localhost:{port}/redoc
    """)
    
    # Try ultra-fast server first, then fallback
    try:
        print("🚀 Loading Ultra-Fast Server (server_fast)...")
        uvicorn.run(
            "api.server_fast:app",
            host=host,
            port=port,
            reload=False,  # Faster startup
            log_level="info"
        )
    except Exception as e:
        print(f"Trying Gemini server: {e}")
        try:
            uvicorn.run(
                "api.server_v2:app",
                host=host,
                port=port,
                reload=False,
                log_level="info"
            )
        except Exception as e2:
            print(f"Falling back to standard server: {e2}")
            uvicorn.run(
                "api.server:app",
                host=host,
                port=port,
                reload=debug,
                log_level="info"
            )


if __name__ == "__main__":
    main()
