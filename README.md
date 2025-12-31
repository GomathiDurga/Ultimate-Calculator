# 🧮 Smart CLI Calculator

**Ultimate terminal calculator**: Math + **ANY units** (km→m) + **ANY currency** (AED→INR) + history.

## Features
- 🧮 **Math**: `10.5*2.3`, `sqrt(16)`, `2^3`, `log(100)`
- 📏 **ANY Units**: `5.7 km m`, `23.9 C F`, `100 m ft`
- 💱 **ANY Currency**: `100 AED INR`, `250 GBP USD`, `75 JPY EUR`
- 📝 **History**: `history` command + `clear`


## Supported Conversions
**Units** (20+ pairs):
- Length: `km↔m`, `miles↔km`, `m↔ft`, `cm↔inch`
- Weight: `kg↔lbs`, `g↔oz`
- Temperature: `C↔F`

**Currencies** (81 pairs):
- USD, INR, AED, EUR, GBP, CAD, AUD, JPY, SGD

## Tech Stack
- Python 3.x
- `re` (regex parsing for ANY value)
- `math` (advanced functions)
- `json` (history persistence)


## Commands
| Command | Description |
|---------|-------------|
| `history` | Show last 8 calculations |
| `help` / `h` | Show all features |
| `clear` | Clear history |
| `quit` / `q` | Exit |


