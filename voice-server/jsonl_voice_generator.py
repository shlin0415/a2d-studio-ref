"""
JSONL Voice Generator
Reads dialogue JSONL output and generates voice audio using GPT-SoVITS.
Uses voice_language from JSONL header for TTS language.

Usage:
    python jsonl_voice_generator.py --jsonl output/real_dialogue.jsonl --output output/voice

Requirements:
    - GPT-SoVITS API running (default: http://127.0.0.1:9880)
    - Character-voice-example folder with voice settings
    - httpx: pip install httpx
"""

import argparse
import asyncio
import json
import shutil
import sys
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

try:
    import httpx
except ImportError:
    print("ERROR: httpx not installed. Run: pip install httpx")
    sys.exit(1)


# ============================================================================
# Data Models
# ============================================================================


@dataclass
class VoiceSettings:
    gpt_weight: str
    sovits_weight: str
    default_ref_voice: str
    default_ref_setting: str
    gpt_type1: str
    gpt_type2: str


@dataclass
class RefAudioSettings:
    speak_speed: float
    seconds_between_sentences: float
    top_k: int
    top_p: float
    temperature: float
    wav_file: str
    ref_text: str
    ref_language: str


@dataclass
class DialogueLine:
    index: int
    character: str
    emotion: str
    text: str
    action: str
    caption_text: str
    voice_text: str
    caption_language: str
    voice_language: str


@dataclass
class JsonlHeader:
    characters: List[str]
    topic: str
    dialogue_language: str
    voice_language: str
    line_count: int


# ============================================================================
# Config Parser
# ============================================================================


class ConfigParser:
    @staticmethod
    def parse_config(config_text: str) -> Dict[str, str]:
        config = {}
        for line in config_text.strip().split("\n"):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip()
            if (value.startswith("'") and value.endswith("'")) or (
                value.startswith('"') and value.endswith('"')
            ):
                value = value[1:-1]
            config[key] = value
        return config

    @staticmethod
    def load_voice_settings(path: Path) -> VoiceSettings:
        config = ConfigParser.parse_config(path.read_text(encoding="utf-8"))
        return VoiceSettings(
            gpt_weight=config["GPT_WEIGHT"],
            sovits_weight=config["SoVITS_WEIGHT"],
            default_ref_voice=config["DEFAULT_REF_VOICE"],
            default_ref_setting=config["DEFAULT_REF_SETTING"],
            gpt_type1=config["GPT_SOVITS_TYPE1"],
            gpt_type2=config["GPT_SOVITS_TYPE2"],
        )

    @staticmethod
    def load_ref_audio_settings(path: Path) -> RefAudioSettings:
        config = ConfigParser.parse_config(path.read_text(encoding="utf-8"))
        return RefAudioSettings(
            speak_speed=float(config["SPEAK_SPEED"]),
            seconds_between_sentences=float(config["SECONDS_BETWEEN_SENTENCES"]),
            top_k=int(config["TOP_K"]),
            top_p=float(config["TOP_P"]),
            temperature=float(config["TEMPERATURE"]),
            wav_file=config["WAV_FILE"],
            ref_text=config["REF_TEXT"],
            ref_language=config["REF_LANGUAGE"],
        )


# ============================================================================
# GPT-SoVITS Client
# ============================================================================


class GPTSoVITSClient:
    def __init__(self, api_url: str = "http://127.0.0.1:9880"):
        self.api_url = api_url
        self.client = httpx.AsyncClient(timeout=120.0)

    async def close(self):
        await self.client.aclose()

    async def health_check(self) -> bool:
        try:
            response = await self.client.get(
                f"{self.api_url}/docs", follow_redirects=True
            )
            return response.status_code == 200
        except Exception as e:
            print(f"[ERROR] Health check failed: {e}")
            return False

    async def set_gpt_weights(self, model_path: str) -> bool:
        try:
            response = await self.client.get(
                f"{self.api_url}/set_gpt_weights",
                params={"weights_path": str(model_path)},
            )
            if response.status_code == 200:
                return True
            print(f"[ERROR] Failed to load GPT model: {response.text}")
            return False
        except Exception as e:
            print(f"[ERROR] GPT weights: {e}")
            return False

    async def set_sovits_weights(self, model_path: str) -> bool:
        try:
            response = await self.client.get(
                f"{self.api_url}/set_sovits_weights",
                params={"weights_path": str(model_path)},
            )
            if response.status_code == 200:
                return True
            print(f"[ERROR] Failed to load SoVITS model: {response.text}")
            return False
        except Exception as e:
            print(f"[ERROR] SoVITS weights: {e}")
            return False

    async def generate_voice(
        self,
        text: str,
        ref_audio_path: str,
        ref_text: str,
        ref_language: str,
        text_language: str,
        speed_factor: float = 1.0,
        top_k: int = 5,
        top_p: float = 1.0,
        temperature: float = 1.0,
    ) -> Optional[bytes]:
        try:
            valid_langs = ["ja", "zh", "en", "yue", "ko"]
            ref_lang_code = (
                ref_language.lower() if ref_language.lower() in valid_langs else "auto"
            )
            text_lang_code = (
                text_language.lower()
                if text_language.lower() in valid_langs
                else "auto"
            )

            payload = {
                "text": text,
                "text_lang": text_lang_code,
                "ref_audio_path": str(ref_audio_path),
                "prompt_text": ref_text,
                "prompt_lang": ref_lang_code,
                "speed_factor": speed_factor,
                "top_k": top_k,
                "top_p": top_p,
                "temperature": temperature,
                "text_split_method": "cut5",
                "media_type": "wav",
            }

            response = await self.client.post(f"{self.api_url}/tts", json=payload)

            if response.status_code == 200:
                return response.content
            print(f"[ERROR] TTS failed: {response.text}")
            return None
        except Exception as e:
            print(f"[ERROR] Voice generation: {e}")
            return None


# ============================================================================
# Character Voice Loader
# ============================================================================


class CharacterVoiceLoader:
    """Load voice settings for a character from Character-voice-example/"""

    def __init__(self, voice_example_dir: Path):
        self.voice_example_dir = voice_example_dir
        self._cache: Dict[
            str, Tuple[VoiceSettings, RefAudioSettings, Path, Path, Path]
        ] = {}

    def load(
        self, character_name: str
    ) -> Optional[Tuple[VoiceSettings, RefAudioSettings, Path, Path, Path]]:
        """
        Load voice settings for a character.

        Returns: (voice_settings, ref_audio_settings, gpt_model_path, sovits_model_path, ref_audio_path)
        """
        if character_name in self._cache:
            return self._cache[character_name]

        char_dir = self.voice_example_dir / character_name
        gpt_dir = char_dir / "GPT-SoVITS"

        if not gpt_dir.exists():
            print(f"[WARN] Voice settings not found for: {character_name}")
            return None

        try:
            voice_settings = ConfigParser.load_voice_settings(
                gpt_dir / "voice_setting.txt"
            )

            ref_setting_path = gpt_dir / voice_settings.default_ref_setting.lstrip("./")
            ref_audio_settings = ConfigParser.load_ref_audio_settings(ref_setting_path)

            gpt_model_path = gpt_dir / voice_settings.gpt_weight
            sovits_model_path = gpt_dir / voice_settings.sovits_weight
            ref_audio_path = gpt_dir / voice_settings.default_ref_voice.lstrip("./")

            result = (
                voice_settings,
                ref_audio_settings,
                gpt_model_path,
                sovits_model_path,
                ref_audio_path,
            )
            self._cache[character_name] = result
            return result
        except Exception as e:
            print(f"[ERROR] Failed to load voice settings for {character_name}: {e}")
            return None


# ============================================================================
# JSONL Parser
# ============================================================================


def parse_jsonl(jsonl_path: Path) -> Tuple[JsonlHeader, List[DialogueLine]]:
    """Parse JSONL file into header and dialogue lines"""
    lines = jsonl_path.read_text(encoding="utf-8").strip().split("\n")

    # First line is header
    header_raw = json.loads(lines[0])["header"]
    header = JsonlHeader(
        characters=header_raw.get("characters", []),
        topic=header_raw.get("topic", ""),
        dialogue_language=header_raw.get("dialogue_language", "zh"),
        voice_language=header_raw.get("voice_language", "zh"),
        line_count=header_raw.get("line_count", len(lines) - 1),
    )

    # Remaining lines are dialogue
    dialogue_lines = []
    for line_str in lines[1:]:
        d = json.loads(line_str)
        dialogue_lines.append(
            DialogueLine(
                index=d.get("index", 0),
                character=d.get("character", ""),
                emotion=d.get("emotion", ""),
                text=d.get("text", ""),
                action=d.get("action", ""),
                caption_text=d.get("caption_text", d.get("text", "")),
                voice_text=d.get("voice_text", d.get("text", "")),
                caption_language=d.get("caption_language", header.dialogue_language),
                voice_language=d.get("voice_language", header.voice_language),
            )
        )

    return header, dialogue_lines


# ============================================================================
# Main Voice Generator
# ============================================================================


class JsonlVoiceGenerator:
    """Generate voice audio from JSONL dialogue file"""

    def __init__(
        self,
        api_url: str = "http://127.0.0.1:9880",
        voice_example_dir: Optional[Path] = None,
    ):
        self.client = GPTSoVITSClient(api_url=api_url)
        base_dir = Path(__file__).parent.parent
        self.voice_loader = CharacterVoiceLoader(
            voice_example_dir or base_dir / "Character-voice-example"
        )

    async def generate_from_jsonl(
        self,
        jsonl_path: Path,
        output_dir: Path,
        clean_output: bool = False,
    ) -> Dict:
        """
        Generate voice audio from a JSONL file.

        Args:
            jsonl_path: Path to dialogue JSONL file
            output_dir: Output directory for audio files
            clean_output: If True, clean output dir before generating

        Returns:
            Dict with generation results
        """
        print(f"\n{'=' * 60}")
        print(f"JSONL Voice Generator")
        print(f"{'=' * 60}")
        print(f"Input:  {jsonl_path}")
        print(f"Output: {output_dir}")

        # Check API
        print(f"\nChecking GPT-SoVITS API...")
        if not await self.client.health_check():
            print("[ERROR] Cannot connect to GPT-SoVITS API")
            return {"success": False, "error": "API not available"}
        print("[OK] API is running")

        # Parse JSONL
        header, dialogue_lines = parse_jsonl(jsonl_path)
        print(f"\nTopic: {header.topic}")
        print(f"Dialogue language: {header.dialogue_language}")
        print(f"Voice language: {header.voice_language}")
        print(f"Lines: {len(dialogue_lines)}")

        # Setup output
        if clean_output and output_dir.exists():
            shutil.rmtree(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        # Track loaded models to avoid reloading
        current_character = None
        results = {"success": True, "generated": 0, "failed": 0, "skipped": 0}

        for line in dialogue_lines:
            char_name = line.character
            print(f"\n--- Line {line.index}: {char_name} ---")
            print(f"  Voice text: {line.voice_text[:60]}...")
            print(f"  Voice lang: {line.voice_language}")

            # Load voice settings
            voice_data = self.voice_loader.load(char_name)
            if voice_data is None:
                print(f"  [SKIP] No voice settings for {char_name}")
                results["skipped"] += 1
                continue

            (
                voice_settings,
                ref_audio_settings,
                gpt_model_path,
                sovits_model_path,
                ref_audio_path,
            ) = voice_data

            # Load models (only if character changed)
            if current_character != char_name:
                print(f"  Loading models for {char_name}...")
                gpt_ok = await self.client.set_gpt_weights(str(gpt_model_path))
                sovits_ok = await self.client.set_sovits_weights(str(sovits_model_path))
                if not (gpt_ok and sovits_ok):
                    print(f"  [ERROR] Failed to load models for {char_name}")
                    results["failed"] += 1
                    continue
                current_character = char_name
                print(f"  [OK] Models loaded")

            # Generate voice
            char_output_dir = output_dir / char_name
            char_output_dir.mkdir(parents=True, exist_ok=True)
            output_filename = f"{line.index:04d}.wav"
            output_path = char_output_dir / output_filename

            audio_bytes = await self.client.generate_voice(
                text=line.voice_text,
                ref_audio_path=str(ref_audio_path),
                ref_text=ref_audio_settings.ref_text,
                ref_language=ref_audio_settings.ref_language,
                text_language=line.voice_language,
                speed_factor=ref_audio_settings.speak_speed,
                top_k=ref_audio_settings.top_k,
                top_p=ref_audio_settings.top_p,
                temperature=ref_audio_settings.temperature,
            )

            if audio_bytes:
                output_path.write_bytes(audio_bytes)
                size_kb = len(audio_bytes) / 1024
                print(f"  [OK] Saved: {output_filename} ({size_kb:.1f} KB)")
                results["generated"] += 1
            else:
                print(f"  [FAIL] Voice generation failed")
                results["failed"] += 1

        await self.client.close()

        print(f"\n{'=' * 60}")
        print(
            f"Results: {results['generated']} generated, {results['failed']} failed, {results['skipped']} skipped"
        )
        print(f"{'=' * 60}")

        return results


# ============================================================================
# CLI Entry Point
# ============================================================================


async def main():
    parser = argparse.ArgumentParser(description="Generate voice from dialogue JSONL")
    parser.add_argument("--jsonl", required=True, help="Path to dialogue JSONL file")
    parser.add_argument("--output", default=None, help="Output directory for audio")
    parser.add_argument(
        "--api-url", default="http://127.0.0.1:9880", help="GPT-SoVITS API URL"
    )
    parser.add_argument(
        "--clean", action="store_true", help="Clean output directory before generating"
    )
    parser.add_argument(
        "--voice-dir", default=None, help="Path to Character-voice-example directory"
    )

    args = parser.parse_args()

    jsonl_path = Path(args.jsonl)
    if not jsonl_path.exists():
        print(f"ERROR: JSONL file not found: {jsonl_path}")
        sys.exit(1)

    output_dir = Path(args.output) if args.output else jsonl_path.parent / "voice"
    voice_dir = Path(args.voice_dir) if args.voice_dir else None

    generator = JsonlVoiceGenerator(
        api_url=args.api_url,
        voice_example_dir=voice_dir,
    )

    result = await generator.generate_from_jsonl(
        jsonl_path=jsonl_path,
        output_dir=output_dir,
        clean_output=args.clean,
    )

    if not result["success"]:
        sys.exit(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nInterrupted")
        sys.exit(130)
