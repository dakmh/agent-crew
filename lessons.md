# Lessons

Rules learned from past mistakes. Read this file at the start of each session.

<!-- Append new rules below as mistakes are corrected. One concise rule per entry. -->

- **Ship tests in the same commit as the code they cover.** Splitting a fix from its regression test leaves a commit that cannot demonstrate what it claims, and a bisect that lands on an unproven fix.
- **Before overwriting a figure recorded in a project's docs, trace where it came from.** When a fresh measurement disagrees with a written one, find the evidence behind the written one first — the reason for the discrepancy is often more informative than the corrected number, and sometimes it is not an error at all. If a figure has no evidentiary home, that absence is itself the finding.
