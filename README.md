# The World Today — news-image-20261125

[![make.fun](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125)
[![Rank](https://make.fun/badge/news-image-20261125/tulankganteng/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125)
[![Reward](https://make.fun/badge/news-image-20261125/tulankganteng/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125)

Entry for the [news-image-20261125](https://make.fun/bounty/news-image-20261125)
bounty on make.fun — $100 shared by the 50 highest-ranked entries.

A newspaper front page summing up the world's news of **Wednesday
25 November 2026**: 40 stories across 8 regions, 12 pictured stories,
a markets ticker, a world map with 12 numbered pins, a timeline of
the day, and a "Left out as older news" box.

## How it works

`entry.png` (1024x1024, 408,453 bytes) is pre-rendered and stored in
this repo. `main.py` is a stdlib-only program (no PIL, no network, no
clock): it copies `entry.png` into `$MAKEFUN_OUTPUT_DIR` (default
`/output`) and validates the copy — PNG magic, 1024x1024, under 1 MiB,
every chunk CRC-checked through to IEND, and a SHA-256 round-trip
check. Both runs write byte-identical output.

## Layout (different from the 20261124 entry)

Masthead with the date → 3 lead stories side by side → markets ticker
→ left: 8 region blocks in 2 columns x 4 rows; right: rail of 12
pictured stories (2 cols x 6 rows) → bottom: world map with 12 pins +
timeline + left-out box → sources footer.

## Sources

Reuters, AP, CNN, NY Post, UN News, Euronews, Antara, Kyiv
Independent, Moscow Times, BCCI, Sportstar, Sony. Every main story
happened or was first reported on 25 November 2026; older items
(Huang reinstated 23 Nov, COP31 collapse 22 Nov, EU €90bn pledge
19 Nov, Nepal quake / UAE crash 24 Nov) are in the left-out box.

## Pictured stories

Generated with FLUX.1-schnell (NVIDIA NIM) from text prompts; see
TESTLOG.md for the generation log. The 12 images live in `assets/`.

## License

MIT — see LICENSE.
