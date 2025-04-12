import atexit
import os
import signal
import subprocess
import sys

from jemma.model.modelInteraction import modelInteraction
from jemma.utils.terminalPrettifier import responseFormatter, warningText
 

def watchCommand(functionToRun: str, directoryStructure: str, codeContent: str):
   if not isinstance(functionToRun, str) or len(functionToRun.strip()) < 2:
        print(warningText("Please provide a valid command for Jemma to watch (minimum 2 characters)"))
        return None
   print(warningText(f'Jemma is watching {functionToRun}'))
   result = subprocess.run(
                functionToRun.strip(),
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )
  
   model_prompt = f"""
        Analyze this command execution context:
        Codebase Structure: {directoryStructure}
        Code Content: {codeContent}
        Executed Command: {functionToRun}
        Command Output: {result.stdout}
        Exit Code: {result.returncode}
        
        Provide concise user-facing analysis of potential issues and suggestions.
        """
   model_response = responseFormatter( modelInteraction(model_prompt))
   print(model_response)