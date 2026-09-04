# Git 提交 Skill

## 触发条件
当用户说 **"提交"**、**"git"**、**"push"**、**"上传"** 或 **"推送到仓库"** 时，自动执行以下操作。

## 仓库信息
- **仓库地址**: `https://github.com/zjf258147/sheepfold`
- **远程名称**: `origin`
- **分支**: `main` 或 `master`（自动检测）

## 执行流程

### 1. 检查 git 状态
```bash
& "C:\Program Files\Git\bin\git.exe" status
```

### 2. 自动生成 commit message
根据修改内容，自动生成中文 commit message，格式：
```
YYYY-MM-DD: 简要描述修改内容
```

### 3. 添加所有文件
```bash
& "C:\Program Files\Git\bin\git.exe" add -A
```

### 4. 提交
```bash
& "C:\Program Files\Git\bin\git.exe" commit -m "commit message"
```

### 5. 推送
```bash
& "C:\Program Files\Git\bin\git.exe" push origin main
```

## 注意事项
- 如果仓库尚未初始化，先执行 `git init` 并关联远程仓库
- 每次提交前先显示将要提交的文件列表，让用户确认
- 推送前显示 commit 内容摘要