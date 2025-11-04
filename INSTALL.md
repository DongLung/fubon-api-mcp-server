# 安裝指南 - Installation Guide

## 安裝 fubon-api-mcp-server

### 方法 1: 從 PyPI 安裝 (推薦)

```bash
pip install fubon-api-mcp-server
```

**注意**: 由於 `fubon_neo` 是富邦證券的私有套件，PyPI 版本可能無法直接安裝所有依賴。

### 方法 2: 從原始碼安裝 (包含私有套件)

```bash
# 1. Clone 專案
git clone https://github.com/Mofesto/fubon-api-mcp-server.git
cd fubon-api-mcp-server

# 2. 創建虛擬環境
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate

# 3. 安裝依賴 (包含本地 wheel)
pip install -r requirements.txt

# 4. 安裝專案
pip install -e .
```

## fubon_neo 套件說明

### 什麼是 fubon_neo？

`fubon_neo` 是富邦證券提供的 Python SDK，用於存取富邦證券交易 API。

### 為什麼包含在專案中？

- **私有套件**: fubon_neo 不在 PyPI 上公開發布
- **CI/CD 需求**: GitHub Actions 需要能夠安裝此套件
- **便利性**: 使用者無需額外下載

### Wheel 文件位置

```
wheels/
└── fubon_neo-2.2.5-cp37-abi3-win_amd64.whl
```

### 支援的平台

- **Python**: 3.7+ (abi3 兼容)
- **作業系統**: Windows AMD64
- **版本**: 2.2.5

### Linux/macOS 使用者

如果你在 Linux 或 macOS 上使用，需要從富邦證券官方下載對應平台的 wheel：

1. 訪問富邦證券 Trade API: https://www.fbs.com.tw/TradeAPI/docs/
2. 下載對應平台的 `fubon_neo` wheel
3. 安裝: `pip install /path/to/fubon_neo-xxx.whl`

## 開發者安裝

### 開發依賴

```bash
# 安裝完整的開發依賴
pip install -e ".[dev]"
```

包含的開發工具：
- pytest, pytest-cov, pytest-xdist, pytest-mock (測試)
- black, isort, flake8 (代碼格式化和檢查)
- mypy (型別檢查)
- bandit, safety (安全檢查)

### 文檔依賴

```bash
pip install -e ".[docs]"
```

## 疑難排解

### 問題: 找不到 fubon_neo

**解決方案 1**: 確認使用本地 wheel
```bash
pip install ./wheels/fubon_neo-2.2.5-cp37-abi3-win_amd64.whl
```

**解決方案 2**: 檢查平台相容性
```bash
# 檢查當前平台
python -c "import platform; print(platform.platform())"

# 如果不是 Windows，需要下載對應平台的 wheel
```

### 問題: Wheel 不相容

如果遇到 wheel 不相容錯誤：

```bash
# 強制安裝 (謹慎使用)
pip install --force-reinstall ./wheels/fubon_neo-2.2.5-cp37-abi3-win_amd64.whl
```

### 問題: CI/CD 失敗

GitHub Actions 會自動使用 wheels 目錄中的 wheel。如果失敗：

1. 確認 wheels 目錄已提交到 Git
2. 確認 requirements.txt 指向正確的 wheel 路徑
3. 檢查 GitHub Actions logs

## 授權和使用條款

**重要**: fubon_neo 是富邦證券的專有軟體

- ✅ **允許**: 已授權的富邦證券客戶使用
- ❌ **禁止**: 未經授權的分發和商業使用
- 📜 **授權**: 請參考富邦證券的使用條款

使用本軟體即表示您同意遵守富邦證券的服務條款。

## 更新 fubon_neo

當富邦證券發布新版本時：

```bash
# 1. 下載新版本的 wheel
# 2. 替換 wheels 目錄中的舊文件
# 3. 更新 requirements.txt 中的檔案名稱
# 4. 提交變更

git add wheels/ requirements.txt
git commit -m "chore: update fubon_neo to version X.X.X"
git push
```

## 取得協助

- **專案問題**: https://github.com/Mofesto/fubon-api-mcp-server/issues
- **富邦 API**: https://www.fbs.com.tw/TradeAPI/docs/
- **文檔**: https://github.com/Mofesto/fubon-api-mcp-server#readme

---

**最後更新**: 2025-11-04  
**fubon_neo 版本**: 2.2.5
