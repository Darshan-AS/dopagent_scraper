# Tasks

- [ ] Find better ways to handle CAPTCHA (currently manual input)
- [ ] Extract navigation responsibility out of the Auth spider. The Auth spider should only handle login/authentication, while navigation to specific sections (like Accounts, Installments) should be handled by their respective spiders or a dedicated navigation class.
- [ ] Add proper and consistent logging across all spiders and utilities to ensure traceability and easy debugging.
- [ ] Refactor the codebase to use functional programming paradigms wherever possible (e.g., using map/filter, pure functions, avoiding state mutations) to improve code readability and testability.
