"""
Test output_generator.py JSONL format with caption_text/voice_text/language fields
Verifies header and line-level language fields are correct
"""

import sys
import io
import json
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

dialogue_server_path = Path(__file__).parent.parent
sys.path.insert(0, str(dialogue_server_path))

from dialogue_gen.output_generator import OutputGenerator
from dialogue_gen.core.models import DialogueLine, CharacterSettings

import logging

logging.basicConfig(level=logging.WARNING)


def make_test_lines():
    """Create sample dialogue lines for testing"""
    return [
        DialogueLine(
            character="艾玛",
            emotion="期待",
            text="这么晚来找我，是有什么事情吗？",
            action="高兴地看着希罗",
            translation_text="こんな遅くに私を訪ねてきて、何か用？",
        ),
        DialogueLine(
            character="希罗",
            emotion="害羞",
            text="其实...有点睡不着",
            action="低头玩弄衣角",
            translation_text="実は...ちょっと眠れないんだ",
        ),
    ]


def test_zh_zh_same_language():
    """Test zh/zh: caption_text == voice_text (same language)"""
    print("\n" + "=" * 60)
    print("TEST: zh/zh output format (same language)")
    print("=" * 60)

    lines = make_test_lines()
    chars = [CharacterSettings(ai_name="艾玛"), CharacterSettings(ai_name="希罗")]

    jsonl = OutputGenerator.generate_jsonl(
        dialogue_lines=lines,
        characters=chars,
        topic="test topic",
        dialogue_language="zh",
        voice_language="zh",
    )

    parsed = [json.loads(l) for l in jsonl.strip().split("\n")]

    # Check header
    header = parsed[0]["header"]
    assert header["dialogue_language"] == "zh", (
        f"Header DL should be zh, got {header['dialogue_language']}"
    )
    assert header["voice_language"] == "zh", (
        f"Header VL should be zh, got {header['voice_language']}"
    )

    # Check first line
    line1 = parsed[1]
    assert line1["caption_text"] == "这么晚来找我，是有什么事情吗？", (
        "caption_text should be Chinese text"
    )
    assert line1["voice_text"] == "这么晚来找我，是有什么事情吗？", (
        "voice_text should equal caption_text when same language"
    )
    assert line1["caption_language"] == "zh", f"caption_language should be zh"
    assert line1["voice_language"] == "zh", f"voice_language should be zh"

    print("  [OK] Header: dialogue_language=zh, voice_language=zh")
    print("  [OK] Line: caption_text == voice_text (same language)")
    return True


def test_zh_ja_different_language():
    """Test zh/ja: caption_text=Chinese, voice_text=Japanese translation"""
    print("\n" + "=" * 60)
    print("TEST: zh/ja output format (different languages)")
    print("=" * 60)

    lines = make_test_lines()
    chars = [CharacterSettings(ai_name="艾玛"), CharacterSettings(ai_name="希罗")]

    jsonl = OutputGenerator.generate_jsonl(
        dialogue_lines=lines,
        characters=chars,
        topic="test topic",
        dialogue_language="zh",
        voice_language="ja",
    )

    parsed = [json.loads(l) for l in jsonl.strip().split("\n")]

    # Check header
    header = parsed[0]["header"]
    assert header["dialogue_language"] == "zh", f"Header DL should be zh"
    assert header["voice_language"] == "ja", f"Header VL should be ja"

    # Check first line
    line1 = parsed[1]
    assert line1["caption_text"] == "这么晚来找我，是有什么事情吗？", (
        "caption_text should be Chinese"
    )
    assert line1["voice_text"] == "こんな遅くに私を訪ねてきて、何か用？", (
        "voice_text should be Japanese translation"
    )
    assert line1["caption_language"] == "zh", "caption_language should be zh"
    assert line1["voice_language"] == "ja", "voice_language should be ja"

    print("  [OK] Header: dialogue_language=zh, voice_language=ja")
    print("  [OK] Line: caption_text=Chinese, voice_text=Japanese")
    return True


def test_backward_compat_language_param():
    """Test backward compat: language= param maps to dialogue_language"""
    print("\n" + "=" * 60)
    print("TEST: backward compat (language= param)")
    print("=" * 60)

    lines = make_test_lines()
    chars = [CharacterSettings(ai_name="艾玛")]

    jsonl = OutputGenerator.generate_jsonl(
        dialogue_lines=lines[:1],
        characters=chars,
        topic="test topic",
        language="ja",  # Old param
    )

    parsed = [json.loads(l) for l in jsonl.strip().split("\n")]
    header = parsed[0]["header"]
    assert header["dialogue_language"] == "ja", (
        "Old language= should map to dialogue_language"
    )

    print("  [OK] Old 'language' param maps to dialogue_language")
    return True


def test_header_fields():
    """Test header contains all required fields"""
    print("\n" + "=" * 60)
    print("TEST: header fields completeness")
    print("=" * 60)

    lines = make_test_lines()
    chars = [CharacterSettings(ai_name="艾玛", character_key="ema")]

    jsonl = OutputGenerator.generate_jsonl(
        dialogue_lines=lines,
        characters=chars,
        topic="test topic",
        dialogue_language="zh",
        voice_language="ja",
    )

    parsed = [json.loads(l) for l in jsonl.strip().split("\n")]
    header = parsed[0]["header"]

    required_fields = [
        "characters",
        "character_count",
        "topic",
        "dialogue_language",
        "voice_language",
        "line_count",
        "format_version",
    ]
    for field in required_fields:
        assert field in header, f"Header missing field: {field}"

    assert header["characters"] == ["ema"], "character_key should be used"
    assert header["line_count"] == 2, (
        f"line_count should be 2, got {header['line_count']}"
    )
    assert header["format_version"] == "2.0", "format_version should be 2.0"

    print("  [OK] All required header fields present")
    print(
        f"  [OK] characters={header['characters']}, line_count={header['line_count']}"
    )
    return True


def main():
    print("\n" + "=" * 60)
    print("OUTPUT FORMAT TEST SUITE")
    print("=" * 60)

    tests = [
        ("zh/zh same language", test_zh_zh_same_language),
        ("zh/ja different language", test_zh_ja_different_language),
        ("backward compat", test_backward_compat_language_param),
        ("header fields", test_header_fields),
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
