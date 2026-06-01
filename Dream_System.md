# Dream Transformation System

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

**【这里插入：梦境世界最终效果图】**

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

**【这里插入：DreamTransformManager蓝图截图】**

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

**【这里插入：材质Lerp节点截图】**

**【这里插入：材质转换前后对比图】**

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

**【这里插入：Sequencer截图】**

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

**【这里插入：Preview按钮截图】**

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

**【这里插入：镜子触发蓝图截图】**

---

## State Persistence

### Challenge

After the sequence finished, transformed objects returned to their original state.

### Solution

Sequencer settings were modified to preserve transformed states after playback.

This allowed the environment to remain inside the dream state permanently.

### Result

The transformed world persists after the sequence completes.

**【这里插入：Keep State设置截图】**

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

