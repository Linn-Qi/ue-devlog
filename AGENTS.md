# Project handoff rules

## Houdini classroom work

- Before diagnosing or modifying this project, read the latest successful baseline at [`Houdini.md#baseline-1126-merged-20261126`](Houdini.md#baseline-1126-merged-20261126). Older dated chapters remain historical references and must not silently override it.
- The latest user-confirmed combined working file is `E:/1126/1126.hip`. `E:/1126/tableright.hip` and `E:/1126/wallright.hip` are protected correct sources. `E:/1126/_merge_rollback/1126.hip` is the pre-merge rollback, not the successful result.
- Confirm the actual full open path, using `hou.hipFile.path()` when available. A filename alone or stale saved `HIPFILE` variable does not identify the active version.
- Keep work within the user's current scope. Preserve already approved assets, original animation, node parameters, UV caches, material dependencies, and source files unless the task authorizes changing them.
- The successful 1126 operation transplanted the complete `/obj/other` asset from tableright while preserving every other target record. It did not generate new chair UVs or rebuild animation. Do not redo whole-scene UV or reduction as a default repair.
- The archived merge script and byte ranges are specific to two checked SHA-256 inputs. Never remove its identity guards or reuse offsets against a changed/re-saved HIP.
- A disk write does not refresh an open Houdini scene. Distinguish archive validation, native loading, user visual confirmation, and full animation/export testing; report only the checks actually completed.
- User delivery preference: standalone, copyable Houdini Python Shell code, with one clear result path and a clearly identified rollback. Avoid dependence on previous Shell variables and avoid unnecessary full-frame cook/export or application restarts.
- Preserve both successful and failed evidence accurately. The latest approval concerns the combined shape at frame 20; it is not a new full-animation, all-UV, SP, UE, or Alembic export certification.
