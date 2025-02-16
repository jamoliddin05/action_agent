from fastapi import FastAPI, HTTPException, Body
from fastapi.responses import StreamingResponse
import asyncio
import subprocess

app = FastAPI()


async def stream_command_output(command: str):
    """Run the command and stream its output in real-time."""
    process = await asyncio.create_subprocess_shell(
        command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    async def generator():
        async for line in process.stdout:
            yield line.decode()
        async for line in process.stderr:
            yield line.decode()
        await process.wait()

    return StreamingResponse(generator(), media_type="text/plain")


@app.post("/execute")
async def execute_command(params: dict = Body()):
    command = params.get("command")
    if not command:
        raise HTTPException(status_code=422, detail="No command specified")

    return await stream_command_output(command)
