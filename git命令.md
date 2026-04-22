[[_杂项]]
## `.gitignore`的使用：
```.gitignore
# 忽略特定文件
.history
# 忽略整个目录
/.history/
# 忽略根目录下特定文件
/.history
```

## `github`查询
```powershell
# 查看状态
git status
# 查看当前分支
git branch
# 查看远程分支
git branch -r
# 查看所有分支
git branch -a
# 查看提交历史
git log --online
```

## `github`使用
```powershell
# 好习惯先pull
git pull origin master --rebase
# 添加所有文件到暂存区
git add .
# 提交到本地仓库
git commit -m "从夯到拉评价一下你的提交"
# 推送到远程
git push origin master
```