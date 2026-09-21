# IMS 生产物料与产品追溯管理系统

IMS 是一套面向生产、仓储和售后场景的物料与产品追溯管理系统，采用前后端分离架构，支持从来料、入库、库存、生产、出库到返厂维修的全流程管理。

## 核心能力

- **一物一码**：为每件产品分配唯一 SN，追踪入库、库存、出库和维修状态
- **库存管理**：采购入库、其他入库、出库、库存调整、盘点和库存流水
- **生产管理**：SKU、物料、BOM、生产任务和工位管理
- **质量与售后**：来料检验、RMA 返厂维修、故障统计和保修提醒
- **业务协同**：客户、供应商、合作方及产品资料统一管理
- **权限审计**：按角色控制菜单和操作权限，记录关键操作日志
- **导出与打印**：支持业务单据导出、打印及移动端访问

## 技术栈

| 层级 | 技术 |
| --- | --- |
| 前端 | Vue 3、Vite、Element Plus、Pinia、Axios |
| 后端 | Python 3.12+、FastAPI、SQLAlchemy 2、Pydantic |
| 数据库 | MySQL 5.7+ |
| 缓存 | Redis 7 |
| 迁移 | Alembic |
| 部署 | Docker Compose |

## 快速启动

### 使用 Docker Compose

环境要求：Docker 20.10+ 和 Docker Compose v2。

```bash
git clone https://github.com/zjf258147/sheepfold.git
cd sheepfold/ims-main
docker compose up -d --build
```

启动后访问：

| 服务 | 地址 |
| --- | --- |
| 前端系统 | http://localhost:8080 |
| 后端健康检查 | http://localhost:8000/health |
| Swagger API 文档 | http://localhost:8000/docs |

默认管理员账号为 `admin`，默认密码为 `admin123`。生产环境请通过环境变量修改管理员密码、数据库密码和 JWT 密钥。

停止服务：

```bash
docker compose down
```

### 本地开发

后端需要 Python 3.12+、uv 和 MySQL；前端需要 Node.js 20+。

```bash
# 后端
cd ims-main/backend
uv sync
uv run alembic upgrade head
uv run python scripts/init_admin.py
uv run uvicorn main:app --reload
```

```bash
# 前端（新终端）
cd ims-main/frontend
npm install
npm run dev
```

本地开发的详细环境变量和数据库配置见 [ims-main/README.md](ims-main/README.md) 与 [后端说明](ims-main/backend/README.md)。

## 项目结构

```text
sheepfold/
├── ims-main/
│   ├── backend/       # FastAPI API、业务服务、数据库迁移和测试
│   ├── frontend/      # Vue 3 Web 前端
│   ├── docs/          # 系统说明、部署和用户操作文档
│   ├── pic/           # 项目截图
│   └── docker-compose.yml
├── doc/               # 项目方案、测试记录和交付文档
└── README.md
```

## API 文档

开发模式启动后可通过以下地址查看接口：

- Swagger UI：`http://localhost:8000/docs`
- ReDoc：`http://localhost:8000/redoc`
- 健康检查：`http://localhost:8000/health`

## 文档

- [项目详细说明](ims-main/README.md)
- [后端开发说明](ims-main/backend/README.md)
- [用户操作手册](ims-main/docs/用户操作手册/IMS用户操作手册.md)
- [二次开发说明](ims-main/docs/二次开发说明书/)

## 许可

本项目的许可和使用范围以仓库中的项目约定为准。