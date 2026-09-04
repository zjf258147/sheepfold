# IMS 生产物料与产品追溯管理系统 - 部署到 Ubuntu 虚拟机指南

## 项目架构概览

| 服务 | 技术栈 | 端口 |
|------|--------|------|
| 前端 | Vue 3 + Element Plus + Nginx | 8080 |
| 后端 | Python 3.12 + FastAPI + SQLAlchemy | 8000 |
| 数据库 | MySQL 5.7 | 3306 |

---

## 第一步：将项目传输到 Ubuntu 虚拟机

在 Windows 宿主机上，将 `ims-main` 文件夹复制到 Ubuntu 虚拟机。有以下几种方式：

### 方式 A：使用共享文件夹（推荐）

在 VMware/VirtualBox 中设置共享文件夹，将 `ims-main` 目录映射到 Ubuntu 的 `/mnt/ims`。

### 方式 B：使用 scp 传输

在 Windows PowerShell 中执行：

```bash
scp -r C:\Users\25075\Desktop\IMS生产物料与产品追溯管理系统\ims-main 你的用户名@ubuntu的IP:/home/你的用户名/ims-main
```

### 方式 C：直接打包传输

在 Windows 上将 `ims-main` 文件夹打包为 zip，通过 U盘/拖拽 等方式传到 Ubuntu 后解压：

```bash
unzip ims-main.zip -d ~/
```

---

## 第二步：前置准备 —— 磁盘空间检查与清理

新安装的 Ubuntu 虚拟机默认磁盘可能只有 20G，更新软件包时容易报 **"设备上没有空间"** 错误。建议在执行后续步骤前先检查。

### 2.1 检查磁盘空间

```bash
# 查看磁盘使用率
df -h

# 查看各目录占用（找出大文件）
du -sh /* 2>/dev/null | sort -rh | head -20
```

如果 `/` 根分区使用率接近 100%，需要先清理。

### 2.2 清理磁盘空间

```bash
# 1. 清理 snap 旧版本（通常能释放 5~8G）
sudo snap list --all | awk '/disabled/{print $1, $3}' | while read name rev; do sudo snap remove "$name" --revision="$rev"; done

# 2. 清理 APT 缓存和旧包
sudo apt clean
sudo apt autoremove --purge -y
sudo apt autoclean

# 3. 清理 systemd 日志
sudo journalctl --vacuum-size=50M

# 4. 清理临时文件
sudo rm -rf /tmp/*
sudo rm -rf /var/tmp/*

# 5. 查看清理效果
df -h /
```

### 2.3 虚拟机磁盘扩容（如果清理后仍不够）

在 VMware/VirtualBox 中关闭虚拟机 → 设置 → 硬盘 → 扩展磁盘容量（如扩展到 30G）。

然后在 Ubuntu 中用 fdisk 扩展分区：

```bash
# 查看当前分区布局
lsblk
sudo fdisk -l
```

假设磁盘为 `/dev/sda`，分区布局如下：

```
设备       启动    起点     末尾     扇区  大小 Id 类型
/dev/sda1  *       2048  1050623  1048576  512M  b W95 FAT32
/dev/sda2       1052670 41940991 40888322 19.5G  5 扩展
/dev/sda5       1052672 41940991 40888320 19.5G 83 Linux
```

#### 步骤一：使用 fdisk 重新分区

```bash
sudo fdisk /dev/sda
```

按以下顺序输入命令：

```
d          # 删除分区
5          # 删除逻辑分区 sda5

d          # 删除分区
2          # 删除扩展分区 sda2

n          # 新建分区
e          # 选择扩展分区 (extended)
2          # 分区号 2
起始扇区   → 直接回车（使用默认值，和原来一样）
结束扇区   → 直接回车（使用磁盘最大空间，即 30G 全部用上）

n          # 新建分区
l          # 选择逻辑分区
起始扇区   → 直接回车
结束扇区   → 直接回车（用满整个扩展分区）

p          # 查看分区表，确认 sda2 和 sda5 都变大了

w          # 写入并退出
```

> **注意**：删除分区不会丢失数据，只要新建分区时起始扇区与原来一致即可。务必确认 `p` 打印的分区表大小正确后再 `w` 写入。

#### 步骤二：重启并扩展文件系统

```bash
# 重启使分区表生效
sudo reboot
```

重启后执行：

```bash
# 扩展文件系统到新分区大小
sudo resize2fs /dev/sda5

# 验证结果（应该看到容量变大了）
df -h /
```

---

## 第三步：在 Ubuntu 上安装 Docker

在 Ubuntu 虚拟机中执行以下命令：

```bash
# 1. 更新软件包
sudo apt update && sudo apt upgrade -y

# 2. 安装必要依赖
sudo apt install -y ca-certificates curl

# 3. 添加 Docker 官方 GPG 密钥
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# 4. 添加 Docker 仓库
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] \
  https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 5. 安装 Docker 和 Docker Compose 插件
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# 6. 将当前用户加入 docker 组（避免每次 sudo）
sudo usermod -aG docker $USER

# 7. 启动 Docker 并设置开机自启
sudo systemctl enable docker
sudo systemctl start docker

# 8. 重新登录或执行以下命令使 docker 组生效
newgrp docker

# 9. 验证安装
docker --version
docker compose version

docker compose version
Docker version 29.7.2, build a7dcaa6
Docker Compose version v5.5.0

```

> **注意**：如果你的 Ubuntu 版本较老（< 20.04），`docker compose`（V2 插件）可能不可用，可用 `docker-compose`（V1）替代：
> ```bash
> sudo apt install -y docker-compose
> # 后续命令中将 docker compose 替换为 docker-compose
> ```

---

## 第四步：配置环境变量

```bash
# 进入项目目录
cd ~/ims-main

# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件
nano .env
```

需要修改的关键配置（**强烈建议修改默认密码**）：

```ini
# 前端访问端口（浏览器打开 http://虚拟机IP:8080）
FRONTEND_PORT=8080
BACKEND_PORT=8000
MYSQL_PORT=3306

# MySQL 密码（必须修改，不要用默认值）
MYSQL_ROOT_PASSWORD=你的强密码
MYSQL_USER=ims
MYSQL_PASSWORD=你的数据库密码
MYSQL_DB=ims

# JWT 密钥（必须修改为长随机字符串，用于用户登录令牌加密）
JWT_SECRET_KEY=请修改为一个长随机字符串
JWT_EXPIRE_MINUTES=1440
LOG_LEVEL=INFO
CORS_ORIGINS=http://localhost:8080,http://127.0.0.1:8080

# 管理员账号（首次启动自动创建，已存在则跳过）
ADMIN_USERNAME=admin
ADMIN_PASSWORD=你的管理员密码
ADMIN_NICKNAME=管理员
```

---

## 第五步：启动服务

```bash
# 在 ims-main 目录下执行
docker compose up -d
```

首次启动会自动完成以下操作：

1. 拉取 `mysql:5.7`、`python:3.12-slim`、`node:20-alpine` 等基础镜像
2. 构建前端（npm ci + vite build）
3. 构建后端（uv sync + 安装 Python 依赖）
4. 启动 MySQL → 等待就绪 → 启动后端（自动执行数据库迁移 + 初始化管理员账号）→ 启动前端 Nginx

### 查看启动状态

```bash
# 实时查看所有日志
docker compose logs -f

# 查看服务运行状态
docker compose ps
```

正常启动后，`docker compose ps` 应该显示 3 个服务都是 `Up` 状态。

---

## 第六步：访问系统

### 1. 查看 Ubuntu 虚拟机 IP 地址

```bash
ip addr show | grep inet
```

通常显示类似 `192.168.x.x` 的地址。

### 2. 在 Windows 浏览器中打开

```
http://虚拟机IP:8080
```

### 3. 登录

使用 `.env` 中配置的管理员账号和密码登录。

---

## 常用管理命令

### 服务控制

```bash
# 停止所有服务
docker compose down

# 重启所有服务
docker compose restart

# 停止并删除所有数据（包括数据库数据，谨慎操作！）
docker compose down -v
```

### 日志查看

```bash
# 查看所有服务日志
docker compose logs -f

# 只看后端日志
docker compose logs -f backend

# 只看前端日志
docker compose logs -f frontend

# 只看数据库日志
docker compose logs -f mysql

# 查看最近 100 行日志
docker compose logs --tail=100 backend
```

### 代码更新后重新部署

```bash
# 重新构建并启动
docker compose up -d --build

# 或者只重建某个服务
docker compose up -d --build backend
docker compose up -d --build frontend
```

### 进入容器调试

```bash
# 进入后端容器
docker compose exec backend bash

# 进入 MySQL 容器
docker compose exec mysql mysql -u ims -p
```

---

## 故障排查

### 1. 端口被占用

```bash
# 检查端口占用情况
sudo ss -tlnp | grep -E '8080|8000|3306'

# 如果端口被占用，修改 .env 中的端口配置
nano .env
# 修改 FRONTEND_PORT、BACKEND_PORT、MYSQL_PORT
```

### 2. 无法访问 Web 页面

检查 Ubuntu 防火墙：

```bash
# 放行端口
sudo ufw allow 8080
sudo ufw allow 8000

# 或直接关闭防火墙（仅开发环境）
sudo ufw disable
```

确认虚拟机网络模式为**桥接模式**（Bridge），这样 Windows 才能直接访问。

### 3. 内存不足导致构建失败

前端构建（npm build）需要较多内存，建议给 Ubuntu 虚拟机分配至少 **4GB 内存**。

### 4. Docker 镜像拉取太慢

配置国内镜像加速器：

```bash
sudo mkdir -p /etc/docker
sudo tee /etc/docker/daemon.json <<-'EOF'
{
  "registry-mirrors": [
    "https://docker.m.daocloud.io",
    "https://dockerproxy.com"
  ]
}
EOF
sudo systemctl daemon-reload
sudo systemctl restart docker
```

### 5. MySQL 容器健康检查失败

```bash
# 查看 MySQL 日志
docker compose logs mysql

# 常见原因：端口冲突、数据目录权限问题
# 清除旧数据重新启动
docker compose down -v
docker compose up -d
```

### 6. 数据库迁移失败

```bash
# 查看后端日志
docker compose logs backend

# 手动进入后端执行迁移
docker compose exec backend bash
uv run alembic upgrade head
```

---

## 数据备份

### 备份 MySQL 数据库

```bash
# 导出数据库
docker compose exec mysql mysqldump -u ims -p ims > ims_backup_$(date +%Y%m%d).sql

# 恢复数据库
docker compose exec -T mysql mysql -u ims -p ims < ims_backup_20260101.sql
```

### 备份上传文件

```bash
# 上传文件存储在 docker volume 中
docker compose cp backend:/app/uploads ./uploads_backup
```

---

## 虚拟机配置建议

| 配置项 | 最低要求 | 推荐配置 |
|--------|---------|---------|
| CPU | 2 核 | 4 核 |
| 内存 | 4 GB | 8 GB |
| 磁盘 | 30 GB | 50 GB |
| 网络 | 桥接模式 | 桥接模式 |
| 系统 | Ubuntu 20.04 | Ubuntu 22.04/24.04 |
