# TOOLY — Architecture technique

## 1. Principles

Tooly is built as a modular application. Business domains must remain separated so that a change in one domain does not force changes in unrelated modules.

Core rules:
1. Frontend, API, business logic and persistence are separate layers.
2. One business datum exists only once.
3. New domains are created in dedicated folders.
4. FR / NL / EN / PL are supported from the start.
5. Business codes are stable and language-independent.
6. Documents are referenced by metadata; external storage may later be delegated to SharePoint.
7. Equipment history is archived, not overwritten.
8. No VMA-specific data is hard-coded.

## 2. Repository layout

```text
Tooly/
├── backend/
│   └── app/
│       ├── api/
│       ├── core/
│       ├── db/
│       ├── domains/
│       │   ├── organization/
│       │   ├── equipment/
│       │   ├── assignments/
│       │   ├── inspections/
│       │   ├── documents/
│       │   ├── external_reports/
│       │   ├── products/
│       │   └── worksites/
│       └── main.py
├── frontend/
│   └── src/
│       ├── app/
│       ├── components/
│       ├── i18n/
│       └── modules/
│           ├── equipment/
│           ├── assignments/
│           ├── inspections/
│           ├── documents/
│           ├── externalReports/
│           ├── products/
│           └── worksites/
├── migrations/
├── tests/
├── documentation/
├── scripts/
└── imports/
```

## 3. Backend domain convention

Each domain should use its own package:

```text
domains/<domain>/
├── models.py
├── schemas.py
├── repository.py
├── service.py
├── router.py
└── __init__.py
```

Large domains may split these files further into submodules. Routers must not contain business rules.

## 4. Frontend module convention

```text
modules/<module>/
├── pages/
├── components/
├── api/
├── types/
├── i18n/
└── styles/
```

Large React components must be split by responsibility.

## 5. First vertical slice

Equipment import → search by number → equipment record → assignment → inspection requirement → worksite verification/inspection → result → next due date → history.
