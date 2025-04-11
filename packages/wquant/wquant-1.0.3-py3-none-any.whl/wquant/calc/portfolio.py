from abc import ABC, abstractmethod
from typing import Any, Dict, List, Union

import numpy as np
import pandas as pd


class ReturnsDataLoader:
    """标准化收益率数据容器"""

    def __init__(self, returns: Any, period: int):
        """

        Args:
            returns (Any): 支持多种格似的收益率输入。
            period (int): 计算年化时使用的周期，如输入的数据为日度，则为250或者252。
        """
        self.returns = self._process_returns(returns)
        self.period = period

    def _process_returns(self, input_data: Any) -> pd.Series:
        """统一处理不同格似的收益率输入"""
        # 处理空值
        if input_data is None:
            raise ValueError("输入的数据不能为None")

        # 格式转化
        if isinstance(input_data, pd.Series):
            processed = input_data.copy()

        elif isinstance(input_data, pd.DataFrame):
            if input_data.shape[1] != 1:
                raise ValueError("若输入DataFrame则必须为单列")
            processed = input_data.iloc[:, 0]

        elif isinstance(input_data, (list, tuple)):
            processed = pd.Series(input_data)

        elif isinstance(input_data, np.ndarray):
            if input_data.ndim != 1:
                raise ValueError("numpy数组必须为一维")
            processed = pd.Series(input_data)

        else:
            try:
                processed = pd.Series(list(input_data))
            except Exception as e:
                raise TypeError(f"不支持的数据类型: {type(input_data)}") from e

        # 类型校验及转换
        if not pd.api.types.is_numeric_dtype(processed):
            processed = pd.to_numeric(processed, errors="coerce")
            if processed.isna().any():
                raise ValueError("包含非数值元素。")

        return processed


class CalculatorError(Exception):
    """计算异常类"""

    pass


class IndicatorCalculator(ABC):
    """指标计算器抽象基类"""

    @abstractmethod
    def calculate(self, data: ReturnsDataLoader) -> Union[float, Dict]:
        """执行计算并返回结果"""
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """返回指标的名称"""
        pass


class AnnualizedReturn(IndicatorCalculator):
    """年化收益率"""

    @property
    def name(self):
        return "annualized_return"

    def calculate(self, data):
        returns = data.returns
        n = len(returns)
        cum_return = (1 + returns).prod()
        return cum_return ** (data.period / n) - 1


class CummulativeReturn(IndicatorCalculator):
    """总收益"""

    @property
    def name(self):
        return "cummulative_return"

    def calculate(self, data):
        returns = data.returns
        return (1 + returns).prod() - 1


class AnnualizedVolatility(IndicatorCalculator):
    """年化波动率"""

    def __init__(self, ddof: int = 1):
        self.ddof = ddof

    @property
    def name(self):
        return "annualized_volatility"

    def calculate(self, data):
        returns = data.returns

        period_volatility = returns.std(ddof=self.ddof)
        return period_volatility * np.sqrt(data.period)


class SharpeRatio(IndicatorCalculator):
    """夏普比率"""

    def __init__(self, risk_free_rate: float = 0.02):
        self.risk_free_rate = risk_free_rate  # 年化无风险利率

    @property
    def name(self):
        return "sharpe_ratio"

    def calculate(self, data):
        returns = data.returns

        # 年化收益
        n = len(returns)
        cum_return = (1 + returns).prod()
        ann_return = cum_return ** (data.period / n) - 1

        # 超额收益
        excess_return = ann_return - self.risk_free_rate

        # 年化波动率
        period_vol = returns.std()
        annualized_vol = period_vol * np.sqrt(data.period)

        return (excess_return / annualized_vol) if annualized_vol != 0 else 0


class MaxDrawdown(IndicatorCalculator):
    """最大回撤"""
        
    @property
    def name(self):
        return "max_drawdown"

    def calculate(self, data):
        returns = data.returns

        cum_returns = (1 + returns).cumprod()
        peak = cum_returns.expanding(min_periods=1).max()
        return (cum_returns / peak - 1).min()


class CalmarRatio(IndicatorCalculator):
    """卡玛比率"""

    @property
    def name(self):
        return "calmar_ratio"

    def calculate(self, data):
        returns = data.returns

        # 计算年化收益率
        n = len(returns)
        cum_return = (1 + returns).prod()
        ann_return = cum_return ** (data.period / n) - 1

        # 计算最大回撤
        cum_returns = (1 + returns).cumprod()
        peak = cum_returns.expanding(min_periods=1).max()
        max_drawdown = (cum_returns / peak - 1).min()

        return (ann_return / abs(max_drawdown)) if max_drawdown != 0 else 0


class MetricsEngine:
    """指标计算引擎"""

    def __init__(self):
        self._calculators = {}

    def register(self, calculator: IndicatorCalculator):
        """注册指标计算器"""
        if not isinstance(calculator, IndicatorCalculator):
            raise CalculatorError("无效的指标计算器类型")
        self._calculators[calculator.name] = calculator

    def _compute_single(self, data: ReturnsDataLoader, metric: str):
        """执行单个指标计算"""
        if metric not in self._calculators:
            raise CalculatorError(f"未注册的指标：{metric}")

        try:
            return {
                "metric": metric,
                "value": self._calculators[metric].calculate(data),
                "status": "success",
            }

        except Exception as e:
            return {"metric": metric, "error": str(e), "status": "failed"}

    def compute(
        self, data: ReturnsDataLoader, metrics: Union[str, List[str]] = None
    ) -> Dict:
        """执行指标计算"""
        if metrics is None:
            return self.compute_all(data)
        elif isinstance(metrics, str):
            return self._compute_single(data, metrics)
        else:
            return {m: self._compute_single(data, m) for m in metrics}

    def compute_all(self, data: ReturnsDataLoader) -> Dict:
        """计算所有已经注册的指标"""
        return {
            name: self._compute_single(data, name) for name in self._calculators.keys()
        }

    @property
    def registered_metrics(self) -> List[str]:
        """返回所有已注册指标名称列表"""
        return list(self._calculators.keys())

