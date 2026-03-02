1, find out how LingChat and SillyTavern get character chatting with LLM API KEY, especially for SillyTavern multi character chatting with a long topic (1000+ words).

# Which components are most important to you?
Character emotion management system?
LLM API integration (prompting, context handling)?
Multi-character conversation orchestration?
Long context management (1000+ words handling)?
these are all vital.

# Specific concerns:
How do they maintain character consistency across long conversations?
How do they manage token limits with large contexts?
How do they handle multi-character interactions?
these are all vital.

# Your end goal:
Are you building a similar system? 
Integrating these systems?
Understanding best practices?
All yes. i want to build a server.
listen to input characters (folders), topic (a tool doc or a daily scene).
server arrange, send prompts to LLM.
LLM return structured dialogue script/dialogue playbook, which contain characters, emotions, talks, actions (which can be achieved by frontend codes and character figs, such as jump).
support english, chinese, and japanese.
server arrange, check, correct format, save.

# LingChat 
lingchat default is that a user chat with a character.
what i want to build is different.
user not join, just look.
lingchat is more complex with voice and more things.
let us start with a simpler one.
it is just task1 now.

maybe Examine the LingChat source (~/ref/LingChat) for prompt/emotion logic and Check SillyTavern source (~/ref/SillyTavern) for multi-character orchestration will help you find good workable examples.

(base) PS D:\aaa-new\setups\a2d-studio\ref> conda activate a2d-studio
(a2d-studio) PS D:\aaa-new\setups\a2d-studio\ref> 

lets try to code for phase 1 first. 
Phase 1 (MVP): Character loader → Prompt builder → LLM integration → Parser → JSONL output

Successfully installed aiohappyeyeballs-2.6.1 aiohttp-3.13.3 aiosignal-1.4.0 async-timeout-5.0.1 attrs-25.4.0 frozenlist-1.8.0 multidict-6.7.1 propcache-0.4.1 pyyaml-6.0.3 yarl-1.23.0
(a2d-studio) PS D:\aaa-new\setups\a2d-studio\ref\dialogue-server> python quick_start.py
Traceback (most recent call last):
  File "D:\aaa-new\setups\a2d-studio\ref\dialogue-server\quick_start.py", line 13, in <module>
    from dialogue_gen.character_loader import CharacterLoader
  File "D:\aaa-new\setups\a2d-studio\ref\dialogue-server\dialogue_gen\character_loader.py", line 14, in <module>
    from .models import CharacterSettings
ModuleNotFoundError: No module named 'dialogue_gen.models'

