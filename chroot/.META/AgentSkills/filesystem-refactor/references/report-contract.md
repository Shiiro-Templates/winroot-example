# Filesystem-refactor report contract

Return a concise natural-language report to the caller. 

## Successful transaction

Account for:

1. the operations actually completed and the final paths or object relationships;
2. the kinds and number or locations of references repaired;
3. credible candidates or semantic mentions intentionally left unchanged, with reasons;
4. every validation performed and its result;
5. requested or relevant validation not run or left inconclusive;
6. recovery or temporary material retained, including its location and purpose;
7. remaining risks or recommended human review.

State completion only when the requested semantic transaction and its required reference repairs are complete.

## Blocked, failed, or partial transaction

Account for:

1. the stage where progress stopped;
2. the facts established from the workspace;
3. the ambiguity, conflict, authorization problem, unresolved reference, validation failure, or changed assumption that prevents continuation;
4. every modification already made and every operation still pending;
5. the current state of affected paths;
6. recovery attempts already made;
7. retained recovery material, its location, and what it can restore;
8. available options and the recommended next choice;
9. the exact decision or clarified intent required from the caller.

Distinguish facts from recommendations. A proposed operation is not approved until the caller expresses the revised intent.

If continuing would change operation semantics—for example, move becoming merge or replace—name both the requested and observed semantics explicitly.