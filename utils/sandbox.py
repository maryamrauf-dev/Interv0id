import ast
import tempfile
import subprocess
import sys
import os

def run_code_safely(code: str, timeout: int = 5) -> str:
    """
    Safely executes user-provided Python code using subprocess and basic static analysis.
    Prevents importing dangerous modules and using dangerous built-ins.
    """
    forbidden_imports = {'os', 'sys', 'subprocess', 'shutil', 'socket', 'urllib', 'requests'}
    forbidden_calls = {'eval', 'exec', 'open', '__import__', 'getattr', 'setattr', 'vars', 'globals', 'locals'}
    
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return f"SyntaxError: {e}"
        
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.split('.')[0] in forbidden_imports:
                    return f"Security Error: Importing '{alias.name}' is not allowed."
        elif isinstance(node, ast.ImportFrom):
            if node.module and node.module.split('.')[0] in forbidden_imports:
                return f"Security Error: Importing from '{node.module}' is not allowed."
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id in forbidden_calls:
                return f"Security Error: Calling '{node.func.id}' is not allowed."
    
    # Provide minimal environment variables to prevent leaking keys like GROQ_API_KEY
    safe_env = {"PATH": os.environ.get("PATH", "")}
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(code)
        temp_path = f.name
        
    try:
        result = subprocess.run(
            [sys.executable, temp_path],
            capture_output=True,
            text=True,
            timeout=timeout,
            env=safe_env
        )
        output = result.stdout
        if result.stderr:
            output += f"\nErrors:\n{result.stderr}"
        return output if output else "NO code executed or no output generated."
    except subprocess.TimeoutExpired:
        return f"Execution Error: Code timed out after {timeout} seconds."
    except Exception as e:
        return f"Execution Error: {str(e)}"
    finally:
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception:
                pass
