# executor.py

import subprocess
import tempfile
from typing import Dict, Any


def run_python(code: str, tests: str, timeout: int = 5) -> Dict[str, Any]:
    """
    执行 Python 代码 + 测试
    """
    with tempfile.NamedTemporaryFile(
        suffix=".py",
        mode="w",
        delete=False,
        encoding="utf-8"
    ) as f:
        f.write(code)
        f.write("\n\n")
        f.write(tests)
        file_path = f.name

    try:
        result = subprocess.run(
            ["python", file_path],
            capture_output=True,
            text=True,
            timeout=timeout
        )

        if result.returncode == 0:
            return {"success": True}
        else:
            return {
                "success": False,
                "error": result.stderr or result.stdout
            }

    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": "Execution timed out"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
