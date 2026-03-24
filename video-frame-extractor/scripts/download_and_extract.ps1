# Download FFmpeg using .NET WebClient (bypasses proxy issues)
$TempDir = "$env:TEMP\ffmpeg-temp"
$FfmpegExe = "$TempDir\ffmpeg.exe"
$VideoPath = "C:\Users\zsz\Downloads\jimeng-2026-02-14-1431-是张小凡，是林惊羽，场景参考 【东方神话锚点】 高动态、清晰、东方史诗感、无崩坏....mp4"
$OutputPath = "C:\Users\zsz\Downloads\jimeng-last-frame.png"

# Create temp directory
if (-not (Test-Path $TempDir)) {
    New-Item -ItemType Directory -Path $TempDir -Force | Out-Null
}

# Download FFmpeg if not exists
if (-not (Test-Path $FfmpegExe)) {
    Write-Host "Downloading FFmpeg..." -ForegroundColor Yellow
    
    # Use gyan.dev builds (reliable mirror)
    $FfmpegUrl = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
    $ZipPath = "$env:TEMP\ffmpeg-release.zip"
    
    try {
        # Use .NET WebClient (usually bypasses proxy issues)
        $webClient = New-Object System.Net.WebClient
        $webClient.Proxy = $null  # Disable proxy
        
        Write-Host "Downloading from gyan.dev..."
        $webClient.DownloadFile($FfmpegUrl, $ZipPath)
        Write-Host "Download complete!" -ForegroundColor Green
        
        # Extract
        Write-Host "Extracting..."
        Expand-Archive -Path $ZipPath -DestinationPath $TempDir -Force
        
        # Find ffmpeg.exe
        $FfmpegFound = Get-ChildItem -Path $TempDir -Recurse -Filter "ffmpeg.exe" | Select-Object -First 1
        if ($FfmpegFound) {
            Copy-Item -Path $FfmpegFound.FullName -Destination $FfmpegExe -Force
            Write-Host "FFmpeg ready: $FfmpegExe" -ForegroundColor Green
        } else {
            throw "Could not find ffmpeg.exe"
        }
        
        # Cleanup
        Remove-Item $ZipPath -Force -ErrorAction SilentlyContinue
    }
    catch {
        Write-Error "Failed: $_"
        exit 1
    }
}

# Extract last frame
Write-Host "Extracting last frame from video..." -ForegroundColor Yellow

$args = @(
    "-sseof", "-0.1",
    "-i", $VideoPath,
    "-vsync", "0",
    "-q:v", "2",
    "-frames:v", "1",
    "-y",
    $OutputPath
)

& $FfmpegExe @args 2>&1 | Out-Null

if (Test-Path $OutputPath) {
    Write-Host "✓ Success! Last frame saved to: $OutputPath" -ForegroundColor Green
} else {
    Write-Error "Failed to extract frame"
}
