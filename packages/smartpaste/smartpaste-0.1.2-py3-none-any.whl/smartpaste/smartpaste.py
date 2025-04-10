import pyperclip
import pyautogui
import time
import sys

def reliable_paste_text(text: str, delay_after_paste: float = 0.1):
    """
    Outputs the given text into the currently focused input field using the
    system clipboard (copy & paste). This is generally the most reliable way
    to handle complex characters like emojis and mixed scripts.

    NOTE: This function pastes the entire text block instantly. It does NOT
    simulate character-by-character typing.

    Args:
        text (str): The text string to output.
        delay_after_paste (float): A small pause (in seconds) after the paste
            command is issued, allowing the target application time to process
            the pasted content. Adjust if pasting large amounts of text or if
            issues occur. Defaults to 0.1.

    Raises:
        ValueError: If delay_after_paste is negative.
        pyperclip.PyperclipException: If clipboard operations fail.
        Exception: Catches potential errors during pyautogui actions.
    """
    if delay_after_paste < 0:
        raise ValueError("delay_after_paste must be non-negative")

    # --- Determine platform-specific paste shortcut ---
    if sys.platform == 'darwin':  # macOS
        modifier_key = 'command'
    else:  # Assume 'ctrl' for Windows and Linux/other
        modifier_key = 'ctrl'
    paste_key = 'v'
    # ---

    original_clipboard_content = None
    clipboard_changed = False

    try:
        # 1. Save current clipboard content (best effort)
        try:
            original_clipboard_content = pyperclip.paste()
        except Exception as e:
            print(f"Warning: Could not read initial clipboard content. {type(e).__name__}: {e}", file=sys.stderr)
            original_clipboard_content = "" # Assume empty if error

        # 2. Copy the desired text to the clipboard
        pyperclip.copy(text)
        clipboard_changed = True
        time.sleep(0.1) # Brief pause to ensure the OS clipboard updates

        # 3. Perform the paste keyboard shortcut
        pyautogui.hotkey(modifier_key, paste_key)

        # 4. Pause after pasting
        if delay_after_paste > 0:
            time.sleep(delay_after_paste)

    except pyperclip.PyperclipException as e:
        print(f"Error: Clipboard operation failed: {e}", file=sys.stderr)
        raise
    except Exception as e:
        print(f"Error: Failed during paste operation: {type(e).__name__}: {e}", file=sys.stderr)
        raise
    finally:
        # 5. Restore original clipboard content (if we saved and changed it)
        if clipboard_changed and original_clipboard_content is not None:
            try:
                time.sleep(0.1) # Brief pause before restoring
                pyperclip.copy(original_clipboard_content)
            except Exception as e:
                print(f"Warning: Could not restore original clipboard content. {type(e).__name__}: {e}", file=sys.stderr)

# ===============================================
#                  Example Usage
# ===============================================
if __name__ == '__main__':
    test_string = "Hello from smartpaste! 😊"

    print("--- Testing reliable_paste_text ---")
    print("Ensure a text input area has focus.")
    print("Pasting in 5 seconds...")
    time.sleep(5)
    print("Pasting now...")
    try:
        reliable_paste_text(test_string, delay_after_paste=0.1)
        print("Pasting complete.")
    except Exception as e:
        print(f"--- ERROR DURING PASTE: {e} ---")

    print("--- Test Finished ---")
