from alfasim_sdk import convert_description_to_alfacase
from pytest_regressions.file_regression import FileRegressionFixture

from alfasim_score.converter.alfacase.base_operation import BaseOperationBuilder
from alfasim_score.converter.alfacase.convert_alfacase import ScoreAlfacaseConverter


def test_create_alfacase_base(
    file_regression: FileRegressionFixture,
    alfacase_gas_lift: ScoreAlfacaseConverter,
) -> None:
    case_description = alfacase_gas_lift.build_base_alfacase_description()
    file_regression.check(
        convert_description_to_alfacase(case_description), encoding="utf-8", extension=".alfacase"
    )


def test_create_alfacase_base_operation_configuration(
    file_regression: FileRegressionFixture,
    base_operation_gas_lift: BaseOperationBuilder,
) -> None:
    configured_alfacase = base_operation_gas_lift.generate_operation_alfacase_description()
    file_regression.check(
        convert_description_to_alfacase(configured_alfacase),
        encoding="utf-8",
        extension=".alfacase",
    )
