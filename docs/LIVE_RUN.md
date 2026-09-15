# Live run checklist

1. Put real `OPENROUTER_API_KEY`, `APIFY_API_TOKEN`, `TAVILY_API_KEY` and/or `EXA_API_KEY` in `.env`.
2. Install Hermes Agent 0.18.1+ and the Apify Hermes plugin.
3. Run `hermes plugins enable apify` and verify with `hermes tools`.
4. Run `./run_hermes.sh` to create the Kanban cards.
5. Run `python -m src.main run --days 30`.
6. Use OpenMontage in its own checkout following its current setup/agent guide. The selected storyboard should be copied into an OpenMontage project under its canonical `projects/<project-id>/` layout.
7. Replace the deterministic fallback render with the OpenMontage final render before submitting.
