# GitGhost

Private version control for your Git ignored files.

## Why use GitGhost?

- **Keep sensitive files private:** Manage secrets, configs, or personal files outside your public repo.
- **Seamless Git integration:** Works alongside your existing Git workflow.
- **Simple commands:** Easily save, check status, or discard private changes.
- **Separate private repo:** Keeps your private data secure and versioned.
- **Cross-platform:** Designed for Linux, works on any system with Python 3.10+.

## Requirements

- Python 3.10 or higher
- Git installed
- GitHub CLI (`gh`) is required for private repo automation

## Installation

Install GitGhost directly from PyPI:

```bash
pip install gitghost
```

## Commands

Initialize GitGhost in your project:

```bash
gitghost init
```

Check status of private files:

```bash
gitghost status
```

Save private changes:

```bash
gitghost save
```

Discard private changes:

```bash
gitghost discard
```

Get help and list all commands:

```bash
gitghost help
```

## How it works

- Specify private files/folders in `.gitghostinclude` (which should also be in `.gitignore`).
- GitGhost manages a **separate private repository** for these files.
- `gitghost save` commits and pushes private changes.
- `gitghost status` shows private file changes.
- Keeps private data out of your public repo, but safely versioned.

## License

This project is licensed under the **MIT License**. See the [LICENSE](https://opensource.org/licenses/MIT) file for details.
