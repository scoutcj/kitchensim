# Manual End-to-End Test for PR 3: LangGraph State & Skeleton

## Prerequisites
1. Backend server is running: `python main.py` (or `./venv/bin/python main.py`)
2. Server should be running on `http://localhost:8000`

## Test 1: Run Workflow via API
**Goal:** Verify workflow runs end-to-end through all 8 nodes

```bash
curl -X POST http://localhost:8000/api/simulate \
  -H "Content-Type: application/json" \
  -d '{"input": "Dinner for 4 people. Make pasta with sauce."}'
```

**Expected:** JSON response with:
- `user_input`: Your input text
- `parsed_data`: Stub data (empty/placeholder)
- `knowledge_base`: Default kitchen config (small_restaurant)
- `recipes`: Empty array (stub)
- `tasks`: Empty DAG (stub)
- `schedule`: Empty schedule (stub)
- `validation`: Default validation (feasible: true)
- `conflicts`: Empty array (stub)
- `output`: "Timeline will be generated here..."

## Test 2: Run Workflow via Python Script
**Goal:** Test workflow directly with Python

```bash
cd backend
./venv/bin/python test_pr3_e2e.py "Dinner for 100 people. We need pasta and salad."
```

**Expected:** 
- All 8 nodes execute
- State flows through each node
- Final state contains all expected fields
- Knowledge base is created with default config

## Test 3: Verify Node Execution Order
**Goal:** Confirm nodes execute in correct sequence

The workflow should execute in this order:
1. `parse_input` → creates `parsed_data`
2. `update_kb` → creates `knowledge_base`
3. `analyze_recipes` → creates `recipes`
4. `build_dag` → creates `tasks`
5. `schedule_tasks` → creates `schedule`
6. `validate` → creates `validation`
7. `detect_conflicts` → creates `conflicts`
8. `format_output` → creates `output`

**How to verify:** Check that each field exists in the response, even if it's stub data.

## Test 4: Test with Different Inputs
**Goal:** Verify workflow handles different inputs

```bash
# Simple input
curl -X POST http://localhost:8000/api/simulate \
  -H "Content-Type: application/json" \
  -d '{"input": "Make breakfast for 2"}'

# Complex input
curl -X POST http://localhost:8000/api/simulate \
  -H "Content-Type: application/json" \
  -d '{"input": "Dinner for 50 people. We need pasta, salad, bread, and dessert. I have 3 ovens and 2 chefs."}'
```

**Expected:** Workflow completes for all inputs (even though nodes are stubs)

## Test 5: Check Knowledge Base Integration
**Goal:** Verify knowledge base is properly integrated

```bash
curl -X POST http://localhost:8000/api/simulate \
  -H "Content-Type: application/json" \
  -d '{"input": "Test"}' | jq '.knowledge_base'
```

**Expected:** 
- `kitchen_type`: "small_restaurant"
- `ovens`: Array with 2 ovens
- `burners`: Array with 6 burners
- `microwaves`: Array with 2 microwaves
- `chefs`: Array with 2 chefs

## Success Criteria

✅ Workflow runs without errors
✅ All 8 nodes execute in sequence
✅ State flows through all nodes
✅ Knowledge base is created with defaults
✅ API endpoint returns valid JSON
✅ All state fields are present in final output
✅ Workflow handles different input types

## Notes

- **This is PR 3 (skeleton)**: All nodes are stubs that return placeholder data
- **Real implementation**: Will come in PRs 4-9
- **Purpose**: Verify the workflow structure and data flow work correctly
- **Next step**: PR 4 will implement `parse_input_node` with real LLM parsing


