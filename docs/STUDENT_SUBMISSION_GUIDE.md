# Project VITAL — Student Submission Guide

This guide explains how teams will organize, version, and submit Project VITAL assignments.

Project VITAL uses **standard GitHub repositories** rather than GitHub Classroom. Your team's GitHub repository will serve as the technical record of your work throughout the course. The course Learning Management System (LMS) remains the official location for assignment submission records, grades, and instructor feedback.

---

# 1. Submission Model

Each team will maintain **one private GitHub repository for the entire Project VITAL course project**.

The general workflow is:

```text
Project VITAL Course Repository
        │
        │ provides assignments, environment, and documentation
        ▼
Your Team Repository
        │
        │ contains your team's work
        ▼
Git Tag
        │
        │ creates a fixed snapshot at the deadline
        ▼
Course LMS
        │
        └── submit repository reference + tag
```

You will continue using the same team repository as the course progresses.

Do **not** submit your assignments directly to the main Project VITAL repository.

---

# 2. Create Your Team Repository

One member of your team should create the repository.

Unless your instructor provides a different naming convention, name it:

```text
VITAL-Team-XX
```

where `XX` is your assigned team name.

Examples:

```text
VITAL-Team-Eagles
VITAL-Team-Q&A
VITAL-Team-TestingEagles
```

## Repository visibility

Create the repository as:

> **Private**

Do not make your team repository public unless your instructor explicitly authorizes it.

---

# 3. Add Your Team Members

The student who creates the repository must add every team member as a collaborator.

In GitHub:

1. Open the team repository.
2. Select **Settings**.
3. Select **Collaborators** or **Collaborators and teams**.
4. Add each team member using their GitHub username.
5. Each student should accept the GitHub invitation.

Every student should work using their **own GitHub account**.

Do not share GitHub accounts.

---

# 4. Add the Instructor

Add the instructor to the private repository using the GitHub username provided by your instructor.

The instructor must be able to access the repository in order to grade your work.

Before the first assignment deadline, verify that the instructor has access.

---

# 5. Clone the Team Repository

Each team member should clone the repository to their own computer.

For example:

```bash
git clone <YOUR-TEAM-REPOSITORY-URL>
cd VITAL-Team-XX
```

Do not copy one student's local repository between computers.

Each team member should clone and work through Git using their own account.

---

# 6. Recommended Repository Structure

Your repository should be organized by assignment.

A typical structure will look like:

```text
VITAL-Team-XX/
│
├── README.md
│
├── assignment-01/
│   ├── exploration-log.md
│   ├── testing-opportunities.md
│   ├── reflection.md
│   ├── feature-map.*
│   └── evidence/
│
├── assignment-02/
│   ├── workflow.md
│   ├── http-trace.md
│   ├── architecture/
│   ├── data/
│   ├── dependencies/
│   ├── testing-analysis.md
│   └── ai-verification-log.md
│
├── assignment-03/
│
└── ...
```

Individual assignments may specify additional required files.

Follow the assignment's instructions when they differ from this general structure.

---

# 7. Your Repository README

Create a `README.md` at the root of the team repository.

At minimum, include:

```markdown
# Project VITAL — Team XX

## Team Members

- Student Name — GitHub username
- Student Name — GitHub username
- Student Name — GitHub username

## Project

This repository contains our team's work for Project VITAL.
```

Do not include student ID numbers, grades, personal phone numbers, home addresses, or other unnecessary personal information.

---

# 8. Working with Git

During the project, use the normal Git workflow:

```bash
git status
git add .
git commit -m "Describe the work completed"
git push
```

Commit messages should briefly explain the work performed.

Good examples:

```text
Add patient exploration observations

Document appointment workflow

Add initial C4 container diagram

Trace vitals fields to database

Add accessibility test cases
```

Avoid meaningless commit messages such as:

```text
stuff

update

final

asdf

changes
```

---

# 9. Individual Contributions

Project VITAL assignments are team-based, but every team member is expected to make **meaningful contributions**.

Students should commit their own work using their own GitHub accounts.

The goal is **not** to maximize the number of commits.

For example, this is not useful:

```text
Student A — 57 tiny commits
Student B — 3 meaningful commits
```

The number of commits alone does not determine contribution.

The instructor may consider:

- Git history;
- quality and scope of contributions;
- pull requests where applicable;
- assignment artifacts;
- peer feedback;
- individual reflections or check-ins;

when evaluating individual participation.

Do not artificially divide work simply to increase commit counts.

You will use AI, the instructor will also use AI. The instructor will use AI to make sure your commit is inside the window of the assignment, and if your contribution is meaningful (no deletions, followed by additions - these kinds of things AI can spot really easily), cosmetic changes, wash-up commits (AI and the instructor will evaluate everything!

---

# 10. Pull Before You Work

Because multiple people are using the same repository, get the latest version before beginning a work session.

```bash
git pull
```

A useful habit is:

```text
Start working
     ↓
git pull
     ↓
make changes
     ↓
git status
     ↓
git add
     ↓
git commit
     ↓
git push
```

Communicate with your teammates when multiple people are editing the same file.

---

# 11. What Must Never Be Committed

Do **not** commit:

- `.env` files;
- passwords;
- API keys;
- access tokens;
- private keys;
- database credentials;
- real patient information;
- protected health information (PHI);
- unnecessary personally identifiable information;
- grades or private peer-evaluation information;
- large generated datasets unless the assignment specifically requires them.

Before committing, always check:

```bash
git status
```

Review what Git is about to include.

---

# 12. Synthetic Data Only

Project VITAL uses healthcare software, but the course environment must contain **synthetic data only**.

Never enter information about:

- yourself;
- classmates;
- friends;
- family members;
- actual patients;
- other identifiable real people.

Names, addresses, dates, diagnoses, medications, and other patient information used for assignments should be fictional.

---

# 13. Preparing an Assignment for Submission

Before the deadline, review your assignment directory.

Confirm that:

- all required deliverables are present;
- links and diagrams work;
- screenshots are readable;
- required Markdown files render correctly on GitHub;
- no secrets or sensitive information are included;
- the latest work has been committed;
- all commits have been pushed to GitHub.

Check:

```bash
git status
```

Ideally, Git should report:

```text
nothing to commit, working tree clean
```

Then push one final time:

```bash
git push
```

---

# 14. Create the Submission Tag

Project VITAL uses a **Git tag** to identify the exact version of the repository being submitted.

This is important because your team will continue changing the repository after an assignment deadline.

For Assignment 1, for example:

```bash
git tag assignment-01
git push origin assignment-01
```

For Assignment 2:

```bash
git tag assignment-02
git push origin assignment-02
```

Future assignments will follow the same pattern:

```text
assignment-01
assignment-02
assignment-03
assignment-04
...
```

The assignment instructions will specify the required tag.

---

# 15. Why We Use Tags

Suppose Assignment 1 is due Friday.

Your repository might look like:

```text
Monday       Wednesday       Friday              Sunday
   │             │              │                   │
   ▼             ▼              ▼                   ▼
exploration → screenshots → assignment-01 → architecture work
                                TAG
```

The repository may continue changing after Friday.

The tag identifies:

> **This is the version our team submitted for Assignment 1.**

The instructor grades the tagged version rather than later changes to the repository.

---

# 16. Verify the Tag

After pushing your tag, verify that it exists.

You can run:

```bash
git tag
```

You should see the assignment tag listed.

You can also open your GitHub repository and view **Tags** to verify that the tag was pushed to GitHub.

Creating a tag only on your computer is **not sufficient**.

It must be pushed to GitHub.

---

# 17. Submitting to the LMS

Only **one team member** needs to submit the team assignment to the LMS unless your instructor specifies otherwise.

Submit the information requested by your instructor.

A typical submission should contain:

```text
Team: VITAL-Team-07

Team Members:
Student A
Student B
Student C

Repository:
<team repository URL>

Submission Tag:
assignment-01

Submission Notes:
(optional)
```

Do not upload a ZIP copy of the repository unless your instructor specifically requests one.

The Git tag is the authoritative technical submission.

---

# 18. What Version Will Be Graded?

The instructor will grade the repository state identified by the required assignment tag.

For example:

```text
assignment-01
```

means:

> Grade the repository exactly as it existed when this tag was created.

Changes pushed after the tag do not automatically become part of that submission.

---

# 19. Fixing Something After You Create a Tag

Do not silently move or replace a submission tag after the deadline.

If you discover a problem **before the deadline**, contact your instructor or follow the course resubmission policy.

If your instructor permits replacing a tag before the deadline, follow the instructions they provide.

If you discover a problem **after the deadline**, do not rewrite the submitted Git history or move the tag unless explicitly authorized.

The LMS timestamp and repository history may be used to determine when work was submitted.

---

# 20. Late Work

Late-work rules are determined by the course syllabus.

If a late submission is permitted, your instructor may ask you to use a separate tag such as:

```text
assignment-01-late
```

Do not create alternate submission tags unless instructed.

---

# 21. Branches

During the first Project VITAL assignments, your team may work primarily on:

```text
main
```

As the course progresses, you will be asked to use branches.

For example:

```text
main
 │
 ├── feature/patient-tests
 ├── feature/accessibility-tests
 └── feature/data-generator
```

Later assignments may require:

- feature branches;
- pull requests;
- code review;
- automated testing;
- continuous integration.

Do not introduce a complicated branching strategy unless the assignment requires it.

---

# 22. Repository History Is Part of the Engineering Record

Git is not only a submission mechanism.

It provides evidence of how a software project evolves.

During Project VITAL, repository history may help you understand:

- when tests were introduced;
- why a test changed;
- who investigated a particular issue;
- when a defect was discovered;
- how the testing strategy evolved;
- whether a regression was introduced;
- how the team collaborated.

Write commits with the assumption that another engineer may need to understand your work later.

---

# 23. Grades and Feedback

GitHub is used for technical project artifacts and version history.

The course LMS remains the official location for:

- grades;
- private instructor feedback;
- individual grading adjustments;
- private peer assessments;
- other protected education records.

Do not store grades or confidential peer feedback in the team GitHub repository.

---

# 24. GitHub Problems Near a Deadline

Do not wait until the final minutes before the deadline to push your work.

Before submission day, confirm that:

```bash
git pull
git status
git push
```

all work correctly.

Also verify that:

- every team member can access the repository;
- the instructor can access the repository;
- GitHub contains the latest commits;
- your assignment tag appears on GitHub.

If GitHub or another required service experiences a documented outage, follow your instructor's course policy.

---

# 25. Final Submission Checklist

Before submitting each assignment, verify:

### Repository

- [ ] Repository is private unless the instructor has authorized otherwise.
- [ ] All team members have access.
- [ ] Instructor has access.
- [ ] Required assignment directory exists.
- [ ] All required deliverables are present.

### Security and Privacy

- [ ] No `.env` file is committed.
- [ ] No passwords or tokens are committed.
- [ ] No real patient data is included.
- [ ] No unnecessary personal information is included.
- [ ] Screenshots contain only appropriate synthetic/course data.

### Git

- [ ] Latest work is committed.
- [ ] Latest commits are pushed to GitHub.
- [ ] `git status` shows no unintentionally uncommitted work.
- [ ] Required assignment tag has been created.
- [ ] Tag has been pushed to GitHub.
- [ ] Tag is visible on GitHub.

### LMS

- [ ] Correct team is identified.
- [ ] Repository reference is submitted.
- [ ] Correct assignment tag is submitted.
- [ ] Required team-member information is included.
- [ ] Submission was completed before the deadline.

---

# Quick Submission Reference

For a typical assignment:

```bash
# Get the latest team work
git pull

# Check your repository
git status

# Add and commit final changes if necessary
git add .
git commit -m "Complete Assignment 1"

# Push commits
git push

# Create the submission snapshot
git tag assignment-01

# Push the tag
git push origin assignment-01
```

Then verify the tag on GitHub and submit the required repository information and tag to the LMS.

---

# Need Help?

If you encounter a Git or GitHub problem:

1. Read the error message carefully.
2. Run `git status`.
3. Do not delete the repository or rewrite Git history as a first troubleshooting step.
4. Preserve your local work.
5. Ask for help before using destructive Git commands you do not understand.

Commands such as `reset --hard`, force-pushes, history rewriting, and deleting tags can permanently discard or obscure work.

When in doubt, **preserve the current state and ask for assistance**.
