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

PASSED:
conda activate a2d-studio ; python quick_start.py

start git (git.md).
please use git when change things.

where is the output file? fixed.

PHASE 1 seem passed.


thanks. you are so good. lets go to next stage.
(1)
use real characters ema and hiro in D:\aaa-new\setups\a2d-studio\ref\Character-fig-setting-example.
use real D:\aaa-new\setups\a2d-studio\ref\.env to access LLM.
to try.
to simply, topic is 'Chatting before sleep'.
(2)
we need to add a change-able limit that each character says <= 5 sentences.
(3)
and i prefer to set default languages to be chinese and japanese:
【期待】这么晚来找我，是有什么事情吗？（高兴地伸了个懒腰）<こんな遅くに私を訪ねてくるなんて、何か用事があるの？>
at phase 1, default Sample LLM output is chinese and english:
【高兴】今天天气真好呀！（高兴地伸了个懒腰）<The weather is wonderful today!>
(4)
and we need to add default settings to .env.

the topic should not be set in .env.
i prefer the topic to be a .md which put outside like characters.

please make sure LLM can only choose emotions which the real character really has (there are corr {emotion}.png files in {character}/fig/). 
(actually, some emotions are named not like emotions, such as 发现问题.png, but never mind, just dynamic load them and send to LLM)

thanks. i check the .json and find some need to improve.
(1)
the character name not show properly.
it should be such as 'hiro' or 'ema'.
```
"index": 0,
      "character": "character_name",
```
(2)
the action should use real character name, not things like "对方".
it should be such as 'hiro' or 'ema'.
```
"action": "走近摸了摸对方的额头",
```
(3)
it seems better to add a style setting to {topic}.md.
style can be 'nsfw' or 'sfw' or 'a little nsfw'.
based on the lingchat experience and my exp, it is ok to set 'a little nsfw' by default. 
(4)
it seems better to add a location setting to {topic}.md.
for example, for chatting-before-sleep.md, set location to be bedroom.

the example way to get tail of run:
```
# 1. Force PowerShell to use UTF-8 for everything
$OutputEncoding = [Console]::InputEncoding = [Console]::OutputEncoding = [System.Text.UTF8Encoding]::new()
# 2. Force Python to use UTF-8 mode
$env:PYTHONUTF8 = 1
# 3. Run your command (using Select-Object to get the tail)
python .\quick_start.py 2>&1 | Select-Object -Last 50
```


<!-- **Phase 2**: Multi-character context → Character alternation → Emotion validation
**Phase 3**: Translation → Token management → Long context handling -->
