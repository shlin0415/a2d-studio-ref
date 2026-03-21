```markdown
# Design System Strategy: Modular Atmospheric Studio

## 1. Overview & Creative North Star
**Creative North Star: The Dimensional Narrative**
This design system moves away from the "flat web" to embrace a workspace that feels like a high-end physical studio. The goal is to reflect the modular nature of AI dialogue generation by treating the UI as a series of **Regions** and **Layers**. We reject the generic "dashboard" look in favor of an editorial, tech-forward interface where content is framed rather than boxed, and hierarchy is communicated through light and depth rather than lines.

### The Editorial Shift
Traditional UIs use heavy borders to separate tools. In this system, we use **Tonal Layering**. By shifting the background values between `surface` and `surface-container` tiers, we create a natural flow that allows the user’s eye to distinguish between the "Main Text Region," the "Character Palette," and the "Timeline" without visual clutter.

---

## 2. Color Palette & Surface Philosophy
The palette is a sophisticated interplay of deep charcoals (`#0c0e10`) and slate, punctuated by high-energy electric pulses.

### The "No-Line" Rule
**Explicit Instruction:** Do not use 1px solid borders to section off major UI areas. 
- Use `surface-container-low` for the base background.
- Use `surface-container-highest` for active modular regions (e.g., the "Main Text/Fig Region").
- Use `surface-container-lowest` to "recess" secondary tools like the Timeline.
Separation is achieved through these value shifts.

### Glass & Gradient Accents
- **Glassmorphism:** For floating controls or settings overlays, use semi-transparent variants of `surface-bright` with a `20px` backdrop-blur. This keeps the AI generation context visible while focusing the user.
- **Signature Gradients:** Primary CTAs (like "Generate Voice") should utilize a subtle linear gradient from `primary` (#6dddff) to `primary-container` (#00d2fd). This adds a "lithic" quality to interactive elements, making them feel tactile.

---

## 3. Typography
We utilize a dual-typeface system to balance technical precision with expressive dialogue.

- **Display & Headlines (Space Grotesk):** This typeface is used for system headers and "Regions." Its geometric, tech-forward rhythm signals the "AI" aspect of the tool. Use `headline-lg` for primary region titles to create an authoritative, editorial anchor.
- **Body & Labels (Manrope):** This is the workhorse. It is chosen for its extreme legibility in dark environments.
    - **Character Chat Text:** Should utilize `body-lg` with increased line-height (1.6) to ensure long-form dialogue remains readable during rapid generation.
    - **Metadata:** Use `label-sm` in `on-surface-variant` for non-essential technical data.

---

## 4. Elevation & Depth
In a "Studio" environment, depth is functional. 

### The Layering Principle
Think of the UI as layers of fine paper or glass:
1.  **Level 0 (Base):** `surface-dim` (#0c0e10).
2.  **Level 1 (Regions):** `surface-container-high`. Use the `xl` (1.5rem) roundedness for these major blocks to give them a "friendly-tech" modular feel.
3.  **Level 2 (Active Elements):** `surface-bright`.

### Ambient Shadows & Ghost Borders
- **Shadows:** Avoid black shadows. Use a tinted shadow based on `surface-container-lowest` with a blur of `32px` and `4%` opacity. It should feel like an ambient occlusion glow, not a drop shadow.
- **Ghost Borders:** If an element needs extra definition (like an Input field), use `outline-variant` at `15%` opacity. Never 100%.

---

## 5. Components

### The "A2D" Buttons
- **Primary:** Gradient fill (`primary` to `primary_container`). `label-md` uppercase for a professional, "studio-switch" feel. Radius: `md` (0.75rem).
- **Secondary:** Transparent background with a "Ghost Border" of `outline`. Hover state shifts the background to `surface-container-highest`.

### Character Modules & Regions
- **Containers:** As seen in the wireframes, these must use `xl` (1.5rem) or `lg` (1rem) corner radii. This softens the "Deep Tech" look and makes the avatars feel integrated.
- **No-Divider Lists:** In the timeline or character lists, do not use lines. Use `spacing-4` (1rem) of vertical white space or a subtle background toggle (`surface-container-low` vs `surface-container-high`) on hover.

### Voice Timeline
- Use `surface-container-lowest` for the timeline track.
- Use `tertiary` (#ff51fa) for the playhead or specific "Dialogue Beats" to create a vibrant contrast against the blue/charcoal base.

### Input Fields
- Floating labels using `label-sm`.
- Focus state: A subtle glow of `primary` (20% opacity) around the container, rather than a thick border change.

---

## 6. Do's and Don'ts

### Do:
- **Use Asymmetry:** Place character avatars with intentional breathing room (using `spacing-8` or `12`).
- **Embrace the Dark:** Trust the `surface-dim` palette; don't feel the need to lighten the UI for "clarity." Dark themes feel premium when contrast is controlled.
- **Modular Thinking:** Treat each part of the UI (Timeline, Chat, Character) as a "Layer" that can be visually stacked.

### Don't:
- **Don't use 1px solid lines:** This is the most important rule. If you feel a line is needed, use a background color shift instead.
- **Don't use pure white:** All text should be `on-surface` (#eeeef0) to prevent eye strain against the dark background.
- **Don't crowd the regions:** Follow the spacing scale strictly. Modular UIs fail when elements feel "pasted" too close together. Use `spacing-6` (1.5rem) as your default gutter between regions.