@echo off
echo ========================================
echo   Microservices Setup Instructions
echo ========================================
echo.
echo STEP 1: Create MySQL Databases
echo --------------------------------
echo Please run the following SQL commands in MySQL:
echo.
echo CREATE DATABASE IF NOT EXISTS db_micro_customer CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
echo CREATE DATABASE IF NOT EXISTS db_micro_book CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
echo CREATE DATABASE IF NOT EXISTS db_micro_cart CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
echo.
echo You can:
echo - Open MySQL Workbench and run create_databases.sql
echo - Or use command prompt: mysql -u root -p ^< create_databases.sql
echo.
pause
echo.
echo STEP 2: Installing Dependencies
echo ================================
echo.

echo Installing packages for Customer Service...
cd customer_service
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error installing Customer Service dependencies
    pause
    exit /b 1
)
cd ..
echo.

echo Installing packages for Book Service...
cd book_service
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error installing Book Service dependencies
    pause
    exit /b 1
)
cd ..
echo.

echo Installing packages for Cart Service...
cd cart_service
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error installing Cart Service dependencies
    pause
    exit /b 1
)
cd ..
echo.

echo ========================================
echo    Running Migrations
echo ========================================
echo.

echo Migrating Customer Service...
cd customer_service
python manage.py makemigrations
python manage.py migrate
cd ..
echo.

echo Migrating Book Service...
cd book_service
python manage.py makemigrations
python manage.py migrate
cd ..
echo.

echo Migrating Cart Service...
cd cart_service
python manage.py makemigrations
python manage.py migrate
cd ..
echo.

echo ========================================
echo    Seeding Book Data
echo ========================================
echo.

cd book_service
python manage.py seed_books
cd ..
echo.

echo ========================================
echo    Setup Complete!
echo ========================================
echo.
echo All services are ready!
echo Run 'run_all.bat' to start all services.
echo.
pause
