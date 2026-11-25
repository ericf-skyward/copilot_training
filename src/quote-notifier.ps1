#requires -Version 5.1
[CmdletBinding()]
param(
    [ValidateSet('Notify', 'Install', 'Uninstall', 'Preview')]
    [string]$Action = 'Notify'
)

$ErrorActionPreference = 'Stop'
$taskName = 'InspirationalQuoteNotifier'
$quotes = @(
    'A small step today can make tomorrow feel possible.'
    'Progress grows from practice, not perfection.'
    'Give yourself room to learn something new today.'
    'You can begin again with the next small choice.'
    'Pause, breathe, and take one useful step forward.'
    'Your effort matters, even before the results are visible.'
    'Make time for the things that help you grow.'
    'Let curiosity turn a challenge into a new beginning.'
)

if ($Action -eq 'Preview') {
    $quotes | Get-Random
    return
}

if ($env:OS -ne 'Windows_NT') {
    throw 'Windows notifications and Task Scheduler require Windows. Use -Action Preview to preview a quote.'
}

switch ($Action) {
    'Install' {
        $user = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name
        $powershell = Join-Path $env:SystemRoot 'System32\WindowsPowerShell\v1.0\powershell.exe'
        $taskAction = New-ScheduledTaskAction -Execute $powershell -Argument (
            '-NoProfile -NonInteractive -WindowStyle Hidden -STA -ExecutionPolicy RemoteSigned -File "{0}"' -f $PSCommandPath
        )
        $triggers = @(8, 12, 16 | ForEach-Object {
            New-ScheduledTaskTrigger -Daily -At ([datetime]::Today.AddHours($_))
        })
        $principal = New-ScheduledTaskPrincipal -UserId $user -LogonType Interactive -RunLevel Limited
        $settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries `
            -MultipleInstances IgnoreNew -ExecutionTimeLimit (New-TimeSpan -Minutes 1)
        Register-ScheduledTask -TaskName $taskName -Action $taskAction -Trigger $triggers `
            -Principal $principal -Settings $settings -Description (
                'Show an inspirational quote at 08:00, 12:00, and 16:00 local time while signed in.'
            ) -Force | Out-Null
        Write-Output "Installed $taskName for $user at 08:00, 12:00, and 16:00 local time."
    }
    'Uninstall' {
        $task = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
        if ($task) {
            $task | Unregister-ScheduledTask -Confirm:$false
        }
        Write-Output "Removed $taskName (if installed)."
    }
    'Notify' {
        # Also suppress notifications if a task is manually started outside daytime.
        $hour = (Get-Date).Hour
        if ($hour -lt 8 -or $hour -ge 20) {
            return
        }

        Add-Type -AssemblyName System.Windows.Forms
        Add-Type -AssemblyName System.Drawing
        $icon = New-Object System.Windows.Forms.NotifyIcon
        try {
            $icon.Icon = [System.Drawing.SystemIcons]::Information
            $icon.Text = 'Inspirational quote'
            $icon.BalloonTipTitle = 'A little inspiration'
            $icon.BalloonTipText = $quotes | Get-Random
            $icon.Visible = $true
            $icon.ShowBalloonTip(15000)
            # Keep the notification icon and its message loop alive while the tip is shown.
            $until = [datetime]::UtcNow.AddSeconds(15)
            while ([datetime]::UtcNow -lt $until) {
                [System.Windows.Forms.Application]::DoEvents()
                Start-Sleep -Milliseconds 100
            }
        }
        finally {
            $icon.Visible = $false
            $icon.Dispose()
        }
    }
}
