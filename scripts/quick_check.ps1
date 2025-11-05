<#
.SYNOPSIS
    Quick CI Check - Fast pre-commit validation

.DESCRIPTION
    This is a lightweight PowerShell script that runs the most important checks quickly.
    Use this for rapid feedback before committing.

.EXAMPLE
    .\quick_check.ps1
    Run quick validation checks

.NOTES
    For full CI validation, use: .\check_and_fix.ps1
#>

# Color output functions
function Write-CheckResult {
    param(
        [string]$Name,
        [bool]$Success
    )
    
    $status = if ($Success) { 
        Write-Host "✓" -ForegroundColor Green -NoNewline
    } else { 
        Write-Host "✗" -ForegroundColor Red -NoNewline
    }
    Write-Host ""
}

function Invoke-QuickCheck {
    param(
        [string]$Name,
        [string]$Command,
        [string[]]$Arguments,
        [string]$FixCommand = $null,
        [string[]]$FixArguments = $null
    )
    
    Write-Host "Checking $Name... " -NoNewline
    
    $result = & $Command $Arguments 2>&1
    $success = $LASTEXITCODE -eq 0
    
    if ($success) {
        Write-Host "✓" -ForegroundColor Green
        return $true
    }
    
    Write-Host "✗" -ForegroundColor Red
    
    if ($FixCommand) {
        Write-Host "  Fixing... " -ForegroundColor Yellow -NoNewline
        $fixResult = & $FixCommand $FixArguments 2>&1
        $fixSuccess = $LASTEXITCODE -eq 0
        
        if ($fixSuccess) {
            Write-Host "✓ Fixed" -ForegroundColor Green
            return $true
        }
        Write-Host "✗ Failed to fix" -ForegroundColor Red
    }
    
    return $false
}

# Main execution
Write-Host "Quick CI Check - Fast validation" -ForegroundColor Cyan
Write-Host ""

$results = @()

# Black formatting (auto-fix)
$results += Invoke-QuickCheck `
    -Name "Code formatting (black)" `
    -Command "black" `
    -Arguments @("--check", "--quiet", "fubon_mcp", "tests", "--exclude", "_version.py") `
    -FixCommand "black" `
    -FixArguments @("--quiet", "fubon_mcp", "tests", "--exclude", "_version.py")

# Import sorting (auto-fix)
$results += Invoke-QuickCheck `
    -Name "Import sorting (isort)" `
    -Command "isort" `
    -Arguments @("--check-only", "fubon_mcp", "tests", "--skip", "_version.py") `
    -FixCommand "isort" `
    -FixArguments @("fubon_mcp", "tests", "--skip", "_version.py")

# Flake8 critical errors (no auto-fix)
$results += Invoke-QuickCheck `
    -Name "Critical code errors (flake8)" `
    -Command "flake8" `
    -Arguments @("fubon_mcp", "tests", "--select=E9,F63,F7,F82", "--quiet")

# Quick test run (most important tests only)
Write-Host "Running quick tests... " -NoNewline

$testResult = & pytest -q --tb=no `
    tests/test_config.py `
    tests/test_models.py `
    tests/test_package.py 2>&1

$testSuccess = $LASTEXITCODE -eq 0

if ($testSuccess) {
    Write-Host "✓" -ForegroundColor Green
} else {
    Write-Host "✗" -ForegroundColor Red
    Write-Host "  Run 'pytest -v' for details" -ForegroundColor Yellow
}

$results += $testSuccess

# Summary
Write-Host ""

if ($results -notcontains $false) {
    Write-Host "✓ All quick checks passed!" -ForegroundColor Green
    Write-Host "Note: Run '.\check_and_fix.ps1' for full CI validation" -ForegroundColor Yellow
    exit 0
} else {
    Write-Host "✗ Some checks failed" -ForegroundColor Red
    Write-Host "Run '.\check_and_fix.ps1 -Fix -Verbose' for details" -ForegroundColor Yellow
    exit 1
}
