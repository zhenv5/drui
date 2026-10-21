# DRUI — GameAgentKit

**Game UI, interaction and game-feel workflows for coding agents.** Cross-Agent · 12 bundled Skills · 20 workflows · read-only independent reviews and optional fix loops. Public name **DRUI**, internal kit **GameAgentKit**.

[Quickstart](QUICKSTART.md) · [20 workflows](docs/DRUI_COMMANDS_ZH.md) · [External Skill dependency policy](docs/EXTERNAL_SKILL_UPDATES.md) · [Releases](https://github.com/zhenv5/drui/releases)

**Installation and updates use the official GitHub source repository, not a release ZIP.** GitHub may automatically offer “Source code (zip)” downloads, but those are not DRUI installers. Use Git to fetch stable version tags.

## Install via Agent

Copy the entire following prompt into Codex, Claude Code, Antigravity or Cursor with local terminal access. You do **not** need DRUI already installed.

```text
请在本机使用 GitHub 源码安装 DRUI（GameAgentKit），官方仓库仅 https://github.com/zhenv5/drui 。不要下载、解压或安装 ZIP。
1. 检查 git、Python 3、本机已有 DRUI 路径、Codex/Claude Code/Antigravity/Cursor 的 Skill 名称冲突；不要移动或覆盖用户自己的 Skills。检查最新 GitHub 正式 Release 的版本 Tag（必须 vX.Y.Z，非预发布），确认发布者及仓库。
2. 若 ~/GameAgentKit 已存在，停止首次安装并报告，不要覆盖。运行 git clone --depth 1 --branch <确认的稳定Tag> https://github.com/zhenv5/drui.git "$HOME/GameAgentKit"（替换 <确认的稳定Tag> 为真实版本）。必须确保远端 origin 是官方仓库、仓库 VERSION 与 Tag 一致，再审查 install.sh 和 gamekit.py。
3. 在源码根目录执行 bash "$HOME/GameAgentKit/install.sh" --agents codex,claude,antigravity,cursor --dry-run；确认仅创建安全的 Skill/CLI 链接后，再执行不带 --dry-run 的命令。占用的同名 Skill 保留，不要强行替换。不要执行第三方 Skill 安装器。
4. 完成后检查 doctor、version、list --beginner 和 deps conflicts；详细命令输出保存在本机日志，不要粘贴给用户。最后必须运行 "$HOME/GameAgentKit/scripts/drui" verify --agents codex,claude,antigravity,cursor，向用户强制输出且仅输出紧凑验证摘要（通常一行；失败时最多附三项具体失败）。不能声称 Agent 已实际加载，除非真实验证。
所有更新和安装必须来自 GitHub 源码 Tag；不使用 Release ZIP、curl|bash、git pull 覆盖、force checkout。DRUI 永不自动升级或批准第三方 Skills。
```

## Update via Agent

Copy this prompt to the coding agent to update an existing GitHub checkout safely:

```text
请将本机已安装的 DRUI / GameAgentKit 用官方 GitHub 源码 Tag 升级，不使用 ZIP；仓库只能是 https://github.com/zhenv5/drui 。
1. 确认 ~/GameAgentKit 是 Git checkout，origin 指向官方仓库，无未提交的源码改动/未追踪文件；先运行 drui version、drui deps check、drui deps conflicts，记录旧版本和独立安装的用户 Skills。不允许覆盖用户数据，也不允许自动更新、lock 或 approve 第三方 Skills。
2. 运行 "$HOME/GameAgentKit/scripts/drui" update --repo zhenv5/drui --check；查看 GitHub 正式 Release 变更和 Tag。若无新版本则停止；如果当前仓库有改动，停止并报告，不要 git reset --hard、clean 或 force checkout。
3. 确认无冲突后执行 "$HOME/GameAgentKit/scripts/drui" update --repo zhenv5/drui --yes。DRUI 使用 Git 获取官方 Tag、验证源码 VERSION，再切换 checkout；不会下载/解压 ZIP。异常中断时保留现场供人工修复，不保证断电事务原子性。
4. 完成后运行 python3 "$HOME/GameAgentKit/gamekit.py" link --agents codex,claude,antigravity,cursor（只链接空位），检查 doctor、version、list --beginner、deps check 和 deps conflicts；日志留本机，不粘贴长清单。最后必须运行 "$HOME/GameAgentKit/scripts/drui" verify --agents codex,claude,antigravity,cursor，向用户强制输出且仅输出紧凑验证摘要（通常一行；失败时最多附三项具体失败）。不得声称已实际加载 Agent。
整个流程严格禁止 curl|bash、静默依赖升级以及对已有第三方 Skill 路径的写入。
```

## Manual GitHub source installation

Prerequisites: Git, Python 3, macOS or Linux, permission to create local Skill links. First check the [latest official stable release](https://github.com/zhenv5/drui/releases/latest) and substitute the matching Tag in the clone command.

```bash
git clone --branch v1.4.0 --depth 1 https://github.com/zhenv5/drui.git "$HOME/GameAgentKit"
bash "$HOME/GameAgentKit/install.sh" --agents codex,claude,antigravity,cursor --dry-run
# Save detailed installation logs locally; print only the mandatory compact verification.
DRUI_LOG=$(mktemp)
if bash "$HOME/GameAgentKit/install.sh" --agents codex,claude,antigravity,cursor >"$DRUI_LOG" 2>&1; then
  "$HOME/GameAgentKit/scripts/drui" verify
else
  tail -n 5 "$DRUI_LOG"
fi
```

`drui` is linked at `~/.local/bin/drui`; add that directory to PATH if necessary. Installation never overwrites a preexisting Skill or CLI of the same name. Four agents currently span five Skill search paths (Antigravity uses two), so a clean install can report 60/60 slots rather than 48/48. The final verifier audits files, not actual Agent loading. If `~/GameAgentKit` exists, do not repeat `git clone` into it.

## Update with GitHub source

```bash
drui update --check
# After reviewing changes and ensuring the checkout is clean:
drui update --yes
```

The updater checks GitHub's latest stable Release to find an immutable version Tag, verifies the official Git origin, checks for local modifications, fetches the Tag using Git, confirms `VERSION` and CLI, and checks out that commit. It **does not use ZIP, extract assets, silently update external Skills, erase user edits, or invoke external installers**. `drui update --check` makes no changes. A crash mid-checkout is not guaranteed to be atomic.

## Start using DRUI

```bash
drui verify                        # one-line result; up to 3 failures if incomplete
drui verify --verbose              # full Skill names, versions, paths and conflicts
drui verify --json                 # machine-readable verification report
drui start                         # first minute overview
drui list --beginner               # curated starter workflows
drui list                          # all 20 stages
drui list --category review        # TL/PM/user independent reviews
drui help usability-review         # permissions, when to use, deliverables
drui prompt review-loop            # print ready-to-paste Agent instruction
drui copy update                   # copy GitHub-update Agent prompt to clipboard
```

The CLI generates prompts, not a running coding agent. User tasks with code changes require explicit instructions and real testing.

## Safety and boundaries

- The UI method priority is official available `oil-ui-pro` > bundled original `oil-ui-plus` > approved external `oil-ui` > generic DRUI. Real access and licensing are not assumed.
- DRUI manages its own built-in Skills only. Existing user-owned Skills are never overwritten; independent upstream upgrades are fingerprint-detected, not auto-approved. See [dependency policy](docs/EXTERNAL_SKILL_UPDATES.md).
- Git provenance is not a substitute for publisher trust or source-code review. GitHub Release tags can be moved by repository administrators; verify publisher, version and commit before installation.
- Real Agent loading, screenshots, builds and true three-party independent reviews require runtime evidence; printed prompts alone do not prove completion.

See [QUICKSTART.md](QUICKSTART.md) for setup, updates and troubleshooting.
