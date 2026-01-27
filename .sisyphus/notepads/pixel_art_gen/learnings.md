# Pixel Art Generation Plan

## Learnings
- 16-bit style (limited color palette, blocky feel).
- Use `PIL` (Pillow) library.
- **Template System**: Separating structural definition (rectangles, offsets) from drawing logic.
- **Modular Component Architecture**: 
  - Defined `character_definitions.py` as a central registry for visual parts.
  - Styles are defined as lists of simple drawing primitives (rect, pixel).
  - This avoids external asset dependencies while allowing high customizability.
- **Web Interface**: 
  - Flask serves both the options (`/options`) and the generator (`/generate`).
  - Frontend dynamically builds dropdowns based on the backend definitions.
  - Full localization (Chinese) enhances user experience.
- **Animation Support**:
  - Implemented logic for Idle, Walk, Attack, and Jump.
  - Used GIF for frontend preview ("make it move") and PNG spritesheet for download.
  - Added simple arm logic to support attack animations.
- **Advanced Customization**:
  - **Randomization**: Implemented client-side logic to randomize parts and colors instantly.
  - **Layer System**: Expanded to include "Back" (Capes/Wings) and "Held" (Weapons) layers with specific animation logic.
  - **Visual Tweaks**: Added a background color picker for the preview to handle different contrast needs.
- **CSS Layout Issues**:
  - `transform: scale()` is purely visual and does not push other elements down, leading to overlap.
  - Solution: Use `width/height` in CSS to physically resize the image while maintaining `image-rendering: pixelated`.

## Decisions
- **Data-Driven Drawing**: Instead of hardcoding "draw_head", "draw_body", the composer now iterates through a layer list and looks up definitions. This makes adding new styles (e.g., "Orc Head", "Wizard Hat") as simple as adding an entry to the dictionary.
- **Self-Contained**: Sticked to procedural generation (drawing rectangles) rather than loading PNG assets to fulfill the prompt's implied constraints and keep the solution portable.
- **UI Layout**: Used a sticky sidebar for the preview panel to prevent it from scrolling off-screen when the option list grows long.
- **Hand Anchoring**: To support weapons, I implemented a simple "Hand Calculation" logic in `gen_character.py` that determines the (x,y) of the right hand based on the current animation frame, then anchors the weapon to that point.

## Completed Tasks
- Generated scripts for Character, Monster, Scene.
- Refactored Character to use Template/YAML.
- Created Web App (Flask) for real-time adjustments.
- Localized Web UI to Chinese.
- Implemented **Modular Part System** (Head, Hair, Body, Legs, Eyes).
- Expanded asset library (5+ styles per category).
- Added **Animation Preview (GIF)** and **Spritesheet Download**.
- Added **Randomization**, **Back Items**, **Weapons**, and **Preview Background Color**.
- Fixed **Layout Overlap** issues.
