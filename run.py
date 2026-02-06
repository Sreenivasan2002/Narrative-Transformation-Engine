#!/usr/bin/env python3
"""
Narrative Transformation System — Main Entry Point
====================================================
An agentic AI pipeline that reimagines classic stories in new universes.

Usage:
    python run.py                          # Default: Mahabharata → GTA
    python run.py --source data/custom.json --target data/custom_world.json
    python run.py --model gpt-4o           # Use a different model

Architecture:
    7 specialist agents orchestrated in a sequential pipeline with a
    self-healing feedback loop:

    Source Analyzer → World Builder → Character Mapper → Plot Transformer
    → Story Writer → Consistency Checker (→ rewrite if fails) → Critic

Author: Sreenivasan
"""

import argparse
import sys
import os
from pathlib import Path

# Fix Windows console encoding for Unicode/emoji support
if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

# Ensure the project root is in the path
sys.path.insert(0, str(Path(__file__).parent))

from agents.orchestrator import Orchestrator

console = Console()


def print_banner():
    """Print a stylish startup banner."""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     🎭  NARRATIVE TRANSFORMATION ENGINE  🎭                 ║
║                                                              ║
║     Reimagining Classic Stories in New Universes             ║
║     Powered by Multi-Agent AI Pipeline                       ║
║                                                              ║
║     Source: Mahabharata (Ancient Indian Epic)                ║
║     Target: GTA (Grand Theft Auto Universe)                  ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """
    console.print(banner, style="bold cyan")


def print_story(outputs: dict):
    """Display the final story in a formatted panel."""
    story = outputs.get("story", "No story generated.")
    console.print()
    console.rule("[bold magenta]📖 THE REIMAGINED STORY[/bold magenta]")
    console.print()
    console.print(Markdown(story))
    console.print()
    console.rule("[bold magenta]END[/bold magenta]")


def print_evaluation(outputs: dict):
    """Display evaluation results."""
    console.print()
    console.rule("[bold yellow]📊 EVALUATION RESULTS[/bold yellow]")
    console.print()

    # Consistency Report
    consistency = None
    for key in sorted(outputs.keys(), reverse=True):
        if key.startswith("consistency_report"):
            consistency = outputs[key]
            break

    if consistency:
        console.print(
            Panel(
                Markdown(consistency),
                title="🔍 Consistency Check",
                border_style="blue",
            )
        )

    # Critic Review
    critic = outputs.get("critic_review")
    if critic:
        console.print(
            Panel(
                Markdown(critic),
                title="⭐ Critic Review",
                border_style="yellow",
            )
        )


def main():
    parser = argparse.ArgumentParser(
        description="Narrative Transformation Engine — Reimagine stories across universes",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run.py                              # Default: Mahabharata → GTA
  python run.py --model gpt-4o              # Use GPT-4o for higher quality
  python run.py --source data/my_story.json --target data/my_world.json
  python run.py --show-intermediate          # Show all agent outputs
        """,
    )

    parser.add_argument(
        "--source",
        type=str,
        default="data/mahabharata.json",
        help="Path to source material JSON (default: data/mahabharata.json)",
    )
    parser.add_argument(
        "--target",
        type=str,
        default="data/gta_universe.json",
        help="Path to target universe JSON (default: data/gta_universe.json)",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="gpt-4o-mini",
        help="OpenAI model to use (default: gpt-4o-mini)",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="output",
        help="Directory to save outputs (default: output/)",
    )
    parser.add_argument(
        "--show-intermediate",
        action="store_true",
        help="Display all intermediate agent outputs",
    )

    args = parser.parse_args()

    # --- Startup ---
    print_banner()

    # Validate files exist
    if not Path(args.source).exists():
        console.print(f"[bold red]Error:[/bold red] Source file not found: {args.source}")
        sys.exit(1)
    if not Path(args.target).exists():
        console.print(f"[bold red]Error:[/bold red] Target file not found: {args.target}")
        sys.exit(1)

    # --- Initialize and Run ---
    orchestrator = Orchestrator(model=args.model)
    orchestrator.load_data(args.source, args.target)

    console.print()
    outputs = orchestrator.run()

    # --- Display Results ---
    if args.show_intermediate:
        for key in ["source_analysis", "world_building", "character_mapping", "plot_outline"]:
            if key in outputs:
                title = key.replace("_", " ").title()
                console.print(
                    Panel(Markdown(outputs[key]), title=f"📋 {title}", border_style="dim")
                )
                console.print()

    print_story(outputs)
    print_evaluation(outputs)

    # --- Save Outputs ---
    orchestrator.save_outputs(args.output_dir)

    console.print()
    console.print(
        Panel(
            "[bold green]Pipeline completed successfully![/bold green]\n\n"
            f"📁 All outputs saved to [bold]{args.output_dir}/[/bold]\n"
            f"📖 Final story: [bold]{args.output_dir}/05_final_story.md[/bold]\n"
            f"📊 Evaluation: [bold]{args.output_dir}/07_critic_review.md[/bold]",
            title="✅ Done",
            border_style="green",
        )
    )


if __name__ == "__main__":
    main()
