
# STV 路径转换器 🌐

一款智能多功能的命令行工具，支持在 Windows 和 Linux 路径格式之间灵活转换，提供样式定制和高级格式化选项。

[Endlish](./README_EN.md)

---

## 功能亮点 ✨

- **自动方向检测**：智能识别输入路径格式（Windows ↔ Linux）。
- **多样式支持**：支持 WSL、Cygwin 和 POSIX 路径规范。
- **环境变量处理**：可选展开或保留环境变量（`%VAR%` ↔ `$VAR`）。
- **自定义挂载前缀**：定义个性化挂载点（如 `/my-mount/`）。
- **格式控制**：
   - 引号处理策略（`always`/`auto`/`never`）
   - 尾部斜杠管理
   - 大小写转换（强制小写/大写）
- **路径验证**：检查 Windows 路径的非法字符。
- **批量处理**：支持从文件或标准输入读取路径。

---

## 安装指南 📦

### 通过 pip 安装
```bash
pip install stv_path_converter
```

### 从源码构建
1. 克隆仓库：
   ```bash
   git clone https://github.com/StarWindv/win-linux-path_converter
   ```
2. 使用 Poetry 安装：
   ```bash
   cd win-linux-path_converter
   pip install .
   ```

---

## 使用示例 🛠️

### 基础转换
```bash
stv_path "C:\Program Files"
# 输出：/mnt/c/Program\ Files

stv_path "/my_mount/c/user/docs" -m my_mount
# 输出：C:\home\user\docs
```

### 高级选项速查表
| 选项                  | 说明                                      |
|-----------------------|-------------------------------------------|
| `-d, --direction`     | 转换方向：`auto`（默认）、`win-to-linux`、`linux-to-win` |
| `-s, --style`         | 转换样式：`wsl`、`cygwin`、`posix`（默认：`wsl`） |
| `-m, --mount-prefix`  | 自定义挂载前缀（如 `/my-mount/`）         |
| `-q, --quote`         | 引号处理策略（`auto`/`always`/`never`）   |
| `-t, --trailing-slash`| 尾部斜杠处理（`keep`/`always`/`never`）   |
| `--lower/--upper`     | 强制输出小写/大写                         |
| `-e, --expand-env`    | 展开环境变量                              |
| `--validate`          | 验证 Windows 路径合法性                  |

### 场景示例
1. 将 Windows UNC 路径转为 WSL 格式：
   ```bash
   stv_path "\\server\share\file.txt" --style wsl
   # 输出：/mnt/server/share/file.txt
   ```

2. 将 Cygwin 路径转为带引号的 Windows 路径：
   ```bash
   stv_path -d linux-to-win "/cygdrive/d/My Documents" --quote always
   # 输出："D:\My Documents"
   ```

3. 从文件批量转换路径：
   ```bash
   stv_path -i paths.txt
   ```

---

## 项目结构 🌳

```
.
├── LICENSE
├── README.md
├── pyproject.toml
└── src
    └── stv_path_converter
        ├── __init__.py
        ├── core
        │   ├── __init__.py
        │   ├── converter.py    # 核心转换逻辑
        │   └── stv_parse.py    # 路径解析工具
        ├── main.py             # CLI 入口
        ├── text
        │   ├── __init__.py
        │   └── change_text.py  # 文本格式化辅助
        └── utils
            ├── __init__.py
            ├── head.py         # 头部工具
            └── lic.py          # 许可证管理
```

---

## 贡献指南 🤝

欢迎贡献代码！欢迎随时提交issue和pr！

---

## 开源协议 📜

本项目采用 MIT 许可证，详见 [LICENSE](./LICENSE)。

---

<sub>🛠️ 为跨平台开发者精心打造。</sub>


### 版本亮点
- **本地化优化**：专为中文用户设计的技术术语表达
- **格式适配**：符合中文标点与排版习惯
- **场景化示例**：贴近实际开发需求的操作演示
- **结构清晰**：与英文版保持一致的层级逻辑
