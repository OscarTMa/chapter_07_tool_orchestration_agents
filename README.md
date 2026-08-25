# Chapter 07: Tool Manipulation and Orchestration Agents

This module implements the third triad of AI agents described in *30 Agents Every AI Engineer Must Build* (Chapter 7). It covers how single and multi-agent systems translate abstract natural language reasoning into grounded, real-world execution through tool invocation, multi-specialist orchestration, and resilient business process state machines.

---

## Agent Architecture and State Workflows

```mermaid
flowchart TD
    %% ==========================================
    %% 1. AGENT 07: THE TOOL-USING AGENT
    %% ==========================================
    T1["1. User Request / Goal"]
    T2["Reasoning Core: Think & Plan"]
    T3[("Tool Registry & Schema Contracts")]
    T4["Execution Engine: Act"]
    T5["Guarded Tool Chest (CSV / Agg / Plot)"]
    T6["Rendered Asset Output"]

    T1 --> T2
    T2 --> T3
    T3 --> T4
    T4 --> T5
    T5 --> T6

    %% Conexión vertical hacia el Agente 08
    T6 --> O1

    %% ==========================================
    %% 2. AGENT 08: CHAIN-OF-AGENTS ORCHESTRATOR
    %% ==========================================
    O1["2. Lead Orchestrator Manager"]
    O2["Specialist Agents (News, Finance, Sentiment)"]
    O3[("Layered Memory (Working & Episodic)")]
    O4{"Conflict Detector<br>abs(Sentiment - Move) > 0.5"}
    O5["LLM Arbiter Reconciliation"]
    O6["Direct Consensus Alignment"]
    O7["Synthesized Market Report"]

    O1 --> O2
    O2 --> O3
    O3 --> O4
    O4 -->|Divergence| O5
    O4 -->|Aligned| O6
    O5 --> O7
    O6 --> O7

    %% Conexión vertical hacia el Agente 09
    O7 --> W1

    %% ==========================================
    %% 3. AGENT 09: THE AGENTIC WORKFLOW SYSTEM
    %% ==========================================
    W1["3. Intake State"]
    W2{"Validation Guard"}
    W3["Risk Assessment (LLM Node)"]
    W4{"Risk & Confidence Evaluation"}
    W5{"HITL Review Gate (Human in the Loop)"}
    W6["Processing Payout"]
    W7["Closed: Approved"]
    W8["Closed: Rejected"]

    W1 --> W2
    W2 -->|Valid| W3
    W2 -->|Invalid| W8
    W3 --> W4
    W4 -->|Confidence >= 0.85 & Low Risk| W6
    W4 -->|Confidence < 0.85 or High Risk| W5
    W5 -->|Approved| W6
    W5 -->|Rejected| W8
    W6 --> W7
```

---

## Agent Triad Breakdown

| # | Agent Name | Core Architectural Pattern | Capability Level | Key Technologies |
| :--- | :--- | :--- | :--- | :--- |
| **07** | **The Tool-Using Agent** | Think-Plan-Act cycle with typed Pydantic contracts and error fallbacks | Level 2 (Tool-Using Agent) | Google GenAI SDK, Pandas, Matplotlib, Pydantic |
| **08** | **The Chain-of-Agents Orchestrator** | Multi-specialist task delegation, layered working/episodic memory, and automated arbitration | Level 3 (Planning & Orchestrator Agent) | Gemini 2.5 Flash, Episodic Logs, Mathematical Divergence Scoring |
| **09** | **The Agentic Workflow System** | Deterministic Finite State Machine (FSM) with embedded LLM reasoning nodes and Human-in-the-Loop gates | Level 3–4 (Governed Agentic Systems) | Finite State Machines, HITL Checkpoints, Audit Trails |

---

## Repository Structure

```text
chapter_07_tool_orchestration_agents/
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
├── 07_tool_using_agent/
│   ├── agent.py
│   ├── tools.py
│   └── main.py
├── 08_chain_of_agents_orchestrator/
│   ├── memory.py
│   ├── specialists.py
│   ├── orchestrator.py
│   └── main.py
└── 09_agentic_workflow_system/
    ├── state_machine.py
    ├── workflow.py
    └── main.py
```

---

## Setup and Installation

### 1. Environment Configuration

```bash
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Upgrade pip and install pinned dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Configure API Keys

```bash
cp .env.example .env
```

Edit `.env` and configure your API key:

```env
GOOGLE_API_KEY="your_actual_gemini_api_key"
```

---

## Execution Instructions

* **Run Agent 07 (Tool-Using Visualization Agent):**
```bash
python 07_tool_using_agent/main.py
```

* **Run Agent 08 (Multi-Agent Market Arbiter):**
```bash
python 08_chain_of_agents_orchestrator/main.py
```

* **Run Agent 09 (Insurance Claims FSM Workflow with HITL):**
```bash
python 09_agentic_workflow_system/main.py
```

---

## Deep Engineering Principles

### 1. Function Calling as Strict Interface Contracts
Tools are not informal script invocations; they are governed by deterministic Pydantic schemas. This enforces compile-time and runtime validation on all parameter payloads passed between the LLM Reasoning Core and physical tools.

### 2. Multi-Agent Memory & Signal Arbitration
Specialist agents remain stateless micro-functions while the central orchestrator maintains state across two distinct memory tiers:
* **Working Memory:** The immediate execution scratchpad.
* **Episodic Memory:** A timestamped audit log of all inter-agent messages.

When specialist outputs diverge (e.g., public sentiment diverges from quantitative stock performance by more than $0.5$ on a normalized $[-1, 1]$ scale), an Arbiter Agent is dynamically engaged to reconcile conflicting signals before final synthesis.

### 3. FSM Governance and Human-in-the-Loop Safety
Critical enterprise operations must avoid unbounded autonomy. The state machine enforces strict guard conditions: claims below $0.85$ confidence or above financial risk thresholds automatically halt the transition pipeline and route to human operators for review before any settlement action is executed.
