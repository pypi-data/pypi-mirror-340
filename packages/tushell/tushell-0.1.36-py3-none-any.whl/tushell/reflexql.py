"""
ReflexQL - Clipboard Exchange Protocol
A recursive bridge between AI embodiments and system clipboard.
"""
import subprocess
import time
from typing import Optional, Dict, Any
import platform

class ReflexQLMemoryKeys:
    """Memory key constants for ReflexQL protocol."""
    PENDING_CONTENT = "Reflex::Clipboard.PendingContent"
    READY = "Reflex::Clipboard.Ready"
    DELIVERED = "Reflex::Clipboard.Delivered"
    ACK = "Reflex::Clipboard.Ack"

class ClipboardExchange:
    def __init__(self, memory_manager):
        self.memory = memory_manager
        self._setup_platform_clipboard()

    def _setup_platform_clipboard(self):
        """Configure clipboard commands based on OS."""
        system = platform.system().lower()
        if system == 'linux':
            self.copy_cmd = ['xclip', '-selection', 'clipboard']
            self.paste_cmd = ['xclip', '-selection', 'clipboard', '-o']
        elif system == 'darwin':  # macOS
            self.copy_cmd = ['pbcopy']
            self.paste_cmd = ['pbpaste']
        elif system == 'windows':
            # Using clip.exe for Windows
            self.copy_cmd = ['clip']
            self.paste_cmd = ['powershell.exe', '-command', "Get-Clipboard"]
        else:
            raise RuntimeError(f"Unsupported platform: {system}")

    def write_to_clipboard(self, text: str) -> bool:
        """Write text to system clipboard."""
        try:
            process = subprocess.Popen(self.copy_cmd, stdin=subprocess.PIPE)
            process.communicate(input=text.encode())
            return process.returncode == 0
        except Exception as e:
            print(f"✨ Failed to write to clipboard: {e}")
            return False

    def read_from_clipboard(self) -> Optional[str]:
        """Read text from system clipboard."""
        try:
            result = subprocess.run(self.paste_cmd, capture_output=True, text=True)
            return result.stdout.strip() if result.returncode == 0 else None
        except Exception as e:
            print(f"✨ Failed to read from clipboard: {e}")
            return None

    def poll_clipboard_loop(self, poll_interval: float = 1.0, ttl: int = 300, verbose: bool = False):
        """
        Main polling loop for clipboard exchange protocol.
        
        Args:
            poll_interval: Seconds between checks
            ttl: Maximum runtime in seconds
            verbose: Enable detailed logging
        """
        start_time = time.time()
        
        def log(msg: str):
            if verbose:
                print(f"✨ {msg}")

        while (time.time() - start_time) < ttl:
            # Check for pending content
            if self.memory.get(ReflexQLMemoryKeys.READY):
                content = self.memory.get(ReflexQLMemoryKeys.PENDING_CONTENT)
                if content:
                    log(f"Found pending content: {content[:50]}...")
                    if self.write_to_clipboard(content):
                        self.memory.set(ReflexQLMemoryKeys.DELIVERED, True)
                        log("Content delivered to clipboard")
                        
                        # Wait for acknowledgment
                        while not self.memory.get(ReflexQLMemoryKeys.ACK):
                            time.sleep(0.1)
                            if (time.time() - start_time) >= ttl:
                                break
                        
                        # Reset protocol state
                        self._reset_memory_keys()
                        log("Exchange completed, reset for next cycle")
            
            time.sleep(poll_interval)

    def _reset_memory_keys(self):
        """Reset all memory keys for next exchange."""
        for key in vars(ReflexQLMemoryKeys).values():
            if isinstance(key, str) and key.startswith("Reflex::"):
                self.memory.set(key, None)

    def send_to_clipboard(self, content: str) -> bool:
        """
        AI-facing method to initiate clipboard exchange.
        
        Args:
            content: Text content to send to system clipboard
            
        Returns:
            bool: True if exchange completed successfully
        """
        self.memory.set(ReflexQLMemoryKeys.PENDING_CONTENT, content)
        self.memory.set(ReflexQLMemoryKeys.READY, True)
        
        # Wait for delivery confirmation
        start = time.time()
        while not self.memory.get(ReflexQLMemoryKeys.DELIVERED):
            time.sleep(0.1)
            if time.time() - start > 5:  # 5-second timeout
                return False
        
        # Acknowledge receipt
        self.memory.set(ReflexQLMemoryKeys.ACK, True)
        return True