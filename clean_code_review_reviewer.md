# Clean Code Review (Reviewer)

## Review score
**7.1 / 10**

## Blocking issues
- None for MVP scope.

## Non-blocking improvements
1. Clarify path semantics in `jobs.yaml` (currently relative-to-config can produce `samples/samples/*` if users include `samples/` prefix).
2. Add explicit validation/warnings when resolved source path does not exist.
3. Add unit tests for path normalization and checkpoint behavior.
4. Add connector adapters for DB/S3/HTTP and retry backoff policies.

## Final recommendation
**DEPLOY**
