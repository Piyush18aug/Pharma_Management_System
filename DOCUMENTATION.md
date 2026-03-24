# Pharmacy Inventory with Expiry Alerts - Project Documentation

## 1. Setup Guide

### Prerequisites
- Python 3.10+
- MySQL Server
- Git (Optional)

### Installation Steps

1.  **Configure Database**
    - **Note**: The project is currently configured to use **SQLite** by default for immediate testing. To use **MySQL**:
    - Uncomment the MySQL database configuration in `pharmacy_system/settings.py` (Lines 78-86).
    - Update `USER` and `PASSWORD` with your MySQL credentials.
    - Create the database: `CREATE DATABASE pharmacy_db CHARACTER SET utf8mb4;`
        ```python
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': 'pharmacy_db',
                'USER': 'root',      # Your Default User
                'PASSWORD': '',      # Your Password
                'HOST': 'localhost',
                'PORT': '3306',
            }
        }
        ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run Migrations**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

4.  **Create Admin User**
    ```bash
    python manage.py createsuperuser
    ```

5.  **Run Server**
    ```bash
    python manage.py runserver
    ```
    Access the site at `http://127.0.0.1:8000/`.

6.  **Scheduled Task (Expiry Check)**
    - To run manually:
        ```bash
        python manage.py check_expiry
        ```
    - For production, add this to a cron job/Task Scheduler.

## 2. System Architecture

The project follows the **Model-View-Controller (MVC)** architectural pattern (MVT in Django terminology).

-   **Frontend**: HTML5, Vanilla CSS3 (Custom Styles), JavaScript.
-   **Backend**: Django 5.x (Python).
-   **Database**: MySQL.

### Modules (Apps)
1.  **Accounts**: Handles User Authentication (Login/Logout) and Role Management (Admin vs Staff).
2.  **Inventory**: Core logic. Manages `Medicine`, `Category`, `ExpiryAlert`, and the Dashboard.
3.  **Reports**: Generates CSV reports for inventory analysis.

## 3. Database Schema

The system uses a Relational Database (MySQL) with the following key tables:

-   **Users (`accounts_user`)**: Stores authentication details and `role` (Admin/Staff). Extends `AbstractUser`.
-   **Categories (`inventory_category`)**: Master table for medicine categories (e.g., Antibiotics, Painkillers).
-   **Medicines (`inventory_medicine`)**: Main inventory table.
    -   Fields: `Name`, `Batch Number`, `Category (FK)`, `Quantity`, `Expiry Date` (Indexed for performance).
-   **ExpiryAlerts (`inventory_expiryalert`)**: Tracks active alerts.
    -   Fields: `Medicine (FK)`, `Date Detected`, `Is Resolved`.
-   **AuditLog (`inventory_auditlog`)**: Logs important user actions (Optional/Extra).

## 4. Features Explained

### Staff Module
-   **Dashboard**: Visualize Total Stock, Expiring Soon (Yellow), and Expired (Red) items.
-   **Medicine Management**: Full CRUD (Create, Read, Update, Delete) capability.
-   **Expiry Alerts**: System automatically calculates days remaining. Items < 30 days are flagged.
-   **Reports**: Download CSV format inventory lists.

### Admin Module
-   **Stock Oversight**: Full access to all medicines.
-   **Alert Management**: Can mark alerts as resolved.
-   **User Management**: Access via Django Admin Panel (`/admin`).

## 5. Future Enhancements

-   **SMS/Email Alerts**: Integrate Twilio or SMTP to send real-time notifications.
-   **Barcode Scanning**: Use JS libraries to scan barcodes for quick lookup.
-   **Multi-branch Support**: Extend database to associate stock with specific branch IDs.
-   **Analytics Dashboard**: Charts and Graphs (Chart.js) for consumption trends.

## 6. Academic Synopsis Compatibility

This project fits the standard MCA/B.Tech mini-project requirements:
-   **Objectives**: To reduce medical waste and improve patient safety by tracking expiration.
-   **Tech Stack**: Covers standard Web Programming curriculum (Python/SQL/HTML).
-   **Advantages**: Automated checking vs Manual checking (Error prone).

---
**Developed by AI Assistant**
