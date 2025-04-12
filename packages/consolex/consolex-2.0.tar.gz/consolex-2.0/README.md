# consolex
If you're familiar with JavaScript and miss the console.log functionality in Python, consolex is perfect for you. It brings the same convenience and style, but with Python syntax!

**consolex** is a Python package that mimics the familiar JavaScript-style console logging in a modern and user-friendly way. With this package, you can easily print logs, warnings, errors, and success messages in the terminal using stylish icons and customizable options.

## 🚀 What's New in v2.0?
- ✅ New `primary()` method
- 🎀 New text colors
- ⚙️ Improved formatting options (`sep`, `end`)
- 🐛 Bug fixes and performance improvements


## Features
- **log()**: Print general messages to the console.
- **warn()**: Print warning messages with a warning icon.
- **error()**: Print error messages with an error icon.
- **success()**: Print success messages with a success checkmark.
- **primary()**: Print primary messages with color.

All methods support custom separators, line endings, and variable numbers of arguments, similar to JavaScript's `console.log`.

## Examples
```
from consolex import console

# Print a log message
console.log("This is a log message.")

# Print a warning message
console.warn("This is a warning message.")

# Print an error message
console.error("This is an error message.")

# Print a success message
console.success("This is a success message.")

# Print a primary message
console.primary("This is a primary message.")
```

## Installation

You can easily install `consolex` via pip:

```bash
pip install consolex
