## MVP 演示验收

已验证完整本地链路：

```text
Python 模拟设备 → MQTT Broker → Gateway 校验与入库
→ 阈值报警 → SQLite → PySide6 Dashboard

# 设备白名单设计

## 目标

限制只有已登记设备可以向网关上传数据。

## 配置文件

设备白名单配置位于：

```text
configs/devices.json
