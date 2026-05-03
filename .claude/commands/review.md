Review the code at the path or pattern given in $ARGUMENTS. Check for:

**Bugs**
- Logic errors, off-by-one mistakes, unhandled edge cases
- Incorrect use of async/await or concurrency primitives
- Resource leaks (unclosed files, DB sessions, connections)
- Wrong assumptions about nullability or optional fields

**Security**
- Injection vulnerabilities (SQL, command, path traversal)
- Missing input validation or over-trusting user-supplied data
- Sensitive data exposed in logs, responses, or error messages
- Insecure defaults or missing authentication/authorization checks

**Code quality**
- Dead code or unreachable branches
- Overly complex logic that could be simplified
- Naming that obscures intent
- Missing or incorrect error handling
- Violations of the project's existing conventions (see CLAUDE.md)

For each finding, state: the file and line number, the category (Bug / Security / Quality), a one-line description, and a concrete fix or suggestion. If nothing is found in a category, say so explicitly. Finish with a short overall verdict.
