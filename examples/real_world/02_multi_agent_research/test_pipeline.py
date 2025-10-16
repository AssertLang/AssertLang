"""
Test suite for Multi-Agent Research Pipeline with Contract Validation

Demonstrates how contracts coordinate multi-agent workflows and validate
agent inputs/outputs.
"""

import pytest
import sys
from pathlib import Path

# Add project root and current directory to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(Path(__file__).parent))

from assertlang.runtime.contracts import ContractViolationError
from pipeline import (
    validate_research_query,
    validate_research_results,
    validate_analysis_input,
    validate_analysis_output,
    validate_report_input,
    validate_final_report,
    can_agent_proceed,
    validate_pipeline_stage,
    meets_quality_threshold,
    validate_task_assignment,
    is_pipeline_complete
)


class TestResearchQueryValidation:
    """Test research agent query input validation."""

    def test_valid_query(self):
        """Valid research query should pass."""
        result = validate_research_query(
            query="What are the latest trends in AI?",
            max_results=10,
            min_quality_score=0.7
        )
        assert result is True

    def test_empty_query_rejected(self):
        """Empty query should be rejected."""
        with pytest.raises(ContractViolationError) as exc_info:
            validate_research_query(
                query="",  # Invalid
                max_results=10,
                min_quality_score=0.7
            )
        assert "non_empty_query" in str(exc_info.value)

    def test_excessive_max_results_rejected(self):
        """Max results > 100 should be rejected."""
        with pytest.raises(ContractViolationError) as exc_info:
            validate_research_query(
                query="AI trends",
                max_results=150,  # Invalid
                min_quality_score=0.7
            )
        assert "positive_max_results" in str(exc_info.value)

    def test_invalid_quality_score_rejected(self):
        """Quality score > 1.0 should be rejected."""
        with pytest.raises(ContractViolationError) as exc_info:
            validate_research_query(
                query="AI trends",
                max_results=10,
                min_quality_score=1.5  # Invalid
            )
        assert "valid_quality_score" in str(exc_info.value)


class TestResearchResultsValidation:
    """Test research agent output validation."""

    def test_valid_results(self):
        """Valid research results should pass."""
        result = validate_research_results(
            results_count=5,
            quality_score=0.8,
            has_sources=True
        )
        assert result is True

    def test_no_results_rejected(self):
        """Zero results should be rejected."""
        result = validate_research_results(
            results_count=0,  # Invalid
            quality_score=0.8,
            has_sources=True
        )
        assert result is False

    def test_no_sources_rejected(self):
        """Results without sources should be rejected."""
        result = validate_research_results(
            results_count=5,
            quality_score=0.8,
            has_sources=False  # Invalid
        )
        assert result is False

    def test_low_quality_rejected(self):
        """Low quality results should be rejected."""
        result = validate_research_results(
            results_count=5,
            quality_score=0.2,  # Below 0.3 threshold
            has_sources=True
        )
        assert result is False


class TestAnalysisValidation:
    """Test analyzer agent validation."""

    def test_valid_analysis_input(self):
        """Valid analysis input should pass."""
        result = validate_analysis_input(
            research_data_size=100,
            analysis_depth="deep"
        )
        assert result is True

    def test_no_data_rejected(self):
        """Analysis without data should be rejected."""
        with pytest.raises(ContractViolationError) as exc_info:
            validate_analysis_input(
                research_data_size=0,  # Invalid
                analysis_depth="deep"
            )
        assert "has_data" in str(exc_info.value)

    def test_valid_analysis_output(self):
        """Valid analysis output should pass."""
        result = validate_analysis_output(
            insights_count=3,
            confidence_score=0.7,
            has_evidence=True
        )
        assert result is True

    def test_no_insights_rejected(self):
        """Analysis without insights should be rejected."""
        result = validate_analysis_output(
            insights_count=0,  # Invalid
            confidence_score=0.7,
            has_evidence=True
        )
        assert result is False

    def test_no_evidence_rejected(self):
        """Analysis without evidence should be rejected."""
        result = validate_analysis_output(
            insights_count=3,
            confidence_score=0.7,
            has_evidence=False  # Invalid
        )
        assert result is False

    def test_low_confidence_rejected(self):
        """Low confidence analysis should be rejected."""
        result = validate_analysis_output(
            insights_count=3,
            confidence_score=0.3,  # Below 0.4 threshold
            has_evidence=True
        )
        assert result is False


class TestReportValidation:
    """Test writer agent validation."""

    def test_valid_report_input(self):
        """Valid report input should pass."""
        result = validate_report_input(
            analysis_size=50,
            target_length=1000,
            format="markdown"
        )
        assert result is True

    def test_excessive_length_rejected(self):
        """Report length > 10000 should be rejected."""
        with pytest.raises(ContractViolationError) as exc_info:
            validate_report_input(
                analysis_size=50,
                target_length=15000,  # Invalid
                format="markdown"
            )
        assert "positive_length" in str(exc_info.value)

    def test_valid_final_report(self):
        """Valid final report should pass."""
        result = validate_final_report(
            report_length=500,
            section_count=5,
            has_citations=True
        )
        assert result is True

    def test_short_report_rejected(self):
        """Report < 100 chars should be rejected."""
        result = validate_final_report(
            report_length=50,  # Too short
            section_count=5,
            has_citations=True
        )
        assert result is False

    def test_few_sections_rejected(self):
        """Report < 3 sections should be rejected."""
        result = validate_final_report(
            report_length=500,
            section_count=2,  # Too few
            has_citations=True
        )
        assert result is False

    def test_no_citations_rejected(self):
        """Report without citations should be rejected."""
        result = validate_final_report(
            report_length=500,
            section_count=5,
            has_citations=False  # Invalid
        )
        assert result is False


class TestAgentCoordination:
    """Test multi-agent coordination logic."""

    def test_agent_can_proceed(self):
        """Agent can proceed when prerequisites met."""
        result = can_agent_proceed(
            agent_name="analyzer",
            previous_agent_completed=True,
            has_required_input=True
        )
        assert result is True

    def test_agent_blocked_by_previous(self):
        """Agent blocked if previous agent not complete."""
        result = can_agent_proceed(
            agent_name="analyzer",
            previous_agent_completed=False,  # Blocker
            has_required_input=True
        )
        assert result is False

    def test_agent_blocked_by_missing_input(self):
        """Agent blocked if missing required input."""
        result = can_agent_proceed(
            agent_name="analyzer",
            previous_agent_completed=True,
            has_required_input=False  # Blocker
        )
        assert result is False


class TestPipelineStageValidation:
    """Test pipeline stage ordering."""

    def test_research_stage_always_valid(self):
        """Research stage can always start."""
        result = validate_pipeline_stage(
            current_stage="research",
            research_complete=False,
            analysis_complete=False
        )
        assert result is True

    def test_analysis_requires_research(self):
        """Analysis stage requires research complete."""
        # Valid: research complete
        assert validate_pipeline_stage(
            current_stage="analysis",
            research_complete=True,
            analysis_complete=False
        ) is True

        # Invalid: research not complete
        assert validate_pipeline_stage(
            current_stage="analysis",
            research_complete=False,
            analysis_complete=False
        ) is False

    def test_writing_requires_both(self):
        """Writing stage requires both research and analysis complete."""
        # Valid: both complete
        assert validate_pipeline_stage(
            current_stage="writing",
            research_complete=True,
            analysis_complete=True
        ) is True

        # Invalid: only research complete
        assert validate_pipeline_stage(
            current_stage="writing",
            research_complete=True,
            analysis_complete=False
        ) is False

        # Invalid: only analysis complete
        assert validate_pipeline_stage(
            current_stage="writing",
            research_complete=False,
            analysis_complete=True
        ) is False


class TestQualityThreshold:
    """Test quality threshold checking."""

    def test_meets_threshold(self):
        """Quality meeting threshold should pass."""
        result = meets_quality_threshold(
            quality_score=0.8,
            required_threshold=0.7
        )
        assert result is True

    def test_below_threshold(self):
        """Quality below threshold should fail."""
        result = meets_quality_threshold(
            quality_score=0.6,
            required_threshold=0.7
        )
        assert result is False

    def test_exact_threshold(self):
        """Quality exactly at threshold should pass."""
        result = meets_quality_threshold(
            quality_score=0.7,
            required_threshold=0.7
        )
        assert result is True


class TestTaskAssignment:
    """Test agent role-task compatibility."""

    def test_researcher_valid_tasks(self):
        """Researcher can do research tasks."""
        assert validate_task_assignment(
            agent_role="researcher",
            task_type="research",
            has_required_tools=True
        ) is True

        assert validate_task_assignment(
            agent_role="researcher",
            task_type="search",
            has_required_tools=True
        ) is True

    def test_researcher_invalid_tasks(self):
        """Researcher cannot do non-research tasks."""
        assert validate_task_assignment(
            agent_role="researcher",
            task_type="writing",
            has_required_tools=True
        ) is False

    def test_analyzer_valid_tasks(self):
        """Analyzer can do analysis tasks."""
        assert validate_task_assignment(
            agent_role="analyzer",
            task_type="analysis",
            has_required_tools=True
        ) is True

        assert validate_task_assignment(
            agent_role="analyzer",
            task_type="synthesis",
            has_required_tools=True
        ) is True

    def test_writer_valid_tasks(self):
        """Writer can do writing tasks."""
        assert validate_task_assignment(
            agent_role="writer",
            task_type="writing",
            has_required_tools=True
        ) is True

        assert validate_task_assignment(
            agent_role="writer",
            task_type="reporting",
            has_required_tools=True
        ) is True

    def test_missing_tools_rejected(self):
        """Task assignment rejected if missing tools."""
        assert validate_task_assignment(
            agent_role="researcher",
            task_type="research",
            has_required_tools=False  # Invalid
        ) is False


class TestPipelineCompletion:
    """Test pipeline completion checking."""

    def test_all_complete(self):
        """Pipeline complete when all stages done."""
        result = is_pipeline_complete(
            research_done=True,
            analysis_done=True,
            writing_done=True
        )
        assert result is True

    def test_incomplete_stages(self):
        """Pipeline incomplete if any stage not done."""
        # Only research
        assert is_pipeline_complete(
            research_done=True,
            analysis_done=False,
            writing_done=False
        ) is False

        # Research and analysis
        assert is_pipeline_complete(
            research_done=True,
            analysis_done=True,
            writing_done=False
        ) is False

        # None complete
        assert is_pipeline_complete(
            research_done=False,
            analysis_done=False,
            writing_done=False
        ) is False


class TestEndToEndWorkflow:
    """Test complete multi-agent workflow."""

    def test_successful_pipeline(self):
        """Test complete successful workflow."""
        # Stage 1: Research
        assert validate_pipeline_stage("research", False, False) is True

        # Validate research query
        assert validate_research_query("AI trends 2025", 20, 0.7) is True

        # Validate research results
        assert validate_research_results(15, 0.8, True) is True

        # Stage 2: Analysis
        assert validate_pipeline_stage("analysis", True, False) is True
        assert can_agent_proceed("analyzer", True, True) is True

        # Validate analysis input
        assert validate_analysis_input(100, "deep") is True

        # Validate analysis output
        assert validate_analysis_output(5, 0.75, True) is True

        # Stage 3: Writing
        assert validate_pipeline_stage("writing", True, True) is True
        assert can_agent_proceed("writer", True, True) is True

        # Validate report input
        assert validate_report_input(50, 1500, "markdown") is True

        # Validate final report
        assert validate_final_report(1500, 6, True) is True

        # Check completion
        assert is_pipeline_complete(True, True, True) is True

    def test_blocked_workflow(self):
        """Test workflow correctly blocks invalid sequences."""
        # Cannot skip to analysis without research
        assert validate_pipeline_stage("analysis", False, False) is False

        # Cannot skip to writing without analysis
        assert validate_pipeline_stage("writing", True, False) is False

        # Agent blocked without prerequisites
        assert can_agent_proceed("analyzer", False, True) is False

    def test_quality_gates(self):
        """Test quality gates block low-quality work."""
        # Low quality research rejected
        assert validate_research_results(5, 0.2, True) is False

        # Low confidence analysis rejected
        assert validate_analysis_output(3, 0.3, True) is False

        # Poor report rejected
        assert validate_final_report(50, 2, False) is False


if __name__ == "__main__":
    # Run tests with verbose output
    pytest.main([__file__, "-v", "--tb=short"])
