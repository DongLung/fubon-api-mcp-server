# GitHub 發佈指南

本指南將幫助您將富邦 MCP 伺服器專案發佈到 GitHub。

## 📋 前置準備

### 1. 創建 GitHub 帳戶
如果您還沒有 GitHub 帳戶，請前往 [github.com](https://github.com) 註冊。

### 2. 創建新的倉庫
1. 登入 GitHub
2. 點擊右上角的 "+" 按鈕，選擇 "New repository"
3. 設定倉庫資訊：
   - **Repository name**: `fubon-api-mcp-server` (建議)
   - **Description**: 富邦證券市場資料 MCP (Model Communication Protocol) 伺服器
   - **Visibility**: Public (公開) 或 Private (私有)
4. **不要** 初始化 README、.gitignore 或 License（因為專案中已有）
5. 點擊 "Create repository"

### 3. 配置 Git（如果尚未配置）
```bash
# 設定您的 Git 用戶資訊
git config --global user.name "您的名字"
git config --global user.email "您的email@example.com"
```

### 4. 配置 SSH 金鑰或個人存取權杖
選擇以下任一種方式進行身份驗證：

#### 方式一：SSH 金鑰（推薦）
```bash
# 檢查是否已有 SSH 金鑰
ls -la ~/.ssh/

# 如果沒有，生成新的 SSH 金鑰
ssh-keygen -t ed25519 -C "您的email@example.com"

# 複製公鑰並添加到 GitHub
cat ~/.ssh/id_ed25519.pub
# 將輸出內容添加到 GitHub Settings > SSH and GPG keys
```

#### 方式二：個人存取權杖
1. 前往 GitHub Settings > Developer settings > Personal access tokens
2. 生成新的 token，選擇 `repo` 權限
3. 複製 token，在推送時使用作為密碼

## 🚀 發佈步驟

### 方法一：使用 PowerShell 腳本（推薦，適用 Windows）

```powershell
# 進入專案目錄
cd D:\FubonMcpServer

# 運行發佈腳本
.\publish_to_github.ps1 -GitHubUsername "Mofesto" -RepositoryName "fubon-api-mcp-server"
```

### 方法二：手動執行

```bash
# 進入專案目錄
cd D:\FubonMcpServer

# 添加遠端倉庫
git remote add origin https://github.com/Mofesto/fubon-api-mcp-server.git

# 推送代碼
git push -u origin main
```

## 🔧 故障排除

### 常見問題

#### 1. "Permission denied" 錯誤
```
解決方案：
- 確保 SSH 金鑰已正確添加到 GitHub
- 或使用個人存取權杖作為密碼
- 確認您對倉庫有推送權限
```

#### 2. "Repository not found" 錯誤
```
解決方案：
- 確認倉庫名稱正確
- 確認倉庫已創建
- 檢查用戶名拼寫
```

#### 3. "Branch 'main' doesn't exist" 錯誤
```
解決方案：
- 確保本地分支名稱是 'main'
- 如果是 'master'，請重新命名：git branch -m master main
```

### 驗證發佈成功

發佈完成後，您可以：
1. 訪問 `https://github.com/Mofesto/fubon-api-mcp-server`
2. 確認所有文件都已上傳
3. 查看 README.md 是否正確顯示

## 📦 進一步發佈

### 發佈到 PyPI
如果您想將包發佈到 PyPI：

```bash
# 安裝發佈工具
pip install twine

# 建立發佈包
python setup.py sdist bdist_wheel

# 發佈到 PyPI（需要帳戶）
twine upload dist/*
```

### 設定 GitHub Actions
考慮添加 CI/CD 工作流程來自動化測試和發佈。

## 🎯 專案資訊

- **專案名稱**: 富邦證券 MCP 伺服器
- **版本**: 1.8.4
- **描述**: 提供完整的台股交易功能與市場數據查詢
- **PyPI Package**: fubon-api-mcp-server
- **VS Code Extension ID**: mofesto.fubon-api-mcp-server
- **授權**: MIT License

## 📞 支援

如果在發佈過程中遇到問題，請檢查：
1. GitHub 狀態頁面
2. 您的網路連接
3. SSH 金鑰或權杖配置
4. 倉庫權限設定