# UI Design Documentation

## Overview
This document describes the user interface design for the Stock Strategy Backtester Lite application.

---

## UI Design Principles

### 1. Consistency
- **Colors**: Uniform color scheme (blue for primary, green for positive, red for negative)
- **Typography**: Consistent font sizes and weights
- **Layout**: Similar patterns across all screens
- **Spacing**: Uniform padding and margins

### 2. Clarity
- **Labels**: Clear, descriptive text
- **Instructions**: Step-by-step guidance (1️⃣, 2️⃣, 3️⃣)
- **Help Text**: Tooltips explaining each parameter
- **Feedback**: Immediate visual response to actions

### 3. User-Friendliness
- **Progressive Disclosure**: Show information when needed
- **Error Prevention**: Validate inputs before processing
- **Error Recovery**: Clear error messages with solutions
- **Forgiving**: Allow users to modify inputs easily

### 4. Accessibility
- **High Contrast**: Easy to read text
- **Large Targets**: Buttons and inputs easy to click
- **Logical Flow**: Natural progression through steps
- **Descriptive Labels**: Clear for screen readers

---

## Screen Designs

### Screen 1: Home / Upload

**Purpose**: Welcome users and initiate data upload

**Elements**:
- Application title and tagline
- Educational disclaimer
- File upload widget
- Instructions on required CSV format

**User Flow**:
1. User reads welcome message
2. User clicks "Browse files" 
3. User selects CSV file
4. System validates and loads data

**Wireframe**: See `wireframes/home.png` and `wireframes/csv import.png`

---

### Screen 2: Data Preview

**Purpose**: Show loaded data and allow date range selection

**Elements**:
- Success message with row count
- Data preview table (last 10 rows)
- Optional date range filter
- Current date range display

**User Flow**:
1. System displays data preview automatically
2. User reviews data
3. User optionally adjusts date range
4. Proceeds to strategy selection

**Wireframe**: See `wireframes/stock preview.png`

---

### Screen 3: Strategy Configuration

**Purpose**: Allow users to select and configure trading strategy

**Elements**:
- Strategy selection dropdown
- Initial capital input
- Transaction cost input
- Strategy-specific parameters (context-sensitive)
- "Run Backtest" button

**User Flow**:
1. User selects strategy from dropdown
2. Parameters update based on strategy
3. User configures strategy parameters
4. User sets capital and costs
5. User clicks "Run Backtest"

**Design Decisions**:
- **Form-based**: Prevents accidental reruns
- **Tooltips**: Help text on all parameters
- **Reasonable Defaults**: Pre-filled with sensible values
- **Validation**: Happens on submit

**Wireframe**: See `wireframes/strategy picker.png`

---

### Screen 4: Results - Performance Metrics

**Purpose**: Display key performance indicators at a glance

**Elements**:
- 5 metric cards in a row:
  - Total Return (%)
  - CAGR (%)
  - Max Drawdown (%)
  - Win Rate (%)
  - Number of Trades

**Design Decisions**:
- **Large Numbers**: Easy to read at a glance
- **Color Coding**: Green for positive, red for negative
- **Percentage Format**: Standard financial formatting
- **Tooltips**: Explain what each metric means

**Visual Hierarchy**:
- Metrics are equal prominence (same size cards)
- Most important metrics first (Total Return, CAGR)
- Risk metrics in middle (Max Drawdown)
- Activity metrics last (Win Rate, # Trades)

---

### Screen 5: Results - Equity Curve

**Purpose**: Visualize portfolio value over time

**Elements**:
- Line chart showing equity over time
- X-axis: Date
- Y-axis: Portfolio value ($)
- Title: "Equity Curve"
- Grid lines for easier reading

**Design Decisions**:
- **Line Chart**: Best for time series data
- **Blue Line**: Professional, easy to see
- **Grid**: Helps read values
- **Rotated Labels**: Dates readable
- **Large Size**: Easy to analyze trends

**What Users Can See**:
- Overall growth/decline trend
- Volatility (how smooth/bumpy)
- Drawdown periods (dips in the line)
- Recovery patterns

**Wireframe**: See `wireframes/equity curve.png`

---

### Screen 6: Results - Trade Log

**Purpose**: Show detailed information about each trade

**Elements**:
- Scrollable table with columns:
  - Entry Date
  - Exit Date
  - Entry Price
  - Exit Price
  - P/L %
- Color-coded P/L (green positive, red negative)
- Sortable columns
- Full width layout

**Design Decisions**:
- **Table Format**: Best for structured data
- **Color Coding**: Quick visual scanning
- **Sortable**: Users can analyze trades
- **Scrollable**: Handles many trades gracefully
- **Precision**: 2 decimal places for readability

**What Users Can See**:
- Individual trade performance
- Trade timing patterns
- Win/loss distribution
- Holding periods

---

## UI Workflow

### Complete User Journey

```
1. [Home] → User uploads CSV
           ↓
2. [Data Preview] → System validates & displays data
           ↓
3. [Date Filter] → User optionally filters date range
           ↓
4. [Strategy Config] → User selects strategy & parameters
           ↓
5. [Submit] → User clicks "Run Backtest"
           ↓
6. [Processing] → System calculates results
           ↓
7. [Results] → Display metrics, chart, and trades
           ↓
8. [Iterate] → User modifies parameters and reruns
```

---

## Layout Structure

### Sidebar (Left)
- **Width**: ~30% of screen
- **Purpose**: Configuration and controls
- **Sections**:
  1. Data Upload
  2. Date Range Filter
  3. Strategy Configuration
- **Sticky**: Stays visible when scrolling

### Main Area (Right)
- **Width**: ~70% of screen
- **Purpose**: Data preview and results
- **Sections**:
  1. Data Preview Table
  2. Performance Metrics
  3. Equity Curve Chart
  4. Trade Log Table
- **Scrollable**: Can scroll through results

---

## Responsive Design

### Desktop (Primary Target)
- Full layout with sidebar
- Charts large and readable
- Tables show all columns

### Tablet
- Sidebar collapses to top
- Charts slightly smaller
- Tables remain full-featured

### Mobile (Basic Support)
- Vertical layout
- Simplified charts
- Scrollable tables
- Touch-friendly controls

---

## Color Scheme

### Primary Colors
- **Blue** (#1f77b4): Primary actions, charts
- **Green** (#2ecc71): Positive values, success
- **Red** (#e74c3c): Negative values, errors
- **Gray** (#7f8c8d): Secondary text, borders

### Background Colors
- **White** (#ffffff): Main background
- **Light Gray** (#f8f9fa): Sidebar background
- **Off-White** (#fafafa): Card backgrounds

### Text Colors
- **Dark Gray** (#2c3e50): Primary text
- **Medium Gray** (#7f8c8d): Secondary text
- **Light Gray** (#bdc3c7): Disabled text

---

## Typography

### Font Family
- Primary: System default (Streamlit's default font)
- Monospace: For numbers and data

### Font Sizes
- **Title**: 32px (H1)
- **Section Header**: 24px (H2)
- **Subsection**: 18px (H3)
- **Body Text**: 14px
- **Captions**: 12px
- **Metrics**: 24px (large numbers)

### Font Weights
- **Bold**: Headers, labels, important numbers
- **Regular**: Body text, descriptions
- **Light**: Captions, help text

---

## Interactive Elements

### Buttons
- **Primary Button** ("Run Backtest")
  - Blue background
  - White text
  - Full width of sidebar
  - Hover effect: Slightly darker blue

### Input Fields
- **Text/Number Inputs**
  - White background
  - Gray border
  - Focus: Blue border
  - Help text below in gray

### File Uploader
- **Drag-and-drop area**
  - Dashed border
  - Large clickable area
  - "Browse files" button
  - Accepted formats shown

### Dropdown/Select
- **Strategy selector**
  - White background
  - Arrow indicator
  - Full width
  - Options appear below

---

## Feedback Mechanisms

### Success Messages
- **Green background**
- **Checkmark icon** ✅
- Examples:
  - "✅ Loaded 250 rows"
  - "✅ Backtest completed successfully"

### Error Messages
- **Red background**
- **X icon** ❌
- **Actionable text**
- Examples:
  - "❌ Missing required columns: Date, Close"
  - "❌ Fast SMA must be less than Slow SMA"

### Warning Messages
- **Yellow/orange background**
- **Warning icon** ⚠️
- Examples:
  - "⚠️ No trades generated with these parameters"

### Info Messages
- **Blue background**
- **Info icon** ℹ️
- Examples:
  - "📤 Upload a CSV to continue"
  - "⚙️ Configure parameters and click Run"

---

## Accessibility Features

### Keyboard Navigation
- Tab through all input fields
- Enter to submit form
- Escape to dismiss dialogs

### Screen Readers
- All images have alt text
- Form labels properly associated
- ARIA labels on custom components

### Color Blindness
- Don't rely solely on color
- Icons supplement colors
- Patterns in charts (if needed)
- High contrast ratios

---

## Mobile Considerations

### Touch Targets
- Minimum 44x44px clickable area
- Adequate spacing between buttons
- Swipe gestures for tables

### Simplified Navigation
- Collapsible sections
- Bottom navigation if needed
- Minimal scrolling required

### Performance
- Lazy load large tables
- Optimize chart rendering
- Compress images

---

## Figma Designs

### Figma Link
https://www.figma.com/design/9AgSClvrB4onGZlJ19ogbf/nihaal

### Screens Included
1. Home page
2. CSV Import
3. Stock Preview
4. Strategy Picker
5. Equity Curve
6. (Need 6th screen - could add Settings or Help screen)

### Design Iterations
- Version 1: Initial wireframes
- Version 2: Added colors and branding
- Version 3: Refined based on implementation
- Current: Fully interactive prototype

---

## UI Improvements Made

### From Original to Refined

**Before**:
- Plain text labels
- No visual hierarchy
- Minimal feedback
- Basic styling

**After**:
- Emoji icons for sections (1️⃣, 2️⃣, 3️⃣)
- Clear visual hierarchy
- Rich feedback (success, error, warning)
- Professional styling
- Help tooltips
- Color-coded metrics
- Responsive layout

---

## User Testing Feedback

### Key Insights
1. **Users want clear steps** → Added numbered sections
2. **Parameters confusing** → Added help text to all inputs
3. **Results overwhelming** → Organized into clear sections
4. **Want to iterate quickly** → Used form to prevent reruns
5. **Hard to scan table** → Added color coding to P/L

### Improvements Implemented
- ✅ Step-by-step workflow
- ✅ Contextual help text
- ✅ Organized results layout
- ✅ Form-based inputs
- ✅ Color-coded trade log

---

## Future UI Enhancements

### Potential Improvements
1. **Strategy Comparison**: Side-by-side results
2. **Interactive Charts**: Zoom, pan, hover details
3. **Export Results**: Download CSV or PDF report
4. **Save Configurations**: Preset parameter combinations
5. **Dark Mode**: Alternative color scheme
6. **Advanced Filters**: Filter trades by various criteria
7. **Help Tour**: Guided walkthrough for new users

---

## Conclusion

The UI design prioritizes:
- **Ease of use**: Intuitive workflow
- **Clarity**: Clear labels and feedback
- **Professionalism**: Clean, modern appearance
- **Education**: Help text and guidance
- **Efficiency**: Fast iteration on parameters

The design balances simplicity for beginners with enough detail for meaningful analysis.

---

**Document End**
