# LaTeX Report Compilation Guide

## 📄 Report Created: `report.tex`

A comprehensive LaTeX document has been created for Digital Assignment 2 covering all requirements:

### ✅ What's Included

1. **Design Principles Applied** (Section 2)
   - Abstraction with code examples
   - Modularity with module table
   - High Cohesion examples
   - Low Coupling implementation

2. **High-Level Architecture** (Section 3)
   - Layered Architecture diagram
   - 3-layer structure explained
   - Component interactions
   - Backtest pipeline flow

3. **User Interface Design** (Section 4)
   - 5 wireframe screens with descriptions
   - UI design philosophy
   - Consistency features
   - Figma prototype link

4. **Design Decisions & Rationale** (Section 6)
   - 10 key decisions documented
   - Alternatives considered
   - Justification for each choice

5. **Design Patterns** (Section 5)
   - Strategy Pattern with code
   - Factory Pattern with code
   - Benefits and examples

6. **Additional Sections**
   - Extensibility examples
   - Testing & validation
   - Deployment instructions
   - Comprehensive appendices

### 📊 Diagrams Included

All diagrams are referenced in the LaTeX with proper paths:
- `diagrams/high_level_architecture.png` (needs rename)
- `diagrams/Architecture.png`
- `diagrams/backtest_pipline.png`
- `wireframes/home.png`
- `wireframes/csv_import.png`
- `wireframes/stock_preview.png`
- `wireframes/strategy_picker.png`
- `wireframes/equity_curve.png`

### 🔧 How to Compile

#### Option 1: Overleaf (Recommended - Easiest)

1. Go to [Overleaf](https://www.overleaf.com/)
2. Create new project → Upload Project
3. Upload `report.tex` file
4. Create folders: `diagrams/` and `wireframes/`
5. Upload all PNG images to respective folders
6. Click "Recompile"
7. Download PDF

#### Option 2: Local LaTeX Installation

**Windows:**
```powershell
# Install MiKTeX
choco install miktex

# Or download from: https://miktex.org/download

# Compile
pdflatex report.tex
pdflatex report.tex  # Run twice for references
```

**Mac:**
```bash
# Install MacTeX
brew install --cask mactex

# Compile
pdflatex report.tex
pdflatex report.tex
```

**Linux:**
```bash
# Install TeX Live
sudo apt-get install texlive-full

# Compile
pdflatex report.tex
pdflatex report.tex
```

#### Option 3: Online LaTeX Compiler

1. Visit [LaTeX Base](https://latexbase.com/)
2. Paste entire `report.tex` content
3. Upload images (requires premium for images)
4. Click "Generate PDF"

### 📝 Required Image Renames

The LaTeX uses underscores in filenames. Rename these files:

```powershell
# In diagrams folder
Rename-Item "diagrams\high level architecture.png" "high_level_architecture.png"

# In wireframes folder  
Rename-Item "wireframes\csv import.png" "csv_import.png"
Rename-Item "wireframes\stock preview.png" "stock_preview.png"
Rename-Item "wireframes\strategy picker.png" "strategy_picker.png"
Rename-Item "wireframes\equity curve.png" "equity_curve.png"
```

### 🎯 Quick Fix for Spaces in Filenames

If you don't want to rename files, update these lines in `report.tex`:

```latex
% Change from:
\includegraphics[width=0.6\textwidth]{diagrams/high_level_architecture.png}

% To:
\includegraphics[width=0.6\textwidth]{diagrams/high level architecture.png}
```

### 📋 Document Statistics

- **Total Pages:** ~15-20 pages (with diagrams)
- **Sections:** 8 main sections + 3 appendices
- **Code Examples:** 10+ listings
- **Diagrams:** 8 figures
- **Tables:** 3 comparison tables
- **Requirements:** All Digital Assignment 2 requirements covered

### ✨ Features

- Professional formatting with fancyhdr
- Color-coded section headers
- Syntax-highlighted code blocks
- Hyperlinked table of contents
- Clickable URLs
- Proper figure captions
- Academic references

### 🚀 Submission Ready

Once compiled, the PDF will be:
- ✅ 6-10 pages minimum requirement (actually 15-20 pages)
- ✅ All required sections included
- ✅ Professional formatting
- ✅ Embedded diagrams
- ✅ Code examples
- ✅ Design decisions explained
- ✅ GitHub links included

### 📤 For Moodle Submission

1. Compile `report.tex` to PDF using any method above
2. Name the PDF: `Stock_Backtester_Design_Nihaal2004.pdf`
3. Upload to Moodle
4. Add comment: "Complete source code and documentation at: https://github.com/Nihaal2004/stock-backtester"

### 🐛 Troubleshooting

**Issue: Images not showing**
- Check image paths match folder structure
- Ensure PNG files are in correct folders
- Try using relative paths without `./`

**Issue: Compilation errors**
- Run pdflatex twice (first pass may show errors)
- Check all packages are installed
- Use Overleaf for hassle-free compilation

**Issue: Table of contents empty**
- Run pdflatex twice - first pass generates ToC, second pass includes it

### 📞 Need Help?

- **LaTeX Tutorial:** https://www.overleaf.com/learn
- **Overleaf Help:** https://www.overleaf.com/learn/how-to/
- **MiKTeX Issues:** https://miktex.org/howto/

---

**Status:** ✅ LaTeX report complete and ready for compilation!
