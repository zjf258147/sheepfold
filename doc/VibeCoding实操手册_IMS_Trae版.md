# DL-IMS Vibe Coding 终极实操手册（Trae IDE 版）

> **核心理念**：Vibe Coding = 自然语言意图 + Trae AI 执行 + 人机协同调试。  
> 你搭架构、定规则、给证据，Trae 补细节。把"聊天记忆"变成"项目记忆"。
>
> **适用项目**：西安敦临计量检测有限公司 — IMS 生产物料与产品追溯管理系统  
> **适用 IDE**：Trae IDE（`.trae/rules/` + `.trae/skills/`）

---

## 一、项目初始化（已完成 90%）

### 1. 当前仓库结构（与 Vibe Coding 标准结构对照）

```text
IMS生产物料与产品追溯管理系统/     # 仓库根目录
├── .trae/                          # ✅ 替代 .cursor/rules + .claude/commands
│   ├── rules/                      # Trae 规则（自动加载到每次对话）
│   │   ├── project_rules.md        # 24条开发宪法（核心文件）
│   │   └── reference.md            # 参考数据（权限矩阵、表结构、业务逻辑）
│   └── skills/                     # Trae Skill 层（共 19 个）
│       ├── code-quality-skill/     # Python 代码质量
│       ├── detect-code-smells/     # 代码异味检测
│       ├── code-review-and-quality/# 多维度代码审查
│       ├── systematic-debugging/   # 系统化调试（4阶段铁律）
│       ├── bug-detective/          # 快速错误排查
│       ├── fastapi-python/         # FastAPI 最佳实践
│       ├── sqlalchemy-alembic-.../ # SQLAlchemy + Alembic
│       ├── vue/                    # Vue 3 Composition API
│       ├── pinia/                  # Pinia 状态管理
│       ├── mysql/                  # MySQL 设计审查
│       ├── mysql-best-practices/   # MySQL 最佳实践
│       ├── docker-patterns/        # Docker 模式
│       ├── webapp-testing/         # Playwright 浏览器测试
│       ├── dingtalk-notify/        # 钉钉通知
│       ├── excel-automation/       # Excel 自动化
│       ├── git-commit/             # Git 提交规范化
│       └── upkeep/                 # 文档代码一致性
├── ims-main/                       # ✅ 主项目目录
│   ├── backend/                    # Python 3.12+ / FastAPI / SQLAlchemy 2.0+
│   │   ├── app/
│   │   │   ├── api/                # API 路由层（/api/v1/）
│   │   │   ├── models/             # SQLAlchemy 模型
│   │   │   ├── schemas/            # Pydantic 请求/响应模型
│   │   │   ├── service/            # 业务逻辑层
│   │   │   ├── core/               # 配置、缓存、安全、调度
│   │   │   ├── db/                 # 数据库连接
│   │   │   ├── utils/              # 工具函数（编号生成等）
│   │   │   └── constants/          # 常量定义
│   │   ├── alembic/                # 数据库迁移
│   │   ├── tests/                  # pytest 测试（contract + scenario）
│   │   └── main.py                 # 入口文件
│   └── frontend/                   # Vue 3 + Vite + Element Plus + Pinia
│       └── src/
│           ├── api/                # API 请求封装
│           ├── components/         # Vue 组件（TablePro、SearchForm 等）
│           ├── layout/             # 布局组件（MainLayout）
│           ├── router/             # 路由配置
│           ├── stores/             # Pinia 状态管理
│           ├── utils/              # 工具函数
│           └── constants/          # 常量/枚举
├── PROJECT_STATE.md                # ✅ 当前进度、待办任务（根目录，AI自动维护）
├── doc/                            # ✅ 文档层
│   ├── 开发方案.md                  # 一期 + 二期总体方案
│   ├── 二期开发方案.md              # 二期详细方案
│   ├── 开发使用说明.md              # 开发环境搭建
│   ├── 开发环境问题记录.md          # ✅ lessons.md 等效（环境问题）
│   ├── bug记录.md                  # ✅ lessons.md 等效（Bug 教训）
│   ├── 主线A_完成报告.md            # 主线A 验收报告
│   ├── 主线B_完成报告.md            # 主线B 验收报告
│   ├── 主线C_完成报告.md            # 主线C 验收报告
│   └── VibeCoding实操手册_IMS_Trae版.md  # 🆕 本文件
└── docker-compose.yml              # Docker 部署
```

### 2. 必写文档对照（已完成检查）

| Vibe Coding 标准 | IMS 项目对应 | 状态 |
|------------------|-------------|:---:|
| PRD.md | `doc/开发方案.md` + `doc/二期开发方案.md` | ✅ |
| ARCH.md | `.trae/rules/project_rules.md` 第1节（技术栈 + 目录结构） | ✅ |
| PROJECT_STATE.md | 根目录 `PROJECT_STATE.md`（AI 自动维护） | ✅ |
| AGENTS.md / CLAUDE.md | `.trae/rules/project_rules.md`（24条开发宪法） | ✅ |
| docs/lessons.md | `doc/开发环境问题记录.md` + `doc/bug记录.md` | ✅ |
| docs/adr/ | 暂无（重大架构决策可后续补充） | ⬜ |
| skills/*.md | `.trae/skills/` 下 19 个 Skill | ✅ |
| evals/ | 暂无（建议后续补充 10+ 回归用例） | ⬜ |

### 3. 开发规范（已在 `.trae/rules/project_rules.md` 中完整定义）

核心规范摘要（完整版见 `project_rules.md`）：

| 规则编号 | 内容 |
|:---:|------|
| 规则0 | **对话前状态摘要**：每次对话先读 PROJECT_STATE.md + git log + git branch |
| 规则1 | **Git 版本控制**：每次修改前先提交，格式 `[模块名] 操作说明` |
| 规则2 | **数据库备份**：结构变更前必须 `mysqldump` 备份 |
| 规则3 | **单次改动可验证**：一次只改一个功能点 |
| 规则4 | **先界面后逻辑**：先做前端页面，再做后端 API |
| 规则5 | **变更原因强制弹窗**：状态变更必须填 `change_reason` |
| 规则6 | **主线独立可测**：每条主线独立验收 |
| 规则7 | **复用现有表**：不重复建供应商表/物料表 |
| 规则8 | **通用验收通则**：审计日志 + 变更原因 + 响应式 + 权限 |
| 规则9 | **后端开发规范**：Model → Schema → API → Service 分层 |
| 规则10 | **前端开发规范**：TablePro + SearchForm + 搜索模式 |
| 规则11 | **代码审查最低标准**：无硬编码、字段完整、审计覆盖、向后兼容 |
| 规则12 | **Skill 检查验证**：14个 Skill 按触发条件调用 |
| 规则13 | **Excel 导出格式**：深蓝标题 + 斑马纹 + 千分位 + SN 文本 |
| 规则14 | **搜索功能复用**：`_keyword_filter` + 前端搜索区模式 |
| 规则15 | **全局检查触发词**：搜索全部相关文件，逐一检查 |
| 规则16 | **主线收尾触发词**：7步收尾检查清单 |
| 规则17 | **完整检测清单触发词**：5步全量检测 |
| 规则18 | **大文件批量修改**：PowerShell 一次性替换 |
| 规则19 | **Bug 记录与追溯**：即时记录到 `doc/bug记录.md` |
| 规则20 | **开发环境问题记录**：记录到 `doc/开发环境问题记录.md` |
| 规则21 | **性能优化规范**：Redis 缓存 + MySQL 优化 + 虚拟滚动 + 游标分页 |
| 规则22 | **测试计划与执行**：合约测试 + 场景测试，自然语言触发词 |
| 规则23 | **文档编写规范**：11项自查清单 |

### 4. Git 与质量闸门（Trae 版）

| 闸门 | IMS 项目做法 |
|------|-------------|
| **计划闸** | 规则0：每次对话先输出状态摘要 + 改动范围，等用户确认 |
| **测试闸** | 规则22：`uv run pytest tests/ -v` 全部通过才算完成 |
| **审查闸** | 规则11 + 规则12：调用 `code-review-and-quality` Skill 多轴审查 |
| **安全闸** | 规则1（Git提交前）、规则2（数据库备份）、规则5（变更原因弹窗） |

---

## 二、每次任务的标准流程（七步闭环 — Trae 版）

### 步骤1：启动对话 → 自动状态检查

Trae 自动执行的 4 步（规则0）：

```
1. 读取 PROJECT_STATE.md
2. 运行 git log --oneline -3
3. 运行 git branch --show-current
4. 运行 git describe --tags --abbrev=0 2>/dev/null || echo "无 Tag"
```

**Trae 输出格式：**

```markdown
## 项目当前状态
- 版本：v2.6（一期完成，二期开发中）
- 分支：master | Tag：无
- 本次目标：[你的任务描述]

## 最近变更
[git log --oneline -3]

## 本次改动范围
- 只改：[文件路径]
- 不改：[排除范围]

## 约束
- 遵守《文档编写规范》
- 遵守《project_rules.md》全部24条规则
- 每次改动后运行检测清单对应项
```

**你只需回复"继续"或补充任务细节**，Trae 就开始工作。

### 步骤2：计划 → 输出改动清单

Trae 输出："要改哪些文件、为什么、用什么命令验证。不碰无关文件。先不写代码，等你确认。"

你在这一步可以：
- 确认范围正确 → 说"继续"
- 调整范围 → 说"不要改 XX，增加 YY"
- 补充细节 → 说"还要考虑 ZZ"

### 步骤3：执行 → 小步改、立即验证

Trae 会：
1. 每次只改 1-2 个文件
2. 改完立即跑对应验证命令
3. 不通过则修复后再继续

**项目验证命令速查：**

```bash
# 后端语法检查
cd ims-main/backend && uv run python -c "from app.api import *"

# 后端测试
cd ims-main/backend && uv run pytest tests/ -v --tb=short

# 前端构建检查
cd ims-main/frontend && npm run build

# 后端启动验证
cd ims-main/backend && uv run uvicorn main:app --port 8000 &

# 前端启动验证
cd ims-main/frontend && npm run dev

# 数据库迁移验证
cd ims-main/backend && uv run alembic upgrade head
```

### 步骤4：反馈 → 把报错贴给 Trae

如果步骤3出现报错，直接把错误信息贴回去。Trae 会调用 `systematic-debugging` Skill 进行4阶段根因分析。

### 步骤5：反思 → Trae 总结根因和规则

Trae 会输出：
- **根因**：为什么出错
- **可复用规则**：如何避免再犯
- **教训**：提炼成 1-3 条规则

### 步骤6：更新 → 写入仓库

Trae 会自动：
1. 新 Bug → 追加到 `doc/bug记录.md`
2. 新环境问题 → 追加到 `doc/开发环境问题记录.md`
3. 重复3次的流程 → 封装为新 Skill（放到 `.trae/skills/`）
4. 更新 `PROJECT_STATE.md`（如果状态有变化）
5. Git 提交（使用 `git-commit` Skill 生成合规 message）

### 步骤7：下次继承 → 新对话自动加载

下次开新对话，Trae 规则0会自动读取所有更新的文件，之前的经验教训不会丢失。

> **关键**：只在聊天里说"下次注意"没用，必须写进仓库（`doc/bug记录.md` / `.trae/rules/` / `.trae/skills/`），并且下次会被 Trae 自动加载。

---

## 三、关键技巧（IMS 项目专项）

### 需求澄清

| 原则 | IMS 项目实践 |
|------|-------------|
| 四要素定义 | **用户**（质检员/仓管员/管理员）→ **场景**（到货检验/返厂维修/出货发货）→ **问题**（当前流程痛点）→ **解决方案**（新增/修改页面/接口） |
| 避免模糊 | ❌"优化库存管理" → ✅"库存明细页增加'仅看库存不足'筛选，库存量 < 安全库存时红色高亮" |
| Trae 复述 | 每次任务前，Trae 自动输出改动范围和约束，确保理解一致 |
| Plan 模式 | Trae 规则0天然是 Plan 模式：先输出计划，确认后才执行 |

### 对话工程（Trae 专项）

| 原则 | IMS 项目实践 |
|------|-------------|
| AI 是协作伙伴 | Trae 不是魔法按钮，是你搭架构、它补细节的搭档 |
| 从大到小 | 先确定主线（A/B/C/D），再细分功能点，最后到具体文件 |
| 具体而非抽象 | ❌"修好返厂维修页面" → ✅"RMA页面维修记录表新增'维修人员'列，数据库 `rma_repair` 表已有 `technician` 字段" |
| 用提问引导 | "这个字段应该在列表页显示还是只在详情页显示？""是否需要导出功能？" |

### 分期与架构

IMS 项目已有清晰分期：

| 分期 | 内容 | 状态 |
|:---:|------|:---:|
| 一期 | 主流程闭环（来料A + 返厂B + 出货C + BOM准备D） | ✅ 已完成 |
| 二期 | 运营增强（场站 + 设备台账 + 盘点 + 库存调整 + 客户扩展） | 🔄 进行中 |
| 三期 | 待规划 | ⬜ |

**架构决策参考**：
- 详细设计文档：`doc/开发方案.md`、`doc/二期开发方案.md`
- 技术栈锁定：`project_rules.md` 第1.2节（不可更改）
- 每期"不做什么"：见各期方案文档的"范围外"部分

### 技术栈锁定（不可更改）

| 层级 | 技术 | 版本要求 |
|------|------|----------|
| 后端框架 | FastAPI | Python 3.12+ |
| 前端框架 | Vue 3 + Element Plus | Composition API + `<script setup>` |
| 状态管理 | Pinia | 最新稳定版 |
| ORM | SQLAlchemy | 2.0+ |
| 数据库 | MySQL | 5.7 |
| 缓存 | Redis | 7（Docker）/ 内存（本地降级） |
| 迁移 | Alembic | 最新稳定版 |
| 部署 | Docker Compose | MySQL + Redis + Backend + Frontend |
| 包管理(Python) | uv | 最新版 |
| 包管理(JS) | npm | 最新版 |
| 后端端口 | 8000 | — |
| 前端端口 | 8080 | — |

### 测试与验收

**上线前必做：需求验收对照检查**

| 步骤 | 操作 |
|:---:|------|
| ① | 打开 `doc/开发方案.md` 或 `doc/二期开发方案.md`，找到对应功能的需求描述 |
| ② | 逐条对照需求，确认每个功能点都已实现且通过测试 |
| ③ | 确认需求中的"边界条件"已覆盖（如：空数据、超长SN、负数数量等） |
| ④ | 确认需求中的"范围外"功能没有被意外实现 |

**非功能需求验收：**

| 检查项 | 标准 |
|--------|------|
| 响应时间 | 列表页首次加载 < 3秒，详情页 < 1秒 |
| 并发能力 | 10 个用户同时操作不报错 |
| 数据一致性 | 关键操作（入库/出货/退货）的事务完整性 |
| 浏览器兼容 | Chrome / Edge 最新版无兼容问题 |
| 移动端 | 手机浏览器访问，界面不破碎、按钮可点（规则8 T-0003） |

| 类型 | 命令 | 标记 |
|------|------|:---:|
| 全部测试 | `uv run pytest tests/ -v` | — |
| 合约测试 | `uv run pytest tests/contract/ -v -m contract` | `contract` |
| 场景测试 | `uv run pytest tests/scenario/ -v -m scenario` | `scenario` |
| 主线A | `pytest tests/contract/test_incoming_contract.py tests/scenario/test_scenario_mainline_a.py -v` | — |
| 主线B | `pytest tests/contract/test_rma_contract.py tests/scenario/test_scenario_mainline_b.py -v` | — |
| 主线C | `pytest tests/contract/test_shipment_contract.py tests/scenario/test_scenario_mainline_c.py -v` | — |
| 主线D | `pytest tests/contract/test_bom_contract.py tests/scenario/test_scenario_mainline_d.py -v` | — |
| 覆盖率 | `uv run pytest tests/ --cov=app --cov-report=html` | — |

**测试隔离**：SQLite `:memory:` 内存数据库，每个测试独立会话，自动回滚。

**自然语言触发词**：

| 你说的话 | Trae 自动执行 |
|----------|-------------|
| "跑测试"、"全部测试" | `uv run pytest tests/ -v` |
| "合约测试" | `uv run pytest tests/contract/ -v -m contract` |
| "场景测试" | `uv run pytest tests/scenario/ -v -m scenario` |
| "主线A测试" | 主线A 合约 + 场景测试 |
| "覆盖率" | `uv run pytest tests/ --cov=app --cov-report=html` |

**证据四类**：
1. **自动化证据**：pytest 测试结果（合约 + 场景）
2. **结构证据**：Alembic 迁移脚本 + 模型定义
3. **行为证据**：Playwright 浏览器截图（`webapp-testing` Skill）
4. **人工审查证据**：diff 审查 + 代码审查 Skill 输出

### 限制 Trae 范围（核心技巧）

| 技巧 | IMS 项目实践 |
|------|-------------|
| 状态摘要锁定 | 每次对话开始 Trae 输出"只改/不改"范围，你确认后生效 |
| 明确排除 | 说"不要动前端页面，只改后端 API"或"只改 Station.vue，不动其他文件" |
| 减法设计 | 新增功能问自己：这个字段真的需要吗？这个筛选条件能砍吗？ |
| 不乱改封装 | `TablePro`、`SearchForm` 等组件封装好后，要求 Trae"复用现有组件，不修改" |

### 参考实现复用

| 原则 | IMS 项目实践 |
|------|-------------|
| 新增页面前 | 先找现有最相似的页面做模板（如新增列表页 → 参考 `InventoryDetail.vue`） |
| 新增 API 前 | 先找现有最相似的 API 做模板（如新增 CRUD → 参考 `incoming.py` 的路由结构） |
| 新增模型前 | 先找现有最相似的表结构做模板（如新增台账 → 参考 `inventory.py` 的字段设计） |
| 封装组件 | 跨页面重复使用 3 次以上的 UI 模式，封装为通用组件放入 `components/` |
| 标准示例 | 建议建 `references/` 文件夹，存放标准 API 响应格式、错误处理示例、组件用法模板 |

> **待完善**：计划在 `.trae/references/` 下建立标准示例库（API 响应格式、错误处理、组件模式），新建功能时 Trae 自动参考。

### 安全底线（IMS 项目专项）

| 原则 | IMS 项目实践 |
|------|-------------|
| 密钥不入前端 | `.env` 文件（`ims-main/backend/.env`）存放数据库密码、Redis 密码、Secret Key |
| 鉴权校验 | 所有 API 通过 `deps.py` 的 `get_current_user` 依赖注入鉴权 |
| 权限控制 | 路由 + 菜单通过 `roles` 数组控制（admin/quality/warehouse/viewer） |
| 审计日志 | 所有关键操作写入 `audit_log` 表（规则8 T-0001） |
| 变更原因 | 状态变更必须填写 `change_reason`（规则5） |
| 不记录密钥 | `.env` 在 `.gitignore` 中，`.env.example` 只含模板不含真实值 |

**密钥管理专项检查（每次提交前）：**

| 检查项 | 命令 / 方法 |
|--------|------------|
| `.env` 不在 Git 暂存区 | `git status` 确认无 `.env` |
| 无硬编码密码/Key | `Grep` 搜索 `password\s*=\s*['\"]`、`secret\s*=\s*['\"]`、`api_key\s*=\s*['\"]` |
| `.env.example` 只含模板 | 确认所有值都是 `your_xxx_here` 或 `change_me` 格式 |
| JWT Secret 复杂度 | 至少 32 位随机字符串，不是 `secret`、`123456` 等弱密码 |
| 数据库密码 | 不是 `root`、`password`、`123456` |
| 生产环境 | 使用密钥管理服务，不手动管理 `.env` |

### 上下文管理（三层）

| 层级 | 文件 | 加载方式 |
|------|------|----------|
| **项目级** | `.trae/rules/project_rules.md`（24条规则）+ `reference.md`（参考数据） | Trae 每次对话自动加载 |
| **功能级** | `PROJECT_STATE.md`（当前进度）+ `doc/二期开发方案.md`（需求） | 对话开始时 Trae 读取 |
| **对话级** | 当前对话中的临时信息、改动范围约定 | 随对话结束而消失 |

**跨会话续接**：一个任务完成后，Trae 自动更新 `PROJECT_STATE.md` + Git 提交，下次对话从最新状态继续。

### 多 Agent / 多 Skill 编排

IMS 项目已有完整的 Skill 编排体系（规则12）：

| 阶段 | 调用的 Skill | 触发条件 |
|------|-------------|----------|
| **Plan** | 无（Trae 规则0 自带 Plan 模式） | 每次对话开始 |
| **执行前检查** | `code-quality-skill` + `detect-code-smells` | 后端代码修改时 |
| **Debug** | `systematic-debugging`（首选）+ `bug-detective`（备用） | 出现报错/异常时 |
| **技术栈审查** | `fastapi-python` / `sqlalchemy-alembic-...` / `vue` / `pinia` / `mysql` / `docker-patterns` | 按修改范围触发 |
| **Review** | `code-review-and-quality` | 合并前 / 重大改动 |
| **测试** | `webapp-testing`（Playwright 浏览器验证） | 前端功能完成时 |
| **一致性** | `upkeep` | 文档代码一致性检查 |

**触发词**："检查"、"全面检查"、"全量检查" → Trae 按顺序调用全部 19 个 Skill。

---

## 四、自进化体系（五层 — IMS 项目对照）

| 层级 | Vibe Coding 标准 | IMS 项目落地 | 状态 |
|:---:|------------------|-------------|:---:|
| **Memory 记忆层** | AGENTS.md、lessons.md、.cursor/rules | `.trae/rules/project_rules.md` + `PROJECT_STATE.md` + `doc/bug记录.md` + `doc/开发环境问题记录.md` | ✅ |
| **Policy 策略层** | 任务模板、Slash Command | 规则0（对话前状态摘要）+ 规则16（主线收尾7步）+ 规则17（5步全量检测） | ✅ |
| **Skill 技能层** | .cursor/rules/*.mdc、skills/*.md | `.trae/skills/` 下 19 个 Skill | ✅ |
| **Tool 工具层** | scripts/、Makefile、package.json scripts | `ims-main/backend/app/utils/`（编号生成、导出工具等） | ⚠️ |
| **Model 模型层** | evals/、RAG、few-shot 示例库 | 暂无（待建立 `evals/`） | ⬜ |

**个人优先级：Memory → Policy → Skill → Tool → Model**  
前 3 层已基本完善，第 4 层按需扩展，第 5 层建议先建 10 条回归用例。

> **📋 evals/ 建设计划**（P1，二期 P0 完成后建）：
> - 位置：`ims-main/backend/tests/regression/`
> - 格式：pytest（与现有测试体系一致，无需新框架）
> - 数量：先建 10 条核心业务流程回归用例
> - 覆盖：来料→入库→出货→返厂→维修→再出货 全流程
> - 触发：每次修改规则前跑一遍，防止规则越改越偏
> - 后续：逐步扩充到 30+ 条

### 封装规则（IMS 项目实践）

| 场景 | 做法 |
|------|------|
| 重复 3 次的流程 | 封装为新 Skill（放到 `.trae/skills/`），或追加到 `project_rules.md` |
| 每次任务后复盘 | 提取 1-3 条可复用规则，追加到 `doc/bug记录.md` |
| 改规则前先验证 | 目前无 evals，建议先建 10 条回归用例再大规模改规则 |
| Git 管理进化 | 每次规则更新通过 Git 提交，`[rules] 更新规则XX`，可 review、可回滚 |
| 人工审核 | 错误经验写进规则会污染以后所有任务，Update 必须人工确认 |

### 避坑（IMS 特供）

1. **规则22 必须执行**：每次改代码后必须 `uv run pytest tests/ -v`，不跑测试就提交 = 给自己埋雷。
2. **规则5 不能忘**：所有状态变更前端必须有弹窗，后端必须校验 `change_reason`，这是审计追溯的命根子。
3. **规则7 不要违反**：用外键 `supplier_id`/`sku_id`，不要存文本"供应商A"。
4. **规则18 大文件用 PowerShell**：800行以上的文件不要逐行 Edit，用 PowerShell 批量替换。
5. **安全第一**：`.env` 绝不提交到 Git，API Key 绝不入前端。
6. **规则要短**：每条规则 2-3 句话 + 验证标准，不要长篇大论。

---

## 五、可直接复制的提示词模板（Trae 版）

### 任务前

```
[直接发任务描述即可，Trae 会自动执行规则0：
1. 读 PROJECT_STATE.md
2. 运行 git log --oneline -3
3. 输出状态摘要和改动范围
4. 等你确认]

示例：
"在 RMA 退货页面增加'维修人员'列，这个字段在 rma_repair 表已有 technician 字段。只改前端 RMA.vue 和后端 RMA schema，不改其他文件。"
```

### 任务后复盘 + 更新

```
复盘本次任务并持久化：
1. 读 git diff 和测试输出
2. 提取 1-3 条可复用规则，追加到 doc/bug记录.md
3. 如果流程重复3次以上，生成 .trae/skills/xxx/SKILL.md
4. 更新 PROJECT_STATE.md 的待办任务状态
5. 不要记录任何密钥
6. 用 git-commit Skill 生成合规 commit message
```

### 封装新 Skill

```
这个流程我们重复3次了，请封装成 Skill：
- 在 .trae/skills/ 下新建 {skill-name}/ 文件夹
- 创建 SKILL.md（参考现有 Skill 的格式）
- 更新 .trae/rules/project_rules.md 规则12的 Skill 列表
```

### 封装脚本工具

```
把刚才的临时 Python 脚本封装成 tools/ 目录下的独立工具：
- 放入 ims-main/backend/app/utils/（如果是项目工具）
- 或放入 scripts/（如果是独立脚本）
要求：有命令行参数、--help、错误处理。
```

### 主线收尾

```
"主线A收尾" / "完成来料管理验收"
→ Trae 自动执行规则16 的 7 步收尾检查：
① 代码质量 ② 代码异味 ③ 技术栈检查
④ 浏览器验证 ⑤ 后端启动 ⑥ 前端启动 ⑦ 输出报告
```

### 全局检查

```
"全局检查" / "全面检查" / "check all"
→ Trae 自动搜索该模块全部相关文件，逐一检查，输出报告
```

### 完整检测清单

```
"执行完整检测清单"
→ Trae 按5步顺序执行：
① 后端测试 ② 前端测试 ③ Skill 代码质量检查
④ 技术栈专项检查 ⑤ 上线检查
```

---

## 六、最小执行清单（IMS 项目定制）

1. **✅ 已完成**：仓库结构 + 核心文档（开发方案、PROJECT_STATE、24条规则、19 Skill）
2. **✅ 已完成**：开发规范 + Git + 质量闸门
3. **每次任务**：Trae 自动读规则（规则0），你只需确认
4. **每次任务**：Trae 输出计划，你确认后再写代码
5. **每次任务**：小步开发，一次一个功能点
6. **每次任务**：`uv run pytest tests/ -v`（规则22）
7. **每次任务**：提供测试结果 + diff 审查
8. **每次任务**：用状态摘要锁定范围，遵守安全底线
9. **每次任务**：测试通过 + Git 提交（规则1）
10. **任务后**：复盘，提取规则写入 `doc/bug记录.md`
11. **重复3次**：封装成 `.trae/skills/` 新 Skill
12. **改规则前**：先建 `evals/`，跑回归验证
13. **上下文管理**：三层管理 + PROJECT_STATE.md 续接
14. **报错处理**：贴给 Trae → `systematic-debugging` Skill 诊断
15. **多 Skill 编排**：Plan（规则0）→ Debug（systematic-debugging）→ Review（code-review-and-quality）
16. **Git 管理**：每次规则更新可 review、可回滚
17. **保持心流**：一个对话一个任务，做完再开新对话

---

## 七、今天就能做的 6 件事（已完成对照）

| # | Vibe Coding 建议 | IMS 项目状态 |
|:---:|------------------|:---:|
| 1 | 建 AGENTS.md | ✅ `.trae/rules/project_rules.md`（24条规则） |
| 2 | 建 docs/lessons.md | ✅ `doc/bug记录.md` + `doc/开发环境问题记录.md` |
| 3 | 建复盘命令 | ✅ 规则16（主线收尾）+ 规则17（完整检测清单） |
| 4 | 任务后更新 lessons | ✅ 规则19 + 规则20 |
| 5 | 重复3次封装 Skill | ✅ `.trae/skills/` 已有 19 Skill |
| 6 | 建 evals/ | ⬜ **待建**（建议放 `ims-main/backend/tests/regression/`） |

---

## 八、IMS 项目独有触发词速查表

| 触发词 | 自动行为 | 对应规则 |
|--------|----------|:---:|
| "继续" | 确认计划，开始执行 | 规则0 |
| "检查"、"全面检查"、"全量检查" | 按顺序调用全部 19 个 Skill | 规则12 |
| "全局检查"、"一致性检查" | 搜索模块全部文件，逐一检查 | 规则15 |
| "主线X收尾"、"XX验收" | 7步收尾检查 | 规则16 |
| "执行完整检测清单" | 5步全量检测 | 规则17 |
| "跑测试"、"全部测试" | `uv run pytest tests/ -v` | 规则22 |
| "合约测试" | 合约测试全部 | 规则22 |
| "场景测试" | 场景测试全部 | 规则22 |
| "主线A测试"~"主线D测试" | 对应主线合约+场景 | 规则22 |
| "覆盖率" | 生成 HTML 覆盖率报告 | 规则22 |

---

## 九、快速参考：IMS 常用命令

```bash
# === 开发启动 ===
# 后端
cd ims-main/backend && uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
# 前端
cd ims-main/frontend && npm run dev

# === 测试 ===
cd ims-main/backend && uv run pytest tests/ -v                    # 全部
cd ims-main/backend && uv run pytest tests/contract/ -v -m contract  # 合约
cd ims-main/backend && uv run pytest tests/scenario/ -v -m scenario  # 场景

# === 数据库 ===
cd ims-main/backend && uv run alembic upgrade head                 # 迁移
docker exec ims-db mysqldump -u root -p ims > backup_$(Get-Date -Format 'yyyyMMdd_HHmmss').sql  # 备份

# === Git ===
git log --oneline -5                                               # 最近提交
git add -A && git commit -m "[模块] 说明"                           # 提交（或让 Trae 用 git-commit Skill）

# === Docker ===
docker compose up -d                                               # 启动全部
docker compose down                                                # 停止
```

---

## 十、Git 回溯规范

### 10.1 什么时候回溯？

| 场景 | 判断标准 |
|------|---------|
| 连续两次修复失败 | 同一问题修复两次仍未解决 |
| 改动导致连锁报错 | 修A导致B/C/D多个模块报错 |
| 测试大面积失败 | 改动后测试通过率从100%骤降到<80% |

### 10.2 回溯步骤

| 步骤 | 操作 |
|:---:|------|
| ① | 停止继续修复 |
| ② | `git log --oneline -10` 查看最近提交 |
| ③ | 找到最后一个稳定版本（测试全绿的提交） |
| ④ | 执行 `git checkout [稳定版本]` 或 `git revert [问题提交]` |
| ⑤ | 在稳定版本上重新分析问题 |

### 10.3 主线完成后的归档

| 操作 | 命令 |
|------|------|
| 打 Tag | `git tag -a v1.0-milestone-A -m "[主线A] 验收通过"` |
| 备份数据库 | `docker exec ims-db mysqldump -u root -p ims > backup_$(Get-Date -Format 'yyyyMMdd').sql` |

### 10.4 回溯后的处理

| 步骤 | 操作 |
|:---:|------|
| ① | 分析根因 |
| ② | 写入 `doc/bug记录.md` |
| ③ | 重新计划（不要直接继续原来的方案） |

---

## 十一、文档更新流程

| 场景 | 更新什么 | 由谁触发 |
|------|---------|---------|
| 每次对话开始 | `PROJECT_STATE.md` 的"最近变更"章节 | Trae 规则0 自动执行 |
| 功能开发完成 | `PROJECT_STATE.md` 的"待办任务"状态 | 任务后复盘 |
| 发现新 Bug | `doc/bug记录.md` 追加记录 | 立即记录（规则19） |
| 遇到环境问题 | `doc/开发环境问题记录.md` 追加记录 | 解决后记录（规则20） |
| 主线验收通过 | `doc/主线X_完成报告.md` 生成报告 | 主线收尾（规则16） |
| 规则更新 | `.trae/rules/project_rules.md` + Git 提交 | 讨论确认后 |
| 新 Skill 创建 | `.trae/skills/xxx/SKILL.md` + 更新规则12 | 流程重复3次后 |
| 架构决策 | `doc/adr/`（建议建） | 重大技术选型时 |

---

**最终记住：**  
**执行 → 反馈 → 反思 → 写进仓库 → 下次自动加载 → 更好的行动。**  
**先图纸（开发方案），后地基（技术栈），再规矩（24条规则）；**  
**小步做，勤测试（pytest），给证据（合约+场景+Playwright），守心流（一个对话一个任务）；**  
**聊天记忆变项目记忆（`.trae/rules/` + `doc/bug记录.md` + `PROJECT_STATE.md`）。**