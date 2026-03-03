NEWS: LingChat and SillyTavern and other external things have been moved to the third_party folder now. Please do not edit files in the third_party folder (which is in .gitignore).

ok, lets try task2 now, before we start task2 to build a voice server, lets find out how LingChat and SillyTavern send requests to external tts server (such as GPT-SoVITS) and get returns. i know LingChat can call vits-simple-api. i seem to remember LingChat and SillyTavern can call GPT-SoVITS. i am not so sure.
things may help you:
{
    GPT-SoVITS-v2pro-20250604
    Github repo source codes: ~/ref/third_party/GPT-SoVITS
    Runnable tool: ~/ref/third_party/GPT-SoVITS-v2pro-20250604
    go-webui.bat
}
{
    vits-simple-api-windows-gpu-v0.6.15
    Github repo source codes: ~/ref/third_party/vits-simple-api
    Runnable tool: ~/ref/third_party/vits-simple-api-windows-gpu-v0.6.15
    start.bat
}

