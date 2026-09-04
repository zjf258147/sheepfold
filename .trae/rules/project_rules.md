# 敦临 IMS 生产物料与产品追溯管理系统 - Trae 开发规则

> **所属单位**：西安敦临计量检测有限公司
> **系统简称**：敦临 IMS（DL-IMS）

## 1. 项目概述

### 1.1 设计目标

用一套系统完整替代 3 张 Excel（到货台账、出货台账、退货台账），实现 **"来料检测 → BOM生产准备 → 发货 → 异常退货（维修/再出货）→ 最终去向"** 全流程闭环管理。

### 1.2 技术栈（重点，不可更改）

| 层级 | 技术 |
|------|------|
| 后端框架 | Python 3.12+ / FastAPI |
| 前端框架 | Vue 3 + Vite + Element Plus + Pinia |
| 数据库 | MySQL 5.7 |
| ORM | SQLAlchemy 2.0+ |
| 数据库迁移 | Alembic |
| 部署 | Docker Compose（MySQL + Backend + Frontend） |
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

> 📋 **开发使用说明**：`doc/开发使用说明.md`（启动方式、访问地址、常见问题）  
> 🐛 **环境问题排查**：`doc/开发环境问题记录.md`（9个问题及解决方案）

---

## 2. Trae 开发宪法规则

### 规则1：Git 版本控制（不可协商）

| 条目 | 内容 |
|------|------|
| 规则 | 每次修改代码前必须先提交当前版本。每次功能完成后必须提交新版本。 |
| 提交格式 | `[模块名] 操作说明`，如 `[audit] 新增 change_reason 字段` |
| 辅助 Skill | 提交时使用 `git-commit` Skill 自动生成符合格式的 commit message 并推送 |
| 验证标准 | `git log --oneline -5` 能看到 ≥5 条记录，每条符合格式 |

### 规则2：数据库备份（不可协商）

| 条目 | 内容 |
|------|------|
| 规则 | 任何数据库结构变更（新增表/字段/修改字段类型/修改枚举）前必须备份。数据迁移必须在测试环境验证通过后才能在生产执行。 |
| 备份命令 | `docker exec ims-db mysqldump -u root -p ims > backup_$(date +%Y%m%d_%H%M%S).sql` |
| 验证标准 | 备份文件大小 > 0KB 且能正常 `mysql < backup.sql` 还原 |

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
| 规则 | 主线A/B/C/D 按顺序开发，前一条主线完全验证通过后，再开始下一条。 |
| 验证标准 | 主线A全部功能通过验收清单后方可开始主线B，依此类推 |

### 规则7：复用现有表，不重复建表

| 条目 | 内容 |
|------|------|
| 规则 | 供应商使用现有 `partner` 表（外键 `supplier_id`），物料使用现有 `product_sku` 表（外键 `sku_id`），不新建供应商表或物料表。 |
| 验证标准 | `incoming_receipt` 和 `rma_return` 表中使用外键关联，而非文本字段 |

### 规则8：通用验收通则（所有功能默认包含）

每完成一个功能点，除该功能点专项验证外，还必须满足以下通则：

| 编号 | 通则内容 | 验证方式 |
|------|----------|----------|
| T-0001 | 操作后审计日志新增记录 | `SELECT * FROM audit_log WHERE entity_no = '单据号' ORDER BY created_at DESC LIMIT 1;`，能查到记录 |
| T-0002 | 变更原因不为空 | 审计日志 `change_reason` 字段非空 |
| T-0003 | 页面响应式 | 手机浏览器打开，界面不破碎、按钮可点 |
| T-0004 | 权限正确 | 用非授权账号尝试操作，返回"无权限"提示 |

### 规则9：后端开发规范

| 条目 | 内容 |
|------|------|
| 模型定义 | 所有新增 Model 放在 `backend/app/models/`，继承 `Base` |
| Schema定义 | 所有新增 Pydantic Schema 放在 `backend/app/schemas/` |
| API路由 | 所有新增 API 放在 `backend/app/api/`，路径前缀 `/api/v1/` |
| 编号生成 | 统一在 `utils/order_no.py` 中扩展，新增 RC/FC/SH/BOM/PR 前缀 |
| 枚举定义 | 所有枚举统一放在 `backend/app/models/enums.py` |
| 服务层 | 复杂业务逻辑放在 `backend/app/service/` |
| 外键关联 | 新增表涉及供应商/物料的，使用 `supplier_id`/`sku_id` 外键，而非文本 |
| 模糊搜索 | 复用 `inventory_service._keyword_filter` 函数，支持 LIKE 模糊匹配 SN 和商品名；新模块 Service 中直接导入使用 |
| 数据完整性 | 从 `product_sku` 填充业务表冗余字段时，若 `unit` 为 NULL，默认赋值为 `'个'`（兜底），避免 NOT NULL 约束报错 |

### 规则10：前端开发规范

| 条目 | 内容 |
|------|------|
| 组件复用 | 优先使用 TablePro、SearchForm 等现有组件 |
| 搜索模式 | 新页面搜索区参考 `InventoryDetail.vue` 模式：keyword 文本输入 + 分类下拉 + SKU 联动下拉 + 状态筛选 + 日期范围，支持模糊搜索和组合筛选 |
| 路由规范 | 参考 `router/index.js` 现有命名规范，使用懒加载 |
| 菜单配置 | 在 `MainLayout.vue` 的 `allMenus` 中配置，使用 `roles` 数组控制权限 |
| 权限控制 | 所有路由和菜单必须配置 `roles` 或 `adminOnly` |
| API调用 | 统一使用 `api/` 目录下的封装方法 |

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

每次功能开发完成后、提交代码前，必须按以下顺序调用 Skill 进行检查验证。按技术栈分类：

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

**`systematic-debugging` 核心铁律**：未完成根因调查前，禁止提出任何修复方案。症状修复 = 失败。

**验证标准**：每次 `git commit` 前，上述 Skill 检查结果必须全部通过。如有未通过项，必须先修复再提交。

---

### 规则13：技术栈 Skill 清单（已安装 14 个）

| 类别 | Skill 名称 | 来源 | 安装量 | 安全 |
|------|-----------|------|:------:|:---:|
| 后端 | `fastapi-python` | mindrally/skills | 12.5K | ✅ |
| 后端 | `sqlalchemy-alembic-expert-best-practices-code-review` | wispbit-ai/skills | 1.6K | ✅ |
| 前端 | `vue` | antfu/skills | 33K | ✅ |
| 前端 | `pinia` | antfu/skills | 17.7K | ✅ |
| 数据库 | `mysql` | planetscale/database-skills | 7.5K | ⚠️ Med |
| 数据库 | `mysql-best-practices` | mindrally/skills | 2.5K | ✅ |
| Docker | `docker-patterns` | affaan-m/ecc | 11K | ⚠️ High |
| 测试 | `webapp-testing` | anthropics/skills | 149K | ✅ |
| 审查 | `code-review-and-quality` | addyosmani/agent-skills | 36.1K | ✅ |
| 审查 | `code-quality-skill` | 本地 | — | ✅ |
| 审查 | `detect-code-smells` | 本地 | — | ✅ |
| 调试 | `systematic-debugging` | obra/superpowers | 246K | ✅ |
| 调试 | `bug-detective` | 本地 | — | ✅ |
| 文档 | `upkeep` | 本地 | — | ✅ |

---

### 规则14：新 Skill 双次验证（不可协商）

| 条目 | 内容 |
|------|------|
| 规则 | 每次新安装的 Skill，必须分别调用 2 次验证其加载成功。首次调用确认路径正确，二次调用确认稳定可用。 |
| 验证方式 | 每个 Skill 分两批调用（每批 2 个），两轮全部通过后方可投入使用 |
| 验证标准 | 两次调用均返回 Skill 完整内容（路径 + 描述 + 详情），无报错、无截断 |

**已验证 Skill 清单（2026-09-03）：**

| Skill | 第1次 | 第2次 | 状态 |
|-------|:---:|:---:|:---:|
| `fastapi-python` | ✅ | ✅ | 就绪 |
| `sqlalchemy-alembic-expert-best-practices-code-review` | ✅ | ✅ | 就绪 |
| `vue` | ✅ | ✅ | 就绪 |
| `pinia` | ✅ | ✅ | 就绪 |
| `mysql` | ✅ | ✅ | 就绪 |
| `mysql-best-practices` | ✅ | ✅ | 就绪 |
| `docker-patterns` | ✅ | ✅ | 就绪 |
| `webapp-testing` | ✅ | ✅ | 就绪 |
| `code-review-and-quality` | ✅ | ✅ | 就绪 |

---

### 规则15：搜索功能复用（不可协商）

| 条目 | 内容 |
|------|------|
| 规则 | 新模块（主线A/B/C/D）的列表页面必须包含搜索功能。后端模糊搜索统一复用 `inventory_service._keyword_filter` 函数，前端搜索区参考 `InventoryDetail.vue` 模式。 |
| 后端复用 | `from app.service.inventory_service import _keyword_filter`，该函数支持：单关键词模糊匹配 SN + 商品名（`LIKE %keyword%`），多行批量搜索 SN（最多 100 个），OR 逻辑连接 |
| 前端模式 | 每个新列表页面至少包含：① 关键词输入框（`keyword`）② 分类下拉（联动 SKU）③ 状态筛选 ④ 日期范围。根据业务场景可增减 |
| 验证标准 | 在搜索框输入关键词后，列表数据按条件过滤；输入部分 SN 能模糊匹配到结果；多行粘贴多个 SN 能批量搜索 |

---

### 规则16：Excel 导出格式规范（不可协商）

| 条目 | 内容 |
|------|------|
| 规则 | 所有业务模块的 Excel 导出统一使用 `item_export.py` 中的通用工具函数，格式统一、美观、专业。 |
| 标题行 | 第1行，深蓝背景 `#4472C4` + 白色粗体 11pt + 居中，列名作为标题 |
| 表头 | （无独立标题行，标题行即列名行） |
| 数据行 | 白色/浅蓝交替斑马纹（`#FFFFFF` / `#DDEBF7`），全表细线边框（`#999999`），自动筛选器 |
| 金额列 | 千分位格式 `#,##0.00`，右对齐 |
| 数量列 | 整数格式 `#,##0`，居中对齐 |
| SN列 | 文本格式（避免科学计数法） |
| 长文本列 | 自动换行（`wrap_text=True`） |
| 列宽 | 序号6 / 编码18 / 名称25 / 规格18 / 数量12 / 日期14 / 金额14 / 备注30 / 其他12 |
| 冻结 | 标题行冻结（冻结首行） |
| 文件名 | 格式 `IMS-{模块名}-{内容}-{日期}.xlsx`，如 `IMS-来料到货-20260904.xlsx` |
| 验证标准 | 下载导出的 Excel 文件，检查：标题行深蓝白字、斑马纹交替、边框完整、金额有千分位、SN为文本、自动筛选可用、滚动时标题固定 |

---

### 规则17：调试流程（不可协商）

| 条目 | 内容 |
|------|------|
| 规则 | 遇到任何报错/异常/bug，必须先调用 `systematic-debugging` Skill 定位根因，再动手改代码。禁止跳过调试直接猜测修复。 |
| 流程 | 报错 → 调用 `systematic-debugging` → 找到根因 → 修复 → 验证 |
| 验证标准 | 修复后错误不再复现，且 `systematic-debugging` 4阶段全部走完 |

### 规则18：前端验证流程（不可协商）

| 条目 | 内容 |
|------|------|
| 规则 | 每次修改前端页面后，调用 `webapp-testing` Skill 在浏览器中自动验证功能，不依赖手动 F5 刷新。 |
| 验证内容 | 页面加载、元素可见性、按钮点击、表单输入、弹窗交互、API 响应断言（非仅截图） |
| 验证标准 | `webapp-testing` 报告全部通过，关键交互有 Playwright 脚本可复用 |

---

### 规则19：主线完成验证与文档归档（不可协商）

| 条目 | 内容 |
|------|------|
| 规则 | 每完成一个主线（A/B/C/D），必须执行前后端运行验证，并将该主线的新增/变更内容归档为文档。 |
| 验证流程 | ① 启动后端 `python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000` ② 启动前端 `npm run dev` ③ 浏览器访问 http://localhost:5173 ④ 登录验证 ⑤ 进入对应模块页面，验证核心功能（列表→搜索→新增→编辑→弹窗） |
| 文档归档 | 在 `doc/` 下创建 `主线X_完成报告.md`，记录：新增表/字段/Schema/API/前端页面/组件/路由/菜单、编号规则、业务规则、验收结果 |
| 验证标准 | 前后端均无报错启动，浏览器能正常登录并访问新模块，核心 CRUD 操作可执行，完成报告已创建 |

### 规则20：开发环境问题记录（不可协商）

| 条目 | 内容 |
|------|------|
| 规则 | 每次开发环境搭建或启动过程中遇到的问题及解决方案，必须记录到 `开发环境问题记录.md`，供后续参考。 |
| 记录内容 | 问题现象、根因分析、解决方案、涉及的命令 |
| 存放位置 | `doc/开发环境问题记录.md` |
| 验证标准 | 文件存在，每个问题有完整的"现象→原因→解决"三段式记录 |

---

## 3. 验收检查点速查表

| 检查项 | 命令/操作 | 预期结果 |
|--------|-----------|----------|
| Git记录 | `git log --oneline -5` | 5条以上记录，格式规范 |
| Skill检查 | 按规则12分类触发：①code-quality ②detect-smells ③code-review ④systematic-debugging ⑤tech-stack ⑥webapp-testing ⑦upkeep | 全部通过，无阻塞项 |
| 数据库表 | `SHOW TABLES;` | 新增表可见 |
| 审计日志 | `SELECT * FROM audit_log WHERE entity_no='RC20260901001';` | 有记录 |
| 角色权限 | 不同角色登录 | 菜单按权限显示 |
| SN关联 | 维修完成 | 新旧SN互相关联 |
| 变更原因 | 状态变更时 | 弹窗必填，不填不可提交 |
| 外键关联 | `DESC incoming_receipt;` | `supplier_id`、`sku_id` 存在且为外键 |
| 模糊搜索 | 在各列表页搜索框输入关键词 | 数据按条件过滤，部分 SN 可模糊匹配，多行 SN 可批量搜索 |
| Excel导出 | 点击导出按钮，打开下载的 xlsx | 标题行+表头+数据完整，斑马纹、边框、金额格式正确，自动筛选可用 |

---

## 4. 开发顺序

### 开发顺序（按优先级）

```
数据库备份 + Git → product_sku改造 → 审计日志改造 → 角色扩展 → SN表改造
→ 原材料库存表 → 主线A（来料管理）→ 主线B（返厂维修）→ 主线C（出货管理）
→ 主线D（BOM）→ 权限与审计 → 扫码功能
```

### 里程碑

| 阶段 | 周期 | 交付物 | 验收标准 |
|------|------|--------|----------|
| 环境搭建 | 1天 | 部署IMS、数据库就绪 | `docker compose up` 成功，浏览器可访问 |
| 数据库改造 | 2天 | 新增16张表、改造SN表、创建审计日志表 | 对应"数据库验证 SQL"全部可执行 |
| 主线A开发 | 4天 | 到货登记→检验→入库→退货 全部功能 | A-01 至 A-07 全部通过 |
| 主线B开发 | 6天 | 退货登记→诊断→分配→维修→换SN→流转→报废审批→再出货 | B-01 至 B-16 全部通过 |
| 主线C开发 | 2天 | 出货登记 | C-01 至 C-04 全部通过 |
| 主线D开发 | 3天 | BOM导入导出→库存对比→采购建议 | D-01 至 D-08 全部通过 |
| 权限与审计 | 2天 | 权限矩阵落地、审计日志验证 | L-01 至 L-05 + P-01 至 P-05 全部通过 |
| 扫码功能 | 1天 | 所有SN输入框接入扫码组件 | S-01 至 S-02 通过 |
| 测试与数据迁移 | 3天 | 2026年历史数据导入、全员测试 | UAT通过 |

---

> 📋 **参考数据**（权限矩阵、表结构、业务逻辑、迁移说明）→ 见 `.trae/rules/reference.md`，AI 按需读取。