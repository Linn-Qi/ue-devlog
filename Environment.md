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

<img width="3037" height="1808" alt="屏幕截图 2026-05-03 211844" src="https://github.com/user-attachments/assets/e27de46d-4e73-4065-bbae-b1370aa3ec19" />


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

<img width="3278" height="1818" alt="屏幕截图 2026-05-06 135431" src="https://github.com/user-attachments/assets/d97ec700-2a55-4bfa-bcbb-fda60f4300af" />
<img width="1202" height="691" alt="屏幕截图 2026-05-05 152921" src="https://github.com/user-attachments/assets/71ce9f90-7d4a-451e-ac1d-474d37ec771e" />
<img width="2582" height="1780" alt="屏幕截图 2026-05-05 115030" src="https://github.com/user-attachments/assets/21eb32e5-92a5-4bdd-bc7e-aa516ebb9e10" />


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

<img width="3773" height="1504" alt="屏幕截图 2026-06-01 133533" src="https://github.com/user-attachments/assets/da156dbf-6073-4b45-812a-9286c81d659a" />

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

<img width="2293" height="1611" alt="屏幕截图 2026-06-01 103205" src="https://github.com/user-attachments/assets/80e0bad9-cc66-4ee0-88ff-26ca76cbb5cc" />


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

<img width="698" height="640" alt="屏幕截图 2026-05-26 093216" src="https://github.com/user-attachments/assets/e70f7420-5355-42a8-8550-79a4976df625" />


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


<img width="1472" height="792" alt="屏幕截图 2026-06-01 091652" src="https://github.com/user-attachments/assets/bd195f75-588b-4cf9-823c-a008d400a971" />
<img width="1186" height="920" alt="屏幕截图 2026-05-12 212707" src="https://github.com/user-attachments/assets/582da198-44b1-48f6-a5ef-805daf117821" />


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
