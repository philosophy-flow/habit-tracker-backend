# OVERVIEW

This application allows users to track their habits over time. It includes many facets of full-stack web application development, including ORM-leveraged CRUD operations against a normalized relational database; user registration, authentication, and token-based sessions; user profile management; and habit tracking, with visualizations for habit streaks and additional statistics.

# FEATURE SCOPE

**Core Features:**
- **User Authentication**: Signup with email verification and session management via JWT.
- **Habit Management**: Add and delete habits; edit name and frequency.
- **Tracking Progress**: Toggle habits as complete / incomplete for the current day.
- **User Profile Support:** Change profile picture, update password and email.
- **Statistics:** Visualize extended tracking info for the month and completion rates.
    - **User profile support and statistics are not yet available.**

**Stretch Goals:**
- **CI/CD Pipeline + Testing:** Deployment pipeline with automated testing step and build steps.
- **Category/Tagging System**: Organize habits by type (health, work, personal, etc.) or color.

<br>

# STACK
- **Frontend:** React/Vite + TypeScript + Tailwind CSS + Redux Toolkit Query
- **Backend & Database:** FastAPI + SQLModel + PostgreSQL

<br>

# HOSTING
- **Frontend / Backend:** Self-hosted on VPS
- **Database:** Supabase

<br>

# LINKS
- [**Project Roadmap**](https://basepraxmatic.net/habitsior-project-roadmap.pdf)
- **Production**
    - [App (habitsior.app)](https://habitsior.app)
    - [API Docs (api.habitsior.app/docs)](https://api.habitsior.app/docs)
- **Code**
    - [Frontend Repository](https://github.com/philosophy-flow/habit-tracker-frontend)
    - [Backend Repository](https://github.com/philosophy-flow/habit-tracker-backend)
- **Additional Assets**
    - [Original Mobile Design (figma)](https://basepraxmatic.net/habitsior-original-mobile-design.fig)
    - [Database Schema (sql)](https://basepraxmatic.net/habitsior-schema.sql)
    - [Database ERD (pdf)](https://basepraxmatic.net/habitsior-erd.pdf)
    - [Authentication Flow Diagram (pdf)](https://basepraxmatic.net/habitsior-auth-flow.pdf)
- **Additional Documentation**
    - [Account Registration (pdf)](https://basepraxmatic.net/habitsior-account-registration.pdf)
    - [Account Authentication (pdf)](https://basepraxmatic.net/habitsior-account-authentication.pdf)
    - [Habits Considerations (pdf)](https://basepraxmatic.net/habitsior-habits-considerations.pdf)