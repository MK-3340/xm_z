# 运行配置说明

## 配置文件
配置文件路径：`configs/config.json`

| 字段 | 作用 |
|---|---|
| broker_host | MQTT Broker 地址 |
| broker_port | MQTT Broker 端口 |
| telemetry_topic | 设备遥测数据 Topic |
| db_path | SQLite 数据库路径 |

## 密钥配置
HMAC 密钥不写入配置文件。

发布端和网关端都需要设置：

```powershell
$env:IOT_HMAC_SECRET = "local-demo-secret"

日志说明

INFO：正常连接、订阅、合法数据处理；

WARNING：非法设备、签名失败、过期时间戳、重复 nonce、非法 payload。


README 今天只追加一小节，不重写全文：

```md
## 配置与日志

网关运行参数位于 `configs/config.json`。

HMAC 密钥使用环境变量 `IOT_HMAC_SECRET` 配置，不写入仓库。

运行前请先阅读 `docs/configuration.md`。