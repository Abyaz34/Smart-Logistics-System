# Contributing to Smart-Logistics-System

To keep our codebase stable and ensure everyone gets marks for their contributions, we follow a streamlined workflow. 

## 1. The Golden Rule
**Never push directly to `dev` or `main`.** All work must be done on your own separate branch and merged via a Pull Request (PR).

* `main`: This is our demo-ready code.
* `dev`: Our active workspace. All your branches will start from here and merge back here.

## 2. Branching Guide
Before you start coding, create a new branch off `dev`. Keep the name simple and descriptive.

**Format:** `<type>/<short-desc>`
* `feat/blue-block-cv` (For building a new feature)
* `fix/dobot-spazzing` (For fixing a bug)
* `docs/update-readme` (For updating documentation)

## 3. Commit Messages (Required for Grading)
We require that every commit includes a summary of achievements and logs individual contributions

**Format:**
`type(scope): short summary`
*(blank line)*
`- Achievement: [Explain what is actually working now]`
`- Assisted by: [Name of teammate, or "None"]`

**Example:**
> feat(vision): add text extraction
>
> - Achievement: Got Tesseract OCR to read 'DXB' and 'SHJ' from the webcam feed.
> - Assisted by: None

*Allowed types:* `feat`, `fix`, `docs`
*Allowed scopes:* `vision`, `dobot`, `mobile`, `logic`

## 4. Opening a Pull Request (PR)
When your code is working and ready to share:
1. Open a PR to merge your branch into `dev`.
2. Title the PR exactly like a commit message (e.g., `feat(logic): add sorting state machine`).
3. **Get it reviewed:** You need at least 1 approval from a teammate before you can click "Squash and Merge". 
4. Delete your branch after merging to keep the repo clean.
