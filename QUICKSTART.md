# Quickstart — GameAgentKit 1.1.0

## 第一次使用 DRUI：先选目标，再运行工作流

```bash
drui start                   # 一分钟引导；不执行 Agent
drui help                    # 我该选哪个工作流？
drui list --beginner         # 精选 6 个入门流程
drui list --category review  # 只看严格评审
drui list --search 操作       # 按场景搜索（支持中英文）
drui help review-user        # 适用场景、权限、交付物和示例
drui prompt review-user     # 打印可复制指令（不运行 Agent）
```

在 Agent 对话中使用 `Use the drui skill, stage review-user, on this project.` 才是请求实际执行。终端的 `prompt` 只输出文本。`drui deps check` 可检测已锁定的外部 Skill 是否变更，但不会执行或升级第三方代码。

## Public v1.1.0：Oil UI Plus 与调用顺序

UI 方法统一优先级（不代表顺序执行四次）：**`oil-ui-pro`（官方、实际已安装） > `oil-ui-plus`（GameAgentKit 原创内置） > `oil-ui`（已安装开源版） > DRUI 其他内置通用流程**。DRUI 永远负责 workflow 编排、三方独立审查及验收。详见 [`docs/UI_SOURCE_ROUTING.md`](docs/UI_SOURCE_ROUTING.md)。

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

# DRUI / GameAgentKit 1.1.0 — Quickstart (macOS / Linux)

**Skill names:** `drui` (workflow orchestrator), `oil-ui-plus` (our original Pro-like UI method); optional external `oil-ui` and official paid `oil-ui-pro`. The extension is global and reusable for any game or UI project.

## DRUI short commands and UI method priority (v1.1.0)

After initial installation or upgrade, `gamekit.py link --agents all` safely makes `~/.local/bin/drui` point to the canonical Skill tool. No existing `drui` command or shell startup files are replaced. If not on PATH, run `python3 ~/GameAgentKit/scripts/drui list` or manually add `export PATH="$HOME/.local/bin:$PATH"` to `~/.zshrc`.

```bash
drui list                 # Chinese grouped workflow menu (20 workflows)
drui help review-user     # Explain a stage and permissions
drui prompt review-loop   # Print prompt for Codex / Claude / AGY; DOES NOT EXECUTE
```

In agent chat: type **`drui list`**, **`drui review-tl`** or **`drui review-loop`**. The agent must load `drui` and observe stage constraints. Reference: `docs/DRUI_COMMANDS_ZH.md`.

## 1. First-time install (Codex + Claude Code + Antigravity)

Download the `GameAgentKit-v1.1.0.zip` asset from https://github.com/zhenv5/drui/releases/tag/v1.1.0 into `~/Downloads`:

```bash
mkdir -p "$HOME/Downloads/GameAgentKit-v1.1.0"
unzip "$HOME/Downloads/GameAgentKit-v1.1.0.zip" -d "$HOME/Downloads/GameAgentKit-v1.1.0"

# Show planned changes, then install
bash "$HOME/Downloads/GameAgentKit-v1.1.0/GameAgentKit/install.sh" --agents all --dry-run
bash "$HOME/Downloads/GameAgentKit-v1.1.0/GameAgentKit/install.sh" --agents all
python3 "$HOME/GameAgentKit/gamekit.py" doctor --agents all
```

Default canonical root: `~/GameAgentKit/`. `all` means Codex, Claude Code, Antigravity IDE and Antigravity CLI. Optional `--agents codex,claude,antigravity,cursor`.

## 2. Upgrade if you already installed a previous GameAgentKit release

Extract v1.1.0 ZIP **into a new staging folder** using the unzip command above; don't unpack over `~/GameAgentKit`:

```bash
python3 "$HOME/GameAgentKit/gamekit.py" upgrade --from "$HOME/Downloads/GameAgentKit-v1.1.0/GameAgentKit" --dry-run
python3 "$HOME/GameAgentKit/gamekit.py" upgrade --from "$HOME/Downloads/GameAgentKit-v1.1.0/GameAgentKit"
python3 "$HOME/GameAgentKit/gamekit.py" link --agents all
python3 "$HOME/GameAgentKit/gamekit.py" doctor --agents all
```

Old kit files are backed up. **V1.2 users should additionally migrate the old skill name** (the original `oil-ui` remains untouched):

```bash
python3 "$HOME/GameAgentKit/gamekit.py" migrate-drui --dry-run
python3 "$HOME/GameAgentKit/gamekit.py" migrate-drui
python3 "$HOME/GameAgentKit/gamekit.py" link --agents all
python3 "$HOME/GameAgentKit/gamekit.py" doctor --agents all
```

If you previously attached a project and want its managed `AGENTS.md`/`CLAUDE.md` entry renamed, run `migrate-drui --project /path/to/game` (with `--dry-run` first). If you earlier extended your original `oil-ui`, the separate opt-in `extend-oil-ui --source /real/path/to/oil-ui --refresh` refreshes **only** the managed block, with a backup. Never automatically change your original Oil UI.

## 3. Your own original Oil UI (optional)

Replace path with the **real** directory containing the original `oil-ui/SKILL.md`:

```bash
python3 "$HOME/GameAgentKit/gamekit.py" register-external --name oil-ui --source "$HOME/.claude/skills/oil-ui" --agents all --dry-run
python3 "$HOME/GameAgentKit/gamekit.py" register-external --name oil-ui --source "$HOME/.claude/skills/oil-ui" --agents all
```

**Do not register a source folder that is itself an already-created kit symlink.** The external `oil-ui` stays separate from `drui`. Registration shares it via links without overwriting or changing the source. If one agent already has its original skill there, collisions are preserved; that is normal.

## 4. Trigger it from ANY game directory

Paste in Codex / Claude Code / Antigravity:

> Use `drui`, stage `full`, on this repository. Review actual screens and interactions, implement highest-impact fixes, rebuild/run on the target platform, capture real screenshots, independently re-review up to 3 rounds, and report evidence or BLOCKED conditions. Automatically select installed official `oil-ui-pro` > our original `oil-ui-plus` > open `oil-ui` > DRUI fallback. Report selected source and evidence of loading; never assume Pro access.

A **single, isolated stage** is also supported:

> Use `drui`, stage `visual-review`. Audit the current Home screen **read-only** using actual screenshots; list P0/P1/P2 findings, cite visual evidence, and make no source changes.

The exact slash-command syntax and automatic Skill discovery vary by Agent; explicitly naming the Skill is the portable trigger.

## 5. Select individual stages

```bash
python3 "$HOME/GameAgentKit/gamekit.py" workflow list
python3 "$HOME/GameAgentKit/gamekit.py" workflow prompt --stage visual-review
python3 "$HOME/GameAgentKit/gamekit.py" workflow prompt --stage usability-review --project "$HOME/Projects/YourGame"
python3 "$HOME/GameAgentKit/gamekit.py" workflow prompt --stage mini-game-scene --output "$HOME/Downloads/mini-game-review-prompt.md"
python3 "$HOME/GameAgentKit/gamekit.py" workflow prompt --stage full
```

`workflow prompt` produces pasteable instructions; **it does not run the agent**. There are **20 entries** (15 existing workflows plus 5 strict-review workflows): `full`, `discover`, `plan`, `implement`, `visual-review`, `usability-review`, `game-feel`, `fix`, `verify`, `screenshot-rebuild`, `component-polish`, `mini-game-scene`, `effects`, `dashboard`, `art-3d`.

## 6. Optional project profile

```bash
python3 "$HOME/GameAgentKit/gamekit.py" attach --project "$HOME/Projects/YourGame" --profile ios-swiftui --name "Your Game"
```

Available profiles: `ios-swiftui`, `web-game`, `puzzle`, `arcade`, `3d-game`, `generic`. No repeated per-game Skill installation. See `docs/DRUI_USAGE.md` for every stage, limitations and example prompts.


## V1.5: Trigger TL / PM / User without running the full design cycle

Paste one of these into Codex, Claude Code, Antigravity (separate chats are best):

> Use `drui`, stage `review-tl`. Inspect the app as a strict Tech Lead. REVIEW-ONLY; provide P0/P1/P2, reproducible steps, code references, test evidence and 5-axis scoring.

> Use `drui`, stage `review-pm`. Inspect as a strict PM: product promise, onboarding, gameplay loop, scope and acceptance tests. REVIEW-ONLY.

> Use `drui`, stage `review-user`. Attempt the full main task cold on a simulator/device as a first-time user; provide an exact step-by-step task trace and friction report. REVIEW-ONLY.

> Use `drui`, stage `review-triad`. Start three isolated reviewer contexts, evaluate separately and arbitrate disagreements. Do not change code.

> Use `drui`, stage `review-loop`. After independent reviews, prioritize fixes, implement in a separate role, rebuild, capture fresh evidence and repeat review for up to 3 useful rounds.

For CLI-generated copy-paste prompts use `python3 ~/GameAgentKit/gamekit.py workflow prompt --stage review-triad`. To prepare three separate report assignments:

```bash
python3 ~/GameAgentKit/gamekit.py review prepare --project "$PWD" --output "$PWD/drui-reviews/run-001"
python3 ~/GameAgentKit/gamekit.py review evaluate --dir "$PWD/drui-reviews/run-001"
```

The second command **fails until** three real review reports have been filled; it never performs testing automatically. See [`docs/DRUI_STRICT_REVIEW_PROTOCOL.md`](docs/DRUI_STRICT_REVIEW_PROTOCOL.md).

## 升级外部开源 Skill 的安全流程

安装后执行一次 `drui deps list` 和 `drui deps lock` 建立本地基线。第三方 Skill 升级后用 `drui deps check` 检测，必须经过独立兼容性审查并通过 `drui deps approve --name <名称> --evidence /path/to/review.md` 才被重新视为可信候选。`drui update` **只更新 GameAgentKit 内置的 drui / oil-ui-plus 等文件，不会更新或覆盖第三方 Skill**。详见 `docs/EXTERNAL_SKILL_UPDATES.md`。

Check duplicate user-owned Skill names: `drui deps conflicts`. Optional: `drui deps conflicts --project /path/to/game`. On detected conflicts the user file is preserved, and runtime resolution must be checked in each Agent.
