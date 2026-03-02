# How to Use the LaTeX Document in Overleaf

## Quick Start (2 minutes)

### Option 1: Upload to Overleaf (Easiest)

1. **Go to Overleaf**: https://www.overleaf.com/
2. **Create New Project** → Click "Upload Project"
3. **Upload the file**: `executive_summary.tex`
4. **Compile**: Click the green "Recompile" button
5. **Download PDF**: Click "Download PDF" button

---

## Option 2: Copy-Paste (If upload doesn't work)

1. **Go to Overleaf**: https://www.overleaf.com/
2. **New Project** → "Blank Project"
3. **Delete** the default content in main.tex
4. **Copy** all content from `executive_summary.tex`
5. **Paste** into the Overleaf editor
6. **Compile**: Click "Recompile"

---

## Adding Images (Optional - If you want diagrams in PDF)

If you want to include the architecture diagrams in your PDF:

### Step 1: Upload Images to Overleaf
1. In Overleaf, click the **folder icon** (top left)
2. Click **"Upload"** button
3. Upload these PNG files from `/docs/design/`:
   - `high level architecture.png`
   - `backtest pipline.png`
   - `home.png`
   - `csv import.png`
   - `strategy picker.png`

### Step 2: Modify LaTeX to Include Images

Replace the ASCII art diagrams with actual images. Find this section in the LaTeX file:

```latex
\begin{figure}[H]
\centering
\begin{minipage}{0.8\textwidth}
\begin{verbatim}
┌─────────────────────────────────────────────────┐
│         PRESENTATION LAYER                      │
...
\end{verbatim}
\end{minipage}
\caption{Three-Layer Architecture}
\end{figure}
```

Replace it with:

```latex
\begin{figure}[H]
\centering
\includegraphics[width=0.8\textwidth]{high level architecture.png}
\caption{Three-Layer Architecture}
\end{figure}
```

---

## Customization Options

### Change Student Name
Find line:
```latex
{\Large\itshape Nihaal2004\par}
```
Change `Nihaal2004` to your actual name/ID.

### Change Date
Find line:
```latex
{\large March 2026\par}
```
Change to current date.

### Adjust Page Margins
Find line:
```latex
\usepackage[margin=1in]{geometry}
```
Change `1in` to `0.8in` for more content per page.

### Change Colors
Find the color definitions section:
```latex
\definecolor{codegreen}{rgb}{0,0.6,0}
```
Modify RGB values to change colors.

---

## Troubleshooting

### Problem: "Package not found" error
**Solution**: Overleaf should have all packages. If not, remove the problematic package line.

### Problem: Compilation takes too long
**Solution**: This is normal for first compile. Wait 30-60 seconds.

### Problem: Images not showing
**Solution**: 
1. Make sure images are uploaded to Overleaf
2. Use the exact filename (case-sensitive)
3. Check file format is PNG

### Problem: Code blocks look weird
**Solution**: The `listings` package handles code. Make sure it's not removed.

### Problem: Links not clickable in PDF
**Solution**: Links should be clickable by default with `hyperref` package.

---

## What the PDF Will Look Like

### Page Count: ~12-14 pages
Includes:
- Title page (1 page)
- Table of contents (1 page)
- Design Principles (2 pages)
- Architecture (2 pages)
- UI Design (2 pages)
- Design Decisions (2 pages)
- Design Patterns (1 page)
- Extensibility (1 page)
- Summary (1 page)
- Conclusion (1 page)

### Features:
- ✅ Professional title page
- ✅ Table of contents with page numbers
- ✅ Colored section headers
- ✅ Code syntax highlighting
- ✅ Tables for comparisons
- ✅ Clickable hyperlinks
- ✅ Page numbers in footer
- ✅ Header with document title

---

## Quick Quality Check

Before submitting, verify:
- [ ] Title page shows your name correctly
- [ ] Table of contents is complete
- [ ] All sections are present
- [ ] Code blocks are readable
- [ ] GitHub links are clickable
- [ ] Page numbers appear
- [ ] PDF is 10-14 pages

---

## Exporting from Overleaf

1. **Click "Download PDF"** button (top right)
2. **Rename file**: `Stock_Backtester_Design_Nihaal2004.pdf`
3. **Check file size**: Should be 200-500 KB (without images) or 1-2 MB (with images)
4. **Open and verify**: Make sure everything looks good

---

## Alternative: Compile Locally

If you prefer to compile on your computer:

### Requirements:
- LaTeX distribution (TeX Live, MiKTeX, or MacTeX)
- Text editor (VS Code with LaTeX Workshop extension)

### Commands:
```bash
pdflatex executive_summary.tex
pdflatex executive_summary.tex  # Run twice for TOC
```

---

## Need Help?

### Overleaf Documentation:
- https://www.overleaf.com/learn

### LaTeX Help:
- https://www.latex-project.org/help/

### Common LaTeX Commands:
- `\textbf{text}` = bold text
- `\textit{text}` = italic text
- `\section{Title}` = new section
- `\newpage` = start new page

---

## Final Tips

1. **Compile Early**: Compile as soon as you upload to catch any errors
2. **Save Often**: Overleaf auto-saves, but manually save important changes
3. **Check Links**: Test all hyperlinks in the final PDF
4. **Print Preview**: Check how it looks if printed
5. **File Size**: Keep under 10 MB for easy uploading to Moodle

---

**The LaTeX file is ready to go! Just upload to Overleaf and compile. Good luck! 🚀**
