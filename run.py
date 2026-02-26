"""
run.py — Launch Manufacture Balance 4.0 Dashboard
"""

import subprocess
import sys
import os

def main():
    app_path = os.path.join(os.path.dirname(__file__), "app.py")

    print("🏭 Starting Manufacture Balance 4.0...")
    print("   Open in browser: http://localhost:8501")
    print("   Press Ctrl+C to stop\n")

    subprocess.run(
        [sys.executable, "-m", "streamlit", "run", app_path,
         "--server.headless", "true"],
    )

if __name__ == "__main__":
    main()
