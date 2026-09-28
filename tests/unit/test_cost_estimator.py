from app.services.cost_estimator import calculate_cost_estimate


def test_cost_estimate_has_required_fields(sample_brief):
    result = calculate_cost_estimate(sample_brief)

    assert "estimated_total" in result
    assert "rag_saving_amount" in result
    assert "rag_saving_percentage" in result


def test_saving_equals_difference(sample_brief):
    result = calculate_cost_estimate(sample_brief)

    expected_saving = round(result["estimated_cost_without_reuse"] - result["estimated_total"], 2)
    assert result["rag_saving_amount"] == expected_saving


def test_cost_is_never_negative(sample_brief):
    result = calculate_cost_estimate(sample_brief)

    assert result["estimated_total"] >= 0
    assert result["rag_saving_amount"] >= 0