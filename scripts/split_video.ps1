# Define directories
$OutputDirectory = ".\output"

# Take the input file from the first argument passed to the script
$InputFile = $args[0]

# Log input file
Write-Host "Input File: $InputFile"

# Validate the input file
if (-Not (Test-Path -Path $InputFile -PathType Leaf)) {
    Write-Host "The specified input file does not exist."
    exit 1
}

# Extract the filename without extension
$FileName = [System.IO.Path]::GetFileNameWithoutExtension($InputFile)

# Log original filename
Write-Host "Original File Name: $FileName"

# Sanitize filename by removing whitespaces and special characters
$SanitizedFileName = $FileName -replace '\s+', '' -replace '[^a-zA-Z0-9]', ''

# Log sanitized filename
Write-Host "Sanitized File Name: $SanitizedFileName"

# Generate a timestamp
$Timestamp = Get-Date -Format "yyyyMMddHHmmss"

# Log timestamp
Write-Host "Timestamp: $Timestamp"

# Create the subfolder in the output directory with a timestamp and sanitized filename
$SubFolderName = "${SanitizedFileName}_${Timestamp}"

# Log subfolder name
Write-Host "SubFolder Name: $SubFolderName"

$SubFolder = Join-Path -Path $OutputDirectory -ChildPath $SubFolderName
New-Item -Path $SubFolder -ItemType Directory -Force

# Run ffmpeg to split the video into frames
$FfmpegCommand = "ffmpeg -i `"$InputFile`" -vf fps=1 `"$SubFolder\frame_%04d.png`""
Write-Host "Running: $FfmpegCommand"
Invoke-Expression $FfmpegCommand
