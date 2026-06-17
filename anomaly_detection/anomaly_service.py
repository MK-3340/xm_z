from anomaly_detection.threshold_detector import detect_threshold_anomaly
from anomaly_detection.zscore_detector import detect_zsore_anomaly


def analyze_sensor_data(data: dict, history: dict[str, list[float]] | None = None) -> dict:
    """
    统一异常分析入口。

    逻辑：
    1. 先做阈值检测，严重超限直接报警；
    2. 阈值正常时，再用 Z-score 判断相对历史异常；
    3. 如果没有历史数据，就只返回正常结果。
    """
    threshold_result = detect_threshold_anomaly(data)

    if threshold_result["is_anomaly"]:
        return threshold_result
    
    if history is None:
        history = {}

    for field in ["temperature", "vibration", "current"]:
        history_values = history.get(field, [])

        zscore_result = detect_zsore_anomaly(
            data=data,
            history_value=history_values,
            field=field,
        )

        if zscore_result["is_anomaly"]:
            return zscore_result
        
        return {
            "is_anomaly": False,
            "alarm_type": None,
            "alarm_reason": None,
            "severity":"normal",
        }