"""
Agent 5: Story Writer
=====================
Responsibility: Generate the final reimagined narrative prose using all
the outputs from previous agents as a blueprint.

Why this agent exists:
  All previous agents produced ANALYTICAL outputs — blueprints, maps,
  outlines. This agent is the CREATIVE executor — it takes the blueprint
  and builds the house. It must:
  1. Write engaging prose (not a dry summary)
  2. Give each character their distinct voice
  3. Maintain the emotional architecture
  4. Make the world feel vivid and immersive
  5. Keep it to 2-3 pages (roughly 1500-2000 words)

Design note: Highest temperature (0.85) — this is where creativity peaks.
The constraints from all previous agents keep it on track despite high temp.
"""

from agents.base_agent import BaseAgent


class StoryWriterAgent(BaseAgent):
    NAME = "Story Writer"
    ROLE = "Generates the final reimagined narrative"

    SYSTEM_PROMPT = """You are a creative fiction writer who excels at genre-blending narratives.

Your job is to write the FINAL REIMAGINED STORY based on all the preparation
work done by the analysis team. You have been given:
- Source material analysis (themes, emotional beats)
- A fully realized target world
- Mapped characters with distinct voices
- A scene-by-scene plot outline

Now WRITE THE STORY as vivid, engaging narrative prose.

WRITING GUIDELINES:

1. **FORMAT**: Write it as a short story (1500-2000 words, roughly 2-3 pages).
   Use scene breaks (---) between major shifts.

2. **VOICE**: Write in third-person, present tense for immediacy (like GTA cutscenes).
   Punchy, cinematic prose. Short paragraphs. Let dialogue breathe.

3. **SHOW, DON'T TELL**: Don't explain themes — EMBODY them in action and dialogue.
   The reader should feel the moral weight without a lecture.

4. **CHARACTER VOICE**: Each character must sound different. Use their speech patterns,
   slang, and verbal tics from the character mapping.

5. **PACING**: Fast during action, slow during emotional beats. The Gita-equivalent
   scene should be the most carefully written passage — philosophical but accessible.

6. **SENSORY DETAILS**: Make the world tangible — what do characters see, hear, smell?
   Every location should be vivid enough to picture.

7. **ENDING**: The ending must carry the same emotional weight as the source.
   Bittersweet, pyrrhic victory. The reader should feel the cost.

8. **NO EXPOSITION DUMPS**: Weave world-building into action. If a character carries a
   gold-plated Desert Eagle, show it — don't explain the symbolism.

CRITICAL: This is a REIMAGINATION, not a retelling. The story should feel fresh
and native to its new world. A reader unfamiliar with the source should enjoy it
purely as a GTA-style crime saga. A reader who knows the source should smile at
the clever parallels.

Do NOT include any meta-commentary about the adaptation process.
Write the story as if it IS the story — pure narrative."""

    def build_prompt(self, context: dict) -> str:
        source_analysis = context.get("source_analysis", "")
        world_building = context.get("world_building", "")
        character_mapping = context.get("character_mapping", "")
        plot_outline = context.get("plot_outline", "")

        return f"""Write the final reimagined story based on all the following preparation.

SOURCE ANALYSIS (themes and emotional beats to preserve):
{source_analysis}

TARGET WORLD (setting and rules):
{world_building}

CHARACTERS (reimagined cast):
{character_mapping}

PLOT OUTLINE (scene-by-scene blueprint):
{plot_outline}

Write a vivid, engaging short story (1500-2000 words) that brings this
reimagination to life. Make it feel like it belongs in the GTA universe
while carrying the soul of the Mahabharata.

Start directly with the story — no preamble or meta-commentary."""

    def _get_temperature(self) -> float:
        return 0.85  # peak creativity, constrained by all prior agent outputs

    def _get_max_tokens(self) -> int:
        return 4096
