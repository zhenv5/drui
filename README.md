# DRUI — GameAgentKit v1.2.0

**DRUI** is the public-facing skill/workflow command; **GameAgentKit** is the internal Python toolkit and installation root. The names intentionally differ.

**Official repository:** https://github.com/zhenv5/drui  
**Installable release asset:** `GameAgentKit-v1.2.0.zip` from [GitHub Releases](https://github.com/zhenv5/drui/releases/tag/v1.2.0). Do **not** use GitHub's generic “Source code (zip)” for the installer because it contains a different outer directory.

**Note:** v1.0.0 is the first public release. Documents named `CHANGELOG_v1.1.md` through `CHANGELOG_v1.7.md` describe the toolkit's earlier internal development iterations, not published releases following v1.0.0.

**12 bundled Skills · 20 selectable workflows · local third-party dependency fingerprint approval.** CLI commands print agent prompts; they do not themselves perform app editing, agent review, or runtime validation.

## Install via Agent

**No DRUI installed yet?** Copy the first prompt using GitHub's code-block **Copy** icon and paste it into a terminal-capable Codex / Claude Code / Antigravity / Cursor conversation. You do not have to run a shell installer yourself. The Agent must have terminal access and must verify results; merely pasting text does not install anything.

### 一键复制：首次安装 / Copy to Agent — Install

```text
请在我当前使用的 macOS/Linux 电脑上安装 DRUI（内部框架 GameAgentKit），官方唯一来源：https://github.com/zhenv5/drui 。你是执行安装的 coding agent，请实际完成操作，不要只给我安装教程。

1. 先确认本机可运行 Python 3、拥有可写的用户目录，并确认你能在此 Agent 会话中使用终端。如无法运行命令，明确说明，绝不声称已安装。检查 ~/GameAgentKit、~/.local/bin/drui 及 Codex/Claude Code/Antigravity/Cursor 的既有 Skills；不得覆盖用户已有文件、目录、不同来源的同名 Skill 或 symlink。如果已经安装，先报告版本并改用官方更新流程，不要直接重新安装。
2. 访问 https://github.com/zhenv5/drui/releases/latest ，确认发布者 zhenv5/drui，选择最新的正式（非 draft / prerelease）版本。只获取该 Release 的 GameAgentKit-vX.Y.Z.zip 和同名 .sha256 校验文件；核对版本与 SHA-256，拒绝校验失败、重定向到不可信站点或不符合预期结构的包。SHA-256 仅用于完整性，不等同于签名或代码安全保证。不要运行 curl | bash 或来历不明的第三方安装脚本。
3. 在临时目录安全解包并阅读 README.md、QUICKSTART.md、install.sh 和关键安装逻辑；留意危险脚本、外部依赖、权限和将写入的路径。先执行安装脚本的 --dry-run，确认不会覆盖用户自有 Skill 后再执行安装。默认安装至 ~/GameAgentKit，并为本机可用的 Agent 建立共享 Skill 入口；不要无故修改 shell profile 或项目文件。若遇到冲突，请保留原文件并列出需要我确认的决定，不要强行覆盖。
4. 通过实际命令检查：python3 ~/GameAgentKit/gamekit.py doctor --agents all（如果只安装部分 Agent 则使用相同 scope）、python3 ~/GameAgentKit/scripts/drui version、python3 ~/GameAgentKit/scripts/drui start、python3 ~/GameAgentKit/scripts/drui deps conflicts。若 drui 已进入 PATH，也验证 drui list --beginner。把版本、安装位置、Agent 覆盖范围、检查结果、潜在冲突和剩余手动步骤汇报给我。不存在运行环境时，不得虚报成功。
5. 外部油 UI/其他第三方 Skills 始终由用户或其发布者管理：不要自动安装、升级、删除或批准外部依赖；不要创建未经审查的 deps lock，也不要绕过指纹检查。只安装官方 DRUI 捆绑的 12 个内置 Skills。
```

### 一键复制：升级现有 DRUI / Copy to Agent — Update

```text
请在我当前使用的 macOS/Linux 电脑上升级已安装的 DRUI（GameAgentKit）到官方最新稳定版本。官方仓库：https://github.com/zhenv5/drui 。你是执行升级的 coding agent，请实际完成检查、备份、更新和回归验证，不要只给我文字指南。

1. 先检查 ~/GameAgentKit、当前 drui version、已固定的 GitHub 更新源、现有用户 Skills 与指纹状态。运行 drui deps list、drui deps conflicts、drui deps check；如果 drui 不在 PATH，使用 python3 ~/GameAgentKit/scripts/drui。`deps check` 发现漂移要如实报告，但绝不自动 lock、approve、覆盖或升级第三方 Skills。如果目录不是官方 DRUI，或固定的源不是 zhenv5/drui，停止并征询我的决定，不能偷偷换源。
2. 用内置安全更新器先执行 drui update --repo zhenv5/drui --check（若已有相同来源也可以省略 --repo），确认官方 GitHub Release 的最新稳定版本及版本差异。阅读 Release Notes 和变更；若已是最新则不要重复安装。如果无法联网、没有通过预检或需要强制覆盖用户文件，不要执行更新。
3. 若来源及预检正常，执行 drui update --repo zhenv5/drui --yes（或等价的 python3 ~/GameAgentKit/gamekit.py update ... --root ~/GameAgentKit）。让内置更新器校验 Release ZIP 和 SHA-256、使用安全暂存与备份，并仅更新 GameAgentKit 托管文件。不要用 git pull、unzip 直接覆盖 ~/GameAgentKit，也不要运行第三方升级器。更新过程中发生错误须保留现场并报告，不能谎称已经回滚或完成。
4. 升级后运行 drui version、drui list --beginner、python3 ~/GameAgentKit/gamekit.py doctor --agents <你实际安装的 Agent scope>、drui deps conflicts 和 drui deps check；必要时先使用 python3 ~/GameAgentKit/gamekit.py link --agents all 的安全重链机制，不能覆盖用户自己的同名 Skill 或命令。报告升级前后版本、发行来源、检查结果、备份路径及仍需处理的冲突。
5. 绝不自动修改第三方 oil-ui / oil-ui-pro 等 Skills，不执行外部安装脚本，也不把 SHA-256 指纹检查表述成兼容性或运行安全证明。
```

After installation, you can also use the local clipboard (macOS pbcopy / Linux wl-copy, xclip or xsel):

```bash
drui agent install           # print exactly the installation prompt above
drui agent update            # print exactly the update prompt above
drui copy install            # copy installation prompt to clipboard
drui copy update             # copy update prompt to clipboard
drui agent update --copy     # alternate spelling
```

**Copy != execute.** These commands never install, upgrade or call an Agent. The first-time prompts are included in the repo under [`prompts/agent-setup/`](prompts/agent-setup/) and can be audited independently. See [`QUICKSTART.md`](QUICKSTART.md) for manual commands.

## New here? Start in 60 seconds (v1.2.0)

DRUI can help decide which workflow to use before you touch the project. The terminal **never runs your Agent**: it explains a workflow or prints a prompt you can paste into Codex, Claude Code, Antigravity or Cursor.

```bash
drui start                      # guided first-use tour
drui help                       # quick goal-to-workflow chooser
drui list --beginner            # six safe starting points
drui list --category review     # core | ui | specialty | review
drui list --search 操作          # search Chinese / English use cases
drui help review-loop           # scope, write permissions, deliverables, example
drui prompt review-loop --project /path/to/game  # print instructions ONLY
drui help commands              # complete quick command reference
```

**Choose by goal:** Can't find the controls → `usability-review` (read-only); unpolished visuals → `visual-review` (read-only); technical/product/user independent feedback → `review-triad` (read-only); review → fix → retest → re-review → `review-loop` (may edit); end-to-end overhaul → `full` (may edit). All 20 workflows and scopes remain in `drui list --json` for tooling. The original `v1.0.0` Release is immutable; v1.1.0 adds onboarding commands.

**Agent chat example:** `Use the drui skill, stage usability-review, on this project. Try the main task as a first-time user; report blockers and evidence. Do not edit files.`

## Public v1.0.0 — Third-party Skill updates (safe by default)

Open-source and paid external Skills can update independently. `drui update` upgrades **only our GameAgentKit**; `oil-ui-pro` / `oil-ui` / other third-party Skills are **not** automatically updated or bundled. Optional local fingerprint gating prevents an upgraded unapproved Pro or open Oil UI from silently replacing bundled `oil-ui-plus`.

```bash
drui deps list       # inventory all user-owned external Skills, even same-name copies
drui deps conflicts  # detect bundled-name collisions, never overwrite
drui deps lock       # create baseline once; does not install or update anything
drui deps check      # inspect changed/new/missing external Skills
drui sources         # priority Pro > Plus > oil-ui > DRUI, with gate
# after reviewing upstream diff and testing:
drui deps approve --name oil-ui --evidence ./oil-ui-compatibility-review.md
```

See [`docs/EXTERNAL_SKILL_UPDATES.md`](docs/EXTERNAL_SKILL_UPDATES.md). If `deps check` reports changes, default DRUI auto mode bypasses modified external sources and uses our unchanged bundled `oil-ui-plus`; explicitly forced external sources fail visibly. Without a baseline, availability is **unverified**.

## DRUI 快捷入口与 Oil UI Plus（v1.0.0）

安装一次，所有游戏与多 Agent 共用。升级后运行 `python3 ~/GameAgentKit/gamekit.py link --agents all` 创建 `~/.local/bin/drui` 命令链接（不覆盖已有同名文件，不修改 Shell PATH）。

```bash
drui list                       # 20 个 workflow，分组中文菜单
drui help review-tl             # 了解某个 workflow
drui prompt review-loop         # 生成可复制给 Agent 的 Prompt，不自动执行
drui list --json                # 机器可读
```

如果 `drui: command not found`：`python3 ~/GameAgentKit/scripts/drui list`；也可以手动向 `~/.zshrc` 增加 `export PATH="$HOME/.local/bin:$PATH"`。

**Agent 对话里**发送 `drui list` 显示菜单；`drui review-tl` 直接请求该 Skill 执行指定审查（需 Agent 成功加载 Skill）；`drui review-loop` 请求完整三方审查-修复闭环。详见 [`docs/DRUI_COMMANDS_ZH.md`](docs/DRUI_COMMANDS_ZH.md)。

---


## V1.7：Oil UI Plus 与调用顺序

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

# GameAgentKit — One skill library for every game, shared across agents

A cross-project, cross-agent **game development toolkit**. It is **not** specific to MathMelo or any game. It ships twelve reusable, original skills for game visual design, UX, feel, level design, art, QA, performance, audio, native iOS and web game development.

**One canonical root**: `~/GameAgentKit/skills/`. Install once. Codex, Claude Code and Google Antigravity (IDE and CLI) load the **same** underlying files through user-global symlinks. No downloads or API keys required. Optional Cursor support.

## DRUI: 20 workflow stages + Oil UI Plus (v1.0.0)

- **Skill name:** `drui` (orchestrator) with bundled original `oil-ui-plus`; `oil-ui` and paid `oil-ui-pro` are external.
- **Reliable cross-agent activation:** `Use the drui skill, stage visual-review, to audit the Home screen. Read-only; use real screenshots.`
- **Complete workflow:** `Use drui stage full; inspect → design → implement → review → fix → verify.`
- **Stage isolation:** the 20 independently selectable workflows can be read/run one at a time; `visual-review` and `usability-review` must not change code. Details: [`docs/DRUI_USAGE.md`](docs/DRUI_USAGE.md).
- **Prompt generator (does not run agents):**

```bash
python3 ~/GameAgentKit/gamekit.py workflow list
python3 ~/GameAgentKit/gamekit.py workflow prompt --stage visual-review
python3 ~/GameAgentKit/gamekit.py workflow prompt --stage component-polish --project ~/Projects/MyGame
python3 ~/GameAgentKit/gamekit.py workflow prompt --stage full
```

### Updated ZIP extraction commands (first install OR upgrade staging)

```bash
mkdir -p "$HOME/Downloads/GameAgentKit-v1.0.0"
unzip "$HOME/Downloads/GameAgentKit-v1.0.0.zip" -d "$HOME/Downloads/GameAgentKit-v1.0.0"
```

Then **first install** using the commands below, or **existing install** using the V1.3 upgrade block below. Don't unpack directly over `~/GameAgentKit`.

## First-time install on Mac / Linux

1. Extract `GameAgentKit-v1.0.0.zip` from the tagged GitHub Release using the `mkdir`/`unzip` commands above; your staging installer is at `~/Downloads/GameAgentKit-v1.0.0/GameAgentKit/install.sh`.
2. From Terminal:

```bash
# Preview without changing anything
bash ~/Downloads/GameAgentKit-v1.0.0/GameAgentKit/install.sh --root "$HOME/GameAgentKit" --agents all --dry-run

# Install canonical kit and link skills globally
bash ~/Downloads/GameAgentKit-v1.0.0/GameAgentKit/install.sh --root "$HOME/GameAgentKit" --agents all

# Check skill paths
python3 ~/GameAgentKit/gamekit.py doctor --agents all
```

**`--agents all` = `codex,claude,antigravity`**. Optional `--agents codex,claude,antigravity,cursor`. Other aliases: `claude-code`, `agy`. The tool refuses to overwrite existing skills at those names; conflicts print `SKIP` and require manual resolution. Symlinks are preferred; `--copy` allows systems that cannot use symlinks but copies will not update automatically.

### Global target paths

| Agent | Shared global skill discovery path |
|---|---|
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Antigravity IDE/app | `~/.gemini/config/skills/` |
| Antigravity CLI (`agy`) | `~/.gemini/antigravity-cli/skills/` |
| Cursor (optional) | `~/.cursor/skills/` |

Every entry points back to `~/GameAgentKit/skills/<name>`; a single modification to a central Skill is reflected in all symlinked agents. Restart the agents if discovery caches do not refresh.

## Use with any new game: NO reinstallation needed

After the global install, open Codex/Claude/Antigravity at any game's repository and prompt:

> Use the globally installed `game-qa-review` and `game-ui-design` skills. Inspect this game, run three independent review/fix/test passes and report actual runtime evidence.

That works without any per-game setup. **Optional project context** helps agents respect the platform, audience, gameplay and art direction:

```bash
python3 ~/GameAgentKit/gamekit.py attach \
  --project "$HOME/Projects/MyNewGame" \
  --profile ios-swiftui --name 'My New Game'

# Other profiles: generic, puzzle, arcade, web-game, 3d-game
python3 ~/GameAgentKit/gamekit.py attach \
  --project "$HOME/Projects/NewBrowserGame" --profile web-game
```

`attach` writes only `.game-agent-kit/config.json`, `.game-agent-kit/PROFILE.md`, and **only if absent** minimal `AGENTS.md` / `CLAUDE.md` entries. It will not overwrite existing project instructions or source code. If a repo already has an `AGENTS.md` or `CLAUDE.md`, it prints a snippet to merge manually. In that case prompt the agent to read `.game-agent-kit/PROFILE.md` until the rules are manually linked.

You can edit a game's `.game-agent-kit/PROFILE.md` to set its actual art, device and gameplay constraints. All games continue pointing to the **same** global skills.

## Important commands

```bash
# Review proposed install or changes
bash ~/Downloads/GameAgentKit-v1.0.0/GameAgentKit/install.sh --dry-run
python3 ~/GameAgentKit/gamekit.py attach --project /path/to/game --profile puzzle --dry-run

# Link existing root to another agent (no copying of skills)
python3 ~/GameAgentKit/gamekit.py link --agents cursor

# Diagnose installed skill links and a project's optional profile
python3 ~/GameAgentKit/gamekit.py doctor --agents all --project /path/to/game

# Update the central kit using a *new* extracted package; old files backed up
python3 ~/GameAgentKit/gamekit.py upgrade --from ~/Downloads/GameAgentKit-v1.0.0/GameAgentKit --dry-run
python3 ~/GameAgentKit/gamekit.py upgrade --from ~/Downloads/GameAgentKit-v1.0.0/GameAgentKit
python3 ~/GameAgentKit/gamekit.py migrate-drui --dry-run   # safe legacy-name check
python3 ~/GameAgentKit/gamekit.py migrate-drui             # archives old packaged skill and exact links
python3 ~/GameAgentKit/gamekit.py link --agents all

# Remove only kit-owned symlinks, no projects or custom skills touched
python3 ~/GameAgentKit/gamekit.py unlink --agents all --dry-run
```

To add a **user-owned** skill, keep it outside the release-managed `~/GameAgentKit/skills/` directory and link it with `gamekit.py register-external --name your-skill --source /path/to/your-skill --agents all`. Existing slots are never overwritten. There is **no need** to re-attach projects.

## Which skills to use?

| Skill | For |
|---|---|
| `game-ui-design` | UI visual hierarchy, game character/UI coherence, contrast |
| `game-ux-flow` | Onboarding, screen flow, controls, children/mobile ergonomics |
| `game-feel-polish` | Feedback, haptics, easing, celebratory interaction |
| `gameplay-design` | Main gameplay loop, progression, levels, rewards |
| `game-art-pipeline` | Character, scenery, sprites, professional art QA |
| `game-qa-review` | Repeatable three-pass independent quality gate |
| `native-ios-game` | SwiftUI/SpriteKit implementation and Xcode verification |
| `web-game` | Canvas/WebGL/DOM games, real browser QA |
| `game-performance` | FPS, loading, memory, rendering and device profiling |
| `game-audio` | Sound effects, mixing, licensing and audio accessibility |
| `drui` | Original Oil UI companion prompts for independent, scored UI review and Pro-like workflows |

Project profiles can be game/platform specific without changing global Skills. The package is compatible with *any* game name; examples are not hard-coded into installer logic.

## Source, licensing and external integrations

- Bundled Skills are original guidance and require no third-party installation. See `docs/THIRD_PARTY.md` for optional upstream Skill links.
- `SKILL.md` is a reusable instruction format, **not** a universal MCP runtime. You must separately connect external tool servers such as Loopcut/ComfyUI and configure accounts/keys for each agent.
- The scripts run locally via Python 3 stdlib and Bash. Install does **not** touch projects or execute downloaded code.
- Real iOS testing requires macOS + Xcode; see `scripts/mac-ios-preflight.sh`. An environment preflight is not a simulator build.
- Installer tests run locally with fake home directories in `tests/test_gamekit.py`; no user's configuration is modified by running tests.
- Review every external Skill's license, permissions and dependencies before adopting it. `GameAgentKit` is independently authored; it does not bundle or redistribute third-party Skill contents.

## Oil UI integration (enhanced in v1.3)

Your existing `oil-ui` Skill remains **owned by you**. The kit does **not** install, modify, reverse engineer or unlock Oil UI Pro. It adds `drui` and the separate original `oil-ui-plus` Skill with implementation prompts for design directions, image-to-functional-UI, usability, a scored 9/10 review target, 19 original card patterns and mini-game effects. See `docs/OIL_UI_CAPABILITY_MATRIX.md` and `prompts/OIL_UI_ENHANCED_WORKFLOW.md`.

The enhanced skill is automatically linked by `link --agents all`. Optionally make your existing Oil UI visible to all agents without copying or overwriting anything:

```bash
# Replace with the ACTUAL directory containing your existing oil-ui/SKILL.md
python3 ~/GameAgentKit/gamekit.py register-external \
  --name oil-ui --source "$HOME/.claude/skills/oil-ui" \
  --agents all --dry-run
python3 ~/GameAgentKit/gamekit.py register-external \
  --name oil-ui --source "$HOME/.claude/skills/oil-ui" \
  --agents all

# Unregister only links that point to the exact source, leave original intact
python3 ~/GameAgentKit/gamekit.py unregister-external \
  --name oil-ui --source "$HOME/.claude/skills/oil-ui" \
  --agents all --dry-run
```

If your source is in a different agent's directory or an external repo, change `--source`. The installer does **not** guess where your skill lives. If a destination already contains a different `oil-ui`, it prints SKIP rather than overwriting.

**UI method selection:** installed official `oil-ui-pro` > bundled original `oil-ui-plus` > external `oil-ui` > DRUI fallback; DRUI then orchestrates native implementation → real screenshot + task completion → independent UI scorecard → fix and repeat up to 3 passes. Aim for 9/10, not invented ratings. For Apple builds use Xcode/Simulator; passing syntax checks is not enough.

Upgrade from V1.0, V1.1 or V1.2 (after extracting V1.3 into its separate staging folder):

```bash
python3 ~/GameAgentKit/gamekit.py upgrade --from ~/Downloads/GameAgentKit-v1.0.0/GameAgentKit --dry-run
python3 ~/GameAgentKit/gamekit.py upgrade --from ~/Downloads/GameAgentKit-v1.0.0/GameAgentKit
python3 ~/GameAgentKit/gamekit.py migrate-drui --dry-run   # safe legacy-name check
python3 ~/GameAgentKit/gamekit.py migrate-drui             # archives old packaged skill and exact links
python3 ~/GameAgentKit/gamekit.py link --agents all
python3 ~/GameAgentKit/gamekit.py doctor --agents all
```

### Optional: append enhancement references inside your existing Oil UI Skill

If you want the original `oil-ui/SKILL.md` to point directly to the extended prompts (rather than relying on agent discovery of the companion skill), **explicitly opt in**. This changes your local original Skill, so a backup is created and the action is idempotent. It does not copy any Pro content:

```bash
python3 ~/GameAgentKit/gamekit.py extend-oil-ui --source "$HOME/.claude/skills/oil-ui" --dry-run
python3 ~/GameAgentKit/gamekit.py extend-oil-ui --source "$HOME/.claude/skills/oil-ui"
```

The existing Oil UI file is not modified by normal install/link/register commands. If a future Oil UI update replaces its SKILL.md, rerun the opt-in extension after reviewing compatibility.

## Quick links

- [`QUICKSTART.md`](QUICKSTART.md): exact install/upgrade commands.
- [`docs/DRUI_USAGE.md`](docs/DRUI_USAGE.md): formal name, triggers, 20 independently runnable workflows, features, limits.
- [`prompts/drui/stages/`](prompts/drui/stages/): per-stage ready-to-paste prompts.

## V1.3 rename / DRUI upgrade notes

`drui` is the **one portable orchestrator Skill** containing the complete 20-workflow UI review system; `oil-ui-plus` is its separately named, bundled Pro-like methodology Skill. Do not install a second copy named `ui-studio` or `oil-ui-enhanced-review`. The owner's existing `oil-ui` is a distinct, optional Skill and must not be renamed, modified, or removed during normal install.

From v1.2, after `upgrade`, run `migrate-drui --dry-run`, then `migrate-drui` and `link --agents all`. Migration archives the old packaged skill and removes only verified kit-owned old-name symlinks; it preserves unknown files, copies and independent skills. To refresh a previously attached project, add `--project /path/to/game` to `migrate-drui`; only managed instruction blocks are rewritten with backups. If the optional original `oil-ui` was previously extended, opt in to `extend-oil-ui --source /original/oil-ui --refresh` (backed up first).

For the stage list, run `python3 ~/GameAgentKit/gamekit.py workflow list`. For an agent prompt, run `python3 ~/GameAgentKit/gamekit.py workflow prompt --stage visual-review`. The latter prints a prompt, not an automatic execution. Full guide: `docs/DRUI_USAGE.md`.


## V1.4: Strict reviewer workflows (Tech Lead, PM, User)

`drui` remains **one Skill**, now with **20 individually invokable workflows** (15 existing + 5 new). The existing `oil-ui` is optional and never overwritten; bundled `oil-ui-plus` does not replace purchased `oil-ui-pro`.

| Workflow | What it does | Changes code? |
|---|---|---|
| `review-tl` | Tech Lead architecture/correctness/performance/maintenance/integration audit | No |
| `review-pm` | PM product value, first-use, flow, scope, progression and acceptance | No |
| `review-user` | User-perspective hands-on task walk-through, discoverability and feedback | No |
| `review-triad` | Run three role audits in separate contexts, compare findings and gate acceptance | No |
| `review-loop` | Three roles review → separate implementer fixes → replay and re-review | Yes, implementation phase only |

**Use in any connected Agent chat:** `Use drui. Stage: review-triad. Audit this game with independent Tech Lead, PM and User reviewers; no changes.` For an implementation loop use `Stage: review-loop`.

```bash
python3 ~/GameAgentKit/gamekit.py workflow list
python3 ~/GameAgentKit/gamekit.py workflow prompt --stage review-tl
python3 ~/GameAgentKit/gamekit.py workflow prompt --stage review-pm
python3 ~/GameAgentKit/gamekit.py workflow prompt --stage review-user
python3 ~/GameAgentKit/gamekit.py workflow prompt --stage review-triad
python3 ~/GameAgentKit/gamekit.py workflow prompt --stage review-loop
```

Generate physically separated assignment files and empty report templates:

```bash
python3 ~/GameAgentKit/gamekit.py review prepare \
  --project "$PWD" --output "$PWD/drui-reviews/run-001"
# Open each PROMPT_<role>.md in three distinct fresh Agent sessions.
# After each report and runtime evidence is completed:
python3 ~/GameAgentKit/gamekit.py review evaluate --dir "$PWD/drui-reviews/run-001"
```

`review prepare` refuses to overwrite an existing output directory. `review evaluate` is strict about missing reports, sessions, screenshots/log paths, scores, open P0/P1s, and incomplete tests. **It checks existence/structure of evidence but cannot authenticate screenshots or truly prove reviewer isolation.** A single agent changing hats inside one session is PROVISIONAL, not three independent reviewers. Explicit real device verification is necessary for a release recommendation.

See [`docs/DRUI_STRICT_REVIEW_PROTOCOL.md`](docs/DRUI_STRICT_REVIEW_PROTOCOL.md) and [`docs/DRUI_REVIEW_REPORT_SCHEMA.md`](docs/DRUI_REVIEW_REPORT_SCHEMA.md).

## Public release verification

```bash
drui version
drui list --json
drui deps list
drui deps conflicts
drui deps lock   # run only after reviewing installed external Skills
drui deps check
# Configure the trusted update source explicitly; this checks metadata only:
drui update --repo zhenv5/drui --check
# When a newer release is available, after reviewing publisher and release notes:
drui update --repo zhenv5/drui --yes
```

`drui deps lock` records a local baseline only and does not constitute security approval. A project-local Skill can shadow a global one; `drui deps conflicts --project /path/to/game` is advisory and cannot guarantee Agent runtime loading order.
