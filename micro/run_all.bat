@echo off
echo ========================================
echo   Starting All Services + Frontend
echo ========================================
echo.
echo Backend Services:
echo - Customer Service: http://localhost:8001
echo - Book Service: http://localhost:8002
echo - Cart Service: http://localhost:8003
echo.
echo Frontend:
echo - Web UI: http://localhost:8000
echo.
echo Starting services in separate windows...
echo.

start "Customer Service - Port 8001" cmd /k "cd customer_service && python manage.py runserver 8001"
timeout /t 2 /nobreak >nul

start "Book Service - Port 8002" cmd /k "cd book_service && python manage.py runserver 8002"
timeout /t 2 /nobreak >nul

start "Cart Service - Port 8003" cmd /k "cd cart_service && python manage.py runserver 8003"
timeout /t 2 /nobreak >nul

start "Frontend - Port 8000" cmd /k "cd frontend && python server.py"

echo.
echo ========================================
echo   All Services Started!
echo ========================================
echo.
echo Backend APIs:
echo - Customer: http://localhost:8001/api/
echo - Book: http://localhost:8002/api/
echo - Cart: http://localhost:8003/api/
echo.
echo Frontend Web UI:
echo - Open: http://localhost:8000
echo.
echo Close individual windows to stop services.
echo.
pause
