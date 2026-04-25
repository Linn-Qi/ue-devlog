# ue-devlog
My Unreal Engine development log &amp; debugging journey
**UE5 Devlog #00 Fighting UE Default Input System**
Before building my own interaction system, I encountered a critical issue with Unreal Engine's default input setup.
Problem:
UE has its own default input behavior:
- Mouse Left Click → interaction
- ESC → exit / pause
However, this conflicted with my design:
- I wanted E → interact
- ESC → close UI (NOT exit the game)
Challenge:
Even after modifying input settings, the system behavior did not fully change.
Some inputs were still controlled by default engine logic.
This made debugging extremely confusing:
- Some keys worked
- Some didn't
- Some triggered unexpected behaviors
Solution:
I had to manually override the default input system
1. Modify Input Mapping (Enhanced Input) I also checked the project input setup to make sure ESC was not conflicting with my custom IA_Esc logic. In this version, ESC is handled inside my PlayerController.
![debug](./屏幕截图%202026-04-25%20105429.png)
2. Reassign interaction key to E
3. Redefine ESC behavior inside PlayerController
4. Avoid using engine default exit logic
5. Ensure all input flows are controlled by my own system
Result:
- E = interaction
- ESC = controlled UI exit
- No unintended engine behavior yet.
What I learned:
Unreal Engine is powerful, but its default systems can become a hidden constraint.
To build a custom gameplay system, you must take full control over input handling.

UE5 Devlog #01 — Fixing Widget Duplication with State Control
Today I finally solved a problem that blocked me for a long time,
Goal: 
Create a basic interaction system:
Press E → show UI
Press ESC → close UI
Problem:
Every time I pressed E, a new widget was created. Cause:
No state control. The system kept creating new widgets without checking if one already existed.
Solution:I introduced a boolean variable: IsUIOpen.
Logic:
- If IsUIOpen == false → create widget
- If IsUIOpen == true → do nothing
- ESC → remove widget + set IsUIOpen = false
 
Result:
The interaction now works correctly without duplication.                  
E → open                                                ESC → close No duplication
What I learned:
In game systems, input alone is not enough. State management is essential to prevent unintended behavior.
This is a small step, but it marks the beginning of building a stable interaction system.

