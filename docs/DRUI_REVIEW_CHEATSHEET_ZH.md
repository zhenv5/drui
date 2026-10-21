# DRUI 严苛 TL / PM / 用户独立评审速查（当前通用流程）

**只有一个 Skill：`drui`**。旧有 15 个工作流保留，新增 5 个严苛评审工作流，合计 20 个。你的开源 `oil-ui` 是可选原始 Skill；如已安装，DRUI 会要求 Agent 参考它，但不解锁 Oil UI Pro。

## 直接在 Codex / Claude Code / Antigravity 对话触发

### 1. 单独技术负责人审查（只审查，不改源码）

> 使用 `drui`，执行 `review-tl`。以严苛 Tech Lead 审查当前项目的真实源码、界面、状态机、性能和风险。给出 P0/P1/P2/P3 问题、复现步骤、文件位置、证据和五维评分。不要修改代码；没有运行证据明确标记 BLOCKED。

### 2. 单独 PM 审查（只审查）

> 使用 `drui`，执行 `review-pm`。独立从 PM 视角评审价值、主任务流程、引导、难度/奖励、功能范围、体验一致性与上线门槛；按用户影响排优先级，给出可验收的修复标准。不要修改代码，不要提前读取其他角色的审查结论。

### 3. 单独用户视角审查（只审查）

> 使用 `drui`，执行 `review-user`。不要先看开发说明，模拟一个首次使用的新用户，在真实 iPhone 模拟器/设备上从首页完成一轮核心任务。记录每一步点击、迟疑、误触、失败恢复、反馈和截图，对可发现性、触控、反馈、信任和乐趣逐项评分；不改代码。缺少设备时标记 BLOCKED，不要伪装做过真实用户测试。

### 4. 一键三方独立审查（只审查）

> 使用 `drui`，执行 `review-triad`。启动三个隔离的评审 Agent / 全新会话，分别做 Tech Lead、PM、用户视角独立审查。三份结论完成前互不读取；完成后合并去重、列出分歧与证据、P0/P1 阻塞项和整改优先级。使用报告验收工具确认，不改源码。若无法真正隔离会话，只能报告 PROVISIONAL。

### 5. 三方评审 → 修复 → 重审（允许修复真实源码）

> 使用 `drui`，执行 `review-loop`。先独立做 TL/PM/用户三方只读评审；合并 P0/P1 并由单独实现角色按优先级修复实际源码。随后重新编译、运行完整用户任务、留新截图，再发起独立复审。最多三轮。三方各 >=9/10、单维 >=8、无未验收 P0/P1 才能考虑通过；否则如实报告阻塞，禁止虚构测试或自评 9.5。

## 命令行直接生成 Prompt

```bash
python3 ~/GameAgentKit/gamekit.py workflow list
python3 ~/GameAgentKit/gamekit.py workflow prompt --stage review-tl
python3 ~/GameAgentKit/gamekit.py workflow prompt --stage review-pm
python3 ~/GameAgentKit/gamekit.py workflow prompt --stage review-user
python3 ~/GameAgentKit/gamekit.py workflow prompt --stage review-triad
python3 ~/GameAgentKit/gamekit.py workflow prompt --stage review-loop
```

`workflow prompt` **只输出可复制给 Agent 的指令**，不会主动运行 Agent。

## 生成三份隔离的 Agent 审查任务

在当前游戏 repo 根目录执行：

```bash
python3 ~/GameAgentKit/gamekit.py review prepare \
  --project "$PWD" \
  --output "$PWD/drui-reviews/run-001"
```

会创建 `PROMPT_tech-lead.md`、`PROMPT_product-manager.md`、`PROMPT_end-user.md`、三份空白 JSON 报告和 `evidence/`。分别把三份 Prompt 交给隔离的 Agent 会话。报告完成后：

```bash
python3 ~/GameAgentKit/gamekit.py review evaluate \
  --dir "$PWD/drui-reviews/run-001"
```

**注意**：评分工具验证报告字段、证据文件是否存在及阻塞问题状态，不具备判定截图真实性、Agent 实际是否使用隔离会话或真实人类用户参与的能力。它通过并非真正的产品上线认证。

## GitHub 源码安装与验证

始终参考 [统一安装与验证手册](INSTALL_AND_VERIFY.md) 以及 [最新稳定 Release](https://github.com/zhenv5/drui/releases/latest)，不要复用旧版本号或 ZIP 安装说明。首次安装从已核对的稳定 Tag 克隆（当前文档示例：`v1.4.5`）：

```bash
git clone --depth 1 --branch v1.4.5 https://github.com/zhenv5/drui.git "$HOME/GameAgentKit"
bash "$HOME/GameAgentKit/install.sh" --agents codex,claude,antigravity,cursor --dry-run
bash "$HOME/GameAgentKit/install.sh" --agents codex,claude,antigravity,cursor
"$HOME/GameAgentKit/scripts/drui" verify   # 必须为退出码 0
```

完整四 Agent 共 5 个目录、预期 60 个内置 Skill 链接；`--agents all` 已统一包含 Cursor。安装器会保留同名用户 Skill，并在最终验证失败时返回非零码；**仍必须检查 verify 退出码**。默认只输出一行结果；用 `--verbose` 查看完整名称、版本和冲突。验证通过仅代表本地文件正确，不能代替在真实 Agent 内完成实际加载测试。
