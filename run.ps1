param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]] $Args
)


# Resolve uv path from env, then from .env file, then fallback
if ($env:UV_PATH) {
    $uv = $env:UV_PATH
} else {
    $uv = $null
    $dotenvPath = Join-Path -Path (Get-Location) -ChildPath ".env"
    if (Test-Path $dotenvPath) {
        $lines = Get-Content -LiteralPath $dotenvPath -ErrorAction SilentlyContinue
        foreach ($line in $lines) {
            if ($line -match '^[#\s]*$') { continue }
            $kv = $line -split '=', 2
            if ($kv.Length -eq 2) {
                $key = $kv[0].Trim()
                if ($key -ieq 'UV_PATH') {
                    $val = $kv[1].Trim()
                    # Strip surrounding quotes if present
                    if ($val.StartsWith('"') -and $val.EndsWith('"')) {
                        $val = $val.Substring(1, $val.Length - 2)
                    }
                    $uv = $val
                    break
                }
            }
        }
    }
    if (-not $uv) {
        $uv = "C:\\Users\\sukum\\.local\\bin\\uv.exe"
    }
}
if (-not (Test-Path $uv)) {
    Write-Error "uv.exe not found at $uv. Install uv or update run.ps1."
    exit 1
}

& $uv run main.py @Args
exit $LASTEXITCODE
