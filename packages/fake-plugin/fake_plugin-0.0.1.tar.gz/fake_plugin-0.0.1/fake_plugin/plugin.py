import os
from time import sleep
from .interface import (
    PluginInterface,
    Backend,
    Metadata,
    ResultType,
    QasmFilePath,
    check_backend,
    check_result_type,
    check_qasm_file,
    Results,
)


class Plugin(PluginInterface):
    """
    The Plugin class is the starting point for quantum-plugins.
    Using this, the server worker can interect directly with
    simulators.
    """

    def __init__(self):
        current_file_path = os.path.dirname(__file__)
        backends_relative_path = os.path.join(current_file_path, "backends.txt")

        with open(backends_relative_path, "r", encoding="UTF-8") as file:
            backends = list(map(lambda x: x.replace("\n", ""), file))
            super().__init__(backends)

    @check_backend
    @check_result_type
    @check_qasm_file
    def execute(
        self,
        target_backend: Backend,
        qasm_file_path: QasmFilePath,
        metadata: Metadata,
        result_type: ResultType,
    ) -> Results:
        """
        A fake execution method which returns fake data.
        """

        data_for_returning = {
            "counts": {"00": 500, "11": 500},
            "quasi_dist": {0: 0.5, 3: 0.5},
            "expval": [1],
        }

        if result_type == "expval":
            assert metadata.get("obs") is not None, "Invalid observables"
            
        sleep(10) # simulate a job running

        return data_for_returning[result_type]  # type: ignore
