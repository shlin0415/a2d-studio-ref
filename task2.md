# GLOBAL VOICE SERVER

thank you very much. 
ok, lets try task2 now.
before we start task2 to build a voice server which can send requests to external tts server (such as GPT-SoVITS) and get returns, lets find out how LingChat and SillyTavern do this. 
i know LingChat can call vits-simple-api. 
i seem to remember LingChat and SillyTavern can call GPT-SoVITS. 
i am not so sure.

NEWS: LingChat and SillyTavern and other external things have been moved to the third_party folder now. Please do not edit files in the third_party folder (which is in .gitignore).

things may help you:
{
    GPT-SoVITS-v2pro-20250604
    Github repo source codes: ~/ref/third_party/GPT-SoVITS
    Runnable tool: ~/ref/third_party/GPT-SoVITS-v2pro-20250604
    go-webui.bat
    Run log: GPT-SoVITS-v2pro-20250604-run.md
}
{
    vits-simple-api-windows-gpu-v0.6.15
    Github repo source codes: ~/ref/third_party/vits-simple-api
    Runnable tool: ~/ref/third_party/vits-simple-api-windows-gpu-v0.6.15
    start.bat
    Run log: vits-simple-api-windows-gpu-v0.6.15-run.md
}
{
    LingChat
    Github repo source codes: ~/ref/third_party/LingChat
    Runnable tool: D:\aaa-new\setups\20260212-lingchat\LingChat
    start.bat
    Run log: lingchat-run.md
}



TTS Priority: Should I prioritize understanding:
vits-simple-api first (simpler, already working in LingChat)?
GPT-SoVITS (more advanced, per-character voice)?
Both equally? 
    Just try GPT-SoVITS first, which is vital.

Voice Server Scope: For Phase 3, should the voice server:
Convert dialogue text → audio (with emotion/speaker mapping)? 
    seem yes.
Support both vits-simple-api and GPT-SoVITS as backends? 
    no, just GPT-SoVITS first, maybe vits-simple-api can be a ref.
Cache generated audio files? 
    seem yes, save to an output folder.
Stream audio or return file paths? 
    not sure, maybe file path.

Character Voice Mapping: How should voices map to characters? 
    the folder name of character and character voice are the same by default, you can check it (character-fig-setting-example-tree.md, character-voice-example-tree.md). 
    let default to be GPT-SoVITS. 
    and let default that the folder name of character and character voice to be the same, and i prefer allow user to manually change, for example, let ema use hiro voice. 
One voice per character (ema = speaker_1, hiro = speaker_2)? 
    seem yes.
Different voices per emotion (ema_happy, ema_sad)? 
    gpt-sovits use ref voice and ref text to control, which can not precisely link to an emotion. 
    vits-simple-api i am not sure. 
    so do not link voice and emotion now.
Load from character folder settings? 
    folder Character-voice-example.

NEWS: Chara Sub Folder names in Character-fig-setting-example have been changed from english to chinese. in normal, if chinese can pass the tests, english can also pass. ema to 艾玛, hiro to 希罗.


the .md is there.
i am not sure if you can access lingchat run tool. 
maybe you can try first? 
there are some bugs when move it to third party.
so it is outside now.
and i am also not sure if lingchat and sillytavern can really call
gpt-sovits. 
never mind, try your best, thanks.


thanks. can you first try to write a small .py demo, input chara voice things from folder Character-voice-example, and send requests to gpt-sovits, and try to get back the gen voice?
i have launched gpt-sovits.
```
D:\aaa-new\setups\a2d-studio\ref\third_party\GPT-SoVITS-v2pro-20250604>runtime\python.exe -I webui.py zh_CN
Running on local URL:  http://0.0.0.0:9874
To create a public link, set `share=True` in `launch()`.
```
please read detail messages for chara voice things from folder Character-voice-example.
```
D:\aaa-new\setups\a2d-studio\ref\Character-voice-example\艾玛\GPT-SoVITS\voice_setting.txt
GPT_SOVITS_TYPE1='v2' 
GPT_SOVITS_TYPE2='v2'
GPT_WEIGHT='manosaba_ema-e15.ckpt'
SoVITS_WEIGHT='manosaba_ema_e8_s864.pth'
DEFAULT_REF_VOICE='./good_ref/0101Adv26_Ema012.wav'
DEFAULT_REF_SETTING='./good_ref/0101Adv26_Ema012.txt'
```
```
D:\aaa-new\setups\a2d-studio\ref\Character-voice-example\艾玛\GPT-SoVITS\good_ref\0101Adv26_Ema012.txt
SPEAK_SPEED=0.95
SECONDS_BETWEEN_SENTENCES=0.5
TOP_K=10
TOP_P=0.9
TEMPERATURE=0.8
WAV_FILE='0101Adv26_Ema012.wav'
REF_TEXT='うん、ノアちゃんは新しくまた何かを描くって言ってた。そのために一旦、白くしたんじゃないかな。'
REF_LANGUAGE='JA'
```
please try to set the above parameters such as SPEAK_SPEED.
please try to input folder Character-voice-example/艾玛, to gen pieces of voice for 'good morning' (english) and '早上好' (chinese) and 'おはよう' (japanese), save to an output folder.
please also try for Character-voice-example/希罗.
attention that the gpt-sovits types of 希罗 and 艾玛 are different.
for 希罗, GPT_SOVITS_TYPE2='v2ProPlus', for 艾玛, GPT_SOVITS_TYPE2='v2'.

wait a second. 
please just use the conda env we used before.
(base) PS D:\aaa-new\setups\a2d-studio\ref> conda activate a2d-studio
(a2d-studio) PS D:\aaa-new\setups\a2d-studio\ref> 
and i seem not launch the api, so please tell me how to do this.

i write a .bat to start the api.
```
set "SCRIPT_DIR=%~dp0"
set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"
cd /d "%SCRIPT_DIR%"
set "PATH=%SCRIPT_DIR%\runtime;%PATH%"
runtime\python.exe api_v2.py -a 127.0.0.1 -p 9880 -c GPT_SoVITS/configs/tts_infer.yaml
@REM runtime\python.exe -I webui.py zh_CN
pause
```
```
INFO:     Started server process [392]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:9880 (Press CTRL+C to quit)
```
and i make sure httpx installed in conda env a2d-studio.
attention that gpt-sovits belong to third party, so its python env is different from conda env a2d-studio. 
and we should not to edit things for third party, if really needed, let me do.
now you seem can continue to try with conda env a2d-studio.

wait a second.
i think it is better to make a voice-server folder.
D:\aaa-new\setups\a2d-studio\ref\voice-server.
and try there.
i make it.
and attention for the folder structure.
structure.md

it seem succeeded but the whole terminal crashed.
i guess it is not your fault.
the result of the gpt-sovits side is in D:\aaa-new\setups\a2d-studio\ref\third_party\gpt-sovits-api-run.md (long).
can you check your env now?
maybe we need to try again.

thanks. you are so good.
i want to try D:\aaa-new\setups\a2d-studio\ref\voice-server\demo_gpt_sovits_voice.py again, to see why the terminal crashed (maybe it is my fault).
this time, please first check your env.
and run demo_gpt_sovits_voice.py, catch the output file to a .out (attention that we are on a windows and vscode github copilot).

thanks.
lets review what we do until now first.
and then we need to build the voice server to accept dialogue-server\output\real_dialogue.json, and generate the corr voice file.
but we seem also need to improve the dialogue-server, to make it clear that which is the real text need to generate voice.
there seem should be caption_text (字幕文本) and voice_text (声音文本).
for dialogue-server\output\real_dialogue.json, the caption_text is chinese, the voice_text is japanese.
and we also need to make sure the action_text will not be used in voice generate.
for example,
{
    "index": 8,
    "character": "艾玛",
    "emotion": "开心",
    "text": "嗯！最喜欢希罗了～",
    "action": "开心地举起双手，配合着让希罗帮她脱下外套",
    "text_jp": "うん！ヒロ大好き～（嬉しそうに両手を上げ、ヒロが上着を脱がせるのに合わせる）",
    "emotion_jp": null,
    "timestamp": null
}
the action_text_jp '（嬉しそうに両手を上げ、ヒロが上着を脱がせるのに合わせる）' is inner text_jp "うん！ヒロ大好き～（嬉しそうに両手を上げ、ヒロが上着を脱がせるのに合わせる）".
the real text need to generate voice is 'うん！ヒロ大好き～'.
and the caption_text is "嗯！最喜欢希罗了～ （开心地举起双手，配合着让希罗帮她脱下外套）", which is text + (action).




❓ Questions Before I Start
Should I modify dialogue-server output format or create a separate transformer that reads the current JSON and creates an enhanced version with caption_text/voice_text_jp?
i prefer improve dialogue-server output format.
For action text extraction: Should I simply remove all text within parentheses （...） from text_jp to get voice_text_jp?
maybe it is stable? i am not sure.
Voice file naming: Should audio files be named like {character}_{index}_{emotion}.wav or something else?
i prefer make a corr .txt file to explain things for the .wav file.
and we may need to make a {dialogue}_voice output folder for each {dialogue}.json file, and put voice files in.
the name of each .wav file can be {character}_{index}.wav, with the {character}_{index}.txt.
and to make sure our system is stable, we need to test 9 different groups. caption_text can be {english, chinese, japanese}. voice_text can also be {english, chinese, japanese}. so 3 * 3 = 9.
please make a plan first, thanks.



❓ Before Implementation: Clarifications Needed
Caption Language Default: Should dialogue-server default to Chinese captions, or should I allow user to specify via PromptBuilder?
    this is vital, allow user to set first.
    we may need to create a dialogue-topic-template.md and tell the user to set caption_text_language and voice_text_language.
    and the setting will be written to {dialogue}.json.
    if empty, let the default caption_text_language to be chinese, and the default voice_text_language also be chinese.
    and please name the variable more general.
    do not use suffix like _en.
    for each dialogue, there will only be one kind of caption_text_language and one kind of voice_text_language, in normal cases.
Voice Language Default: Should voice-server default to Japanese voice (as in your example), or read from dialogue output?
    first read from {dialogue}.json which should include the user setting, and if empty, default is chinese.
Action Text Stability: Your regex approach （[^）]*） seems solid. Should I also handle cases like:
Multiple parentheses in one line?
Nested parentheses?
Mixed () and （）?
    yes, please handle these edge cases carefully.
Metadata Format: Should the .txt file use simple KEY=VALUE format (like voice_setting.txt) or JSON?
    maybe better to use JSON.
so please renew the plan, thanks.

you are an ai llm app expert. can you help me? thanks. can you read full-chat-record.md, a2d-studio.txt, to review what we have done?
and please also read AGENTS.md.


1. Read the existing TASK2_ANALYSIS.md and TASK2_INVESTIGATION_SUMMARY.md to see what's already been investigated? yes, thanks.



please read session-ses_3299-1.md.
and there is a new task that a test is needed for gpt sovits to check if it suffer the model change time bottleneck.
can you help me figure out if gpt sovits will suffer the model change time bottleneck when using multi chara voice gen? 
my situation is, two characters, two different models, each one say one sentence at a time, then switch chara.
please refer to demo_gpt_sovits_voice.py.
please help me write a .py file to test the time cost when using only one port (9880).
please help me write a .py file to test the time cost when using two ports (31801, 31802).

How many dialogue turns to test? (e.g., 10 turns = 5 sentences per character, or 20 turns?)
10 turns ok.
Test sentences: Should I use the same dialogue from Phase 2 (real_dialogue.jsonl) or simple 固定 sentences like "你好"? 
you can try to use real_dialogue.jsonl.
Pre-requisite: Are there already GPT-SoVITS instances running on ports 31801 and 31802, or should the test script start them? 
yes, i opened all of them.

can you use git to accept these changes.

can you help me run the tests you built.
maybe you need to use similar: 
Ran terminal command: cd "d:\aaa-new\setups\a2d-studio\ref\voice-server" ; conda activate a2d-studio ; $OutputEncoding = [Console]::InputEncoding = [Console]::OutputEncoding = [System.Text.UTF8Encoding]::new(); $env:PYTHONUTF8 = 1; python demo_gpt_sovits_voice.py 2>&1 | Tee-Object -FilePath demo_gpt_sovits_voice.output

i told you to attention the command:
cd "d:\aaa-new\setups\a2d-studio\ref\voice-server" ; conda activate a2d-studio ; $OutputEncoding = [Console]::InputEncoding = [Console]::OutputEncoding = [System.Text.UTF8Encoding]::new(); $env:PYTHONUTF8 = 1; python demo_gpt_sovits_voice.py 2>&1 | Tee-Object -FilePath demo_gpt_sovits_voice.output
do you not understand the utf-8 setting in it?
if you use similar commands to use utf-8, you may succeed.

ok, thanks, maybe you are right. maybe just edit the .py to use utf-8.
please plan first.

it depends on will it break the program.

ok, lets do it and test.

thanks, do you save the generated voice files? i want to check them.

thanks, please make the test py save the voice files and re run the tests.

thank you very much.




do you know how to accept the changes in opencode win desktop app?
you help me git the changes before, but it seem keep the changes and let me check.

