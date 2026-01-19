# WP-Bench Results Summary

**Date:** January 18, 2026

## Scoring Rubric

WP-Bench evaluates AI models on three dimensions:

### Knowledge Score (40% of overall)

Multiple-choice questions testing WordPress API knowledge. Models must select the correct answer from 4 options.

- **What it measures:** Understanding of WordPress core APIs, best practices, and conventions
- **Scoring:** Binary (correct = 1.0, incorrect = 0.0)
- **Example:** "Which hook fires after WordPress is fully loaded?" → `wp_loaded`

### Correctness Score (30% of overall)

Code execution tests where generated PHP code runs in a real WordPress environment.

- **What it measures:** Whether the code actually works when executed
- **Scoring:** Runtime assertions verify functional behavior (e.g., "Is the block registered?", "Does the hook fire?")
- **Example:** "Register a custom block type" → Code is executed, then `WP_Block_Type_Registry::get_instance()->is_registered()` verifies success

### Quality Score (30% of overall)

Static analysis of generated code for patterns and best practices.

- **What it measures:** Code structure, use of correct APIs, security practices
- **Scoring:** Weighted regex pattern matching (e.g., uses `register_block_type`, includes proper escaping)
- **Example:** Code must contain `register_block_type` and follow WordPress naming conventions

### Overall Score Formula

```
Overall = (Knowledge × 0.4) + (Correctness × 0.3) + (Quality × 0.3)
```

---

## Test Suite: wp-core-v1

**Total Tests:** 46 knowledge + 28 execution = 74 total

### Knowledge Tests by Category (46 tests)

| Category | Tests | Topics |
|----------|-------|--------|
| Block API | 6 | Block processor, block.json schema, attributes, supports, render |
| Block Hooks | 5 | Block insertion, hooked blocks, anchor blocks |
| Block Editor | 4 | Editor internals, block patterns, templates |
| DataViews | 4 | DataViews component, fields, filters |
| Abilities API | 3 | User capabilities, primitive capabilities |
| Block Bindings | 3 | Bindings API, sources, connected blocks |
| Caching | 3 | Object cache, transients, cache groups |
| Hooks | 3 | Actions, filters, hook priorities |
| Interactivity API | 3 | Directives, state management, context |
| HTML API | 2 | Tag processor, HTML parsing |
| Queries | 2 | WP_Query, query vars |
| REST API | 2 | Endpoints, authentication |
| Security | 2 | Nonces, escaping, sanitization |
| Font Library | 1 | Font management |
| Gotchas | 1 | Common WordPress pitfalls |
| Internationalization | 1 | Translation functions |
| Roles & Caps | 1 | User roles, capabilities |

### Execution Tests by Category (28 tests)

| Category | Tests | Tasks |
|----------|-------|-------|
| HTML API | 6 | Tag processing, attribute manipulation, DOM traversal |
| Block API | 5 | Block registration, dynamic blocks, attributes, patterns |
| Abilities API | 2 | Custom capabilities, primitive capabilities |
| Block Bindings | 2 | Custom binding sources |
| Caching | 2 | Object cache operations, transients |
| Interactivity API | 2 | State management, directives |
| REST API | 2 | Custom endpoints, route handling |
| Block Hooks | 1 | Hooked block registration |
| Database | 1 | Custom table operations |
| Font Library | 1 | Font registration |
| Hooks | 1 | Action/filter registration |
| Post Meta | 1 | Meta registration and retrieval |
| Shortcodes | 1 | Shortcode registration |
| WP_Query | 1 | Custom queries |

### New Tests Added (Issue #6)

The following tests were added to expand Block API coverage:

**Knowledge Tests (4 new):**

- `k-blockjson-schema-001` (basic) - Required fields in block.json
- `k-blockjson-attributes-001` (intermediate) - Valid attribute types
- `k-blockjson-supports-001` (intermediate) - Block supports flags
- `k-blockjson-render-001` (hard) - Server-side rendering in block.json

**Execution Tests (4 new):**

- `e-block-register-001` (basic) - Register a static block with register_block_type()
- `e-block-dynamic-001` (intermediate) - Create dynamic block with render_callback
- `e-block-attributes-001` (intermediate) - Block with typed attributes
- `e-block-pattern-001` (hard) - Register a block pattern

---

## Model Results

| Model | Knowledge | Correctness | Quality | Overall |
|-------|-----------|-------------|---------|---------|
| gpt-5.2 (reasoning: high) | 91.30% | 45.24% | **98.53%** | **75.05%** |
| gemini/gemini-3-flash-preview | 84.78% | 50.00% | 94.74% | 73.86% |
| gpt-5.2 (reasoning: low) | 91.30% | 42.26% | 96.91% | 73.37% |
| gpt-5.2 (reasoning: medium) | 91.30% | 42.26% | 96.91% | 73.37% |
| anthropic/claude-sonnet-4-5 | 84.78% | **51.79%** | 88.66% | 72.75% |
| gpt-5.2 | 91.30% | 40.48% | 96.91% | 72.65% |
| anthropic/claude-opus-4-5 (thinking) | 89.13% | 42.86% | 94.55% | 72.25% |
| gemini/gemini-2.5-pro | 86.96% | 41.07% | 96.91% | 71.59% |
| anthropic/claude-haiku-4-5 | 78.26% | 44.64% | 93.07% | 69.26% |
| anthropic/claude-opus-4-5 | 76.09% | 42.86% | 96.23% | 68.84% |
| openai/gpt-5-mini | 84.78% | 39.29% | 91.75% | 68.67% |
| gemini/gemini-3-pro-preview | 69.57% | 46.43% | 94.74% | 67.86% |
| gemini/gemini-2.5-flash | 60.87% | 30.36% | 94.74% | 58.83% |

---

## Key Findings

### Best Performers

- **Highest Correctness:** Claude Sonnet 4.5 (51.79%), Gemini 3 Flash (50.00%)
- **Highest Knowledge:** GPT-5.2 family (91.30%)
- **Highest Quality:** GPT-5.2 reasoning: high (98.53%)
- **Best Overall:** GPT-5.2 reasoning: high (75.05%)

### GPT-5.2 Reasoning Effort Analysis

| Reasoning Level | Correctness | Quality | Overall |
|-----------------|-------------|---------|---------|
| none (default)  | 40.48%      | 96.91%  | 72.65%  |
| low             | 42.26%      | 96.91%  | 73.37%  |
| medium          | 42.26%      | 96.91%  | 73.37%  |
| high            | 45.24%      | 98.53%  | 75.05%  |

Higher reasoning effort improves correctness and code quality scores.

### Model Configuration Notes

- GPT-5.2-nano and GPT-5.2-mini require `temperature=1.0`
- GPT-5.2 with `reasoning_effort` requires `temperature=1.0`
- Claude extended thinking requires `temperature=1.0` and has 8K output tokens/min rate limit
- Gemini 3 Pro Preview has 25 req/min rate limit (run with `concurrency=1`)

---

## Fixes Applied This Session

1. **Sandbox Error Handling:** Modified to ignore `E_USER_NOTICE` level errors (WordPress "doing it wrong" notices)
2. **Static Analysis Regex:** Changed delimiter from `/` to `#` to fix pattern matching for paths like `wpbench/greeting`

---

## Raw Results

Individual JSON result files are available in the `output/` directory with timestamps.
