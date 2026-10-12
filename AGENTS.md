# Sortify — Agent Guidelines & Operational Rules

This document outlines mandatory protocols and quality standards for AI coding agents working on the Sortify repository.

---

## 1. Pre-Implementation Verification & Codebase Sweep
Before writing, modifying, or deleting any code:
1. **Quick Codebase Sweep:** Inspect existing files, project structure, schemas, and dependencies relevant to the task to ensure alignment with existing architecture.
2. **Review Recent Changes:** Check `git status`, recent commits (`git log -n 5`), and recent diffs to stay informed about active work and prevent overwriting teammates' changes.
3. **Check Contracts & Configurations:** Cross-reference existing schemas (Pydantic models, Firestore models, API route contracts, and component props) before making assumptions.

---

## 2. Branch Naming Conventions
When branching or proposing branches, strictly follow the repository convention:

```text
<type>/<subteam>/<your-name>/<feature-name>
```

* **Subteams:** `frontend`, `backend`, `ml`, `docs`
* **Examples:**
  * Frontend: `feat/frontend/alex/camera-ui`
  * Backend: `feat/backend/sam/classify-endpoint`
  * AI/ML: `feat/ml/jordan/mobilenet-training`
  * Bug fixes: `fix/backend/sam/cors-headers`
  * Documentation: `docs/caden/api-contracts`

*(Never use generic names like `test`, `temp`, `dev`, or branches lacking owner identity).*

---

## 3. Atomic Commits
* **Single Logical Change:** Keep commits small, atomic, and focused on one specific responsibility.
* **No Mixed Concerns:** Do not combine bug fixes, refactoring, documentation updates, and new features into a single commit.
* **Clean Working Tree:** Stage only the files directly related to the change.

---

## 4. Commit Message Conventions
Follow Conventional Commits formatted in lowercase imperative mood without trailing periods:

```text
<type>(<scope>): <concise description>
```

* **Types:**
  * `feat`: New feature or user-facing capability
  * `fix`: Bug fix or patch
  * `docs`: Documentation updates only
  * `chore`: Tooling, configs, dependencies, or scaffolding
  * `refactor`: Code restructuring without functional change
  * `test`: Adding or updating test suites
* **Examples:**
  * `feat(camera): add viewfinder preview`
  * `chore: initialize universal project directories with ignore.md placeholders`

---

## 5. Post-Implementation Unbiased Code Tracing & Verification
Once code is written, do NOT immediately commit or declare completion. Perform a rigorous, unbiased self-review:

1. **Execution Trace:** Mentally trace every code path, including branch conditions, exceptions, edge cases, null/undefined inputs, and async flows.
2. **Lint & Static Check:** Run linters and checks locally:
   * Python: `ruff check .`
   * Format check: `ruff format --check .`
   * Frontend: check dependencies and syntax
3. **Proactive Bug Fixing:** If any flaw, vulnerability, unhandled exception, or regression is detected, fix it immediately before committing.

---

## 6. Push to Main
* Once changes are verified, trace-tested, and cleanly committed:
  1. Verify the branch is up-to-date with remote (`git pull origin main`).
  2. Push the atomic commits to `main` (`git push origin main`).
  3. Confirm clean working tree with `git status`.
