import pytest
from fake_plugin import Plugin


class TestReturningData:
    """
    Tests to check that all types of results are returning data correctly
    """

    def test_counts(self):
        p = Plugin()
        result = p.execute(
            metadata={},
            qasm_file_path="./tests/test.qasm",
            result_type="counts",
            target_backend="fake1",
        )

        zero = result.get("00")
        three = result.get("11")

        assert zero == 500
        assert three == 500

    def test_quasi(self):
        p = Plugin()
        result = p.execute(
            metadata={},
            qasm_file_path="./tests/test.qasm",
            result_type="quasi_dist",
            target_backend="fake1",
        )

        zero = result.get(0)
        three = result.get(3)

        assert zero == 0.5
        assert three == 0.5

    def test_expval_failed(self):
        p = Plugin()

        with pytest.raises(AssertionError):
            p.execute(
                metadata={},
                qasm_file_path="./tests/test.qasm",
                result_type="expval",
                target_backend="fake1",
            )

    def test_expval_success(self):
        p = Plugin()

        results = p.execute(
            metadata={"obs": []},
            qasm_file_path="./tests/test.qasm",
            result_type="expval",
            target_backend="fake1",
        )

        assert len(results) == 1
        assert results[0] == 1
