<#
.SYNOPSIS
    Script to completely reset a Git repository
.DESCRIPTION
    This script preserves your current files but eliminates all Git history
    by removing the .git directory and creating a fresh repository.
#>

$repoPath = Split-Path -Parent $PSScriptRoot
$backupPath = "$repoPath-backup-$(Get-Date -Format 'yyyyMMdd-HHmmss')"
$gitRemoteUrl = $null

Write-Host "⚠️ WARNING: This will COMPLETELY RESET your Git repository ⚠️" -ForegroundColor Red
Write-Host "All commit history will be permanently deleted." -ForegroundColor Yellow
Write-Host "Your files will be preserved." -ForegroundColor Yellow
Write-Host ""

$confirmation = Read-Host "Do you want to proceed? (yes/no)"
if ($confirmation -ne "yes") {
    Write-Host "Operation cancelled by user"
    exit
}

# Get the current remote URL before we delete .git
Set-Location $repoPath
if (Test-Path "$repoPath\.git") {
    $gitRemoteUrl = git remote get-url origin 2>$null
    if ($LASTEXITCODE -ne 0) {
        $gitRemoteUrl = Read-Host "Enter your GitHub repository URL (e.g., https://github.com/username/repo.git)"
    }
} else {
    $gitRemoteUrl = Read-Host "Enter your GitHub repository URL (e.g., https://github.com/username/repo.git)"
}

# Create a backup
Write-Host "Creating backup at $backupPath..." -ForegroundColor Cyan
Copy-Item -Path "$repoPath\*" -Destination $backupPath -Recurse -Force -Exclude @(".git", ".git-mirror")

# Remove old Git repository
if (Test-Path "$repoPath\.git") {
    Write-Host "Removing old Git repository..." -ForegroundColor Cyan
    Remove-Item -Path "$repoPath\.git" -Recurse -Force
}

# Initialize new repository
Write-Host "Initializing new Git repository..." -ForegroundColor Cyan
Set-Location $repoPath
git init

# Make sure .gitignore is in place before first commit
if (-not (Test-Path "$repoPath\.gitignore")) {
    Write-Host "Creating .gitignore file..." -ForegroundColor Cyan
    @"
# Environment variables and secrets
.env
*/.env
**/.env

# Local development configurations
.env.local
.env.development
.env.test
.env.production

# Python virtual environment
venv/
env/
ENV/
.venv/

# Node.js
node_modules/
npm-debug.log
yarn-debug.log
yarn-error.log

# Build outputs
dist/
build/
*.pyc
__pycache__/

# Logs
*.log

# OS files
.DS_Store
Thumbs.db

# IDE files
.idea/
.vscode/
*.swp
*.swo
"@ | Out-File -FilePath "$repoPath\.gitignore" -Encoding utf8
}

# Add all files and make initial commit
Write-Host "Adding files to new repository..." -ForegroundColor Cyan
git add .
git commit -m "Initial commit with clean history"

# Set up remote
if ($gitRemoteUrl) {
    Write-Host "Setting up remote origin: $gitRemoteUrl" -ForegroundColor Cyan
    git remote add origin $gitRemoteUrl
}

Write-Host ""
Write-Host "✅ Git repository has been completely reset!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Push to GitHub: git push -f origin main" -ForegroundColor White
Write-Host "2. If this doesn't work, you might need to create a new repository on GitHub" -ForegroundColor White
Write-Host "   and set the remote: git remote set-url origin https://github.com/username/new-repo.git" -ForegroundColor White
Write-Host ""
Write-Host "Your files have been backed up to: $backupPath" -ForegroundColor Yellow
