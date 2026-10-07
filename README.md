# 电科商城 H5 用户端完整测试实战

> 个人测试作品项目：在无需求文档、无源码、无后台权限的条件下，对企业内部福利商城 H5 完成黑盒测试闭环。

## 📌 项目简介

- **被测对象**：电科商城 H5（`https://app.cetconline.com/mallapp/`）
- **测试类型**：功能测试 / 兼容性测试 / 接口测试 / UI 自动化测试 / AI 辅助测试
- **测试周期**：约 3 周（个人独立完成）
- **测试环境**：Windows + Chrome 154 / 微信内置浏览器 / Safari (iOS)

## 🛠 技术栈

| 类型 | 工具 |
|---|---|
| 接口抓包 | Charles、Chrome DevTools |
| 接口测试 | Postman |
| UI 自动化 | Python 3.11 + Selenium 4 + pytest + Allure |
| 移动端模拟 | Chrome mobile emulation（iPhone 12 Pro） |
| 登录态方案 | Cookie 注入（绕开图形 + 短信验证码） |
| 用例管理 | Excel / 飞书表格 |
| AI 辅助 | LLM 生成用例、分析缺陷、草拟脚本 |

## 📊 测试成果

| 维度 | 数量 | 通过率 |
|---|---|---|
| 功能测试用例 | **82 条**（登录 18 / 首页 10 / 搜索 10 / 详情 10 / 购物车 12 / 结算 12 / 订单 10） | 执行率 100% |
| 兼容性矩阵 | 3 浏览器 × 3 分辨率 = 9 组 | 8/9 通过，1 个 Safari 样式小问题 |
| 接口测试断言 | 4 个只读接口 × 6 条断言 = **24 条** | **24/24 通过**，平均响应 491ms |
| UI 自动化用例 | **6 条**（登录态 / 首页 / 关键词 / 搜索框 / 搜索流程 / 购物车） | **4 passed, 2 skipped**，127s |
| 提交缺陷 | 约 18 个（P1~P3） | 已跟踪回归 |

## 📁 项目结构

```
h5_mall_test/
├── config.py                 # 本地配置（含 cookie，已 gitignore）
├── config.example.py        # 配置模板（公开）
├── conftest.py              # pytest fixture：driver 初始化、cookie 注入、失败截图
├── testcases/
│   └── test_login.py         # 6 条 UI 自动化用例
├── pages/                    # 页面对象（POM，可扩展）
├── screenshots/              # 运行时自动截图
├── reports/                  # 测试报告、Allure 产物
├── docs/
│   ├── 最终测试报告.md        # 完整测试报告
│   ├── 接口测试操作手册.md    # Charles + Postman 操作手册
│   └── 电科商城H5测试用例集.xlsx
└── .gitignore
```

## 🚀 如何运行

### 1. 环境准备

```powershell
# 推荐 Python 3.11
pip install selenium pytest allure-pytest
# 下载与本机 Chrome 匹配的 chromedriver，放到项目根目录
```

### 2. 配置 cookie

```powershell
copy config.example.py config.py
# 编辑 config.py，填入你手动登录后从 F12 拿到的 cookie
```

### 3. 跑 UI 自动化

```powershell
# 普通运行
python -m pytest testcases/ -v -s

# 带 Allure 数据收集
python -m pytest testcases/ -v -s --alluredir=reports/allure-results

# 生成 HTML 报告
allure generate reports/allure-results -o reports/allure-report --clean
allure open reports/allure-report
```

## 🔍 关键技术点

### 1. Cookie 注入绕开验证码
H5 登录需要图形验证码 + 短信验证码，无法自动化。方案：手动登录一次，从 F12 复制 cookie，Selenium `add_cookie` 注入到新会话，服务端即认登录态。

### 2. 黑盒下接口测试的边界
- 只重放**只读接口**（列表、详情），不重放写接口（加购、下单），避免污染生产数据；
- 接口响应体为 hex 加密，只能校验外层结构（状态码、业务 status、result 字段），无法断言业务字段值——此限制已在报告中诚实披露。

### 3. 主动 skip 而非硬凑通过率
- 搜索用例：首页搜索框是"假 div"，点击跳转 `/commoditySearch`，真正 input 在新页面；直接对隐藏 input 发 `send_keys` 无效，已记录为后续优化项；
- 购物车用例：依赖 JS 侧 localStorage token，HTTP cookie 注入覆盖不到，黑盒下主动 skip 并记录风险。

## 📸 截图证据

- `reports/UI自动化测试结果.png`：PowerShell 终端输出（4 passed, 2 skipped）
- `reports/Allure总览.png`：Allure Dashboard 饼图
- `reports/Allure用例详情.png`：单条用例执行详情
- `screenshots/`：运行时自动截图（首页、搜索、购物车）

## ⚠️ 已知限制

1. 接口响应体加密，无法直接断言业务字段值；
2. 购物车、下单流程的 UI 自动化覆盖不全（依赖 JS 登录态）；
3. 无需求文档，用例基于探索式测试反推；
4. 项目为个人实践，非团队项目。

## 📚 学到了什么

- 完整测试生命周期：需求反推 → 用例设计 → 功能/兼容/接口/自动化执行 → 缺陷管理 → 测试报告；
- 黑盒条件下的测试策略取舍：什么能自动化、什么该 skip、什么要手动；
- Selenium 实战坑：chromedriver 版本匹配、Cookie domain 不匹配、mobile emulation、显式等待；
- 用 LLM 提效：用例草拟、缺陷描述、脚本初稿，但输出必须人工校验。
