import traceback
import tempfile
import subprocess
import sys


class PythonREPL:
    def run(self, code: str, tests: str):
        """
        执行 code + tests，返回 (success, output)
        """
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".py", delete=False, encoding="utf-8"
        ) as f:
            f.write(code + "\n\n" + tests)
            path = f.name

        try:
            result = subprocess.run(
                [sys.executable, path],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result.returncode == 0:
                return True, result.stdout
            else:
                return False, result.stderr
        except Exception:
            return False, traceback.format_exc()
