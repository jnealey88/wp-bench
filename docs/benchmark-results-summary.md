# WP-Bench Results Summary

**Date:** January 19, 2026

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

---

## Model Results

| Model | Knowledge | Correctness | Quality | Overall | Time (s) | Tokens | Cost |
|-------|-----------|-------------|---------|---------|----------|--------|------|
| gemini/gemini-3-flash-preview | 84.78% | **50.00%** | 94.74% | **73.86%** | 69 | 13,346 | $0.02 |
| anthropic/claude-sonnet-4-5 | 89.13% | 48.21% | 92.37% | 73.74% | 97 | 15,804 | $0.14 |
| gpt-5.2 (reasoning: high) | **91.30%** | 41.67% | **98.53%** | 73.62% | 859 | 78,344 | $1.02 |
| anthropic/claude-opus-4-5 (thinking) | **91.30%** | 44.64% | 91.86% | 72.81% | 1,247 | 89,168 | $2.03 |
| gpt-5.2 | **91.30%** | 40.48% | 96.91% | 72.65% | 105 | 14,253 | $0.12 |
| gpt-5.2 (reasoning: low) | 89.13% | 40.48% | 98.53% | 72.49% | 207 | 22,861 | $0.24 |
| gpt-5.2 (reasoning: medium) | 89.13% | 40.48% | 98.53% | 72.49% | 364 | 39,687 | $0.47 |
| anthropic/claude-opus-4-5 | 76.09% | 46.43% | 96.23% | 70.27% | 181 | 24,098 | $0.45 |
| openai/gpt-4.1 | 82.61% | 41.07% | 94.74% | 69.63% | 80 | 12,486 | $0.06 |
| anthropic/claude-haiku-4-5 | 78.26% | 44.64% | 93.07% | 69.26% | 74 | 19,488 | $0.07 |
| openai/gpt-5-mini | 82.61% | 42.86% | 90.41% | 69.05% | 539 | 64,650 | $0.12 |
| gemini/gemini-2.5-pro | 89.13% | 33.93% | 96.91% | 69.38% | 599 | 137,534 | $1.32 |
| gemini/gemini-3-pro-preview | 69.57% | 42.86% | 94.74% | 66.43% | 419 | 29,504 | $0.29 |
| gemini/gemini-2.5-flash | 67.39% | 28.57% | 94.74% | 60.07% | 281 | 99,678 | $0.23 |

---

## Key Findings

### Best Performers

- **Best Overall:** Gemini 3 Flash (73.86%) - also fastest (69s) and cheapest ($0.02)
- **Highest Correctness:** Gemini 3 Flash (50.00%), Claude Sonnet 4.5 (48.21%)
- **Highest Knowledge:** GPT-5.2 family, Claude Opus 4.5 (thinking) (91.30%)
- **Highest Quality:** GPT-5.2 reasoning: high/low/medium (98.53%)

### Best Value Models

| Model | Overall | Time | Cost | Value Rating |
|-------|---------|------|------|--------------|
| gemini/gemini-3-flash-preview | 73.86% | 69s | $0.02 | Best overall value |
| openai/gpt-4.1 | 69.63% | 80s | $0.06 | Good budget option |
| anthropic/claude-haiku-4-5 | 69.26% | 74s | $0.07 | Fast and affordable |
| gpt-5.2 | 72.65% | 105s | $0.12 | Good balance |

### GPT-5.2 Reasoning Effort Analysis

| Reasoning Level | Correctness | Quality | Overall | Time | Cost |
|-----------------|-------------|---------|---------|------|------|
| none (default)  | 40.48%      | 96.91%  | 72.65%  | 105s | $0.12 |
| low             | 40.48%      | 98.53%  | 72.49%  | 207s | $0.24 |
| medium          | 40.48%      | 98.53%  | 72.49%  | 364s | $0.47 |
| high            | 41.67%      | 98.53%  | 73.62%  | 859s | $1.02 |

Higher reasoning effort shows diminishing returns - `high` provides only +1% overall at 8x the cost.

### Model Configuration Notes

- GPT-5.2-nano and GPT-5.2-mini require `temperature=1.0`
- GPT-5.2 with `reasoning_effort` requires `temperature=1.0`
- Claude extended thinking requires `temperature=1.0` and has 8K output tokens/min rate limit
- Gemini 3 Pro Preview has 25 req/min rate limit (run with `concurrency=1`)

---

## Raw Results

Individual JSON result files are available in the `output/` directory with timestamps.
