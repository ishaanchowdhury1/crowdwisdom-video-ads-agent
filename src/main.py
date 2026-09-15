import argparse, json, subprocess, sys
from pathlib import Path
from .utils import write_json, read_json
from .config import settings
from .validators import validate_script

ROOT = Path(__file__).resolve().parents[1]


def hermes(prompt: str):
    """Run a Hermes CLI task. Creative decisions live in Hermes profiles/prompts."""
    cmd = ["hermes", "-p", prompt]
    return subprocess.run(cmd, cwd=ROOT, check=True, text=True)


def demo():
    """Create a complete assessment-ready artifact set without paid API calls."""
    ads = read_json(ROOT / "data/ads/fixture_ads.json")
    write_json(ROOT / "data/ads/successful_ads.json", ads)
    analysis = read_json(ROOT / "data/research/fixture_analysis.json")
    write_json(ROOT / "data/research/marketing_analysis.json", analysis)
    research = read_json(ROOT / "data/research/fixture_research.json")
    write_json(ROOT / "data/research/research.json", research)
    for i in range(1, 4):
        src = ROOT / f"data/scripts/fixture_ad_{i:02d}.json"
        dst = ROOT / f"data/scripts/ad_script_{i:02d}.json"
        dst.write_text(src.read_text())
        validate_script(dst)
    print("Demo artifacts generated. Run: python tools/render_demo.py")


def run(days: int):
    prompt = f"""You are the lead Hermes agent for the CrowdWisdomTrading video ads assessment. Run the project pipeline for the last {days} days. Use the ads-manager, marketing-analyzer, research-agent, script-agent and video-agent profiles in profiles/. Use Apify for recent successful ads, Tavily or Exa for recent ICP/pain research, save all intermediate JSON artifacts under data/, generate three storyboard JSON files, and hand the best concept to OpenMontage. Never expose API keys in files or logs. Keep investment claims factual and include an educational disclaimer. Work through the Hermes Kanban board and leave a clear completion summary."""
    hermes(prompt)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("demo")
    r = sub.add_parser("run")
    r.add_argument("--days", type=int, default=30)
    args = parser.parse_args()
    if args.cmd == "demo": demo()
    else: run(args.days)
