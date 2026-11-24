# THE WORLD TODAY — Monday 23 November 2026

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/akbare12/news-23-b100-front-page-dense/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/akbare12/news-23-b100-front-page-dense/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

One image summing up 23 November 2026's world news: 31 stories across 6 regions.

## The day

- **AI rout hits Asia** — Kospi −3.3% to 4,708.54, sheds 161 pts; intraday −5.8%. Samsung −3.1%, SK Hynix −2.5%.
- **Guterres: regulate AI before it's too late** — Bridgetown summit; 150 delegates back a risk framework (blueprint, not treaty).
- **US lead over China at record low** — Asia Power Index 2026: US 78.9, China 73.6, gap 5.3, narrowest since 2018. India third at 40.5.

Plus 10 more stories, an 18-item ALSO list, a world map with numbered pins, and a DATE CHECK box that keeps 22/21/19 November stories out of the 23 November record.

## Build

`draw.py` (PIL) renders `entry.png` (1024×1024, < 1 MiB). `main.py` (stdlib only) validates the PNG and copies it to `$MAKEFUN_OUTPUT_DIR/entry.png`:

```sh
python3 draw.py
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Chips: REPORTED = confirmed by wires. CLAIM = one side's claim, not independently confirmed. ONGOING = still developing. Scenes are drawn illustrations, not photographs.
