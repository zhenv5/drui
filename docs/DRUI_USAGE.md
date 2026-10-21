当前公开版本请看仓库 `VERSION` 和 [Release](https://github.com/zhenv5/drui/releases/latest)。在 Agent 对话中可请求 `drui list`；终端 `drui list`/`help`/`prompt` 只输出文本，不自动执行 Agent。详见 [命令手册](DRUI_COMMANDS_ZH.md) 和 [安装验证](INSTALL_AND_VERIFY.md)。

# DRUI — user manual / 使用说明

## 名称及区别

- 外部 `oil-ui` 为你原本安装的开源 Skill；本包另内置独立的 `oil-ui-plus`（原创 Pro 类工作流），官方付费 `oil-ui-pro` 只在合法安装并可访问时优先使用。
- GameAgentKit 提供的原创通用 Skill：**`drui`**，一次全局安装、多个 Agent/项目共用；包含 20 个可独立触发的流程。
- 工具包：`GameAgentKit`。它还包括 `game-ui-design`、`game-qa-review`、`game-feel-polish` 等。
- 这是独立的原创流程工具，**不是 Oil UI Pro**，不声称解锁付费版真实能力。

## 触发方式

Agent 对自然语言是否自动匹配 Skill 的策略不同。最稳妥的跨 Agent 调用：

```text
Use the drui skill for the open project.
Stage: visual-review
Scope: Home screen only.
Read-only review. Capture/inspect a real simulator screenshot; report issues.
Do not edit project files.
```

部分 Agent 可识别 `/drui` 等斜杠命令，但**不是跨平台保证的命令**。Codex、Claude Code、Antigravity 均优先使用明确的 Skill 名称和阶段名称。更需要自动发现时，在项目 `AGENTS.md` / `CLAUDE.md` 写入说明；GameAgentKit `attach` 只会在没有现有规则时创建入口，不覆盖用户规则。

## 20 个工作流入口：原 15 个 + 5 个独立评审工作流

| stage 标识 | 中文作用 | 默认模式 | 示例自然语言 |
|---|---|---|---|
| `full` | 全流程：诊断→方案→实现→审查→修复→验收 | 完整流程 | `Use drui stage full on this game` |
| `discover` | 现状审查、问题分类、需求澄清 | 只读 | `stage discover; report only` |
| `plan` | 多方向视觉方案与实施计划 | 只读 | `stage plan; propose 3 distinct directions` |
| `implement` | 实际 UI / UX 开发 | 修改代码 | `stage implement; implement approved design` |
| `visual-review` | 字体、层级、配色、美术、对齐 | 只读 | `stage visual-review; assess screenshots` |
| `usability-review` | 真正完成核心用户任务、交互状态 | 只读 | `stage usability-review; test touch controls` |
| `game-feel` | 动画、音效、输入即时反馈、节奏 | 默认审查 | `stage game-feel; review input feedback only` |
| `fix` | 按 P0/P1/P2 清单修复 | 修改代码 | `stage fix; address previous P0 issues` |
| `verify` | 构建运行、真机/模拟器截图、独立评分 | 只读验收 | `stage verify; rerun all core tasks` |
| `screenshot-rebuild` | 按参考截图重建**可交互**页面 | 修改代码 | `stage screenshot-rebuild; preserve behavior` |
| `component-polish` | 单按钮/卡片/控件多状态精修 | 修改代码 | `stage component-polish; improve pause button only` |
| `mini-game-scene` | 游戏场景/HUD/触控和状态矩阵 | 默认审查 | `stage mini-game-scene; scene QA only` |
| `effects` | 光轨、点阵、渐变和动效 | 默认审查 | `stage effects; audit reduced motion` |
| `dashboard` | 工具 / 数据面板信息结构 | 默认审查 | `stage dashboard; review data states` |
| `art-3d` | 美术资产、角色一致性及 3D 管线 | 默认审查 | `stage art-3d; inspect asset quality` |

**单独运行**表示每次只执行选定阶段；单独跑 `visual-review` 不会自行修代码，`fix` 需已有待修问题，`verify` 需可运行环境和测试依据。某些阶段需要先提供当前截图、项目位置、设计参考或上一轮 Issue，但这不意味着必须按整个全流程重新跑一遍。

## 命令行选择提示词（支持复制给任意 Agent）

```bash
python3 ~/GameAgentKit/gamekit.py workflow list
python3 ~/GameAgentKit/gamekit.py workflow prompt --stage visual-review
python3 ~/GameAgentKit/gamekit.py workflow prompt --stage component-polish --project ~/Projects/YourGame
python3 ~/GameAgentKit/gamekit.py workflow prompt --stage full --output ~/Downloads/full-review.md
```

CLI 负责输出文本**不会替你调用其他 Agent、运行 Xcode、执行测试、推送到 GitHub**。选阶段后将文本粘贴到 Codex / Claude Code / Antigravity / Cursor 等有相应项目访问权限的 Agent。这解决了不同平台 Skill 调用格式不一致的问题。


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

## 核心能力与能力边界

- 设计方向：可出 2–3 个明确不同的方案，也可以仅修复原 UI，无须每次重做风格。
- 功能状态：页面正常、加载、空数据、错误、完成、暂停、恢复、禁用、动态文本、不同屏幕。
- 视觉质量：排版、颜色、留白、信息重点、减少机械化 AI 设计、针对参考截图做严格对比。
- 手感和小游戏：交互可发现性、触控、反馈时序、动画、可选特效、可读 HUD、帧率。
- 独立审查：七项评分 + 真实截图 + 用户任务步骤；最多三轮有价值的修复循环，**9/10 是目标而非保证**。
- 特殊模式：截图重建、单组件精修、19 种原创卡片模式及 SwiftUI 示例、数据面板、资产 3D 审查。
- 真机/模拟器需要系统工具、正确平台及可运行代码；无法运行时如实标记 `BLOCKED` / `NOT RUN`，不能声称 9/10。
- 包内原创提示词不含 Oil UI Pro 专有代码/模板或授权。

## 当前安装、更新与验证（仅 GitHub 源码）

统一操作规范见 **[INSTALL_AND_VERIFY.md](INSTALL_AND_VERIFY.md)**：涵盖命令行直接安装、Agent 一键复制 Prompt、GitHub Tag 更新、短摘要、退出码和排错。

```bash
git clone --depth 1 --branch v1.4.4 https://github.com/zhenv5/drui.git "$HOME/GameAgentKit"
bash "$HOME/GameAgentKit/install.sh" --agents codex,claude,antigravity,cursor --dry-run
bash "$HOME/GameAgentKit/install.sh" --agents codex,claude,antigravity,cursor
"$HOME/GameAgentKit/scripts/drui" verify          # 一行摘要；必须检查退出码
"$HOME/GameAgentKit/scripts/drui" verify --verbose # 全部状态、版本和路径
"$HOME/GameAgentKit/scripts/drui" verify --json    # 机器可读
```

DRUI 保留已有同名用户 Skills，因此从 v1.4.4 起安装/链接命令会根据内置 verify 的结果返回非零码，**仍建议最终单独运行 verify 验收**；默认四个 Agent 跨五个目录共 60 个链接，`--agents all` 也包括 Cursor。验证本地链接并不代表 Agent 已实际加载。

## 严苛三方独立评审

直接调用：`Use drui, stage review-tl / review-pm / review-user / review-triad / review-loop`。

- `review-tl`：技术负责人角度，审查架构、正确性、性能、可维护性、集成风险，**只评审不改代码**。
- `review-pm`：PM 角度，价值、首用引导、功能流程、范围控制、留存及验收标准，**只评审**。
- `review-user`：用户角度，真实启动、点按、完成任务、犯错后恢复与交互反馈，**只评审**；模拟儿童体验不得冒充实际儿童调研。
- `review-triad`：分离三份任务，要求互不提前读取他方评分和结论，汇总冲突、阻塞事项与优先级，**只评审**。
- `review-loop`：先独立评审，交给另一个实现环节修复，再重新运行和复审，最多三轮。

新 CLI：`gamekit.py review prepare --project <repo> --output <new-folder>` 和 `gamekit.py review evaluate --dir <folder>`。评审模板位于 `prompts/drui/reviewers/`，JSON 契约在 `docs/DRUI_REVIEW_REPORT_SCHEMA.md`，严苛标准位于 `docs/DRUI_STRICT_REVIEW_PROTOCOL.md`。

验收要求：**三位审查角色各 >=9/10，任何单项 >=8，P0/P1 无未验证的缺陷，真实截图/任务记录存在，验证结果和角色隔离可审计**。无真机/模拟器环境必须显示 BLOCKED，不得虚报 9.5 分。软件只能检测报告字段/证据路径是否存在，不能证实评审真实性。
