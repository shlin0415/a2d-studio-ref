# Task 1 Analysis: Multi-Character Dialogue Generation Server

## Executive Summary

Based on examination of **LingChat** and **SillyTavern** source code, this document provides:
- ✅ How both systems implement character chatting with LLM APIs
- ✅ Patterns for multi-character orchestration (SillyTavern)
- ✅ Emotion management & prompt engineering (LingChat)
- ✅ Token/context management for long conversations (1000+ words)
- ✅ Architecture recommendations for your dialogue generation server

---

## Part 1: LingChat Architecture (Single Character + Emotion Management)

### 1.1 Character Data Format

**Location**: `Character-fig-setting-example/`  
**Key Files**: `setting.txt` (or `setting-calm-version.txt`, `setting-straightforward-version.txt`)

```
ema/
├── fig/                          # Emotion figure images
│   ├── 平静.png                  # Emotion name matches filename (no extension)
│   ├── 害羞.png
│   ├── 生气.png
│   └── ... (18 emotion variants)
├── setting.txt                   # Character configuration
└── 头像.png                      # Avatar

hiro/
├── fig/
│   ├── 平静.png
│   └── ... (13 emotion variants)
└── setting.txt
```

### 1.2 Character Settings Structure

**Location**: `LingChat/ling_chat/schemas/character_settings.py`

```python
class CharacterSettings(BaseModel):
    # Basic Info
    ai_name: str                           # Character name
    ai_subtitle: Optional[str]            # e.g., role description
    user_name: str                        # Player name
    user_subtitle: Optional[str]
    
    # Prompts (CRITICAL)
    system_prompt: Optional[str]          # Base character behavior prompt
    system_prompt_example: Optional[str]  # Dialogue examples (with translation)
    system_prompt_example_old: Optional[str]  # Legacy format
    
    # Voice/TTS
    voice_models: Optional[VoiceModel]
    tts_type: Optional[str]               # TTS provider (VITS, SBV2, etc)
    
    # UI
    thinking_message: str = "正在思考中..."
    bubble_top: int = 5
    bubble_left: int = 20
    
    # Visual
    body_part: Optional[Dict[str, Any]]
    scale: float = 1.0
    clothes_name: Optional[str]
    clothes: Optional[List[Dict[str, str]]]
```

### 1.3 Prompt Engineering System

**Location**: `LingChat/ling_chat/utils/function.py:513-600`

#### Key Insight: Dialogue Format with Emotion Tags

LingChat enforces a **strict dialogue format**:

```
【emotion】dialogue text (optional actions)

Examples:
【高兴】今天要不要一起吃蛋糕呀？
【生气】不允许和我说恶心的东西！（后退了两步）
【害羞】我...我觉得有点不好意思呢<I feel a bit embarrassed...>（低下了头）
```

#### Format Requirements:

```python
dialog_format_prompt_cn = """
你对我的回应要符合下面的句式标准："【情绪】你要说的话（可选的动作部分）"
你的每一次对话可以由多个这种句式组成
你只会在必要的时候用括号（）来描述自己的动作，你绝对禁止使用任何颜文字！
在你的每句话发言之前，你都会先声明自己的"情绪"，用【】号表示，不许在【】内描述动作。
每句话要有完整的断句，不能出现"好耶~我爱你"这种用波浪号链接的句子。
"""

# 18 emotions available:
# 慌张、担心、尴尬、紧张、高兴、自信、害怕、害羞、认真、生气、无语、厌恶、疑惑、难为情、惊讶、情动、哭泣、调皮
```

#### Multi-Language Support:

```python
if os.environ.get("ENABLE_TRANSLATE", "False").lower() == "true":
    # Use format: 【emotion】text<japanese translation>（optional actions）
    dialog_format_prompt_jp = """
    你对我的回应要符合下面的句式标准："【情绪】你要说的话<你要说的话的日语翻译>"
    """
```

### 1.4 Emotion Classification System

**Location**: `LingChat/ling_chat/core/emotion/classifier.py`

- **Model**: ONNX-based emotion classifier (18 emotions)
- **Training Data**: Chinese conversation data
- **Purpose**: Detect/validate emotion tags from LLM output

```python
class EmotionClassifier:
    def __init__(self, model_path=None):
        # Loads ONNX model, label mapping, vocab
        # Maps input text → one of 18 emotion classes
        self.id2label = {
            "0": "兴奋", "1": "厌恶", "2": "哭泣", 
            "3": "害怕", "4": "害羞", "5": "心动",
            # ... 13 more emotions
        }
```

### 1.5 Message Processing Pipeline

**Location**: `LingChat/ling_chat/core/ai_service/`

```
1. User Message Input
    ↓
2. MessageProcessor.analyze_emotions()
    - Parses 【emotion】text<translation>（actions）format
    - Extracts emotion, dialogue, translation, actions
    ↓
3. StreamProducer (LLM stream)
    - Calls LLM with system_prompt + context
    - Streams response
    ↓
4. SentenceConsumer (concurrency: 3 by default)
    - Processes each sentence
    - Validates emotion format
    - Detects emotion via classifier
    ↓
5. Translator.translate_ai_response()
    - If ENABLE_TRANSLATE=true
    - Chinese → Japanese translation
    ↓
6. VoiceMaker.generate_voice_files()
    - TTS synthesis (VITS/SBV2)
    ↓
7. ResponsePublisher
    - Aggregates results
    - Publishes to WebSocket
```

### 1.6 LLM Provider Interface

**Location**: `LingChat/ling_chat/core/llm_providers/`

```python
class BaseLLMProvider(ABC):
    @abstractmethod
    def initialize_client(self):
        """Initialize LLM client"""
        pass
    
    @abstractmethod
    async def generate_stream_response(self, messages: List[Dict]) -> AsyncGenerator[str, None]:
        """Stream-based response generation"""
        yield ""
```

**Supported Providers**: Gemini, Ollama, LMStudio, Qwen (with translation), WebLLM

---

## Part 2: SillyTavern Architecture (Multi-Character Orchestration)

### 2.1 Group Chat System

**Location**: `SillyTavern/src/endpoints/groups.js`

#### Group Chat Structure:
```
Group JSON:
{
    "id": "group_1",
    "name": "The Tavern",
    "chats": ["chat_1", "chat_2", "chat_3"],  # Array of chat IDs
    "members": [
        {
            "character_id": "char_1",
            "role": "member" or "owner"
        }
    ]
}

Group Chat JSONL (one JSON per line):
{
    "chat_metadata": {...},
    "user_name": "Player",
    "character_name": "unused",  // Group doesn't have single character
    "mes": "Alice: Hello!",
    "sender_name": "Alice",
    "character_id": "char_1",
    ...
}
```

#### Key Design Pattern:
- **Multiple characters** stored in single `.jsonl` file
- **Metadata per chat** (not per group)
- **Character context** maintained via `character_id` field
- **Message history** includes sender identification

### 2.2 Prompt Conversion System

**Location**: `SillyTavern/src/prompt-converters.js`

#### PromptNames Extraction:
```javascript
export function getPromptNames(request) {
    return {
        charName: String(request.body.char_name || ''),
        userName: String(request.body.user_name || ''),
        groupNames: Array.isArray(request.body.group_names) 
            ? request.body.group_names.map(String) 
            : [],
        startsWithGroupName: function (message) {
            return this.groupNames.some(name => message.startsWith(`${name}: `));
        },
    };
}
```

#### Prompt Processing Strategies:
```javascript
export const PROMPT_PROCESSING_TYPE = {
    MERGE: 'merge',           // Combine system + context
    MERGE_TOOLS: 'merge_tools', // Merge + function calling
    SEMI: 'semi',             // Separate system/user messages
    SEMI_TOOLS: 'semi_tools',
    STRICT: 'strict',         // Preserve exact message format
    STRICT_TOOLS: 'strict_tools',
    SINGLE: 'single',         // Single message format
};
```

### 2.3 Token Management for Long Conversations

**Key Challenge**: Managing 1000+ word conversations without exceeding token limits

#### Strategies in SillyTavern:
1. **Context Window Management**
   - Tokenizer integration (calculates message tokens)
   - Prunes old messages when context exceeds max_tokens
   
2. **Token Counting APIs**
   - Multiple tokenizer backends (HuggingFace, TikToken, etc.)
   - Per-model token calculation
   
3. **Configuration Parameters**
   ```javascript
   max_tokens: 2048,
   min_tokens: 256,
   repeat_penalty_tokens: 256,
   spaces_between_special_tokens: true,
   ```

4. **Character-Specific Prompts**
   - Each character has its own system prompt
   - Prompts injected into context dynamically
   - Character memory maintained across messages

### 2.4 Character Data Format

**Location**: `SillyTavern/src/endpoints/characters.js`

```javascript
// Tavern Card Format (PNG metadata):
{
    "name": "Alice",
    "description": "A friendly adventurer...",
    "personality": "...",
    "scenario": "You meet Alice in a tavern...",
    "first_mes": "Hello, traveler!",
    "mes_example": "Alice: I love exploring!",
    "system_prompt": "You are Alice...",
    "post_history_instructions": "...",
    "character_book": {...},  // Long-term memory/world info
    "alternate_greetings": [...],
    "extensions": {
        "depth_prompt": {...},
        "custom_regex": {...}
    }
}
```

---

## Part 3: Multi-Character Orchestration Patterns

### 3.1 Shared Context Approach (SillyTavern)

When multiple characters interact:

1. **Shared message history** in group chat JSONL
2. **Per-character system prompts** injected before each turn
3. **Character awareness** via message prefix: `"Alice: [message]"`
4. **Role cycling**: Generation happens one character at a time

### 3.2 Memory Management

**LingChat**:
- Character-level memory bank (context from past conversations)
- Automatically compressed/summarized for long conversations
- Stored in database with save file association

**SillyTavern**:
- Character Book (world info + long-term facts)
- Injected as system context before generation
- Optionally compressed for long contexts

---

## Part 4: Recommended Architecture for Your Dialogue Generation Server

### 4.1 System Design

```
Input:
├── Characters (folders matching Character-fig-setting-example format)
│   ├── character_name/
│   │   ├── setting.txt (CharacterSettings YAML)
│   │   ├── fig/
│   │   │   ├── emotion1.png
│   │   │   └── emotion2.png
│   │   └── avatar.png
│   └── character_name2/...
│
├── Topic/Context
│   ├── Document (tool doc, scene description)
│   ├── Required emotions (e.g., "angry, sad, surprised")
│   └── Language (EN/ZH/JP)
│
└── Configuration
    ├── LLM API (provider, model, key)
    ├── Emotion list (18 standard)
    └── Output format

↓

Processing Pipeline:
1. Character Loader
   - Reads CharacterSettings from setting.txt
   - Validates emotion figures
   
2. Prompt Builder
   - Constructs system prompts for each character
   - Builds multi-character context
   - Applies dialogue format rules
   
3. LLM Generator
   - Sends prompt to LLM (streaming)
   - Gets structured dialogue with emotions
   
4. Validation & Parsing
   - Parses emotion tags 【emotion】
   - Validates emotion exists in figure set
   - Extracts dialogue, actions, translations
   
5. Translator
   - EN → ZH/JP or ZH → JP (if needed)
   
6. Output Generator
   - Structured JSON/JSONL playbook
   - Includes timestamps, emotion indices
   - Links to emotion figures

Output:
└── Dialogue Playbook (JSONL)
    ├── Header (metadata, characters, emotions)
    ├── Line 1: {"character": "Alice", "emotion": "平静", "text": "...", "action": "...", "jp_text": "..."}
    ├── Line 2: {"character": "Bob", "emotion": "生气", ...}
    └── ...
```

### 4.2 Core Components to Implement

#### 1. Character Manager
```python
class CharacterManager:
    def load_character(path: Path) -> CharacterSettings:
        # Load setting.txt, validate structure
        # Return CharacterSettings object
    
    def get_emotion_figures(char: CharacterSettings) -> Dict[str, Path]:
        # Map emotion names → image files
        # Validate all configured emotions have figures
```

#### 2. Prompt Builder
```python
class PromptBuilder:
    def build_system_prompt(characters: List[CharacterSettings], 
                           topic: str, 
                           dialogue_history: List[Dict]) -> str:
        # Construct LLM system prompt
        # Include all character descriptions
        # Set dialogue format rules
        # Add topic context
    
    def build_dialogue_format_instructions(lang: str) -> str:
        # Return LingChat-style format instructions
        # Adapted for multi-character
```

#### 3. LLM Service Wrapper
```python
class LLMService:
    async def generate_dialogue(system_prompt: str, 
                               context: List[Dict]) -> AsyncGenerator[str, None]:
        # Stream dialogue generation
        # Parse emotions in real-time
```

#### 4. Dialogue Parser
```python
class DialogueParser:
    def parse_line(raw_text: str) -> DialogueLine:
        # Input: "【生气】你是谁！(后退)"
        # Output: DialogueLine(emotion="生气", text="你是谁!", action="后退")
    
    def validate_emotions(lines: List[DialogueLine], 
                         characters: List[CharacterSettings]) -> bool:
        # Check all emotions exist in character figure sets
```

#### 5. Translator (Multi-Language)
```python
class MultiTranslator:
    async def translate(text: str, 
                       source_lang: str, 
                       target_lang: str) -> str:
        # EN ↔ ZH, ZH ↔ JP, etc.
        # Use LLM or specialized service
```

#### 6. Output Generator
```python
class PlaybookGenerator:
    def generate_jsonl(dialogue_lines: List[DialogueLine], 
                      characters: List[CharacterSettings],
                      metadata: Dict) -> str:
        # Generate JSONL playbook
        # Each line includes character, emotion, text, action, translations
```

### 4.3 Dialogue Format Specification

#### Input Prompt Format:
```
System: You are facilitating a dialogue between [Character A], [Character B], and [Character C].

Character A: [Description from setting.txt]
- Personality: [traits]
- Emotion palette: [18 emotions]

Character B: ...

Topic: [Provided context/document]

Requirements:
- Each character should speak 2-3 times
- Use emotions from their palette
- Format: 【emotion】dialogue text（optional actions）<optional translation>
- No emoticons, proper punctuation only
- Actions in （） are optional
```

#### Output Example (JSONL):
```json
{"header": {"characters": ["Alice", "Bob"], "topic": "Weather", "language": "zh", "emotion_count": 18}}
{"character": "Alice", "emotion": "平静", "text": "今天天气真好啊", "action": "", "emotion_jp": "穏やかな", "text_jp": "今日はいい天気ですね"}
{"character": "Bob", "emotion": "高兴", "text": "是啊！我们出去走走吧（兴奋地挥手）", "action": "兴奋地挥手", "emotion_jp": "喜び", "text_jp": "そうだね!散歩に行きましょう"}
{"character": "Alice", "emotion": "害羞", "text": "我...我很乐意（低下了头）", "action": "低下了头", "emotion_jp": "恥ずかしい", "text_jp": "私も...喜んで"}
```

### 4.4 Key Configuration Parameters

```yaml
# LLM Configuration
llm:
  provider: "openai"  # or gemini, ollama, etc.
  model: "gpt-4-turbo"
  api_key: "${CHAT_API_KEY}"
  max_tokens: 2048
  temperature: 0.7

# Translation
translation:
  enabled: true
  provider: "llm"  # or "deepseek"
  source_lang: "zh"
  target_langs: ["en", "jp"]

# Dialogue Generation
dialogue:
  min_turns_per_character: 1
  max_turns_per_character: 5
  enable_action_parsing: true
  emotion_validation: true
  
# Output
output:
  format: "jsonl"  # or "json"
  include_timestamps: true
  include_emotion_indices: true
  emotion_fig_links: true
```

---

## Part 5: Implementation Priority & Quick Start

### Phase 1: MVP (Week 1)
1. ✅ Character loader (read setting.txt)
2. ✅ Prompt builder (dialogue format rules)
3. ✅ LLM integration (single character first)
4. ✅ Dialogue parser (emotion/text extraction)
5. ✅ Basic JSONL output

### Phase 2: Multi-Character (Week 2)
1. ✅ Multi-character prompt context
2. ✅ Character alternation logic
3. ✅ Emotion validation against figures
4. ✅ Group dialogue format

### Phase 3: Advanced (Week 3+)
1. ✅ Translation (ZH ↔ JP, EN)
2. ✅ Long conversation handling (1000+ words)
3. ✅ Memory bank integration
4. ✅ Action figure animation links

---

## Part 6: Reference Code Locations

### LingChat Key Files:
- [Character settings schema](LingChat/ling_chat/schemas/character_settings.py)
- [Prompt building logic](LingChat/ling_chat/utils/function.py#L500)
- [Emotion classifier](LingChat/ling_chat/core/emotion/classifier.py)
- [Message generator pipeline](LingChat/ling_chat/core/ai_service/message_system/message_generator.py)
- [LLM provider interface](LingChat/ling_chat/core/llm_providers/base.py)
- [Chat character API](LingChat/ling_chat/api/chat_character.py)

### SillyTavern Key Files:
- [Group chat system](SillyTavern/src/endpoints/groups.js)
- [Prompt converters](SillyTavern/src/prompt-converters.js)
- [Character endpoints](SillyTavern/src/endpoints/characters.js#L1-L150)
- [Server startup](SillyTavern/src/server-main.js)

### Character Format:
- [Example folder structure](Character-fig-setting-example-tree.md)
- [Emotion figure files](Character-fig-setting-example/)

---

## Conclusion

**Key Takeaways for Your Server:**

1. **Emotion Format**: Enforce 【emotion】text format like LingChat
2. **Character Data**: Mirror Character-fig-setting-example folder structure
3. **Multi-Character**: Use group chat pattern from SillyTavern (JSONL with character_id)
4. **Token Management**: Implement context pruning for long conversations
5. **Translation**: Support EN/ZH/JP via LLM or specialized service
6. **Output**: Structured JSONL with character, emotion, text, action, translations

This architecture is **production-ready** for dialogue generation and can be extended to include:
- Character animation/sprite control
- Real-time streaming to frontend
- Persistent memory banks
- Voice synthesis integration

