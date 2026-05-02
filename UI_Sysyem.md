
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

<img width="2510" height="1723" alt="屏幕截图 2026-04-27 164431" src="https://github.com/user-attachments/assets/c33964a5-d5f6-465e-a098-687a884f3cd0" />

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

<img width="1982" height="1234" alt="屏幕截图 2026-04-27 164400" src="https://github.com/user-attachments/assets/b2222cc1-0628-4a3f-a304-d6fb65f43b93" />
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

**UE5 Devlog #03: Interaction system restructuring + dynamic interaction + video UI (working version)**
Today was not about a single feature, but more about restructuring the whole interaction system and pushing it into a more usable state.
1. Interaction system restructuring (main task)
The biggest change today was reorganizing the responsibility between PlayerController and InteractObject.
Before

•	PlayerController was handling too much
•	It was directly controlling interaction content (UI, actions, etc.)
•	The structure was messy and hard to extend
After

•	PlayerController
o	Handles input only (E / ESC)
o	Keeps track of state (CurrentInteractObject, CurrentUI, IsUIOpen)
•	InteractObject
o	Handles actual interaction behavior
o	(create UI, play animation, trigger logic)

What I changed
•	Moved interaction logic out of PlayerController into InteractObject
•	Added functions to standardize interaction calls
•	Introduced BPI (Blueprint Interface) for communication
Result
•	Interaction logic is much cleaner now
•	Easier to scale to multiple objects
•	Previous bugs (mainly call chain issues) are fixed
2. Communication setup (BPI)
Used BPI as the main communication layer between systems.

Purpose
•	Let PlayerController trigger interactions without knowing details
•	Make different interact objects share the same interface
•	Prepare for future extensions (UI / animation / other events)

3. New interaction type: moving object (sphere)
Today I tried a different type of interaction instead of the usual “open door”.
What’s different
•	This one includes movement logic
•	Not just triggering animation
•	Needs its own behavior handling

Takeaway
This helped test whether the current interaction structure is flexible enough.
So far, it works.
4. ESC closing logic (important)
Added a proper ESC-based UI closing system.


How it works
•	Controlled by PlayerController
•	CurrentUI stores the active UI
•	IsUIOpen controls state

Result
-	Full UI lifecycle is now complete
-	(open → interact → close)
-	Works consistently with E key logic

5. Video UI system (major progress)
This was the most frustrating part earlier, but today it finally works.
1. Material issue (critical fix)
Previous problem:
-	Video was always black


Fix:
-	Changed material type from Surface → User Interface

-	Connected Media Texture correctly to Emissive
2. Playback issue
Before:<img width="2119" height="988" alt="屏幕截图 2026-04-28 220420" src="https://github.com/user-attachments/assets/32403a54-4319-4779-a8b6-83655ce92a9e" />

-	UI opened but video didn’t play
-	Frame was stuck
Now:
-	Video plays normally
-	Tested multiple times, consistent
-	Trigger feels smooth

Current understanding (not fully confirmed)
The issue was probably related to:
•	Media Player initialization timing
•	Execution order between UI creation and Play call
•	Blueprint execution flow
(Not fully isolated yet, but system is working now)

6. Key takeaway
Today was less about “making something work” and more about:
→ turning a messy setup into something structured and reusable
What improved:
•	Clear separation of responsibility
•	Consistent communication (BPI)
•	Multiple interaction types working
•	UI lifecycle fully connected

7. Next step
•	Extend this system to:
o	subtitle UI
o	animation UI
o	scene triggers
•	Apply video UI to actual demo scene (mirror sequence)
•	Test stability in more complex setups
Summary

**UE5 Devlog #04: Interaction Order & Prompt Control+Prompt UI Showing Incorrectly**

Today was the first time the interaction system started to feel like an actual system, not just scattered functions.
Devlog – Interaction Order & Prompt Control

**Problem 1: Interaction Order Chaos**
Issue
All interactable objects could be triggered regardless of progression.
Players could interact with later-stage objects before completing earlier ones, breaking the intended flow.

Cause
Interaction logic had no restriction based on progression.
EnterInteractRange would register any object as valid, without checking whether it should be available at the current stage.
<img width="2493" height="1503" alt="屏幕截图 2026-05-01 164041" src="https://github.com/user-attachments/assets/3a937dff-454d-4d2c-995e-a149df1e71ae" />

Solution
Introduced a stage-based interaction control system:
<img width="2421" height="1369" alt="屏幕截图 2026-05-01 163944" src="https://github.com/user-attachments/assets/92c10a15-c29c-4b8e-8632-dc35c806dcf2" />

Each interactable object has a variable: RequiredStage
PlayerController maintains: CurrentStoryStage
Before allowing interaction:

RequiredStage == CurrentStoryStage

<img width="742" height="370" alt="屏幕截图 2026-05-01 162701" src="https://github.com/user-attachments/assets/6fba61e1-d2ec-400d-9706-f703296b6360" />

Only if the condition is true:

Set CurrentInteractObject
Allow interaction
Result
<img width="2309" height="1244" alt="屏幕截图 2026-05-01 163053" src="https://github.com/user-attachments/assets/20925811-69bc-4c0b-aa19-dfd7d84788bf" />


-Interaction now follows a strict sequence
-Player cannot skip ahead
-System is scalable for future level design

**Problem 2: Prompt UI Showing Incorrectly**

Issue
“Press E” prompt appeared on all interactable objects, even when they were not supposed to be interactable yet.

This created confusion:
<img width="2421" height="1369" alt="屏幕截图 2026-05-01 163944" src="https://github.com/user-attachments/assets/74006423-38f7-464a-a1fd-ebd31a7cc841" />

Player sees prompt
But interaction is invalid
Feels like a bug

-Cause
Prompt display logic was not synchronized with interaction logic.
ShowPrompt was triggered whenever entering overlap range, without checking stage validity.

-Solution
Moved prompt control into stage validation logic:

Prompt is only shown if object passes stage check
Otherwise prompt is not shown
Implementation logic:
<img width="762" height="892" alt="屏幕截图 2026-05-01 162441" src="https://github.com/user-attachments/assets/bba72e72-52b7-4b30-b7d8-2733fc0123ff" />

Cast to InteractBase
→ Get RequiredStage
→ Compare with CurrentStoryStage
→ Branch

True:
Set CurrentInteractObject
Show Prompt

False:
Do nothing

-Result

Prompt only appears on valid objects
-No misleading UI feedback
-Player experience becomes clear and predictable
-Key Takeaways
-Interaction logic and UI feedback must be strictly synchronized
-PlayerController controls global state (stage, current object)
-InteractObject only defines its own requirements and behavior
-System Impact
-Improved system clarity
-Easier debugging
-Better player guidance
Also creates a foundation for:

Story-driven progression
Controlled interaction flow
Future expansion

