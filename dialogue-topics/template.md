# Topic Template

## IMPORTANT: Stage Splitting
If your topic content is long (e.g., fanfiction), you should manually split it into stages using the stage markers below. This helps with screen display and prevents LLM context issues.

**Default: No stages** - If you don't split, the entire content is treated as Stage_1.

---

## Metadata (Required)
|---Style: {sfw|a little nsfw|nsfw}---|
|---Location: {scene location}---|
|---Mood: {atmosphere, mood description}---|

---

## Topic Description
|====Start of Topic Description====|
{2-3 sentence description of what this topic is about}
|====End of Topic Description====|

---

## Setting
|====Start of Setting====|
- Time: {time of day}
- Location: {place description}
- Context: {what's happening}
- Other: {any additional setting info}
|====End of Setting====|

---

## Key Points
|====Start of Key Points====|
- {Key point 1}
- {Key point 2}
- {Key point 3}
|====End of Key Points====|

---

## Expected Tone
|====Start of Expected Tone====|
{Describe the expected tone of dialogue - e.g., intimate but not romantic, peaceful and comforting, etc.}
|====End of Expected Tone====|

---

## Character Interactions
|====Start of Character Interactions====|
{Describe how characters should interact - their relationship, emotional dynamics, etc.}
|====End of Character Interactions====|

---

## Detail (MAIN CONTENT - For Learning/Fanfiction topics)
|====Start of Detail====|
{This is the main content that characters will discuss/follow/learn from.
For LEARNING topics: Characters should NOT read this directly, but discuss key insights.
For FANFICTION topics: Characters follow this story with the specified similarity %.
For LETTER topics: This is the letter content.
 
Use code blocks for code content.
Use > quotes for content to read aloud.}

|<===Start of Stage_1===>|
{Stage 1 content - first ~100 lines or logical chunk}
|<===End of Stage_1===>|

|<===Start of Stage_2===>|
{Stage 2 content - second ~100 lines or logical chunk}
|<===End of Stage_2===>|

|<===Start of Stage_N===>|
{Stage N content}
|<===End of Stage_N===>|
|====End of Detail====|

---

## Optional Fields
|---Similarity: {0-100}---|
|---ReadForbidden: {regex or pattern to avoid reading directly}---|

---

# EXAMPLE: Simple Topic (No Stages)

|---Style: a little nsfw---|
|---Location: Bedroom---|
|---Mood: Intimate, comfortable, relaxed---|

# Chatting Before Sleep

## Topic Description
|====Start of Topic Description====|
A late-night conversation between two characters before bedtime. The atmosphere is calm, intimate, and reflective.
|====End of Topic Description====|

## Setting
|====Start of Setting====|
- Time: Late evening, just before sleep
- Location: Bedroom
- Context: Characters are winding down for the day
- Other: Intimate space
|====End of Setting====|

## Key Points
|====Start of Key Points====|
- Natural, conversational tone
- References to daily activities or thoughts
- Gentle teasing or playful banter may be appropriate
- Topics may include: tomorrow's plans, today's experiences, feelings, etc.
|====End of Key Points====|

## Expected Tone
|====Start of Expected Tone====|
- Intimate but not necessarily romantic
- Peaceful and comforting
- Occasionally humorous or touching
- Some vulnerability and emotional openness is expected
|====End of Expected Tone====|

## Character Interactions
|====Start of Character Interactions====|
- Characters should feel comfortable with each other
- Dialogue should feel natural, like close friends or partners talking
- Emotional vulnerability is acceptable in this context
- Light physical contact is acceptable
|====End of Character Interactions====|

## Detail
|====Start of Detail====|
This topic has no specific detail content - characters have a free-form conversation about their day, feelings, and plans.
|====End of Detail====|

---

# EXAMPLE: Fanfiction Topic (With Stages)

|---Style: a little nsfw---|
|---Location: School - Classroom and Hallway---|
|---Mood: Sweet, slightly tense, romantic---|
|---Similarity: 80---|

# How to Become Childhood Friend's Girlfriend (Part 1)

## Topic Description
|====Start of Topic Description====|
A sweet school romance where Hiro helps Emma deal with a love letter from another student. This is a fanfiction based on the original story.
|====End of Topic Description====|

## Setting
|====Start of Setting====|
- Time: Lunch break, sunny day
- Location: Classroom and school hallway
- Context: A girl gives Emma a love letter and asks her to meet at the gym
- Other: School setting with students
|====End of Setting====|

## Key Points
|====Start of Key Points====|
- Show Hiro's protective nature toward Emma
- Show Emma's gentle personality
- Include the misunderstanding about the "love letter"
- Build up the romantic tension between childhood friends
|====End of Key Points====|

## Expected Tone
|====Start of Expected Tone====|
- Sweet and heartwarming
- Slight jealousy/possessiveness from Hiro
- Playful banter between the two
- Underlying romantic tension
|====End of Expected Tone====|

## Character Interactions
|====Start of Character Interactions====|
- Hiro and Emma are childhood friends (发小)
- They trust each other deeply
- Hiro is slightly overprotective of Emma
- Emma is gentle and sometimes shy
- There's an underlying romantic tension neither has confessed yet
|====End of Character Interactions====|

## Detail
|====Start of Detail====|
This is a fanfiction based on the original story. Characters should follow the plot points but can paraphrase dialogue.

|<===Start of Stage_1===>|
"Hiro-san!"
A blue-haired girl runs into the classroom, shouting your name.
"You really need to come with me! It's an emergency!"
This is Snowly, your classmate.
"What happened? Is it about Emma?"
"You got it! Someone gave Emma a love letter! And she's supposed to meet them behind the gym at lunch!"
Love letter? You think about Emma's gentle smile, those trusting eyes...
You need to go find her.
|<===End of Stage_1===>|

|<===Start of Stage_2===>|
You rush to the gym and spot a silver-haired girl - it's Emma!
She's talking to a girl you don't recognize.
"So, did you read my letter?"
"I... I haven't had time yet..."
What?! She's reading a letter from another person?!
Your chest feels tight. You step forward.
"Emma!"
Both girls turn to look at you.
"Hiro-san! What are you doing here?"
"I came to... check if you're okay."
The other girl looks uncomfortable and leaves.
"...Was that a love letter?"
Emma blushes pink.
"It's... it's not what you think..."
|<===End of Stage_2===>|
|====End of Detail====|

---

# EXAMPLE: Learning Topic

|---Style: a little nsfw---|
|---Location: University study room---|
|---Mood: Focused, curious, collaborative---|

# Learning CUDA

## Topic Description
|====Start of Topic Description====|
Two characters learn about CUDA programming, specifically comparing CPU and GPU performance for vector addition.
|====End of Topic Description====|

## Setting
|====Start of Setting====|
- Time: Afternoon study session
- Location: University open learning space
- Context: Characters are studying together, one wants to learn about GPU programming
- Other: Computer with CUDA available
|====End of Setting====|

## Key Points
|====Start of Key Points====|
- Understand why GPU is faster for parallel tasks
- Learn about CUDA memory allocation (cudaMalloc)
- See the timing difference between CPU and GPU
- Discuss "Arithmetic Intensity" concept
|====End of Key Points====|

## Expected Tone
|====Start of Expected Tone====|
- Educational but not boring
- Curious and exploratory
- One character explains, the other asks questions
- Some confusion and "aha" moments expected
|====End of Expected Tone====|

## Character Interactions
|====Start of Character Interactions====|
- One character (teacher) knows CUDA basics
- The other (student) is curious and wants to learn
- Patient explanation, lots of questions
- Student may make mistakes and teacher corrects
|====End of Character Interactions====|

## Detail
|====Start of Detail====|
Characters should NOT read the code directly. They should discuss key concepts:

- The code performs vector addition (adding two arrays)
- CPU version uses a simple for loop
- GPU version uses CUDA kernels with thousands of threads
- The key is "parallel" - GPU can do millions of calculations at once
- cudaMalloc is like malloc but for GPU memory
- Timing shows GPU is much faster for large arrays

IMPORTANT: Do NOT read the code block directly. Discuss the CONCEPTS and insights instead.
|====End of Detail====|

---

# SYMBOL REFERENCE

## Section Markers (Use ====)
|====Start of {Section Name}====|
...content...
|====End of {Section Name}====|

Valid sections:
- Topic Description
- Setting
- Key Points
- Expected Tone
- Character Interactions
- Detail

## Stage Markers (Use <===)
|<===Start of Stage_{N}===>|
...content...
|<===End of Stage_{N}===>|

Stages should be used when:
- Content is very long (>100 lines)
- Content naturally divides into distinct parts
- Screen display needs分期显示

## Metadata Markers
|---{FieldName}: {value}---|

Valid metadata:
- Style: sfw | a little nsfw | nsfw
- Location: {location description}
- Mood: {mood description}
- Similarity: {0-100} (for fanfiction)
- ReadForbidden: {regex} (what NOT to read directly)
