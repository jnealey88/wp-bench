# WP-Bench Datasets

This directory contains the benchmark test suites and tooling for publishing to Hugging Face Hub.

## Structure

```
datasets/
├── suites/                    # Source of truth (human-editable JSON)
│   └── wp-core-v1/
│       ├── execution/         # Code generation tests (one file per category)
│       │   ├── hooks.json
│       │   ├── rest-api.json
│       │   └── ...
│       └── knowledge/         # Multiple choice / short answer tests
│           ├── hooks.json
│           ├── rest-api.json
│           └── ...
├── data/                      # Generated Parquet for HF (gitignored)
│   └── test.parquet
├── export_dataset.py          # Converts suites → Parquet
└── README.md
```

## Local Development

The harness loads directly from `suites/` JSON files:

```yaml
# wp-bench.yaml
dataset:
  source: local
  name: wp-core-v1
```

## Publishing to Hugging Face

1. **Export to Parquet:**
   ```bash
   python datasets/export_dataset.py
   ```

2. **Upload to HF Hub:**
   ```bash
   huggingface-cli upload WordPress/wp-bench-v1 datasets/data/
   ```

3. **Users can then load:**
   ```python
   from datasets import load_dataset
   ds = load_dataset("WordPress/wp-bench-v1", split="test")
   ```

## Adding New Suites

1. Create `suites/<suite-name>/execution/` and `knowledge/` directories
2. Add category JSON files (e.g., `hooks.json`, `rest-api.json`) to each directory
3. Follow the schema in existing suites
4. Run `python datasets/export_dataset.py` to include in Parquet export

## Schema

### Execution Tests
| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique test ID |
| `prompt` | string | Task description for the model |
| `requirements` | array | List of requirements the solution must meet |
| `static_checks` | object | Regex patterns to check in generated code |
| `runtime_checks` | object | Assertions to run in WordPress environment |
| `reference_solution` | string | Example correct solution |

#### Runtime Checks Schema

The `runtime_checks` object supports the following fields:

| Field | Type | Description |
|-------|------|-------------|
| `setup` | string | PHP code to run before the generated code |
| `teardown` | string | PHP code to run after assertions |
| `fire_hooks` | array | WordPress hooks to fire after code execution |
| `assertions` | array | List of assertion objects to verify behavior |

##### fire_hooks

The `fire_hooks` field allows tests to trigger WordPress action hooks after the generated code has been executed. This is useful for testing code that registers callbacks (e.g., block registration on `init`).

```json
{
  "runtime_checks": {
    "fire_hooks": ["init", "wp_loaded"],
    "assertions": [...]
  }
}
```

**Use cases:**

- Testing `add_action('init', ...)` callbacks by firing `init` after code execution
- Testing block registration that depends on WordPress being initialized
- Testing any hook-dependent functionality

**Note:** Hooks are fired in the order specified in the array.

### Knowledge Tests
| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique test ID |
| `prompt` | string | Question text |
| `choices` | array | Multiple choice options `[{key, text}]` |
| `correct_answer` | string | Correct choice key (e.g., "B") |
