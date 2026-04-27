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

**UE5 Devlog #01 — Fixing Widget Duplication with State Control**
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
 ![debug](./屏幕截图%202026-04-25%20212952.png)
Result:
The interaction now works correctly without duplication.                  
E → open                                                ESC → close No duplication
What I learned:
In game systems, input alone is not enough. State management is essential to prevent unintended behavior.
This is a small step, but it marks the beginning of building a stable interaction system.
---

UE5 Devlog #02 — Fixing Self Reference & PlayerController Interaction System

Today I fixed a core issue in my UE5 interaction system: how to correctly pass the interaction object (Self) into the PlayerController and build a stable E / ESC UI workflow.

---

### 1. Problem

My initial setup had the following behavior:

* Overlap detection worked (Press E UI showed correctly)
* E key was detected but UI did not open reliably
* ESC key could not close UI
* IsValid and Branch logic seemed inconsistent
* UI sometimes duplicated or failed to respond

This made the system feel unstable and hard to debug.

### 2. Root Cause

The issue came from two main problems:

1. The interaction object (Self) was not reliably passed into PlayerController
2. I mixed two different concepts in my logic:

* Interaction state (what I can interact with)
* UI state (what is currently open)

Because of this, input handling became unpredictable.

### 3. Fix — Correct Self Transmission

Inside my BP_InteractiveObject:

On Begin Overlap:

* Cast to Character
* Get Controller
* Cast to PlayerController
* Pass Self into PlayerController

Set:

CurrentInteractObject = Self

This ensures that the PlayerController always knows which object is currently interactable.

(Insert Blueprint Screenshot Here)

---

### 4. System Design — Separate Responsibilities

I rebuilt the logic using three variables in PlayerController:

* CurrentInteractObject → what the player can interact with
* CurrentUI → the currently opened UI
* IsUIOpen → whether a UI is open

This separation is the key to making the system stable.

### 5. E Key — Open UI Logic

E key is responsible for interaction.

Flow:

* Check IsValid(CurrentInteractObject)
* Check IsUIOpen

If:

* Object is valid
* UI is NOT open

Then:

* Create Widget
* Set CurrentUI
* Add to Viewport
* Set IsUIOpen = true

This prevents UI duplication and ensures only one UI exists at a time.

(Insert Blueprint Screenshot Here)


### 6. ESC Key — Close UI Logic

ESC is responsible only for UI control.

Flow:

* Check IsUIOpen

If true:

* Remove CurrentUI from parent
* Clear CurrentUI
* Set IsUIOpen = false

Important:

ESC does NOT depend on CurrentInteractObject anymore.
This fixes the issue where UI could not close after leaving the object.

(Insert Blueprint Screenshot Here)


### 7. Debug Issue — Persistent Blue Text

I encountered a constant blue debug text on screen.

Cause:

* Print String node using a Key
* It created a persistent debug display

Fix:

* Remove Key
* Or disable “Print to Screen”


### 8. Result

After restructuring:

* E opens UI reliably
* ESC closes UI correctly
* No duplicate widgets
* Multiple interactable objects work correctly
* System behavior is stable and predictable

### 9. Key Takeaway

The most important lesson:

Do NOT mix interaction state and UI state.

CurrentInteractObject = what I can interact with
CurrentUI = what is currently open

Separating these two concepts fixed almost all issues.


### 10. Next Step

This system can now scale into:

* Dialogue UI
* Door interaction UI
* Reading / narrative UI

Next upgrade:

Each interactable object will have its own UI Class
PlayerController will dynamically create the correct UI based on the object
