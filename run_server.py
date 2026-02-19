"""
Start the Queue Management System server
"""
import uvicorn
from config import settings
import os
import uvicorn
port = int(os.environ.get("PORT", 10000))

if __name__ == "__main__":
    print("=" * 60)
    print(f"🇪🇹 {settings.app_name}")
    print(f"Version: {settings.version}")
    print("=" * 60)
    print(f"\n🚀 Starting server on http://{settings.host}:{settings.port}")
    print(f"📖 API Documentation: http://localhost:{settings.port}/docs")
    print(f"📊 Alternative Docs: http://localhost:{settings.port}/redoc")
    print("\nPress CTRL+C to stop the server\n")
    print("=" * 60)
    
    uvicorn.run(
        "main:app",
       # host=settings.host,
        host="0.0.0.0",
        port=settings.port,
        reload=True,
        log_level="info"
    )

