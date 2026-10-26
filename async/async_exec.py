import asyncio
import sys
import subprocess

async def run_command(argv: list[str]) -> dict:
    proc = await asyncio.create_subprocess_exec(
        *argv,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    stdout, stderr = await proc.communicate()

    ret_out = stdout.decode('utf-8', errors='replace')
    ret_err = stderr.decode('utf-8', errors='replace')

    status = "success" if proc.returncode == 0 else "failed"
    print ({
        "status" : status,
        "returncode" : proc.returncode,
        "stdout" : ret_out,
        "stderr" : ret_err
    })

    return {
        "status" : status,
        "returncode" : proc.returncode,
        "stdout" : ret_out,
        "stderr" : ret_err
    }




async def main():
    py = sys.executable

    success = await run_command([
        py, "-c", "print('hello')"
    ])


    assert success == {
        "status": "ok",
        "returncode": 0,
        "stdout": "hello\n",
        "stderr": ""
    }


    failure = await run_command([
        py, "-c",
        "import sys; print('error', file=sys.stderr); sys.exit(7)"
    ])

    assert failure == {
        "status": "failed",
        "returncode": 7,
        "stdout": "",
        "stderr": "error\n"
    }


    print("ALL TESTS PASSED")

asyncio.run(main())