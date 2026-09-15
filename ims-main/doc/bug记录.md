# Bug 记录

> 记录格式：编号、日期、严重程度、模块、现象、根因、修复方案、涉及文件、教训

---

## BUG-001

| 字段 | 内容 |
|------|------|
| 编号 | BUG-001 |
| 日期 | 2026-09-08 |
| 严重程度 | 中 |
| 模块 | 场景测试 - 主线A/B/C/D |
| 现象 | 场景测试多处报 `KeyError: 'data'` 或 `KeyError: 'id'`，测试无法通过 |
| 根因 | API 响应格式不统一：部分端点返回原始数据（Incoming、RMA POST），部分端点返回 `R` 包装数据（Shipment、BOM、RMA GET）。测试代码对响应格式的假设与实际不一致。 |
| 修复方案 | 逐一分析每个 API 端点的实际响应格式，修正测试中的断言：<br/>- Incoming POST/GET → 原始数据，移除 `["data"]`<br/>- RMA POST → 原始数据，移除 `["data"]`<br/>- RMA GET → R 包装，保留 `["data"]`<br/>- Shipment → R 包装，保留 `["data"]`<br/>- BOM POST → R 包装，添加 `["data"]` |
| 涉及文件 | `tests/scenario/test_scenario_mainline_a.py`<br/>`tests/scenario/test_scenario_mainline_b.py`<br/>`tests/scenario/test_scenario_mainline_c.py`<br/>`tests/scenario/test_scenario_mainline_d.py` |
| 教训 | 新模块开发时 API 响应格式应统一。建议在 `app/schemas/common.py` 的 `R` 类文档中注明各模块的响应格式约定。 |

---

## BUG-002

| 字段 | 内容 |
|------|------|
| 编号 | BUG-002 |
| 日期 | 2026-09-08 |
| 严重程度 | 中 |
| 模块 | 返厂维修 - 报废审批流程 |
| 现象 | S006 场景测试报错 `ValueError: 该返厂单已报废`，报废单创建被拦截 |
| 根因 | `rma_service.py` 中诊断结果设为 "SCRAP" 时，立即将返厂单状态设为 "SCRAPPED"。后续创建报废单时，状态校验发现已报废，拒绝创建。 |
| 修复方案 | 移除诊断时对 SCRAP 结果的自动状态设置。改为在报废审批通过时（`approve_scrap`）才将返厂单状态设为 "SCRAPPED"。 |
| 涉及文件 | `app/service/rma_service.py`（诊断逻辑） |
| 教训 | 业务流程的中间状态不应由上游操作自动设置，应由下游操作在完成时设置。避免状态机出现"跳步"问题。 |

---

## BUG-003

| 字段 | 内容 |
|------|------|
| 编号 | BUG-003 |
| 日期 | 2026-09-08 |
| 严重程度 | 低 |
| 模块 | 场景测试 - 主线C |
| 现象 | `assert res.status_code != 200` 断言失败，删除出货单后查询返回 200 |
| 根因 | 删除成功后查询已删除的出货单，API 使用 `R.fail()` 返回 HTTP 200 但 `code=-1`，不是 404。 |
| 修复方案 | 将断言改为 `assert res.json()["code"] != 0`，检查业务错误码而非 HTTP 状态码。 |
| 涉及文件 | `tests/scenario/test_scenario_mainline_c.py` |
| 教训 | 项目使用 `R` 统一包装，业务错误返回 HTTP 200 + code≠0。测试断言应检查 `code` 字段，而非 HTTP 状态码。 |

---

## BUG-004

| 字段 | 内容 |
|------|------|
| 编号 | BUG-004 |
| 日期 | 2026-09-08 |
| 严重程度 | 低 |
| 模块 | 场景测试 - 主线D |
| 现象 | 齐套分析断言 `assert availability["items"][0]["required_qty"] == 210.0` 失败，实际值为 200.0 |
| 根因 | BOM 创建时物料数量为 200，齐套分析中 required_qty 应为 200.0 而非 210.0。测试预期值写错。 |
| 修复方案 | 将预期值从 210.0 修正为 200.0。 |
| 涉及文件 | `tests/scenario/test_scenario_mainline_d.py` |
| 教训 | 测试预期值应与测试数据保持一致，避免复制粘贴导致的数值错误。 |