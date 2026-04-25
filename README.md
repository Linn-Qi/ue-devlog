# ue-devlog
My Unreal Engine development log &amp; debugging journey
UE5 Devlog #00 Fighting UE Default Input System
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
 屏幕截图%202026-04-25%20105429.png
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

