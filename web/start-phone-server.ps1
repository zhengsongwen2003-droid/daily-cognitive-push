$ErrorActionPreference = "Stop"

$port = 8000
$webRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$addresses = Get-NetIPAddress -AddressFamily IPv4 |
  Where-Object {
    $_.IPAddress -notlike "127.*" -and
    $_.IPAddress -notlike "169.254.*" -and
    $_.IPAddress -notlike "198.18.*" -and
    $_.InterfaceAlias -notlike "*Loopback*"
  }

$ip = ($addresses |
  Where-Object { $_.InterfaceAlias -like "*WLAN*" } |
  Select-Object -First 1 -ExpandProperty IPAddress)

if (-not $ip) {
  $ip = ($addresses | Select-Object -First 1 -ExpandProperty IPAddress)
}

Set-Location -LiteralPath $webRoot

Write-Host ""
Write-Host "Daily cognitive card server is running."
Write-Host "Computer URL: http://127.0.0.1:$port/"
if ($ip) {
  Write-Host "Phone URL: http://$ip`:$port/"
  Write-Host "Make sure your phone and computer are on the same Wi-Fi."
}
Write-Host "Keep this window open. Closing it stops phone access."
Write-Host ""

python -m http.server $port --bind 0.0.0.0
