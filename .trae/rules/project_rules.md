# 敦临 IMS 生产物料与产品追溯管理系统 - Trae 开发规则

> **所属单位**：西安敦临计量检测有限公司
> **系统简称**：敦临 IMS（DL-IMS）

## 1. 项目概述

### 1.1 设计目标

用一套系统完整替代 3 张 Excel（到货台账、出货台账、退货台账），实现 **"来料检测 → BOM生产准备 → 发货 → 异常退货（维修/再出货）→ 最终去向"** 全流程闭环管理。

### 1.2 技术栈（不可更改）

| 层级 | 技术 |
|------|------|
| 后端框架 | Python 3.12+ / FastAPI |
| 前端框架 | Vue 3 + Vite + Element Plus + Pinia |
| 数据库 | MySQL 5.7 |
| 缓存 | Redis 7（Docker 部署时启用，本地开发自动降级为内存缓存） |
| ORM | SQLAlchemy 2.0+ |
| 数据库迁移 | Alembic |
| 部署 | Docker Compose（MySQL + Redis + Backend + Frontend） |
| 后端端口 | 8000 |
| 前端端口 | 8080 |
| 包管理(Python) | uv |
| 包管理(JS) | npm |

### 1.3 核心原则

- 唯一 SN 贯穿成品全生命周期
- 新旧 SN 强制关联（维修换码）
- 所有操作强制记录"谁、何时、改了什么、为什么"
- 权限最小化与职责分离
- 批次 + 可选 SN 双轨制管理原材料
- 复用 IMS 现有表结构（partner、product_sku、inventory_item、audit_log），保持数据一致性

### 1.4 四大业务主线

| 主线 | 名称 | 对应原 Excel | 核心功能 |
|------|------|-------------|----------|
| 主线A | 采购来料管理 | 物料到货记录台账 | 到货登记 → 来料检验 → 合格入库 / 不合格退货 |
| 主线B | 成品返厂维修 | 场站异常退货记录台账 | 退货登记 → 诊断 → 维修换新SN → 报废审批 → 再出货 |
| 主线C | 出货管理 | 出货记录台账 | 出货登记 → 关联U9任务单 → 物流信息 |
| 主线D | BOM & 生产准备 | 新增 | BOM导入/导出 → 库存对比 → 齐套分析 → 采购建议 |

### 1.5 项目目录结构

```
ims-main/
├── backend/
│   ├── app/
│   │   ├── api/          # API路由层
│   │   ├── core/         # 配置、安全、依赖注入
│   │   ├── db/           # 数据库连接
│   │   ├── models/       # SQLAlchemy 模型
│   │   ├── schemas/      # Pydantic 请求/响应模型
│   │   ├── service/      # 业务逻辑层
│   │   ├── utils/        # 工具函数
│   │   └── constants/    # 常量定义
│   ├── alembic/          # 数据库迁移
│   ├── main.py           # 入口文件
│   └── pyproject.toml    # Python 项目配置
├── frontend/
│   ├── src/
│   │   ├── api/          # API 请求封装
│   │   ├── components/   # Vue 组件
│   │   ├── layout/       # 布局组件
│   │   ├── router/       # 路由配置
│   │   ├── stores/       # Pinia 状态管理
│   │   ├── utils/        # 工具函数
│   │   └── constants/    # 常量/枚举
│   └── package.json
└── docker-compose.yml
```

### 1.6 常用命令

```bash
# 启动全部服务
docker compose up -d

# 仅启动后端开发
cd ims-main/backend && uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 仅启动前端开发
cd ims-main/frontend && npm run dev

# 数据库迁移
cd ims-main/backend && uv run alembic upgrade head

# 数据库备份
docker exec ims-db mysqldump -u root -p ims > backup_$(date +%Y%m%d_%H%M%S).sql

# 查看Git提交记录
git log --oneline -5
```

> 📋 **开发使用说明**：`doc/开发使用说明.md` | 🐛 **环境问题排查**：`doc/开发环境问题记录.md`

---

## 2. Trae 开发宪法规则

### 规则0：对话前状态摘要（每次对话必读，不可协商）

每次对话开始时，AI 必须先执行以下 4 步，再开始任何工作：

```
1. 读取 PROJECT_STATE.md（项目根目录）
2. 运行 git log --oneline -3
3. 运行 git branch --show-current
4. 运行 git describe --tags --abbrev=0 2>/dev/null || echo "无 Tag"
```

然后输出以下格式的状态摘要：

```markdown
## 项目当前状态
- 版本：v2.6（一期完成，二期开发中）
- 分支：[当前分支] | Tag：[最近 Tag]
- 本次目标：[一句话描述本次任务]

## 最近变更
[git log --oneline -3 的输出]

## 本次改动范围
- 只改：[文件路径列表]
- 不改：[排除范围]

## 约束
- 遵守《文档编写规范》
- 遵守《project_rules.md》全部规则
- 每次改动后运行检测清单对应项
```

用户确认（回复"继续"或描述任务）后，AI 开始工作。

**对话流程：**

```
用户打开对话
    ↓
AI 自动执行：
    1. 读取 PROJECT_STATE.md
    2. 运行 git log --oneline -3
    3. 运行 git branch --show-current + git describe --tags
    4. 输出状态摘要
    5. 向用户确认本次任务范围
    ↓
用户说"继续"或描述任务
    ↓
AI 开始工作
```

---

### 规则1：Git 版本控制（不可协商）

| 条目 | 内容 |
|------|------|
| 规则 | 每次修改代码前必须先提交当前版本。每次功能完成后必须提交新版本。 |
| 提交格式 | `[模块名] 操作说明`，如 `[audit] 新增 change_reason 字段` |
| 辅助 Skill | 提交时使用 `git-commit` Skill 自动生成符合格式的 commit message 并推送 |
| 验证标准 | `git log --oneline -5` 能看到 ≥5 条记录，每条符合格式 |
| 回溯规则 | 连续两次修复失败时：① 停止修复 ② `git log --oneline -10` ③ 找到最后稳定版本 ④ `git checkout` 或 `git revert` ⑤ 在稳定版重新分析 |
| 主线归档 | 主线验收后打 Tag：`git tag -a v1.0-milestone-A -m "[主线A] 验收通过"` |
| 密钥安全 | 提交前检查：`.env` 不在暂存区、无硬编码密码/Key、`.env.example` 只含模板值 |

### 规则2：数据库备份（不可协商）

| 条目 | 内容 |
|------|------|
| 规则 | 任何数据库结构变更前必须备份。数据迁移必须在测试环境验证通过后才能在生产执行。 |
| 备份命令 | `docker exec ims-db mysqldump -u root -p ims > backup_$(date +%Y%m%d_%H%M%S).sql` |
| 验证标准 | 备份文件大小 > 0KB 且能正常还原 |


### 规则17：完整检测清单触发词（不可协商）

| 条目 | 内容 |
|------|------|
| 规则 | 当用户说"执行完整检测清单"时，AI 按 **两阶段** 自动执行。阶段1（离线）立即跑；阶段1完成后询问用户是否启动服务进入阶段2（在线）。共覆盖清单 v2.14 全部项目。 |
| 触发词 | **"执行完整检测清单"** |

**执行流程：**

```
用户说 "执行完整检测清单"
    ↓
阶段1（离线，无需启动服务，约15分钟）
    ① 后端测试 → ② 前端测试 → ③ Skill代码质量 → ④ 技术栈专项 → ⑤ 上线检查(离线)
    ↓
阶段1完成后，输出报告 + 询问：
    "阶段1完成。要现在启动前后端服务继续跑阶段2吗？"
    ↓
用户同意 → 启动服务 → 阶段2
用户拒绝 → 结束，标记阶段2为 ⚠️ 待执行
```

---

**阶段1：离线检查（立即自动执行）**

| 步骤 | 内容 | 覆盖清单 | 命令/操作 |
|:---:|------|:---:|-----------|
| ① | **后端测试** | §1.1~1.6 | `pytest tests/ -v --tb=short`（已有测试）；创建并跑 `tests/smoke/` API 全量冒烟（94端点）；创建并跑序列化异常测试 §1.3.10 |
| ② | **前端单元测试** | §1.4 | `npm run test`（Vitest）；检查二期 5 个测试文件是否存在，缺失则先创建再跑 |
| ③ | **Skill 代码质量** | §2, §3 | `code-quality-skill` → `detect-code-smells` → `code-review-and-quality`；密钥管理检查（.env/前端硬编码/日志泄漏）、全局异常处理器检查、参考实现复用检查 |
| ④ | **技术栈专项** | §2.2 | FastAPI / Vue / SQLAlchemy+Alembic / Pinia / MySQL / Docker（按修改范围调用） |
| ⑤ | **上线检查（离线）** | §4.19, §5.1~5.2, §6.1, §A1~A4 | Git规范检查（commit格式+里程碑Tag）→ 数据库备份恢复演练 → 环境配置 → 数据字典更新 `generate_data_dict.py` → **APK离线检查** `uv run pytest tests/apk/ -v -m "not apkfull"`（43项：环境6+配置10+资源14+插件3） |

**阶段2：在线检查（需启动服务后执行）**

| 步骤 | 内容 | 覆盖清单 | 命令/操作 |
|:---:|------|:---:|-----------|
| ⑥ | **前端路由遍历** | §4.15~4.16 | 启动后端 `uv run uvicorn main:app --port 8000` + 前端 `npm run dev` → 23页面500检查 → 多角色遍历（5角色×23页面）→ 空数据渲染 → 加载状态 |
| ⑦ | **E2E + 浏览器** | §4.1, §4.7 | E2E 端到端（13用例）→ 跨浏览器渲染（Chrome/Edge/Firefox/Safari）→ 浏览器打印兼容 |
| ⑧ | **打印 + Excel** | §4.2~4.3 | 6种单据打印 → 打印分页（25行跨页）→ Excel 5000行导出性能 |
| ⑨ | **性能 + 并发** | §3.4, §4.4 | 50用户并发 → 慢查询 EXPLAIN → 大数据量渲染 → 404路由/请求超时 |
| ⑩ | **APK + 在线验收** | §4.9~4.10, §4.14, §4.17~4.18, §5.3~5.5, §A5 | **APK完整编译** `uv run pytest tests/apk/ -v -m apkfull`（6项：debug编译+release编译+签名验证+混淆检查）→ 网络切换 → UI视觉一致性 → 轮询提醒开发验证 → 二期功能验证 → 性能验证（系统启动<10s）→ **需求验收对照**（4主线+二期+权限矩阵，对照PRD逐条） |

---

**执行后输出格式：**

```
## 完整检测清单执行报告（v2.14）

### 阶段1（离线）
| 步骤 | 检查项 | 结果 | 备注 |
|:---:|--------|:---:|------|
| ① | 后端测试 | ✅/❌ | N通过/N失败 |
| ② | 前端单元测试 | ✅/❌ | ... |
| ③ | Skill代码质量 | ✅/❌ | ... |
| ④ | 技术栈专项 | ✅/❌ | ... |
| ⑤ | 上线检查(离线)+APK离线 | ✅/❌ | ... |

### 阶段2（在线）
| 步骤 | 检查项 | 结果 | 备注 |
|:---:|--------|:---:|------|
| ⑥ | 前端路由遍历 | ✅/❌/⚠️ | ... |
| ⑦ | E2E+浏览器 | ✅/❌/⚠️ | ... |
| ⑧ | 打印+Excel | ✅/❌/⚠️ | ... |
| ⑨ | 性能+并发 | ✅/❌/⚠️ | ... |
| ⑩ | APK编译+在线验收 | ✅/❌/⚠️ | ... |

总结：阶段1 X/6 通过 | 阶段2 Y/5 通过（或 ⚠️ 待执行）
未完成项剩余：N 项
```

### APK 专项检查触发词

| 触发词 | 自动执行动作 |
|--------|-------------|
| "APK检查"、"APK离线检查" | `uv run pytest tests/apk/ -v -m "not apkfull"`（43项轻量检查） |
| "APK编译"、"编译APK" | `uv run pytest tests/apk/ -v -m apkfull`（6项完整编译验证） |
| "APK全量"、"APK全部" | `uv run pytest tests/apk/ -v`（49项全量） |

### 规则3：单次改动可验证

| 条目 | 内容 |
|------|------|
| 规则 | 每次只改一个功能点，改完立即验证。不允许同时改多个功能点然后一起验证。 |
| 验证标准 | 每次改动后执行对应功能点的验证检查，通过后方可进入下一个改动 |

### 规则4：先界面后逻辑

| 条目 | 内容 |
|------|------|
| 规则 | 新增功能时，先做前端页面（用户能看见），再做后端API和业务逻辑。 |
| 验证标准 | 浏览器能访问到新页面，看到界面元素和正确的标签/占位符 |

### 规则5：变更原因强制弹窗（不可协商）

| 条目 | 内容 |
|------|------|
| 规则 | 所有涉及状态变更、数量修改、SN变更、审批操作的操作，前端必须弹窗强制填写"变更原因"，不填则提交按钮禁用。后端必须校验 `change_reason` 非空。 |
| 验证标准 | 执行状态变更操作时，弹窗出现且"提交"按钮灰显；填写文字后按钮可用；审计日志中 `change_reason` 字段有值 |

### 规则6：主线独立可测

| 条目 | 内容 |
|------|------|
| 规则 | 每条主线完成后，必须通过该主线的全部验收清单，方可进入下一条。二期同样适用。 |

### 规则7：复用现有表，不重复建表

| 条目 | 内容 |
|------|------|
| 规则 | 供应商使用现有 `partner` 表（外键 `supplier_id`），物料使用现有 `product_sku` 表（外键 `sku_id`），不新建供应商表或物料表。 |
| 验证标准 | 新表中使用外键关联，而非文本字段 |

### 规则8：通用验收通则（所有功能默认包含）

每完成一个功能点，除该功能点专项验证外，还必须满足以下通则：

| 编号 | 通则内容 | 验证方式 |
|------|----------|----------|
| T-0001 | 操作后审计日志新增记录 | `SELECT * FROM audit_log WHERE entity_no = '单据号' ORDER BY created_at DESC LIMIT 1;` |
| T-0002 | 变更原因不为空 | 审计日志 `change_reason` 字段非空 |
| T-0003 | 页面响应式 | 手机浏览器打开，界面不破碎、按钮可点 |
| T-0004 | 权限正确 | 用非授权账号尝试操作，返回"无权限"提示 |

### 规则9：后端开发规范

| 条目 | 内容 |
|------|------|
| 模型定义 | 所有新增 Model 放在 `backend/app/models/`，继承 `Base` |
| Schema定义 | 所有新增 Pydantic Schema 放在 `backend/app/schemas/` |
| API路由 | 所有新增 API 放在 `backend/app/api/`，路径前缀 `/api/v1/` |
| 编号生成 | 统一在 `utils/order_no.py` 中扩展 |
| 枚举定义 | 所有枚举统一放在 `backend/app/models/enums.py` |
| 服务层 | 复杂业务逻辑放在 `backend/app/service/` |
| 外键关联 | 新增表涉及供应商/物料的，使用 `supplier_id`/`sku_id` 外键，而非文本 |
| 模糊搜索 | 复用 `inventory_service._keyword_filter` 函数，支持 LIKE 模糊匹配 SN 和商品名 |
| 数据完整性 | 从 `product_sku` 填充业务表冗余字段时，若 `unit` 为 NULL，默认赋值为 `'个'`（兜底） |

### 规则10：前端开发规范

| 条目 | 内容 |
|------|------|
| 组件复用 | 优先使用 TablePro、SearchForm 等现有组件 |
| 搜索模式 | 新页面搜索区参考 `InventoryDetail.vue` 模式：keyword 文本输入 + 分类下拉 + SKU 联动下拉 + 状态筛选 + 日期范围 |
| 路由规范 | 参考 `router/index.js` 现有命名规范，使用懒加载 |
| 菜单配置 | 在 `MainLayout.vue` 的 `allMenus` 中配置，使用 `roles` 数组控制权限 |
| 权限控制 | 所有路由和菜单必须配置 `roles` 或 `adminOnly` |
| API调用 | 统一使用 `api/` 目录下的封装方法 |
| UI一致性 | 新增页面颜色/字体/间距/按钮风格与现有页面保持一致，不引入新设计语言 |

### 规则11：代码审查最低标准

代码审查时使用 `code-quality-skill` 和 `detect-code-smells` 两个 Skill 辅助检查：

| 条目 | 要求 | 检查 Skill |
|------|------|------------|
| 无硬编码 | 所有配置项（前缀、状态值、角色名）使用枚举或常量 | `code-quality-skill` |
| 字段完整 | 新增表必须包含 `created_at` 和 `updated_at` | `code-quality-skill` |
| 审计覆盖 | 所有关键操作必须写入审计日志 | `code-quality-skill` |
| 向后兼容 | 新增字段必须 `nullable=True` 或有默认值 | `code-quality-skill` |
| 外键优先 | 关联数据使用外键，不存文本 | `code-quality-skill` |
| 代码异味 | 无 Long Method / Large Class / Duplicate Code 等问题 | `detect-code-smells` |

### 规则12：Skill 检查验证（不可协商）

每次功能开发完成后、提交代码前，必须按以下顺序调用 Skill 进行检查验证。

#### 12.1 代码质量检查（开发完成 → 提交前）

| 序号 | Skill 名称 | 用途 | 触发条件 | 通过标准 |
|------|-----------|------|----------|----------|
| ① | `code-quality-skill` | Python 代码质量检查 | 后端代码有修改时 | 无 WARNING 级别以上问题 |
| ② | `detect-code-smells` | 代码异味检测 | 新增/修改 >50行代码时 | 无异味需要重构 |
| ③ | `code-review-and-quality` | 多维度代码审查 | 合并前 / 重大改动时 | 多轴检查通过 |

#### 12.2 调试排查（遇到错误时）

| 序号 | Skill 名称 | 用途 | 触发条件 | 通过标准 |
|------|-----------|------|----------|----------|
| ④ | `systematic-debugging` | 系统化调试（4阶段铁律） | 出现任何 bug/错误/异常/测试失败时 | 根因已定位，修复已验证 |
| ⑤ | `bug-detective` | 快速错误排查（备用） | 简单错误快速定位时 | 错误已定位 |

**核心铁律**：遇到任何报错/异常/bug，必须先调用 `systematic-debugging` 定位根因，再动手改代码。禁止跳过调试直接猜测修复。未完成根因调查前，禁止提出任何修复方案。

#### 12.3 技术栈专项检查（按修改范围触发）

| 序号 | Skill 名称 | 技术栈 | 用途 | 触发条件 |
|------|-----------|--------|------|----------|
| ⑥ | `fastapi-python` | FastAPI | FastAPI 最佳实践 | 修改 API 路由/服务层时 |
| ⑦ | `sqlalchemy-alembic-expert-best-practices-code-review` | SQLAlchemy+Alembic | ORM 模型/迁移审查 | 修改 Model/迁移脚本时 |
| ⑧ | `vue` | Vue 3 | Vue 3 Composition API | 修改 Vue 组件时 |
| ⑨ | `pinia` | Pinia | 状态管理最佳实践 | 修改 Store 时 |
| ⑩ | `mysql` | MySQL | 数据库设计/查询审查 | 修改表结构/查询时 |
| ⑪ | `mysql-best-practices` | MySQL | 数据库最佳实践 | 修改表结构/查询时 |
| ⑫ | `docker-patterns` | Docker | Docker/Compose 模式 | 修改 Dockerfile/docker-compose 时 |

#### 12.4 测试与一致性（提交前）

| 序号 | Skill 名称 | 用途 | 触发条件 | 通过标准 |
|------|-----------|------|----------|----------|
| ⑬ | `webapp-testing` | Web 应用测试（Playwright） | 前端功能开发完成时 | 浏览器验证通过 |
| ⑭ | `upkeep` | 文档代码一致性 | 改动涉及配置/表结构/API时 | 文档与代码一致 |

**前端验证流程**：每次修改前端页面后，调用 `webapp-testing` Skill 在浏览器中自动验证功能（页面加载、元素可见性、按钮点击、表单输入、弹窗交互、API 响应断言），不依赖手动 F5 刷新。

**全面检查触发词**：当用户说"检查"、"全面检查"、"检测"、"verify"、"check"时，必须按顺序调用全部上述 Skill 进行检查，不得跳过。输出格式：每个 Skill 输出 名称 + 范围 + 问题数 + 通过/未通过。

**验证标准**：每次 `git commit` 前，上述 Skill 检查结果必须全部通过。

---

### 规则13：Excel 导出格式规范（不可协商）

| 条目 | 内容 |
|------|------|
| 规则 | 所有业务模块的 Excel 导出统一使用 `item_export.py` 中的通用工具函数，格式统一。 |
| 标题行 | 第1行，深蓝背景 `#4472C4` + 白色粗体 11pt + 居中 |
| 数据行 | 白色/浅蓝交替斑马纹（`#FFFFFF` / `#DDEBF7`），全表细线边框（`#999999`），自动筛选器 |
| 金额列 | 千分位格式 `#,##0.00`，右对齐 |
| SN列 | 文本格式（避免科学计数法） |
| 长文本列 | 自动换行（`wrap_text=True`） |
| 冻结 | 标题行冻结（冻结首行） |
| 文件名 | 格式 `IMS-{模块名}-{内容}-{日期}.xlsx` |
| 验证标准 | 下载导出的 Excel 文件，检查：标题行深蓝白字、斑马纹交替、边框完整、金额有千分位、SN为文本、自动筛选可用 |

### 规则14：搜索功能复用（不可协商）

| 条目 | 内容 |
|------|------|
| 规则 | 新模块的列表页面必须包含搜索功能。后端模糊搜索统一复用 `inventory_service._keyword_filter` 函数，前端搜索区参考 `InventoryDetail.vue` 模式。 |
| 后端复用 | `from app.service.inventory_service import _keyword_filter`，支持：单关键词模糊匹配 SN + 商品名（`LIKE %keyword%`），多行批量搜索 SN（最多 100 个），OR 逻辑连接 |
| 前端模式 | 每个新列表页面至少包含：① 关键词输入框（`keyword`）② 分类下拉（联动 SKU）③ 状态筛选 ④ 日期范围 |
| 验证标准 | 输入关键词后列表数据按条件过滤；部分 SN 能模糊匹配；多行粘贴多个 SN 能批量搜索 |

### 规则15：全局检查触发词（不可协商）

| 条目 | 内容 |
|------|------|
| 规则 | 当用户说"全局检查"、"全面检查"、"全量检查"、"check all"时，AI 必须先搜索该模块的所有相关文件，逐一检查，而非只改用户提到的那一处。 |
| 触发词 | "全局检查"、"全面检查"、"全量检查"、"check"、"verify"、"一致性检查"、"检查所有" |
| 执行流程 | ① 搜索该模块相关代码（SearchCodebase / Grep）② 列出涉及的所有文件 ③ 逐一检查每个文件 ④ 保持一致性调整 ⑤ 输出检查报告 |
| 验证标准 | AI 输出至少列出 3 个相关文件，跨文件一致性已确认 |

### 规则16：主线收尾触发词（不可协商）

| 条目 | 内容 |
|------|------|
| 规则 | 当用户说"主线[字母]收尾"、"完成[模块名]验收"时，AI 必须按以下 7 步自动执行收尾检查。 |
| 触发词 | "主线[字母]收尾"、"主线[字母]完成"、"[模块名]验收"、"收尾检查"、"交付检查" |

**主线收尾 7 步检查清单：**

| 步骤 | 操作 | 命令/动作 |
|:---:|------|-----------|
| ① | 代码质量检查 | 调用 `code-quality-skill` |
| ② | 代码异味检测 | 调用 `detect-code-smells` |
| ③ | 技术栈专项检查 | 调用 `fastapi-python` + `vue` + `sqlalchemy-alembic-expert-best-practices-code-review`（按修改范围） |
| ④ | 浏览器验证 | 调用 `webapp-testing` 验证核心流程 |
| ⑤ | 后端启动验证 | `uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000`，确认无报错 |
| ⑥ | 前端启动验证 | `npm run dev`，确认无报错 |
| ⑦ | 结果记录 | 输出总结报告，记录到 `doc/主线[字母]_完成报告.md` |

**收尾输出格式：**

```
## 主线X 收尾检查报告
| 步骤 | 检查项 | 结果 | 备注 |
|:---:|--------|:----:|------|
| ① | 代码质量 | ✅/❌ | ... |
... 
总结：通过/未通过，待修复项：[列表]
```

### 规则18：大文件批量修改规范（不可协商）

| 条目 | 内容 |
|------|------|
| 规则 | 修改超过 800 行的大文件时，必须使用 PowerShell 一次性批量替换，禁止逐个 Edit 调用。 |
| 原因 | Edit 工具每次修改都要搜索匹配、定位、写入，VS Code 诊断每次保存都触发，大文件会越来越慢。 |
| 解决方案 | 使用 PowerShell 的 `-replace` 操作符一次性批量替换，1 次读写完成。 |

```powershell
$content = Get-Content 文件名.py -Raw -Encoding UTF8
$content = $content -replace '旧值1', '新值1'
$content = $content -replace '旧值2', '新值2'
$content | Set-Content 文件名.py -NoNewline -Encoding UTF8
Write-Host "Done!"
```

| 验证标准 | 替换后 `Grep` 检查旧值已全部消失，新值全部出现 |

### 规则19：Bug 记录与追溯（不可协商）

| 条目 | 内容 |
|------|------|
| 规则 | 每次发现问题/Bug 必须即时记录到 `bug记录.md`，不得跳过。修复后更新状态为"已修复"。 |
| 记录内容 | 编号、日期、严重程度、模块、现象、根因、修复方案、涉及文件、教训 |
| 存放位置 | `doc/bug记录.md` |
| 验证标准 | 每个 Bug 有完整记录，状态已更新，教训已提炼 |

### 规则20：开发环境问题记录（不可协商）

| 条目 | 内容 |
|------|------|
| 规则 | 每次开发环境搭建或启动过程中遇到的问题及解决方案，必须记录到 `doc/开发环境问题记录.md`。 |
| 记录内容 | 问题现象、根因分析、解决方案、涉及的命令 |
| 验证标准 | 文件存在，每个问题有完整的"现象→原因→解决"三段式记录 |

### 规则21：性能优化规范（不可协商）

所有新模块开发及现有模块改造，必须遵循以下四层性能优化规范。

#### 21.1 Redis 缓存层

| 项目 | 规范 |
|------|------|
| 启用条件 | Docker Compose 部署时自动启用 Redis；本地开发降级为内存缓存 |
| 缓存后端 | `app/core/cache.py` — 统一缓存抽象，支持 Redis 和 MemoryCache 双模式 |
| 高频下拉选项 | 分类列表（`get_categories`）、往来单位分组（`get_groups`）必须加缓存，TTL=600s |
| 缓存失效 | 数据变更时必须调用 `invalidate_cache(key)` 立即失效对应缓存 |
| 缓存键规范 | 格式 `ims:{模块}:{资源}`，如 `ims:categories:all` |
| 新模块接入 | 新增高频只读查询默认评估是否需要加缓存 |
| 验证标准 | 第二次请求同一接口，响应时间明显缩短；数据变更后缓存立即刷新 |

#### 21.2 MySQL 查询优化

| 项目 | 规范 |
|------|------|
| 连接池 | `pool_size=10` + `max_overflow=20`，`pool_pre_ping=True` + `pool_recycle=3600` |
| 查询超时 | 通过 `init_command` 设置 `max_execution_time=30000`（30秒） |
| 事务隔离 | 使用 `READ-COMMITTED`，避免长事务锁表 |
| 分页查询 | 默认使用偏移分页（`OFFSET/LIMIT`）；大数据量场景（>1万条）使用游标分页 |
| 索引建议 | 所有 `WHERE` 条件字段、`JOIN` 外键字段、`ORDER BY` 字段建议建索引 |
| 验证标准 | 慢查询日志无超过 3 秒的查询；`EXPLAIN` 输出 type 不为 ALL |

#### 21.3 前端无限滚动（虚拟滚动）

| 项目 | 规范 |
|------|------|
| 适用场景 | 库存明细、入库记录、出货记录等大数据量列表页面 |
| 实现方式 | Element Plus `v-infinite-scroll` 指令 + 游标分页 API |
| 模式切换 | 页面提供"普通分页"和"无限滚动"切换按钮，默认普通分页 |
| 加载提示 | 底部显示"加载中..."和"已加载全部 N 条"状态 |
| 每次加载量 | 默认 `page_size=50` |
| 新页面开发 | 列表数据量预计 >500 条时，默认同时提供两种分页模式 |
| 验证标准 | 滚动到底部自动加载更多，无卡顿；切换回普通分页正常 |

#### 21.4 游标分页（Cursor Pagination）

| 项目 | 规范 |
|------|------|
| 适用场景 | 大数据量列表（>1万条）、无限滚动加载、实时数据流 |
| 实现方式 | 基于主键 ID 降序，cursor 为 Base64 编码的 JSON `{"id": last_id}` |
| Schema | 使用 `CursorPageResult`（`app/schemas/common.py`），包含 `items`、`next_cursor`、`has_more` |
| API 端点 | 在现有列表端点基础上增加 `/cursor` 子路径 |
| 服务层 | 新增 `get_items_cursor()` 方法，复用查询条件构建 |
| 新模块接入 | 预计数据量 >5000 条的列表，默认增加游标分页端点 |
| 验证标准 | 首次请求返回 items + next_cursor；用 next_cursor 请求下一页数据不重复不遗漏 |

### 规则22：测试计划与执行（不可协商）

| 条目 | 内容 |
|------|------|
| 规则 | 每次修改代码后，必须根据修改范围运行对应的测试类型。 |
| 测试文档 | `ims-main/backend/tests/测试计划.md` |
| 种子数据 | `ims-main/backend/tests/seed_data.py` |

| 类型 | 标记 | 用途 |
|------|------|------|
| 合约测试 | `contract` | 验证 API 请求/响应格式、状态码、字段完整性 |
| 场景测试 | `scenario` | 验证端到端业务流程完整性 |

**运行命令：**

```bash
cd ims-main/backend && uv run pytest tests/ -v          # 全部测试
uv run pytest tests/contract/ -v -m contract           # 合约测试
uv run pytest tests/scenario/ -v -m scenario           # 场景测试
```

**自然语言触发词：**

| 触发词 | 自动执行动作 |
|--------|-------------|
| "跑测试"、"运行测试"、"全部测试" | `uv run pytest tests/ -v` |
| "合约测试"、"跑合约"、"契约测试" | `uv run pytest tests/contract/ -v -m contract` |
| "场景测试"、"跑场景"、"流程测试" | `uv run pytest tests/scenario/ -v -m scenario` |
| "主线A测试"、"跑A线" | `uv run pytest tests/contract/test_incoming_contract.py tests/scenario/test_scenario_mainline_a.py -v` |
| "主线B测试"、"跑B线" | `uv run pytest tests/contract/test_rma_contract.py tests/scenario/test_scenario_mainline_b.py -v` |
| "主线C测试"、"跑C线" | `uv run pytest tests/contract/test_shipment_contract.py tests/scenario/test_scenario_mainline_c.py -v` |
| "主线D测试"、"跑D线" | `uv run pytest tests/contract/test_bom_contract.py tests/scenario/test_scenario_mainline_d.py -v` |
| "覆盖率"、"测试报告" | `uv run pytest tests/ --cov=app --cov-report=html` |

**测试隔离机制：**

| 机制 | 说明 |
|------|------|
| 数据库 | SQLite `:memory:` 内存数据库，每个测试独立会话 |
| 主键兼容 | `BigInteger` 自动转换为 `Integer` |
| 种子数据 | `seed_data` fixture 提供用户、SKU、供应商 |
| 回滚 | 每个测试结束后自动回滚事务 |

**验证标准**：`uv run pytest tests/ -v` 全部通过，零失败。

---

### 规则23：文档编写规范（不可协商）

| 条目 | 内容 |
|------|------|
| 规则 | 编写 IMS 系统说明书和用户操作手册时，必须严格遵守 `docs/文档编写规范.md`。 |

**编写每章后 Trae 必须自查：**

- 标题层级正确（不超过四级）
- 所有状态值使用代码格式（`` `STATUS` ``）
- 所有按钮名称加粗（**按钮**）
- 所有表格有表头对齐标记
- Mermaid 图表标注语言类型
- 操作步骤使用 `**步骤N：标题**` 格式
- 路径使用 `→` 连接
- 注意事项用 `⚠️` 前缀
- 代码块标注语言类型
- 图片路径正确（相对路径）
- 无绝对路径引用
- 所有枚举值/状态值/字段名与代码一致

**触发词：** "编写说明书第X章" → 开始编写《系统说明书》对应章节；"编写操作手册第X章" → 开始编写《用户操作手册》对应章节；"检查文档规范" → 按上述清单逐项核对。

> 📋 **参考数据**（权限矩阵、表结构、业务逻辑、迁移说明）→ 见 `.trae/rules/reference.md`，AI 按需读取。