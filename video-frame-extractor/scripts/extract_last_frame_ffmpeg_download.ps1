# Download and use FFmpeg to extract last frame
$videoPath = "C:\Users\zsz\Downloads\jimeng-2026-02-14-1431-是张小凡，是林惊羽，场景参考 【东方神话锚点】 高动态、清晰、东方史诗感、无崩坏....mp4"
$outputPath = "C:\Users\zsz\Downloads\jimeng-last-frame.png"
$ffmpegDir = "$env:TEMP\ffmpeg-temp"
$ffmpegExe = "$ffmpegDir\ffmpeg.exe"

# Create temp directory
if (-not (Test-Path $ffmpegDir)) {
    New-Item -ItemType Directory -Path $ffmpegDir -Force | Out-Null
}

# Download FFmpeg if not exists
if (-not (Test-Path $ffmpegExe)) {
    Write-Host "Downloading FFmpeg..." -ForegroundColor Yellow
    $ffmpegUrl = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
    $zipPath = "$env:TEMP\ffmpeg.zip"
    
    try {
        Invoke-WebRequest -Uri $ffmpegUrl -OutFile $zipPath -UseBasicParsing
        Write-Host "Extracting FFmpeg..." -ForegroundColor Yellow
        Expand-Archive -Path $zipPath -DestinationPath $env:TEMP -Force
        
        # Find and copy ffmpeg.exe
        $extractedFfmpeg = Get-ChildItem -Path $env:TEMP -Recurse -Filter "ffmpeg.exe" | Select-Object -First 1
        if ($extractedFfmpeg) {
            Copy-Item -Path $extractedFfmpeg.FullName -Destination $ffmpegExe -Force
            Write-Host "FFmpeg ready!" -ForegroundColor Green
        }
    }
    catch {
        Write-Error "Failed to download FFmpeg: $_"
        exit 1
    }
}

# Extract last frame
Write-Host "Extracting last frame..." -ForegroundColor Yellow
$args = @(
    "-sseof", "-0.1",
    "-i", $videoPath,
    "-vsync", "0",
    "-q:v", "2",
    "-frames:v", "1",
    "-y",
    $outputPath
)

& $ffmpegExe @args

if (Test-Path $outputPath) {
    Write-Host "Success! Last frame saved to: $outputPath" -ForegroundColor Green
} else {
    Write-Error "Failed to extract frame"
}
