*This project has been created as part of the 42 curriculum by jamsilva.*

# 🐍 Python_Module_05-10

![Language](https://img.shields.io/badge/language-Python_3.10+-blue.svg)
![42](https://img.shields.io/badge/42-Python_Piscine-black.svg)
![Status](https://img.shields.io/badge/status-Completed-success.svg)
![Lint](https://img.shields.io/badge/flake8_%2B_mypy-passing-brightgreen.svg)

---

## Description

`Python_Module_05-10` covers the advanced track of the 42 Python curriculum, from **Module 05 to Module 10**. Building on core syntax, OOP, exception handling and data structures (Modules 00–04), this repository moves into software architecture, design patterns, dependency management, data validation and functional programming.

Each module is framed as a step in an architectural journey through a different "realm", introducing one enterprise-grade concept at a time: abstract base classes, Python's import mechanics, classic design patterns, virtual environments, Pydantic validation, and functional programming.

---

## Project Overview

| Module | Theme      | Main Focus                                                                |
|:------:|:-----------|:---------------------------------------------------------------------------|
| **05** | Code Nexus | Abstract Base Classes (`ABC`), polymorphism, data streams                  |
| **06** | The Codex  | Import mechanics, package architecture (`__init__.py`), circular imports  |
| **07** | DataDeck   | Design patterns — Abstract Factory, Capabilities/Mixins, Strategy         |
| **08** | The Matrix | Virtual environments (`venv`), package managers (`pip` / Poetry), `.env`  |
| **09** | Cosmic Data| Data validation & schemas with **Pydantic v2** (`BaseModel`, `@model_validator`) |
| **10** | FuncMage   | Functional programming — lambdas, higher-order functions, closures, `functools`, decorators |

---

## Key Features

- **Polymorphic data pipelines** — unified processing interfaces built on `abc.ABC` and `@abstractmethod`.
- **Modular package design** — relative vs. absolute imports, namespace isolation, and circular-import resolution.
- **Architectural design patterns** — Abstract Factory, Mixin/Capabilities and Strategy patterns applied to a card-game domain.
- **Data engineering basics** — isolated runtimes (`venv`), dependency locking (`pip` vs. Poetry), and secure config loading (`python-dotenv`).
- **Schema validation & integrity** — data models built with **Pydantic v2**, with field constraints, nested models and custom validators.
- **Functional paradigm** — `lambda`, higher-order functions, closures with `nonlocal`, memoization (`lru_cache`), and custom decorators.
- **Strict compliance** — fully PEP 8 compliant, validated with `flake8` and statically typed with `mypy`.

---

## Module Breakdown

### Module 05 — Code Nexus (Polymorphic Data Streams)
Abstract architecture and a unified data-processing interface.
- **Abstract Base Classes** — interface contracts via `abc.ABC` and `@abstractmethod`.
- **Specialized processors** — `NumericProcessor`, `TextProcessor`, `LogProcessor`.
- **Stream ingestion & polymorphism** — heterogeneous data handled through one adaptive stream, without breaking type safety.

### Module 06 — The Codex (Import Mechanics)
Python's import system and package construction.
- **Package initialization** — `__init__.py` turning directories into packages, `__all__` management.
- **Import pathways** — absolute vs. relative imports across nested subpackages (`alchemy.grimoire`, `alchemy.transmutation`).
- **Circular dependency resolution** — identified and fixed without touching `sys.path`.

### Module 07 — DataDeck (Abstract Card Architecture)
Classic GoF design patterns applied to a scalable card-game system.
- **Abstract Factory** — `FlamelingFactory`, `AquabubFactory` producing families of related objects.
- **Capabilities & Mixins** — extending card behaviour through modular capability interfaces.
- **Strategy Pattern** — battle strategies and effects decoupled from the core card entity.

### Module 08 — The Matrix (Virtual Environments & Config)
Environment setup and configuration security.
- **Environment detection** — `sys.prefix`, `site-packages`, and venv detection in `construct.py`.
- **Dependency management** — `pip` (`requirements.txt`) vs. Poetry (`pyproject.toml`); Matrix data analysed with `pandas`, `numpy`, `matplotlib`.
- **Secret management** — environment variables read securely from `.env` via `python-dotenv`.

### Module 09 — Cosmic Data (Pydantic Models & Validation)
Robust data parsing and schema enforcement with **Pydantic v2**.
- **Schema definition** — `BaseModel` and `Field` constraints.
- **Custom validation** — root/model validators with `@model_validator(mode='after')`.
- **Nested models** — Space Stations, Alien Contacts and Space Crew, with automatic type conversion.

### Module 10 — FuncMage (Functional Programming)
- **Anonymous functions** — `lambda` with `map()`, `filter()`, `sorted()` and aggregations.
- **Higher-order functions** — functions as first-class citizens, composition, `Callable` annotations.
- **Closures & scope** — lexical scoping, state preservation, `nonlocal`.
- **Functools & operators** — `functools.reduce`, `functools.partial`, `functools.lru_cache`.
- **Decorator mastery** — custom decorators built with `@functools.wraps`.

---

## Project Structure

```
.
├── module05/
│   ├── ex0/                   # Data Processor (ABC)
│   └── ex1/                   # Polymorphic Data Streams
├── module06/
│   ├── alchemy/                # Main package
│   │   ├── grimoire/           # Subpackage
│   │   └── transmutation/      # Subpackage
│   ├── ft_alembic_*.py         # Basic import experiments
│   ├── ft_distillation_*.py    # Alias and submodule imports
│   ├── ft_transmutation_*.py   # Cross-package imports
│   └── ft_kaboom_*.py          # Circular dependency resolution
├── module07/
│   ├── ex0/                   # Abstract Factory (Creature Factory)
│   ├── ex1/                   # Capabilities & Mixins
│   ├── ex2/                   # Strategy Pattern
│   └── battle.py               # Root test runner
├── module08/
│   ├── ex0/                   # Virtual Environment Detection (construct.py)
│   ├── ex1/                   # Dependency Management (loading.py, pip vs poetry)
│   └── ex2/                   # Mainframe Secrets (oracle.py, .env)
├── module09/
│   ├── ex0/                   # Space Station Model (Pydantic BaseModel)
│   ├── ex1/                   # Alien Contact Validation (@model_validator)
│   └── ex2/                   # Space Crew (Nested Pydantic Models)
├── module10/
│   ├── ex0/                   # Lambda Sanctum (lambda_spells.py)
│   ├── ex1/                   # Higher Realm (higher_magic.py)
│   ├── ex2/                   # Memory Depths (Closures & nonlocal)
│   ├── ex3/                   # Ancient Library (functools_artifacts.py)
│   └── ex4/                   # Master's Tower (decorator_mastery.py)
└── README.md
```

---

## Instructions

### Requirements

- **Python 3.10+**
- `flake8`, `mypy`
- `pydantic` (Module 09)
- `python-dotenv`, `pandas`, `numpy`, `matplotlib` (Module 08)

### Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Execution

| Command                              | Runs                                   |
|---------------------------------------|-----------------------------------------|
| `python3 module05/ex0/data_processor.py` | Module 05 — polymorphic data processor |
| `python3 module07/battle.py`          | Module 07 — card battle demo            |
| `python3 module08/ex0/construct.py`   | Module 08 — virtual-env detection       |

Other exercises follow the same pattern: run the script directly from its `exN/` directory.

### Validation

```bash
flake8 .
mypy .
```

*Both tools must return zero errors for the code to be considered fully compliant.*

---

## What I Learned

- **Software architecture** — designing modular, extensible software with Abstract Base Classes and GoF patterns.
- **Python package internals** — namespace resolution, relative/absolute imports, circular-dependency debugging.
- **Data engineering workflows** — isolating runtimes, managing dependencies with Poetry, securing configuration keys.
- **Production data validation** — guaranteeing integrity for complex nested structures with Pydantic v2.
- **Functional concepts** — purity, higher-order composition, closures, memoization, decorators.

---

## Resources

- [Python 3 Documentation](https://docs.python.org/3/)
- [PEP 8 — Style Guide for Python Code](https://peps.python.org/pep-0008/)
- [PEP 484 — Type Hints](https://peps.python.org/pep-0484/)
- [Pydantic v2 Documentation](https://docs.pydantic.dev/latest/)
- [Real Python — Imports, OOP Patterns & Functional Programming](https://realpython.com/)

### AI Usage

AI was used as a Socratic learning aid for:
- Clarifying architectural patterns (Abstract Factory, Strategy Pattern).
- Debugging circular-import mechanics and Pydantic v2 validation pipelines.
- Formulating test cases and checking edge-case type annotations.

All implementations, tests and final verifications were done manually.

---

## Author

**Jamielly R.**

https://github.com/Jamielly
