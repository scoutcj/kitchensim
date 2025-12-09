# Phase 1: Core Kitchen Simulator MVP

## Overview
Build a working kitchen simulator that takes natural language input, parses it into structured data, creates a deterministic schedule, and displays it in a text-based format. This is the foundation before adding visualization and Monte Carlo simulation.

## Tech Stack
- **Backend:** FastAPI (Python) with LangGraph for agent orchestration
- **Frontend:** React + TypeScript
- **LLM:** Anthropic Claude (with function calling)
- **Data:** In-memory for MVP (Pydantic models / JSON structures)

## Architecture

### LangGraph State Machine

**State Schema (Pydantic Model):**
```python
class KitchenSimulatorState(TypedDict):
    user_input: str                    # Raw natural language input
    parsed_data: ParsedData            # Structured data from parser
    knowledge_base: KnowledgeBase      # Static kitchen info (equipment, staff)
    recipes: List[Recipe]              # Parsed recipes with tasks
    tasks: TaskDAG                     # Unified dependency graph
    schedule: Schedule                 # Final timeline with resource assignments
    conflicts: List[Conflict]          # Detected bottlenecks/risks
    validation: ValidationResult       # LLM validation + answers
    output: str                        # Formatted text timeline
```

**Node Descriptions:**

1. **`parse_input_node`**
   - **Input:** `state.user_input` (raw natural language)
   - **Does:** Uses ParserAgent (Claude) to extract structured data
   - **Output:** Updates `state.parsed_data` with:
     - Event details (date, time, guest count, event type)
     - Recipe text/menu items
     - Constraints (staff count, equipment available)
     - User knowledge base overrides (e.g., "I have 3 ovens")
   - **Example:** "Dinner for 100 people, here's my pasta recipe..." → structured dict

2. **`update_kb_node`**
   - **Input:** `state.parsed_data` (contains user_overrides)
   - **Does:** Merges user overrides into knowledge_base
   - **Output:** Updates `state.knowledge_base` with user-specified values
   - **Note:** Knowledge base contains ONLY static kitchen info:
     - Kitchen layout (microwaves, ovens, stoves/burners - individual resources with IDs)
     - Staff configuration (chefs, prep chefs, cook chefs, servers - individual with IDs)
     - Equipment specs (oven capacity, stove burners, microwave capacity)
     - Multipliers (skill level, ability, energy level - applied task-selectively)
     - **NOT task timing** (that comes from recipes)
   - **Example:** User says "I have 3 ovens" → knowledge_base.oven_count = 3

3. **`analyze_recipes_node`**
   - **Input:** `state.parsed_data.recipes_text` + `state.knowledge_base`
   - **Does:** Uses RecipeAgent (Claude) to parse recipes → tasks
   - **Output:** Updates `state.recipes` with list of Recipe objects
   - **RecipeAgent extracts:**
     - Task breakdown (explicit + implicit steps)
     - Duration estimates (from recipe instructions, NOT knowledge base)
     - Dependencies (what must happen before)
     - Resource needs (oven, stove, chef, prep station)
   - **Example Output:** See detailed JSON example below

4. **`build_dag_node`**
   - **Input:** `state.recipes` (list of Recipe objects, each with tasks)
   - **Does:** Flattens all tasks from all recipes into unified DAG
   - **Output:** Updates `state.tasks` with:
     - All tasks from all recipes as nodes
     - Dependency edges (task A → task B if A depends on B)
     - Validates no cycles
   - **Note:** Takes tasks across ALL recipes and builds one unified graph

5. **`schedule_node`**
   - **Input:** `state.tasks` (DAG) + `state.knowledge_base` (resources)
   - **Does:** Runs SchedulerAgent (topological sort + resource allocation)
   - **Output:** Updates `state.schedule` with:
     - Start/end times for each task
     - Resource assignments (which oven, which chef)
     - Timeline respecting dependencies and resource constraints
   - **Algorithm:** Topological sort → resource-aware scheduling

6. **`validate_node`**
   - **Input:** `state.schedule` + `state.parsed_data` (original request)
   - **Does:** Uses Claude to check if schedule makes sense, answers user questions
   - **Output:** Updates `state.validation` with:
     - Validation result (feasible/risky/impossible)
     - Answers to feasibility questions ("Can we handle this?")
     - Suggestions for improvements

7. **`detect_conflicts_node`**
   - **Input:** `state.schedule` + `state.knowledge_base`
   - **Does:** Uses ConflictAgent to find bottlenecks, resource overloads, timing issues
   - **Output:** Updates `state.conflicts` with list of warnings/errors:
     - Overlapping resource usage
     - Insufficient resources
     - Tasks that can't finish in time
     - Critical path bottlenecks

8. **`format_output_node`**
   - **Input:** `state.schedule` + `state.conflicts` + `state.validation`
   - **Does:** Formats everything into readable text timeline
   - **Output:** Updates `state.output` with formatted string
   - **Format:** Timeline grouped by time, shows resources, highlights conflicts

**Node Output Format:**
- All nodes output Pydantic objects (Python dicts/objects)
- LangGraph passes these as state updates
- Think of it as JSON-like structures passed between nodes

### Agent Roles (as classes/functions)
- **ParserAgent:** LLM-based extraction of structured data
- **RecipeAgent:** Analyzes recipes, extracts timing/dependencies
- **SchedulerAgent:** DAG-based scheduling with resource constraints
- **ResourceAgent:** Checks equipment/staff availability
- **ConflictAgent:** Detects bottlenecks and risks
- **KnowledgeBase:** Manages default assumptions + user overrides

## Pull Request Breakdown

We'll implement Phase 1 in 11 focused PRs, working step-by-step:

### PR 1: Project Foundation
**Goal:** Get basic structure running
- FastAPI app with health endpoint
- React app with basic UI
- Environment setup (Claude API key)
- Basic file structure

**Files:**
- `backend/main.py`
- `backend/requirements.txt` (FastAPI, langgraph, anthropic, pydantic)
- `frontend/` (Vite + React + TypeScript setup)
- `.env.example` (ANTHROPIC_API_KEY)

**Test:** Can hit `/api/health` from frontend

---

### PR 2: Knowledge Base System
**Goal:** Static kitchen info storage
- Default knowledge base JSON (ovens, chefs, equipment)
- `KnowledgeBase` class (load, update, query)
- API endpoint to update KB

**Files:**
- `backend/knowledge_base/defaults.json`
- `backend/knowledge_base/kb.py`
- `backend/api/knowledge.py`

**Test:** Can load defaults, can update oven_count, can query values

---

### PR 3: LangGraph State & Skeleton
**Goal:** State machine structure (nodes don't do real work yet)
- `KitchenSimulatorState` Pydantic model
- 8 node functions (stubs that pass data through)
- LangGraph workflow wired up
- Test with mock data

**Files:**
- `backend/state.py`
- `backend/graph.py`
- `backend/nodes/` (8 node files as stubs)

**Test:** Can run graph with mock state, data flows through all nodes

---

### PR 4: Parser Agent
**Goal:** Extract structured data from natural language
- `ParserAgent` class with Claude integration
- Pydantic schemas for extracted data
- Function calling setup
- Wire into `parse_input_node`

**Files:**
- `backend/agents/parser.py`
- `backend/schemas/parsed.py`

**Test:** "Dinner for 100 people" → extracts {guest_count: 100, event_type: "dinner"}

---

### PR 5: Recipe Agent
**Goal:** Parse recipes into tasks
- `RecipeAgent` class
- Claude prompt for recipe analysis
- Task inference (explicit + implicit steps)
- Wire into `analyze_recipes_node`

**Files:**
- `backend/agents/recipe.py`
- `backend/schemas/recipe.py`

**Test:** Recipe text → list of tasks with timing, dependencies, resources

---

### PR 6: DAG Builder
**Goal:** Convert tasks into dependency graph
- `TaskDAG` class
- Build graph from all recipe tasks (unified DAG)
- Validate no cycles
- Wire into `build_dag_node`

**Files:**
- `backend/scheduler/dag.py`

**Test:** Multiple recipes → unified DAG with correct dependencies

---

### PR 7: Scheduler Algorithm
**Goal:** Core scheduling logic
- Topological sort
- Resource allocation algorithm
- Timeline calculation
- **Buffer time:** Add buffer time between tasks and service windows when estimating completion
- **Service windows:** Consider service start/end times when scheduling
- Wire into `schedule_node`

**Files:**
- `backend/scheduler/algorithm.py`

**Test:** DAG + resources → schedule with start/end times, resource assignments, buffer times included

---

### PR 8: Validation & Conflict Detection
**Goal:** Check schedule quality
- `ConflictAgent` class
- Claude validation
- Wire into `validate_node` and `detect_conflicts_node`

**Files:**
- `backend/agents/conflict.py`
- `backend/agents/validator.py`

**Test:** Schedule → detects conflicts, validates feasibility

---

### PR 9: Output Formatter
**Goal:** Human-readable timeline
- Text formatter
- Include buffer times and service windows in output
- Show estimated completion times with buffers
- Wire into `format_output_node`
- API endpoint returns formatted output

**Files:**
- `backend/formatters/timeline.py`
- Update `backend/main.py` with `/api/simulate`

**Test:** Schedule → readable text timeline with buffer times and service windows clearly indicated

---

### PR 10: Frontend Integration
**Goal:** End-to-end flow
- Connect React to `/api/simulate`
- Display results
- Error handling
- Basic styling

**Files:**
- `frontend/src/components/Simulator.tsx`
- `frontend/src/api/client.ts`

**Test:** Full E2E - input → output displayed

---

### PR 11: Polish & Edge Cases
**Goal:** Handle errors, edge cases, improve UX
- Error handling
- Loading states
- Edge case handling
- Logging

**Files:**
- Various updates across codebase

**Test:** All 8 test cases from phase1.md pass

---

## Step-by-Step Implementation

### Step 1: Project Setup
1. Initialize Python backend
   - Create `backend/` directory
   - Set up `requirements.txt` (FastAPI, langgraph, anthropic, pydantic)
   - Create `backend/main.py` with FastAPI app
   - Set up CORS for React frontend

2. Initialize React frontend
   - Create `frontend/` directory
   - Set up Vite + React + TypeScript
   - Create basic app structure
   - Set up API client for backend calls

3. Environment setup
   - Create `.env.example` with `ANTHROPIC_API_KEY`
   - Set up `.env` (gitignored)

### Step 2: Knowledge Base System
1. Create default knowledge base
   - `backend/knowledge_base/defaults.json` with static kitchen info
   - **Resources tracked:** Microwaves (with wattage), Ovens (with max_temp, capacity), Burners (with type, individual not grouped as Stove)
   - **Staff tracked:** Chefs, Prep Chefs, Cook Chefs, Servers (individual with IDs)
   - **Multipliers:** Skill level, Ability, Energy level (applied task-selectively, not globally)
   - **Default kitchen configurations:**
     - **Home:** 1 oven, 4 burners, 1 microwave, 1 chef
     - **Small Restaurant:** 2 ovens, 6 burners, 2 microwaves, 2 chefs
     - **Commercial:** 4 ovens, 8 burners, 5 microwaves, 5 chefs
   - **Important:** Knowledge base contains ONLY static kitchen configuration
   - **NOT task timing** (that comes from recipe analysis)
   - **Structure:** Pydantic models (Oven, Burner, Microwave, Chef classes) for type safety
   - **Session-scoped for MVP:** Each simulation gets a Kitchen instance, structure supports future DB persistence

2. Create `KnowledgeBase` class
   - Load defaults from JSON
   - Merge user overrides (from LLM extraction in parse_input_node)
   - Provide lookup methods for resources, staff, multipliers
   - Track individual resources with IDs (e.g., "oven_1", "chef_1")
   - Example: User says "I have 3 ovens" → creates 3 Oven instances with IDs

3. **Multiplier Application (Task-Selective)**
   - Multipliers are NOT global - they apply differently based on task type
   - Energy level affects prep tasks (chopping, peeling) more than passive tasks (boiling)
   - Skill level affects complex cooking tasks more than simple prep
   - Example: Tired chef → "chop onions" gets 1.3x multiplier, "boil pasta" gets 1.05x (mostly passive)
   - Implementation: `Chef.get_task_multiplier(task_type: str) -> float`

### Step 3: LangGraph State & Nodes
1. Define state schema (Pydantic models)
   - `KitchenSimulatorState` with all fields

2. Create node functions:
   - `parse_input_node(state)` → uses ParserAgent
   - `update_kb_node(state)` → merges user overrides
   - `analyze_recipes_node(state)` → uses RecipeAgent
   - `build_dag_node(state)` → creates task graph
   - `schedule_node(state)` → uses SchedulerAgent
   - `validate_node(state)` → LLM validation
   - `detect_conflicts_node(state)` → uses ConflictAgent
   - `format_output_node(state)` → creates text timeline

3. Build LangGraph workflow
   - Define edges between nodes
   - Add conditional edges (if conflicts found, loop back)

### Step 4: Parser Agent
1. Create `ParserAgent` class
   - Uses Claude with function calling
   - Extracts:
     - Event details (date, time, guest count, event type)
     - Recipes/menu items (raw text)
     - Constraints (staff count, equipment available)
     - User knowledge base overrides (e.g., "I have 3 ovens")
   - Returns structured dict (Pydantic model)

2. Define Pydantic schemas for extracted data:
   - `EventDetails` (date, time, guest_count, event_type)
   - `RecipeText` (raw recipe text/menu items)
   - `Constraint` (staff, equipment)
   - `KnowledgeOverride` (user-specified kitchen config changes)

### Step 5: Recipe Agent
1. Create `RecipeAgent` class
   - Takes recipe text/ingredients
   - Uses Claude to extract:
     - Task breakdown (explicit + implicit steps)
     - Duration estimates (from recipe instructions, NOT knowledge base)
     - Dependencies (what must happen before)
     - Resource needs (oven, stove, chef, prep station)
   - **Infers implicit tasks:** e.g., "cubed potatoes" → infers "cube potatoes" task
   - Returns structured recipe data (Pydantic model)

2. **Example RecipeAgent Output:**
   ```json
   {
     "recipe_name": "Pasta Carbonara",
     "servings": 4,
     "tasks": [
       {
         "id": "task_1",
         "name": "Cube pancetta",
         "description": "Cube 2 cups of pancetta",
         "duration_minutes": 5,
         "duration_source": "inferred",
         "dependencies": [],
         "resources_needed": ["prep_station", "chef"],
         "task_type": "prep",
         "implicit": true
       },
       {
         "id": "task_2",
         "name": "Boil pasta",
         "description": "Boil 1 lb pasta for 12 minutes",
         "duration_minutes": 12,
         "duration_source": "explicit",
         "dependencies": [],
         "resources_needed": ["stove", "pot", "chef"],
         "task_type": "cook",
         "implicit": false
       },
       {
         "id": "task_3",
         "name": "Saute pancetta",
         "description": "Saute pancetta in pan for 8 minutes until crispy",
         "duration_minutes": 8,
         "duration_source": "explicit",
         "dependencies": ["task_1"],
         "resources_needed": ["stove", "pan", "chef"],
         "task_type": "cook",
         "implicit": false
       },
       {
         "id": "task_6",
         "name": "Combine and toss",
         "description": "Combine pasta, pancetta, and sauce in pan, toss for 2 minutes",
         "duration_minutes": 2,
         "duration_source": "explicit",
         "dependencies": ["task_3", "task_4", "task_5"],
         "resources_needed": ["stove", "pan", "chef"],
         "task_type": "cook",
         "implicit": false
       }
     ]
   }
   ```
   - **Key points:**
     - Dependencies: "Saute pancetta" depends on "Cube pancetta" (task_1 → task_3)
     - "Combine and toss" depends on 3 tasks (all must finish first)
     - Resources: each task lists what it needs
     - Implicit tasks: inferred from recipe context

### Step 6: Task DAG Builder
1. Create `TaskDAG` class
   - **Input:** `state.recipes` (list of Recipe objects, each with tasks)
   - **Does:** Flattens all tasks from ALL recipes into unified DAG
   - Builds dependency graph:
     - Nodes = all tasks from all recipes
     - Edges = dependencies (task A → task B if B depends on A)
   - Validates no cycles
   - **Output:** Updates `state.tasks` with unified DAG structure

2. Example:
   ```python
   # Input: Multiple recipes
   recipes = [
       {name: "Pasta Carbonara", tasks: [task_1, task_2, task_3, ...]},
       {name: "Caesar Salad", tasks: [task_8, task_9, ...]},
       {name: "Garlic Bread", tasks: [task_10, task_11, ...]}
   ]
   
   # Output: Unified DAG
   dag = {
       "nodes": [task_1, task_2, ..., task_11],  # All tasks
       "edges": [
           (task_1, task_3),  # task_1 → task_3 dependency
           (task_2, task_5),
           (task_3, task_6),
           ...
       ]
   }
   ```

### Step 7: Scheduler Agent (Core Algorithm)
1. Implement topological sort
   - Get valid task ordering from DAG
   - Handle cycles (shouldn't happen, but validate)

2. Implement resource-aware scheduling
   - Track resource availability over time
   - Assign tasks to resources (ovens, chefs, stations)
   - Handle parallelization (if resources available)
   - Calculate start/end times for each task

3. Algorithm pseudocode:
   ```
   tasks = topological_sort(dag)
   schedule = {}
   resource_timeline = {oven: [], chef: [], ...}
   
   for task in tasks:
       earliest_start = max(dependency.end_time for dependency in task.dependencies)
       resource = find_available_resource(task.resources, earliest_start)
       task.start_time = max(earliest_start, resource.available_at)
       task.end_time = task.start_time + task.duration
       resource_timeline[resource].append(task)
   ```

### Step 8: Validation & Conflict Detection
1. Create `ConflictAgent` class
   - Checks for:
     - Overlapping resource usage
     - Insufficient resources
     - Tasks that can't finish in time
     - Critical path bottlenecks
   - Returns list of conflicts/risks

2. Create `validate_node` (Claude-based)
   - Sends schedule to Claude
   - Asks: "Does this schedule make sense? Any issues?"
   - Returns validation result + suggestions

### Step 9: Output Formatter
1. Create text-based timeline formatter
   - Groups tasks by time
   - Shows resource assignments
   - Highlights critical path
   - Lists conflicts/warnings
   - Example output:
     ```
     Timeline for Dinner Service (100 guests)
     ========================================
     
     14:00 - Prep vegetables (Chef 1, Station 1) [30 min]
     14:00 - Prep pasta dough (Chef 2, Station 2) [45 min]
     14:30 - Start sauce (Chef 1, Stove 1) [20 min]
     14:45 - Boil pasta (Chef 2, Stove 2) [15 min]
     15:00 - Plate dishes (Chef 1 + Chef 2) [10 min]
     
     Critical Path: Prep pasta dough → Boil pasta → Plate
     Warnings: Oven overloaded at 15:00 (3 tasks need oven, only 2 available)
     ```

### Step 10: FastAPI Endpoints
1. Create `/api/simulate` endpoint
   - Takes: `{ "input": "natural language string" }`
   - Runs LangGraph workflow
   - Returns: `{ "schedule": {...}, "output": "formatted text", "conflicts": [...] }`

2. Create `/api/health` endpoint
   - Basic health check

### Step 11: React Frontend
1. Create input component
   - Text area for natural language input
   - Submit button
   - Loading state

2. Create output component
   - Displays formatted timeline (pre-formatted text or structured)
   - Shows conflicts/warnings
   - Basic styling

3. Wire up API calls
   - Call `/api/simulate` on submit
   - Handle errors
   - Display results

### Step 12: Integration & Polish
1. Error handling
   - Claude API failures
   - Invalid input parsing
   - Scheduling failures

2. Logging
   - Log each node execution
   - Log Claude API calls (for debugging)

3. Basic styling
   - Make frontend presentable
   - Responsive layout

## Testable Section: End-to-End Tests

### Test 1: Simple Single Dish
**Input:**
```
"We're making pasta for 4 people. Boil pasta for 15 minutes, then make sauce for 20 minutes, then plate."
```

**Expected Output:**
- Parsed: 4 guests, 1 dish (pasta)
- Tasks: [Boil pasta (15 min), Make sauce (20 min), Plate (5 min)]
- Schedule: Boil pasta → Make sauce → Plate (sequential, no conflicts)
- Timeline shows all tasks with times
- No conflicts detected

**How to Test:**
1. Open frontend
2. Paste input
3. Submit
4. Verify timeline shows all tasks in correct order
5. Verify no warnings/conflicts

---

### Test 2: Multiple Dishes with Dependencies
**Input:**
```
"Dinner for 10 people. We need to prep vegetables (30 min), then make sauce (20 min depends on prep), boil pasta (15 min), and plate everything (5 min, depends on sauce and pasta)."
```

**Expected Output:**
- Tasks: Prep (30 min) → [Sauce (20 min), Pasta (15 min)] → Plate (5 min)
- Schedule shows parallelization (sauce and pasta can happen simultaneously after prep)
- Timeline shows prep finishes, then sauce and pasta start together
- Plate starts after both sauce and pasta finish

**How to Test:**
1. Submit input
2. Verify prep happens first
3. Verify sauce and pasta can run in parallel (same start time after prep)
4. Verify plate happens after both complete

---

### Test 3: Resource Constraints
**Input:**
```
"We have 1 oven. We need to bake bread (60 min), roast chicken (45 min), and bake dessert (30 min). All can start at the same time."
```

**Expected Output:**
- Tasks identified: 3 baking tasks
- Schedule shows sequential oven usage (can't all start at once)
- Timeline: Bread (0-60), Chicken (60-105), Dessert (105-135)
- Conflict warning: "3 tasks need oven, but only 1 available - tasks must be sequential"

**How to Test:**
1. Submit input
2. Verify tasks are scheduled sequentially (not parallel)
3. Verify conflict warning appears
4. Verify total time = 135 minutes (sum of all tasks)

---

### Test 4: User Knowledge Override
**Input:**
```
"Pasta dinner for 6. My pasta is freshly made so it only needs to cook for 5 minutes. Boil pasta, make sauce (20 min), then plate."
```

**Expected Output:**
- Knowledge base override: pasta cook time = 5 min (not default 15 min)
- Tasks: Boil pasta (5 min), Make sauce (20 min), Plate (5 min)
- Schedule uses 5 min for pasta (not 15)
- Timeline reflects shorter pasta time

**How to Test:**
1. Submit input
2. Verify pasta task shows 5 minutes (not 15)
3. Verify timeline is shorter than default
4. Check backend logs to confirm knowledge base was updated

---

### Test 5: Complex Multi-Dish Service
**Input:**
```
"Brunch for 50 people next Saturday. We're serving:
- Eggs benedict: poach eggs (5 min), make hollandaise (15 min, depends on prep), assemble (3 min)
- Pancakes: make batter (10 min), cook pancakes (20 min, depends on batter), serve (2 min)
- Coffee: brew (5 min), serve (1 min)

We have 2 chefs and 2 stoves. Can we handle this?"
```

**Expected Output:**
- Multiple dishes parsed correctly
- Dependencies identified (hollandaise depends on prep, pancakes depend on batter)
- Resource allocation: 2 chefs, 2 stoves used efficiently
- Parallelization possible (eggs and pancakes can be made simultaneously)
- Timeline shows efficient resource usage
- Answer to "can we handle this?" in output

**How to Test:**
1. Submit input
2. Verify all dishes and tasks are identified
3. Verify dependencies are respected
4. Verify resources are allocated (chefs/stoves assigned)
5. Verify parallelization where possible
6. Verify answer to feasibility question

---

### Test 6: Conflict Detection
**Input:**
```
"Dinner for 100 people. We need to:
- Prep vegetables: 2 hours
- Cook main course: 1.5 hours (needs 3 ovens)
- Prep appetizers: 1 hour
- Plate everything: 30 minutes

We only have 2 ovens. Service starts at 6pm, prep can start at 2pm."
```

**Expected Output:**
- Schedule created
- Conflict detected: "Main course needs 3 ovens but only 2 available"
- Timeline shows what's possible with 2 ovens
- Warning about insufficient resources
- Suggestion: "Consider starting prep earlier or reducing oven needs"

**How to Test:**
1. Submit input
2. Verify conflict is detected and displayed
3. Verify schedule still generated (best effort)
4. Verify warning message is clear
5. Verify suggestion is provided

---

### Test 7: Edge Case - Impossible Schedule
**Input:**
```
"We need to serve 200 people at 6pm. Prep takes 8 hours, cooking takes 4 hours, plating takes 1 hour. We can start at 5pm."
```

**Expected Output:**
- Schedule attempted
- Conflict: "Total time required (13 hours) exceeds available time (1 hour)"
- Clear error message
- Suggestion: "Start prep earlier or reduce scope"

**How to Test:**
1. Submit input
2. Verify impossible schedule is detected
3. Verify clear error message
4. Verify helpful suggestion

---

### Test 8: Natural Language Variations
**Input (various phrasings):**
- "Can we serve 50 people brunch and 30 people dinner on the same day?"
- "What's the fanciest dinner I can make in 1 hour with 2 ovens?"
- "The salmon delivery is delayed by 2 hours. Can we still plate on time?"

**Expected Output:**
- System handles different question types
- For feasibility questions: provides yes/no + explanation
- For optimization questions: provides best-effort answer
- For constraint changes: recalculates schedule

**How to Test:**
1. Try each variation
2. Verify system doesn't crash
3. Verify appropriate response type for each question
4. Verify schedule is still generated when applicable

---

## Success Criteria for Phase 1

✅ Natural language input is parsed into structured data
✅ Recipes are analyzed and broken into tasks with timing
✅ Task dependencies are identified and respected
✅ Resource constraints are checked and enforced
✅ Schedule is generated with realistic timing
✅ Conflicts and bottlenecks are detected
✅ Output is readable and actionable
✅ System handles edge cases gracefully
✅ Frontend and backend communicate correctly
✅ End-to-end flow works for all test cases above

## Next Steps (Phase 2)
- Add D3 visualization (Gantt chart)
- Add interactive parameter sliders
- Add Monte Carlo simulation
- Add resource utilization views
- Enhance knowledge base with RAG

## Future Phases (Post-MVP)

### Multi-Kitchen Support
- Support for multiple people working on the same base kitchen configuration
- Shared resource pools across kitchen instances
- Coordination between multiple kitchen simulations
- **Note for current implementation:** Structure knowledge base to support future multi-kitchen scenarios, but keep MVP session-scoped

### User Profiles & Persistence
- Database integration (SQLite → PostgreSQL)
- User authentication
- Saved kitchen profiles ("My Home Kitchen", "Restaurant A", etc.)
- Historical data (what schedules worked before)
- **Note for current implementation:** Use Pydantic models that can easily serialize to DB schemas later

