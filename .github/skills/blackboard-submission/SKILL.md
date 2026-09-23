---
name: blackboard-submission
description: Prepares and submits the CSCI 6032 Homework 2 repository (j0371/csci6032-hw2-j0371) to Blackboard. Runs a preflight (branch, git status, recent commits, remote URL, required files, secret/private-data scan), builds csci6032-hw2-<github-username>.tar.gz from the committed HEAD, and — only after explicit human confirmation at each gated step — navigates to the Blackboard assignment and submits it. Use when the student invokes /blackboard-submission, or asks to dry-run, prepare, stage, or submit the Homework 2 Blackboard archive. Never pre-authorized for shell or browser tools; every command and browser action must be confirmed individually.
---

# Blackboard submission skill

This skill prepares and, only with explicit human confirmation at every gated
step, submits this repository's Homework 2 archive to Blackboard. It never
stores, requests, or types Blackboard credentials, and it never commits
Blackboard content (screenshots, receipts, browser data, personal
information) back into this public repository.

No tool is pre-approved. Every `git`/shell command and every
`playwright-browser_*` call must be proposed individually and confirmed by
the student before it runs. Do not attempt to batch-approve or silently
chain restricted actions.

## Mode selection

Before doing anything else, determine the mode from the student's request:

- **Dry run**: the student said "dry run", "check only", "preflight only", or
  similar. Perform every check through Step 6 below, report the results, and
  stop. Do not touch the browser and do not submit anything.
- **Real submission**: the student asked to actually submit. Perform every
  step in order, including the browser steps, but still stop at every gate
  described below.

If the mode is ambiguous, ask the student which mode they want before doing
anything else.

## Step 1 — Confirm the expected repository

1. Run `git rev-parse --show-toplevel` and confirm the CLI's working
   directory is inside that toplevel (never operate from the home directory
   or an unrelated parent folder).
2. Run `git remote get-url origin` and `git remote get-url --push origin`.
   Both must resolve to `j0371/csci6032-hw2-j0371` on `github.com` (with or
   without a `.git` suffix and regardless of `https://`/`git@` form).
3. If the repository or remote does not match, **stop immediately** and tell
   the student this skill is only for the `j0371/csci6032-hw2-j0371`
   homework repository.
4. Extract `<github-username>` from the matched remote URL (the owner
   segment, e.g. `j0371`). This value is used later for the archive filename.

## Step 2 — Preflight checks

Run each of the following and show the raw output to the student:

1. `git branch --show-current` — the current branch.
2. `git status --porcelain=v1 --untracked-files=all` — must be empty for a
   clean tree; also run plain `git status` for a human-readable view.
3. `git log --oneline -20` — recent commit history, so the student can see
   the checkpoint commits are present (equivalent commit wording is fine;
   this is for human review, not exact string matching).
4. `git fetch origin` followed by `git rev-parse HEAD` and
   `git rev-parse origin/<current-branch>` — used again in Step 4.
5. Confirm every required path exists at the repo root and is tracked
   (`git ls-files -- <path>` returns it):
   - the homework notebook (the tracked `*.ipynb` file matching
     `CSCI6032_hw2*.ipynb` at the repo root — flag it if more than one
     candidate exists or if none is found)
   - `README.md`
   - `AGENTS.md`
   - `sample.txt`
   - `Dockerfile`
   - `src/text_stats.py`
   - `tests/test_text_stats.py`
   - `.github/skills/blackboard-submission/SKILL.md` (this file)
6. Scan the committed tree for likely secrets or private data with something
   like `git grep -nIiE "(api[_-]?key|secret|password|token|BEGIN [A-Z]+ PRIVATE KEY|PLAYWRIGHT_MCP_EXTENSION_TOKEN)" -- . ':(exclude).github/skills/blackboard-submission/SKILL.md'`
   and separately confirm no browser-artifact paths are tracked, e.g.
   `git ls-files | Select-String -Pattern "\.playwright-mcp|\.env($|\.)|cookies|\.chrome-profile"`.
   Report any hits verbatim so the student can judge them; do not decide on
   the student's behalf that a hit is safe.

## Step 3 — Stop conditions

Stop and clearly report the problem (do not proceed to Step 4) if any of the
following is true:

- The working tree is not clean (Step 2.2 found modified/untracked files).
- Any required file from Step 2.5 is missing or untracked.
- Step 2.6 found an unresolved secret or private-data pattern.
- Step 1 could not confirm the expected repository/remote.

## Step 4 — Confirm the branch has been pushed

Using the values captured in Step 2.4, confirm
`git rev-parse HEAD` equals `git rev-parse origin/<current-branch>`. If they
differ, stop and tell the student to push (or pull/rebase, as appropriate)
before continuing. Do not push on the student's behalf without asking first.

## Step 5 — Build the submission archive

1. Compute the archive name: `csci6032-hw2-<github-username>.tar.gz`, using
   the username captured in Step 1.
2. Build it from the committed `HEAD` only, writing it **outside the
   repository** (e.g. to the OS temp directory) so it can never be picked up
   by a later `git status` or accidentally committed:
   `git archive --format=tar.gz -o "<temp-dir>/csci6032-hw2-<github-username>.tar.gz" HEAD`.
   `git archive` inherently includes only committed, tracked files at `HEAD`
   — it cannot include `.git`, untracked caches, or ignored files, so no
   separate exclude list is needed.
3. Confirm the file was created and report its size and full path.

## Step 6 — Show the proposed submission

Before doing anything else, present to the student, verbatim:

- The exact notebook file path that will be described in the submission.
- The exact archive path and filename from Step 5.
- The exact repository URL (`https://github.com/j0371/csci6032-hw2-j0371`).
- The exact submission comment text to be entered, which — for a real
  submission — is only ever this fixed statement plus the repository URL:

  ```text
  I used my blackboard-submission skill, reviewed the staged artifacts, explicitly
  approved the final submission action, and verified Blackboard's confirmation.
  ```

- The full file listing inside the archive, obtained with
  `tar -tzf "<archive-path>"`, so the student can verify no unrelated files,
  credentials, or caches are present.

## Step 7 — Dry-run stop point

If this is a dry run (see "Mode selection"), stop here. Summarize every
check performed, its result, and the archive contents from Step 6. Do not
open, navigate, or interact with the browser, and do not submit anything.

## Step 8 — Ask before touching the browser

Before calling any `playwright-browser_*` tool, explicitly ask the student
for permission to open or control the Blackboard tab for this submission.
Do not proceed until they say yes.

## Step 9 — Authentication boundary

Tell the student to personally log in to Blackboard in the connected tab if
they are not already authenticated. Never request, read, type, store,
autofill, or otherwise expose a Blackboard username, password, or session
token/cookie. If a login form is visible, stop and wait for the student to
authenticate themselves before continuing.

## Step 10 — Navigate and stage (no submission yet)

1. Use `playwright-browser_snapshot` to see the current page and confirm the
   connected tab is on the course Blackboard site.
2. Navigate only within this course to find the Homework 2 submission
   assignment (e.g. via the course's Assignments/Content area). Use
   accessibility snapshots to identify a link/button whose text matches
   this homework (allow for reasonable variants such as "Homework 2",
   "HW2", "Homework #2").
3. Before staging anything, show the student the resulting page's heading/
   title and ask them to confirm it is the correct submission page. Do not
   guess past this checkpoint.
4. Once confirmed, attach the archive from Step 5 via the page's file
   upload control (`playwright-browser_file_upload`), and enter the
   repository URL and the fixed comment text from Step 6 into the
   appropriate text fields. Do not click any submit/finish control yet.

## Step 11 — Stop before the irreversible action

Take a fresh `playwright-browser_snapshot` of the staged form. Show the
student exactly what is staged (attached file name, repository URL text,
comment text) and identify the exact control that will finally submit the
assignment. Do not interact with that control yet.

## Step 12 — Require explicit confirmation, again

Ask the student to explicitly confirm this specific submission right now
(e.g. "yes, submit now"). A general/earlier approval to run this skill, or
approval of an individual tool call, is not sufficient — this confirmation
must be about this exact staged submission.

## Step 13 — Submit and verify

Only after the Step 12 confirmation, click the submit control. Then:

1. Take a snapshot of the resulting page and report the confirmation
   heading, receipt, or success message shown by Blackboard.
2. If no clear confirmation appears, say so plainly and tell the student to
   verify manually rather than assuming success.

## Step 14 — Keep Blackboard data out of the repository

Never write Blackboard screenshots, receipts, page content, grades, or any
personal information into any file in this repository. Any staging or log
artifacts (e.g. the archive built in Step 5, browser console logs) must stay
outside the repository or be excluded by `.gitignore`; do not `git add` them.
