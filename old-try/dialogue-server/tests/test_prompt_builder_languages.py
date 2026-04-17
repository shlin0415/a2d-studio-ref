"""
Test prompt_builder.py with different language combinations
Verifies format changes based on dialogue_language and voice_language
"""

import sys
import io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

dialogue_server_path = Path(__file__).parent.parent
sys.path.insert(0, str(dialogue_server_path))

from dialogue_gen.prompt_builder import PromptBuilder
from dialogue_gen.core.models import CharacterSettings

import logging

logging.basicConfig(level=logging.WARNING)


def test_same_language():
    """Test zh/zh: no translation in prompt"""
    print("\n" + "=" * 60)
    print("TEST: zh/zh (same language, no translation)")
    print("=" * 60)

    char = CharacterSettings(ai_name="Alice", ai_subtitle="A friendly character")

    prompt = PromptBuilder.build_system_prompt(
        user_name="Player",
        characters=[char],
        topic="Two friends chat",
        dialogue_language="zh",
        voice_language="zh",
    )

    # Should have Chinese dialogue format WITHOUT translation
    assert "Chinese dialogue（action" in prompt, "Should mention Chinese dialogue"
    assert "<Japanese translation>" not in prompt, "Should NOT have translation format"
    assert "这么晚来找我" in prompt, "Should have Chinese example"

    print("  [OK] Format: Chinese dialogue without translation")
    print("  [OK] Example: Chinese text only")
    return True


def test_zh_ja():
    """Test zh/ja: Japanese translation in prompt"""
    print("\n" + "=" * 60)
    print("TEST: zh/ja (different languages, with translation)")
    print("=" * 60)

    char = CharacterSettings(ai_name="Alice")

    prompt = PromptBuilder.build_system_prompt(
        user_name="Player",
        characters=[char],
        topic="Two friends chat",
        dialogue_language="zh",
        voice_language="ja",
    )

    # Should have Chinese + Japanese translation format
    assert "Chinese dialogue（action" in prompt, "Should mention Chinese dialogue"
    assert "<Japanese translation>" in prompt, "Should have Japanese translation format"
    assert "这么晚来找我" in prompt, "Should have Chinese example"
    assert "こんな遅くに" in prompt, "Should have Japanese example"
    assert "MUST include <Japanese> translation" in prompt, "Should enforce translation"

    print("  [OK] Format: Chinese dialogue with Japanese translation")
    print("  [OK] Example: Chinese + Japanese")
    print("  [OK] Constraint: MUST include translation")
    return True


def test_ja_ja():
    """Test ja/ja: Japanese only"""
    print("\n" + "=" * 60)
    print("TEST: ja/ja (same language, Japanese)")
    print("=" * 60)

    char = CharacterSettings(ai_name="Alice")

    prompt = PromptBuilder.build_system_prompt(
        user_name="Player",
        characters=[char],
        topic="Two friends chat",
        dialogue_language="ja",
        voice_language="ja",
    )

    assert "Japanese dialogue（action" in prompt, "Should mention Japanese dialogue"
    assert (
        "<" not in prompt.split("Example Format:")[1].split("###")[0]
        or "translation"
        not in prompt.split("Example Format:")[1].split("###")[0].lower()
    ), "Should NOT have translation in example"
    assert "こんな遅くに" in prompt, "Should have Japanese example"
    assert "All dialogue text must be in Japanese" in prompt, "Should enforce Japanese"

    print("  [OK] Format: Japanese dialogue without translation")
    print("  [OK] Example: Japanese text only")
    print("  [OK] Constraint: dialogue in Japanese")
    return True


def test_en_zh():
    """Test en/zh: English dialogue with Chinese translation"""
    print("\n" + "=" * 60)
    print("TEST: en/zh (English dialogue, Chinese voice)")
    print("=" * 60)

    char = CharacterSettings(ai_name="Alice")

    prompt = PromptBuilder.build_system_prompt(
        user_name="Player",
        characters=[char],
        topic="Two friends chat",
        dialogue_language="en",
        voice_language="zh",
    )

    assert "English dialogue（action" in prompt, "Should mention English dialogue"
    assert "<Chinese translation>" in prompt, "Should have Chinese translation format"
    assert "Why did you come" in prompt, "Should have English example"
    assert "这么晚来找我" in prompt or "有点睡不着" in prompt, (
        "Should have Chinese example"
    )
    assert "All dialogue text must be in English" in prompt, "Should enforce English"

    print("  [OK] Format: English dialogue with Chinese translation")
    print("  [OK] Example: English + Chinese")
    print("  [OK] Constraint: dialogue in English")
    return True


def test_backward_compat():
    """Test backward compat: language= param still works"""
    print("\n" + "=" * 60)
    print("TEST: backward compat (language= param)")
    print("=" * 60)

    char = CharacterSettings(ai_name="Alice")

    prompt = PromptBuilder.build_system_prompt(
        user_name="Player",
        characters=[char],
        topic="Two friends chat",
        language="ja",  # Old param
    )

    assert "Japanese dialogue" in prompt, "Should respect old language param"

    print("  [OK] Old 'language' param still works")
    return True


def main():
    print("\n" + "=" * 60)
    print("PROMPT BUILDER LANGUAGE TEST SUITE")
    print("=" * 60)

    tests = [
        ("zh/zh same language", test_same_language),
        ("zh/ja translation", test_zh_ja),
        ("ja/ja Japanese", test_ja_ja),
        ("en/zh English+Chinese", test_en_zh),
        ("backward compat", test_backward_compat),
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
