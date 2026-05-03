---
name: commit
description: Use this skill when the user asks to "commit", "make a commit", or "commit the changes". It commits currently staged changes following the Conventional Commits format. Never amend existing commits — always create a new one.
---

## Steps

1. **Inspect staged changes**

   Run these in parallel to understand what will be committed:

   ```bash
   git diff --cached
   git status
   ```

2. **Draft the commit message**

   Use the [Conventional Commits](https://www.conventionalcommits.org/) format:

   ```
   <type>(<scope>): <short summary>
   ```

   - **type** — one of: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `perf`, `ci`, `build`
   - **scope** — optional; name of the module, layer, or file affected (e.g. `appointments`, `crud`, `auth`)
   - **summary** — imperative mood, lowercase, no trailing period, ≤72 characters

   Add a body only when the *why* is not obvious from the summary. Skip footers (no `Co-Authored-By` or similar trailers).

   Examples:
   ```
   feat(appointments): add duration field with 15-minute multiple validation
   fix(crud): correct partial update to use exclude_unset=True
   test(appointments): add coverage for overlapping slot edge case
   chore: update uv lockfile
   ```

3. **Commit using a HEREDOC** (preserves formatting)

   ```bash
   git commit -m "$(cat <<'EOF'
   <type>(<scope>): <summary>

   <optional body>
   EOF
   )"
   ```

4. **Verify success**

   ```bash
   git log --oneline -3
   git status
   ```

   Confirm the commit appears and the working tree is clean.

## Rules

- Only commit what is already staged. Do not run `git add` unless the user explicitly asks.
- Never use `--no-verify` or skip hooks.
- Never amend a previous commit — always create a new one.
- Do not push unless the user explicitly asks.
