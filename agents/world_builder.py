"""
Agent 2: World Builder
======================
Responsibility: Construct the rules, logic, and texture of the TARGET universe.
Takes the target universe description and fleshes it out into a coherent world
with internal consistency.

Why this agent exists:
  A reimagined story fails if the new world feels like a thin skin over the
  original. The world needs its OWN logic — economics, power structures,
  technology, culture — that naturally creates the SAME types of conflicts
  as the source material, without forcing them.

  Example: In Mahabharata, the dice game works because gambling is a
  kshatriya (warrior) obligation. In GTA, it works because underground
  casinos are where power brokers make deals. The MECHANISM changes but
  the FUNCTION (a trap that exploits the hero's code of honor) stays.

Design note: Medium temperature (0.6) — creative but coherent.
"""

from agents.base_agent import BaseAgent


class WorldBuilderAgent(BaseAgent):
    NAME = "World Builder"
    ROLE = "Constructs the target universe with coherent internal rules"

    SYSTEM_PROMPT = """You are a world-building expert who creates internally consistent fictional universes.

Your job is to take a target universe concept and flesh it out into a FULLY REALIZED WORLD
that can naturally support the narrative elements that will be transplanted into it.

Critical requirement: The world must feel ORGANIC, not forced. Don't just re-skin the
source material — create a world where the equivalent conflicts, power struggles, and
emotional dynamics would NATURALLY arise.

Output the following sections:

1. **WORLD OVERVIEW** — The setting in vivid detail. Geography, atmosphere, social structure.
   Make it feel lived-in.

2. **POWER STRUCTURE** — Who runs this world? What are the factions? How is power gained,
   held, and lost? This MUST create natural analogues for the source story's conflicts.

3. **SOCIAL RULES** — What does this society value? What's taboo? What codes of honor exist?
   These rules must create the same types of moral dilemmas as the source.

4. **TECHNOLOGY & TOOLS** — What tech/tools exist? How do they shape conflict and communication?
   Map these to the weapons, vehicles, and artifacts of the source.

5. **KEY LOCATIONS** — 5-7 locations that will serve as stages for the reimagined plot.
   Each location should have a function in the story.

6. **WORLD-SPECIFIC CONFLICT GENERATORS** — What unique features of THIS world create
   tension, danger, and moral grey areas? These should naturally produce situations
   analogous to the source material's key conflicts.

7. **TONE & AESTHETIC** — The sensory experience of this world. Colors, sounds, rhythms.

Make this world feel like it could exist independently of any story — a place where
MANY stories could happen, and our reimagined narrative is just one of them."""

    def build_prompt(self, context: dict) -> str:
        target_universe = context.get("target_universe", "")
        source_analysis = context.get("source_analysis", "")

        return f"""Build a fully realized version of the following target universe.

TARGET UNIVERSE CONCEPT:
{target_universe}

The world you build must be able to NATURALLY support the following narrative elements
(extracted from the source material). Don't force-fit them — create a world where
equivalent conflicts would organically arise:

SOURCE MATERIAL ANALYSIS (for reference — what the world needs to support):
{source_analysis}

Build this world with internal consistency and vivid detail."""

    def _get_temperature(self) -> float:
        return 0.6

    def _get_max_tokens(self) -> int:
        return 4000
