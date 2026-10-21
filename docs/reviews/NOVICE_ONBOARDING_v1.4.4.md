# DRUI v1.4.4 — 新手用户视角审查

**角色说明：** 这是从“第一次使用 Coding Agent/不熟悉 DRUI”的新用户视角所做的情境走查；并非真实招募的独立用户可用性研究。先不把 TL 结论当用户答案，检查能否从 README 按步骤完成首次使用。

## 任务一：不懂 DRUI，能从哪里开始？

**原版卡点（P2）：** README 一开始是很长的安装 Prompt，没有三步导航，“复制给 Agent”和“在终端执行”分支不够清晰。**处理：** README 增加 `Start here`：有 Agent → 复制 Prompt；偏终端 → 点手动安装；安装后 → `verify`、`start`、只读 `usability-review`。

## 任务二：安装过程中报 `PASS/FAIL`，我能知道发生了什么吗？

**原版卡点（P1）：** 直接安装 `--agents all` 和默认验证对象不一致，且同名冲突跳过后安装命令可能返回 0。**处理：** `all` 现在是四 Agent，自动验证结束时失败返回非零；手动执行 `drui verify` 成功时一行，失败时至多 3 个具体问题。`--verbose` 查看全部详情。安装报错先看日志，不强制覆盖同名 Skill。

## 任务三：只有 Codex，没有装另外三种 Agent？

**原版卡点（P2）：** 默认 `drui verify` 仍检查四个，因此若安装只选择 Codex 会出现大量 `MISSING`。**处理：** 文档明确 `install.sh --agents codex` 对应 `drui verify --agents codex`。这两个命令范围应一致；不把“未选择的 Agent”当作失败。

## 任务四：安装完首次使用哪个功能？

**原版卡点（P2）：** 默认引导先看到 `review-loop`，它可以修源代码；首次使用更适合选择只读任务。**处理：** `drui start` 先推荐 `usability-review`；Agent 内示例指令明确 `Read-only; do not edit files`。终端打印 Prompt ≠ 自动执行任务。

## 用户预期验收

1. 从 README 两种入口能找到安装方式；`--agents all` 和默认四 Agent 验证一致。
2. 成功时只显示 `DRUI vX PASS | ... | runtime untested` 类短摘要，失败不会被终端的退出码误标记成功。
3. 安装仅一个 Agent 时提供对应范围的验证方法。
4. 第一次运行只读工作流，不意外修改项目。
5. 第三方用户文件仍保留；文件验证不能代表 Agent 真正加载。

**未实测内容：** 未进行真实新手访谈、计时观察、真实四 Agent 图形界面操作；上述属于基于源码、Prompt 和文档的模拟走查。
