# FinLume

The prefix "Fin" relates to finance, while "Lume" suggests illumination or clarity,
implying that your app brings light to financial management.

Finance - Bill Tracker App

This will be an App that users can track theirs personal bills, subscriptions etc.

Structure:

- FinLume/
  -- app/
  --- main.py
  --- models.py
  --- schemas.py
  --- crud.py
  --- database.py
  --- routers/
  ---- **init**.py
  ---- users.py
  ---- bills.py
  ---- subscriptions.py
  -- tests/
  -- requirements.txt
  -- README.md

Possible Features to implement:

- User Registration and Authentication
  Allow users to sign up, log in, and log out.
  Secure passwords with hashing and use JWT for session management.

- Track Bills and Subscriptions
  Users can create, read, update, and delete bills and subscriptions.
  Implement categories (e.g., utilities, entertainment) for better organization.

- Notifications
  Send reminders for upcoming bills or subscription renewals via email or SMS.

- Analytics Dashboard
  Provide users with an overview of their spending habits using basic data visualization (e.g., bar charts for monthly expenditure).

- Budgeting Tool
  Allow users to set a monthly budget and track their progress.

- Search and Filter
  Enable users to search and filter their entries based on date, category, or amount.
