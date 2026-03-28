# Topic name // 主题名称

## Topic Description // 主题描述
|====Start of Topic Description====|
TOPIC_Type='None' // 默认是None, 可选: 'Learning' (学习知识/代码, DETAIL里直接贴代码); 'Story' (自由发挥, DETAIL里随便); 'Fanfiction' (同人故事, DETAIL里贴收集来的同人文或剧本，重新演绎加配音); 'ASMR' (自由发挥, DETAIL里随便, 配音会尽量换成悄悄话/轻语, 并降低音量).
------
(you can write your description here freely) // 随便按需要写
|====End of Topic Description====|

## Setting // 设置
|====Start of Setting====|
Style='sfw' // 默认是在工作时安全, 可选: 'nsfw', 即在工作时不安全; 'a little nsfw'.
Time='Multiple times' // 默认是多个时间
Mood='Multiple reasonable mood' // 默认是多种合理的可能的情绪
Context='Characters are spending time together' // 默认是主角们正在一起度过时间
Location='Multiple places' // 默认是多个场所
Dialogue_Language='zh' // 对话字幕语言 / Caption language: 'zh'=中文, 'en'=英文, 'ja'=日文
Voice_Language='zh' // 语音合成语言 / TTS voice language: 'zh'=中文, 'en'=英文, 'ja'=日文
DETAIL_Follow=80 // 角色对DETAIL内容的忠实度: 低=自由发挥, 高=忠实还原 / How closely to follow DETAIL: low=free, high=faithful. 常见预设: Learning=80, Fanfiction=80, Story=60, ASMR=60
DETAIL_Direct_Use_For_Voice=0 // 角色在对话中直接引用DETAIL用于配音的频率: 低=从不直接引用, 高=逐句朗读 / How often characters directly quote DETAIL for voice: low=never, high=read aloud. 常见预设: Learning=20, Fanfiction=90, Story=20, ASMR=20
IF_Print_To_Screen=['None'] // 是否打印DETAIL里Stage的内容到屏幕上，默认是不打印, 可自己设置要打印哪些: ['Stage_1', 'Stage_3', ..., 'Stage_n']; ['All'].
MAX_Real_Time=-1 // 最大现实持续时间, 默认是随机应变, 内容播完为止, 可选持续时间(单位分钟/min): 1, ..., 1440000.
------
Other left soft things // 剩下的随便按需写, 这部分的限制或者说效力是更加轻微的
|====End of Setting====|

## Detail // 细节
|====Start of Detail====|
DETAIL_File='DETAIL-topic-template.md' // 默认是DETAIL-主题名字.md，跟SETTING-主题名字.md在同一个目录下
------
(you can write your description here freely) // 随便按需要写
|====End of Detail====|
