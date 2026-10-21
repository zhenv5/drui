# DRUI 全量 Tech Lead 文档/发布复查（v1.4.3）

审查类型：在本对话中**单独从 Tech Lead 视角**审查公开仓库当前源码、文档及 CI 契约；随后提交修复并由 GitHub CI 复验。不是另一个独立人类/隔离 Agent 或用户机器上的实测。

## 审查范围与证据

- GitHub `main` 树中的 README、QUICKSTART、SECURITY、CONTRIBUTING、当前 docs、历史 changelogs、DRUI Skill 和 Agent 安装/升级 Prompt。
- `scripts/drui`、`gamekit.py` 已注册命令、Git-only updater、Skill 验证器与 `.github/workflows/` 发布方式；GitHub Tag/Release 与源码版本契约。
- 已存在的 CI 与本轮新增一致性回归测试（文档相对链接、克隆 Tag 版本、归档标题、自动 Release 来源）。

## 初审发现与处理

| ID | 严重度 | 发现 | 修复 |
|---|---|---|---|
| DOC-01 | P1 | 严苛评审速查表仍明确使用 `v1.3.0`，且 `--agents all` 会漏装 Cursor | 更新为已核对稳定 Tag 的 Git clone，显式四 Agent + `verify` 返回码 |
| DOC-02 | P1 | CONTRIBUTING 要求手动推 Tag，与 `publish.yml` 自动打 Tag 存在双重发布风险 | 明确只能由 CI 自动打 Tag 和发布，不移动已发布 Tag，并给出维护清单 |
| DOC-03 | P1 | 旧 `publish-v1.0.0.yml` 仍可手动触发 ZIP 发布，违反现行 Git-source-only 规范 | 从当前代码树移除废弃工作流；不篡改历史 v1.0.0 Tag/Release |
| DOC-04 | P2 | 内部 GameAgentKit V1.4/1.5/1.7/1.8 标注与 DRUI 公共 SemVer 容易混淆 | 当前手册/Skill 去除历史版本作为现行标题，历史 changelog 标注 ARCHIVED |
| DOC-05 | P2 | README 把 Git Tag 称为 `immutable`，表述强于实际保障 | 改为 reviewed stable Tag，强调由管理员控制，升级前审查提交差异 |
| DOC-06 | P2 | 第三方策略仍标题 `public v1.0.0`，`deps check` 无锁的意义不明确 | 改为现行策略、说明 opt-in lock、无 baseline 不等于安装失败 |
| DOC-07 | P2 | 多处文档对首次安装、四 Agent 的范围、版本示例与路径说明不一致 | 更新 README、Quickstart、评审速查、使用手册、安装指南和第三方说明 |
| DOC-08 | P2 | 公开文档更新缺少通用静态核对，容易再次留下错误链接或旧 Clone Tag | 新增 documentation consistency tests（本地 Markdown 链接、Tag、发布工作流、归档标注） |

## 回归与验收

- 在 PR 上运行 Python 编译、全量 unittest、新文档契约测试及 `tests/smoke_git_install.sh`，CI 应全绿后方可合并发布。
- 仅把 GitHub Source Tag/Commit 作为来源可追溯性，**不冒充签名供应链证明**。
- `drui verify` 文件/链接检查正确也**不能证明真实 Codex/Claude Code/Antigravity/Cursor 已加载**。
- Git checkout 不是中断原子事务。保留用户自有 Skill，不进行隐式安装或升级第三方依赖。
- 归档 docs 只标明历史含义，不改写原始历史变更内容；历史 Release 不删除。

**结论（以 GitHub CI 为最终代码门槛）：** 更新后当前用户/维护者文档形成统一 Git-first 工作流。真实 Agent 加载与发布者签名验证仍须后续独立验收。
