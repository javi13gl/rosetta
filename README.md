# rosetta 𓂀

**decode your prompts, pay less tokens**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Stars](https://img.shields.io/github/stars/javi13gl/rosetta?style=flat&color=yellow)](https://github.com/javi13gl/rosetta/stargazers)

A [Claude Code](https://code.claude.com) skill that translates your prompts to English before Claude processes them — cutting **up to 71% of total tokens** on real prompts when combined with [caveman](https://github.com/JuliusBrussee/caveman).

Works with any language. Auto-detects input. No API key needed.

[Install](#install) • [Benchmarks](#benchmarks) • [Before/After](#before--after) • [Why](#why-the-science)

---

## Before / After

**Spanish bug fix — same result, 36% less tokens:**

| 🗣️ Normal Claude (828 tokens) | 🪨 Caveman (587 tokens) | 𓂀 rosetta + caveman (530 tokens) |
|---|---|---|
| He revisado el archivo `buggy_auth.py` y he encontrado dos problemas críticos de seguridad. El primero está en la comparación de expiración del token: estás usando `<` en lugar de `<=`, lo que significa que los tokens que expiran exactamente en el momento actual seguirán siendo aceptados. El segundo problema es más grave: la lista `tokens_seen` se inicializa como una lista vacía dentro de la función, lo que significa que se reinicia en cada llamada, haciendo que la detección de replay attacks sea completamente inefectiva... | 2 security bugs. `expiry <` should be `<=` — tokens expiring now still accepted. `tokens_seen` init inside fn → resets each call → replay detect never works. Fix: | `expiry < → <=`. `tokens_seen` init inside fn → reset each call → replay detect broken. Fix: |

**Japanese error handling — same result, 71% less tokens:**

| 🗣️ Normal Claude (3,300 tokens) | 🪨 Caveman (2,100 tokens) | 𓂀 rosetta + caveman (950 tokens) |
|---|---|---|
| ご要望の通り、`data_processor.py`の全関数にエラーハンドリングを追加しました。`process_csv`関数については、ファイルが存在しない場合は`FileNotFoundError`を、読み取り権限がない場合は`PermissionError`をキャッチするように修正しました。また、`calculate_average`関数では、データが空の場合のゼロ除算エラーと、データ型の問題による`ValueError`に対応しました... | 3 fns, no error handling. `process_csv`: catch `FileNotFoundError`, `PermissionError`. `calculate_average`: guard empty list → `ZeroDivisionError`, catch `ValueError`. `save_results`: catch `PermissionError`. Fix: | `process_csv`: catch `FileNotFoundError`, `PermissionError`. `calculate_average`: guard empty list → ZeroDivisionError, catch `ValueError` bad types. `save_results`: catch `PermissionError`. Fix: |

Same fix. Same accuracy. Less token.

---

## Benchmarks

Real token counts from Claude Code TUI. Same prompt, three modes, fresh session each time.

💡 Across testing, longer prompts generally produced higher percentage savings, since the translation overhead stays fixed while tokenization gains scale with prompt length.

### Spanish — Bug fix (80-word prompt)

| Mode | Tokens | vs Normal | vs Caveman |
|---|---|---|---|
| Normal ES | 828 | - | - |
| Caveman ES | 587 | -29% | - |
| **rosetta + caveman** | **530** | **-36%** | **-10%** |

### Japanese — Error handling (pure Japanese prompt, no English technical terms)

| Mode | Tokens | vs Normal | vs Caveman |
|---|---|---|---|
| Normal JA | 3,300 | - | - |
| Caveman JA | 2,100 | -36% | - |
| **rosetta + caveman** | **950** | **-71%** | **-55%** |

> 💡 The Japanese result shows a key insight: rosetta's savings scale with how "pure" the native language is. Prompts mixing native language with English technical terms (function names, file names) see smaller gains. Prompts written in pure native language see the full effect of the tokenization factor.

---

## Multilingual Support

Rosetta auto-detects your language. No configuration needed — just use `/t` in any language.

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
/t このファイルにはエラー処理が全くありません。考えられるすべての問題に対してエラー処理を追加してください

# Chinese
/t 检查认证模块，token过期检查使用了<而不是<=，还有重放攻击检测也有问题

# Arabic
/t راجع وحدة المصادقة، يستخدم فحص انتهاء الرمز < بدلاً من <=
```

Write short prompts and code-heavy tasks directly in English — rosetta overhead not worth it below the break-even point or when output is mostly code blocks.

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
│  REAL-WORLD NET (Spanish)  ████████░░░░  36% │
│  REAL-WORLD NET (Japanese) ████████████  71% │
└──────────────────────────────────────────────┘
```

---

## How It Works

```
You type:    /t このファイルにはエラー処理が全くありません...
                          ↓
             translate.py → Google Translate API (free, no key)
             auto-detects language, translates to English
                          ↓
Claude receives: "This file has no error handling at all..."
                          ↓
             caveman compresses the response
                          ↓
You get:     terse English answer, up to 71% fewer tokens
```

Claude never sees the original language. Zero LLM translation cost.

---

## Limitations

- Requires Python 3 and internet access for Google Translate
- Only worth using above the break-even point for your language (see table above)
- Less effective when prompts mix native language with English technical terms (function names, file paths)
- Less effective for code-heavy tasks where output is mostly code blocks (caveman doesn't compress code)
- Bash tool call appears in Claude Code transcript — this overhead defines the break-even

---

## Credits

- [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) — the output compression layer rosetta pairs with
- Ahia et al., EMNLP 2023 — *Do All Languages Cost the Same?* — the tokenization cost research behind rosetta's design

---

## License

MIT
