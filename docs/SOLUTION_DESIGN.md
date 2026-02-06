# Solution Design Document
## Narrative Transformation Engine — Mahabharata x GTA

---

## 1. Approach Diagram

```
                    ┌─────────────────────────────────┐
                    │         USER INPUT              │
                    │  Source: mahabharata.json       │
                    │  Target: gta_universe.json      │
                    └───────────────┬─────────────────┘
                                    │
                    ┌───────────────▼─────────────────┐
                    │       ORCHESTRATOR              │
                    │ (Pipeline Controller + Context) │
                    └───────────────┬─────────────────┘
                                    │
          ╔═════════════════════════╧═══════════════════════════╗
          ║              PHASE 1: ANALYSIS                      ║
          ╚═════════════════════════╤═══════════════════════════╝
                                    │
                    ┌───────────────▼─────────────────┐
                    │    AGENT 1: Source Analyzer     │
                    │    Temp: 0.3 (analytical)       │
                    │                                 │
                    │    IN:  Source material JSON    │
                    │    OUT: Narrative DNA           │
                    │         - Core themes           │
                    │         - Character archetypes  │
                    │         - Plot skeleton         │
                    │         - Emotional architecture│
                    │         - Symbolic elements     │
                    │         - Power dynamics        │
                    └───────────────┬─────────────────┘
                                    │
          ╔═════════════════════════╧═══════════════════════════╗
          ║         PHASE 2: WORLD & CHARACTER CONSTRUCTION     ║
          ╚═════════════════════════╤═══════════════════════════╝
                                    │
                    ┌───────────────▼─────────────────┐
                    │    AGENT 2: World Builder       │
                    │    Temp: 0.6 (creative+coherent)│
                    │                                 │
                    │    IN:  Target universe JSON    │
                    │         + Source analysis       │
                    │    OUT: Realized world with     │
                    │         - Power structures      │
                    │         - Social rules          │
                    │         - Key locations         │
                    │         - Conflict generators   │
                    └───────────────┬─────────────────┘
                                    │
                    ┌───────────────▼───────────────────┐
                    │    AGENT 3: Character Mapper      │
                    │    Temp: 0.7 (creative)           │
                    │                                   │
                    │    IN:  Source analysis           │
                    │         + World building          │
                    │         + Original character data │
                    │    OUT: Transformed characters    │
                    │         - New identities          │
                    │         - Preserved essences      │
                    │         - Signature traits        │
                    │         - Sample dialogue         │
                    └───────────────┬───────────────────┘
                                    │
          ╔═════════════════════════╧═══════════════════════════╗
          ║         PHASE 3: PLOT & STORY GENERATION            ║
          ╚═════════════════════════╤═══════════════════════════╝
                                    │
                    ┌───────────────▼─────────────────┐
                    │    AGENT 4: Plot Transformer    │
                    │    Temp: 0.7 (creative)         │
                    │                                 │
                    │    IN:  Source analysis         │
                    │         + World building        │
                    │         + Character mapping     │
                    │    OUT: Scene-by-scene outline  │
                    │         with source parallels   │
                    └───────────────┬─────────────────┘
                                    │
                    ┌───────────────▼─────────────────┐
                    │    AGENT 5: Story Writer        │
                    │    Temp: 0.85 (peak creativity) │
                    │                                 │
                    │    IN:  ALL previous outputs    │
                    │    OUT: Final narrative prose   │
                    │         (1500-2000 words)       │
                    └───────────────┬─────────────────┘
                                    │
          ╔═════════════════════════╧═══════════════════════════╗
          ║         PHASE 4: EVALUATION & SELF-HEALING          ║
          ╚═════════════════════════╤═══════════════════════════╝
                                    │
                    ┌───────────────▼─────────────────┐
                    │   AGENT 6: Consistency Checker  │
                    │   Temp: 0.2 (strict/analytical) │
                    │                                 │
                    │   IN:  Story + World rules      │
                    │        + Character specs        │
                    │   OUT: Issue report + score     │
                    │        PASS (>= 7) or FAIL      │
                    └───────────────┬─────────────────┘
                                    │
                              ┌─────▼──────┐
                              │ Score >= 7?│
                              └──┬─────┬───┘
                           Yes   │     │   No
                                 │     │
                                 │     └──────► Story Writer RERUNS
                                 │              with feedback
                                 │              (max 2 attempts)
                                 │              ──── Self-Healing Loop ────
                                 │
                    ┌────────────▼────────────────────┐
                    │    AGENT 7: Critic / Evaluator  │
                    │    Temp: 0.5 (balanced)         │
                    │                                 │
                    │    IN:  Final story + Source    │
                    │         + Consistency report    │
                    │    OUT: Quality assessment      │
                    │         - Storytelling quality  │
                    │         - Adaptation quality    │
                    │         - Specific feedback     │
                    └───────────────┬─────────────────┘
                                    │
                    ┌───────────────▼─────────────────┐
                    │        FINAL OUTPUT             │
                    │   output/05_final_story.md      │
                    │   + all intermediate artifacts  │
                    └─────────────────────────────────┘
```

---

## 2. Solution Design: How the System Works End-to-End

### Architecture: Sequential Agent Pipeline with Self-Healing

The system follows a **DAG (Directed Acyclic Graph)** pattern where 7 specialist agents execute in sequence, each building on the outputs of previous agents through a **shared context dictionary**.

**Key architectural decisions:**

1. **Shared Context Pattern**: A single Python dict flows through the pipeline. Each agent reads what it needs and writes its output back. This is simpler and more debuggable than message-passing between agents.

2. **Agent Abstraction**: Every agent inherits from `BaseAgent` with a standard contract: `build_prompt(context) -> str` and `run(context) -> str`. The orchestrator doesn't know or care about agent internals.

3. **Temperature Stratification**: Each agent has a calibrated temperature setting:
   - Analytical agents (Source Analyzer, Consistency Checker): 0.2-0.3
   - Construction agents (World Builder, Character Mapper, Plot Transformer): 0.6-0.7
   - Creative agent (Story Writer): 0.85
   - Evaluation agent (Critic): 0.5

4. **Self-Healing Loop** (the "clever idea"): After the Story Writer generates output, the Consistency Checker evaluates it. If the score is below 7/10, the story is automatically rewritten with the checker's feedback injected. This makes the system self-correcting — most pipelines just generate and hope for the best.

5. **Separation of Construction and Evaluation**: Agents 1-5 BUILD the story. Agents 6-7 EVALUATE it. This separation prevents the generator from grading its own homework.

### Data Flow

```
User Input → JSON files (source + target)
→ Source Analyzer extracts narrative DNA
→ World Builder constructs target universe (using DNA as constraints)
→ Character Mapper transforms the cast (using DNA + world)
→ Plot Transformer reimagines structure (using DNA + world + characters)
→ Story Writer generates prose (using ALL above)
→ Consistency Checker validates (against world rules + character specs)
→ [Optional: Story Writer revises with feedback]
→ Critic evaluates final quality
→ All outputs saved to output/ directory
```

---

## 3. Alternatives Considered

| Approach | Pros | Cons | Why Rejected |
|----------|------|------|--------------|
| **Single mega-prompt** | Simple, one API call | No structure, inconsistent, not reproducible | Can't control quality at each step |
| **Two-step (analyze + generate)** | Quick, fewer API calls | World-building is thin, characters lack depth | Not enough specialization |
| **Parallel agents** | Faster execution | Agents can't build on each other's work | Defeats the purpose of progressive context |
| **Fine-tuned model** | Potentially better quality | Expensive, not reproducible, overkill for demo | Doesn't demonstrate prompt engineering |
| **RAG with vector DB** | Could retrieve similar adaptations | Over-engineered for this scope, needs large dataset | Adds complexity without proportional value |
| **Our approach: 7-agent sequential pipeline** | Each agent specialized, outputs build progressively, self-healing loop catches errors | More API calls, slower | Best balance of quality, control, and demonstrable engineering |

### Prompting Strategy: Few-Shot vs. Structured Instructions

We chose **structured system prompts with explicit output formats** over few-shot prompting because:
- Few-shot examples for narrative transformation would be very long and token-expensive
- Structured formats (section headers, numbered lists) give more consistent outputs
- Each agent's system prompt acts as a detailed "job description" — the agent knows exactly what's expected

---

## 4. Challenges & Mitigations

### Challenge 1: Maintaining Thematic Coherence Across Agents
**Problem**: Each agent runs independently. Agent 5 might write a story that contradicts Agent 2's world rules.
**Mitigation**: The shared context dict passes ALL previous outputs forward. The Story Writer sees the world rules, character specs, AND plot outline — not just the plot.

### Challenge 2: Preventing "Re-Skinning" (Shallow Adaptation)
**Problem**: LLMs tend to just rename characters and locations without deeply reimagining the narrative.
**Mitigation**: The Plot Transformer's system prompt explicitly instructs "Transform FUNCTIONS, not events." It asks "What situation in THIS world would exploit the hero's sense of honor?" rather than "What's the GTA version of a dice game?"

### Challenge 3: Character Voice Consistency
**Problem**: In a generated story, all characters tend to sound the same.
**Mitigation**: The Character Mapper creates sample dialogue for each character. The Story Writer receives these voice samples as part of its context.

### Challenge 4: Output Quality Variance
**Problem**: LLM outputs vary between runs, sometimes producing lower quality.
**Mitigation**: The **self-healing loop** — if the Consistency Checker scores below 7/10, the Story Writer automatically revises with specific feedback. This converts a single-shot generation into an iterative refinement process.

### Challenge 5: Token Limits and Context Window
**Problem**: By Agent 5, the accumulated context is very large.
**Mitigation**: Each agent's `build_prompt()` selects only the context it NEEDS, not everything. The Source Analyzer's 4000-word output is compressed by the time it reaches the Story Writer.

---

## 5. Future Improvements

1. **Interactive Mode**: Let users intervene between agents — e.g., approve the character mapping before generating the story. Would make it a collaborative tool.

2. **Parallel Agent Execution**: World Builder and Character Mapper could run in parallel (both depend on Source Analysis but not on each other), cutting pipeline time by ~30%.

3. **Multi-Model Strategy**: Use GPT-4o for creative agents (Story Writer) and GPT-4o-mini for analytical agents (Consistency Checker) to optimize cost/quality.

4. **Template Library**: Store successful transformations as templates. "Mahabharata → GTA" becomes a reusable pattern for "any epic → any crime universe."

5. **API/Web Interface**: Wrap the pipeline in a FastAPI server with a React frontend. Users pick source + target from dropdowns, watch agents work in real-time via WebSocket.

6. **Human-in-the-Loop Evaluation**: Add a step where human feedback is collected and used to fine-tune the system prompts over time (RLHF-lite).

7. **Multi-Language Support**: Generate the reimagined story in multiple languages — the plot/character artifacts are language-agnostic.

8. **Version Control for Narratives**: Track how the story evolves across revision attempts, building a "diff" view of creative changes.
