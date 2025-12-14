# Udemy Design System - Complete Documentation

This design system recreates Udemy's exact visual identity for use in your practice test generator.

---

## 🎨 Color Palette

### Primary Colors

```css
--udemy-purple: #A435F0          /* Udemy's signature purple */
--udemy-purple-dark: #8710D8     /* Hover/active states */
--udemy-purple-light: #C0A0F0    /* Lighter accents */
--udemy-purple-lightest: #F3EFFD /* Very light backgrounds */
```

**Usage:**
- Primary actions (CTAs, links, buttons)
- Brand elements
- Interactive highlights

### Grayscale Palette

```css
--udemy-gray-900: #1C1D1F  /* Primary text, dark UI elements */
--udemy-gray-800: #2D2F31  /* Secondary headings */
--udemy-gray-700: #3E4143  /* Tertiary text */
--udemy-gray-600: #6A6F73  /* Body text, captions */
--udemy-gray-500: #9DA3A7  /* Placeholder text */
--udemy-gray-400: #D1D7DC  /* Borders, dividers */
--udemy-gray-300: #E4E8EB  /* Subtle borders */
--udemy-gray-200: #F2F3F5  /* Disabled states */
--udemy-gray-100: #F7F9FA  /* Page background */
--udemy-white: #FFFFFF     /* Cards, surfaces */
```

**Usage:**
- Text hierarchy: 900 for headings, 600 for body
- Borders: 400 for standard, 300 for subtle
- Backgrounds: 100 for pages, white for cards

### Semantic Colors

```css
/* Success */
--udemy-success: #2D864E
--udemy-success-light: #ECF5F0

/* Warning */
--udemy-warning: #B4690E
--udemy-warning-light: #FCF8F1

/* Error */
--udemy-error: #C91C00
--udemy-error-light: #FCF0EF

/* Info */
--udemy-info: #1C6FDB
--udemy-info-light: #EBF5FF
```

**Usage:**
- Alerts and notifications
- Form validation states
- Status indicators

---

## 🔤 Typography

### Font Stack

```css
font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
```

**Note:** Udemy uses "Graphik" (custom font). **Inter** is the closest free alternative.

### Import Inter Font

Add to your HTML `<head>`:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
```

### Type Scale

| Element | Size | Weight | Line Height | Usage |
|---------|------|--------|-------------|-------|
| **H1** | 48px (3rem) | 700 | 1.2 | Page titles |
| **H2** | 36px (2.25rem) | 700 | 1.2 | Section headings |
| **H3** | 30px (1.875rem) | 700 | 1.375 | Subsection headings |
| **H4** | 24px (1.5rem) | 700 | 1.375 | Card titles |
| **H5** | 20px (1.25rem) | 600 | 1.375 | Small headings |
| **H6** | 18px (1.125rem) | 600 | 1.5 | Tiny headings |
| **Body** | 16px (1rem) | 400 | 1.5 | Primary content |
| **Body Small** | 14px (0.875rem) | 400 | 1.5 | Secondary content |
| **Caption** | 14px (0.875rem) | 400 | 1.5 | Captions, metadata |
| **Overline** | 12px (0.75rem) | 700 | 1.5 | Labels, tags |
| **Button** | 16px (1rem) | 700 | - | All button text |

### Font Weights

```css
--udemy-weight-regular: 400    /* Body text */
--udemy-weight-medium: 500     /* Emphasis */
--udemy-weight-semibold: 600   /* Subheadings */
--udemy-weight-bold: 700       /* Headings, buttons */
```

---

## 📏 Spacing Scale

Udemy uses a consistent 4px base unit:

```css
--udemy-space-1: 4px
--udemy-space-2: 8px    /* Tight spacing */
--udemy-space-3: 12px   /* Small gaps */
--udemy-space-4: 16px   /* Standard spacing */
--udemy-space-5: 20px
--udemy-space-6: 24px   /* Medium spacing */
--udemy-space-8: 32px   /* Large spacing */
--udemy-space-10: 40px
--udemy-space-12: 48px  /* Extra large */
--udemy-space-16: 64px  /* Section spacing */
--udemy-space-20: 80px  /* Hero spacing */
```

**Guidelines:**
- **4px (1)**: Tight element spacing
- **8px (2)**: Label-to-input, icon gaps
- **12px (3)**: Small vertical rhythm
- **16px (4)**: Default padding, margins
- **24px (6)**: Card padding
- **32px+ (8+)**: Section spacing

---

## 🔲 Border Radius

```css
--udemy-radius-sm: 4px   /* Buttons, inputs, badges */
--udemy-radius-md: 6px   /* Cards */
--udemy-radius-lg: 8px   /* Large cards, modals */
--udemy-radius-full: 9999px /* Pills, avatars */
```

---

## 🌑 Shadows

```css
--udemy-shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05)
/* Subtle depth for small elements */

--udemy-shadow-base: 0 2px 4px rgba(0, 0, 0, 0.08), 0 4px 12px rgba(0, 0, 0, 0.08)
/* Standard cards */

--udemy-shadow-md: 0 4px 8px rgba(0, 0, 0, 0.12), 0 2px 4px rgba(0, 0, 0, 0.08)
/* Elevated cards, dropdowns */

--udemy-shadow-lg: 0 8px 16px rgba(0, 0, 0, 0.16), 0 4px 8px rgba(0, 0, 0, 0.08)
/* Modals, popovers */

--udemy-shadow-hover: 0 4px 16px rgba(0, 0, 0, 0.16)
/* Card hover state */
```

---

## 🧩 Component Guidelines

### Buttons

#### Variants

**1. Primary Button**
```html
<button class="udemy-btn udemy-btn-primary udemy-btn-md">
  Enroll Now
</button>
```

- **Background:** #A435F0 (purple)
- **Text:** White
- **Hover:** #8710D8 (darker purple)
- **Usage:** Main CTAs, primary actions

**2. Secondary Button**
```html
<button class="udemy-btn udemy-btn-secondary udemy-btn-md">
  Learn More
</button>
```

- **Background:** White
- **Text:** #1C1D1F (dark gray)
- **Border:** 1px solid #1C1D1F
- **Hover:** Inverts (dark background, white text)
- **Usage:** Secondary actions

**3. Outline Button**
```html
<button class="udemy-btn udemy-btn-outline udemy-btn-md">
  Preview
</button>
```

- **Background:** Transparent
- **Border:** 1px solid #1C1D1F
- **Hover:** Filled dark
- **Usage:** Tertiary actions

**4. Ghost Button**
```html
<button class="udemy-btn udemy-btn-ghost udemy-btn-md">
  Cancel
</button>
```

- **Background:** Transparent
- **Hover:** Light gray background (#F2F3F5)
- **Usage:** Subtle actions, navs

**5. Link Button**
```html
<button class="udemy-btn udemy-btn-link">
  View Details
</button>
```

- **Style:** Underlined purple text
- **Usage:** Inline links, low-priority actions

#### Sizes

```html
<button class="udemy-btn udemy-btn-primary udemy-btn-sm">Small</button>
<button class="udemy-btn udemy-btn-primary udemy-btn-md">Medium</button>
<button class="udemy-btn udemy-btn-primary udemy-btn-lg">Large</button>
```

| Size | Padding | Min Height |
|------|---------|------------|
| Small | 8px 12px | 32px |
| Medium | 12px 16px | 40px |
| Large | 16px 24px | 48px |

#### States

- **Disabled:** 60% opacity, no pointer events
- **Focus:** Purple outline ring (3px)
- **Loading:** Show spinner, disable interaction

---

### Cards

#### Basic Card
```html
<div class="udemy-card">
  <h4 class="udemy-h4">Course Title</h4>
  <p class="udemy-body-sm">Course description goes here.</p>
</div>
```

- **Background:** White
- **Border:** 1px solid #D1D7DC
- **Padding:** 24px
- **Border Radius:** 4px
- **Hover:** Lift with shadow

#### Simple Card (Less padding)
```html
<div class="udemy-card-simple">
  <!-- Content -->
</div>
```

- **Padding:** 16px
- **Usage:** Compact information

#### Elevated Card
```html
<div class="udemy-card-elevated">
  <!-- Content -->
</div>
```

- **No border**
- **Box Shadow:** Base shadow
- **Hover:** Increased shadow (md)
- **Usage:** Featured content, course cards

---

### Form Inputs

#### Text Input
```html
<div>
  <label class="udemy-label" for="email">Email Address</label>
  <input
    type="email"
    id="email"
    class="udemy-input"
    placeholder="Enter your email"
  />
  <span class="udemy-helper-text">We'll never share your email.</span>
</div>
```

**Specs:**
- **Border:** 1px solid #D1D7DC
- **Border Radius:** 4px
- **Padding:** 12px 16px
- **Font Size:** 16px
- **Hover:** Border changes to #6A6F73
- **Focus:** Purple border (#A435F0) + 2px purple ring

#### Error State
```html
<div>
  <label class="udemy-label" for="password">Password</label>
  <input
    type="password"
    id="password"
    class="udemy-input udemy-input-error"
    placeholder="Enter password"
  />
  <span class="udemy-error-text">Password must be at least 8 characters</span>
</div>
```

- **Border:** #C91C00 (red)
- **Focus Ring:** Red
- **Error Text:** Red, 14px

#### Textarea
```html
<textarea class="udemy-input" rows="4" placeholder="Description"></textarea>
```

Same styles as input

#### Select Dropdown
```html
<select class="udemy-input">
  <option>Beginner</option>
  <option>Intermediate</option>
  <option>Advanced</option>
</select>
```

---

### Badges / Tags

```html
<span class="udemy-badge udemy-badge-purple">Bestseller</span>
<span class="udemy-badge udemy-badge-success">New</span>
<span class="udemy-badge udemy-badge-warning">Limited</span>
<span class="udemy-badge udemy-badge-error">Sold Out</span>
<span class="udemy-badge udemy-badge-gray">Coming Soon</span>
```

**Specs:**
- **Font Size:** 12px
- **Font Weight:** Bold
- **Padding:** 4px 8px
- **Border Radius:** 4px
- **Text Transform:** Uppercase
- **Letter Spacing:** 0.02em

---

### Alerts

```html
<!-- Info Alert -->
<div class="udemy-alert udemy-alert-info">
  <strong>Info:</strong> Your course has been updated successfully.
</div>

<!-- Success Alert -->
<div class="udemy-alert udemy-alert-success">
  <strong>Success:</strong> Payment processed!
</div>

<!-- Warning Alert -->
<div class="udemy-alert udemy-alert-warning">
  <strong>Warning:</strong> Your trial ends in 3 days.
</div>

<!-- Error Alert -->
<div class="udemy-alert udemy-alert-error">
  <strong>Error:</strong> Failed to upload file.
</div>
```

**Specs:**
- **Padding:** 16px
- **Border:** 1px solid (semantic color)
- **Background:** Light variant of semantic color
- **Border Radius:** 4px
- **Font Size:** 14px

---

### Navigation Bar

```html
<nav class="udemy-nav">
  <div class="udemy-container" style="display: flex; justify-content: space-between; align-items: center;">
    <div style="font-size: 1.5rem; font-weight: 700; color: #A435F0;">
      Your Logo
    </div>
    <div style="display: flex; gap: 16px;">
      <a href="#" class="udemy-nav-link">Courses</a>
      <a href="#" class="udemy-nav-link udemy-nav-link-active">My Learning</a>
      <a href="#" class="udemy-nav-link">Teach</a>
    </div>
  </div>
</nav>
```

**Specs:**
- **Background:** White
- **Border Bottom:** 1px solid #D1D7DC
- **Padding:** 16px 0
- **Link Color:** #1C1D1F
- **Link Hover:** #A435F0
- **Active Link:** Purple + bold

---

## 📱 Responsive Breakpoints

Udemy uses these breakpoints:

```css
/* Mobile */
@media (max-width: 767px) { }

/* Tablet */
@media (min-width: 768px) and (max-width: 1023px) { }

/* Desktop */
@media (min-width: 1024px) { }

/* Large Desktop */
@media (min-width: 1340px) { }
```

**Container Max Width:** 1340px

---

## 🎯 Component States

### Hover States
- **Buttons:** Darken primary color
- **Cards:** Elevate with shadow
- **Links:** Change to purple
- **Inputs:** Darken border

### Focus States
- **Buttons:** 3px outline ring
- **Inputs:** 2px colored ring
- **All interactive:** Visible focus indicator

### Active States
- **Buttons:** Slightly darker than hover
- **Links:** Purple + bold
- **Tabs:** Underline + purple

### Disabled States
- **Opacity:** 60%
- **Cursor:** not-allowed
- **No hover effects**

---

## 📦 Layout Patterns

### Udemy's Typical Patterns

**1. Hero Section**
```
┌─────────────────────────────────┐
│                                 │
│    [Large Bold Heading]         │
│    [Subtitle text]              │
│    [CTA Button]                 │
│                                 │
└─────────────────────────────────┘
```
- **Background:** White or light gray
- **Padding:** 64px vertical
- **Max Width:** 1340px centered

**2. Course Card Grid**
```
┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐
│ Card │ │ Card │ │ Card │ │ Card │
└──────┘ └──────┘ └──────┘ └──────┘
```
- **Gap:** 16px
- **Responsive:** 1/2/3/4 columns

**3. Sidebar + Content**
```
┌─────┬──────────────────┐
│Side │  Main Content    │
│bar  │                  │
│     │                  │
└─────┴──────────────────┘
```
- **Sidebar:** 280px fixed
- **Gap:** 24px

---

## ✅ Do's and Don'ts

### ✅ Do
- Use plenty of white space
- Keep borders subtle (#D1D7DC)
- Use purple (#A435F0) sparingly for CTAs
- Make clickable areas large (min 40px height)
- Use consistent 4px spacing increments
- Apply hover states on all interactive elements

### ❌ Don't
- Use gradient backgrounds
- Overuse shadows
- Make text smaller than 14px
- Use purple for everything
- Ignore focus states
- Use fancy fonts

---

## 🛠 Usage Examples

### Full Button Component (HTML + CSS)

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Udemy Button</title>
  <link rel="stylesheet" href="/static/css/udemy-theme.css">
</head>
<body style="padding: 40px; background-color: var(--udemy-gray-100);">

  <h2 class="udemy-h2">Button Examples</h2>

  <div style="display: flex; gap: 16px; margin-bottom: 24px;">
    <button class="udemy-btn udemy-btn-primary udemy-btn-md">Primary</button>
    <button class="udemy-btn udemy-btn-secondary udemy-btn-md">Secondary</button>
    <button class="udemy-btn udemy-btn-outline udemy-btn-md">Outline</button>
    <button class="udemy-btn udemy-btn-ghost udemy-btn-md">Ghost</button>
  </div>

  <h3 class="udemy-h3">Button Sizes</h3>
  <div style="display: flex; gap: 16px; align-items: center;">
    <button class="udemy-btn udemy-btn-primary udemy-btn-sm">Small</button>
    <button class="udemy-btn udemy-btn-primary udemy-btn-md">Medium</button>
    <button class="udemy-btn udemy-btn-primary udemy-btn-lg">Large</button>
  </div>

</body>
</html>
```

### Full Card Component

```html
<div class="udemy-card">
  <span class="udemy-badge udemy-badge-purple">Bestseller</span>
  <h4 class="udemy-h4" style="margin-top: 12px;">Complete Python Bootcamp</h4>
  <p class="udemy-caption">Learn Python like a Professional!</p>
  <div style="margin-top: 16px; display: flex; align-items: center; gap: 8px;">
    <span style="font-weight: 700; font-size: 1.25rem; color: var(--udemy-gray-900);">$13.99</span>
    <span style="text-decoration: line-through; color: var(--udemy-gray-600);">$84.99</span>
  </div>
  <button class="udemy-btn udemy-btn-primary udemy-btn-md" style="margin-top: 16px; width: 100%;">
    Add to Cart
  </button>
</div>
```

### Full Form Example

```html
<div class="udemy-card" style="max-width: 480px;">
  <h3 class="udemy-h3">Create Your Account</h3>

  <form style="margin-top: 24px;">
    <!-- Name Input -->
    <div style="margin-bottom: 16px;">
      <label class="udemy-label" for="name">Full Name</label>
      <input
        type="text"
        id="name"
        class="udemy-input"
        placeholder="Enter your name"
      />
    </div>

    <!-- Email Input -->
    <div style="margin-bottom: 16px;">
      <label class="udemy-label" for="email">Email</label>
      <input
        type="email"
        id="email"
        class="udemy-input"
        placeholder="Enter your email"
      />
      <span class="udemy-helper-text">We'll send course recommendations.</span>
    </div>

    <!-- Password Input with Error -->
    <div style="margin-bottom: 24px;">
      <label class="udemy-label" for="password">Password</label>
      <input
        type="password"
        id="password"
        class="udemy-input udemy-input-error"
        placeholder="Create a password"
      />
      <span class="udemy-error-text">Password must be at least 8 characters</span>
    </div>

    <!-- Submit Button -->
    <button type="submit" class="udemy-btn udemy-btn-primary udemy-btn-lg" style="width: 100%;">
      Sign Up
    </button>
  </form>
</div>
```

---

## 🚀 Quick Start

1. **Include the CSS file:**
```html
<link rel="stylesheet" href="/static/css/udemy-theme.css">
```

2. **Import Inter font:**
```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
```

3. **Start using components:**
```html
<button class="udemy-btn udemy-btn-primary udemy-btn-md">Get Started</button>
```

---

## 📚 Resources

- **Udemy Homepage:** https://www.udemy.com
- **Inter Font:** https://fonts.google.com/specimen/Inter
- **Tailwind Config:** See `tailwind.config.js`
- **CSS Variables:** See `udemy-theme.css`

---

## 🎨 Color Reference Sheet

| Color Name | Hex | Usage |
|------------|-----|-------|
| Purple | #A435F0 | Primary CTA, links |
| Purple Dark | #8710D8 | Hover states |
| Gray 900 | #1C1D1F | Headings, primary text |
| Gray 600 | #6A6F73 | Body text, captions |
| Gray 400 | #D1D7DC | Borders, dividers |
| Gray 100 | #F7F9FA | Page background |
| White | #FFFFFF | Cards, surfaces |
| Success | #2D864E | Success states |
| Warning | #B4690E | Warning states |
| Error | #C91C00 | Error states |

---

**This design system is a complete recreation of Udemy's visual language.** Use it to make your practice test generator look like a native Udemy tool!
