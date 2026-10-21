# DRUI — 快捷命令与 Workflow 清单（持续更新）

`drui` 是主流程 Skill，包含 20 个工作流；独立的 `oil-ui-plus` 是我们原创、内置的近似 Pro UI 方法 Skill（**非官方 Pro**）。按 `oil-ui-pro`（实际安装时）> `oil-ui-plus` > `oil-ui` > DRUI 兜底自动选择。


## Oil UI Plus 与调用顺序

UI 方法统一优先级（不代表顺序执行四次）：**`oil-ui-pro`（官方、实际已安装） > `oil-ui-plus`（GameAgentKit 原创内置） > `oil-ui`（已安装开源版） > DRUI 其他内置通用流程**。DRUI 永远负责 workflow 编排、三方独立审查及验收。详见 [UI_SOURCE_ROUTING.md](UI_SOURCE_ROUTING.md)。

```bash
# 查看当前可访问的 UI 方法及自动选择结果（只检测文件，不等于成功调用）
drui sources

# 自动优先：官方 Pro 真实安装时优先，否则使用 Oil UI Plus
drui prompt review-loop

# 明确使用我们自己的 Plus（忽略官方 Pro）
drui prompt review-loop --ui-source plus
drui plus      # full + Plus 的快捷入口

# 明确使用官方 Pro：未安装会报错，不会暗中换成 Plus
drui prompt full --ui-source pro

# 查看单个 Agent 可以发现的来源
drui sources --agent claude
```

在 Agent 对话中：`drui review-loop --ui-source plus`、`drui full`、`drui sources`。终端 `drui` 只打印提示词；**不会在命令行直接运行设计和审查**。

## 新用户从这里开始

```bash
drui start                     # 1 分钟上手，无自动安装或执行
drui help                      # 按目标推荐合适的工作流
drui help commands             # 完整命令速查
drui list --beginner           # 6 个常用工作流
drui list --category ui        # 核心 core / 界面 ui / 专项 specialty / 独立评审 review
drui list --search 操作         # 按中文、英文、应用场景搜索
drui help usability-review     # 何时使用、预期交付、权限、可复制的示例
drui prompt usability-review   # 生成 Agent Prompt，不执行
```

如果不知道选哪一个：**玩家不知道怎么操作** → `usability-review`（只读）；**美术质量不够** → `visual-review`（只读）；**需要 TL/PM/用户分别评审** → `review-triad`（只读）；**希望评审后直接修复并回归** → `review-loop`（可修改）；**全流程优化** → `full`（可修改）。终端命令不能自动运行 Agent。

## 在 Agent 对话里使用（Codex / Claude Code / Antigravity 等）

| 你输入 | Agent 应执行的行为 |
| --- | --- |
| `drui list` | 输出以下 20 个工作流的名字与用途，不修改项目 |
| `drui help review-tl` | 解释 Tech Lead 审查范围、只读规则和交付物 |
| `drui visual-review` | 针对当前项目开展视觉独立审查（不修改代码） |
| `drui review-tl` | 执行 Tech Lead 独立技术审查（不修改代码） |
| `drui review-pm` | 执行 PM 独立评审（不修改代码） |
| `drui review-user` | 尝试执行真实用户任务并提交证据（不修改代码） |
| `drui review-triad` | 创建三个彼此隔离的评审任务；不具备隔离能力则标记 PROVISIONAL |
| `drui review-loop` | 独立评审 → 修复 → 实际验证 → 复审，最多三轮 |
| `drui prompt review-loop` | 只输出可复制的完整 Prompt，不执行任务 |

在不同 Agent 中，自动 Skill 发现并非绝对可靠；若输入 `drui list` 未触发，请使用 **“Use the drui skill and list its workflows”**。不能从同一会话假冒三名独立 reviewer。

## 安装与验收（GitHub 源码）

请先阅读 **[INSTALL_AND_VERIFY.md](INSTALL_AND_VERIFY.md)**，其中包括用户自行执行的 Git clone / install、Agent 安装 Prompt、短验证、失败返回码和排错。

```bash
bash "$HOME/GameAgentKit/install.sh" --agents codex,claude,antigravity,cursor --dry-run
bash "$HOME/GameAgentKit/install.sh" --agents codex,claude,antigravity,cursor
"$HOME/GameAgentKit/scripts/drui" verify             # 短摘要，验收必须返回 0
"$HOME/GameAgentKit/scripts/drui" verify --verbose   # 每个 Skill/版本/路径
"$HOME/GameAgentKit/scripts/drui" verify --json      # 机器可读
```

完整四 Agent 共 5 个安装目录 × 12 个内置 Skills = **60** 项。安装器因保护用户同名 Skill 可能跳过链接而返回 0，务必再运行 verify。仅通过文件检查不意味着 Agent 已真正读取。旧别名 `--agents all` 不含 Cursor。

## 在 Mac 终端里使用（命令不会自动启动 Agent）

```bash
# 如升级后需要补齐链接，可使用（不会覆盖已有同名命令）
python3 ~/GameAgentKit/gamekit.py link --agents codex,claude,antigravity,cursor

# 只列清单 / 查看具体说明 / 生成执行 Prompt
drui list
drui help review-tl
drui prompt review-loop

# 指定项目生成 Prompt
drui prompt review-loop --project "$PWD"

# 可机器读取的 JSON 清单
drui list --json
```

安装器默认创建 `~/.local/bin/drui` 的安全软链接，**不会改动** `~/.zshrc` 或覆盖已有同名命令。若提示 `command not found`，先使用绝对路径：

```bash
python3 ~/GameAgentKit/scripts/drui list
```

如需在任何终端直接输入 `drui`，把以下这一行手动加入你的 `~/.zshrc`，然后重新打开终端（或 `source ~/.zshrc`）：

```bash
export PATH="$HOME/.local/bin:$PATH"
```

## 全部工作流（20 个，均可单独选择）

### Ⅰ. 核心开发与管理（6）

| Workflow | 说明 | 默认权限 |
| --- | --- | --- |
| `full` | 从现状诊断到实现、审查、修复、验证的完整循环 | 可改代码 |
| `discover` | 诊断用户路径与功能问题，建立问题清单 | 只审查 |
| `plan` | 设计方向比较、UI Refresh / Flow Fix / New Feature 决策 | 只审查 |
| `implement` | 基于批准的方案实现真实界面/交互 | 可改代码 |
| `fix` | 根据审查报告修复已知问题 | 可改代码 |
| `verify` | 真实运行、回归测试与最终验收报告 | 只审查 |

### Ⅱ. UI 与游戏体验（5）

| Workflow | 说明 | 默认权限 |
| --- | --- | --- |
| `visual-review` | 信息层级、排版、配色、美术一致性与 AI 模板感 | 只审查 |
| `usability-review` | 操作链、触控、引导、错误/空白状态、可访问性 | 只审查 |
| `game-feel` | 动画节奏、输入响应、手感、声音与反馈 | 依请求 |
| `screenshot-rebuild` | 将参考截图还原成真实可交互界面 | 可改代码 |
| `component-polish` | 深度精修指定组件与所有交互状态 | 可改代码 |

### Ⅲ. 专项设计（4）

| Workflow | 说明 | 默认权限 |
| --- | --- | --- |
| `mini-game-scene` | 游戏场景布局、HUD、操作区、状态/反馈专项 | 依请求 |
| `effects` | 光轨、渐变、视差、转场与微交互 | 依请求 |
| `dashboard` | 家长面板、报表、数据工具页的风格和功能 | 依请求 |
| `art-3d` | Melo 等角色一致性、3D/2.5D 资产与渲染验收 | 依请求 |

### Ⅳ. 严苛三方独立评审（5）

| Workflow | 说明 | 默认权限 |
| --- | --- | --- |
| `review-tl` | Tech Lead：架构、代码、状态、性能、风险、测试证据 | 只审查 |
| `review-pm` | PM：用户价值、玩法循环、范围、留存、验收标准 | 只审查 |
| `review-user` | 用户：无提示完成真实任务，复现卡点、检查易用性 | 只审查 |
| `review-triad` | 三方隔离评审、对比与分歧仲裁，不修复 | 只审查 |
| `review-loop` | 三方评审 → P0/P1 修复 → 新证据 → 再审查 | 可改代码 |

**严格验收：** 未运行目标平台则标记 `BLOCKED / NOT RUN`；三个评审不能共用同一审查上下文冒充独立评审；任何未解决 P0/P1 均不能发布放行。评分只能来自有证据的报告，不能靠自评凑到 9/10。

## 老命令依旧有效

```bash
python3 ~/GameAgentKit/gamekit.py workflow list
python3 ~/GameAgentKit/gamekit.py workflow list --json
python3 ~/GameAgentKit/gamekit.py workflow prompt --stage visual-review
```

更多资料：`skills/drui/SKILL.md`、`docs/DRUI_STRICT_REVIEW_PROTOCOL.md`、`docs/DRUI_REVIEW_CHEATSHEET_ZH.md`。

## 让 Agent 安装或更新 DRUI（复制 Prompt）

第一次使用无需安装 drui 命令：到 [官方 README](https://github.com/zhenv5/drui#install-via-agent)，从“首次安装”或“升级现有 DRUI”代码块点击复制，粘贴到支持终端的 Agent 会话。

已安装的用户：

```bash
drui agent install          # 显示可粘贴给 Agent 的安装指令
drui agent update           # 显示更新指令
drui copy install           # 复制到系统剪贴板
drui copy update            # 复制更新 Prompt（不执行更新）
drui agent update --copy    # 同上
```

本功能**只复制文本**，不执行 Agent、不联网、不操作用户文件或第三方 Skills。未检测到 pbcopy、wl-copy、xclip、xsel 时会输出可手动复制的内容，返回非零码；不得声称已复制。
