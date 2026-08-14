# Project VITAL

## Assignment 1 — System Exploration: Learning the System Under Test

**Week 1 | Team Assignment | OpenEMR**

---

## Purpose

Before you can test a software system effectively, you must understand what it does.

In this assignment, your team will explore **OpenEMR** from a user's perspective. You will complete realistic workflows, observe system behavior, identify major functional areas, and begin recognizing behaviors and risks that should eventually be tested.

During this week, treat OpenEMR primarily as a **black box**. Your goal is not yet to understand its PHP implementation or database schema.

In Week 2, you will move inside the system and investigate how selected behaviors are implemented.

---

## Learning Objectives

By the end of this assignment, you should be able to:

- Navigate and use an unfamiliar, real-world software system.
- Identify major system features, workflows, actors, and relationships.
- Observe and document software behavior systematically.
- Distinguish between successful execution and correct/appropriate behavior.
- Identify risks, questions, and candidate testing opportunities from exploratory use.
- Create an initial functional model of the System Under Test (SUT).

---

## Team and Time Expectations

Work in **teams of 3–4 students**, unless your instructor specifies otherwise.

All team members should actively interact with OpenEMR. Do not assign one person to operate the system while everyone else only watches.

Plan for approximately **2–3 hours of team work outside class**, in addition to guided in-class exploration.

---

## Before You Begin

Your Project VITAL environment must be running, and you must be able to log in to OpenEMR.

Complete the **Project VITAL Student Setup Guide** before beginning this assignment.

> **Data rule:** Use only fictional/synthetic information. Do not enter your own name, date of birth, address, phone number, medical information, or information about any real person.

---

## Scenario

Your team has joined a software quality group responsible for evaluating OpenEMR.

Before designing formal tests, you must become familiar with the product and understand its observable behavior.

Your team will create a fictional patient and follow that patient through several common workflows.

---

# Part A — Guided System Exploration

Complete the tasks below.

The assignment intentionally tells you **what outcome to achieve**, but it does not provide click-by-click instructions.

**Finding how to perform each task is part of the exercise.**

| # | Task | What to Do |
|---|---|---|
| 1 | **Explore the interface** | Identify at least five major functional areas of OpenEMR. Record what you believe each area is used for. |
| 2 | **Create at least 3 synthetic patient** | Create fictional patients with demographic and contact information. Use invented data only. |
| 3 | **Find the patient** | Locate your patient using at least two different search criteria or approaches. |
| 4 | **Edit patient information** | Change at least one demographic field. Navigate away, return, and verify whether the change persisted. |
| 5 | **Schedule an appointment** | Schedule an appointment for the patient with a provider. |
| 6 | **Navigate through the appointment** | Locate the appointment in the calendar and determine whether/how you can navigate from it back to the patient record. |
| 7 | **Create a clinical encounter** | Create an encounter for your synthetic patient. |
| 8 | **Record vital signs** | Enter several vital signs, such as height, weight, temperature, pulse, and blood pressure. |
| 9 | **Add a problem or diagnosis** | Add a fictional clinical problem/diagnosis to the patient record. |
| 10 | **Add a medication** | Add a medication or medication-related record using a clearly fictional clinical scenario. |
| 11 | **Add an allergy** | Add a fictional allergy to the patient record. |
| 12 | **Add a note or document** | Associate a short note or document containing synthetic content with the patient or encounter. |
| 13 | **Review patient history** | Find where previous encounters, problems, medications, allergies, or other historical information can be reviewed. |
| 14 | **Locate a report or summary** | Find a patient report, summary, or comparable view. Identify what information OpenEMR combines in that view. |
| 15 | **Verify persistence** | Log out and log back in. Verify that the patient and key information you created remain available. |

---

# Part B — Exploration Challenges

Investigate the following questions.

You are **not** being told whether OpenEMR should allow or prevent these situations. Your responsibility is to determine and document what the system actually does.

1. Can you create **two patients with the same name and date of birth**?
2. Can the **same provider be scheduled for overlapping appointments**?
3. Can you enter a **physiologically unrealistic or impossible vital-sign value**?

For each challenge, record:

- What you attempted.
- What the system did.
- Whether the system accepted or rejected the action.
- Any message, warning, or validation you observed.
- Whether the result raises a testing question.

> **Important:** Do not assume that because the system accepts an action, the behavior is correct.

---

# Part C — Observe the Web Interaction

Use your browser's **Developer Tools** and open the **Network** panel.

Clear the network log, change one field in your synthetic patient's record, and save the change.

Identify a request that appears related to the operation.

Record:

- The user action you performed.
- HTTP method (for example, `GET` or `POST`).
- Request URL or endpoint.
- HTTP status code.
- What you believe the request accomplished.

You are **not expected to understand every request**.

The purpose is to begin connecting visible user actions to the underlying web interactions. You will investigate these connections more deeply in Week 2.

---

# Part D — Exploration Log

Maintain a concise **Exploration Log** while you work.

Do not write a click-by-click transcript. Record observations that would help another tester understand the system.

Use the following format:

| Task / Feature | Observed Result | What We Learned | Question / Concern |
|---|---|---|---|
| Create patient | Patient saved and assigned an identifier | Patient data persists beyond the form | What prevents duplicate patients? |
| | | | |
| | | | |
| | | | |

Add rows as necessary.

Your log should capture meaningful observations from across the system, not simply indicate that each task was completed.

---

# Part E — Identify Testing Opportunities

As you explore OpenEMR, begin thinking like a software tester.

Identify **at least 8 behaviors, risks, or questions** that you believe deserve formal testing later in the course.

For each one, document:

| Observation | What Could Go Wrong? | Candidate Test Idea |
|---|---|---|
| Date of birth is entered during registration | A future or invalid date might be accepted | Attempt to register a patient with a future DOB |
| | | |
| | | |
| | | |

Your ideas do not need to be complete test cases yet.

At this stage, we are interested in your ability to recognize **testable behavior and potential risk**.

Remember:

> **"The software allowed it" does not necessarily mean "the software behaved correctly."**

---

# Part F — Initial System Feature Map

Create a **one-page visual feature map** showing the major OpenEMR functional areas your team discovered and how they appear to relate from a user's perspective.

This is a **functional map**, not an architecture diagram.

For example, your map might have a structure similar to:

```text
OpenEMR
│
├── Patient Management
│
├── Scheduling
│
├── Clinical Records
│   ├── Encounters
│   ├── Vitals
│   ├── Problems
│   └── Medications
│
└── Reports
```

Your actual map should reflect what **your team discovered through exploration**.

Do not copy an existing OpenEMR architecture diagram.

---

# Required Deliverables

Submit **one team package** containing the following:

1. **Exploration Log**
   - Covers the major tasks and meaningful observations from your exploration.

2. **Exploration Challenge Results**
   - Results for all three challenge questions.
   - Include what you attempted, what happened, and your interpretation.

3. **Network Observation**
   - User action.
   - HTTP method.
   - URL/endpoint.
   - Status code.
   - Your interpretation of what the request accomplished.

4. **Testing Opportunities**
   - At least **8 candidate testing ideas**.
   - Each should connect an observation to a potential problem/risk and a possible test.

5. **System Feature Map**
   - One-page visual representation of the major functional areas you discovered.

6. **Evidence**
   - Include **5–8 screenshots total** showing meaningful milestones or observations.
   - Do **not** submit screenshots of every click.

7. **Team Reflection**
   - Approximately **250–400 words**.
   - Address:
     - What surprised your team about OpenEMR?
     - What parts of the system now seem most important or risky to test?
     - Why?

---

# Evidence and Submission Guidelines

- Use only synthetic information in screenshots and artifacts.
- Screenshots should support an observation or claim, not simply prove that you opened a page.
- Clearly label figures/screenshots.
- Refer to evidence from your written work where appropriate.
- Organize the submission so another testing team could understand what you explored.
- Do not include passwords, `.env` contents, tokens, API keys, or other credentials.
- Commit only course-appropriate artifacts to your team repository.

---

# Evaluation

This assignment is primarily about **systematic exploration and thoughtful observation**.

You are **not graded on how many bugs you find**.

A behavior does not need to be a defect to represent a valuable testing opportunity.

| Criterion | Weight | Evidence of Strong Work |
|---|---:|---|
| **System exploration and workflow completion** | 25% | Core workflows are completed; evidence demonstrates meaningful interaction with the system. |
| **Exploration log and quality of observations** | 20% | Observations are specific, accurate, concise, and demonstrate increasing understanding of OpenEMR. |
| **Testing opportunities and reasoning** | 20% | At least 8 useful candidate tests are identified and connected logically to observed behavior or risk. |
| **Exploration challenges + network observation** | 15% | Challenges are investigated objectively; network evidence connects a user action to a web request. |
| **System feature map** | 10% | Map clearly communicates major functional areas and user-visible relationships at an appropriate level of abstraction. |
| **Communication, evidence, and team reflection** | 10% | Submission is organized, uses evidence appropriately, protects synthetic/private data, and reflects thoughtfully on the system. |
| **Total** | **100%** | |

---

# Use of Generative AI

Generative AI may be used as a **learning and investigation aid**, subject to your instructor's course AI policy.

However:

- Your team remains responsible for verifying every claim against the running system and other evidence.
- Do not submit AI-generated descriptions of OpenEMR behavior that your team did not personally investigate.
- Do not provide credentials, passwords, patient information, or other sensitive information to AI tools.
- AI output should be treated as a hypothesis or starting point, **not as evidence that the system behaves a particular way**.

If AI is used, keep a brief record of what it was used for.

Identify at least **one instance** in which your team:

- verified an AI-generated suggestion;
- corrected it;
- refined it; or
- rejected it based on evidence from the actual system.

---

# Looking Ahead — Week 2

This week asks:

> **What does the system do?**

In Week 2, you will ask:

> **How does the system do it?**

You will select or be assigned a workflow you explored this week and investigate it from several perspectives:

```text
User behavior
      ↓
URL / HTTP flow
      ↓
System architecture
      ↓
Components / source code
      ↓
Data model
      ↓
Dependencies
```

You will create architecture artifacts such as a **C4 model, URL/workflow map, focused ERD, and component/dependency analysis**.

Finally, you will return to some of the testing opportunities identified in this assignment and ask:

> **Now that we understand more about how the system works, how should our testing strategy change?**
