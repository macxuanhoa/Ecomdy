# Decision Log

| ID | Decision | Basis | State |
|---|---|---|---|
| DEC-001 | Preserve `origin/main` and work on `setup/phase-0-audit`. | Remote `main` already contains commit `560cf0d`; local starter is not based on it. | Applied |
| DEC-002 | Keep original PDFs, workbook, and image out of Git. | Source README directs local-only storage; Git ignore is configured; GitHub repository is public. | Applied |
| DEC-003 | Treat the challenge workbook as the source for mandatory requirements; treat blueprint and image extensions as proposals unless the challenge brief confirms them. | Direct reading of the supplied workbook, PDFs, and image. | Applied |
| DEC-004 | Do not characterize Ecomdy as an implemented product. | The local repository contains documentation and diagrams, no application source/runtime. | Applied |
| DEC-005 | Keep DevHarness OS independent from Ecomdy runtime logic. | Existing Ecomdy instructions and source blueprint define separate responsibilities. | Applied |
