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

# 安全设计说明

## 1. 设备白名单

白名单文件：

`configs/devices.json`

只有 `allowed_devices` 中登记的设备编号可以通过网关准入校验。

当前允许设备：

- motor_001

## 2. HMAC-SHA256 签名

设备端与网关通过环境变量 `IOT_HMAC_SECRET` 使用同一个共享密钥。

签名覆盖除 `signature` 外的全部 payload 字段。

网关处理顺序：

1. JSON 解析
2. 字段校验
3. 设备白名单校验
4. HMAC 签名校验
5. SQLite 入库
6. 异常检测与报警入库

## 3. 当前边界

HMAC 用于验证消息来源和完整性，不负责加密。

当前版本未加入 timestamp 时间窗口和 nonce 去重，因此防重放保护后续实现。

README 只加一段：

## 安全机制

- 设备白名单：拒绝未登记设备
- HMAC-SHA256：拒绝未签名、错误签名或被篡改的数据
- 当前安全设计说明见 `docs/security_design.md`


---
## HMAC 本地运行说明

网关会对 MQTT 数据执行设备白名单和 HMAC 签名校验。
只有字段校验、白名单校验、HMAC 校验均通过的数据，才会写入 SQLite。

本地演示时，需要在发布器和网关终端设置相同环境变量：

```powershell
$env:IOT_HMAC_SECRET = "本地测试密钥"

运行顺序：

1. 启动 Mosquitto Broker


2. 启动 gateway.mqtt_subscriber


3. 启动 simulators.mqtt_publisher


4. 启动 simulators.abnormal_publisher 验证报警链路



安全说明：HMAC 用于验证消息来源和完整性，不用于加密 MQTT 负载内容。

再在 README 顶部加一句当前状态：

```md