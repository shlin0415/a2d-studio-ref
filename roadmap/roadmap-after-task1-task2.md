
## Roadmap after task1 and task2
## The next stage of a2d-studio task1 and task2

### improvement roadmap 1
Four types of topics:
(1). simple topic such as chatting-before-sleep.md.
(2). learning topic such as learn-cuda.md. 
    in this kind of topic, there will be things such as '## Detail' which record what characters are learning. 
    and characters should/must not read what they are learning directly. 
    we should/must let characters discuss the key points or the trap exprience (踩坑经历) or their feelings (feel difficult, complex or something).
(3). fanfiction (同人文) topic such as fanfiction.md. 
    in this kind of topic, there will be things such as '## Detail' which record the character story directly. 
    and maybe something about writer and website messages which should/must be ignored. 
    so the character chat which LLM return, should/must follow the character story in '## Detail' with 100% - 0% similarity. 
    when 100%, the LLM should/must Restore as closely as possible to the character story in '## Detail', even can use copy.
(4). letter topic such as letter.md. 
    in this kind of topic, there will be things such as '## Detail' which record the letter from someone else. 
    so characters should/must introduce the letter and The Correspondent. 
    if necessary, characters should/must read something in letter directly.
P.S. tried topics are in ./dialogue-topics/. not-tried topics are in ./origin-messy-topics/.

WHAT NEED TO IMPROVE:
(1). SPLIT AND RESIZE. 
    the topics may be long. 
    because a2d-studio finally need to play on a screen (./screen-server/ ?), there needs split of '## Detail', which need to consider the screen size (pc, 1920 * 1080; phone, 1080 * 2400/2400 * 1080; other sizes), ratio (pc, 16 * 9; phone, 9 * 20/20 * 9; other ratios), font size (such as 16, 20, 24), letter spacing (0.25 letter, 0.5 letter, etc), line spacing (0.5, 1, 1.5, 2, etc). 
    LLM may need to split things to N stages, each stage for one page on the screen.
    when return, stage by stage, and also return the start line number and the end line number.
    and if user just want to resize the screen or the font, and do not change other things.
    how to arrange all the texts and voices already prepared? maybe this task is for (./screen-server/ ?).
(2). STRUCTURE. 
    we need to make a topic template, to let the user know how to prepare topics. 
    and the topic should make it clear: 
        A. what is things should follow 100% - 0% (user set parameter);
        B. what is things should not repeat or directly read (such as the codes to learn);
        C. what config should be edited, the edit is tmp for only this topic or forever (user set parameter);
        D. which topic structure is necessary and should always be there, the default values are what.
    and there may be other kinds of topics in the future, so make the topic template more general.
    we need to write annotation to topic template which is clear.
(3). STREAMING OUTPUT. 
    because the topics may be long, we can not wait until LLM finish. 
    once dialogue-server accept one complete unit of voice gen info, the voice-server should read it and generate voice and corr files. 
    so there is an async thing.
(4). EDIT AND REGENERATE.
    because the user may need to edit the .json file which contains the LLM-gen character chats.
    and the user may only edit the subtitle text in one language, and clear the voice text in another language which may be hard for user to edit directly. 
    so we need to use git or something to find out which units are edited, and ask LLM to re generate the voice text.
    so we need to continue the connection with LLM until the user finish edit and say it is ok to stop.
    to avoid send messages to LLM from zero over and over again, which cost much money.
    this task is also a part for (./screen-server/ ?).
(5). SCREEN.
    the ./screen-server/ need to launch such as a webpage or a frontend or a ui page to let users to control.
        A. basic page.
            contain character fig region, character text region, main text/fig/background region, function region (auto play icon, setting icon, timeline, one-step-forward icon, one-step-back icon), Dynamic Notification Pop-up info region, etc. 
            at this place, each step means that one character say one sentence.
            we should allow users to generate different versions of voices for one sentence (gpt-sovits).
            we need to allow users to set N, and try N random refs, and record which refs and voice-gen-settings are tried.
        B. setting page.
            contain all settings and configs that can be edit by user.
        C. cache folder.
            prepare one big folder for each topic, which contains all files needed to play that topic.
            this cache folder can be used on different computers.
            users can restart from the place when something have been done last time.
            first put the cache folder to ./processing-topic-folders/, and if all things finished, put to ./finished-topic-folders/, and allow users to move back to ./processing-topic-folders/ and edit again.

REFERENCE:
    in ./third-party, lingchat, webgal, sillytavern, gpt-sovits. we should learn from these good projects.


