param([int]$Port = 5173)

$ErrorActionPreference = "Stop"

$conn = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue
if ($conn) {
    Write-Host "  ❌ 端口 $Port 已被占用" -ForegroundColor Red
    Write-Host "  进程名: $((Get-Process -Id $conn.OwningProcess).ProcessName)" -ForegroundColor Yellow
    Write-Host "  PID: $($conn.OwningProcess)" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  释放端口: taskkill /PID $($conn.OwningProcess) [/F]" -ForegroundColor Cyan
    exit 1
}
Write-Host "  ✅ 端口 $Port 可用" -ForegroundColor Green
exit 0