import subprocess
from typing import Optional, Dict, Any
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("ChatGPT")

def run_applescript(script: str) -> Dict[str, Any]:
    """Run an AppleScript and return its output and status."""
    try:
        result = subprocess.run(
            ['osascript', '-e', script],
            capture_output=True,
            text=True,
            check=True
        )
        return {
            "success": True,
            "output": result.stdout.strip()
        }
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.strip()
        help_msg = ""
        
        if "is not allowed to send keystrokes" in error_msg:
            help_msg = (
                "Permission Error: The script needs accessibility permissions.\n"
                "1. Open System Settings > Privacy & Security > Accessibility\n"
                "2. Add and enable your terminal application\n"
                "3. Also check System Settings > Privacy & Security > Automation"
            )
        elif "not allowed to send apple events to" in error_msg.lower():
            help_msg = (
                "Permission Error: The script needs automation permissions.\n"
                "1. Open System Settings > Privacy & Security > Automation\n"
                "2. Enable permissions for your terminal to control 'ChatGPT' and 'System Events'"
            )
        
        return {
            "success": False,
            "error": error_msg,
            "help": help_msg
        }

@mcp.tool()
def ask_chatgpt(prompt: str) -> Dict[str, Any]:
    """
    Send a prompt to ChatGPT macOS app and optionally wait for a response.
    
    Args:
        prompt: The text to send to ChatGPT
    
    Returns:
        Dict containing operation status
    """
    script = f'''
    tell application "ChatGPT"
        activate
        delay 1
        
        tell application "System Events"
            tell process "ChatGPT"
                keystroke "{prompt}"
                delay 0.5
                keystroke return
            end tell
        end tell
    end tell
    '''
    
    result = run_applescript(script)
    
    if result["success"]:
        return {
            "operation": "ask_chatgpt",
            "status": "success",
            "message": result["output"]
        }
    else:
        return {
            "operation": "ask_chatgpt",
            "status": "error",
            "message": result["error"],
            "help": result["help"]
        }

def main():
    """Entry point for the MCP server."""
    mcp.run()

if __name__ == "__main__":
    main() 