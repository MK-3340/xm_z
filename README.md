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