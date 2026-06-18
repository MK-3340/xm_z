# 边缘智能工业物联网网关与设备异常检测系统

## Day 1：项目骨架与虚拟设备模拟器

今天完成了项目基础结构和第一个虚拟设备程序。

## 目录说明

- simulators/：存放虚拟设备模拟器
- gateway/：后续存放网关接收程序
- tests/：后续存放自动化测试
- docs/：存放项目文档、截图和学习记录

## 今日功能

虚拟设备 motor_001 每秒生成一条 JSON 格式的工业设备数据。

字段包括：

- device_id：设备编号
- timestamp：数据生成时间
- temperature：温度
- vibration：振动值
- current：电流
- status：设备状态

## 运行方式

```bash
python simulators/virtual_device.py
```

---

## Day 2：虚拟设备数据生成模块优化与单元测试

今天完成了虚拟设备模拟器的结构优化。

### 完成内容

- 将设备数据生成逻辑封装为 `generate_device_data()`
- 修复字段名错误：`tempeerature` 改为 `temperature`
- 新增 pytest 单元测试，验证字段完整性和数据范围
- 新增 `.gitignore`，避免提交虚拟环境和缓存文件

### 运行方式

运行虚拟设备：

```bash
python simulators/virtual_device.py
```

运行测试：

```bash
python -m pytest
```
---

## Day 3：MQTT 发布与订阅最小闭环

今天完成了虚拟设备数据通过 MQTT 发布，并由网关订阅端接收。

### 完成内容

- 新增 `simulators/mqtt_publisher.py`
- 新增 `gateway/mqtt_subscriber.py`
- 使用 topic：`factory/motor_001/telemetry`
- 虚拟设备每秒生成一条 JSON 数据，并发布到 MQTT Broker
- 网关订阅端接收并打印 JSON 消息

### 运行方式

启动 MQTT Broker：

```bash
mosquitto -v
---

---
```
## Day 4：本地 Mosquitto 与 MQTT 闭环验收

今天完成了本地 MQTT Broker 环境验证，并跑通了虚拟设备到网关订阅端的数据链路。

### 完成内容

- 启动本地 Mosquitto Broker
- 运行 `gateway/mqtt_subscriber.py` 订阅 topic
- 运行 `simulators/mqtt_publisher.py` 发布虚拟设备数据
- 验证 publisher → broker → subscriber 链路可用

### 当前链路

```text
virtual_device.py
        ↓
mqtt_publisher.py
        ↓
localhost:1883 Mosquitto
        ↓
mqtt_subscriber.py
```

### 运行命令

启动 Mosquitto：

```powershell
& "C:\Program Files\mosquitto\mosquitto.exe" -v
```

启动订阅端：

```powershell
python -m gateway.mqtt_subscriber
```

启动发布端：

```powershell
python -m simulators.mqtt_publisher
```

### 验收标准

订阅端能持续收到 `motor_001` 的 JSON 数据。

### 下一步

在订阅端加入 JSON 解析、字段校验和异常兜底。
---

## Day 5：MQTT 消息解析与字段校验

今天完成了网关订阅端的消息解析和基础字段校验。

### 完成内容

- 新增 `gateway/payload_validator.py`
- 实现 JSON 字符串解析
- 校验设备数据必要字段
- 校验 temperature、vibration、current 的基本范围
- 修改 `gateway/mqtt_subscriber.py`
- 网关收到非法消息时不会崩溃，而是输出错误信息
- 新增 `tests/test_payload_validator.py`

### 当前链路

```text
virtual_device.py
        ↓
mqtt_publisher.py
        ↓
localhost:1883 Mosquitto
        ↓
mqtt_subscriber.py
        ↓
payload_validator.py
        ↓
合法数据打印 / 非法数据拒绝

---


```
## Day 6：修复 MQTT 订阅端与 payload 校验测试

今天对 Day 5 的网关消息解析与字段校验进行了修复和验收。

### 完成内容

- 修复 `gateway/mqtt_subscriber.py` 中 f-string 字段输出问题
- 修复 `gateway/payload_validator.py` 中 device_id、timestamp 校验逻辑
- 优化错误提示信息
- 补充 payload 校验测试用例
- 重新运行 `python -m pytest`
- 验证 MQTT publisher → broker → subscriber → payload_validator 链路可用

### 当前阶段

项目当前处于阶段3：

```text
MQTT 订阅
    ↓
JSON 解析
    ↓
字段完整性校验
    ↓
数值范围校验
    ↓
合法数据打印 / 非法数据拒绝
---
```
## Day 7：SQLite 数据库存储模块

今天完成了设备数据的 SQLite 最小落库功能。

### 完成内容

- 新增 `database/db_manager.py`
- 新增 `database/__init__.py`
- 新增 `tests/test_db_manager.py`
- 实现 SQLite 数据库初始化
- 实现设备数据插入
- 实现最新一条设备数据查询
- 使用 pytest 验证数据库建表、插入和查询功能

### 当前链路

```text
virtual_device.py
        ↓
mqtt_publisher.py
        ↓
localhost:1883 Mosquitto
        ↓
mqtt_subscriber.py
        ↓
payload_validator.py
        ↓
SQLite sensor_data 表
---
```
## Day 8：MQTT 合法数据自动写入 SQLite

今天完成了网关订阅端与 SQLite 数据库模块的连接。

### 完成内容

- 修改 `gateway/mqtt_subscriber.py`
- 网关收到 MQTT 消息后先进行 JSON 解析和字段校验
- 合法数据自动调用 `insert_sensor_data()` 写入 SQLite
- 非法数据不会入库，并输出错误信息
- 使用 `get_latest_sensor_data()` 验证最新数据可以查询

### 当前链路

```text
virtual_device.py
        ↓
mqtt_publisher.py
        ↓
localhost:1883 Mosquitto
        ↓
mqtt_subscriber.py
        ↓
payload_validator.py
        ↓
db_manager.py
        ↓
data/iot_data.db

---
```
## Day 9：SQLite 最新数据查询脚本

今天完成了数据库最新数据查询脚本，用于验证 MQTT 合法数据是否已经成功写入 SQLite。

### 完成内容

- 新增 `database/query_latest.py`
- 修复 `gateway/mqtt_subscriber.py` 中 `current` 输出字段拼写
- 使用 `get_latest_sensor_data()` 查询最新一条设备数据
- 验证 MQTT 入库后的数据可以通过命令行查询

### 当前链路

```text
virtual_device.py
        ↓
mqtt_publisher.py
        ↓
localhost:1883 Mosquitto
        ↓
mqtt_subscriber.py
        ↓
payload_validator.py
        ↓
db_manager.py
        ↓
data/iot_data.db
        ↓
query_latest.py

### Day 10：修复 SQLite 历史查询测试，完成最近 10 条传感器数据查询。
```
### Day 11：阈值异常检测函数

今天新增了最小阈值异常检测模块。

### 完成内容

- 新增 `anomaly_detection/threshold_detector.py`
- 实现 `detect_threshold_anomaly(data)`
- 支持温度、振动、电流三类阈值异常判断
- 新增 `tests/test_threshold_detector.py`
- 使用 pytest 验证正常数据不报警，异常数据触发报警

### 验收命令


运行：

```powershell
python -m pytest tests/test_payload_validator.py tests/test_threshold_detector.py -q
python -m pytest -q
### Day 11 修复记录

- 修复 timestamp 空字符串校验问题
- 修复 README Day 11 测试命令代码块未闭合问题
- 重新运行 payload 校验测试和阈值检测测试
### Day 11 修复记录

- 修复 timestamp 空字符串校验问题
- 修复 README Day 11 测试命令代码块未闭合问题
- 重新运行 payload 校验测试和阈值检测测试
```
## Day 12：阈值报警写入 SQLite

今天完成了阈值异常检测与报警表的最小闭环。

### 完成内容

- 修改 `gateway/mqtt_subscriber.py`
- MQTT 合法数据入库后，调用 `detect_threshold_anomaly(data)`
- 当检测到温度、振动或电流异常时，构造报警记录
- 调用 `insert_alarm(alarm)` 写入 SQLite 的 `alarms` 表
- 新增 `tests/test_alarm_db.py`，验证报警可以写入数据库

### 当前链路

```text
mqtt_publisher.py
        ↓
mqtt_subscriber.py
        ↓
payload_validator.py
        ↓
sensor_data 表
        ↓
threshold_detector.py
        ↓
alarms 表
## Day 13：异常数据发布脚本

今天新增了 `simulators/abnormal_publisher.py`，用于发送温度、振动、电流三类异常数据。

### 完成内容

- 新增异常数据发布脚本
- 构造 temperature、vibration、current 三类异常 payload
- 通过 MQTT 发布到 `factory/motor_001/telemetry`
- 网关接收后完成校验、阈值检测、报警入库
- 使用 SQLite 查询验证 `alarms` 表新增报警记录

### 验证命令

```powershell
python -m simulators.abnormal_publisher
## Day 14：Z-score 测试修复

今天没有修改 `anomaly_detection/zscore_detector.py`，只修改了 `tests/test_zscore_detector.py`。

修复内容：

- 测试导入改为当前代码中实际存在的 `calculate_zscore`
- 测试导入改为当前代码中实际存在的 `detect_zsore_anomaly`
- 删除对不存在函数 `calculate_mean`、`calculate_std` 的导入
- 按当前函数参数 `history_value: list[float]` 编写测试

验证命令：

```powershell
python -m pytest tests/test_zscore_detector.py -q

## Day 15：阈值 + Z-score 统一异常分析服务

今天新增了 `anomaly_detection/anomaly_service.py`。

### 完成内容

- 新增 `analyze_sensor_data(data, history)`
- 先执行阈值异常检测
- 阈值未触发时，再执行 Z-score 异常检测
- 统一返回 `is_anomaly / alarm_type / alarm_reason / severity`
- 新增 `tests/test_anomaly_service.py`

### 验证命令

```powershell
python -m pytest tests/test_anomaly_service.py -q
python -m pytest -q
