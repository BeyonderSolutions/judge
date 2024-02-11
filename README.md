![judge](https://img.shields.io/badge/judge-0.1.5-green) ![flake8](https://img.shields.io/badge/flake8-6.1.0-blue)

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
You create Judge reports from a GitHub Action. Here is an example that automatically posts a comment on a pull request using [thollander's actions-comment-pull-request](https://github.com/thollander/actions-comment-pull-request):
<details>
<summary>judge_report.yml</summary>

```yaml
name: ⚖️ Judge
on:
  pull_request:
    branches:
      - main
      - development
jobs:
  judge:
    name: Judge Report
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
          python-version: ${{ matrix.python-version }}
      - name: Install dependencies
        run: |
          pip install --upgrade pip
          pip install git+https://github.com/BeyonderSolutions/judge.git
      - name: Run Judge
        run: |
          judge
      - name: Archive Judge Report
        uses: actions/upload-artifact@v2
        with:
          name: judge-report
          path: judge_report.md
  comment_pr:
    name: Comment Pull Request
    needs: judge
    permissions:
      pull-requests: write
    runs-on: ubuntu-latest
    steps:
      - name: Download Judge Report
        uses: actions/download-artifact@v2
        with:
          name: judge-report
          path: ./
      - name: Comment PR
        uses: thollander/actions-comment-pull-request@v2
        with:
          filePath: ./judge_report.md
```
</details>


## Tips
- ⚠️ Don't forget to ignore `judge_report.md` on your `.gitignore`!
- 💡 If running on a **VS Code** terminal, you can `Ctrl`+`Left-Click` on a filename to open it directly on your IDE.
