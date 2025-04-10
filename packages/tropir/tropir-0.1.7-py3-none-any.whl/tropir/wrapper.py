"""
Wrapper module for patching OpenAI API calls.
"""

import functools
import time
import traceback
import json
import uuid
import os
import inspect
from datetime import datetime
from typing import Any, Dict, List

from .transport import send_log
from .config import get_config


def format_stack_trace(stack_frames):
    """Format stack trace frames into a structured format with detailed information.
    
    Args:
        stack_frames: Stack frames from traceback.extract_stack()
        
    Returns:
        Formatted stack trace as a string with each frame containing detailed information
    """
    formatted_frames = []
    current_dir = os.getcwd()

    # Process each frame
    for frame in stack_frames:
        # Skip tropir internal frames for clarity
        if isinstance(frame, traceback.FrameSummary) and 'site-packages/tropir' in frame.filename:
            continue

        # Basic frame information
        if isinstance(frame, traceback.FrameSummary):
            # Extract the frame data
            frame_data = {
                "file": frame.filename,
                "line": frame.lineno,
                "function": frame.name,
                "code": frame.line.strip() if frame.line else "",
                "relative_path": os.path.relpath(frame.filename, current_dir) if os.path.isabs(frame.filename) else frame.filename
            }
            
            # Format nicely for display
            frame_str = f"File \"{frame_data['relative_path']}\", line {frame_data['line']}, in {frame_data['function']}\n"
            if frame_data['code']:
                frame_str += f"  {frame_data['code']}\n"
            
            formatted_frames.append(frame_str)
        else:
            # Handle string frames (from format_stack)
            frame_str = frame.strip()
            if frame_str:
                formatted_frames.append(frame_str)
    
    return "\n".join(formatted_frames)


def patch_openai():
    """Set up tracking for OpenAI by patching the ChatCompletion.create method."""
    try:
        # Import the specific class where the 'create' method resides
        from openai.resources.chat.completions import Completions as OpenAICompletions

        # Check if the 'create' method exists and hasn't been patched yet
        if hasattr(OpenAICompletions, "create") and not getattr(OpenAICompletions.create, '_tropir_patched', False):
            original_create_method = OpenAICompletions.create  # Get the original function

            # Create the wrapped version
            patched_create = create_wrapper(original_create_method)

            # Replace the original method on the class with the patched one
            OpenAICompletions.create = patched_create
            print("Successfully patched OpenAI API")
        elif hasattr(OpenAICompletions, "create") and getattr(OpenAICompletions.create, '_tropir_patched', False):
            print("OpenAI Completions.create already patched.")

    except ImportError:
        print("Could not import 'openai.resources.chat.completions'. OpenAI tracking may not work.")
    except Exception as e:
        print(f"Failed during OpenAI patching process: {e}")


def process_messages(messages):
    """Process OpenAI messages to handle special content types"""
    processed_messages = []
    for msg in messages:
        if isinstance(msg, dict) or hasattr(msg, "keys"):
            # Convert frozendict to dict if needed
            msg_dict = dict(msg) if not isinstance(msg, dict) else msg
            processed_msg = msg_dict.copy()
            content = msg_dict.get("content")

            # Handle list-type content (multimodal messages)
            if isinstance(content, list):
                processed_content = []
                for item in content:
                    if isinstance(item, dict):
                        item_copy = item.copy()
                        # Handle image types in OpenAI messages
                        if "image_url" in item_copy:
                            url = item_copy["image_url"].get("url", "")
                            if url and url.startswith("data:image"):
                                item_copy["image_url"]["url"] = "[BASE64_IMAGE_REMOVED]"
                        processed_content.append(item_copy)
                    else:
                        processed_content.append(item)
                processed_msg["content"] = processed_content
            elif isinstance(content, str):
                # Strip leading and trailing newlines from string content
                processed_msg["content"] = content.strip('\n')

            processed_messages.append(processed_msg)
        else:
            # Handle non-dict message objects
            try:
                # For OpenAI message objects
                content = getattr(msg, "content", str(msg))
                if isinstance(content, str):
                    content = content.strip('\n')
                
                processed_msg = {
                    "role": getattr(msg, "role", "unknown"),
                    "content": content
                }
                processed_messages.append(processed_msg)
            except Exception:
                # If all else fails, create a basic message
                processed_messages.append({
                    "role": getattr(msg, "role", "unknown"),
                    "content": str(getattr(msg, "content", str(msg)))
                })

    return processed_messages


def create_wrapper(original_method):
    """Create a wrapper for the OpenAI ChatCompletion.create method."""
    @functools.wraps(original_method)
    def wrapped_method(*args, **kwargs):
        config = get_config()
        if not config["enabled"]:
            return original_method(*args, **kwargs)

        start_time = time.perf_counter()
        success = True
        response = None
        
        # Capture stack trace before calling the original method
        # Skip this wrapper frame and only show user code
        stack_frames = traceback.extract_stack()[:-1]  # Remove the last frame (this wrapper)
        stack_trace = format_stack_trace(stack_frames)
        
        try:
            # Call the original method
            response = original_method(*args, **kwargs)
            return response
        except Exception as e:
            success = False
            raise
        finally:
            if config["enabled"]:
                duration = time.perf_counter() - start_time
                try:
                    # Process messages
                    processed_messages = process_messages(kwargs.get("messages", []))
                    
                    # Extract usage information
                    usage = {}
                    if hasattr(response, "usage"):
                        if hasattr(response.usage, "model_dump"):
                            usage = response.usage.model_dump()
                        else:
                            try:
                                usage = vars(response.usage)
                            except:
                                usage = {}
                    
                    # Standardize usage structure
                    standardized_usage = {
                        "prompt_tokens": usage.get("prompt_tokens", 0),
                        "completion_tokens": usage.get("completion_tokens", 0),
                        "total_tokens": usage.get("total_tokens", 0)
                    }
                    
                    # Extract response text
                    response_text = ""
                    if hasattr(response, "choices") and response.choices:
                        if hasattr(response.choices[0], "message") and response.choices[0].message:
                            if hasattr(response.choices[0].message, "content") and response.choices[0].message.content:
                                response_text = response.choices[0].message.content
                    
                    # Prepare log data
                    log_data = {
                        "log_id": str(uuid.uuid4()),
                        "timestamp": datetime.utcnow().isoformat(),
                        "provider": "openai",
                        "request": {
                            "model": kwargs.get("model", "unknown"),
                            "messages": processed_messages,
                            "temperature": kwargs.get("temperature"),
                            "max_tokens": kwargs.get("max_tokens"),
                            "top_p": kwargs.get("top_p"),
                            "frequency_penalty": kwargs.get("frequency_penalty"),
                            "presence_penalty": kwargs.get("presence_penalty"),
                            "stop": kwargs.get("stop"),
                        },
                        "response": response_text,
                        "usage": standardized_usage,
                        "duration": duration,
                        "success": success,
                        "stack_trace": stack_trace
                    }
                    
                    # Send the log
                    send_log(log_data)
                except Exception as e:
                    print(f"[TROPIR ERROR] Error during logging: {e}")
    
    # Mark the patched function so we don't patch it again
    wrapped_method._tropir_patched = True
    return wrapped_method 