import pytest
import polars as pl
import polars_financial.metrics  # noqa
from math import isclose
from polars_financial.days import DAILY, MONTHLY, WEEKLY

returns = {
    "empty": [],
    "none": [None, None],
    "one-return": [0.01],
    "simple-benchmark": [0.0, 0.01, 0.0, 0.01, 0.0, 0.01, 0.0, 0.01, 0.0],
    "mixed-nan": [float("nan"), 0.01, 0.1, -0.04, 0.02, 0.03, 0.02, 0.01, -0.1],
    "mixed-none": [None, 0.01, 0.1, -0.04, 0.02, 0.03, 0.02, 0.01, -0.1],
    "positive": [0.01, 0.02, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01],
    "negative": [0.0, -0.06, -0.07, -0.01, -0.09, -0.02, -0.06, -0.08, -0.05],
    "all—negative": [-0.02, -0.06, -0.07, -0.01, -0.09, -0.02, -0.06, -0.08, -0.05],
    "for-annual": [0.0, 0.01, 0.1, -0.04, 0.02, 0.03, 0.02, 0.01, -0.1],
    "flat-line": [0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01],
}


cum_return_test_data = [
    ("empty", []),
    ("none", [0, 0]),
    (
        "mixed-nan",
        [
            0,
            0.01,
            0.111,
            0.06656,
            0.0878912,
            0.1205279,
            0.1429385,
            0.1543679,
            0.0389311,
        ],
    ),
    (
        "mixed-none",
        [
            0,
            0.01,
            0.111,
            0.06656,
            0.0878912,
            0.1205279,
            0.1429385,
            0.1543679,
            0.0389311,
        ],
    ),
    (
        "negative",
        [
            0.0,
            -0.06,
            -0.1258,
            -0.134542,
            -0.2124332,
            -0.2281846,
            -0.2744935,
            -0.3325340,
            -0.3659073,
        ],
    ),
]

cum_return_final_test_data = [
    # ("empty", None),
    ("none", 0),
    ("mixed-nan", 0.0389311),
    ("mixed-none", 0.038931),
    ("negative", -0.3659073),
]


max_drawdown_test_data = [
    # ("empty", None),
    ("none", 0),
    ("one-return", 0),
    ("mixed-nan", -0.1),
    ("positive", 0),
    ("negative", -0.365907),
]

ann_return_test_data = [
    ("mixed-nan", DAILY, 1.9135925373194231),
    ("for-annual", WEEKLY, 0.24690830513998208),
    ("for-annual", MONTHLY, 0.052242061386048144),
]

ann_volatility_test_data = [
    ("flat-line", DAILY, 0.0),
    ("mixed-nan", DAILY, 0.9136465399704637),
    ("for-annual", WEEKLY, 0.38851569394870583),
    ("for-annual", MONTHLY, 0.18663690238892558),
]

calmar_ratio_test_data = [
    ("flat-line", DAILY, None),  # TODO: check if this is actually None?
    ("one-return", DAILY, None),  # TODO: check if this is actually None?
    ("mixed-nan", DAILY, 19.135925373194233),
    ("for-annual", WEEKLY, 2.4690830513998208),
    ("for-annual", MONTHLY, 0.52242061386048144),
]

sharpe_ratio_test_data = [
    ("empty", 0.0, None),
    ("none", 0.0, None),
    ("one-return", 0.0, None),
    ("mixed-nan", "mixed-nan", None),
    ("mixed-nan", 0.0, 1.7238613961),
    ("positive", 0.0, 52.9150262212),
    ("negative", 0.0, -24.406808633),
    ("flat-line", 0.0, float("inf")),
    (["mixed-nan", "simple-benchmark"], "simple-benchmark", 0.3411141144),
]

downside_risk_test_data = [
    ("empty", 0.0, DAILY, None),
    ("one-return", 0.0, DAILY, 0.0),
    ("mixed-nan", "mixed-nan", DAILY, 0.0),
    ("mixed-nan", 0.0, DAILY, 0.6044832503882),
    ("mixed-nan", 0.1, DAILY, 1.7161730681956),
    ("for-annual", 0.0, WEEKLY, 0.25888650451),
    ("for-annual", 0.1, WEEKLY, 0.773304597167),
    ("for-annual", 0.0, MONTHLY, 0.12436505404),
    ("for-annual", 0.1, MONTHLY, 0.37148351242),
]


def _test_single_value(data, input, expected, method, *args, **kwargs):

    if isinstance(input, list):
        schema = {inp: pl.Float64 for inp in input}
        data_dict = {inp: data[inp] for inp in input}

        input_first = input[0]
    else:
        schema = {input: pl.Float64}
        data_dict = {input: data[input]}
        input_first = input

    metric = getattr(pl.col(input_first).metrics, method)

    df_output = pl.DataFrame(data_dict, schema=schema).select(metric(*args, **kwargs))

    if expected is None:
        assert df_output[0, 0] is None
    else:
        assert isclose(df_output[0, 0], expected, rel_tol=1e-05)


@pytest.mark.parametrize("input, expected", max_drawdown_test_data)
def test_max_drawdown(input, expected):
    _test_single_value(returns, input, expected, "max_drawdown")


@pytest.mark.parametrize("input, expected", cum_return_final_test_data)
def test_cum_return_final(input, expected):
    _test_single_value(returns, input, expected, "cum_return_final")


@pytest.mark.parametrize("input, annual_obs, expected", ann_return_test_data)
def test_ann_return(input, annual_obs, expected):
    _test_single_value(returns, input, expected, "ann_return", annual_obs=annual_obs)


@pytest.mark.parametrize("input, annual_obs, expected", ann_volatility_test_data)
def test_ann_volatility(input, annual_obs, expected):
    _test_single_value(
        returns, input, expected, "ann_volatility", annual_obs=annual_obs
    )


@pytest.mark.parametrize("input, annual_obs, expected", calmar_ratio_test_data)
def test_calmar_ratio(input, annual_obs, expected):
    _test_single_value(returns, input, expected, "calmar_ratio", annual_obs=annual_obs)


@pytest.mark.parametrize("input, risk_free, expected", sharpe_ratio_test_data)
def test_ann_sharpe_ratio(input, risk_free, expected):
    _test_single_value(
        returns, input, expected, "ann_sharpe_ratio", risk_free=risk_free
    )


@pytest.mark.parametrize(
    "input, required_return, annual_obs, expected", downside_risk_test_data
)
def test_ann_downside_risk(input, required_return, annual_obs, expected):
    _test_single_value(
        returns,
        input,
        expected,
        "ann_downside_risk",
        required_return=required_return,
        annual_obs=annual_obs,
    )


up_capture_ratio_test_data = [
    ("empty", pl.col("empty"), DAILY, None),
    ("one-return", pl.col("one-return"), DAILY, 1.0),
    ("mixed-nan", pl.col("mixed-nan"), DAILY, 1.0),
    (["positive", "mixed-nan"], pl.col("mixed-nan"), DAILY, 0.0076167762),
    (["all—negative", "mixed-nan"], pl.col("mixed-nan"), DAILY, -0.0004336328),
]


@pytest.mark.parametrize(
    "input, benchmark, annual_obs, expected", up_capture_ratio_test_data
)
def test_up_capture_ratio(input, benchmark, annual_obs, expected):
    _test_single_value(
        returns,
        input,
        expected,
        "up_capture_ratio",
        benchmark=benchmark,
        annual_obs=annual_obs,
    )
