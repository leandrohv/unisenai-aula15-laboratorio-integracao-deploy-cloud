$ErrorActionPreference = "Stop"
Set-Location (Split-Path -Path $PSScriptRoot -Parent)
docker compose -f compose.yaml -f compose.lab.yaml config --quiet
if ($LASTEXITCODE -ne 0) { throw "Compose invalido" }
docker compose -f compose.yaml -f compose.lab.yaml ps
if ($LASTEXITCODE -ne 0) { throw "Falha ao consultar servicos" }
$port = 8081
if (Test-Path .env) {
  $line = Get-Content .env | Where-Object { $_ -match '^APP_PORT=' } | Select-Object -First 1
  if ($line) { $port = [int](($line -split '=', 2)[1]) }
}
foreach ($route in @('/api/live', '/api/ready', '/api/info', '/api/tasks')) {
  Write-Host "Verificando $route"
  Invoke-RestMethod -Uri "http://127.0.0.1:$port$route" | ConvertTo-Json -Depth 5
}
Write-Host 'Validacao concluida. Registrar evidencias.'
