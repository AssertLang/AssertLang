"""
Test suite for Data Processing Workflow with Contract Validation

Demonstrates how contracts validate data pipeline stages and enforce
workflow state transitions.
"""

import pytest
import sys
from pathlib import Path

# Add project root and current directory to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(Path(__file__).parent))

from assertlang.runtime.contracts import ContractViolationError
from workflow import (
    validate_ingestion_input,
    validate_ingested_data,
    validate_data_quality,
    validate_transformation_input,
    validate_transformation_output,
    validate_enrichment_input,
    validate_enrichment_result,
    validate_export_config,
    validate_export_result,
    can_transition_to_stage,
    should_retry_stage,
    validate_batch_config,
    calculate_batch_count,
    is_pipeline_complete,
    validate_schema_compliance,
    validate_throughput,
    is_error_threshold_exceeded
)


class TestIngestionValidation:
    """Test data ingestion validation."""

    def test_valid_ingestion_input(self):
        """Valid ingestion inputs should pass."""
        result = validate_ingestion_input(
            source_url="https://api.example.com/data",
            format="json",
            max_size_mb=1000
        )
        assert result is True

    def test_empty_source_url_rejected(self):
        """Empty source URL should be rejected."""
        with pytest.raises(ContractViolationError) as exc_info:
            validate_ingestion_input(
                source_url="",  # Invalid
                format="json",
                max_size_mb=1000
            )
        assert "valid_source" in str(exc_info.value)

    def test_excessive_size_rejected(self):
        """Size > 10000 MB should be rejected."""
        with pytest.raises(ContractViolationError) as exc_info:
            validate_ingestion_input(
                source_url="https://api.example.com/data",
                format="json",
                max_size_mb=15000  # Invalid
            )
        assert "reasonable_size" in str(exc_info.value)

    def test_valid_ingested_data(self):
        """Valid ingested data should pass."""
        result = validate_ingested_data(
            record_count=1000,
            size_mb=500,
            has_schema=True
        )
        assert result is True

    def test_no_records_rejected(self):
        """Zero records should be rejected."""
        result = validate_ingested_data(
            record_count=0,  # Invalid
            size_mb=500,
            has_schema=True
        )
        assert result is False

    def test_no_schema_rejected(self):
        """Data without schema should be rejected."""
        result = validate_ingested_data(
            record_count=1000,
            size_mb=500,
            has_schema=False  # Invalid
        )
        assert result is False

    def test_oversized_data_rejected(self):
        """Data exceeding size limit should be rejected."""
        result = validate_ingested_data(
            record_count=1000,
            size_mb=11000,  # Exceeds 10000 limit
            has_schema=True
        )
        assert result is False


class TestDataQualityValidation:
    """Test data quality validation."""

    def test_valid_data_quality(self):
        """High quality data should pass."""
        result = validate_data_quality(
            completeness_score=0.95,
            error_rate=0.02,
            duplicate_rate=0.05
        )
        assert result is True

    def test_low_completeness_rejected(self):
        """Low completeness score should be rejected."""
        result = validate_data_quality(
            completeness_score=0.7,  # Below 0.8 threshold
            error_rate=0.02,
            duplicate_rate=0.05
        )
        assert result is False

    def test_high_error_rate_rejected(self):
        """High error rate should be rejected."""
        result = validate_data_quality(
            completeness_score=0.95,
            error_rate=0.1,  # Above 0.05 threshold
            duplicate_rate=0.05
        )
        assert result is False

    def test_high_duplicate_rate_rejected(self):
        """High duplicate rate should be rejected."""
        result = validate_data_quality(
            completeness_score=0.95,
            error_rate=0.02,
            duplicate_rate=0.15  # Above 0.1 threshold
        )
        assert result is False


class TestTransformationValidation:
    """Test transformation stage validation."""

    def test_valid_transformation_input(self):
        """Valid transformation input should pass."""
        result = validate_transformation_input(
            input_record_count=1000,
            transformation_type="map",
            has_mapping_rules=True
        )
        assert result is True

    def test_no_input_records_rejected(self):
        """Transformation without input records should be rejected."""
        with pytest.raises(ContractViolationError) as exc_info:
            validate_transformation_input(
                input_record_count=0,  # Invalid
                transformation_type="map",
                has_mapping_rules=True
            )
        assert "has_records" in str(exc_info.value)

    def test_no_mapping_rules_rejected(self):
        """Transformation without mapping rules should be rejected."""
        with pytest.raises(ContractViolationError) as exc_info:
            validate_transformation_input(
                input_record_count=1000,
                transformation_type="map",
                has_mapping_rules=False  # Invalid
            )
        assert "has_rules" in str(exc_info.value)

    def test_filter_transformation_valid(self):
        """Filter transformation can reduce record count."""
        result = validate_transformation_output(
            input_count=1000,
            output_count=800,  # Reduced by filter
            transformation_type="filter"
        )
        assert result is True

    def test_filter_cannot_increase_count(self):
        """Filter transformation cannot increase record count."""
        result = validate_transformation_output(
            input_count=1000,
            output_count=1200,  # Invalid: increased
            transformation_type="filter"
        )
        assert result is False

    def test_map_transformation_preserves_count(self):
        """Map transformation must preserve record count."""
        result = validate_transformation_output(
            input_count=1000,
            output_count=1000,  # Same count
            transformation_type="map"
        )
        assert result is True

    def test_map_different_count_rejected(self):
        """Map transformation with different count should be rejected."""
        result = validate_transformation_output(
            input_count=1000,
            output_count=800,  # Invalid: different
            transformation_type="map"
        )
        assert result is False

    def test_aggregate_reduces_count(self):
        """Aggregate transformation typically reduces count."""
        result = validate_transformation_output(
            input_count=1000,
            output_count=100,  # Aggregated
            transformation_type="aggregate"
        )
        assert result is True

    def test_expand_increases_count(self):
        """Expand transformation can increase count."""
        result = validate_transformation_output(
            input_count=1000,
            output_count=3000,  # Expanded
            transformation_type="expand"
        )
        assert result is True

    def test_expand_cannot_decrease_count(self):
        """Expand transformation cannot decrease count."""
        result = validate_transformation_output(
            input_count=1000,
            output_count=800,  # Invalid: decreased
            transformation_type="expand"
        )
        assert result is False


class TestEnrichmentValidation:
    """Test data enrichment validation."""

    def test_valid_enrichment_input(self):
        """Valid enrichment input should pass."""
        result = validate_enrichment_input(
            primary_record_count=1000,
            enrichment_source="customer_database",
            join_key="customer_id"
        )
        assert result is True

    def test_no_primary_data_rejected(self):
        """Enrichment without primary data should be rejected."""
        with pytest.raises(ContractViolationError) as exc_info:
            validate_enrichment_input(
                primary_record_count=0,  # Invalid
                enrichment_source="customer_database",
                join_key="customer_id"
            )
        assert "has_primary_data" in str(exc_info.value)

    def test_valid_enrichment_result(self):
        """Valid enrichment result should pass."""
        result = validate_enrichment_result(
            input_count=1000,
            enriched_count=950,
            match_rate=0.95
        )
        assert result is True

    def test_enriched_exceeds_input_rejected(self):
        """Enriched count exceeding input should be rejected."""
        result = validate_enrichment_result(
            input_count=1000,
            enriched_count=1200,  # Invalid: exceeds input
            match_rate=0.95
        )
        assert result is False

    def test_low_match_rate_rejected(self):
        """Low match rate should be rejected."""
        result = validate_enrichment_result(
            input_count=1000,
            enriched_count=400,
            match_rate=0.4  # Below 0.5 threshold
        )
        assert result is False


class TestExportValidation:
    """Test data export validation."""

    def test_valid_export_config(self):
        """Valid export configuration should pass."""
        result = validate_export_config(
            destination="s3://bucket/output",
            format="parquet",
            batch_size=1000
        )
        assert result is True

    def test_excessive_batch_size_rejected(self):
        """Batch size > 10000 should be rejected."""
        with pytest.raises(ContractViolationError) as exc_info:
            validate_export_config(
                destination="s3://bucket/output",
                format="parquet",
                batch_size=15000  # Invalid
            )
        assert "valid_batch_size" in str(exc_info.value)

    def test_valid_export_result(self):
        """Valid export result should pass."""
        result = validate_export_result(
            total_records=1000,
            exported_records=999,
            failed_records=1
        )
        assert result is True

    def test_counts_dont_match_rejected(self):
        """Export result with mismatched counts should be rejected."""
        result = validate_export_result(
            total_records=1000,
            exported_records=900,
            failed_records=50  # Total doesn't match
        )
        assert result is False

    def test_high_failure_rate_rejected(self):
        """High failure rate (> 1%) should be rejected."""
        result = validate_export_result(
            total_records=1000,
            exported_records=980,
            failed_records=20  # 2% failure rate
        )
        assert result is False


class TestStateTransitions:
    """Test pipeline state transitions."""

    def test_ingest_to_validate_valid(self):
        """Transition from ingest to validate should be valid."""
        result = can_transition_to_stage(
            current_stage="ingest",
            next_stage="validate",
            current_stage_complete=True
        )
        assert result is True

    def test_cannot_transition_if_incomplete(self):
        """Cannot transition if current stage not complete."""
        result = can_transition_to_stage(
            current_stage="ingest",
            next_stage="validate",
            current_stage_complete=False  # Incomplete
        )
        assert result is False

    def test_validate_to_transform_valid(self):
        """Transition from validate to transform should be valid."""
        result = can_transition_to_stage(
            current_stage="validate",
            next_stage="transform",
            current_stage_complete=True
        )
        assert result is True

    def test_transform_to_enrich_valid(self):
        """Transition from transform to enrich should be valid."""
        result = can_transition_to_stage(
            current_stage="transform",
            next_stage="enrich",
            current_stage_complete=True
        )
        assert result is True

    def test_transform_to_export_valid(self):
        """Transition from transform directly to export should be valid."""
        result = can_transition_to_stage(
            current_stage="transform",
            next_stage="export",
            current_stage_complete=True
        )
        assert result is True

    def test_enrich_to_export_valid(self):
        """Transition from enrich to export should be valid."""
        result = can_transition_to_stage(
            current_stage="enrich",
            next_stage="export",
            current_stage_complete=True
        )
        assert result is True

    def test_invalid_transition_rejected(self):
        """Invalid stage transition should be rejected."""
        result = can_transition_to_stage(
            current_stage="ingest",
            next_stage="transform",  # Skipping validate
            current_stage_complete=True
        )
        assert result is False

    def test_backward_transition_rejected(self):
        """Backward transition should be rejected."""
        result = can_transition_to_stage(
            current_stage="transform",
            next_stage="validate",  # Going backward
            current_stage_complete=True
        )
        assert result is False


class TestRetryLogic:
    """Test retry logic validation."""

    def test_should_retry_transient_error(self):
        """Should retry transient errors within retry limit."""
        result = should_retry_stage(
            error_count=2,
            max_retries=5,
            is_transient_error=True
        )
        assert result is True

    def test_no_retry_max_reached(self):
        """Should not retry if max retries reached."""
        result = should_retry_stage(
            error_count=5,
            max_retries=5,
            is_transient_error=True
        )
        assert result is False

    def test_no_retry_permanent_error(self):
        """Should not retry permanent errors."""
        result = should_retry_stage(
            error_count=1,
            max_retries=5,
            is_transient_error=False  # Permanent error
        )
        assert result is False


class TestBatchProcessing:
    """Test batch processing validation."""

    def test_valid_batch_config(self):
        """Valid batch configuration should pass."""
        result = validate_batch_config(
            batch_size=1000,
            total_records=50000,
            max_parallel_batches=10
        )
        assert result is True

    def test_excessive_parallel_batches_rejected(self):
        """Too many parallel batches should be rejected."""
        with pytest.raises(ContractViolationError) as exc_info:
            validate_batch_config(
                batch_size=1000,
                total_records=50000,
                max_parallel_batches=150  # Invalid
            )
        assert "valid_parallel" in str(exc_info.value)

    def test_calculate_batch_count_exact(self):
        """Calculate batch count for exact division."""
        result = calculate_batch_count(
            total_records=10000,
            batch_size=1000
        )
        assert result == 10

    def test_calculate_batch_count_with_remainder(self):
        """Calculate batch count with remainder."""
        result = calculate_batch_count(
            total_records=10500,
            batch_size=1000
        )
        assert result == 11  # 10 full batches + 1 partial


class TestPipelineCompletion:
    """Test pipeline completion validation."""

    def test_all_stages_complete(self):
        """Pipeline complete when all stages done."""
        result = is_pipeline_complete(
            ingestion_done=True,
            validation_done=True,
            transformation_done=True,
            enrichment_done=True,
            export_done=True
        )
        assert result is True

    def test_incomplete_stages(self):
        """Pipeline incomplete if any stage not done."""
        result = is_pipeline_complete(
            ingestion_done=True,
            validation_done=True,
            transformation_done=True,
            enrichment_done=False,  # Not done
            export_done=False
        )
        assert result is False


class TestSchemaValidation:
    """Test schema compliance validation."""

    def test_valid_schema_compliance(self):
        """Valid schema compliance should pass."""
        result = validate_schema_compliance(
            required_fields_count=10,
            present_fields_count=10,
            type_mismatch_count=0
        )
        assert result is True

    def test_missing_fields_rejected(self):
        """Missing required fields should be rejected."""
        result = validate_schema_compliance(
            required_fields_count=10,
            present_fields_count=8,  # Missing 2 fields
            type_mismatch_count=0
        )
        assert result is False

    def test_type_mismatches_rejected(self):
        """Type mismatches should be rejected."""
        result = validate_schema_compliance(
            required_fields_count=10,
            present_fields_count=10,
            type_mismatch_count=2  # 2 type mismatches
        )
        assert result is False


class TestThroughputValidation:
    """Test throughput performance validation."""

    def test_valid_throughput(self):
        """Valid throughput should pass."""
        result = validate_throughput(
            records_processed=10000,
            time_seconds=100,
            min_records_per_second=50
        )
        assert result is True  # 100 records/sec > 50 min

    def test_low_throughput_rejected(self):
        """Low throughput should be rejected."""
        result = validate_throughput(
            records_processed=1000,
            time_seconds=100,
            min_records_per_second=50
        )
        assert result is False  # 10 records/sec < 50 min


class TestErrorThresholds:
    """Test error threshold validation."""

    def test_within_error_threshold(self):
        """Error rate within threshold should pass."""
        result = is_error_threshold_exceeded(
            error_count=10,
            total_records=10000,
            max_error_rate=0.01
        )
        assert result is False  # 0.1% < 1%

    def test_exceeded_error_threshold(self):
        """Error rate exceeding threshold should fail."""
        result = is_error_threshold_exceeded(
            error_count=200,
            total_records=10000,
            max_error_rate=0.01
        )
        assert result is True  # 2% > 1%


class TestEndToEndWorkflow:
    """Test complete data processing workflow."""

    def test_successful_pipeline(self):
        """Test complete successful workflow."""
        # Stage 1: Ingestion
        assert validate_ingestion_input(
            "https://api.example.com/data", "json", 1000
        ) is True

        assert validate_ingested_data(10000, 500, True) is True

        # Transition to validation
        assert can_transition_to_stage("ingest", "validate", True) is True

        # Stage 2: Validation
        assert validate_data_quality(0.95, 0.02, 0.05) is True
        assert validate_schema_compliance(10, 10, 0) is True

        # Transition to transformation
        assert can_transition_to_stage("validate", "transform", True) is True

        # Stage 3: Transformation
        assert validate_transformation_input(10000, "map", True) is True
        assert validate_transformation_output(10000, 10000, "map") is True

        # Transition to enrichment
        assert can_transition_to_stage("transform", "enrich", True) is True

        # Stage 4: Enrichment
        assert validate_enrichment_input(10000, "customer_db", "id") is True
        assert validate_enrichment_result(10000, 9500, 0.95) is True

        # Transition to export
        assert can_transition_to_stage("enrich", "export", True) is True

        # Stage 5: Export
        assert validate_export_config("s3://bucket/output", "parquet", 1000) is True
        assert validate_export_result(9500, 9495, 5) is True

        # Check completion
        assert is_pipeline_complete(True, True, True, True, True) is True

    def test_blocked_pipeline(self):
        """Test workflow correctly blocks invalid sequences."""
        # Cannot skip validation stage
        assert can_transition_to_stage("ingest", "transform", True) is False

        # Cannot transition with incomplete stage
        assert can_transition_to_stage("ingest", "validate", False) is False

    def test_quality_gates(self):
        """Test quality gates block low-quality data."""
        # Low quality data rejected
        assert validate_data_quality(0.7, 0.02, 0.05) is False

        # High error rate rejected
        assert validate_data_quality(0.95, 0.1, 0.05) is False

        # Schema violations rejected
        assert validate_schema_compliance(10, 8, 0) is False


if __name__ == "__main__":
    # Run tests with verbose output
    pytest.main([__file__, "-v", "--tb=short"])
