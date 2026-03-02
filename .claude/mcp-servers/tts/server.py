"""Text-to-Speech MCP Server using edge-tts.

Provides speech synthesis with 300+ voices via Microsoft Edge TTS.
Requires: pip install edge-tts
"""

from mcp.server.fastmcp import FastMCP
import subprocess
import tempfile
import os

mcp = FastMCP("Text-to-Speech")

DEFAULT_VOICE = "en-US-GuyNeural"


@mcp.tool()
def speak(text: str, voice: str = DEFAULT_VOICE) -> str:
    """Speak text aloud. Generates audio and plays it via the default media player."""
    try:
        tmp = os.path.join(tempfile.gettempdir(), "claude_tts_output.mp3")
        result = subprocess.run(
            ["edge-tts", "--voice", voice, "--text", text, "--write-media", tmp],
            capture_output=True, text=True, timeout=30,
        )
        if result.returncode != 0:
            return f"Error generating speech: {result.stderr}"
        if not os.path.exists(tmp):
            return "Error: audio file not created"
        # Play via default media player (non-blocking)
        subprocess.Popen(
            ["cmd", "/c", "start", "/min", "", tmp],
            creationflags=subprocess.CREATE_NO_WINDOW,
        )
        preview = text[:80] + "..." if len(text) > 80 else text
        return f"Speaking: '{preview}' with voice {voice}"
    except Exception as e:
        return f"Error: {e}"


@mcp.tool()
def save_speech(text: str, output_path: str, voice: str = DEFAULT_VOICE) -> str:
    """Save text-to-speech audio to an MP3 file."""
    try:
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        result = subprocess.run(
            ["edge-tts", "--voice", voice, "--text", text, "--write-media", output_path],
            capture_output=True, text=True, timeout=60,
        )
        if result.returncode != 0:
            return f"Error: {result.stderr}"
        size_kb = os.path.getsize(output_path) / 1024
        return f"Saved speech to {output_path} ({size_kb:.1f} KB)"
    except Exception as e:
        return f"Error: {e}"


@mcp.tool()
def list_voices(language: str = "en") -> str:
    """List available TTS voices. Filter by language code (e.g. 'en', 'hi', 'ja')."""
    try:
        result = subprocess.run(
            ["edge-tts", "--list-voices"],
            capture_output=True, text=True, timeout=15,
        )
        if result.returncode != 0:
            return f"Error: {result.stderr}"
        lines = result.stdout.strip().split("\n")
        if language:
            filtered = []
            current_block = []
            for line in lines:
                if line.startswith("Name:"):
                    if current_block and any(language.lower() in l.lower() for l in current_block):
                        filtered.extend(current_block)
                        filtered.append("")
                    current_block = [line]
                else:
                    current_block.append(line)
            if current_block and any(language.lower() in l.lower() for l in current_block):
                filtered.extend(current_block)
            return "\n".join(filtered[:100]) if filtered else f"No voices found for language '{language}'"
        return "\n".join(lines[:100])
    except Exception as e:
        return f"Error: {e}"


@mcp.tool()
def get_voice_info(voice_name: str) -> str:
    """Get info about a specific voice by name (e.g. 'en-US-GuyNeural')."""
    try:
        result = subprocess.run(
            ["edge-tts", "--list-voices"],
            capture_output=True, text=True, timeout=15,
        )
        lines = result.stdout.strip().split("\n")
        found = []
        capturing = False
        for line in lines:
            if line.startswith("Name:") and voice_name.lower() in line.lower():
                capturing = True
                found.append(line)
            elif capturing:
                if line.startswith("Name:"):
                    break
                found.append(line)
        return "\n".join(found) if found else f"Voice '{voice_name}' not found"
    except Exception as e:
        return f"Error: {e}"


if __name__ == "__main__":
    mcp.run()
