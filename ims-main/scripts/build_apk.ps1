<#
DL-IMS APK Build Script
用途：一键打包 Android APK，含代码提交完整性检查
用法：cd ims-main && powershell -ExecutionPolicy Bypass -File scripts/build_apk.ps1
#>

$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Resolve-Path "$scriptDir/.."
$frontendDir = "$projectRoot/frontend"
$backendDir = "$projectRoot/backend"
$androidDir = "$frontendDir/android"
$distApkDir = "$projectRoot/dist-apk"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "DL-IMS APK Build Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# ============================================================
# Step 1: Check git status
# ============================================================
Write-Host "[1/9] 检查工作区状态..." -ForegroundColor Yellow -NoNewline
Push-Location $projectRoot
try {
    $status = git status --porcelain 2>$null
    if ($status) {
        Write-Host " FAIL" -ForegroundColor Red
        Write-Host ""
        Write-Host "错误：工作区不干净，有以下未提交文件：" -ForegroundColor Red
        Write-Host $status
        Write-Host ""
        Write-Host "请先提交所有改动后再打包。" -ForegroundColor Red
        exit 1
    }
    Write-Host " OK" -ForegroundColor Green
} finally {
    Pop-Location
}

# ============================================================
# Step 2: Check critical files in Git
# ============================================================
Write-Host "[2/9] 检查关键文件..." -ForegroundColor Yellow -NoNewline
$criticalFiles = @(
    "ims-main/frontend/src/utils/apiConfig.js",
    "ims-main/frontend/src/components/ServerSettingsDialog.vue",
    "ims-main/frontend/src/utils/request.js",
    "ims-main/frontend/src/views/Login.vue",
    "ims-main/backend/app/api/settings.py",
    "ims-main/frontend/android/app/src/main/AndroidManifest.xml"
)

$missing = @()
Push-Location $projectRoot
try {
    foreach ($f in $criticalFiles) {
        git ls-files --error-unmatch $f 2>$null
        if ($LASTEXITCODE -ne 0) {
            $missing += $f
        }
    }
} finally {
    Pop-Location
}

if ($missing.Count -gt 0) {
    Write-Host " WARN" -ForegroundColor Yellow
    Write-Host "警告：以下关键文件未在 Git 中跟踪：" -ForegroundColor Yellow
    foreach ($m in $missing) {
        Write-Host "  - $m" -ForegroundColor Yellow
    }
} else {
    Write-Host " OK (6/6)" -ForegroundColor Green
}

# ============================================================
# Step 3: Clean dist/
# ============================================================
Write-Host "[3/9] 清理 dist/..." -ForegroundColor Yellow -NoNewline
$distPath = "$frontendDir/dist"
if (Test-Path $distPath) {
    Remove-Item -Recurse -Force $distPath
}
Write-Host " OK" -ForegroundColor Green

# ============================================================
# Step 4: Run backend tests
# ============================================================
Write-Host "[4/9] 后端测试..." -ForegroundColor Yellow
Push-Location $backendDir
try {
    uv run pytest tests/ -v --tb=short
    if ($LASTEXITCODE -ne 0) {
        Write-Host ""
        Write-Host "错误：后端测试不通过，终止打包。" -ForegroundColor Red
        exit 1
    }
} finally {
    Pop-Location
}
Write-Host " OK 通过" -ForegroundColor Green

# ============================================================
# Step 5: Run frontend tests
# ============================================================
Write-Host "[5/9] 前端测试..." -ForegroundColor Yellow
Push-Location $frontendDir
try {
    npm run test
    if ($LASTEXITCODE -ne 0) {
        Write-Host ""
        Write-Host "错误：前端测试不通过，终止打包。" -ForegroundColor Red
        exit 1
    }
} finally {
    Pop-Location
}
Write-Host " OK 通过" -ForegroundColor Green

# ============================================================
# Step 6: Build frontend
# ============================================================
Write-Host "[6/9] 前端构建 (npm run build)..." -ForegroundColor Yellow
Push-Location $frontendDir
try {
    npm run build
    if ($LASTEXITCODE -ne 0) {
        Write-Host ""
        Write-Host "错误：前端构建失败，终止打包。" -ForegroundColor Red
        exit 1
    }
} finally {
    Pop-Location
}

if (-not (Test-Path "$frontendDir/dist/index.html")) {
    Write-Host "错误：dist/index.html 不存在，构建可能未成功。" -ForegroundColor Red
    exit 1
}
Write-Host " OK dist/ 已生成" -ForegroundColor Green

# ============================================================
# Step 7: Capacitor sync
# ============================================================
Write-Host "[7/9] Capacitor 同步 (npx cap sync)..." -ForegroundColor Yellow
Push-Location $frontendDir
try {
    npx cap sync android
    if ($LASTEXITCODE -ne 0) {
        Write-Host ""
        Write-Host "错误：Capacitor 同步失败，终止打包。" -ForegroundColor Red
        exit 1
    }
} finally {
    Pop-Location
}
Write-Host " OK" -ForegroundColor Green

# ============================================================
# Step 8: Gradle build
# ============================================================
Write-Host "[8/9] Gradle 打包 (assembleDebug)..." -ForegroundColor Yellow
if (-not (Test-Path "$androidDir/gradlew")) {
    Write-Host "错误：找不到 gradlew，请确认 Android 项目已正确初始化。" -ForegroundColor Red
    exit 1
}
Push-Location $androidDir
try {
    .\gradlew assembleDebug
    if ($LASTEXITCODE -ne 0) {
        Write-Host ""
        Write-Host "错误：Gradle 打包失败。" -ForegroundColor Red
        exit 1
    }
} finally {
    Pop-Location
}
Write-Host " OK" -ForegroundColor Green

# ============================================================
# Step 9: Copy APK to dist-apk/
# ============================================================
Write-Host "[9/9] 复制 APK..." -ForegroundColor Yellow -NoNewline

$apkSource = "$androidDir/app/build/outputs/apk/debug/app-debug.apk"
if (-not (Test-Path $apkSource)) {
    Write-Host " FAIL" -ForegroundColor Red
    Write-Host "错误：找不到 APK 文件：$apkSource" -ForegroundColor Red
    exit 1
}

New-Item -ItemType Directory -Force -Path $distApkDir | Out-Null

$pkgJson = Get-Content "$frontendDir/package.json" -Raw | ConvertFrom-Json
$version = $pkgJson.version
$buildTime = Get-Date -Format "yyyyMMdd-HHmmss"
$apkName = "DL-IMS-v${version}-${buildTime}.apk"
$apkDest = "$distApkDir/$apkName"

Copy-Item $apkSource $apkDest -Force

$staticDir = "$projectRoot/backend/static/download"
New-Item -ItemType Directory -Force -Path $staticDir | Out-Null
Copy-Item $apkSource "$staticDir/ims-latest.apk" -Force

Write-Host " OK" -ForegroundColor Green

# ============================================================
# Output summary
# ============================================================
$latestCommit = git -C $projectRoot log -1 --format="%h %s"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "打包完成！" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  版  本：$version"
Write-Host "  构建时间：$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
Write-Host "  最新提交：$latestCommit"
Write-Host "  APK 大小：$([math]::Round((Get-Item $apkDest).Length / 1MB, 2)) MB"
Write-Host "  APK 路径：$apkDest"
Write-Host "  下载路径：$staticDir/ims-latest.apk"
Write-Host "========================================" -ForegroundColor Cyan