"""
Agent 7: Critic / Evaluator
============================
Responsibility: Final quality assessment from a READER's perspective.
Unlike the Consistency Checker (which is technical QA), the Critic
evaluates the story as a piece of creative writing.

Why this agent exists:
  A story can be perfectly consistent yet boring. A story can follow all
  the rules yet lack emotional impact. The Critic evaluates:
  - Is it a GOOD story? Would someone want to read it?
  - Does the adaptation add value? (Not just "the same story but reskinned")
  - Is it clever? Does the mapping feel inspired or obvious?

  This agent represents the EVALUATOR mentioned in the assignment rubric.
  It provides the self-assessment that shows we thought critically about output quality.

Design note: Medium temperature (0.5) — balanced judgment, not too rigid
or too creative. The Critic needs to be fair but honest.
"""

from agents.base_agent import BaseAgent


class CriticAgent(BaseAgent):
    NAME = "Critic & Evaluator"
    ROLE = "Final quality assessment from a reader and evaluator perspective"

    SYSTEM_PROMPT = """You are a literary critic and creative adaptation expert.

Your job is to evaluate the FINAL OUTPUT of a narrative transformation system.
You evaluate it from TWO perspectives:

PERSPECTIVE 1 — AS A READER:
Would someone enjoy reading this story on its own merit?
- Is the prose engaging?
- Are the characters compelling?
- Does the plot hook you?
- Is the world vivid?
- Does the ending land?

PERSPECTIVE 2 — AS AN ADAPTATION EVALUATOR:
How well does this transformation work?
- Does it preserve the ESSENCE of the source material?
- Is the mapping between source and target worlds clever and organic?
- Does the new setting add something to the story (not just re-skin it)?
- Are the parallels satisfying for someone who knows the source?
- Can someone who DOESN'T know the source enjoy it as a standalone?

Provide your evaluation in this format:

**STORYTELLING QUALITY** (rate 1-10, explain)
- Prose quality
- Character depth
- Plot engagement
- World immersion
- Emotional impact

**ADAPTATION QUALITY** (rate 1-10, explain)
- Thematic fidelity
- Creative mapping
- World integration
- Added value beyond re-skinning
- Standalone readability

**STANDOUT MOMENTS** — 2-3 specific moments that work especially well

**AREAS FOR IMPROVEMENT** — 2-3 specific suggestions

**OVERALL VERDICT** — A final 2-3 sentence assessment

Be honest and specific. Praise what works. Critique what doesn't.
Reference specific passages when possible."""

    def build_prompt(self, context: dict) -> str:
        source_data = context.get("source_material", "")
        story = context.get("story", "")
        consistency_report = context.get("consistency_report", "")

        return f"""Evaluate this reimagined narrative.

ORIGINAL SOURCE MATERIAL (for comparison):
{source_data}

GENERATED STORY:
{story}

CONSISTENCY CHECK RESULTS (for context):
{consistency_report}

Provide your honest critical evaluation as both a reader and an adaptation expert."""

    def _get_temperature(self) -> float:
        return 0.5

    def _get_max_tokens(self) -> int:
        return 2500
