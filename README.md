![judge](https://img.shields.io/badge/judge-0.1.2-green) ![flake8](https://img.shields.io/badge/flake8-6.1.0-blue)

# ⚖️ judge
Lazily review Python project inconsistencies and vulnerabilities.

## Installation
```bash
pip install git+https://github.com/BeyonderSolutions/judge.git
```

## Usage

### Running on current working directory

```bash
judge
```


### Running on another directory

```bash
judge /path/to/dir
```


### Running on a GitHub Workflow

```yaml
name: ⚖️ Judge Report

on:
  pull_request:
    branches:
      - main
      - development

jobs:
  judge:
    runs-on: [ubuntu-latest]
    defaults:
      run:
        working-directory: ./
    
    strategy:
      matrix:
        python-version: ["3.10"]

    steps:
      - name: Setup repository environment
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version}}

      - name: Install dependencies
        run: |
          pip install --upgrade pip
          pip install git+https://github.com/BeyonderSolutions/judge.git

      - name: Run Judge
        run: judge
```


## Tips
- ⚠️ Don't forget to ignore `judge_report.md` on your `.gitignore`!
- 💡 If running on a **VS Code** terminal, you can `Ctrl`+`Left-Click` on a filename to open it directly on your IDE.
