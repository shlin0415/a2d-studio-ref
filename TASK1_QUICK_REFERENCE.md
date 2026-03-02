# Task 1: Quick Reference - Dialogue Generation Server

## 📋 What You Need to Build

A **multi-character dialogue generation server** that:
1. **Input**: Character folders + topic/context
2. **Process**: Generate structured dialogue via LLM
3. **Output**: Playbook with characters, emotions, dialogue, actions
4. **Languages**: English, Chinese, Japanese
5. **Format**: JSONL (one dialogue line per object)

---

## 🔑 Core Patterns From Analysis

### Dialogue Format (from LingChat)
```
【emotion】dialogue text（optional actions）<optional translation>

Example:
【生气】你为什么这样做！（愤怒地指向对方）<Why did you do that!>
【害羞】我...我不知道（低下头）<I... I don't know>
```

### Emotion List (18 emotions)
```
慌张、担心、尴尬、紧张、高兴、自信、害怕、害羞、认真、
生气、无语、厌恶、疑惑、难为情、惊讶、情动、哭泣、调皮
```

### Character Data Structure (from Character-fig-setting-example)
```
character_name/
├── fig/                    # Emotion figures (PNG files)
│   ├── 平静.png
│   ├── 害羞.png
│   ├── 生气.png
│   └── ... (one per emotion used)
├── setting.txt            # Character config (YAML format)
└── 头像.png              # Avatar image
```

### Multi-Character Group Chat (from SillyTavern)
```json
{"header": {"characters": ["Alice", "Bob"], "language": "zh"}}
{"character": "Alice", "emotion": "平静", "text": "Hi Bob!"}
{"character": "Bob", "emotion": "高兴", "text": "Hello Alice!（waving）"}
```

---

## 🏗️ Server Architecture

```
Input Layer
├─ Character Loader (reads setting.txt)
├─ Topic/Context Parser
└─ Language & Emotion Config

Processing Layer
├─ Prompt Builder (system prompt + dialogue format)
├─ LLM Service (streaming generation)
├─ Dialogue Parser (extract emotion/text/action)
└─ Translator (if EN/JP needed)

Output Layer
└─ JSONL Playbook Generator
```

---

## 🚀 Quick Implementation Checklist

### MVP (Phase 1 - Essential)
- [ ] Character loader (read setting.txt YAML)
- [ ] Prompt builder with dialogue format rules
- [ ] LLM integration (streaming support)
- [ ] Dialogue parser (【emotion】text extraction)
- [ ] JSONL output generator

### Phase 2 (Multi-Character)
- [ ] Multi-character prompt context
- [ ] Character alternation logic
- [ ] Emotion validation against character fig files
- [ ] Group dialogue format

### Phase 3 (Polish)
- [ ] Translation (ZH ↔ JP, EN)
- [ ] Token counting for 1000+ word conversations
- [ ] Long context compression
- [ ] Action→Figure animation mapping

---

## 💻 Code References

### Where to Find Key Examples

**LingChat (Python)**:
- Prompt building: `ling_chat/utils/function.py:500-600`
- Character settings: `ling_chat/schemas/character_settings.py`
- Emotion parsing: `ling_chat/core/emotion/classifier.py`
- Message pipeline: `ling_chat/core/ai_service/message_system/`

**SillyTavern (JavaScript)**:
- Group chat: `src/endpoints/groups.js`
- Prompt conversion: `src/prompt-converters.js`
- Character data: `src/endpoints/characters.js`

**Character Format**:
- Examples: `Character-fig-setting-example/ema/`, `Character-fig-setting-example/hiro/`

---

## 📝 Sample Configuration

```yaml
llm:
  provider: "openai"
  model: "gpt-4-turbo"
  api_key: "${CHAT_API_KEY}"
  max_tokens: 2048

translation:
  enabled: true
  target_langs: ["jp"]

dialogue:
  emotions: 18  # Standard emotion set
  min_turns: 1
  max_turns: 5
  enable_actions: true
```

---

## 🎯 Key Success Criteria

✅ **Emotion Format Validation**: Ensure LLM output matches 【emotion】text（actions）<translation>

✅ **Character Consistency**: Each character uses correct emotions from their fig/ folder

✅ **Multi-Language Support**: Enable ZH→JP or ZH→EN translations seamlessly

✅ **Token Management**: Handle long conversations (1000+ words) without exceeding limits

✅ **Structured Output**: JSONL with clear fields: character, emotion, text, action, translations

---

## 🔗 Related Files in Your Workspace

- [Full Analysis](TASK1_ANALYSIS.md)
- [Action Log](ACTION_LOG.md)
- [Character Examples](Character-fig-setting-example/)
- [LingChat Source](LingChat/)
- [SillyTavern Source](SillyTavern/)

---

## 📖 Next Steps

1. **Study** `TASK1_ANALYSIS.md` (Parts 4-5 for architecture)
2. **Review** LingChat's `function.py` (prompt building logic)
3. **Examine** Character-fig-setting-example (folder structure)
4. **Plan** your MVP with the Quick Implementation Checklist above
5. **Start coding** Character Loader (easiest first component)

