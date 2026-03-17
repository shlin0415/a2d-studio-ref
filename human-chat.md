

### a2d-studio after task1 and task2
please help me conclude what have been done until now.
you can look files in tried-tasks-sessions-files/.
in brief, it is task1 and task2.
please also look source codes in *-server/ and files in *example/ and *topics/.
NEVER edit existing old files.
create a new file roadmap/what-have-been-down.md and write down your conclution.

thanks. please read roadmap/roadmap-after-task1-task2.md.
and then integrate roadmap/roadmap-after-task1-task2.md and roadmap/what-have-been-down.md, create a new file roadmap/roadmap.md and write down your results into it.
the key point is, i am not clear the order to do things.
which one should do first? which one second?
which one is necessary? which one make sense? which one is not reasonable?
and also important, how to do one thing? are there existing solutions in third_party/?
and also important, how to test if one thing is achieved or failed?
Whenever possible, we should employ the most concise yet reliable approach to implement functionality, utilizing minimal code and minimal external dependencies.
and we should make sure that each step is small, small enough for both LLM and human check.
please write down your opinion, the order and possible solution plans.
this is vital, thank you.
this is a long task, you can stop everywhere if you need and ask us and then continue.
during the task, the only file need to be edited is roadmap/roadmap.md.


thanks. 
1. **Priority order**: Does this order make sense? Any task should be higher/lower priority?
seem ok.
2. **Topic types**: Are the 4 types correct? Should any be added/removed?
seem ok.
3. **Streaming**: Is async dialogue→voice important for your use case, or is batch processing acceptable?
yes, async is important.
4. **Screen/UI**: Should we build from scratch or extend WebGAL? WebGAL has more features but may be complex.
i am not sure. it is better that we do not need to start a webgal. so we can learn from webgal.
5. **Scope**: Is there a specific topic you want to finish first? That could guide prioritization.
emmm, each seem vital.
do you have any other concerns?
if not, we will start phase 1.


Before we start Phase 1, a few concerns to clarify:
1. **Topic Template structure**: The template I proposed has `similarity` and `read_forbidden` fields. For **fanfiction** topics, the `similarity` parameter (0-100%) is tricky - should it apply to:
   - Dialogue only (what characters say)?
   - Or also plot/setting from ## Detail?
   My proposal: `similarity` applies to **dialogue only** - characters paraphrase or copy lines.
   i guess you are right.

2. **Learning topic**: The learn-cuda.md has a ~90 line code block. Should characters:
   - Just discuss the *concepts* (CPU vs GPU timing)?
   - Or also try to explain specific code lines?
   My proposal: Characters discuss key insights, NOT read code directly.
   i guess you seem right. characters NOT read code directly, but can discuss something like the function or the importance of one code line.

3. **Fanfiction is very long**: The fanfiction.md is ~540 lines. This will likely exceed LLM context. Should we:
   - Split fanfiction into multiple "stages" (first 100 lines, next 100 lines)?
   - Or assume LLM handles it (if using large context model)?
   My proposal: Keep as-is for now, let LLM handle. If it fails, add chunking later.
   i think at this place we need to consider the split. i update some for phone.
   because a2d-studio finally need to play on a screen (./screen-server/ ?), there needs split of '## Detail', which need to consider the screen size (pc, 1920 * 1080; phone, 1080 * 2400/2400 * 1080; other sizes), ratio (pc, 16 * 9; phone, 9 * 20/20 * 9; other ratios), font size (such as 16, 20, 24), letter spacing (0.25 letter, 0.5 letter, etc), line spacing (0.5, 1, 1.5, 2, etc). 
   as you say, llm may can not handle it, we may need to write some function codes to help split.
   are there some tools which can simulate the screen?
   and we split stages based on the ## detail text words num and screen size...
   and we can just print the text to .txt or .png or something to let you and me check when developing.
   after we split stages, what will happen to LLM ask?
   will LLM although forget? in my knowledge, the context limit always there.
   i think modern llm can handle at most of the time (128k - 1024k). 
   so the stages just help us to handle when the screen is not big enough.

4. **Testing criteria**: For each small step, I'll verify:
   - Step 1.1: Template file created → Run quick_start.py → Should still work
   - Step 1.2: Each topic type → Generate dialogue → Check output matches expected behavior

5. **Output format change**: Adding `caption_text` and `voice_text` fields will change the JSONL format. Is this backward-compatible with existing code?
   i am not sure, we may need to change accordingly.

**Question**: Should I also look at how WebGAL handles scenarios (for future Screen/UI reference), or dive straight into Phase 1 implementation? 
    emmm, i think you can look at how WebGAL handles scenarios (for future Screen/UI reference), maybe we can find some ways to split stages?

