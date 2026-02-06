# Narrative Transformation Engine

### Reimagining the Mahabharata in the Grand Theft Auto Universe

> *"What kind of person in a GTA crime world would face the same dilemmas as Arjuna on the battlefield of Kurukshetra?"*

An agentic AI pipeline that systematically transforms classic narratives into new universes — preserving emotional DNA while reimagining every surface detail.

---

## The Concept

**Source:** Mahabharata — the ancient Indian epic of family, duty, betrayal, and the cost of war.

**Target:** Grand Theft Auto — a neon-lit crime universe of gang wars, moral ambiguity, and the pursuit of power.

**Why this works:** Both worlds orbit the same themes — loyalty weaponized into tragedy, power that corrupts everyone who touches it, and victories that feel like defeats. The Mahabharata's Hastinapura becomes San Hastina, a corrupt metropolis. The dice game becomes a rigged casino night. Kurukshetra becomes a city-wide gang war. Krishna becomes the mysterious fixer who knows too much.

---

## Architecture

Seven specialist AI agents collaborate in a sequential pipeline, each building on the previous agent's work:

```
┌──────────────┐   ┌──────────────┐   ┌──────────────────┐   ┌──────────────────┐
│   Source     │──▶│    World     │──▶│    Character    │──▶│      Plot       │
│   Analyzer   │   │    Builder   │   │    Mapper        │   │    Transformer   │
│   (temp 0.3) │   │   (temp 0.6) │   │    (temp 0.7)    │   │    (temp 0.7)    │
└──────────────┘   └──────────────┘   └──────────────────┘   └──────────────────┘
       │                                                              │
       │              Narrative DNA flows forward ─────────────────▶ │
       │                                                              ▼
       │                                                    ┌──────────────────┐
       │                                                    │   Story Writer   │
       │                                                    │   (temp 0.85)    │
       │                                                    └────────┬─────────┘
       │                                                             │
       │            ┌────────────────────────────────────────────────┘
       │            ▼
       │   ┌──────────────────┐        ┌──────────────────┐
       │   │   Consistency    │──┐     │   Critic /       │
       │   │   Checker        │  │     │   Evaluator      │
       │   │   (temp 0.2)     │  │     │   (temp 0.5)     │
       │   └──────────────────┘  │     └──────────────────┘
       │            │            │              ▲
       │       Score < 7?        │              │
       │            │            │     Score >= 7 → proceed
       │            ▼            │              │
       │   ┌──────────────┐      │              │
       │   │ Self-Healing │──────┘──────────────┘
       │   │ Rewrite Loop │
       │   └──────────────┘
```

### The Clever Idea: Self-Healing Loop

Most AI pipelines are fire-and-forget. Ours **evaluates its own output** and **rewrites if quality is insufficient**. The Consistency Checker scores the story against world rules and character specs — if it scores below 7/10, the Story Writer automatically revises with the checker's specific feedback injected as guidance.

---

## Quick Start

### Prerequisites

- Python 3.10+
- OpenAI API key

### Setup

```bash
# Clone and enter the project
cd pratilipi

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Configure

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your-api-key-here
```

### Run

```bash
# Default: Mahabharata → GTA Universe
python run.py

# Use a more powerful model
python run.py --model gpt-4o

# Show all intermediate agent outputs
python run.py --show-intermediate

# Custom source and target
python run.py --source data/custom_source.json --target data/custom_target.json
```

---

## Project Structure

```
pratilipi/
├── run.py                      # Main entry point
├── requirements.txt            # Python dependencies
├── .env                        # API keys (gitignored)
│
├── agents/                     # The 7-agent pipeline
│   ├── __init__.py
│   ├── llm_client.py           # Centralized LLM interface
│   ├── base_agent.py           # Abstract agent contract
│   ├── orchestrator.py         # Pipeline controller + self-healing loop
│   ├── source_analyzer.py      # Agent 1: Deconstructs source material
│   ├── world_builder.py        # Agent 2: Builds target universe
│   ├── character_mapper.py     # Agent 3: Transforms characters
│   ├── plot_transformer.py     # Agent 4: Reimagines plot structure
│   ├── story_writer.py         # Agent 5: Generates narrative prose
│   ├── consistency_checker.py  # Agent 6: QA — validates consistency
│   └── critic_agent.py         # Agent 7: Final quality evaluation
│
├── data/                       # Source material & target universes
│   ├── mahabharata.json        # Mahabharata narrative data
│   └── gta_universe.json       # GTA universe specifications
│
├── output/                     # Generated outputs (after running)
│   ├── 01_source_analysis.md
│   ├── 02_world_building.md
│   ├── 03_character_mapping.md
│   ├── 04_plot_outline.md
│   ├── 05_final_story.md       # The reimagined story
│   ├── 06_consistency_report.md
│   ├── 07_critic_review.md
│   └── pipeline_context.json
│
└── docs/
    └── SOLUTION_DESIGN.md      # Architecture, alternatives, trade-offs
```

---

## Agent Deep Dive

| Agent | Role | Temperature | Why This Setting |
|-------|------|-------------|------------------|
| **Source Analyzer** | Extracts narrative DNA — themes, archetypes, emotional beats | 0.3 | Analytical task; needs consistency, not creativity |
| **World Builder** | Constructs the GTA universe with coherent internal rules | 0.6 | Creative but must stay internally consistent |
| **Character Mapper** | Transforms Mahabharata characters into GTA equivalents | 0.7 | Needs creative mapping while preserving essence |
| **Plot Transformer** | Reimagines the story structure scene-by-scene | 0.7 | Creative but must follow the emotional architecture |
| **Story Writer** | Generates the final narrative prose | 0.85 | Peak creativity — constrained by all prior outputs |
| **Consistency Checker** | Validates story against world rules and character specs | 0.2 | Must be pedantic and strict; QA, not creative |
| **Critic** | Final quality assessment from reader + evaluator perspective | 0.5 | Balanced — needs both analytical rigor and creative judgment |

---

## Character Mapping Preview

| Mahabharata | GTA Universe | Why It Works |
|-------------|--------------|--------------|
| **Yudhishthira** | Eldest son, rightful heir to Kuru Corp | Honor-bound leader whose rules are weaponized against him |
| **Arjuna** | Elite enforcer / best shooter | Moral crisis before the final mission |
| **Bhima** | The muscle, feared by everyone | Raw power, rage as both weapon and weakness |
| **Draupadi** | The woman whose humiliation starts the war | Her demand for justice drives the entire narrative |
| **Duryodhana** | Ambitious cousin who seizes the empire | Charismatic villain who genuinely believes he's right |
| **Karna** | Kid from the streets, fights for the wrong side | Most tragic character — loyalty over blood |
| **Krishna** | The Fixer — strategist, manipulator, philosopher | The one who sees the whole board |
| **Shakuni** | The uncle, master schemer | Every manipulation traced back to him |
| **Bhishma** | The old guard, bound by oath to the wrong side | Institutional loyalty vs. moral truth |

---

## Design Decisions

### Why Sequential, Not Parallel?
Each agent DEPENDS on prior outputs. The Character Mapper can't work without the World Builder's output. Sequential with shared context > parallel with incomplete information.

### Why Separate Construction and Evaluation?
Agents 1-5 BUILD. Agents 6-7 JUDGE. The generator should never grade its own homework. This separation ensures honest quality assessment.

### Why JSON Data Files?
Source material and target universes are stored as structured JSON, not hardcoded. This makes the system **reusable** — swap `mahabharata.json` for `hamlet.json` and `gta_universe.json` for `cyberpunk.json` to get a completely different transformation.

### Why Temperature Stratification?
Different tasks need different creativity levels. A consistency checker that's "creative" defeats its purpose. A story writer that's "analytical" produces flat prose. Calibrated temperatures give each agent the right balance.

---

## Extending the System

### Add a New Source Story

Create a JSON file in `data/` following this structure:

```json
{
  "title": "Your Story",
  "core_themes": ["theme1", "theme2"],
  "emotional_essence": "One paragraph capturing the soul of the story",
  "central_conflict": "The main tension",
  "major_characters": [
    {
      "name": "Character Name",
      "role": "Their function",
      "traits": ["trait1", "trait2"],
      "arc": "Their journey",
      "key_flaw": "Their fatal weakness"
    }
  ],
  "key_plot_points": [
    {
      "event": "Event Name",
      "description": "What happens",
      "emotional_weight": "How it should feel"
    }
  ]
}
```

### Add a New Target Universe

```json
{
  "universe": "Universe Name",
  "setting": {
    "city": "Location",
    "description": "The world in detail",
    "era": "Time period",
    "tone": "Emotional/aesthetic tone"
  },
  "world_rules": ["rule1", "rule2"],
  "genre_conventions": ["convention1", "convention2"]
}
```

Then run:
```bash
python run.py --source data/your_story.json --target data/your_universe.json
```

---

## Built With

- **Python 3.10+** — Core language
- **OpenAI API** — LLM provider (GPT-4o-mini default, GPT-4o supported)
- **Rich** — Terminal UI with colored output and panels
- **Pydantic** — Data validation
- **python-dotenv** — Environment configuration

---

