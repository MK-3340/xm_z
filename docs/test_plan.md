# 测试计划

## 单元测试
- payload 字段、类型、范围校验
- HMAC 正确签名、错误签名、缺失签名
- timestamp 时间窗口
- nonce 重复检测
- 阈值异常检测

## 模块测试
- publisher 生成的数据可通过校验和 HMAC 验证
- subscriber 合法消息可入库
- subscriber 错误签名消息不可入库

## 手工集成测试
Broker -> Subscriber -> Publisher -> SQLite -> Dashboard -> Alarm

docs/run_demo.md 写今天使用的五终端启动顺序。