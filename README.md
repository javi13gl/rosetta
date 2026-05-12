# rosetta 𓂀

**decode your prompts, pay less tokens**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A [Claude Code](https://code.claude.com) skill that translates your prompts to English before Claude processes them — cutting **up to 49% of total tokens** on real prompts when combined with [caveman](https://github.com/JuliusBrussee/caveman).

Works with any language. Auto-detects input. No API key needed.

[Install](#install) • [Benchmarks](#benchmarks) • [Before/After](#before--after) • [Why](#why-the-science)

---

## Before / After

| | |
|---|---|
| 🗣️ Normal Claude ES (1750 tokens) | `revisa todos los archivos python del proyecto, hay un bug en load_config que puede fallar silenciosamente...` → Claude reads Spanish, responds verbose |
| 𓂀 rosetta + caveman (980 tokens) | `/t revisa todos los archivos python...` → Claude receives English, responds terse. **44% less tokens.** |

Same fix. Same accuracy. Less token.

---

## Benchmarks

Real token counts from Claude Code TUI. Same prompt, three modes, fresh session each time.

### Short prompts (<65 words) — caveman wins here

| Task | Normal ES | Caveman ES | rosetta + caveman | Saved vs normal |
|---|---|---|---|---|
| Explain Python garbage collector | 661 | 512 | 565 | -15% |

> ⚠️ For short prompts, rosetta's bash tool call overhead (~35 tokens) exceeds translation savings. Use caveman alone.

### Long prompts (65+ words) — rosetta wins here

| Task | Normal ES | Caveman ES | rosetta + caveman | Saved vs normal | Saved vs caveman |
|---|---|---|---|---|---|
| Explain GC in detail (70 words) | 1720 | 1340 | 810 | **-53%** | **-40%** |
| Review Python files for bugs (65 words) | 1750 | 1600 | 980 | **-44%** | **-39%** |
| **Average** | **1735** | **1470** | **895** | **-48%** | **-39%** |

**Break-even point for Spanish: ~65 words.** Above that, rosetta consistently beats caveman alone by ~39%.

---

## Multilingual Support

Rosetta auto-detects your language. No configuration needed — just use `/t` in any language.

The savings vary significantly by language. Non-Latin scripts benefit the most due to how LLM tokenizers work:

| Language | Token cost vs English | Input savings | Break-even point |
|---|---|---|---|
| French | 1.2x | ~17% | ~100 words |
| Italian | 1.2x | ~17% | ~100 words |
| Portuguese | 1.3x | ~23% | ~80 words |
| Spanish | 1.5x | ~33% | ~65 words |
| Korean | 1.6x | ~37% | ~55 words |
| Japanese | 1.8x | ~44% | ~45 words |
| Chinese (Simplified) | 2.0x | ~50% | ~40 words |
| Arabic | 2.0x | ~50% | ~40 words |
| Russian | 2.5x | ~60% | ~35 words |

For Japanese, Chinese, Arabic, or Russian speakers, rosetta is significantly more impactful than for Spanish or French users. A Japanese developer writing 50-word prompts already exceeds the break-even point.

All data based on Ahia et al., EMNLP 2023 — *Do All Languages Cost the Same?*

---

## Install

### With caveman (recommended)

Install caveman first:
```bash
npx skills add JuliusBrussee/caveman
```

Then rosetta:

**macOS / Linux:**
```bash
mkdir -p ~/.claude/scripts ~/.claude/commands
curl -o ~/.claude/scripts/translate.py https://raw.githubusercontent.com/javi13gl/rosetta/main/scripts/translate.py
curl -o ~/.claude/commands/t.md https://raw.githubusercontent.com/javi13gl/rosetta/main/commands/t.md
```

**Windows (PowerShell):**
```powershell
mkdir -p "$env:USERPROFILE\.claude\scripts", "$env:USERPROFILE\.claude\commands"
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/javi13gl/rosetta/main/scripts/translate.py" -OutFile "$env:USERPROFILE\.claude\scripts\translate.py"
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/javi13gl/rosetta/main/commands/t.md" -OutFile "$env:USERPROFILE\.claude\commands\t.md"
```

No API key needed. Uses Google Translate free tier.

---

## Usage

Start every session:
```
/caveman
```

Write long prompts in your language with `/t`:

```
# Spanish
/t revisa el módulo de autenticación, el token expiry usa < en vez de <=

# Japanese
/t 認証モジュールを確認して、トークンの有効期限チェックが<を使っています

# Chinese
/t 检查认证模块，token过期检查使用了<而不是<=

# Arabic
/t راجع وحدة المصادقة، يستخدم فحص انتهاء الرمز < بدلاً من <=
```

Write short prompts directly in English — rosetta overhead not worth it below the break-even point for your language.

---

## Why: The Science

### LLMs tokenize English cheaper than any other language

Ahia et al., EMNLP 2023 — *"Do All Languages Cost the Same? Tokenization in the Era of Commercial Language Models"* — measured tokenization costs across 24 languages. The finding: English is the cheapest language to process by a wide margin.

The root cause: GPT-4, Claude, and Gemini are trained on English-dominant datasets. Tokenizers learn to compress what they see most. English gets ultra-efficient encoding; everything else is treated as foreign. The same sentence "Hello, my name is Sarah" costs 7 tokens in English, 11 in Spanish, 35 in Hindi, and 42 in Greek.

For a developer writing 100-token non-English prompts all day, the waste compounds fast — up to 60% of input tokens wasted on Russian, and 50% on Chinese or Arabic.

### Why rosetta only activates above the break-even point

The translation mechanism uses a bash tool call with a fixed overhead of ~35 tokens. For short prompts, this overhead exceeds the translation savings. The break-even point depends on how expensive your language is to tokenize:

```
Break-even formula:
(native_tokens × savings_rate) > 35 overhead tokens

Spanish (33% savings): break-even at ~106 tokens (~65 words)
Japanese (44% savings): break-even at ~80 tokens  (~45 words)
Russian  (60% savings): break-even at ~58 tokens  (~35 words)
```

### Combined with caveman output compression

[Caveman](https://github.com/JuliusBrussee/caveman) cuts ~65% of output tokens. Rosetta cuts input tokens based on your language. Combined effect:

```
┌──────────────────────────────────────────────┐
│  INPUT SAVINGS (rosetta)                     │
│    Spanish  ████░░░░  33%                    │
│    Japanese ██████░░  44%                    │
│    Russian  ████████  60%                    │
│                                              │
│  OUTPUT SAVINGS (caveman)  ████████████  65% │
│                                              │
│  REAL-WORLD NET (Spanish)  ████████░░░░  49% │
│  REAL-WORLD NET (Japanese) ██████████░░  57% │
│  REAL-WORLD NET (Russian)  ████████████  63% │
└──────────────────────────────────────────────┘
```

---

## How It Works

```
You type:    /t revisa el módulo de autenticación...
                          ↓
             translate.py → Google Translate API (free, no key)
             auto-detects language, translates to English
                          ↓
Claude receives: "review the authentication module..."
                          ↓
             caveman compresses the response
                          ↓
You get:     terse English answer, up to 49-63% fewer tokens
```

Claude never sees the original language. Zero LLM translation cost.

---

## Limitations

- Requires Python 3 and internet access for Google Translate
- Only worth using above the break-even point for your language (see table above)
- Bash tool call appears in Claude Code transcript — this overhead defines the break-even
- Output is always in English — pair with caveman for maximum compression

---

## Credits

- [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) — the output compression layer rosetta pairs with
- Ahia et al., EMNLP 2023 — *Do All Languages Cost the Same?* — the tokenization cost research behind rosetta's design

---

## License

MIT
