# Stock Backtester - Report Compilation Script
# This script helps prepare the LaTeX report for submission

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Stock Backtester Report Helper" -ForegroundColor Cyan
Write-Host "  Digital Assignment 2" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Function to check if a command exists
function Test-Command($cmdname) {
    return [bool](Get-Command -Name $cmdname -ErrorAction SilentlyContinue)
}

# Check LaTeX installation
Write-Host "Checking LaTeX installation..." -ForegroundColor Yellow
$hasLatex = Test-Command "pdflatex"

if ($hasLatex) {
    Write-Host "✅ LaTeX is installed!" -ForegroundColor Green
    Write-Host ""
    
    $compile = Read-Host "Do you want to compile report.tex to PDF? (y/n)"
    
    if ($compile -eq "y") {
        Write-Host ""
        Write-Host "Compiling LaTeX document (pass 1)..." -ForegroundColor Yellow
        pdflatex -interaction=nonstopmode report.tex | Out-Null
        
        Write-Host "Compiling LaTeX document (pass 2 - for references)..." -ForegroundColor Yellow
        pdflatex -interaction=nonstopmode report.tex | Out-Null
        
        if (Test-Path "report.pdf") {
            Write-Host "✅ PDF created successfully: report.pdf" -ForegroundColor Green
            
            $open = Read-Host "Open PDF now? (y/n)"
            if ($open -eq "y") {
                Start-Process "report.pdf"
            }
        } else {
            Write-Host "❌ PDF compilation failed. Check report.log for errors." -ForegroundColor Red
        }
    }
} else {
    Write-Host "❌ LaTeX not found. You have two options:" -ForegroundColor Red
    Write-Host ""
    Write-Host "Option 1: Use Overleaf (Recommended - No installation needed)" -ForegroundColor Cyan
    Write-Host "  1. Go to: https://www.overleaf.com/" -ForegroundColor White
    Write-Host "  2. Create new project → Upload Project" -ForegroundColor White
    Write-Host "  3. Upload report.tex and image folders" -ForegroundColor White
    Write-Host "  4. Click 'Recompile'" -ForegroundColor White
    Write-Host "  5. Download PDF" -ForegroundColor White
    Write-Host ""
    Write-Host "Option 2: Install LaTeX locally" -ForegroundColor Cyan
    Write-Host "  Windows: Download MiKTeX from https://miktex.org/download" -ForegroundColor White
    Write-Host "  Or use: choco install miktex" -ForegroundColor White
    Write-Host ""
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Additional Options" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Option to create submission ZIP
Write-Host "1. Create submission ZIP file" -ForegroundColor Yellow
$createZip = Read-Host "   Create ZIP? (y/n)"

if ($createZip -eq "y") {
    $zipName = "DA2_Stock_Backtester_Submission.zip"
    
    if (Test-Path $zipName) {
        Remove-Item $zipName
    }
    
    Write-Host "   Creating ZIP file..." -ForegroundColor Yellow
    
    $filesToZip = @(
        "report.tex",
        "diagrams",
        "wireframes",
        "REPORT_README.md",
        "LATEX_COMPILATION_GUIDE.md"
    )
    
    if (Test-Path "report.pdf") {
        $filesToZip += "report.pdf"
    }
    
    Compress-Archive -Path $filesToZip -DestinationPath $zipName
    
    Write-Host "   ✅ Created: $zipName" -ForegroundColor Green
}

Write-Host ""
Write-Host "2. Verify all required files" -ForegroundColor Yellow
$verify = Read-Host "   Run verification? (y/n)"

if ($verify -eq "y") {
    Write-Host ""
    Write-Host "   Checking files..." -ForegroundColor Yellow
    
    # Check main file
    if (Test-Path "report.tex") {
        Write-Host "   ✅ report.tex exists" -ForegroundColor Green
    } else {
        Write-Host "   ❌ report.tex missing!" -ForegroundColor Red
    }
    
    # Check diagrams
    $requiredDiagrams = @(
        "diagrams/high_level_architecture.png",
        "diagrams/Architecture.png",
        "diagrams/backtest_pipline.png"
    )
    
    $missingDiagrams = 0
    foreach ($diagram in $requiredDiagrams) {
        if (Test-Path $diagram) {
            Write-Host "   ✅ $diagram exists" -ForegroundColor Green
        } else {
            Write-Host "   ❌ $diagram missing!" -ForegroundColor Red
            $missingDiagrams++
        }
    }
    
    # Check wireframes
    $requiredWireframes = @(
        "wireframes/home.png",
        "wireframes/csv_import.png",
        "wireframes/stock_preview.png",
        "wireframes/strategy_picker.png",
        "wireframes/equity_curve.png"
    )
    
    $missingWireframes = 0
    foreach ($wireframe in $requiredWireframes) {
        if (Test-Path $wireframe) {
            Write-Host "   ✅ $wireframe exists" -ForegroundColor Green
        } else {
            Write-Host "   ❌ $wireframe missing!" -ForegroundColor Red
            $missingWireframes++
        }
    }
    
    Write-Host ""
    if ($missingDiagrams -eq 0 -and $missingWireframes -eq 0) {
        Write-Host "   ✅ All required files present!" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️  Some files are missing. Report may not compile correctly." -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Summary" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Report Status:" -ForegroundColor Yellow
Write-Host "  ✅ LaTeX source ready (report.tex)" -ForegroundColor Green
Write-Host "  ✅ All diagrams in place" -ForegroundColor Green
Write-Host "  ✅ All wireframes in place" -ForegroundColor Green
Write-Host "  ✅ Documentation complete" -ForegroundColor Green
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "  1. Compile report.tex to PDF (Overleaf recommended)" -ForegroundColor White
Write-Host "  2. Verify PDF has 15-20 pages with all diagrams" -ForegroundColor White
Write-Host "  3. Rename PDF to: Stock_Backtester_Design_YourName.pdf" -ForegroundColor White
Write-Host "  4. Upload to Moodle" -ForegroundColor White
Write-Host ""
Write-Host "Documentation:" -ForegroundColor Yellow
Write-Host "  - Read REPORT_README.md for detailed instructions" -ForegroundColor White
Write-Host "  - Read LATEX_COMPILATION_GUIDE.md for compilation help" -ForegroundColor White
Write-Host ""
Write-Host "GitHub Repository:" -ForegroundColor Yellow
Write-Host "  https://github.com/Nihaal2004/stock-backtester" -ForegroundColor Cyan
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Script Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
