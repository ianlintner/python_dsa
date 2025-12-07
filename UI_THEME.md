# UI Theme Integration Guide

This Flask app now uses **Tailwind CSS** with the **[@ianlintner/theme](https://www.npmjs.com/package/@ianlintner/theme)** preset for a modern, responsive interface with built-in dark mode support.

## Architecture

### Frontend Stack

- **Tailwind CSS 3.3+** - Utility-first CSS framework
- **@ianlintner/theme** - Custom theme preset with semantic colors and components
- **Vanilla JavaScript** - No frontend framework dependencies

### File Structure

```text
flask_app/
├── templates/
│   ├── base.html              # Main layout with header, footer, modal
│   ├── index.html             # Dashboard with search and filtering
│   └── [other pages...]
├── static/
│   ├── input.css              # Entry point (imports theme styles & Tailwind)
│   ├── output.css             # Generated Tailwind CSS (built via npm)
│   └── [other assets...]
```

### Build Process

- **Input**: `flask_app/static/input.css` imports theme styles and Tailwind directives
- **Build Tool**: Tailwind CSS CLI
- **Output**: `flask_app/static/output.css` (loaded by Flask templates)

## Setup & Development

### Initial Setup

```bash
# Install npm dependencies
npm install

# Build CSS (generates flask_app/static/output.css)
npm run build:css
```

### Development Workflow

**Watch mode** (auto-rebuild on file changes):

```bash
npm run watch:css
```

**Manual build**:

```bash
npm run build:css
```

### Adding to Flask

The templates reference the built CSS:

```html
<link rel="stylesheet" href="{{ url_for('static', filename='output.css') }}">
```

## Theme Features

### Colors & Styling

The theme provides semantic color tokens (via CSS variables) that work in light and dark modes:

- **Primary**: Blue (default brand color)
- **Destructive**: Red (alerts, errors)
- **Muted**: Gray (secondary text, disabled states)
- **Accent**: System accent color

### Dark Mode

Dark mode is automatically applied based on:

1. localStorage preference (`theme` key)
2. System preference (`prefers-color-scheme`)
3. Default: Dark mode

Toggle via the theme selector in the header:

```javascript
// Theme toggle (in base.html)
document.documentElement.classList.toggle('dark', theme === 'dark');
```

### Responsive Design

All components use Tailwind's responsive prefixes:

- `sm:`, `md:`, `lg:` breakpoints for mobile-first design
- Grid layouts adapt from 1 → 2 → 3 columns

## Customization

### Extending the Theme

Edit `tailwind.config.js`:

```javascript
const config = {
  presets: [themePreset],
  theme: {
    extend: {
      colors: {
        // Add custom colors
        brand: '#0066cc',
      },
      spacing: {
        // Add custom spacing
      },
    },
  },
};
```

### Adding Custom Components

In `flask_app/static/input.css`:

```css
@layer components {
  .my-card {
    @apply bg-white dark:bg-slate-900 rounded-lg shadow-md p-4;
  }
}
```

### Modifying Colors

The theme uses CSS variables defined by `@ianlintner/theme`. Override them in your input.css:

```css
:root {
  --primary: 200 100% 50%;  /* HSL format */
  --secondary: 280 100% 50%;
}

[data-theme="light"] {
  --background: 0 0% 100%;
  --foreground: 0 0% 0%;
}
```

## Component Patterns

### Demo Card

```html
<article class="demo-card">
  <div class="demo-card-title">Card Title</div>
  <p class="demo-card-description">Description text</p>
  <button class="px-3 py-2 bg-blue-600 text-white rounded-lg">Action</button>
</article>
```

### Modal

The demo modal uses vanilla JavaScript:

```javascript
openModal(title);  // Show modal
closeModal();      // Hide modal
runDemo(id, title); // Run and display demo output
```

### Badges & Tags

```html
<span class="badge-info">Info badge</span>
<span class="badge-warning">Warning badge</span>
```

## Performance

### Bundle Size

- **Tailwind CSS**: ~32 KB (gzipped)
- **Theme Styles**: Included in Tailwind output
- **JavaScript**: ~2 KB (modal & search logic)

### Optimization

- Unused CSS automatically removed (Tailwind purge)
- Template paths configured in `tailwind.config.js`
- Dark mode using CSS class (no extra HTTP requests)

## Troubleshooting

### CSS not updating

```bash
# Clear and rebuild
rm flask_app/static/output.css
npm run build:css
```

### Theme not applying

1. Verify `output.css` is being served: Check Flask logs
2. Clear browser cache (Ctrl+Shift+Del or Cmd+Shift+Delete)
3. Verify `dark` class is on `<html>` element

### Missing dependencies

```bash
# Reinstall all packages
rm -rf node_modules package-lock.json
npm install
npm run build:css
```

## Deployment

### Production Build

```bash
# Build CSS for production
npm run build:css
```

The generated `flask_app/static/output.css` is all that's needed—Node.js is not required at runtime.

### CI/CD

```bash
npm install
npm run build:css
python -m pip install -e ".[dev]"
pytest -q
```

## Resources

- [Tailwind CSS Docs](https://tailwindcss.com/docs)
- [@ianlintner/theme NPM Package](https://www.npmjs.com/package/@ianlintner/theme)
- [Tailwind CSS Dark Mode](https://tailwindcss.com/docs/dark-mode)
