$txt = Get-Content .\technologies.html
$start = ($txt | Select-String "<header" | Select-Object -First 1).LineNumber - 1
$end = ($txt | Select-String "</header>" | Select-Object -First 1).LineNumber - 1
$headerBlock = ($txt[$start..$end]) -join "`n"
$startF = ($txt | Select-String "<footer" | Select-Object -First 1).LineNumber - 1
$endF = ($txt | Select-String "</footer>" | Select-Object -Last 1).LineNumber - 1
$footerBlock = ($txt[$startF..$endF]) -join "`n"

Get-ChildItem -Recurse -Filter *.html | ForEach-Object {
    if ($_.Name -ne 'technologies.html') {
        $c = Get-Content $_.FullName -Raw
        $c = [regex]::Replace($c,'<header.*?</header>',$headerBlock,[Text.RegularExpressions.RegexOptions]::Singleline)
        $c = [regex]::Replace($c,'<footer.*?</footer>',$footerBlock,[Text.RegularExpressions.RegexOptions]::Singleline)
        Set-Content $_.FullName $c
        Write-Host "Updated headers/footers in" $_.FullName
    }
}
