"""
Test new topic_loader.py with SETTING-*.md files
Verifies parsing of Dialogue_Language, Voice_Language, DETAIL_Follow, DETAIL_Direct_Use_For_Voice
"""

import sys
import io
from pathlib import Path

# Force UTF-8 output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

# Add dialogue-server to path
dialogue_server_path = Path(__file__).parent.parent
sys.path.insert(0, str(dialogue_server_path))

from dialogue_gen.topic_loader import TopicLoader, TopicMetadata

import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# Path to dialogue-topics
TOPICS_DIR = dialogue_server_path.parent / "dialogue-topics"


def test_chatting_before_sleep():
    """Test SETTING-chatting-before-sleep.md (None type, no DETAIL)"""
    print("\n" + "=" * 60)
    print("TEST: SETTING-chatting-before-sleep.md")
    print("=" * 60)

    path = TOPICS_DIR / "SETTING-chatting-before-sleep.md"
    content, meta = TopicLoader.load_topic(path)

    assert meta.title == "Chatting Before Sleep", f"Title mismatch: {meta.title}"
    assert meta.topic_type == "None", f"Type mismatch: {meta.topic_type}"
    assert meta.style == "a little nsfw", f"Style mismatch: {meta.style}"
    assert meta.dialogue_language == "zh", f"DL mismatch: {meta.dialogue_language}"
    assert meta.voice_language == "zh", f"VL mismatch: {meta.voice_language}"
    assert meta.detail_file is None, f"Should have no DETAIL file: {meta.detail_file}"

    print(f"  ✓ Title: {meta.title}")
    print(f"  ✓ Type: {meta.topic_type}")
    print(f"  ✓ Languages: {meta.dialogue_language} -> {meta.voice_language}")
    print(f"  ✓ Style: {meta.style}")
    print(f"  ✓ No DETAIL file (correct for None type)")

    return True


def test_learn_cuda():
    """Test SETTING-learn-cuda.md (Learning type, DETAIL with code)"""
    print("\n" + "=" * 60)
    print("TEST: SETTING-learn-cuda.md")
    print("=" * 60)

    path = TOPICS_DIR / "SETTING-learn-cuda.md"
    content, meta = TopicLoader.load_topic(path)

    assert meta.title == "Learn CUDA", f"Title mismatch: {meta.title}"
    assert meta.topic_type == "Learning", f"Type mismatch: {meta.topic_type}"
    assert meta.dialogue_language == "zh", f"DL mismatch: {meta.dialogue_language}"
    assert meta.voice_language == "zh", f"VL mismatch: {meta.voice_language}"
    assert meta.detail_follow == 80, f"Follow mismatch: {meta.detail_follow}"
    assert meta.detail_direct_use_for_voice == 20, (
        f"DirectUse mismatch: {meta.detail_direct_use_for_voice}"
    )
    assert meta.detail_file == "DETAIL-learn-cuda.md", (
        f"DETAIL file mismatch: {meta.detail_file}"
    )

    print(f"  ✓ Title: {meta.title}")
    print(f"  ✓ Type: {meta.topic_type}")
    print(f"  ✓ Languages: {meta.dialogue_language} -> {meta.voice_language}")
    print(f"  ✓ DETAIL_Follow: {meta.detail_follow}")
    print(f"  ✓ DETAIL_Direct_Use_For_Voice: {meta.detail_direct_use_for_voice}")
    print(f"  ✓ DETAIL_File: {meta.detail_file}")

    return True


def test_fanfiction():
    """Test SETTING-fanfiction.md (Fanfiction type, DETAIL with story)"""
    print("\n" + "=" * 60)
    print("TEST: SETTING-fanfiction.md")
    print("=" * 60)

    path = TOPICS_DIR / "SETTING-fanfiction.md"
    content, meta = TopicLoader.load_topic(path)

    assert meta.title == "Fanfiction", f"Title mismatch: {meta.title}"
    assert meta.topic_type == "Fanfiction", f"Type mismatch: {meta.topic_type}"
    assert meta.dialogue_language == "zh", f"DL mismatch: {meta.dialogue_language}"
    assert meta.voice_language == "ja", f"VL mismatch: {meta.voice_language}"
    assert meta.detail_follow == 80, f"Follow mismatch: {meta.detail_follow}"
    assert meta.detail_direct_use_for_voice == 90, (
        f"DirectUse mismatch: {meta.detail_direct_use_for_voice}"
    )
    assert meta.detail_file == "DETAIL-fanfiction.md", (
        f"DETAIL file mismatch: {meta.detail_file}"
    )

    print(f"  ✓ Title: {meta.title}")
    print(f"  ✓ Type: {meta.topic_type}")
    print(f"  ✓ Languages: {meta.dialogue_language} -> {meta.voice_language}")
    print(f"  ✓ DETAIL_Follow: {meta.detail_follow}")
    print(f"  ✓ DETAIL_Direct_Use_For_Voice: {meta.detail_direct_use_for_voice}")
    print(f"  ✓ DETAIL_File: {meta.detail_file}")

    return True


def test_template():
    """Test SETTING-topic-template.md (template file)"""
    print("\n" + "=" * 60)
    print("TEST: SETTING-topic-template.md")
    print("=" * 60)

    path = TOPICS_DIR / "SETTING-topic-template.md"
    content, meta = TopicLoader.load_topic(path)

    assert meta.dialogue_language == "zh", f"DL mismatch: {meta.dialogue_language}"
    assert meta.voice_language == "zh", f"VL mismatch: {meta.voice_language}"
    assert meta.detail_follow == 80, f"Follow mismatch: {meta.detail_follow}"
    assert meta.detail_direct_use_for_voice == 0, (
        f"DirectUse mismatch: {meta.detail_direct_use_for_voice}"
    )

    print(f"  ✓ Default languages: {meta.dialogue_language} -> {meta.voice_language}")
    print(
        f"  ✓ Default DETAIL params: Follow={meta.detail_follow}, DirectUse={meta.detail_direct_use_for_voice}"
    )

    return True


def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("TOPIC LOADER NEW FORMAT - TEST SUITE")
    print("=" * 60)

    tests = [
        ("chatting-before-sleep", test_chatting_before_sleep),
        ("learn-cuda", test_learn_cuda),
        ("fanfiction", test_fanfiction),
        ("template", test_template),
    ]

    passed = 0
    failed = 0

    for name, test_fn in tests:
        try:
            if test_fn():
                passed += 1
        except Exception as e:
            print(f"  ✗ FAILED: {e}")
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
