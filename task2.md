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
the result of the 