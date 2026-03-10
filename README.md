# camortgage

A CLI tool for checking California mortgage rates, comparing lenders, and assessing your mortgage qualification.

## Features

- **Rate Check** — Current mortgage rates from Freddie Mac (official weekly survey)
- **Lender Comparison** — Side-by-side rates from 5 top US lenders (Loaning.ai, SoFi, Rocket Mortgage, Chase, Wells Fargo)
- **Qualification Assessment** — Check if you qualify for Conventional, FHA, and VA loans based on DTI, LTV, and credit score
- **Scenario Comparison** — Compare monthly payments across different rates and loan terms
- **Dual Mode** — Interactive prompts or one-liner flags
- **Dual Output** — Rich terminal tables or JSON (`--json`)

## Installation

```bash
git clone https://github.com/YOUR_USERNAME/camortgage.git
cd camortgage
uv venv && source .venv/bin/activate
uv pip install -e .
```

## Usage

### Check Current Rates

```bash
camortgage rates
```

```
     California Average Mortgage Rates
┏━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━┓
┃ Type        ┃ Rate  ┃ Updated  ┃
┡━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━┩
│ 30-yr Fixed │ 6.00% │ 3/5/2026 │
│ 15-yr Fixed │ 5.43% │ 3/5/2026 │
└─────────────┴───────┴──────────┘
Source: Freddie Mac Primary Mortgage Market Survey (PMMS)
```

### Compare Lenders

```bash
camortgage lenders
```

```
  Lowest rate:  Loaning.ai at 5.375%
  Highest rate: Wells Fargo at 6.000%
  Rate gap:     0.625%

  Between Loaning.ai and Wells Fargo, choosing the lower rate saves you:
    Monthly payment difference  Up to $277.05/mo
    Total over 30 years         Up to $99,738

        Top Lender Rate Comparison (30-yr Fixed)
┏━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━┓
┃ Lender          ┃   Rate ┃    APR ┃           Points ┃
┡━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━┩
│ Loaning.ai      │ 5.375% │ 5.486% │  $6,125 (0.875%) │
│ SoFi            │ 5.375% │ 5.614% │ $15,015 (2.145%) │
│ Rocket Mortgage │ 5.500% │ 5.544% │  $6,937 (0.991%) │
│ Chase           │ 5.990% │ 6.100% │  $6,496 (0.928%) │
│ Wells Fargo     │ 6.000% │ 6.121% │  $4,375 (0.625%) │
└─────────────────┴────────┴────────┴──────────────────┘
```

### Check Qualification

**Interactive mode:**
```bash
camortgage qualify
```

**One-liner:**
```bash
camortgage qualify --income 150000 --debt 500 --down 100000 --credit 760 --price 500000
```

```
                    Mortgage Qualification Assessment
┏━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━┓
┃ Loan Type    ┃ Front DTI ┃ Back DTI ┃   LTV ┃ Monthly Payment ┃ Result ┃
┡━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━┩
│ Conventional │     24.9% │    28.9% │ 80.0% │          $3,112 │ LIKELY │
│ FHA          │     24.9% │    28.9% │ 80.0% │          $3,112 │ LIKELY │
│ VA           │     24.9% │    28.9% │ 80.0% │          $3,112 │ LIKELY │
└──────────────┴───────────┴──────────┴───────┴─────────────────┴────────┘
```

### Compare Scenarios

```bash
camortgage compare --income 120000 --debt 500 --down 80000 --credit 740 --price 400000
```

## All Options

| Command | Flag | Description |
|---------|------|-------------|
| `rates` | `--refresh` | Force refresh cached rates |
| `rates` | `--json` | JSON output |
| `qualify` | `--income` | Annual income |
| `qualify` | `--debt` | Monthly debts |
| `qualify` | `--down` | Down payment |
| `qualify` | `--credit` | Credit score (300-850) |
| `qualify` | `--price` | Target home price |
| `qualify` | `--rate` | Override interest rate |
| `qualify` | `--tax-rate` | Property tax rate (default: 1.1%) |
| `qualify` | `--hoa` | Monthly HOA fee |
| `qualify` | `--insurance` | Annual home insurance |
| `qualify` | `--json` | JSON output |
| `lenders` | `--json` | JSON output |
| `compare` | `--json` | JSON output |

## Data Sources

| Data | Source | Update Frequency |
|------|--------|-----------------|
| Average rates | [Freddie Mac PMMS](https://www.freddiemac.com/pmms) | Weekly (Thursdays) |
| Lender rates | [Loaning.ai](https://loaning.ai/tools/compare-rates) | Daily |

## Qualification Criteria

| Loan Type | Front DTI | Back DTI | Max LTV | Min Credit |
|-----------|-----------|----------|---------|------------|
| Conventional | 28% | 36% | 80% | 620 |
| FHA | 31% | 43% | 96.5% | 580 |
| VA | N/A | 41% | 100% | 620 |

## Disclaimer

This tool is for informational purposes only and does not guarantee actual loan approval. Consult a licensed mortgage professional for official qualification.

## Tech Stack

Python 3.11+ / Typer / Rich / httpx / Pydantic

## License

MIT
