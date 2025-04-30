# Assignment - 4: OpenRouter Routing System Documentation

#### Aditya Jhaveri (N13689134 - aaj6301)

## PDDL Domain Explanation

### Overview
The domain file defines the planning problem for routing requests to appropriate LLMs through OpenRouter using STRIPS planning with typing.

### Key Components

**Types**
- *llm*: Language models (GPT-4, Claude 3, etc.)
- *provider*: Companies offering LLMs (OpenAI, Anthropic)
- *capability*: Model features (coding, multilingual)
- *request*: User queries to route  
- *account*: User accounts with budgets
- *slot*: LLM capacity units
- *budgetunit*: Monetary units for costing

**Predicates**
- Availability and capability checks (`llm-available`, `has-capability`)
- Assignment tracking (`request-assigned`, `assigned-to`)
- Resource management (`llm-has-slot`, account budget units)
- Ownership relations (`belongs-to`, `belongs-to-account`)

**Action**  
Single `assign-request` action that:
1. Checks LLM availability and capabilities
2. Verifies request unassigned status
3. Confirms account has sufficient budget
4. Effects include updating assignment state and deducting resources

## PDDL Problem Explanation

### Scenario Setup
Defines a concrete routing scenario with:

**Objects**
- 4 LLMs (GPT-4, Claude 3, BingChat, Bard)
- Corresponding providers
- 5 capability-specific requests
- Limited slots (6 total) and budget units (10 total)

**Initial State**
- Maps each LLM to its provider
- Specifies each model's capabilities
- Sets request requirements
- Allocates slots and budget units

**Goal Condition**
- All 5 requests must be successfully assigned

## System Components

### 1. PDDL Validator
- Verifies domain and problem file syntax
- Checks type consistency
- Validates initial state satisfies preconditions
- Confirms goal is well-formed

### 2. PDDL Solver
- Uses Fast Downward planner
- Finds valid action sequences
- Ensures all constraints are met
- Produces step-by-step assignment plan

### 3. OpenRouter API Implementation

**Core Features**
- Direct API integration (alternative to MCP)
- Dynamic request routing
- Real-time cost tracking
- Async request handling

**Operation Flow**
1. Receives solved plan from PDDL system
2. Executes actual API calls to OpenRouter
3. Handles runtime adjustments
4. Monitors real usage against predictions

## Key Differences: PDDL vs API Approach

| Aspect                | PDDL System               | API Implementation     |
|-----------------------|---------------------------|-------------------------|
| Planning              | Automated formal planning | Custom business logic   |
| Flexibility           | Constrained by model      | Highly adaptable        |
| Cost Control          | Budget units              | Real API pricing        |
| Real-time Adaptability| Limited                   | Continuous adjustments  |

---

The system combines rigorous upfront planning with practical runtime execution for optimal LLM request routing.

#### Aditya Jhaveri (N13689134 - aaj6301)