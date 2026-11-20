# scenario-id: US-02/SC-9
"""SC-9: pytest covers all StatusCalculator rules BR-01 to BR-08.
Then: exit_code equals 0
"""
import json
import subprocess
import sys


def main():
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/test_status_calculator.py", "-v", "--tb=short"],
        capture_output=True,
        text=True,
    )
    print(json.dumps({"exit_code": result.returncode}))


if __name__ == "__main__":
    main()
