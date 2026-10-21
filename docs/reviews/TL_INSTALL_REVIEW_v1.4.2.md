# Tech Lead 审查记录：DRUI GitHub 安装与短验证（v1.4.2）

**审查身份：** 本对话中单独从 Tech Lead 视角进行的只读源码与文档审查，随后实施修复。并非独立人类审查员或隔离的第二个 Agent 会话；不声称在用户的 Mac/Codex/Claude/Antigravity/Cursor 内进行了真实运行。

## 检查范围

- README、QUICKSTART、SECURITY、命令手册、MAINTENANCE、安装/更新 Agent Prompts
- install.sh、gamekit.py 的 install/link/verify、scripts/verify_install.py、scripts/github_update.py
- GitHub Source-only 发布与 tests/smoke_git_install.sh

## 初审发现及修复

| ID | 优先级 | 证据与问题 | 修复与验收 |
|---|---|---|---|
| TL-01 | P1 | README 与 Quickstart 的安装失败分支以 tail 为最后命令，可能将真实安装失败误报为成功 | 失败分支明确返回非零；测试三个文档的成功、安装失败、verify 失败路径 |
| TL-02 | P1 | SECURITY 仍描述 ZIP/SHA-256 验证流程，而实际升级已改为 Git Source Tag | 重写安全模型，明确 official origin、Tag、干净 Git tree、信任边界 |
| TL-03 | P1 | gamekit.py cmd_install/provision 保留同名用户 Skill 并可能返回 0，实际未必链接完整 | 强制手动和 Agent 流程最后运行 drui verify 并检查退出码；不覆盖外部 Skills |
| TL-04 | P2 | User Manual 仍展示 v1.3.0 旧路径与迁移主流程 | 统一为 v1.4.2 Git 安装与权威操作手册 |
| TL-05 | P2 | 4 Agents / 5 目录 / 60 链接、旧 --agents all 不含 Cursor 容易混淆 | 在安装、命令、维护文档中明确说明，保留详细与 JSON 模式 |
| TL-06 | P2 | 未建立 deps fingerprint lock 时 deps check 会失败，但不代表 DRUI 安装失败 | 修改 Prompt 与指南，不自动 lock / approve |
| TL-07 | P2 | 部分 docs 相对链接错误；安装说明重复且易漂移 | 统一 docs/INSTALL_AND_VERIFY.md，修正文档导航并测试一致性 |

## 第二轮复查标准

- GitHub CI 必须通过 Python 编译、全量 unittest、Git clone 安装冒烟与新增 shell 退出码测试；如失败不能宣称发布完成。
- drui verify PASS 只能说明本地链接、元数据及 CLI 状态正常，不是实际 Agent 发现、加载或执行成功。
- Git Tag / Object hash 不保证发布者身份；签名与供应链来源证明仍需单独建设。
- Git checkout 遇到断电/进程中止不是原子操作，可能需要人工恢复；不能用硬重置消除用户改动。
- 未更改第三方 Skill 或用户实际机器文件。
- 正常发布示例仅为预期格式，不代表用户本机成功。

**TL 结论：** 完成以上文档与测试修复后，可在 GitHub CI 全绿前提下接受文档/安装验收契约。跨 Agent 真正加载测试仍需在目标设备独立进行。
