def detect_threshold_anomaly(data:dict) -> dict:
    """
    最小阈值异常检测。
    输入：一条已经通过 payload_validator 校验的设备数据。
    输出：是否异常、异常原因、严重程度。    
    """
    reasons = []

    if data["temperature"] > 85:
        reasons.append(f"temperature too high: {data['temperature']}")

    if data["vibration"] > 5:
        reasons.append(f"vibration too high:{data['vibration']}")

    if data["current"] >20 :
        reasons.append(f"current too high:{data['current']}")

    if not reasons:
        return{
            "is_anomaly":False,
            "alarm_type":None,
            "alarm_reason":None,
            "severity":"normal",
        }
    
    return {
        "is_anomaly":True,
        "alarm_type": "threshold",
        "alarm_reason": "; ".join(reasons),
        "severity":"high",
        }
