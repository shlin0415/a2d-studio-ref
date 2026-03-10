"""
Test: Single Port Bottleneck (Model Switching)
================================================

Tests the time cost when using a single GPT-SoVITS port (9880) with model switching.

Scenario:
- 2 characters (Ema, Hiro) with different models
- 10 dialogue turns (alternating characters)
- Each turn requires loading new models

Usage:
    python test_single_port_bottleneck.py

Requirements:
    - GPT-SoVITS API running at http://127.0.0.1:9880
    - Character-voice-example folder with voice settings
"""

import asyncio
import json
import time
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional
import sys

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
    """Settings from voice_setting.txt"""

    gpt_weight: str
    sovits_weight: str
    default_ref_voice: str
    default_ref_setting: str
    gpt_type1: str
    gpt_type2: str


@dataclass
class RefAudioSettings:
    """Settings from reference audio config file"""

    speak_speed: float
    seconds_between_sentences: float
    top_k: int
    top_p: float
    temperature: float
    wav_file: str
    ref_text: str
    ref_language: str


@dataclass
class TimingResult:
    """Timing result for a single operation"""

    operation: str
    duration_seconds: float


@dataclass
class TurnResult:
    """Timing result for a single dialogue turn"""

    turn_index: int
    character: str
    text: str
    model_load_time: float
    generation_time: float
    total_time: float


# ============================================================================
# Configuration Parser
# ============================================================================


class ConfigParser:
    """Parse voice configuration files with key='value' format"""

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
    def load_voice_settings(voice_setting_path: Path) -> VoiceSettings:
        if not voice_setting_path.exists():
            raise FileNotFoundError(f"Voice settings not found: {voice_setting_path}")

        config = ConfigParser.parse_config(
            voice_setting_path.read_text(encoding="utf-8")
        )

        return VoiceSettings(
            gpt_weight=config["GPT_WEIGHT"],
            sovits_weight=config["SoVITS_WEIGHT"],
            default_ref_voice=config["DEFAULT_REF_VOICE"],
            default_ref_setting=config["DEFAULT_REF_SETTING"],
            gpt_type1=config["GPT_SOVITS_TYPE1"],
            gpt_type2=config["GPT_SOVITS_TYPE2"],
        )

    @staticmethod
    def load_ref_audio_settings(ref_setting_path: Path) -> RefAudioSettings:
        if not ref_setting_path.exists():
            raise FileNotFoundError(f"Reference settings not found: {ref_setting_path}")

        config = ConfigParser.parse_config(ref_setting_path.read_text(encoding="utf-8"))

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
# GPT-SoVITS API Client
# ============================================================================


class GPTSoVITSClient:
    """Async HTTP client for GPT-SoVITS API"""

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
        except Exception:
            return False

    async def set_gpt_weights(self, model_path: str) -> float:
        """Load GPT model weights and return time taken"""
        start_time = time.perf_counter()
        try:
            response = await self.client.get(
                f"{self.api_url}/set_gpt_weights",
                params={"weights_path": str(model_path)},
            )
            elapsed = time.perf_counter() - start_time
            if response.status_code == 200:
                return elapsed
            else:
                raise Exception(f"Failed to load GPT: {response.text}")
        except Exception as e:
            raise Exception(f"Error setting GPT weights: {e}")

    async def set_sovits_weights(self, model_path: str) -> float:
        """Load SoVITS model weights and return time taken"""
        start_time = time.perf_counter()
        try:
            response = await self.client.get(
                f"{self.api_url}/set_sovits_weights",
                params={"weights_path": str(model_path)},
            )
            elapsed = time.perf_counter() - start_time
            if response.status_code == 200:
                return elapsed
            else:
                raise Exception(f"Failed to load SoVITS: {response.text}")
        except Exception as e:
            raise Exception(f"Error setting SoVITS weights: {e}")

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
    ) -> tuple[Optional[bytes], float]:
        """
        Generate speech from text and return (audio_bytes, time_taken)
        """
        start_time = time.perf_counter()
        try:
            ref_lang_code = (
                ref_language.lower()
                if ref_language.lower() in ["ja", "zh", "en", "yue", "ko"]
                else "auto"
            )
            text_lang_code = (
                text_language.lower()
                if text_language.lower() in ["ja", "zh", "en", "yue", "ko"]
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

            elapsed = time.perf_counter() - start_time

            if response.status_code == 200:
                return response.content, elapsed
            else:
                raise Exception(f"TTS failed: {response.text}")

        except Exception as e:
            raise Exception(f"Error generating voice: {e}")


# ============================================================================
# Character Voice Manager
# ============================================================================


class CharacterVoiceManager:
    """Manage character voice generation"""

    def __init__(self, character_name: str, character_folder: Path):
        self.character_name = character_name
        self.character_folder = character_folder
        self.gpt_sovits_folder = character_folder / "GPT-SoVITS"

        self.voice_settings = ConfigParser.load_voice_settings(
            self.gpt_sovits_folder / "voice_setting.txt"
        )

        ref_setting_path = (
            self.gpt_sovits_folder
            / self.voice_settings.default_ref_setting.lstrip("./")
        )
        self.ref_audio_settings = ConfigParser.load_ref_audio_settings(ref_setting_path)

        self.gpt_model_path = self.gpt_sovits_folder / self.voice_settings.gpt_weight
        self.sovits_model_path = (
            self.gpt_sovits_folder / self.voice_settings.sovits_weight
        )
        self.ref_audio_path = (
            self.gpt_sovits_folder / self.voice_settings.default_ref_voice.lstrip("./")
        )


# ============================================================================
# Test Runner
# ============================================================================


async def run_single_port_test(
    dialogue_lines: List[dict],
    ema_manager: CharacterVoiceManager,
    hiro_manager: CharacterVoiceManager,
    output_path: Path,
) -> dict:
    """Run test using single port with model switching"""

    client = GPTSoVITSClient(api_url="http://127.0.0.1:9880")

    print("\n" + "=" * 70)
    print("SINGLE PORT TEST (Model Switching)")
    print("=" * 70)
    print(f"Port: 9880")
    print(f"Dialogue turns: {len(dialogue_lines)}")
    print("=" * 70)

    results = []
    total_model_load_time = 0
    total_generation_time = 0

    # Track current model to avoid redundant loads
    current_gpt = None
    current_sovits = None

    for i, line in enumerate(dialogue_lines):
        character = line.get("character", "")
        text = line.get("text", "")

        # Determine which character
        if character == "艾玛":
            manager = ema_manager
            char_key = "ema"
        else:
            manager = hiro_manager
            char_key = "hiro"

        turn_result = TurnResult(
            turn_index=i,
            character=char_key,
            text=text[:30] + "..." if len(text) > 30 else text,
            model_load_time=0,
            generation_time=0,
            total_time=0,
        )

        print(f"\n--- Turn {i + 1}: {char_key} ---")
        print(f"Text: {text[:40]}...")

        # Model loading (only if different from current)
        model_load_time = 0

        if str(manager.gpt_model_path) != current_gpt:
            print(f"  Loading GPT: {manager.gpt_model_path.name}...")
            gpt_time = await client.set_gpt_weights(str(manager.gpt_model_path))
            current_gpt = str(manager.gpt_model_path)
            model_load_time += gpt_time
            print(f"    GPT loaded in {gpt_time:.2f}s")

        if str(manager.sovits_model_path) != current_sovits:
            print(f"  Loading SoVITS: {manager.sovits_model_path.name}...")
            sovits_time = await client.set_sovits_weights(
                str(manager.sovits_model_path)
            )
            current_sovits = str(manager.sovits_model_path)
            model_load_time += sovits_time
            print(f"    SoVITS loaded in {sovits_time:.2f}s")

        if model_load_time == 0:
            print(f"  Models already loaded (skipped)")

        turn_result.model_load_time = model_load_time

        # Generate voice
        print(f"  Generating voice...")
        audio_bytes, gen_time = await client.generate_voice(
            text=text,
            ref_audio_path=str(manager.ref_audio_path),
            ref_text=manager.ref_audio_settings.ref_text,
            ref_language=manager.ref_audio_settings.ref_language,
            text_language="zh",
            speed_factor=manager.ref_audio_settings.speak_speed,
            top_k=manager.ref_audio_settings.top_k,
            top_p=manager.ref_audio_settings.top_p,
            temperature=manager.ref_audio_settings.temperature,
        )

        turn_result.generation_time = gen_time
        turn_result.total_time = model_load_time + gen_time

        total_model_load_time += model_load_time
        total_generation_time += gen_time

        print(f"    Generated in {gen_time:.2f}s")
        print(f"    Total: {turn_result.total_time:.2f}s")

        results.append(asdict(turn_result))

    await client.close()

    # Calculate summary
    num_turns = len(dialogue_lines)
    summary = {
        "test_type": "single_port_model_switching",
        "port": 9880,
        "num_turns": num_turns,
        "total_time": sum(r["total_time"] for r in results),
        "avg_model_load_time": total_model_load_time / num_turns,
        "avg_generation_time": total_generation_time / num_turns,
        "avg_total_time": sum(r["total_time"] for r in results) / num_turns,
        "total_model_load_time": total_model_load_time,
        "total_generation_time": total_generation_time,
    }

    output = {"summary": summary, "turns": results}

    # Save to file
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    return output


# ============================================================================
# Main
# ============================================================================


async def main():
    # Setup paths
    base_dir = Path(__file__).parent.parent
    character_voice_example = base_dir / "Character-voice-example"
    output_dir = Path(__file__).parent / "output"

    # Load dialogue from real_dialogue.jsonl
    dialogue_path = base_dir / "dialogue-server" / "output" / "real_dialogue.jsonl"

    if not dialogue_path.exists():
        print(f"ERROR: Dialogue file not found: {dialogue_path}")
        print("Please run Phase 2 first to generate real_dialogue.jsonl")
        sys.exit(1)

    # Parse dialogue lines (skip header)
    dialogue_lines = []
    with open(dialogue_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            data = json.loads(line)
            # Skip header
            if "header" in data:
                continue
            dialogue_lines.append(data)

    # Take first 10 turns
    dialogue_lines = dialogue_lines[:10]

    print(f"Loaded {len(dialogue_lines)} dialogue lines")

    # Initialize character managers
    ema_manager = CharacterVoiceManager("艾玛", character_voice_example / "艾玛")
    hiro_manager = CharacterVoiceManager("希罗", character_voice_example / "希罗")

    print(f"Ema GPT: {ema_manager.gpt_model_path.name}")
    print(f"Ema SoVITS: {ema_manager.sovits_model_path.name}")
    print(f"Hiro GPT: {hiro_manager.gpt_model_path.name}")
    print(f"Hiro SoVITS: {hiro_manager.sovits_model_path.name}")

    # Check API health
    client = GPTSoVITSClient(api_url="http://127.0.0.1:9880")
    print("\n[CHECK] Checking GPT-SoVITS API at port 9880...")
    is_healthy = await client.health_check()
    await client.close()

    if not is_healthy:
        print("❌ Cannot connect to GPT-SoVITS API at http://127.0.0.1:9880")
        print("   Please ensure GPT-SoVITS API is running")
        sys.exit(1)
    print("✓ API is running")

    # Run test
    output_path = output_dir / "single_port_test_result.json"
    result = await run_single_port_test(
        dialogue_lines=dialogue_lines,
        ema_manager=ema_manager,
        hiro_manager=hiro_manager,
        output_path=output_path,
    )

    # Print summary
    print("\n" + "=" * 70)
    print("SINGLE PORT TEST RESULTS")
    print("=" * 70)
    print(f"Total turns: {result['summary']['num_turns']}")
    print(f"Total time: {result['summary']['total_time']:.2f}s")
    print(f"Avg model load time: {result['summary']['avg_model_load_time']:.2f}s")
    print(f"Avg generation time: {result['summary']['avg_generation_time']:.2f}s")
    print(f"Avg total time per turn: {result['summary']['avg_total_time']:.2f}s")
    print(f"\nResults saved to: {output_path}")
    print("=" * 70)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⚠️  Test interrupted by user")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        import traceback

        traceback.print_exc()
