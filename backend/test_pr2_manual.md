# Manual End-to-End Test for PR 2: Knowledge Base System

## Prerequisites
1. Backend server is running: `python main.py` (or `./venv/bin/python main.py`)
2. Server should be running on `http://localhost:8000`

## Test 1: Load Defaults
**Goal:** Verify we can load default kitchen configurations

```bash
# Get default small restaurant kitchen
curl http://localhost:8000/api/knowledge/kitchen
```

**Expected:** JSON response with:
- `kitchen_type: "small_restaurant"`
- `ovens`: Array with 2 ovens
- `burners`: Array with 6 burners
- `microwaves`: Array with 2 microwaves
- `chefs`: Array with 2 chefs

## Test 2: Update Kitchen Configuration
**Goal:** Verify we can update kitchen with user overrides

```bash
# Update existing oven capacity
curl -X POST http://localhost:8000/api/knowledge/kitchen/update \
  -H "Content-Type: application/json" \
  -d '{
    "overrides": {
      "ovens": [{"id": "oven_1", "capacity": 5}]
    }
  }'
```

**Expected:** Response shows `oven_1` now has `capacity: 5`

## Test 3: Add New Resource
**Goal:** Verify we can add new resources

```bash
# Add a new oven
curl -X POST http://localhost:8000/api/knowledge/kitchen/update \
  -H "Content-Type: application/json" \
  -d '{
    "overrides": {
      "add_oven": {"id": "oven_3", "capacity": 4, "max_temp": 600}
    }
  }'
```

**Expected:** Response shows 3 ovens total (original 2 + new one)

## Test 4: Query Values
**Goal:** Verify we can query specific values

```bash
# Get kitchen config
curl http://localhost:8000/api/knowledge/kitchen | jq '.ovens[0]'
```

**Expected:** First oven details with `id`, `capacity`, `max_temp`

## Test 5: Reset to Defaults
**Goal:** Verify we can reset kitchen configuration

```bash
# Reset to home kitchen
curl -X POST http://localhost:8000/api/knowledge/kitchen/reset?kitchen_type=home
```

**Expected:** Response shows home kitchen config (1 oven, 4 burners, 1 microwave, 1 chef)

## Test 6: Different Kitchen Types
**Goal:** Verify all three kitchen types work

```bash
# Test home
curl -X POST http://localhost:8000/api/knowledge/kitchen/reset?kitchen_type=home

# Test commercial
curl -X POST http://localhost:8000/api/knowledge/kitchen/reset?kitchen_type=commercial
```

**Expected:** Each type returns correct resource counts

## Success Criteria
✅ Can load defaults for all three kitchen types
✅ Can update existing resources (ovens, burners, chefs)
✅ Can add new resources
✅ Can query specific values
✅ Can reset to defaults
✅ All API endpoints return valid JSON

