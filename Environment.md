# Environment Art Pipeline

## Overview

This environment was developed through an iterative production workflow combining environmental storytelling, lighting design, technical validation, and real-time optimization.

The goal was not only to create a visually appealing scene, but also to support narrative delivery, player navigation, and future gameplay interactions.

<img width="1785" height="1057" alt="屏幕截图 2026-05-22 113804" src="https://github.com/user-attachments/assets/e979823a-bf38-489a-a8a3-2e777af62d99" />
<img width="3208" height="1593" alt="屏幕截图 2026-05-31 163056" src="https://github.com/user-attachments/assets/730fa32b-0bd0-4bd8-a630-4da66ad75dfa" />


---

## Phase 1 — Whiteboxing & Spatial Exploration

### Goal

Establish the overall spatial structure before investing time into assets and materials.

### Workflow

The environment was initially built using simple whitebox geometry.

Focus areas:

* Room proportions
* Navigation flow
* Camera composition
* Interaction locations
* Storytelling layout

At this stage, visual quality was intentionally ignored.

The objective was to validate space and player movement as early as possible.

### Result

A playable environment structure was established before asset production began.

<img width="1570" height="1678" alt="屏幕截图 2026-06-01 132706" src="https://github.com/user-attachments/assets/b44578e5-13c7-4a50-b31e-eedab33f29d8" />


---

## Phase 2 — Lighting Exploration

### Challenge

The scene relied heavily on atmosphere and environmental storytelling.

Lighting needed to guide player attention while supporting the emotional tone of the narrative.

### Workflow

Instead of waiting until the end of production, lighting development started immediately after the whitebox stage.

Key goals:

* Establish visual focal points
* Define player navigation paths
* Build emotional contrast
* Test environmental mood

### Result

A clear visual language was established before asset integration.

This allowed lighting to become part of the design process rather than a final polish step.

<img width="2893" height="1499" alt="屏幕截图 2026-05-01 164334" src="https://github.com/user-attachments/assets/29368e38-3562-46a7-b587-290bf0bfa5da" />
<img width="1697" height="1486" alt="屏幕截图 2026-05-01 164218" src="https://github.com/user-attachments/assets/614b42e9-7305-428f-adec-4198f6796cec" />
<img width="2744" height="1508" alt="屏幕截图 2026-05-01 164425" src="https://github.com/user-attachments/assets/67b92759-9b4a-4111-a507-597f8eb0b8bf" />

---

## Phase 3 — Large Scale Asset Integration

### Workflow

After the environment layout and lighting direction were approved:

* Downloaded assets were imported in bulk
* Scene composition was prioritized over asset quality
* Materials were left unrefined during early assembly

The objective was to evaluate:

* Scene density
* Composition
* Visual balance
* Narrative potential

before entering the refinement phase.

### Result

A complete environmental prototype was created rapidly, allowing faster iteration and evaluation.



---

## Lighting Investigation

### Challenge

Multiple Unreal Engine lighting workflows were tested during production.

Explored options:

* Baked Lighting
* Dynamic Lighting
* Lumen

### Observation

Baked lighting produced inconsistent results within this project and reduced iteration speed.

### Final Decision

The project adopted a fully dynamic lighting workflow.

### Reasons

* Faster iteration
* Better artistic control
* Easier debugging
* Compatible with real-time environment transitions
* Supports Dream Transformation System

### Result

Improved workflow flexibility and faster scene development.

**【这里放Lumen或灯光测试截图】**

---

## Environmental Animation

### Challenge

Static environments felt visually lifeless.

### Solution A — Alembic Animation

Environmental cloth motion was simulated in Blender and exported using Alembic Cache.

Pipeline:

Blender Cloth Simulation

↓

Alembic Export (.abc)

↓

Unreal Engine

### Advantages

* Natural movement
* Realistic cloth behavior
* Fast setup

### Limitations

* Limited runtime control
* Difficult to modify after export

**【这里放窗帘Alembic动画截图】**

---

### Solution B — World Position Offset

Additional motion was created directly inside Unreal Engine using World Position Offset animation.

Applications:

* Secondary movement
* Subtle environmental motion
* Real-time parameter control

### Final Workflow

Large Motion:

* Alembic Animation

Small Motion:

* World Position Offset

This hybrid workflow provided both realism and runtime flexibility.

**【这里放WPO材质节点截图】**

---

## Environment Validation

### Challenge

As scene complexity increased, asset quality issues became more noticeable.

Common issues included:

* Incorrect pivots
* Collision errors
* Scale inconsistencies
* Broken imported assets

### Solution

A dedicated validation pass was performed throughout production.

Validation areas:

* Scale
* Pivot placement
* Collision setup
* Asset organization

### Result

Improved scene stability and reduced debugging time later in production.

**【这里放碰撞检测或者调试截图】**

---

## Visual Storytelling

Lighting and composition were used as storytelling tools throughout the environment.

Design considerations included:

* Warm vs cool contrast
* Player guidance
* Visual focal points
* Emotional atmosphere
* Narrative framing

The objective was to support storytelling through environmental design rather than relying solely on dialogue or UI.

**【这里放最终效果图】**

---

## Key Takeaway

The environment production process evolved from simple scene assembly into a structured workflow involving:

* Spatial design
* Lighting development
* Asset integration
* Environmental animation
* Technical validation
* Real-time optimization

The final result combines artistic direction with technical implementation to create an interactive narrative environment.
