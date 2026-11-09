---
name: filesystem-refactor
description: Refactor filesystem objects and preserve intended references. Use when renaming, moving, merging, replacing, or deleting Non-temporary files or directories.
---

# Filesystem refactor

Treat each invocation as one semantic transaction. A transaction may contain several operations of different kinds; independent transactions get separate workers.

## Own the intent

Express the transaction in natural language so another agent can determine:

- the source objects;
- whether each requested change is a rename, move, merge, replace, or delete;
- the intended final locations and object relationships;
- the workspace and modification boundary;
- collision and reference dispositions already decided;
- additional requirements;
- whether to run builds, full tests, or other costly validation.

Use whatever form communicates the intent uniquely. Fixed fields are unnecessary. Let the worker infer facts that can be safely discovered from the environment.

Moving, merging, replacing, and deleting are distinct semantics. If the requested result is ambiguous, clarify it before delegation.

## Delegate one transaction

When subagents are available, appoint one worker as the transaction’s only workspace writer. Give it:

1. the natural-language transaction;
2. the workspace and authority boundary;
3. any additional requirements;
4. the path to [`references/worker-protocol.md`](references/worker-protocol.md);
5. an instruction to read that protocol before inspecting or changing the workspace.
6. access to any available LSP or MCP for analysis, code/symbol resolution and cross-reference discovery.

Use a delegation such as:

> Execute this single filesystem-refactor transaction. Read `<skill-path>/references/worker-protocol.md` before inspecting or changing the workspace. You are the transaction’s only workspace writer.  
>  
> <transaction intent, boundary, and additional requirements>

The worker owns discovery, planning, execution, reference repair, recovery materials, and verification from end to end.

Keep the worker protocol behind this pointer: the worker needs it; the delegating agent does not.

When subagents are unavailable, become the worker: read
[`references/worker-protocol.md`](references/worker-protocol.md) and follow it completely.

## Handle worker returns

A completed report closes the transaction.

A blocked report returns facts and decision rights to the caller. Resolve the ambiguity or risk, then communicate the revised transaction intent explicitly to the existing worker. In particular, explicitly approve any change of semantics such as:

- move becoming merge;
- move becoming replace;
- merge discarding a colliding object;
- delete or replace requiring an undecided reference disposition.

Start a replacement worker only when resumption is unavailable or unsafe, and pass forward the prior report and artifacts. Preserve one workspace writer per transaction.