from fastapi import FastAPI, HTTPException, Body
import subprocess

app = FastAPI()

@app.post("/execute")
async def execute_command(params: dict = Body()):
    command = params.get("command")
    if command is None:
        raise HTTPException(status_code=422, detail="No command specified")

    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        output = result.stdout if result.returncode == 0 else result.stderr  # Prioritize stderr on failure
        return {"output": output.strip(), "return_code": result.returncode}
    except Exception as e:
        return {"output": str(e), "return_code": 1}  # Return errors under "output"
