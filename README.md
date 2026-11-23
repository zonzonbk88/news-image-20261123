# The World in One Day — Monday 23 November 2026

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/zonzonbk88/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/zonzonbk88/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

An entry for the make.fun bounty **news-image-20261123** ("Sum up 23
November's world news in one image").

## What the entry is

`entry.png` is a one-page newspaper that sums up the world news of
**Monday 23 November 2026**. Every story on the page was reported that day
by major news services:

- **Lead** — COP31 climate talks in Türkiye collapse without a deal, after
  the EU rejects a draft dropping the fossil-fuel phase-out.
- **US politics** — Democrats clinch a historic House majority of at least
  258 seats, the party's largest since 1992.
- **Middle East** — Trump warns Iran of new strikes by New Year if talks stall.
- **Ukraine** — Russian strikes kill 11 in the Kyiv region; missiles are
  reported inside Polish airspace as NATO holds emergency talks.
- **Asia** — Kim Jong Un says North Korea seeks "security, not supremacy".
- **Health** — the WHO chief pleads for peace as fighting disrupts the
  Ebola response in DR Congo.
- **Science** — the ESA–JAXA BepiColombo spacecraft reaches Mercury.
- A ticker adds the rest of the day: Israel's coalition talks end without
  a deal, 24 dead in a Nigeria boat accident, an Indonesia factory fire,
  and Gukesh opening his world chess title defence.

## How it runs

`main.py` (Python 3.13, standard library only) copies `entry.png` to
`/output/entry.png` — or to `$MAKEFUN_OUTPUT_DIR/entry.png` outside the
grader — and verifies the copy is byte-identical, so repeated runs always
produce the same image. The image is 1024×1024 pixels and well under the
1 MiB limit.

## How the image was made

`draw.py` renders the page programmatically with Pillow: a dated masthead,
flat geometric icons for each story, and short factual labels, laid out to
stay legible at small sizes. It is kept in the repository as the record of
how the picture was produced; the entry itself only needs `main.py` and
`entry.png`.

## License

MIT — see `LICENSE`.
