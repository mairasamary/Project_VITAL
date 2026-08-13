# Project VITAL — Instructor Semester Setup Guide

This guide is for instructors preparing **Project VITAL** for a new semester or adopting the project for the first time.

Its purpose is to make the course reproducible without requiring the instructor to remember how the environment, assignments, and student workflow were originally configured.

Use this document as the pre-semester checklist before releasing Project VITAL to students.

---

# 1. Project VITAL Repository Model

Project VITAL should be treated as a **reusable course kit**, not as the repository where students submit their work.

The recommended model is:

```text
Canonical Project VITAL Repository
        │
        │ course materials
        │ assignments
        │ Docker environment
        │ instructor documentation
        ▼
Students clone/use course materials
        │
        ▼
Private Team Repositories
        │
        ▼
Git Tags identify submissions
        │
        ▼
Institutional LMS
grades + private feedback
```

The canonical Project VITAL repository should contain reusable teaching materials.

Semester-specific student work should **not** be committed to the canonical repository.

---

# 2. Recommended Repository Structure

A typical Project VITAL repository should contain:

```text
Project_VITAL/
│
├── README.md
├── LICENSE
├── .gitignore
│
├── assignments/
│   ├── 01-system-exploration/
│   │   └── README.md
│   ├── 02-system-architecture/
│   │   └── README.md
│   └── ...
│
├── docs/
│   ├── STUDENT_SETUP.md
│   └── STUDENT_SUBMISSION_GUIDE.md
│
├── environment/
│   ├── docker-compose.yml
│   ├── .env.example
│   ├── README.md
│   ├── VERSION.md
│   ├── setup.sh
│   ├── reset.sh
│   └── status.sh
│
├── data/
├── tests/
├── rubrics/
│
└── instructor/
    ├── README.md
    └── SEMESTER_SETUP.md
```

As Project VITAL grows, additional instructor-only reference material may be added under `instructor/`.

---

# 3. Two Ways to Start a Semester

There are two common situations.

## Situation A — You Already Maintain Project VITAL

If you are the maintainer of the canonical repository, begin by updating your local copy:

```bash
git clone https://github.com/mairasamary/Project_VITAL.git
cd Project_VITAL
```

If you already have a local copy:

```bash
cd Project_VITAL
git switch main
git pull
```

Confirm:

```bash
git status
```

The working tree should be clean before you begin semester preparation.

---

## Situation B — Another Instructor Is Adopting Project VITAL

Another instructor should generally **fork** the canonical repository through GitHub.

After creating the fork:

```bash
git clone <URL-OF-INSTRUCTOR-FORK>
cd Project_VITAL
```

Optionally configure the original Project VITAL repository as `upstream`:

```bash
git remote add upstream https://github.com/mairasamary/Project_VITAL.git
```

Verify:

```bash
git remote -v
```

A typical result is:

```text
origin      instructor's fork
upstream    canonical Project VITAL repository
```

This allows the adopting instructor to customize their fork while still retrieving future Project VITAL improvements.

---

# 4. Do Not Rebuild the Course from Scratch

A new semester should normally begin from the existing Project VITAL repository.

Do **not**:

- recreate assignments manually;
- copy files one at a time into a new repository;
- recreate the Docker environment from memory;
- download an arbitrary current OpenEMR release;
- replace pinned dependencies without validation.

Instead:

```text
Existing validated Project VITAL release
                │
                ▼
Review versions
                │
                ▼
Validate environment
                │
                ▼
Make intentional updates
                │
                ▼
Validate again
                │
                ▼
Release semester version
```

---

# 5. Create a Semester Preparation Branch

Do not make semester-preparation changes directly on `main`.

Create a branch:

```bash
git switch main
git pull
git switch -c semester/2026-fall
```

Immediately push the new semester branch to GitHub:

```bash
git push -u origin semester/2026-fall
```

This step is important. A branch created with `git switch -c` initially exists **only in your local repository**. A separate validation clone will not be able to see or switch to that branch until it has been pushed to the remote repository.

Verify that the branch exists remotely:

```bash
git branch -a
```

You should see an entry similar to:

```text
remotes/origin/semester/2026-fall
```

For another semester:

```text
semester/2027-spring
semester/2027-fall
semester/2028-spring
```

Use the naming convention:

```text
semester/YYYY-term
```

This branch is the workspace for validating and preparing that semester's version.

---

# 6. Review the Current Course Baseline

Before changing anything, review:

```text
environment/VERSION.md
environment/docker-compose.yml
environment/.env.example
docs/STUDENT_SETUP.md
docs/STUDENT_SUBMISSION_GUIDE.md
assignments/
```

Record the current baseline.

At minimum, identify:

- Project VITAL version, if defined;
- OpenEMR version;
- database image/version;
- required Docker/Docker Compose assumptions;
- exposed ports;
- default synthetic/course credentials;
- current assignments;
- current student submission model.

Do not assume that because the environment worked last semester it will work unchanged this semester.

---

# 7. Decide Whether to Upgrade OpenEMR

A new semester does **not** automatically require a new OpenEMR version.

The priority for a teaching environment is:

> **Reproducibility and stability before novelty.**

If the current pinned version supports the course learning goals and has no reason that makes it unsuitable for continued classroom use, keeping the validated version may be preferable.

Consider upgrading when:

- the existing version is no longer practical to obtain or run;
- important security considerations require a change;
- the new version provides functionality needed by the course;
- the current version has compatibility problems with current Docker environments;
- you intentionally want students to investigate a newer version.

Do not change the image from a pinned version to a moving tag such as `latest` merely to obtain a newer release.

---

# 8. If You Change a Version

If OpenEMR, MariaDB, or another environment dependency changes:

1. Update `docker-compose.yml`.
2. Update `VERSION.md`.
3. Review `.env.example`.
4. Review the student setup documentation.
5. Perform the complete clean-install validation described below.
6. Run Assignments 1 and 2 against the new version.
7. Update screenshots/instructions if UI behavior changed.
8. Record the change in the semester/release notes.

A dependency upgrade is not complete until the **student workflow** has been validated.

---

# 9. Test as a New Student

This is one of the most important pre-semester steps.

Do not validate only from your existing Docker volumes.

Existing volumes may hide setup problems.

First, make sure important local work is backed up.

Then stop/remove the test environment and volumes according to the Project VITAL environment instructions.

For the course environment, this may include:

```bash
cd environment
docker compose down -v
```

Remember:

> `-v` deletes the local course database volume.

Only do this when you intentionally want a clean test environment.

---

# 10. Perform a Clean Student Installation

Ideally, test from a fresh clone in a separate directory.

**Before creating the validation clone, confirm that the semester branch has been pushed to GitHub.** From your main working copy, you can verify this with:

```bash
git branch -a
```

Look for:

```text
remotes/origin/semester/2026-fall
```

If the remote branch is missing, push it first:

```bash
git push -u origin semester/2026-fall
```

Then create the clean validation clone:

```bash
cd ~/Desktop
git clone https://github.com/mairasamary/Project_VITAL.git Project_VITAL_TEST
cd Project_VITAL_TEST
```

If validating a semester branch before it is merged, fetch the remote branches and switch to the semester branch **before entering the `environment` directory**:

```bash
git fetch origin
git switch semester/2026-fall
```

If Git does not automatically create the local tracking branch, use:

```bash
git switch --track origin/semester/2026-fall
```

Verify that you are on the correct branch:

```bash
git branch
```

You should see:

```text
  main
* semester/2026-fall
```

Now enter the environment directory:

```bash
cd environment
```

Create the local configuration:

```bash
cp .env.example .env
```

Then verify Docker:

```bash
docker --version
docker compose version
docker info
```

Run:

```bash
docker run hello-world
```

Then:

```bash
docker compose pull
docker compose up -d
```

Check:

```bash
docker compose ps
```

If necessary:

```bash
docker compose logs openemr
```

Finally, open the configured local OpenEMR URL in a browser and log in.

---

# 11. Validate the Student Setup Guide

Follow:

```text
docs/STUDENT_SETUP.md
```

**exactly as written.**

Do not rely on your knowledge of Docker to skip unclear steps.

While following the guide, ask:

- Does every command still work?
- Are filenames correct?
- Are paths correct?
- Are credentials correct?
- Are ports correct?
- Does the first startup take longer than the guide suggests?
- Are there new Docker warnings?
- Are macOS instructions still reasonable?
- Are Windows instructions still reasonable?
- Are Linux instructions still reasonable?
- Does OpenEMR look substantially different?
- Can a student reasonably recover from common errors?

Correct the guide when you discover discrepancies.

---

# 12. Validate the Core OpenEMR Workflow

Before releasing the semester environment, manually verify at least the core workflow used in Assignment 1.

At minimum:

- [ ] Log in.
- [ ] Create a synthetic patient.
- [ ] Search for the patient.
- [ ] Edit patient demographics.
- [ ] Schedule an appointment.
- [ ] Create an encounter.
- [ ] Enter vital signs.
- [ ] Add a problem/diagnosis.
- [ ] Add a medication-related record.
- [ ] Add an allergy.
- [ ] Add a note/document if used by the assignment.
- [ ] Review patient history.
- [ ] Locate a report/summary.
- [ ] Log out.
- [ ] Log back in.
- [ ] Confirm data persistence.

If any assignment task is no longer practical in the pinned OpenEMR version, update the assignment before the semester begins.

---

# 13. Validate Assignment 1

Review:

```text
assignments/01-system-exploration/README.md
```

Perform the assignment as a student would.

Check:

- Can all required tasks be completed?
- Are menu names still accurate?
- Are the exploration challenges still meaningful?
- Can students access browser Developer Tools?
- Is the Network observation feasible?
- Are 5–8 screenshots sufficient?
- Is the expected time realistic?
- Are the deliverables clear?
- Does the rubric still match the deliverables?

Do not assume last semester's assignment remains valid after an OpenEMR upgrade.

---

# 14. Validate Assignment 2

Review:

```text
assignments/02-system-architecture/README.md
```

Select at least one representative workflow and perform enough investigation to verify that students can reasonably locate:

- meaningful HTTP requests;
- relevant source-code locations;
- relevant database tables;
- useful component relationships;
- useful dependencies.

Confirm that the expected C4, ERD, and dependency artifacts are achievable within the assigned time.

Maintain an instructor/reference investigation when possible.

This reference should not necessarily be distributed to students before submission.

---

# 15. Review Course Safety Boundaries

Project VITAL includes testing activities that can become inappropriate if directed at external systems.

Before every semester, verify that assignments clearly state:

- use synthetic data only;
- do not test public OpenEMR demo systems;
- do not perform security testing against external systems;
- do not expose the local OpenEMR instance publicly;
- do not commit credentials;
- SQL injection experiments must target only explicitly authorized course environments;
- load/denial-of-service activities must target only explicitly authorized isolated environments;
- students must follow institutional computing policies.

Security-testing instructions should define the authorized target and scope explicitly.

---

# 16. Review Student Privacy and Data Handling

Confirm that Project VITAL still follows the course's privacy approach.

The recommended model is:

```text
GitHub team repository
        │
        ├── technical artifacts
        ├── synthetic test data
        └── project history

Institutional LMS
        │
        ├── grades
        ├── private instructor feedback
        ├── peer assessments
        └── protected education records
```

Do not use the team repository as the gradebook.

Before the semester, review whether institutional policies require changes to:

- repository visibility;
- student GitHub account usage;
- retention of student work;
- use of external AI services;
- peer evaluation;
- screenshots;
- generated data.

Follow your institution's current policies and applicable regulations.

---

# 17. Review the Student Submission Model

Read:

```text
docs/STUDENT_SUBMISSION_GUIDE.md
```

The standard Project VITAL submission model is:

```text
Private Team Repository
        ↓
Assignment Work
        ↓
Git Tag
        ↓
LMS Submission
```

Example tags:

```text
assignment-01
assignment-02
assignment-03
```

Confirm that this workflow is compatible with your institution and LMS.

---

# 18. Decide How Team Repositories Will Be Created

Without GitHub Classroom, the default Project VITAL model is:

1. Students form/receive teams.
2. One student creates the private team repository.
3. The student adds all teammates.
4. The student adds the instructor.
5. The team uses that repository throughout the semester.
6. Assignment submissions are identified by Git tags.
7. The LMS stores the official submission record and grade.

You may replace this process if your institution provides another repository-management mechanism.

Document any semester-specific change in the LMS.

---

# 19. Prepare the LMS

Project VITAL intentionally does not depend on a particular LMS.

Before the semester, create LMS assignment entries corresponding to the Project VITAL assignments.

For each assignment, configure:

- assignment title;
- release date;
- due date;
- grading points;
- rubric;
- team/group submission behavior;
- late policy;
- submission instructions.

For repository-based submissions, students generally need to provide:

```text
Team name
Team members
Repository reference
Submission tag
Optional submission note
```

Grades and private feedback should remain in the LMS.

---

# 20. Review Assignment Weights and Rubrics

The reusable Project VITAL materials provide recommended rubrics.

Before the semester, decide whether the weights match your course.

If you change grading weights, ensure that:

- the assignment document;
- LMS rubric;
- syllabus;
- instructor grading materials;

all agree.

Avoid maintaining contradictory grading information in multiple locations.

---

# 21. Review Generative AI Expectations

Because Project VITAL may intentionally incorporate generative AI into software-testing education, review the AI policy each semester.

Decide:

- which AI tools students may use;
- whether institutional accounts are required;
- what information may be shared with AI tools;
- what AI-use documentation is required;
- whether AI verification logs are graded;
- what constitutes unacceptable substitution of AI output for student investigation.

Assignments should continue emphasizing:

> **AI output is not evidence.**

Students should verify claims against the actual system, source, database, documentation, or runtime evidence.

---

# 22. Keep Semester-Specific Information Out of Reusable Materials When Possible

Avoid embedding details such as:

```text
Due Friday, September 18 at 11:59 PM
```

inside the reusable Project VITAL assignment unless necessary.

Prefer:

```text
See the LMS for the due date.
```

Keep semester-specific information in:

- LMS;
- syllabus;
- semester notes;
- instructor configuration.

This reduces maintenance when the course is reused.

---

# 23. Decide Whether Semester Changes Belong in Project VITAL

During preparation, ask whether each change is:

### Reusable improvement

Examples:

- clearer Docker troubleshooting;
- corrected assignment instructions;
- improved rubric wording;
- safer security-testing guidance;
- improved data-generation tooling.

These changes should normally return to the canonical Project VITAL repository.

### Semester-specific change

Examples:

- Fall 2026 due date;
- current team list;
- section-specific grading adjustment;
- temporary class schedule;
- room number.

These generally should **not** become permanent reusable Project VITAL content.

---

# 24. Merge Reusable Semester Improvements

After validation, commit changes on the semester branch:

```bash
git status
git add .
git commit -m "Prepare Project VITAL for Fall 2026"
git push -u origin semester/2026-fall
```

Review the changes carefully.

When ready, merge reusable improvements into `main` through your normal review process.

For example, using a pull request is recommended.

After merge:

```bash
git switch main
git pull
```

---

# 25. Create a Course Release

Once the semester version is validated, create an immutable version identifier.

A recommended release tag format is:

```text
vital-YYYY-term
```

For example:

```bash
git tag -a vital-2026-fall -m "Project VITAL Fall 2026 course baseline"
git push origin vital-2026-fall
```

Examples:

```text
vital-2026-fall
vital-2027-spring
vital-2027-fall
```

This identifies the exact Project VITAL baseline used for that course offering.

---

# 26. Why Create a Semester Release Tag?

Suppose Project VITAL continues evolving during the semester.

You may later change:

- Assignment 4;
- documentation;
- Docker configuration;
- instructor materials.

The tag:

```text
vital-2026-fall
```

preserves the exact baseline that existed when the semester began.

This helps with:

- reproducibility;
- grading questions;
- future research;
- course assessment;
- debugging;
- comparing semesters.

---

# 27. Consider a Versioned Release for Major Changes

Semester tags identify course offerings.

Separately, major Project VITAL releases may use semantic-style versions such as:

```text
v1.0.0
v1.1.0
v2.0.0
```

For example:

```text
v1.0.0
    First complete reusable course kit

v1.1.0
    New accessibility testing module

v2.0.0
    Major OpenEMR/environment upgrade
```

You do not need to create a new major Project VITAL version merely because a new semester begins.

---

# 28. Test the Released Version One More Time

After creating the semester baseline, perform a final sanity check from the exact commit/tag students will use.

At minimum verify:

```bash
git status
docker compose pull
docker compose up -d
docker compose ps
```

Then:

- open OpenEMR;
- log in;
- verify one patient workflow;
- verify assignment links;
- verify documentation paths.

This catches errors introduced during the final preparation/merge.

---

# 29. Student Release Checklist

Before telling students to begin, confirm:

## Repository

- [ ] Canonical repository is accessible.
- [ ] Correct semester/release baseline is identified.
- [ ] README points students to the correct starting documentation.
- [ ] `.gitignore` protects `.env` and other local secrets.
- [ ] No instructor-only answer material is accidentally exposed.

## Environment

- [ ] Docker images pull successfully.
- [ ] Containers start successfully.
- [ ] OpenEMR opens locally.
- [ ] Login credentials work.
- [ ] Data persists after restart.
- [ ] Reset procedure works.
- [ ] Core Assignment 1 workflow works.

## Documentation

- [ ] `STUDENT_SETUP.md` has been tested.
- [ ] `STUDENT_SUBMISSION_GUIDE.md` matches the current process.
- [ ] Assignment paths are correct.
- [ ] Assignment instructions match the current OpenEMR version.
- [ ] Security/safety boundaries are explicit.

## LMS

- [ ] Assignment entries exist.
- [ ] Due dates are correct.
- [ ] Rubrics are correct.
- [ ] Team submission settings are correct.
- [ ] Repository/tag submission instructions are included.
- [ ] Grades/private feedback remain in the LMS.

## Students

- [ ] Team formation process is defined.
- [ ] Repository naming convention is defined.
- [ ] Instructor GitHub username is provided.
- [ ] Students know repositories must be private unless otherwise authorized.
- [ ] Students know to use synthetic data only.

---

# 30. Suggested First-Week Instructor Sequence

A practical semester launch sequence is:

```text
Before classes
      │
      ├── Validate Project VITAL release
      ├── Validate Docker/OpenEMR
      ├── Validate Assignment 1
      ├── Configure LMS
      └── Create semester release tag
              │
              ▼
First class / course launch
              │
              ├── Introduce Project VITAL
              ├── Explain System Under Test
              ├── Review synthetic-data rule
              └── Assign environment setup
                      │
                      ▼
Students complete setup
                      │
                      ├── Git works
                      ├── Docker works
                      ├── OpenEMR runs
                      └── Login works
                              │
                              ▼
Create team repositories
                              │
                              ▼
Assignment 1 — System Exploration
                              │
                              ▼
Assignment 2 — System Architecture
```

Do not wait until Assignment 1 is due to discover that a student cannot run the environment.

Whenever possible, make successful environment setup an early course checkpoint.

---

# 31. If You Need to Reproduce an Older Semester

Use the semester release tag.

For example:

```bash
git clone https://github.com/mairasamary/Project_VITAL.git
cd Project_VITAL
git checkout vital-2026-fall
```

You are now viewing the Project VITAL baseline associated with that semester.

To return to current development:

```bash
git switch main
git pull
```

Avoid editing directly while checked out at an old tag.

---

# 32. Updating an Instructor Fork from the Canonical Repository

If you are using a fork and configured the canonical repository as `upstream`:

```bash
git fetch upstream
git switch main
git merge upstream/main
```

Then:

```bash
git push origin main
```

Review upstream changes before merging them into an active course.

Do not automatically update a live semester environment without testing.

---

# 33. Mid-Semester Updates

Once students have begun working, prioritize stability.

For a minor documentation correction:

1. Fix the documentation.
2. Commit the correction.
3. Notify students clearly.

For a significant environment change:

1. Determine whether the change is actually necessary.
2. Test migration from the current student environment.
3. Determine whether student data will be affected.
4. Provide explicit migration instructions.
5. Avoid forcing an upgrade immediately before an assignment deadline.

Do not casually change pinned Docker images during an active assignment.

---

# 34. End-of-Semester Maintenance

At the end of the semester, create a short instructor retrospective.

Record:

- setup problems students encountered;
- Docker/platform problems;
- unclear assignment instructions;
- tasks that took longer than expected;
- OpenEMR behaviors that changed;
- successful/unsuccessful testing activities;
- rubric issues;
- AI-use observations;
- privacy/security concerns;
- improvements to make next semester.

Reusable improvements should be incorporated into Project VITAL before the next release.

---

# 35. Recommended Semester Lifecycle

The complete lifecycle is:

```text
                    PROJECT VITAL MAIN
                           │
                           ▼
                 Review existing baseline
                           │
                           ▼
               Create semester prep branch
                           │
                           ▼
                  Review dependencies
                           │
                           ▼
             Decide whether upgrades are needed
                           │
                           ▼
                 Clean student-style install
                           │
                           ▼
                 Validate documentation
                           │
                           ▼
               Validate Assignments 1 & 2
                           │
                           ▼
                 Review safety/privacy
                           │
                           ▼
                     Configure LMS
                           │
                           ▼
               Merge reusable improvements
                           │
                           ▼
                 Create semester release tag
                           │
                           ▼
                    Final sanity test
                           │
                           ▼
                       RELEASE
                           │
                           ▼
                      Teach course
                           │
                           ▼
                 Semester retrospective
                           │
                           ▼
                 Improve Project VITAL
                           │
                           └──────────────► next semester
```

---

# Quick Start — Returning Instructor

If you have taught Project VITAL before and need the condensed version:

```bash
# 1. Update Project VITAL
git switch main
git pull

# 2. Create semester preparation branch
git switch -c semester/2026-fall

# Push it immediately so a clean validation clone can access it
git push -u origin semester/2026-fall

# 3. Review
# environment/VERSION.md
# environment/docker-compose.yml
# docs/STUDENT_SETUP.md
# docs/STUDENT_SUBMISSION_GUIDE.md
# assignments/

# 4. Validate Docker
docker --version
docker compose version
docker info

# 5. Validate from a clean environment
cd environment
cp .env.example .env
docker compose pull
docker compose up -d
docker compose ps

# 6. Run the core Assignment 1 workflow

# 7. Verify at least one Assignment 2 architecture workflow

# 8. Update documentation/assignments as necessary

# 9. Commit semester preparation
git add .
git commit -m "Prepare Project VITAL for Fall 2026"
git push -u origin semester/2026-fall

# 10. Review and merge reusable changes into main

# 11. Create semester baseline
git switch main
git pull
git tag -a vital-2026-fall -m "Project VITAL Fall 2026 course baseline"
git push origin vital-2026-fall
```

Then perform the **Student Release Checklist** before releasing the repository to students.

---

# Guiding Principle

When preparing a new semester, remember:

> **Do not ask whether the repository still exists. Ask whether a new student can successfully reproduce the complete learning environment from the repository today.**

A Project VITAL semester is ready only when the course environment, documentation, assignments, submission workflow, and safety boundaries have been validated together.
