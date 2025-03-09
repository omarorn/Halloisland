# Install Azure CLI using the MSI installer
$ProgressPreference = 'SilentlyContinue'
Invoke-WebRequest -Uri https://aka.ms/installazurecliwindows -OutFile .\AzureCLI.msi
Start-Process msiexec.exe -Wait -ArgumentList '/I AzureCLI.msi /quiet'
Remove-Item .\AzureCLI.msi

# Refresh environment variables without requiring restart
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User") 

Write-Host "Azure CLI installed successfully. Please restart your PowerShell session or run 'refreshenv' if you have chocolatey installed."

# Grant permissions to service principal
Write-Host "Now configuring permissions for service principal..."

# Set your variables with the actual resource group and VM name from your environment
$appId = "eb98290b-d23d-466b-86da-99a385d56c9b"
$resourceGroupName = "resgr-wise-quality-manual"
$vmName = "Ai-kit-omaromar"
$subscriptionId = "ffc22328-ef21-4a0c-8c9d-23afbe50d45f"

# Function to check if logged in
function Test-AzLogin {
    try {
        $account = az account show | ConvertFrom-Json
        Write-Host "Logged in as $($account.user.name)"
        return $true
    }
    catch {
        Write-Host "Not logged into Azure. Please run 'az login' first."
        return $false
    }
}

# Check if Azure CLI is in path and user is logged in
if (Get-Command az -ErrorAction SilentlyContinue) {
    if (Test-AzLogin) {
        # Set the subscription context
        Write-Host "Setting subscription context..."
        az account set --subscription $subscriptionId
        
        # Assign Contributor role to the service principal at VM level
        Write-Host "Assigning Contributor role to service principal for VM..."
        az role assignment create --assignee $appId --role "Contributor" --scope "/subscriptions/$subscriptionId/resourceGroups/$resourceGroupName/providers/Microsoft.Compute/virtualMachines/$vmName"
        
        # Or assign at resource group level for broader access
        # Write-Host "Assigning Contributor role to service principal for resource group..."
        # az role assignment create --assignee $appId --role "Contributor" --resource-group $resourceGroupName
        
        Write-Host "Role assignment complete. The service principal now has Contributor access."
    }
}
else {
    Write-Host "Azure CLI not found in path. Please restart your PowerShell session after installation."
}
