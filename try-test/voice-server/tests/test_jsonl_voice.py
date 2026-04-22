"""
Test jsonl_voice_generator.py components
Tests JSONL parsing and voice settings loading (no API calls needed)
"""

import sys
import io
import json
import tempfile
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

voice_server_path = Path(__file__).parent.parent
sys.path.insert(0, str(voice_server_path))

from jsonl_voice_generator import (
    parse_jsonl,
    ConfigParser,
    CharacterVoiceLoader,
    JsonlHeader,
    DialogueLine,
)

import logging

logging.basicConfig(level=logging.WARNING)

# Path to project root
PROJECT_ROOT = Path(__file__).parent.parent.parent


def make_test_jsonl(tmp_path: Path) -> Path:
    """Create a test JSONL file"""
    header = {
        "header": {
            "characters": ["艾玛", "希罗"],
            "character_count": 2,
            "topic": "test topic",
            "dialogue_language": "zh",
            "voice_language": "ja",
            "line_count": 2,
            "format_version": "2.0",
        }
    }
    line1 = {
        "index": 0,
        "character": "艾玛",
        "emotion": "期待",
        "text": "这么晚来找我",
        "action": "看着希罗",
        "caption_text": "这么晚来找我",
        "voice_text": "こんな遅くに",
        "caption_language": "zh",
        "voice_language": "ja",
    }
    line2 = {
        "index": 1,
        "character": "希罗",
        "emotion": "害羞",
        "text": "其实...有点睡不着",
        "action": "低头",
        "caption_text": "其实...有点睡不着",
        "voice_text": "実は...眠れない",
        "caption_language": "zh",
        "voice_language": "ja",
    }

    jsonl_path = tmp_path / "test_dialogue.jsonl"
    content = json.dumps(header, ensure_ascii=False) + "\n"
    content += json.dumps(line1, ensure_ascii=False) + "\n"
    content += json.dumps(line2, ensure_ascii=False)
    jsonl_path.write_text(content, encoding="utf-8")
    return jsonl_path


def test_parse_jsonl():
    """Test JSONL parsing: header and dialogue lines"""
    print("\n" + "=" * 60)
    print("TEST: JSONL parsing")
    print("=" * 60)

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        jsonl_path = make_test_jsonl(tmp_path)

        header, dialogue_lines = parse_jsonl(jsonl_path)

        # Check header
        assert header.dialogue_language == "zh", (
            f"DL should be zh, got {header.dialogue_language}"
        )
        assert header.voice_language == "ja", (
            f"VL should be ja, got {header.voice_language}"
        )
        assert header.topic == "test topic"
        assert len(header.characters) == 2

        # Check dialogue lines
        assert len(dialogue_lines) == 2, (
            f"Should have 2 lines, got {len(dialogue_lines)}"
        )

        line0 = dialogue_lines[0]
        assert line0.character == "艾玛"
        assert line0.caption_text == "这么晚来找我"
        assert line0.voice_text == "こんな遅くに"
        assert line0.caption_language == "zh"
        assert line0.voice_language == "ja"

        line1 = dialogue_lines[1]
        assert line1.character == "希罗"
        assert line1.voice_text == "実は...眠れない"

        print("  [OK] Header parsed correctly")
        print("  [OK] 2 dialogue lines parsed correctly")
        print("  [OK] caption_text and voice_text correct")
        return True


def test_parse_jsonl_same_language():
    """Test zh/zh: voice_text should equal caption_text"""
    print("\n" + "=" * 60)
    print("TEST: JSONL parsing (same language)")
    print("=" * 60)

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        header = {
            "header": {
                "characters": ["艾玛"],
                "topic": "test",
                "dialogue_language": "zh",
                "voice_language": "zh",
                "line_count": 1,
            }
        }
        line1 = {
            "index": 0,
            "character": "艾玛",
            "emotion": "平静",
            "text": "你好呀",
            "action": "",
            "caption_text": "你好呀",
            "voice_text": "你好呀",
            "caption_language": "zh",
            "voice_language": "zh",
        }

        jsonl_path = tmp_path / "test_same_lang.jsonl"
        content = json.dumps(header, ensure_ascii=False) + "\n"
        content += json.dumps(line1, ensure_ascii=False)
        jsonl_path.write_text(content, encoding="utf-8")

        header, lines = parse_jsonl(jsonl_path)

        assert header.voice_language == "zh"
        assert lines[0].voice_text == "你好呀"
        assert lines[0].voice_text == lines[0].caption_text

        print("  [OK] Same language: voice_text == caption_text")
        return True


def test_config_parser():
    """Test config parser with voice settings format"""
    print("\n" + "=" * 60)
    print("TEST: Config parser")
    print("=" * 60)

    config_text = """
GPT_SOVITS_TYPE1='v2'
GPT_WEIGHT='test.ckpt'
SoVITS_WEIGHT='test.pth'
DEFAULT_REF_VOICE='./good_ref/test.wav'
DEFAULT_REF_SETTING='./good_ref/test.txt'
"""
    config = ConfigParser.parse_config(config_text)
    assert config["GPT_WEIGHT"] == "test.ckpt"
    assert config["DEFAULT_REF_VOICE"] == "./good_ref/test.wav"

    print("  [OK] Config parsing works correctly")
    return True


def test_character_voice_loader():
    """Test loading character voice settings from Character-voice-example/"""
    print("\n" + "=" * 60)
    print("TEST: Character voice loader (艾玛)")
    print("=" * 60)

    voice_example_dir = PROJECT_ROOT / "Character-voice-example"
    if not voice_example_dir.exists():
        print("  [SKIP] Character-voice-example not found")
        return True

    loader = CharacterVoiceLoader(voice_example_dir)
    result = loader.load("艾玛")

    if result is None:
        print("  [SKIP] 艾玛 voice settings not found")
        return True

    voice_settings, ref_audio_settings, gpt_path, sovits_path, ref_audio_path = result

    assert voice_settings.gpt_weight.endswith(".ckpt"), f"GPT weight should be .ckpt"
    assert voice_settings.sovits_weight.endswith(".pth"), (
        f"SoVITS weight should be .pth"
    )
    assert gpt_path.exists(), f"GPT model file should exist: {gpt_path}"
    assert sovits_path.exists(), f"SoVITS model file should exist: {sovits_path}"
    assert ref_audio_path.exists(), f"Ref audio should exist: {ref_audio_path}"
    assert ref_audio_settings.ref_language == "JA", f"Ref language should be JA"

    print(f"  [OK] GPT model: {gpt_path.name}")
    print(f"  [OK] SoVITS model: {sovits_path.name}")
    print(f"  [OK] Ref audio: {ref_audio_path.name}")
    print(f"  [OK] Ref language: {ref_audio_settings.ref_language}")
    return True


def test_character_voice_loader_hiro():
    """Test loading 希罗 voice settings"""
    print("\n" + "=" * 60)
    print("TEST: Character voice loader (希罗)")
    print("=" * 60)

    voice_example_dir = PROJECT_ROOT / "Character-voice-example"
    if not voice_example_dir.exists():
        print("  [SKIP] Character-voice-example not found")
        return True

    loader = CharacterVoiceLoader(voice_example_dir)
    result = loader.load("希罗")

    if result is None:
        print("  [SKIP] 希罗 voice settings not found")
        return True

    voice_settings, ref_audio_settings, gpt_path, sovits_path, ref_audio_path = result

    assert gpt_path.exists(), f"GPT model should exist: {gpt_path}"
    assert sovits_path.exists(), f"SoVITS model should exist: {sovits_path}"
    assert ref_audio_path.exists(), f"Ref audio should exist: {ref_audio_path}"

    print(f"  [OK] GPT model: {gpt_path.name}")
    print(f"  [OK] SoVITS model: {sovits_path.name}")
    print(f"  [OK] Ref audio: {ref_audio_path.name}")
    return True


def main():
    print("\n" + "=" * 60)
    print("JSONL VOICE GENERATOR TEST SUITE")
    print("=" * 60)

    tests = [
        ("JSONL parsing (zh/ja)", test_parse_jsonl),
        ("JSONL parsing (zh/zh)", test_parse_jsonl_same_language),
        ("Config parser", test_config_parser),
        ("Voice loader (艾玛)", test_character_voice_loader),
        ("Voice loader (希罗)", test_character_voice_loader_hiro),
    ]

    passed = 0
    failed = 0

    for name, test_fn in tests:
        try:
            if test_fn():
                passed += 1
        except Exception as e:
            print(f"  [FAIL] {e}")
            import traceback

            traceback.print_exc()
            failed += 1

    print("\n" + "=" * 60)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("=" * 60)

    if failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
