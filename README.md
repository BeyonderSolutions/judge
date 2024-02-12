![judge](https://img.shields.io/badge/judge-0.1.5-green) ![flake8](https://img.shields.io/badge/flake8-6.1.0-blue) ![pytest](https://img.shields.io/badge/pytest-8.0.0-blue)

# ⚖️ judge
Lazily review Python project inconsistencies, tests and vulnerabilities.

## Installation
```bash
pip install git+https://github.com/BeyonderSolutions/judge.git
```

## Usage

### Running on current working directory

```bash
judge
```


### Running on specific directory

```bash
judge /path/to/dir
```

### Flags
| Flag(s) | Description |
| --- | --- |
| `--run-all`, `-a` | Runs all analyzers. |
| `--flake8`, `-f8` | Runs the `flake8` analyzer. |
| `--pytest`, `-pt` | Runs the `pytest` analyzer. |


### Running on a GitHub Workflow
You create Judge reports from a GitHub Action. Here is an example that automatically posts a comment on a pull request using [thollander's actions-comment-pull-request](https://github.com/thollander/actions-comment-pull-request):
<details>
<summary>📄 judge_report.yml</summary>

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

## Configuration

### Using the `judge_settings.toml` configuration file
This is a `TOML` file that defines project constants so that you don't have to write flags every five minutes for running reports. Here is an example `judge_settings.toml` file:

```toml
[judge]
defaults = ["flake8"]

[flake8]
ignore = ["E402", "F401", "F403", "W503"]
exclude = ["playground/"]
```

#### Properties
| Program | Value | Type | Description |
| --- | --- | --- | --- |
| `judge` | `defaults` | `List[str]` | The analyzers that should run by default when running `judge` with no other flags. Adding any other argument flags overrides this setting.
| `flake8` | `ignore` | `List[str]` | The PEP8 error codes to ignore.
| `flake8` | `exclude` | `List[str]` | The files and directories to ignore (uses `.gitignore` style syntax).



## Tips
- ⚠️ Don't forget to ignore `judge_report.md` on your `.gitignore`!
- 💡 If running on a **VS Code** terminal, you can `Ctrl`+`Left-Click` on a filename to open it directly on your IDE.
- 💡 If running on a **VS Code** terminal, you can `Ctrl`+`Left-Click` on a `flake8` error code to view more information about it.
