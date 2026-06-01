

## Overview

The Dream Transformation System was developed to control large-scale environment transitions during narrative sequences.

The goal was to transform the entire scene from a normal environment into a dream state while keeping all visual changes synchronized.

The system controls:

* Material transitions
* Lighting transitions
* Sequencer events
* Environmental effects
* Story progression

through a centralized manager architecture.

<img width="3216" height="1733" alt="屏幕截图 2026-05-31 163612" src="https://github.com/user-attachments/assets/0be5eef6-9744-44ad-bed0-6d2f0fd630f6" />


---

## Design Goal

The transformation needed to feel like a world-scale event rather than an isolated object animation.

Requirements included:

* Multiple materials changing simultaneously
* Lighting changes occurring in sync
* Story events triggering automatically
* Future scalability for additional effects

---

## Dream Transformation Manager

### Solution

A dedicated Blueprint Manager was created:

**BP_DreamTransformManager**

This Blueprint acts as the global controller for the transformation process.

Responsibilities:

* Start Dream Event
* Control timing
* Trigger material transitions
* Trigger lighting transitions
* Communicate with Sequencer
* Coordinate global state changes

### Result

All transformation logic became centralized and easier to manage.

<img width="2900" height="1352" alt="屏幕截图 2026-06-01 102503" src="https://github.com/user-attachments/assets/57e31d72-7a50-481d-bd85-732930c5087e" />
<img width="2492" height="1083" alt="屏幕截图 2026-06-01 102517" src="https://github.com/user-attachments/assets/f2102a11-ba11-420e-bdfa-72bfdfb7981e" />
<img width="3807" height="1664" alt="屏幕截图 2026-06-01 102848" src="https://github.com/user-attachments/assets/3ef622c9-f196-47f7-a605-9bcbc936cad1" />


---

## Material Transition Workflow

### Challenge

Dozens of scene materials needed to change simultaneously.

Managing individual materials manually would be difficult to maintain.

### Solution

A shared material workflow was created.

Materials expose transformation parameters and blend between two visual states.

The transition is controlled through a single global value.

### Result

Entire environments can transition using one centralized control source.

<img width="3344" height="1685" alt="屏幕截图 2026-06-01 103121" src="https://github.com/user-attachments/assets/edc05500-d05c-48df-bd9c-34e27c3dfd60" />


<img width="3033" height="1626" alt="屏幕截图 2026-05-28 215445" src="https://github.com/user-attachments/assets/862a8458-2cec-4b42-991d-6fac0e728f61" />


---

## Sequencer Integration

### Goal

Synchronize visual transformation with narrative events.

### Workflow

Sequencer was integrated into the Dream System.

This allowed:

* Video playback
* Camera events
* Lighting changes
* Material transitions

to occur at the same moment.

### Result

The transformation feels like a unified cinematic event rather than separate effects.

<img width="3799" height="1953" alt="屏幕截图 2026-06-01 135239" src="https://github.com/user-attachments/assets/81b09ac9-2aa0-4cf1-856d-272db88eb4f9" />


---

## Editor Preview Workflow

### Challenge

Testing the transformation required repeatedly launching the level and replaying the sequence.

This significantly slowed iteration.

### Solution

A custom Preview function was added directly into the Dream System.

The Preview button allows the final dream state to be visualized instantly inside the editor.

### Benefits

* Faster iteration
* Faster debugging
* Easier art direction
* Immediate visual feedback

### Key Takeaway

Building editor-side preview tools significantly improves production efficiency during look development.

<img width="3799" height="1953" alt="屏幕截图 2026-06-01 135239" src="https://github.com/user-attachments/assets/eda8d720-d41d-4325-8a70-850f5d7b6a98" />

---

## Mirror Trigger System

### Goal

Use the mirror interaction as the narrative trigger for entering the dream state.

### Workflow

The mirror event triggers:

* Delayed events
* Object animations
* Visibility changes
* Dream Transformation Manager

The system uses chained Blueprint events to create a staged transformation sequence.

### Result

The dream transition becomes part of the narrative experience rather than a simple visual effect.

<img width="3344" height="1623" alt="屏幕截图 2026-06-01 135516" src="https://github.com/user-attachments/assets/137d6404-e614-49f6-8cdd-f0723ee383d9" />


---

## State Persistence

### Challenge

After the sequence finished, transformed objects returned to their original state.

### Solution

Sequencer settings were modified to preserve transformed states after playback.

This allowed the environment to remain inside the dream state permanently.

### Result

The transformed world persists after the sequence completes.

<img width="2454" height="1559" alt="屏幕截图 2026-06-01 135807" src="https://github.com/user-attachments/assets/63df3911-a9c9-44fd-b3ba-f5b3eaa3365f" />


---

## Technical Highlights

* Global Blueprint Manager
* Centralized Transition Control
* Material Parameter Workflow
* Sequencer Integration
* Editor Preview Tool
* Mirror Trigger Events
* State Persistence System

---

## Key Takeaway

The Dream Transformation System evolved beyond a simple visual effect.

It became a centralized framework for controlling environment transitions, narrative progression, material changes, and cinematic events through a single scalable system.

