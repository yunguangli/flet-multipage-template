# Flet Multi-Page Routing Template

A clean, well-documented skeleton for building multi-page applications with Flet.

## Features

1. **Simple Routing System**: Easy navigation between pages using routes
2. **Session Management**: Share data between pages using `page.session`
3. **Singleton Pattern**: Shared object instance accessible from all pages
4. **Navigation History**: Track user navigation path
5. **Page-Specific Data**: Store data specific to each page
6. **Comprehensive Comments**: Detailed explanations for beginners

## Project Structure




## How It Works

### 1. **Routing System**
- `main.py` handles all route changes
- Each route (`/`, `/page1`, `/page2`, `/page3`) maps to a different view
- `page.go("/route")` triggers navigation

### 2. **Session Data Management**
- Use `page.session.set(key, value)` to store data
- Use `page.session.get(key)` to retrieve data
- Session data persists across page navigations

### 3. **Singleton Object**
- One instance shared across all pages
- Can store application-wide data (DB connections, AI models, config)
- Accessed via `page.session.get("shared_singleton")`

### 4. **Navigation Flow**
- Home → Page 1 → Page 2 → Page 3
- Each page has forward/backward navigation
- Navigation history tracked in session

## Key Concepts for Beginners

### **Page Session (`page.session`)**
- Dictionary-like storage attached to user's session
- Perfect for storing temporary data
- Cleared when browser closes (unless using server-side storage)

### **Views (`ft.View`)**
- Each page is a `View` object
- Contains all UI controls for that page
- Has a route (e.g., `/page1`)

### **Navigation**
- `page.go("/route")`: Navigate to new page
- `page.views.pop()`: Remove current view (back navigation)
- App bar back buttons for intuitive navigation

## How to Use This Template

1. **Install Flet** (if not already installed):
   ```bash
   pip install flet

## Extending the Template
Adding a New Page:
Create newpage.py with a function that returns ft.View

Import it in main.py

Add route handler in route_change function

Add navigation buttons in existing pages

Modifying Singleton:
Edit shared_singleton.py to add:

Database connections

API clients

Configuration settings

User authentication data

Storing User Data:
Use page.session for:

User preferences

Form data

Shopping cart items

Current workflow state

Best Practices Demonstrated
Separation of Concerns: Each page in its own file

State Management: Session for temporary, Singleton for shared

Clean Navigation: Consistent forward/back buttons

Error Prevention: Check for existing session data

Beginner-Friendly: Detailed comments and simple patterns

Common Use Cases
This template can be adapted for:

E-commerce: Product pages, cart, checkout

Dashboards: Multiple data views

Forms: Multi-step form wizards

Educational Apps: Lessons, quizzes, progress tracking

Admin Panels: Different management sections