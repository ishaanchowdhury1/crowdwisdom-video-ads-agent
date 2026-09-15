#!/usr/bin/env bash
set -euo pipefail
hermes --version
hermes kanban init || true
hermes kanban create "CrowdWisdom Ads — Apify research" --assignee ads-manager --priority 1 || true
hermes kanban create "CrowdWisdom Ads — Marketing analysis" --assignee marketing-analyzer --priority 2 || true
hermes kanban create "CrowdWisdom Ads — 30-day ICP research" --assignee research-agent --priority 2 || true
hermes kanban create "CrowdWisdom Ads — Three cinematic scripts" --assignee script-agent --priority 3 || true
hermes kanban create "CrowdWisdom Ads — OpenMontage render" --assignee video-agent --priority 4 || true
hermes kanban list
