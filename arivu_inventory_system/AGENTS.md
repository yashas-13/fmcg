# Contributor Guide for Arivu Inventory Management System

This guide serves as the foundational agreement for all development within the Arivu IMS project. It outlines our core principles, development environment, coding standards, and how AI agents are expected to operate and present their work.

---

## 1. Core Development Principles

These principles should guide every decision and piece of code generated:

* **Security First:** Always prioritize security. Implement authentication, authorization (RBAC), input validation, and proper error handling with security implications in mind. Never expose sensitive data directly to the frontend.
* **Modularity & Separation of Concerns:** Keep components loosely coupled. Business logic belongs in services, API handling in routes, data definitions in models, and UI in templates/static files.
* **Readability & Maintainability:** Code should be clear, concise, and easy for other developers (human or AI) to understand and modify.
* **Data Integrity:** Ensure database operations are transactional and maintain data consistency.
* **Scalability (Consideration):** While starting simple, design choices should allow for future growth and increased load without major rewrites.

---

## 2. Project Overview & Structure

The Arivu IMS is a Flask-based application designed to manage inventory and production for manufacturers and sales/orders for retailers, accessible via distinct dashboards.

* **Project Root (`arivu_inventory_system/`):** The top-level container for the entire project.
    * `AGENTS.md`: This very guide for AI agent configuration.
    * `README.md`: General project description and setup instructions.
    * `arivu-venv/`: The Python virtual environment.
    * `arivu.db`: The SQLite database file (for development/testing).
    * `frontend/`: **Temporary storage for initial HTML templates. These *will be moved* to `supply_chain_system/templates/` and their associated CSS/JS to `supply_chain_system/static/` during project setup phase.**
    * `requirements.txt`: Python package dependencies.
* **`supply_chain_system/`**: The main Python Flask application package.
    * **`__init__.py`**: Application factory for `create_app()`.
    * **`main.py`**: The primary entry point for running the Flask application.
    * **`config/settings.py`**: Centralized application configurations (DB URI, `SECRET_KEY`, etc.).
    * **`database/`**: Database core logic and ORM models.
        * `core.py`: SQLAlchemy engine, session management, `create_all_tables()`.
        * `models.py`: **All** SQLAlchemy ORM model definitions (User, Product, Order, ProductionBatch, RawMaterial, etc.).
    * **Domain Modules (e.g., `auth/`, `users/`, `products/`, `inventory/`, `production/`, `orders/`, `finished_goods/`):** Each module encapsulates a specific functional domain.
        * `routes.py`: Contains Flask Blueprints/API endpoints for the module.
        * `service.py`: **Crucial.** Contains all core business logic for the module, interacting with `database/models.py`. Routes should call services, not interact directly with models or DB sessions.
    * **`utils/`**: General utility functions and decorators.
        * `decorators.py`: `@login_required`, `@role_required`.
        * `logger.py`: Centralized logging configuration.
    * **`templates/`**: (To be created/populated) Flask's default directory for Jinja2 HTML templates.
    * **`static/`**: (To be created/populated) Flask's default directory for static assets (CSS, JavaScript).
        * **`static/css/`**: Will contain project-specific `style.css` and **Bootstrap CSS files (e.g., `bootstrap.min.css`)**.
        * **`static/js/`**: Will contain project-specific `main.js` and **Bootstrap JavaScript files (e.g., `bootstrap.bundle.min.js`)**.

---

## 3. Development Environment & Setup

* **Virtual Environment:** Always activate `arivu-venv` before running any commands or writing code that uses dependencies.
    ```bash
    source arivu-venv/bin/activate
    ```
* **Dependency Installation:** Install required Python packages.
    ```bash
    pip install -r requirements.txt
    ```
* **Database Initialization & Seeding:**
    * The `create_all_tables()` function should be callable (e.g., through a management command or `main.py` on first run).
    * A `seed_db.py` script is expected to populate initial `User` accounts (manufacturer, retailer roles) and basic `Product`, `RawMaterial` data for testing.
* **Run Application:**
    ```bash
    python supply_chain_system/main.py
    ```

---

## 4. Contribution & Style Guidelines

* **Code Quality:**
    * **Python:** Adhere strictly to PEP 8. Use `flake8` for linting.
    * **SQLAlchemy:** Utilize the ORM effectively for database interactions; avoid raw SQL unless absolutely necessary.
    * **JavaScript:** Maintain clean, readable, modern ES6+ JavaScript.
    * **HTML/CSS:** Semantic HTML, well-structured CSS (e.g., BEM-like naming for classes if component-based). **Leverage Bootstrap classes for styling and responsive design.**
* **Modularization:** All new features or refactorings *must* follow the `routes.py` (API) -> `service.py` (Business Logic) -> `database/models.py` (Data Layer) pattern. No direct model interaction from routes.
* **Error Handling:** Implement robust error handling at both Backend (return appropriate HTTP status codes and JSON error messages) and Frontend (display user-friendly messages). Use Python's `try...except` and JavaScript's `try...catch` blocks.
* **Logging:** Use `supply_chain_system/utils/logger.py` for all application logging. Log informational messages, warnings, and errors appropriately. Avoid excessive logging in development that would clutter production logs.
* **Security:** Always sanitize user inputs. Use parameterized queries (ORM handles this). Never hardcode sensitive information.
* **Performance:** Optimize database queries (e.g., eager loading where appropriate). Consider efficiency of data processing in services for large datasets.

---

## 5. Validating Changes

All changes must pass the following validation steps. An AI agent should propose specific manual testing steps with each feature implementation.

* **Automated Tests (Future):**
    * **Unit Tests:** For `service.py` functions and utility helpers (e.g., `decorators.py`).
    * **Integration Tests:** For API endpoints (testing `routes.py` and service interaction).
    * *(Note: Initial setup may not include a test suite, but design for testability. AI should propose adding tests for new complex logic.)*
* **Manual Testing:**
    1.  **Application Startup:** Verify `python supply_chain_system/main.py` starts without errors.
    2.  **Database Integrity:** Ensure `arivu.db` is correctly created/migrated, and seeded data is present.
    3.  **Login Functionality:**
        * Access `/login` (or `/` if root is login).
        * Log in successfully with `manufacturer` credentials.
        * Log in successfully with `retailer` credentials.
        * Test invalid credentials.
    4.  **Dashboard Access & RBAC:**
        * After manufacturer login, verify redirection to Manufacturer Dashboard. Attempt to manually navigate to retailer routes (`/api/retailer/...`) and verify `403 Forbidden`.
        * After retailer login, verify redirection to Retailer Dashboard. Attempt to manually navigate to manufacturer routes (`/api/manufacturer/...`) and verify `403 Forbidden`.
    5.  **Manufacturer Dashboard Features:**
        * Verify all production schedule data displays correctly.
        * Verify raw material stock data displays correctly.
        * Test creating new production batches.
        * Test completing existing production batches (check stock updates).
    6.  **Retailer Dashboard Features:**
        * Verify sales summary and top products display.
        * Verify pending orders list displays.
        * Verify finished goods stock displays.
        * Test updating order status (e.g., 'shipped', 'delivered').
    7.  **Error Handling:** Test edge cases (e.g., invalid input to API, missing data) and observe appropriate error messages on both frontend and backend logs.
    8.  **Frontend Responsiveness:** Verify that the UI (due to Bootstrap) adapts gracefully to different screen sizes (browser resizing).

---

## 6. How to Work (For AI Agents)

* **Context Exploration Strategy:**
    * **Narrow Down First:** Start by analyzing the specific files mentioned in the prompt.
    * **Expand as Needed:** If context is insufficient, expand exploration to:
        * Associated `service.py` for `routes.py` tasks.
        * `database/models.py` for any data-related tasks.
        * `supply_chain_system/utils/decorators.py` for authentication/authorization.
        * `supply_chain_system/main.py` for application setup/blueprint registration.
        * `supply_chain_system/config/settings.py` for configuration variables.
        * **Frontend-specific context:** `supply_chain_system/templates/` and `supply_chain_system/static/` for UI and asset management.
    * **Prioritize Existing Patterns:** Replicate existing patterns (e.g., how a `routes.py` calls a `service.py` function) when adding new features.
* **Code Generation Expectations:**
    * **Completeness:** Provide full, runnable code blocks for all specified files/sections. Do not provide partial snippets unless explicitly instructed.
    * **Modularity:** Always place business logic into `service.py` files. Create new service methods as needed.
    * **Defensive Coding:** Include basic input validation, type hints (if applicable), and error handling (`try...except`).
    * **Reusability:** Identify and utilize existing utility functions or create new, generic ones in `supply_chain_system/utils/` when common logic is needed.
    * **Bootstrap Integration:** When creating or modifying frontend HTML, actively use Bootstrap classes for styling and components (e.g., `container`, `row`, `col`, `table`, `btn`, `form-control`, `navbar`).
* **Testing Protocol:**
    * For *every* non-trivial code generation or modification task, propose **specific, actionable manual testing steps** that verify the implemented functionality (referencing Section 5).
    * If unit/integration test suites are introduced later, propose adding or updating relevant tests.
* **Documentation Protocol:**
    * Add clear docstrings to new functions and classes.
    * Add concise inline comments for complex or non-obvious logic.
    * If a major feature is implemented, suggest updating the `README.md` with relevant usage instructions.
* **Output Format & Presentation:**
    * Clearly state the file path (`e.g., supply_chain_system/production/routes.py`) before providing the code block.
    * For modifications, clearly indicate which lines are added, removed, or changed.
    * Summarize the changes made and their impact on the system's functionality.
* **Debugging & Error Reporting:**
    * If encountering issues or ambiguities, report them clearly, referencing relevant file paths, line numbers, and error messages (if applicable).
    * Suggest potential causes or debugging steps.
* **Task Splitting:** For highly complex requests, propose breaking them down into smaller, focused sub-tasks, estimating the effort for each.
* **Adaptation & Learning:** Continuously learn from feedback and previous iterations. Self-correct and adapt to evolving project requirements and conventions.
## 7. Agent Iteration & Self-Review

* **Analyze Before Acting:** Thoroughly read related code and documentation before modifying files.
* **Iterative Workflow:** Make small, focused commits and run validation checks after each change.
* **Self Review:** Re-read modified sections to ensure compliance with this guide and fix simple mistakes.
* **Learning Record:** Note important decisions or lessons in PR summaries to assist future contributors.

