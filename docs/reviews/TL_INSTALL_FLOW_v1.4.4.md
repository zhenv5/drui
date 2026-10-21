# DRUI v1.4.4 — Tech Lead 视角审查

**范围与限制：** 本次由同一助手先从 Tech Lead 角度独立形成检查项、再与新手视角对照；不是另一名人类或真正隔离会话。审查对象为 GitHub v1.4.3 的 CLI、安装、Skill 链接验证、更新和现有回归测试。测试结果以此 PR GitHub Actions 为准，不声称在真实 Mac 的四个 Agent 内加载通过。

| ID | 严重度 | 源码事实/影响 | 处理 |
|---|---|---|---|
| TL-01 | P1 | `cmd_install` 和 `cmd_link` 在末尾执行 `installation_report`，但此前未使用结果决定退出码。用户自有同名 Skill 被保护、`verify` 失败后，自动化仍可能把 exit 0 当成功 | 非 dry-run 下读取 `summary.complete`，失败返回非零码，已有用户文件不变 |
| TL-02 | P1 | `args_agents('all')` 只展开 3 个 Agent；`drui verify` 默认检查 4 个。默认 `install.sh` 和 `verify` 范围不一致 | `all` 统一覆盖 Codex/Claude Code/Antigravity/Cursor，共 5 个目录、12 × 5 = 60 Skill 链接 |
| TL-03 | P1 测试 | 旧测试曾把覆盖保护时的成功退出码当正常，因此阻碍修复 | 回归测试改为同时要求非零退出码 + 用户文件保持不变；新增 `all` 与默认 `verify` 一致性测试 |
| TL-04 | P2 | README/Quickstart/使用手册/Agent Prompt 仍描述旧失败行为，用户容易误用 | 新手首用步骤、单 Agent 安装范围和最终验收文字一致化 |
| TL-05 | P2 | `drui start` 入门主路径直接推荐 `review-loop`（可改文件），不适合作为第一个无风险任务 | 先推荐只读 `usability-review`，明确 `review-loop` 属进阶 |

## 检查方法与结论

- 代码审查：源文件 `gamekit.py`、`scripts/drui`、`scripts/verify_install.py`；仔细区分 `install/link/verify` 的范围和退出码。
- 不触碰第三方 Skill，不自动移除同名占位；只有本地文件和链接通过才输出安装 PASS。
- 维护 `--verbose`、`--json` 细节路径，正常验证仍保持一行。单 Agent 安装必须用对应 `verify --agents <name>`。
- 继续验证 GitHub-tag Source-only 安装、20 个 Workflows、12 个 Skills、完整回归和文档一致性。
- **仍未完成：** 真正独立 Agent 会话和 macOS 四工具真实加载测试、发布者签名证明、断电中断原子更新。本轮不能因此声称完全生产级运行验证。

CI 全绿且 Release 发布成功后，这轮代码与文档修改可标记完成。
