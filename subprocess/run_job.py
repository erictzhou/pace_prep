import subprocess
import sys

def run_job(command: list[str], timeout: float) -> dict:

    stdout = ""
    stderr = ""
    returncode = 0
    status = "success"
    try:
        result = subprocess.run(command,
                       check=True,
                       text=True,
                       timeout=timeout,
                       capture_output=True)
        stdout = result.stdout
        stderr = result.stderr
        returncode = result.returncode
    except subprocess.TimeoutExpired:
        returncode = None
        status = "timeout"
    except subprocess.CalledProcessError as exc:
        status = "failed"
        returncode = exc.returncode
        stdout = exc.stdout
        stderr = exc.stderr

    return {
        "status" : status,
        "returncode" : returncode,
        "stdout" : stdout,
        "stderr" : stderr
    }

print(run_job(
    ["python", "-c", "print('hello')"],
    timeout=2
))

print(run_job(
    ["python", "-c", "import sys; sys.exit(2)"],
    timeout=2
))

print(run_job(
    ["python", "-c", "import time; time.sleep(10)"],
    timeout=1
))

assert run_job(["ls", ".."], 2)["stdout"].strip() \
    == "python_fundamentals\nsubprocess"
assert run_job([sys.executable, "script.py"], 2)["returncode"] \
    == 3

assert run_job([sys.executable, "slept.py"], 0.02)["returncode"] \
    == None

try:
    result = run_job(["doesn't exit", "hi 2 3"], 0.02)["status"].strip()
    raise AssertionError("Expected FileNotFoundError")
except FileNotFoundError:
    pass