@echo off
chcp 65001 >nul
title IMS 开发环境启动

echo ============================================
echo   IMS 生产物料与产品追溯管理系统
echo   开发环境启动脚本
echo ============================================
echo.

:: 获取脚本所在目录
set "ROOT=%~dp0"
set "BACKEND=%ROOT%backend"
set "FRONTEND=%ROOT%frontend"

:: ── 1. 启动 MySQL ──────────────────────────────
echo [1/3] 启动 MySQL 数据库...
set "MYSQL_EXE=C:\Program Files\MySQL\MySQL Server 5.7\bin\mysqld.exe"
set "MYSQL_INI=C:\ProgramData\MySQL\MySQL Server 5.7\my.ini"

if exist "%MYSQL_EXE%" (
    echo   正在启动 MySQL...
    start "MySQL" /MIN "%MYSQL_EXE%" --defaults-file="%MYSQL_INI%" --console
    echo   MySQL 已在新窗口启动
) else (
    echo   [警告] 未找到 MySQL: %MYSQL_EXE%
    echo   请确保 MySQL 已安装或手动启动
)
echo.

:: ── 2. 启动后端 ────────────────────────────────
echo [2/3] 启动后端服务 (端口 8000)...
if exist "%BACKEND%" (
    cd /d "%BACKEND%"
    if not exist ".venv" (
        echo   [警告] 未找到虚拟环境 .venv，请先运行: uv sync
    ) else (
        start "IMS-Backend" cmd /k "title IMS 后端服务 && .venv\Scripts\python.exe -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"
        echo   后端已在新窗口启动 (http://localhost:8000)
        echo   API 文档: http://localhost:8000/docs
    )
) else (
    echo   [错误] 未找到后端目录: %BACKEND%
)
echo.

:: ── 3. 启动前端 ───────────────────────────────
echo [3/3] 启动前端开发服务器 (端口 5173)...
if exist "%FRONTEND%" (
    cd /d "%FRONTEND%"
    if not exist "node_modules" (
        echo   首次运行，正在安装前端依赖 (npm install)...
        call npm install
        if errorlevel 1 (
            echo   [错误] npm install 失败，请检查 Node.js 安装
            goto :end
        )
        echo   依赖安装完成
    )
    start "IMS-Frontend" cmd /k "title IMS 前端服务 && npm run dev"
    echo   前端已在新窗口启动 (http://localhost:5173)
) else (
    echo   [错误] 未找到前端目录: %FRONTEND%
)
echo.

:: ── 完成 ──────────────────────────────────────
:end
echo ============================================
echo   启动完成！
echo.
echo   前端页面: http://localhost:5173
echo   API 文档: http://localhost:8000/docs
echo   健康检查: http://localhost:8000/health
echo.
echo   登录账号: admin / admin123
echo ============================================
echo.
echo   按任意键关闭此窗口（不影响服务运行）...
pause >nul