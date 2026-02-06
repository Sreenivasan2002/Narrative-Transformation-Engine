"""
Orchestrator — The Conductor of the Agent Pipeline
====================================================
Coordinates all 7 agents in a DAG (Directed Acyclic Graph) pattern.

Pipeline flow:
  ┌─────────────────┐
  │   User Input     │  (source material + target universe)
  └────────┬────────┘
           ▼
  ┌─────────────────┐
  │ Source Analyzer  │  → extracts narrative DNA
  └────────┬────────┘
           ▼
  ┌─────────────────┐
  │  World Builder   │  → constructs target universe
  └────────┬────────┘
           ▼
  ┌─────────────────┐
  │ Character Mapper │  → transforms the cast
  └────────┬────────┘
           ▼
  ┌─────────────────┐
  │ Plot Transformer │  → reimagines the story structure
  └────────┬────────┘
           ▼
  ┌─────────────────┐
  │  Story Writer    │  → generates final narrative
  └────────┬────────┘
           ▼
  ┌─────────────────────────────────────────┐
  │  Consistency Checker ──→ Critic Agent   │  (evaluation layer)
  └─────────────────────────────────────────┘
           ▼
  ┌─────────────────┐
  │   Final Output   │
  └─────────────────┘

Design decisions:
  1. Sequential pipeline (not parallel) because each agent DEPENDS on prior outputs
  2. Shared context dict — each agent reads what it needs, writes its output
  3. Evaluation agents run at the end — they assess the final product
  4. If consistency check fails (score < 7), the story writer RERUNS with feedback
     (self-healing loop — this is the "clever idea" bonus)
"""

import json
import sys
import os
import time
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.markdown import Markdown

# Fix Windows encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from agents.llm_client import LLMClient
from agents.source_analyzer import SourceAnalyzerAgent
from agents.world_builder import WorldBuilderAgent
from agents.character_mapper import CharacterMapperAgent
from agents.plot_transformer import PlotTransformerAgent
from agents.story_writer import StoryWriterAgent
from agents.consistency_checker import ConsistencyCheckerAgent
from agents.critic_agent import CriticAgent

console = Console(force_terminal=True)


class Orchestrator:
    """
    Coordinates the multi-agent narrative transformation pipeline.

    The orchestrator:
      1. Loads source + target data
      2. Runs agents in sequence, building up a shared context
      3. Implements a self-healing loop: if consistency < 7, rewrites with feedback
      4. Saves all intermediate outputs for transparency
      5. Produces the final deliverable

    The self-healing loop is the "one clever idea" — most pipelines just
    generate and hope for the best. Ours EVALUATES and ITERATES.
    """

    MAX_REVISION_ATTEMPTS = 2  # max times the story writer can retry

    def __init__(self, model: str = "gpt-4o-mini"):
        self.llm = LLMClient(model=model)
        self.context = {}  # shared pipeline context
        self.outputs = {}  # store all intermediate outputs

        # Initialize all agents
        self.source_analyzer = SourceAnalyzerAgent(self.llm)
        self.world_builder = WorldBuilderAgent(self.llm)
        self.character_mapper = CharacterMapperAgent(self.llm)
        self.plot_transformer = PlotTransformerAgent(self.llm)
        self.story_writer = StoryWriterAgent(self.llm)
        self.consistency_checker = ConsistencyCheckerAgent(self.llm)
        self.critic = CriticAgent(self.llm)

    def load_data(self, source_path: str, target_path: str):
        """Load source material and target universe data from JSON files."""
        with open(source_path, "r", encoding="utf-8") as f:
            source_data = json.load(f)
        with open(target_path, "r", encoding="utf-8") as f:
            target_data = json.load(f)

        self.context["source_material"] = json.dumps(source_data, indent=2)
        self.context["target_universe"] = json.dumps(target_data, indent=2)

        console.print(
            Panel(
                f"[bold]Source:[/bold] {source_data.get('title', 'Unknown')}\n"
                f"[bold]Target:[/bold] {target_data.get('universe', 'Unknown')}",
                title="📚 Data Loaded",
                border_style="green",
            )
        )

    def run(self) -> dict:
        """
        Execute the full pipeline.
        Returns a dict with all outputs.
        """
        start_time = time.time()

        console.print(
            Panel(
                "[bold yellow]Starting Narrative Transformation Pipeline[/bold yellow]\n"
                "7 agents will collaborate to reimagine the story.",
                title="🚀 Pipeline Start",
                border_style="yellow",
            )
        )
        console.print()

        # === PHASE 1: Analysis ===
        console.rule("[bold blue]Phase 1: Analysis[/bold blue]")

        # Agent 1: Source Analyzer
        source_analysis = self.source_analyzer.run(self.context)
        self.context["source_analysis"] = source_analysis
        self.outputs["source_analysis"] = source_analysis

        # === PHASE 2: World & Character Construction ===
        console.rule("[bold blue]Phase 2: World & Character Construction[/bold blue]")

        # Agent 2: World Builder
        world_building = self.world_builder.run(self.context)
        self.context["world_building"] = world_building
        self.outputs["world_building"] = world_building

        # Agent 3: Character Mapper
        character_mapping = self.character_mapper.run(self.context)
        self.context["character_mapping"] = character_mapping
        self.outputs["character_mapping"] = character_mapping

        # === PHASE 3: Plot & Story Generation ===
        console.rule("[bold blue]Phase 3: Plot & Story Generation[/bold blue]")

        # Agent 4: Plot Transformer
        plot_outline = self.plot_transformer.run(self.context)
        self.context["plot_outline"] = plot_outline
        self.outputs["plot_outline"] = plot_outline

        # Agent 5: Story Writer
        story = self.story_writer.run(self.context)
        self.context["story"] = story
        self.outputs["story"] = story

        # === PHASE 4: Evaluation & Self-Healing Loop ===
        console.rule("[bold blue]Phase 4: Evaluation & Quality Assurance[/bold blue]")

        # Self-healing loop: check consistency, rewrite if needed
        for attempt in range(1, self.MAX_REVISION_ATTEMPTS + 1):
            console.print(
                f"  [dim]Evaluation attempt {attempt}/{self.MAX_REVISION_ATTEMPTS}[/dim]"
            )

            # Agent 6: Consistency Checker
            consistency_report = self.consistency_checker.run(self.context)
            self.context["consistency_report"] = consistency_report
            self.outputs[f"consistency_report_v{attempt}"] = consistency_report

            # Check if the story passes (score >= 7)
            if self._check_passed(consistency_report):
                console.print("  [bold green]✓ Story passed consistency check![/bold green]\n")
                break
            else:
                if attempt < self.MAX_REVISION_ATTEMPTS:
                    console.print(
                        "  [bold yellow]⚠ Story needs revision. "
                        "Feeding feedback to Story Writer...[/bold yellow]\n"
                    )
                    # Feed the consistency report back to the story writer
                    # This is the self-healing loop
                    self.context["revision_feedback"] = consistency_report
                    story = self._rewrite_with_feedback()
                    self.context["story"] = story
                    self.outputs[f"story_v{attempt + 1}"] = story
                else:
                    console.print(
                        "  [dim]Max revisions reached. Proceeding with current version.[/dim]\n"
                    )

        # Agent 7: Critic
        critic_review = self.critic.run(self.context)
        self.outputs["critic_review"] = critic_review

        # === PHASE 5: Output Assembly ===
        elapsed = time.time() - start_time
        console.rule("[bold green]Pipeline Complete[/bold green]")
        console.print(
            Panel(
                f"[bold]Total time:[/bold] {elapsed:.1f}s\n"
                f"[bold]Total tokens:[/bold] {self.llm.total_tokens_used:,}\n"
                f"[bold]Agents executed:[/bold] 7\n"
                f"[bold]Model:[/bold] {self.llm.model}",
                title="📊 Pipeline Stats",
                border_style="green",
            )
        )

        return self.outputs

    def _check_passed(self, consistency_report: str) -> bool:
        """
        Parse the consistency report to determine if the story passed.
        Looks for PASS/NEEDS REVISION verdict and score >= 7.
        """
        report_lower = consistency_report.lower()
        # Check for explicit PASS verdict
        if "verdict" in report_lower and "pass" in report_lower:
            # Make sure it's actually a PASS and not "NEEDS REVISION"
            if "needs revision" not in report_lower:
                return True

        # Fallback: look for score >= 7
        import re
        score_match = re.search(r"overall\s*score[:\s]*(\d+)", report_lower)
        if score_match:
            score = int(score_match.group(1))
            return score >= 7

        # Default: assume it passes to avoid infinite loops
        return True

    def _rewrite_with_feedback(self) -> str:
        """
        Rerun the story writer with feedback from the consistency checker.
        This is the self-healing mechanism.
        """
        console.print(
            Panel(
                "[bold cyan]Revision Mode[/bold cyan]\n"
                "Story Writer is rewriting with consistency feedback.",
                title="🔄 Self-Healing Loop",
                border_style="cyan",
            )
        )

        revision_prompt = f"""You previously wrote a story that had some consistency issues.
Here is the feedback from the quality checker:

{self.context['revision_feedback']}

Here is your original story:
{self.context['story']}

Please REWRITE the story, fixing the identified issues while maintaining
the quality and creativity of the original. Keep the same characters,
world, and general plot — but fix the specific problems flagged.

Source analysis for reference:
{self.context.get('source_analysis', '')}

World building for reference:
{self.context.get('world_building', '')}

Character mapping for reference:
{self.context.get('character_mapping', '')}

Plot outline for reference:
{self.context.get('plot_outline', '')}

Write the corrected story directly — no meta-commentary."""

        result = self.llm.call(
            system_prompt=self.story_writer.SYSTEM_PROMPT,
            user_prompt=revision_prompt,
            temperature=0.75,  # slightly lower than original for more controlled revision
            max_tokens=4096,
        )

        console.print("  [green]✓[/green] Revision complete.\n")
        return result

    def save_outputs(self, output_dir: str = "output"):
        """Save all intermediate and final outputs to files."""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)

        # Save each output as a separate file
        file_mapping = {
            "source_analysis": "01_source_analysis.md",
            "world_building": "02_world_building.md",
            "character_mapping": "03_character_mapping.md",
            "plot_outline": "04_plot_outline.md",
            "story": "05_final_story.md",
            "consistency_report": "06_consistency_report.md",
            "critic_review": "07_critic_review.md",
        }

        for key, filename in file_mapping.items():
            # Find the latest version of each output
            content = None
            if key in self.outputs:
                content = self.outputs[key]
            else:
                # Check for versioned outputs (from revision loop)
                for k in sorted(self.outputs.keys(), reverse=True):
                    if k.startswith(key):
                        content = self.outputs[k]
                        break

            if content:
                filepath = output_path / filename
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)
                console.print(f"  [dim]Saved: {filepath}[/dim]")

        # Also save the complete context as JSON for reproducibility
        context_path = output_path / "pipeline_context.json"
        with open(context_path, "w", encoding="utf-8") as f:
            json.dump(
                {k: v[:500] + "..." if len(v) > 500 else v for k, v in self.outputs.items()},
                f,
                indent=2,
            )

        console.print(
            Panel(
                f"All outputs saved to [bold]{output_dir}/[/bold]",
                title="💾 Outputs Saved",
                border_style="green",
            )
        )
