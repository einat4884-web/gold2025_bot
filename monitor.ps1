$path   = "C:\Users\haya1843\Downloads\Gold2025_Clean_IBKR\heartbeat.txt"
$thresh = 15
if (!(Test-Path $path)) { Write-Host "no heartbeat"; exit 1 }

$mins = (New-TimeSpan -Start (Get-Item $path).LastWriteTime -End (Get-Date)).TotalMinutes

if ($mins -gt $thresh) {
  Add-Type -AssemblyName PresentationFramework
  [System.Windows.MessageBox]::Show("Gold2025 Auto Push: No run in over $thresh minutes (last $([math]::Round($mins,1))m)","Gold2025 Monitor") | Out-Null
  "ALERT $(Get-Date) $([math]::Round($mins,1)) m" | Out-File -Append "C:\Users\haya1843\Downloads\Gold2025_Clean_IBKR\monitor.log"
} else {
  "OK $(Get-Date) $([math]::Round($mins,1)) m" | Out-File -Append "C:\Users\haya1843\Downloads\Gold2025_Clean_IBKR\monitor.log"
}
