import math


def calculate_mean(values: list[float]) -> float:
    if not values:
        raise ValueError("values must not be empty")
    return sum(values) / len(values)


def calculate_zscore(value: float,history_values: list[float]) -> float:
    """
    计算value相对于历史数据的z-score
    如果历史数据为空，或标准差为0，返回0.0，避免程序崩溃。
    """
    if not history_values:
        return 0.0
    
    mean = sum(history_values) / len(history_values)

    variance = sum((x - mean) ** 2 for x in history_values ) / len(history_values)
    std = math.sqrt(variance)

    if std == 0:
        return 0.0
    
    return (value - mean) / std


def detect_zsore_anomaly(
        data: dict,
        history_value: list[float],
        field: str = "temperature",
        threshold: float = 3.0,
) -> dict: 
    """
    使用 Z-score 判断某个字段是否异常。
    默认判断 temperature.
    """
    value = float(data[field])
    zscore = calculate_zscore(value,history_value)

    if abs(zscore) >= threshold:
        return {
            "is_anomaly": True,
            "alarm_type": "zscore",
            "alarm_reason": f"{field} zscore too high: value={value},zscore={zscore:.2f}",
            "severity": "medium",
            "zscore": round(zscore,2),
        }
    
    return {
        "is_anomaly": False,
        "alarm_type": None,
        "alarm_reason":None,
        "severity": "normal",
        "zscore": round(zscore, 2),
    }