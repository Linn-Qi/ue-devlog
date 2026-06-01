# Gameplay Interaction Framework

## Overview

This system was developed to build a **scalable gameplay interaction framework** inside Unreal Engine 5.

Rather than creating isolated interaction events, the goal was to establish a reusable architecture capable of supporting UI interactions, object interactions, progression systems, video playback, and future gameplay expansion.

The framework combines:

* **Input Management**
* **State Control**
* **Blueprint Communication**
* **UI Lifecycle Management**
* **Interaction Progression Validation**

into a unified gameplay interaction architecture.

---

## System Architecture

### Core Design

**PlayerController** is responsible for:

* Input handling
* Interaction state management
* UI state management
* Active object tracking

**InteractObject** is responsible for:

* UI creation
* Animation triggering
* Object-specific logic
* Story events

This separation keeps interaction logic scalable and easy to maintain.

---

### Architecture Diagram

<img width="2405" height="1352" alt="屏幕截图 2026-06-01 124543" src="https://github.com/user-attachments/assets/796a0005-78a8-4d1e-882f-e0d43a3ba403" />


---

## Input System

### Challenge

Unreal Engine's default input behavior conflicted with the custom interaction workflow.

Required controls:

* **E = Interact**
* **ESC = Close UI**

### Solution

Implemented a centralized **PlayerController input workflow** using Enhanced Input.

All interaction requests pass through a single control layer before executing gameplay logic.

### Result

* Stable interaction handling
* Predictable input behavior
* Easier debugging

<img width="2301" height="1442" alt="屏幕截图 2026-05-01 163952" src="https://github.com/user-attachments/assets/ff6e620a-b867-48e7-b7e0-8bf8543409d3" />

---

## UI Lifecycle Management

### Problem

Every interaction key press created a new widget instance.

This resulted in:

* Duplicate UI creation
* Input conflicts
* Unstable behavior

### Solution

Introduced a **state-driven UI management system**.

Core variables:

* **IsUIOpen**
* **CurrentUI**

Before creating a widget, the system validates current UI state.

### Result

* No duplicate widgets
* Stable UI lifecycle
* Consistent user experience

<img width="2866" height="1646" alt="屏幕截图 2026-06-01 102423" src="https://github.com/user-attachments/assets/1fb272b9-39a1-42b0-b2d4-70a81d75b82f" />


---

## Interaction State Management

### Core Variables

* **CurrentInteractObject**
* **CurrentUI**
* **IsUIOpen**

Each variable serves an independent responsibility.

### Key Design Decision

**Interaction State and UI State must remain independent.**

Separating these responsibilities eliminated multiple interaction bugs throughout development.

### Result

* Cleaner architecture
* Easier debugging
* Better scalability

<img width="2734" height="1825" alt="image" src="https://github.com/user-attachments/assets/973033d4-dce7-4f0a-9063-050bc3209f25" />


---

## Blueprint Interface Communication

### Goal

Reduce coupling between systems.

### Solution

Implemented **Blueprint Interface Communication**.

PlayerController triggers interactions without needing implementation details from individual objects.

Every interactable object follows the same communication contract while maintaining its own behavior.

### Benefits

* Scalable architecture
* Easier maintenance
* Faster feature expansion

<img width="2686" height="1630" alt="屏幕截图 2026-05-22 222645" src="https://github.com/user-attachments/assets/f16d5b3a-66ab-4e50-87b1-f5fdf6584fa4" />


---

## Stage-Based Progression System

### Goal

Control interaction order throughout gameplay.

### Implementation

Each interactable object contains:

* **RequiredStage**

PlayerController maintains:

* **CurrentStoryStage**

Interaction becomes available only when:

**RequiredStage == CurrentStoryStage**

### Result

* Controlled progression
* Narrative sequencing
* Prevented premature access

<img width="762" height="892" alt="屏幕截图 2026-05-01 162441" src="https://github.com/user-attachments/assets/82251822-6642-4cb9-b8e9-53e90b160804" />
<img width="742" height="370" alt="屏幕截图 2026-05-01 162701" src="https://github.com/user-attachments/assets/5759caee-a882-48fb-8839-b3530a0fef39" />


---

## Video UI Integration

### Problem

Video playback initially failed.

Media assets appeared correctly configured but rendered as a black screen inside UI widgets.

### Investigation

Tested:

* Media Player
* Media Texture
* UI Materials
* Media Playlist

The Media Playlist introduced conflicts within the playback workflow.

### Final Pipeline

**File Media Source**

↓

**Media Player**

↓

**Media Texture**

↓

**UI Material**

↓

**Widget**

### Result

Stable video playback inside narrative UI sequences.

<img width="3756" height="1629" alt="屏幕截图 2026-06-01 102658" src="https://github.com/user-attachments/assets/8f50d325-370a-4ab8-b3b1-feb346a1c1f3" />


<img width="3810" height="1810" alt="屏幕截图 2026-05-23 134524" src="https://github.com/user-attachments/assets/5abbb09e-404e-4717-8140-3402719a9c97" />


---

## Technical Highlights

* **Enhanced Input workflow**
* **State-driven UI lifecycle management**
* **PlayerController-centered interaction framework**
* **Blueprint Interface communication**
* **Video playback integration**
* **Stage-based progression control**
* **Reusable gameplay architecture**
* **Structured debugging workflow**

---

## Key Takeaway

The biggest lesson from this project was learning how to transform isolated gameplay features into a structured system.

Instead of solving individual bugs one by one, the focus gradually shifted toward:

* **Architecture Design**
* **State Management**
* **System Communication**
* **Scalability**

The final result is a reusable gameplay interaction framework capable of supporting future UI systems, narrative systems, animation systems, and additional gameplay mechanics.

<img width="1621" height="1006" alt="屏幕截图 2026-06-01 092031" src="https://github.com/user-attachments/assets/db7b6ab3-ecd4-4b43-a42b-f787caad939e" />
