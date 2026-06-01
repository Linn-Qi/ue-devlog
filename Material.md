

## **Overview**

This section covers the complete asset production workflow used throughout the project, including modeling, UV preparation, texturing, material development, optimization, and asset integration.

The workflow was built around a simple principle:

**Use the right software for the right task.**

* **Blender** → Modeling, UVs, asset cleanup
* **Substance Painter** → Texturing and material creation
* **Unreal Engine 5** → Material integration, lighting, and final scene assembly

---

## **Asset Validation & Reconstruction**

### **Challenge**

Many downloaded assets appeared visually usable but contained significant production issues.

Common problems included:

* Broken geometry
* Missing textures
* Invalid pivots
* Poor UV layouts
* Excessive polygon counts
* Unstable imported materials

### **Solution**

Instead of relying entirely on downloaded content, critical assets were rebuilt or repaired manually inside Blender.

This process included:

* Asset cleanup
* Geometry correction
* UV reconstruction
* Material reassignment
* Optimization

### **Result**

Project assets became easier to maintain, modify, and optimize.


<img width="3806" height="1869" alt="屏幕截图 2026-05-22 172227" src="https://github.com/user-attachments/assets/faba5acc-3b49-4279-bf26-27cb3c909ffc" />

---

## **Blender Modeling Workflow**

### **Challenge**

Several key environment assets could not be used directly and required reconstruction.

Examples included:

* Windows
* Washing Machine
* Small Props
* Interior Decorations

### **Workflow**

Blender was used primarily for:

* Modeling
* Topology Cleanup
* UV Preparation
* Polygon Reduction
* Basic Animation Setup

### **Key Lesson**

**Proper geometry preparation is critical.**

Even small modeling mistakes can create major problems later during texturing and material development.

### **Result**

Clean geometry significantly improved downstream workflows.

<img width="3791" height="1441" alt="屏幕截图 2026-06-01 142555" src="https://github.com/user-attachments/assets/ad647c60-a1e9-44b1-9e9b-876c126f617b" />

---

## **UV Preparation**

### **Challenge**

Many texturing problems were ultimately caused by poor UV layouts.

Common issues included:

* Stretched textures
* Inconsistent texel density
* Oversized UV islands
* Misaligned projections

### **Solution**

UVs were manually adjusted before entering Substance Painter.

Important considerations:

* Consistent scale
* Proper island placement
* Efficient texture usage
* Avoiding unnecessary stretching

### **Result**

Materials became easier to control and projection workflows became significantly more reliable.

### **Key Takeaway**

**A good texture starts with a good UV layout.**

<img width="925" height="668" alt="屏幕截图 2026-05-15 165902" src="https://github.com/user-attachments/assets/bc03238a-6f92-4205-91d9-b25b34d8adb8" />



---

## **Rapid Asset Production Workflow**

### **Goal**

Create small environmental assets quickly without sacrificing visual quality.

### **Workflow**

1. Generate reference textures using AI tools.
2. Reconstruct simplified geometry inside Blender.
3. Prepare UVs.
4. Import into Substance Painter.
5. Use Projection workflow to transfer details.
6. Export and integrate into Unreal Engine.

### **Advantages**

* Fast production speed
* Good visual quality
* Low asset complexity
* Efficient for small props

### **Example Assets**

* Washing Machine
* Cables
* Small Environment Props

### **Result**

A reusable workflow for rapidly producing supporting environment assets.


<img width="1614" height="930" alt="屏幕截图 2026-05-21 105336" src="https://github.com/user-attachments/assets/b92a87f9-fd31-42ed-9615-59e18103ce39" />

---

## **Substance Painter Workflow**

### **Challenge**

Materials created directly inside Blender often produced inconsistent results after importing into Unreal Engine.

### **Solution**

Substance Painter became the primary texturing tool.

Responsibilities:

* Texture Creation
* Material Detailing
* Projection Workflow
* Surface Variation
* Export Preparation

### **Benefits**

Compared with Blender materials:

* Better texture control
* More predictable UE integration
* Cleaner export workflow
* Improved visual consistency

### **Result**

Substance Painter became the central material production tool within the pipeline.

<img width="1890" height="992" alt="屏幕截图 2026-05-21 140327" src="https://github.com/user-attachments/assets/71eee27f-323f-44ca-b782-924f0103c3e4" />
---

## **Glass Material Development**

### **Challenge**

Glass was one of the most difficult materials in the project.

Problems included:

* Weak reflections
* Missing rain detail
* Poor visibility indoors
* Unreal Engine glass rendering limitations

### **Solution**

Custom glass materials were rebuilt and adjusted using:

* Roughness variation
* Normal blending
* Rain masks
* Dirt masks

Additional interior lighting was introduced to improve readability.

### **Result**

The final material balanced realism and visual clarity.

### **Technical Highlights**

* Rain Streak Shader
* Roughness-Driven Detail
* Reflection Tuning
* Interior Readability Optimization

<img width="1407" height="866" alt="屏幕截图 2026-05-18 132950" src="https://github.com/user-attachments/assets/f21df2e0-ae03-4afa-ad63-f6642ff3a20c" />
<img width="1909" height="1013" alt="屏幕截图 2026-05-17 153348" src="https://github.com/user-attachments/assets/d30734fe-99f8-4023-8671-79073e462ff6" />

---

## **Software Responsibility Separation**

### **Blender**

Used for:

* Modeling
* UVs
* Topology Cleanup
* Basic Animation

### **Substance Painter**

Used for:

* Texturing
* Material Creation
* Projection Workflow

### **Unreal Engine 5**

Used for:

* Material Integration
* Lighting
* Blueprint Systems
* Sequencer
* Final Environment Assembly

### **Key Takeaway**

**Trying to perform every task inside one software often creates unnecessary complexity.**

A dedicated pipeline produces better results and faster iteration.


---

## **Technical Takeaways**

Throughout production, several important lessons emerged:

* Downloaded assets are rarely production-ready.
* UV quality directly affects material quality.
* Substance Painter provides more reliable material workflows than Blender for UE projects.
* Small asset production benefits greatly from structured workflows.
* Glass materials require additional artistic adjustments to remain readable.
* A clear software pipeline dramatically improves efficiency and stability.

