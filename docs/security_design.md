# 安全设计

## 1. 设备白名单
网关只接受 configs/devices.json 中登记的设备编号。

## 2. HMAC 签名认证
发布端使用共享密钥对完整 payload 生成 HMAC-SHA256 签名。
网关验签成功后才允许数据进入数据库。

## 3. timestamp 时间窗口
网关只接受最近 60 秒内的消息，拒绝明显过期的旧消息。

## 4. nonce 防重放
每条 MQTT 消息包含随机 nonce。
同一 device_id 和 nonce 的组合只能被网关接受一次。

## 当前边界
nonce 当前保存在网关进程内存中。
程序重启后 nonce 记录会清空。
生产环境可用 Redis 或 SQLite 保存带过期时间的 nonce。