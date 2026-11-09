@echo off
setlocal
set "SAFELY_CLEAN_SCRIPT=%~f0"
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -Command "$s=[IO.File]::ReadAllText($env:SAFELY_CLEAN_SCRIPT); & ([scriptblock]::Create(($s -split '(?m)^:POWERSHELL_PAYLOAD\r?\n',2)[1]))"
if errorlevel 2 exit /b 0
if errorlevel 1 exit /b 1
(goto) 2>nul & powershell.exe -NoLogo -NoProfile -Command "try { Remove-Item -LiteralPath '%~f0' -Force -ErrorAction Stop; Write-Host 'Cleanup completed.'; exit 0 } catch { Write-Host ('ERROR removing script: ' + $_.Exception.Message); Write-Host 'Press Enter to exit.'; [void][Console]::ReadLine(); exit 1 }"
:POWERSHELL_PAYLOAD
$ErrorActionPreference = 'Stop'
$removed = [Collections.Generic.List[string]]::new()
$failed = [Collections.Generic.List[string]]::new()
$hasGit = $false
$removingGit = $false
function Report {
    Write-Host 'Removed items:'
    $removed | ForEach-Object { Write-Host "  $_" }
    Write-Host 'Failed items:'
    $failed | ForEach-Object { Write-Host "  $_" }
}
function Remove-Checked([string]$Path, [bool]$Immediate = $false) {
    if (-not (Test-Path -LiteralPath $Path)) { return }
    try {
        Remove-Item -LiteralPath $Path -Recurse -Force -ErrorAction Stop
        if (Test-Path -LiteralPath $Path) { throw 'Item still exists.' }
        $removed.Add($Path)
    } catch {
        $failed.Add("${Path}: $($_.Exception.Message)")
        if ($Immediate -or -not $hasGit -or $removingGit) { throw }
    }
}
function Git-Output([string[]]$GitArgs) {
    $result = @(& git -C $root @GitArgs 2>&1)
    if ($LASTEXITCODE -ne 0) { throw "Git check failed: $($result -join ' ')" }
    return $result
}
try {
    $root = (Get-Item -LiteralPath '.').FullName
    $self = [IO.Path]::GetFullPath($env:SAFELY_CLEAN_SCRIPT)
    if ([IO.Path]::GetDirectoryName($self) -ine $root) { throw 'Run this script from its own directory.' }
    if ($root.TrimEnd('\') -match '(?i)example$') { throw 'Directories ending in example are protected.' }
    $tag = Join-Path $root 'SafetyProtect.Tag'
    $token = 'WINROOT-SAFE-CLEAN-7F4E89C2-36A1-4D85-B902-61CF8340EA77'
    if (-not (Test-Path -LiteralPath $tag -PathType Leaf)) { throw 'SafetyProtect.Tag is missing.' }
    if (-not ([IO.File]::ReadAllText($tag).Contains($token))) { throw 'SafetyProtect.Tag does not contain the required token.' }
    if (@(Get-ChildItem -LiteralPath $root -Force | Where-Object { $_.Name.EndsWith('.p', [StringComparison]::OrdinalIgnoreCase) }).Count) { throw 'The working directory contains an item ending in .p.' }
    # Inspect every entry without following junctions or symbolic links.
    $entries = [Collections.Generic.List[IO.FileSystemInfo]]::new()
    $pending = [Collections.Generic.Stack[string]]::new()
    $pending.Push($root)
    if ((Get-Item -LiteralPath $root -Force).Attributes -band [IO.FileAttributes]::ReparsePoint) { throw 'The working directory is a reparse point.' }
    while ($pending.Count) {
        foreach ($entry in Get-ChildItem -LiteralPath $pending.Pop() -Force) {
            if ($entry.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw "Reparse points are not allowed: $($entry.FullName)" }
            $entries.Add($entry)
            if ($entry.PSIsContainer) { $pending.Push($entry.FullName) }
        }
    }
    $gitPath = Join-Path $root '.git'
    $hasGit = Test-Path -LiteralPath $gitPath
    if ($hasGit) {
        if (-not (Get-Command git -CommandType Application -ErrorAction SilentlyContinue)) { throw 'Git is required when .git exists.' }
        $top = @(Git-Output @('rev-parse', '--show-toplevel'))
        if ([IO.Path]::GetFullPath($top[0]) -ine $root) { throw 'Git repository root does not match the working directory.' }
        if (@(Git-Output @('stash', 'list')).Count) { throw 'Git stash is not empty. Resolve it before cleaning.' }
        if (@(Git-Output @('status', '--porcelain=v1', '--untracked-files=all', '--ignore-submodules=none')).Count) { throw 'Git has staged, modified, or untracked files. Commit or resolve them first.' }
    }
    # Select only files containing the complete three-line keeper block.
    $ignoreFiles = @($entries | Where-Object { -not $_.PSIsContainer -and $_.Name -ieq '.gitignore' } | Where-Object {
        [IO.File]::ReadAllText($_.FullName) -match '(?m)^# Git Keeper\r?\n\*\r?\n!\.gitignore\r?$'
    })
    $keepers = @($entries | Where-Object { -not $_.PSIsContainer -and $_.Name -ieq '.gitkeeper' })
    Write-Host "Working directory: $root"
    Write-Host 'This permanently removes the safety tag, .github, .ci, .vscode, keeper files, .git, and this script.'
    if ((Read-Host 'Type YES to start') -cne 'YES') { Write-Host 'Cancelled.'; exit 2 }
    Remove-Checked $tag $true
    foreach ($name in @('.github', '.ci', '.vscode')) { Remove-Checked (Join-Path $root $name) }
    foreach ($entry in $ignoreFiles) { Remove-Checked $entry.FullName }
    foreach ($entry in $keepers) { Remove-Checked $entry.FullName }
    if ($failed.Count) { throw 'Cleanup failed. Git metadata has been preserved. Roll back the removed items using Git before retrying.' }
    $removingGit = $true
    Remove-Checked $gitPath $true
    # The batch epilogue removes this script after leaving the batch context.
    Report
    Write-Host 'Cleanup finished; removing this script next.'
    exit 0
} catch {
    Write-Host "ERROR: $($_.Exception.Message)"
    Report
    if ($hasGit -and -not $removingGit -and $removed.Count) { Write-Host 'Git metadata was preserved. Review and roll back removed items using Git.' }
    Write-Host 'Press Enter to exit.'
    [void][Console]::ReadLine()
    exit 1
}