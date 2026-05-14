# a2d-studio 已尝试内容总结

> 时间跨度: 2026-03-02 ~ 2026-05-11
> 核心: 多角色对话生成 + 语音合成 + 前端展示

---

## 一、对话生成系统 (`try-test/dialogue-server/`)

### 已完成管线（6个模块）

| 模块 | 最近修改 | 文件位置 | 作用 |
|------|----------|----------|------|
| character_loader | Mar 3 | `dialogue_gen/character_loader.py` | 从 `Character-fig-setting-example/` 加载角色，自动发现 `fig/` 情绪立绘 |
| prompt_builder | **Mar 29** | `dialogue_gen/prompt_builder.py` | 构建 LLM system prompt，`【情绪】文本（动作）<翻译>` 格式，9种语言组合 |
| llm_service | Mar 3 | `dialogue_gen/llm_service.py` | OpenAI/DeepSeek API 封装，streaming + non-streaming，async |
| dialogue_parser | **Mar 29** | `dialogue_gen/dialogue_parser.py` | 解析LLM输出，提取情绪/对话/动作/翻译，多角色轮询 |
| output_generator | **Mar 29** | `dialogue_gen/output_generator.py` | 输出 JSONL/JSON/CSV/TXT，`caption_text`/`voice_text` 双字段 |
| dialogue_generator | Mar 28 | `dialogue_gen/dialogue_generator.py` | 主编排器，协调所有模块 |

### 两次迭代

**Phase1+2 MVP (3/2~3/3)**:
- 6大模块建成，DeepSeek API 集成，首个真实输出 `real_dialogue.jsonl`
- 数据模型 `core/models.py`（CharacterSettings, DialogueLine, DialoguePlaybook, STANDARD_EMOTIONS 18种）

**格式大改 — mimo-dv-test-plan (3/28~3/29)**:
- 新话题模板格式：`|---meta---|` / `|====Section====|` / `|<===Stage_N===>|`
- 新增 `Dialogue_Language` / `Voice_Language` 双语言，支持 9 种组合
- 改名：`DETAIL_Similarity → DETAIL_Follow`，`DETAIL_ReadForbidden → DETAIL_Direct_Use_For_Voice`
- 删除旧 `text_jp` 字段，改为 `caption_text`（屏幕字幕）+ `voice_text`（TTS用）
- 3个话题文件全部转换：chatting-before-sleep（Simple），learn-cuda（Learning），fanfiction（Fanfiction / 4 Stage）

### 测试状态
测试文件位置: `dialogue-server/tests/`
- `test_components.py` — 6组件单元测试
- `test_topic_loader_new_format.py` — 新格式解析（4测试）
- `test_prompt_builder_languages.py` — 9种语言组合（5测试）
- `test_output_format.py` — caption/voice字段（4测试）
- **全部通过**

---

## 二、语音系统 (`try-test/voice-server/`)

| 文件 | 最近修改 | 作用 |
|------|----------|------|
| `jsonl_voice_generator.py` | **Mar 29** | 读JSONL → 按角色切换GPT/SoVITS模型 → 调GPT-SoVITS API → 输出wav |
| `demo_gpt_sovits_voice.py` | Mar 4 | 早期单角色语音演示（艾玛/希罗，中/日/英） |
| `test_single_port_bottleneck.py` | Mar 10 | 单端口+模型切换瓶颈测试 |
| `test_dual_port_performance.py` | Mar 10 | 双端口+各占一路对比测试 |
| `compare_results.py` | Mar 10 | 两种方案对比分析 |

### 发现的瓶颈
- GPT-SoVITS 角色间切换要重载模型权重（GPT .ckpt + SoVITS .pth），耗时高
- 测试了双端口方案（31801/31802 各占一路）对比单端口方案

---

## 三、前端设计 (`try-test/frontend-design/`)

| 条目 | 说明 |
|------|------|
| 技术栈 | React 19 + Vite 6 + Tailwind CSS 4 + react-rnd + motion + lucide-react |
| 来源 | Google AI Studio 生成的工程 |
| 当前状态 | `dist/` 已构建产出，**未与后端连接** |
| 核心组件 | `App.tsx` — 可拖拽Resize的Region布局系统（对话区×2、立绘区×2、主工作区、浮动区） |
| 设计参考 | PNG界面截图×4 + PPTX设计文档 |

---

## 四、时间线

| 时间段 | 事件 | 关键产出 |
|--------|------|----------|
| 3/2 ~ 3/3 | Phase1+2 MVP | 6模块对话服务器 + DeepSeek集成 + 首次输出 |
| 3/4 | 语音演示 | `demo_gpt_sovits_voice.py` |
| 3/10 | 瓶颈测试 | 单/双端口对比 + 分析 |
| 3/15 | 路线图 | `roadmap.md` 优先级排序 |
| 3/20 ~ 3/21 | 前端设计 | React前端 + 布局系统 + `dist/` |
| **3/28 ~ 3/29** | **格式大改** | 新模板/新语言字段/caption_voice分离/JSONL语音管线/28测试全部通过 |
| 4/7 ~ 4/13 | 文档更新 | AGENTS.md, CLAUDE.md, human-chat-template.md |
| 5/11 | 小改 | AGENTS.md |

---

## 五、关键架构决策

1. **caption / voice 分离** — 屏幕显示内容 ≠ TTS发音内容，各有独立语言设置
2. **4种话题类型** — Simple / Learning / Fanfiction / Letter，各有不同的LLM prompt策略
3. **Stage分阶** — 长话题（如fanfiction 554行）按叙事弧切分为4个Stage，未来可配合屏幕尺寸分页
4. **角色语音模型切换** — 已验证是性能瓶颈，双端口方案可规避但需要管理两套API实例
5. **旧文件保留** — 所有重大改动均将旧文件重命名为 `old-*` 或 `.bak`，保证可回滚

---

## 六、尚未做的事

| 事项 | 状态 |
|------|------|
| `screen-server/` | **完全为空** — 应该是最终播放器/画面服务器 |
| 对话→语音流式管线 | 未实现（当前是 batch：全量对话→再统一转语音） |
| 前端 ↔ 后端连接 | 未实现 |
| 编辑+重新生成工作流 | 未实现 |
| 按屏幕尺寸分页 | 未实现 |
| `voice-server/`（根目录）| 为空 |
| `dialogue-server/`（根目录）| 为空 |

当前 `try-test/` 内的管线已全线打通（话题 → topic_loader → prompt_builder → LLM → parser → output_generator(jsonl) → jsonl_voice_generator(wav)），28个测试全部通过。核心组件处于实验验证完成、待集成的状态。

---

## 七、参考文件

- `time-action-record.md` — 详细操作日志
- `roadmap/roadmap.md` — 完整路线图与优先级分析
- `chatting-with-llm.md` — 技术话题挑战分析
- `brain-storm.md` — 零散想法（GPT-SoVITS加速、图文分离、比例适配等）
- `tried-tasks-sessions-files/` — 历史会话记录与任务分析文档
