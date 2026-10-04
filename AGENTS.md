# AGENTS.md

## Project

This repository contains the ETL core for a production treasury processing system.

Correctness, determinism and auditability always take priority over code aesthetics.

---

## Hard Constraints

Never:

- modify the database schema
- create migrations
- invent database models
- invent business rules
- invent accounting logic
- invent reconciliation logic
- modify .env
- expose secrets

If database information is required:

Ask the user.

Never guess.

---

## Architecture

Respect the existing layered architecture.

- processors → external layouts
- services → business logic
- repositories → persistence
- main.py → orchestration
- libs → infrastructure

Do not move responsibilities between layers.

---

## Development Rules

Before writing code:

- understand the existing implementation
- reuse existing processors
- reuse existing services
- reuse existing repositories

Do not create duplicate implementations.

Prefer extending existing code.

---

## Coding Standards

- Python 3.10+
- type hints
- snake_case
- comments in English
- prefer vectorized pandas operations over `.apply()` or loops
- document the "why" (business intent, accounting context), never the "what" (no code parroting)
- use PEP 257 docstrings instead of narrating code line-by-line
- prefer early returns to avoid deeply nested blocks

---

## Data Integrity & Pandas Rules

- Prevent Cartesian products: always verify and deduplicate catalog/mapping keys (`drop_duplicates`) before a `merge` to avoid multiplying financial transactions.
- Clean and normalize merge keys (types, whitespace, decimals) before relational joins.
- Avoid redundant operations (e.g., do not call `reset_index` right after `concat(ignore_index=True)`).
- Fail Fast: never catch broad `Exception` in transformation pipelines; catch only specific expected errors (e.g., `SQLAlchemyError`) and keep DataFrame manipulations outside `try/except` to expose bugs immediately.

---

## Review Priorities

Priority order:

1. Business correctness
2. Data integrity
3. Determinism
4. Maintainability
5. Performance

Never optimize for elegance.

Optimize for correctness.

---

When requirements are unclear:

Ask.

Never assume.