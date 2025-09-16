# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **skill sessions booking platform** - a full-stack web application where users can create, browse, and book learning sessions with instructors. The project has been completely transformed from an Airbnb clone to support skill-sharing across various domains (coding, cooking, photography, language practice, etc.).

## Architecture

### Backend (`/backend`)
- **Framework**: Flask with SQLAlchemy ORM
- **Database**: MySQL with PyMySQL connector
- **API**: RESTful API using Flask-RESTx for documentation
- **Authentication**: Flask-Bcrypt for password hashing
- **Dependencies**: flask, flask-restx, flask-bcrypt, sqlalchemy, flask-sqlalchemy, flask-migrate, pymysql, cryptography, flask-cors

### Frontend (`/frontend`)
- **Framework**: Next.js (Pages Router) with React 19
- **UI Library**: Chakra UI
- **HTTP Client**: Axios
- **Styling**: Built-in Next.js CSS support

## Key Commands

### Backend Development
```bash
# Install dependencies
cd backend && pip install -r requirements.txt

# Run development server
cd backend && python run.py
# Server runs on http://localhost:5000 with auto-reload

# Run tests
cd backend && pytest filename
```

### Frontend Development
```bash
# Install dependencies
cd frontend && npm install

# Run development server
cd frontend && npm run dev
# Server runs on http://localhost:3000

# Build for production
cd frontend && npm run build

# Lint code
cd frontend && npm run lint
```

## Core Domain Models

The application is built around these main entities:

### User Model (`app/models/user.py`)
- Supports both learners and instructors (`is_instructor` flag)
- Profile fields: bio, profile_picture, phone, location, experience_level, hourly_rate
- Enhanced relationships: `skill_sessions_r`, `bookings_r`, `reviews_written_r`, `reviews_received_r`
- Methods: `add_skill_session()`, `add_booking()`, `get_average_rating()`

### SkillSession Model (`app/models/skill_session.py`)
- Represents learning opportunities created by instructors
- Session types: online, in-person, hybrid
- Fields: duration, max_participants, difficulty_level, location coordinates
- Methods: `get_available_spots()`, `is_fully_booked()`, `get_average_rating()`
- Connected to skills via many-to-many relationship

### Booking Model (`app/models/booking.py`)
- Manages session reservations with status workflow: pending → confirmed → completed
- Supports multiple participants per booking with automatic price calculation
- Methods: `confirm_booking()`, `cancel_booking()`, `complete_booking()`, `is_cancellable()`
- Only completed bookings allow review submission

### Review Model (`app/models/review.py`)
- Users review both sessions and instructors after completion
- Requires valid booking_id to ensure only participants can review
- Tracks reviewer (`user_id`) and reviewee (`instructor_id`)
- Enhanced validation to prevent duplicate reviews and ensure completion

### Skill Model (`app/models/skill.py`)
- Categorizes sessions by skill type (Technology, Arts, Language, Cooking, Music, etc.)
- Fields: name, description, category
- Many-to-many relationship with sessions for flexible tagging

## API Endpoints Structure

### Complete API Coverage
All endpoints have been updated to support the skill sessions domain:

- **`/api/v1/users`** - User management (existing, enhanced with instructor fields)
- **`/api/v1/skills`** - Skill categories CRUD with category filtering
- **`/api/v1/skill-sessions`** - Session management with instructor validation and availability
- **`/api/v1/bookings`** - Complete booking lifecycle with status management
- **`/api/v1/reviews`** - Review system with booking validation

### Key API Features
- Comprehensive validation for skill sessions domain
- Nested resource details (instructor info, skills, reviews)
- Status-based filtering (active sessions, confirmed bookings)
- Automatic calculations (pricing, availability, ratings)

## Services & Persistence Architecture

### Facade Layer (`app/services/facade.py`)
- **Class**: `SkillSessionsFacade` (renamed from HBnBFacade)
- **Global Instance**: `facade` - used by all API endpoints
- **Business Logic**: Handles all cross-model validations and workflows
- **Key Methods**:
  - Session management with instructor validation
  - Booking creation with availability checks
  - Review creation with completion validation

### Repository Pattern (`app/persistence/`)
- **`skill_repository.py`** (formerly amenity_repository.py) - Skill categorization
- **`skill_session_repository.py`** (formerly place_repository.py) - Session queries
- **`booking_repository.py`** (new) - Booking status and user filtering
- **`user_repository.py`** - Enhanced for instructor queries
- **`review_repository.py`** - Updated for session/instructor reviews

### Model Associations (`app/models/associations.py`)
- **`session_skill`** table - Many-to-many between SkillSession and Skill

## Database Configuration

- Development database: MySQL via PyMySQL
- Connection string in `config.py`: `mysql+pymysql://hbnb:hbnb_password@localhost/hbnb_db`
- SQLAlchemy models with automatic table creation on app startup
- Flask-Migrate ready for database migrations (commented out in `__init__.py`)

## Key Architecture Patterns

### Facade Pattern
- `SkillSessionsFacade` provides unified interface to business logic
- Manages complex interactions between models and persistence layers
- All API endpoints use facade methods rather than direct model access

### Repository Pattern
- SQLAlchemy-based repositories for database operations
- Specialized query methods for domain-specific needs
- Abstracts data access from business logic

### Layered Architecture
```
API Endpoints (app/api/v1/)
    ↓
Facade Layer (app/services/facade.py)
    ↓
Models (app/models/)
    ↓
Repositories (app/persistence/)
    ↓
Database
```

## Business Logic & Validation

### Booking Workflow
1. **Create**: Validate session availability and instructor status
2. **Confirm**: Change status from pending to confirmed
3. **Complete**: Mark as completed (enables review creation)
4. **Cancel**: Only allowed for pending/confirmed bookings before session date

### Review System
- Only users with completed bookings can create reviews
- Reviews target both the session and the instructor
- Prevents duplicate reviews and self-reviews
- Automatic rating calculations for instructors and sessions

### Session Management
- Instructors can only create sessions if `is_instructor = True`
- Availability tracking based on `max_participants` vs confirmed bookings
- Session deactivation without deletion for history preservation

## Current State

**✅ FULLY UPDATED**: The entire backend has been transformed for the skill sessions domain:
- ✅ Models completely updated with new fields and relationships
- ✅ Services layer (facade) rewritten for skill sessions business logic
- ✅ Persistence layer updated with new repositories and queries
- ✅ API endpoints completely rewritten for new domain
- ✅ Application configuration updated with new namespaces

**❌ PENDING**: Frontend components still need updating to match the new API structure and domain.