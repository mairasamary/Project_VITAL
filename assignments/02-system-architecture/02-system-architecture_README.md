# Project VITAL

## Assignment 2 — System Architecture: Understanding the System Under Test

**Week 2 | Team Assignment | OpenEMR**

---

## Purpose

In Assignment 1, you explored OpenEMR from the outside and asked:

> **What does the system do?**

You used OpenEMR as a user, completed realistic workflows, observed its behavior, and identified potential testing opportunities.

In this assignment, you will begin opening the black box and ask:

> **How does the system do it?**

Your team will select or be assigned one OpenEMR workflow and trace it from the user interface toward the implementation and data layer. You will use multiple forms of evidence to build a focused model of the system.

The goal is **not** to reverse-engineer all of OpenEMR. OpenEMR is much too large for that. Instead, you will learn how to investigate one meaningful slice of a large unfamiliar system.

---

## Learning Objectives

By the end of this assignment, you should be able to:

- Move from a user-level understanding of a system toward an architectural understanding.
- Describe a software system at multiple levels of abstraction.
- Use the C4 model to represent system context, containers, and selected components.
- Trace a user workflow through URLs and HTTP requests.
- Locate source-code components associated with an observed system behavior.
- Identify database tables and relationships relevant to a selected workflow.
- Construct a focused dependency model for part of a large software system.
- Use architectural evidence to improve software-testing decisions.
- Distinguish between what you **know from evidence**, what you **infer**, and what remains **uncertain**.

---

## Team and Time Expectations

Work with the same team of **3–4 students** from Assignment 1 unless your instructor specifies otherwise.

All team members should participate in the investigation.

Plan for approximately **3–5 hours of team work outside class**, in addition to guided in-class activities.

---

## Starting Point

Return to the OpenEMR environment and artifacts from Assignment 1.

You should have:

- a working OpenEMR instance;
- your synthetic patient and workflow observations;
- your Exploration Log;
- your System Feature Map;
- your Network observation;
- your initial Testing Opportunities.

You will now investigate one workflow in substantially greater depth.

---

# Part A — Select a Workflow

Your instructor will assign a workflow or approve your team's selection.

Possible workflows include:

1. **Patient registration**
2. **Patient search and demographic update**
3. **Appointment scheduling**
4. **Clinical encounter creation**
5. **Recording vital signs**
6. **Problems / diagnoses**
7. **Medication-related workflow**
8. **Allergy recording**
9. **Clinical note/document workflow**

Your investigation should focus on **one workflow**.

Do not attempt to document the architecture of the entire OpenEMR system.

---

## Define the Workflow Boundary

Before investigating implementation details, define exactly what your team considers the beginning and end of the workflow.

For example:

```text
Workflow: Record Patient Vitals

START
User opens an existing patient encounter
        ↓
User opens the Vitals form
        ↓
User enters vital-sign values
        ↓
User saves the form
        ↓
User returns to the encounter
        ↓
Saved vitals are visible
END
```

Document:

- Workflow name
- Primary user/actor
- Starting condition
- Ending condition
- Main user-visible steps
- Important data involved

This boundary will define the scope of the rest of your architecture investigation.

---

# Part B — Reproduce and Trace the Workflow

Perform your selected workflow again in OpenEMR.

This time, investigate what happens behind the user interface.

Open your browser's **Developer Tools → Network** panel before beginning the workflow.

For the major steps, record relevant HTTP activity.

Your trace should include at least **3 meaningful requests** associated with the workflow.

For each request, record:

| User Action | HTTP Method | URL / Endpoint | Status | Request / Response Observation | Interpretation |
|---|---|---|---|---|---|
| Save patient information | POST | ... | 200 | ... | Appears to submit demographic changes |
| | | | | | |
| | | | | | |

Do not document every image, stylesheet, JavaScript file, or background request.

Focus on requests that appear directly related to the behavior you are investigating.

---

# Part C — C4 Architecture Model

Use the **C4 model** to describe OpenEMR at progressively deeper levels.

Your diagrams should communicate your understanding rather than attempt to capture every implementation detail.

## C4 Level 1 — System Context

Create a **System Context diagram** showing OpenEMR and the people or external systems relevant to your selected workflow.

Consider:

- Who uses OpenEMR?
- What role is performing your workflow?
- Are there external systems involved?
- What is inside versus outside the system boundary?

Keep this diagram high-level.

---

## C4 Level 2 — Containers

Create a **Container diagram** showing the major runtime/technical parts relevant to the Project VITAL OpenEMR environment.

For example, your investigation may identify concepts such as:

```text
User / Browser
      │
      ▼
OpenEMR Web Application
      │
      ▼
Database
```

Your actual diagram should be based on evidence from the Project VITAL environment and OpenEMR documentation/source.

For each container, identify:

- Name
- Responsibility
- Relevant technology, if known
- How it communicates with other containers

---

## C4 Level 3 — Focused Components

Now zoom into the portion of OpenEMR involved in **your selected workflow**.

Identify important components such as:

- pages;
- controllers;
- forms;
- classes;
- services;
- modules;
- functions;
- APIs;
- database-access components;

as appropriate to the workflow.

You do **not** need to document every file involved.

Your goal is to identify enough components to explain how the workflow appears to be implemented.

Your component diagram should connect:

```text
User action
      ↓
Web request / endpoint
      ↓
Relevant application component(s)
      ↓
Data access / storage
```

---

# Part D — Source-Code Investigation

Use the OpenEMR source code corresponding to the course version.

Do **not** investigate the moving development branch if it differs from the version used by the Project VITAL environment.

Locate source files or components that appear relevant to your workflow.

For at least **3 important source-code locations**, record:

| File / Component | Why You Think It Matters | Evidence | Confidence |
|---|---|---|---|
| `...` | Appears to process... | URL, function name, form action, code reference, etc. | High / Medium / Low |
| | | | |
| | | | |

You are not expected to understand every line of PHP.

Instead, practice navigating unfamiliar source code using:

- repository search;
- filenames;
- URLs;
- form actions;
- function/class names;
- database table names;
- imports/includes;
- call relationships;
- comments/documentation;
- IDE navigation tools.

---

## Evidence vs. Assumption

For important architectural claims, distinguish among:

### Observed

You directly saw evidence.

Example:

> The browser sent a POST request to endpoint X when we saved the form.

### Inferred

Evidence strongly suggests a relationship, but you have not completely verified it.

Example:

> File Y appears to process the request because the form action targets it and it references the same fields.

### Unknown

You could not determine the answer with reasonable effort.

Example:

> We could not determine which component performs validation before the database operation.

**It is acceptable to report uncertainty.**

A carefully documented unknown is better than an unsupported architectural claim.

---

# Part E — Focused Data Model / ERD

Investigate the database structures associated with your selected workflow.

You are **not** expected to create an ERD for the entire OpenEMR database.

Create a **focused ERD** containing only the tables/entities needed to explain your workflow.

For example:

```text
Patient
   │
   │ 1:N
   ▼
Encounter
   │
   │ 1:N
   ▼
Vitals / Observation Data
```

Your actual diagram must use the relevant OpenEMR tables and relationships discovered through your investigation.

For each table included, identify when possible:

- Table name
- Primary key
- Relevant foreign keys
- Important fields for your workflow
- Relationship to other included tables

---

## Connect UI Data to Database Data

Choose at least **3 pieces of data** entered or displayed during your workflow.

Trace each one from the user interface to the database as far as you can.

| UI Data | Example Synthetic Value | Table | Column / Field | Evidence |
|---|---|---|---|---|
| Patient DOB | 2000-01-15 | ... | ... | ... |
| | | | | |
| | | | | |

If you cannot determine a field confidently, document the uncertainty.

---

# Part F — Focused Dependency Map

Create a small dependency map showing important dependencies among the components involved in your workflow.

Depending on the workflow, dependencies might include:

- one PHP file including another;
- a class using another class;
- a component calling a service;
- a form invoking an endpoint;
- a component querying a database table;
- a module depending on shared OpenEMR functionality.

For example:

```text
Workflow UI
    │
    ▼
Handler / Endpoint
    │
    ├────► Shared Service
    │
    └────► Data Access
                 │
                 ▼
              Database
```

Your map should be **focused and readable**.

Do not submit an automatically generated graph containing hundreds of files.

---

# Part G — Revisit Your Testing Ideas

Return to the Testing Opportunities your team identified in Assignment 1.

Select **3 testing ideas** related to your chosen workflow.

For each one, explain how your new architectural understanding affects the way you would test it.

Use the following format:

| Week 1 Testing Idea | Architecture Finding | Revised / Improved Testing Strategy |
|---|---|---|
| Attempt to create duplicate patients | Patient records use an internal identifier independent of name/DOB | Test duplicate demographic data and verify that encounters remain associated with the correct internal patient ID |
| | | |
| | | |

Your revised strategy should demonstrate that architecture can influence:

- where you test;
- what data you inspect;
- what dependencies matter;
- what failure modes you consider;
- what level of testing may be appropriate.

---

# Part H — Architecture Questions

As a team, answer the following briefly:

1. What part of the workflow was easiest to trace? Why?
2. What part was hardest to trace? Why?
3. Where did the implementation differ from what you expected after Assignment 1?
4. What architectural dependency seems most important for testing this workflow?
5. If this workflow failed, what other parts of OpenEMR might be affected?
6. What remains uncertain about your architecture model?

---

# Required Deliverables

Submit **one team package** containing:

1. **Workflow Definition**
   - Actor
   - Starting condition
   - Ending condition
   - Main steps
   - Important data

2. **URL / HTTP Workflow Trace**
   - At least 3 meaningful requests
   - User action
   - Method
   - URL/endpoint
   - Status
   - Interpretation

3. **C4 System Context Diagram**

4. **C4 Container Diagram**

5. **Focused C4 Component Diagram**

6. **Source-Code Investigation Table**
   - At least 3 important source-code locations
   - Evidence and confidence for each

7. **Focused ERD**
   - Only entities relevant to your selected workflow

8. **UI-to-Database Trace**
   - At least 3 pieces of data

9. **Focused Dependency Map**

10. **Architecture-Informed Testing Analysis**
    - Revisit 3 testing ideas from Assignment 1

11. **Architecture Questions**
    - Brief responses to all six questions

12. **Evidence**
    - Include only screenshots/code excerpts necessary to support important claims

---

# Diagram Requirements

Your diagrams may be created using an appropriate diagramming tool.

Examples include:

- Mermaid
- PlantUML
- draw.io / diagrams.net
- Lucidchart
- another instructor-approved tool

Diagrams should be:

- readable;
- clearly labeled;
- focused on your workflow;
- stored in a format that can be reviewed;
- accompanied by source when the tool supports text-based diagram definitions.

Visual quality is useful, but **architectural reasoning and evidence are more important than decoration**.

---

# Evidence and Citation Expectations

Architecture diagrams are claims about how a system works.

Therefore, important claims should be supported by evidence.

Evidence may include:

- observed HTTP requests;
- OpenEMR source code;
- database schema;
- configuration files;
- Docker configuration;
- official OpenEMR documentation;
- runtime behavior.

When practical, include the relevant:

- file path;
- function/class name;
- endpoint;
- table/column;
- configuration location;
- source-code line or nearby identifier.

Do not create an architecture diagram based solely on what an AI tool tells you.

---

# Evaluation

This assignment evaluates your ability to investigate and reason about an unfamiliar software system.

You are **not** expected to produce a perfect or complete model of OpenEMR.

You are expected to produce a **focused, evidence-based, internally consistent model** of your selected workflow.

| Criterion | Weight | Evidence of Strong Work |
|---|---:|---|
| **Workflow definition and HTTP trace** | 15% | Workflow boundary is clear and meaningful requests are accurately connected to user actions. |
| **C4 System Context + Container models** | 15% | Diagrams use appropriate abstraction and accurately represent the relevant system environment. |
| **Focused component architecture** | 15% | Important implementation components are identified and relationships are supported by evidence. |
| **Source-code investigation** | 10% | Relevant code locations are identified with clear reasoning, evidence, and appropriate confidence. |
| **Focused ERD + UI-to-database trace** | 15% | Data model is appropriately scoped and connects user-visible information to relevant storage structures. |
| **Dependency map** | 10% | Important dependencies are represented clearly without unnecessary system-wide complexity. |
| **Architecture-informed testing analysis** | 15% | Testing ideas are meaningfully improved using architectural knowledge rather than simply rewritten. |
| **Communication, evidence, and uncertainty** | 5% | Submission is organized, claims are supported, and uncertainty is documented rather than hidden. |
| **Total** | **100%** | |

---

# Use of Generative AI

Generative AI may be used as an **investigation aid**, subject to your instructor's course AI policy.

Appropriate uses may include:

- explaining unfamiliar PHP syntax;
- suggesting search terms;
- helping interpret a code fragment;
- explaining an unfamiliar architectural concept;
- suggesting possible relationships to investigate;
- helping generate diagram syntax after your team determines the architecture.

However, AI output is **not evidence**.

If an AI tool says:

> "OpenEMR stores this information in table X."

your next question should be:

> **How can we verify that?**

Your team is responsible for validating architectural claims against the actual Project VITAL/OpenEMR environment.

Do not provide passwords, credentials, sensitive information, or real patient information to AI tools.

---

## AI Verification Requirement

Include a short **AI Verification Log** if your team uses generative AI.

Document at least **2 meaningful AI-generated claims or suggestions** that you investigated.

| AI Suggestion / Claim | How We Verified It | Result |
|---|---|---|
| AI suggested that component X handles... | Examined endpoint Y and source file Z | Confirmed / Partially confirmed / Rejected |
| | | |

Finding that AI was wrong is **not a failure**.

Recognizing and correcting an unsupported or incorrect AI claim demonstrates good engineering practice.

---

# Looking Ahead

Assignment 1 asked:

> **What does the system do?**

Assignment 2 asks:

> **How does the system do it?**

The next phase of Project VITAL will ask:

> **How do we determine whether it does it correctly?**

Your architecture artifacts should now give you a foundation for deciding:

```text
What are we testing?
        ↓
Where should we test it?
        ↓
What should be isolated?
        ↓
What needs to work together?
        ↓
What evidence tells us that it works?
```

These questions will lead into **unit, integration, system, and acceptance testing**.
