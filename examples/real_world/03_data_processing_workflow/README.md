# Data Processing Workflow with Contract Validation

**Real-world example demonstrating contract-based validation for data pipelines (LangGraph/Airflow integration).**

## Quickstart (5 minutes)

```bash
# 1. Generate Python code from contracts
python3 -c "
from dsl.al_parser import parse_al
from language.python_generator_v2 import generate_python
with open('workflow.al'), 'r') as f:
    ir_module = parse_al(f.read())
with open('workflow.py', 'w') as f:
    f.write(generate_python(ir_module))
"

# 2. Run comprehensive test suite (58 tests)
python3 -m pytest test_workflow.py -v

# 3. Integrate with your data pipeline
from workflow import (
    validate_ingested_data,
    validate_data_quality,
    can_transition_to_stage
)

# Validate data after ingestion
if not validate_ingested_data(record_count=1000, size_mb=500, has_schema=True):
    raise ValueError("Invalid ingested data")

# Check stage transitions
if can_transition_to_stage("ingest", "validate", current_stage_complete=True):
    # Proceed to validation stage
    pass
```

**Result**: Runtime-validated data pipeline with quality gates at each stage.

---

## What This Example Demonstrates

### 1. **5-Stage Pipeline Validation**
- **Ingestion** - Validate source data (format, size, schema)
- **Validation** - Quality checks (completeness, errors, duplicates)
- **Transformation** - Type-specific validation (filter/map/aggregate/expand)
- **Enrichment** - Match rate and join validation
- **Export** - Result validation (counts, failure rates)

### 2. **Quality Gates**
- Completeness score thresholds (min 80%)
- Error rate limits (max 5%)
- Duplicate detection (max 10%)
- Schema compliance checking
- Throughput validation

### 3. **State Transition Enforcement**
- Sequential stage execution (no skipping)
- Completion checking before transitions
- Error handling and retry logic

### 4. **Transformation Validation**
- **Filter**: Output ≤ input count
- **Map**: Output = input count (1-to-1)
- **Aggregate**: Output ≤ input count (many-to-one)
- **Expand**: Output ≥ input count (1-to-many)

---

## Real-World Applications

### LangGraph Data Pipeline
```python
from langgraph.graph import StateGraph
from workflow import (
    validate_ingested_data,
    validate_data_quality,
    can_transition_to_stage
)

class PipelineState(TypedDict):
    current_stage: str
    record_count: int
    quality_score: float

workflow = StateGraph(PipelineState)

def ingest_node(state):
    # Ingest data
    data = load_from_source()
    
    # Validate ingested data
    if not validate_ingested_data(
        record_count=len(data),
        size_mb=data.size_mb,
        has_schema=True
    ):
        raise ValueError("Ingestion validation failed")
    
    return {"current_stage": "validate", "record_count": len(data)}

def validate_node(state):
    # Check can transition
    if not can_transition_to_stage("ingest", "validate", True):
        raise ValueError("Cannot transition to validate")
    
    # Validate quality
    quality_metrics = calculate_quality(state["data"])
    
    if not validate_data_quality(
        completeness_score=quality_metrics.completeness,
        error_rate=quality_metrics.error_rate,
        duplicate_rate=quality_metrics.duplicate_rate
    ):
        raise ValueError("Data quality below threshold")
    
    return {"current_stage": "transform"}

workflow.add_node("ingest", ingest_node)
workflow.add_node("validate", validate_node)
workflow.add_edge("ingest", "validate")
```

### Airflow DAG with Contract Validation
```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from workflow import validate_transformation_output

def transform_data(**context):
    input_data = context['ti'].xcom_pull(task_ids='ingest')
    
    # Apply transformation
    output_data = apply_map_transformation(input_data)
    
    # Validate transformation
    if not validate_transformation_output(
        input_count=len(input_data),
        output_count=len(output_data),
        transformation_type="map"
    ):
        raise ValueError("Map transformation invalid - count mismatch")
    
    return output_data

dag = DAG('data_pipeline', schedule_interval='@daily')

transform_task = PythonOperator(
    task_id='transform',
    python_callable=transform_data,
    dag=dag
)
```

---

## The Problem We're Solving

### Without Contracts

```python
# ❌ No validation of ingested data
def ingest():
    data = load_source()
    # What if data is empty?
    # What if schema is missing?
    # What if size exceeds limits?
    return data

# ❌ Stages execute out of order
current_stage = "transform"  # Skipped ingestion and validation!

# ❌ Low-quality data propagates
data = {"completeness": 0.5, "error_rate": 0.2}  # Terrible quality
proceed_to_next_stage(data)  # Garbage flows through pipeline

# ❌ Wrong transformation logic
output = filter_transformation(input_data)
# Filter increased record count? That's wrong!
```

### With Contracts

```python
# ✅ Validate ingested data
validate_ingested_data(
    record_count=len(data),
    size_mb=data.size_mb,
    has_schema=True
)  # Raises error if invalid

# ✅ Enforce stage order
can_transition_to_stage(
    current_stage="ingest",
    next_stage="transform",  # ❌ Skipping validation
    current_stage_complete=True
)  # Returns False

# ✅ Quality gates block bad data
validate_data_quality(
    completeness_score=0.5,  # ❌ Below 0.8 threshold
    error_rate=0.2,  # ❌ Above 0.05 threshold
    duplicate_rate=0.05
)  # Returns False

# ✅ Transformation validation
validate_transformation_output(
    input_count=100,
    output_count=150,  # ❌ Filter shouldn't increase
    transformation_type="filter"
)  # Returns False
```

---

## Running the Tests

```bash
# Full test suite (58 tests)
python3 -m pytest test_workflow.py -v

# Specific test categories
pytest test_workflow.py::TestIngestionValidation -v
pytest test_workflow.py::TestDataQualityValidation -v
pytest test_workflow.py::TestTransformationValidation -v
pytest test_workflow.py::TestStateTransitions -v
pytest test_workflow.py::TestEndToEndWorkflow -v
```

**Test Results**: 58/58 passing
- Ingestion validation (7 tests)
- Data quality (4 tests)
- Transformation (11 tests)
- Enrichment (5 tests)
- Export (5 tests)
- State transitions (8 tests)
- Batch processing (4 tests)
- Schema validation (3 tests)
- End-to-end workflows (3 tests)

---

## Key Patterns

### Quality Gate Pattern
```python
# Stage 1: Ingest
data = ingest_from_source()
if not validate_ingested_data(len(data), data.size_mb, True):
    raise QualityGateError("Ingestion failed")

# Stage 2: Validate quality
metrics = calculate_metrics(data)
if not validate_data_quality(
    metrics.completeness,
    metrics.error_rate,
    metrics.duplicate_rate
):
    raise QualityGateError("Quality below threshold")

# Proceed only if quality gates pass
```

### Transformation Type Validation
```python
# Filter: reduces records
validate_transformation_output(100, 80, "filter")  # ✅ Valid

# Map: preserves count
validate_transformation_output(100, 100, "map")  # ✅ Valid

# Aggregate: reduces records
validate_transformation_output(100, 10, "aggregate")  # ✅ Valid

# Expand: increases records
validate_transformation_output(100, 300, "expand")  # ✅ Valid
```

### Stage Transition Pattern
```python
# Always check before transitioning
if not can_transition_to_stage(
    current_stage="validate",
    next_stage="transform",
    current_stage_complete=True
):
    raise ValueError("Cannot transition - prerequisites not met")

# Valid sequence: ingest → validate → transform → enrich → export
```

---

## Common Pitfalls

### 1. Skipping Quality Checks

**❌ Wrong**:
```python
data = ingest()
transform(data)  # No quality validation!
```

**✅ Correct**:
```python
data = ingest()
validate_data_quality(...)  # Quality gate
transform(data)
```

### 2. Wrong Transformation Type

**❌ Wrong**:
```python
# Filter that increases count?
filtered = data[:150]  # Input was 100 records!
```

**✅ Correct**:
```python
filtered = apply_filter(data)
validate_transformation_output(
    len(data), len(filtered), "filter"
)  # Catches the error
```

### 3. Skipping Pipeline Stages

**❌ Wrong**:
```python
data = ingest()
export(data)  # Skipped validation, transform, enrich!
```

**✅ Correct**:
```python
can_transition_to_stage("ingest", "export", True)  # Returns False
```

---

## Next Steps

1. **Integrate with your pipeline** - Add contracts to existing Airflow/LangGraph workflows
2. **Customize thresholds** - Adjust quality gates for your data requirements
3. **Add more stages** - Extend with additional pipeline stages
4. **Monitor violations** - Track contract violations over time

---

## Learn More

- **[Example 1: E-commerce Orders](../01_ecommerce_orders/)** - State machine validation
- **[Example 2: Multi-Agent Research](../02_multi_agent_research/)** - Agent coordination
- **[Example 4: API Rate Limiting](../04_api_rate_limiting/)** - Rate limit validation
- **[Example 5: State Machine Patterns](../05_state_machine_patterns/)** - Generic state machines
- **[AssertLang Documentation](../../../docs/)** - Complete language guide
