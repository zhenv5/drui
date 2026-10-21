# DRUI · 安装、更新与验证

**官方来源：** [zhenv5/drui](https://github.com/zhenv5/drui) · [最新稳定 Release](https://github.com/zhenv5/drui/releases/latest)。DRUI 仅通过 GitHub **Git 源码**安装/更新，不使用 ZIP；需要 Git、Python 3 和 macOS/Linux。

## 1. 命令行首次安装

在官方 Release 页核对最新稳定版本 Tag（`vX.Y.Z`，非 prerelease），下面 `v1.4.2` 是本版示例；未来有新版本应替换。若已存在 `~/GameAgentKit`，不要覆盖。

```bash
git clone --depth 1 --branch v1.4.2 https://github.com/zhenv5/drui.git "$HOME/GameAgentKit"
git -C "$HOME/GameAgentKit" remote get-url origin
cat "$HOME/GameAgentKit/VERSION"
# 阅读 install.sh / gamekit.py 并检查将创建哪些链接
bash "$HOME/GameAgentKit/install.sh" --agents codex,claude,antigravity,cursor --dry-run
```

确认 dry-run 没有准备覆盖用户文件后，再运行。安装输出写到本地临时日志，**只显示简短验证结果**，异常时命令必须返回非零码：

```bash
DRUI_LOG=$(mktemp)
if bash "$HOME/GameAgentKit/install.sh" --agents codex,claude,antigravity,cursor >"$DRUI_LOG" 2>&1; then
  "$HOME/GameAgentKit/scripts/drui" verify
else
  echo "DRUI install failed; details: $DRUI_LOG" >&2
  tail -n 3 "$DRUI_LOG" >&2
  false
fi
```

重要：安装器**保留现有同名用户 Skill**，即使跳过冲突，安装命令本身也可能返回 0。只有后续 `drui verify` 退出码也为 0，才能确认选定 Agent 的本地文件安装成功。

## 2. 验证命令与输出

```bash
"$HOME/GameAgentKit/scripts/drui" verify         # 默认四个 Agent；一行摘要
drui verify --agents codex,cursor               # 仅指定 Agent
drui verify --verbose                           # 完整 Skill/版本/路径/冲突清单
drui verify --json                              # 机器可读的完整结果
drui verify --project /path/to/game             # 额外检查项目 Skill 遮蔽
```

成功时的**示例**（不是用户机器的实测结果）：

```text
DRUI v1.4.2 PASS | 4 agents | 60/60 Skill links | 0 errors, 0 warnings | runtime untested
```

四个 Agent 共 **5 个 Skill 目录**：Codex 1、Claude Code 1、Antigravity 2、Cursor 1；各有 12 个内置 Skills，故 60/60。旧别名 **`--agents all` 只包含 Codex、Claude、Antigravity，不包含 Cursor**，建议明确传入四个 Agent。

| 状态 | 含义 |
|---|---|
| `OK` | 本地链接指向内置 Skill，元数据匹配 |
| `MISSING` | 链接不存在 |
| `BROKEN` | 链接损坏 |
| `COLLISION` | 已有用户 Skill 占用位置，未覆盖 |
| `INVALID` | 内置 Skill 元数据不符 |

默认输出只有一行，失败时最多增加一行、列出前三个问题。摘要中的 warning 可能是 `~/.local/bin` 不在 PATH，或项目中的同名 Skill 可能遮蔽全局版本。使用 `--verbose` 查详情。内置 Skill 版本跟随 DRUI 发布版本；外部 Skill 只有在自己的 `SKILL.md` 声明时才显示独立版本，否则为 `unknown`。**验证本地文件不等于 Agent 实际加载或执行成功。**

## 3. 一键复制 Prompt 给 Agent

首次安装不要求先有 DRUI 命令：从 [README 安装 Prompt](../README.md#install-via-agent) 复制给有本机终端权限的 Codex、Claude Code、Antigravity、Cursor。已安装用户可以：

```bash
drui agent install      # 显示安装 Prompt
drui agent update       # 显示更新 Prompt
drui copy install       # 复制到剪贴板
drui copy update        # 复制更新 Prompt
```

这几个命令只打印或复制文字，**不自行安装/更新**。Agent 应审查来源和 dry-run、真正执行验证、检查退出码，最后**只回报短摘要**（成功一行；失败最多三项）和必要阻塞原因，不粘贴长日志。未建立外部 Skill 指纹锁时 `deps check` 会报无 baseline，这**不是 DRUI 安装失败**；不要自动 `lock` / `approve`。

## 4. GitHub 源码升级

```bash
"$HOME/GameAgentKit/scripts/drui" update --repo zhenv5/drui --check
# 查看变更并确认 git status 干净，然后显式同意升级：
"$HOME/GameAgentKit/scripts/drui" update --repo zhenv5/drui --yes
python3 "$HOME/GameAgentKit/gamekit.py" link --agents codex,claude,antigravity,cursor
"$HOME/GameAgentKit/scripts/drui" verify           # 以退出码验收
```

更新器只接受官方 Git origin 和最新正式 Release Tag，拒绝脏工作区，不下载 ZIP、不给第三方 Skill 自动升级。Git checkout 不是断电原子操作；若中断应检查工作树，不要擅自 `reset --hard`。

## 5. 故障排查

| 症状 | 处理 |
|---|---|
| `drui: command not found` | 用 `"$HOME/GameAgentKit/scripts/drui"`；必要时手动设置 `export PATH="$HOME/.local/bin:$PATH"` |
| `MISSING` | 复查安装 Agent 范围，运行 `python3 ~/GameAgentKit/gamekit.py link --agents codex,claude,antigravity,cursor` 后重新 verify |
| `BROKEN` | 检查 `~/GameAgentKit` 是否被移动；不要自动删除用户文件 |
| `COLLISION` | `drui verify --verbose`、`drui deps conflicts`；保留用户 Skill，人工处理 |
| `INVALID` | 核对仓库 Skill 内容与 `VERSION`；停止宣称验证成功 |
| `PASS` 但 Agent 找不到 Skill | 在目标 Agent 新会话说 `Use the drui skill and list its workflows` 并检查它读取的实际文件 |
| `deps check` 无 baseline | 先 `drui deps list`；用户审查后可自愿执行 `drui deps lock` |
| 安装失败 | 阅读 `DRUI_LOG` 路径，保留非零退出码和原始日志；不要假报 PASS |

**信任边界：** Git Tag / Git 对象哈希并不保证发布者身份或防范仓库被入侵；需要审查来源与变更。真实 Agent 加载必须在对应 Agent 中独立测试。参阅 [SECURITY.md](../SECURITY.md) 和 [第三方依赖规则](EXTERNAL_SKILL_UPDATES.md)。
