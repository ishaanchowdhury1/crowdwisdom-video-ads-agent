# CrowdWisdom Trading — Hermes Video Ads Agent

An end-to-end Python/Hermes agent pipeline for producing cinematic 30–60 second video ads for CrowdWisdomTrading.com.

## Architecture

```text
Hermes Kanban
   ├── Ads Manager → Apify Meta Ad Library → successful_ads.json
   ├── Marketing Analyzer → hooks / pains / ICP → marketing_analysis.json
   ├── Research Agent → Tavily/Exa (last 30 days) → research.json
   ├── Script Agent → 3 creative directions → ad_script_*.json
   └── Video Agent → OpenMontage manifest → final MP4
```

The implementation is intentionally **agent-first**: Hermes profiles own reasoning and stage decisions; Python supplies deterministic API adapters, JSON persistence, validation, and rendering helpers.

## Requirements

- Python 3.11–3.13
- Hermes Agent 0.18.1+
- Apify API token
- Tavily and/or Exa API token
- OpenRouter API key (or configure another Hermes-supported provider)
- FFmpeg for the local fallback renderer
- OpenMontage for the preferred production renderer

Hermes' current Apify integration supports Apify Actors through `apify_discover`, `apify_start`, and `apify_collect`; the plugin requires Hermes Agent 0.18.1+ and Python 3.11–3.13.

## Quick start

```bash
cp .env.example .env
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# install Hermes Agent separately if not already installed
pip install -U hermes-agent
pip install apify-hermes-agent-plugin
hermes plugins enable apify

# initialize a board
hermes kanban init

# inspect the pipeline
python -m src.main --help

# run with live services
python -m src.main run --days 30
```

If APIs are not configured, the pipeline can be demonstrated with the included fixture data:

```bash
python -m src.main demo
```

## Secrets

Never commit `.env`. The assignment asks for the Apify/Tavily/Exa credentials by email so the evaluator can rerun the code. Put them in the email, not GitHub. `.env.example` contains only placeholders.

## Outputs

- `data/ads/successful_ads.json`
- `data/research/marketing_analysis.json`
- `data/research/research.json`
- `data/scripts/ad_script_01.json` … `ad_script_03.json`
- `output/final_ad.mp4`
- `output/manifest.json`

## Creative direction

The included demo direction is **THE NOISE**: a trader is overwhelmed by conflicting market opinions, the noise collapses into silence, and the visual story resolves into collective intelligence from CrowdWisdom. The ad avoids generic “text ad” treatment and uses trading-floor motion, signal convergence, chart movement, and cinematic sound design.

## Important disclaimer

This project generates marketing content for an assessment. It must not imply guaranteed investment returns. Generated ads include an informational/educational disclaimer.
