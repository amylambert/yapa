# YAPA - Technical Architecture Specification

This engineering manifest details the system architecture, underlying models,
and operational specifications of the YAPA system framework.

## 1. System Architecture & Environment

The ecosystem runs on a decoupled multi-container layout managed via Docker:

- **Application Layer:** Django 5.0 Framework running Python 3.11+.
- **Persistence Layer:** PostgreSQL 16+ relational engine.
- **Environment Governance:** Configuration constants are localized inside a
  non-committed `.env` file managed by `django-environ`.

## 2. Structural Abstraction Layer (`core` App)

To enforce DRY principles and eliminate database JOIN query overhead during
heavy iteration loops, core fields leverage an abstract architecture root.

### `ComponentBlueprint` Model

An abstract codebase structure sharing essential attributes across apps:

- `name` (Encrypted TextField)
- `description` (Encrypted TextField)
- `priority` (TextChoices: `LOW`, `MEDIUM`, `HIGH`)
- `start_date` / `end_date` (Chronological validation controls)
- `owner` (Foreign Key referencing Django's standard User identity)

### Column-Level Field Encryption

Data sensitivity is maintained at rest via `EncryptedTextField`. It automatically
intercepts strings and pipes them through a symmetrical key framework:

- **Engine:** Cryptography library running standard `Fernet` recipes.
- **Key Derivation:** Safely hashes a 32-byte URL-safe base64 key generated
  directly from Django's unique environment `SECRET_KEY`.

## 3. App Modules & Domain Contexts

- **`accounts`**: Manages credential hashing loops, secure signups, profile metadata,
  and async user attribute mutations via validated `XMLHttpRequest` blocks.
- **`core`**: Consolidates layout contexts and runs optimization metrics evaluating
  the closest task deadlines across all combined streams.
- **`notes`**: Handles parent-child document relationships, automatic model-level validation
  ensuring notes don't exceed the dates of their parent project, and localized many-to-many
  tag generation blocks.

## 4. AJAX & Async Interoperability Controls

Asynchronous inline editing endpoints (like `NoteInlineUpdateView` and
`AccountUpdateView`) perform real-time partial writes:

- Payload processing enforces strict field whitelisting parameters.
- Request sources are validated using explicit `x-requested-with` checking.
- Strict execution hooks run `.full_clean()` explicitly before calling `.save()`
  to catch chronological validation issues before writing to the database.
