# Optional upstream skills and MCPs

This package works **offline** with original bundled `SKILL.md` files. It never downloads or executes third-party content automatically.

Optional upstream skills you may investigate:
- [game-ui-design](https://github.com/omer-metin/skills-for-antigravity) — general game UI craft.
- [game-ui-ux, game-feel, game assets](https://github.com/gamedev-skills/awesome-gamedev-agent-skills) — cross-engine interaction and feedback patterns.
- [SwiftUI Pro](https://github.com/twostraws/SwiftUI-Agent-Skill) — native iOS conventions.
- [iOS Simulator Skill](https://github.com/conorluddy/ios-simulator-skill) — Mac UI automation; needs separate setup.
- [OpenAI develop-web-game](https://github.com/openai/skills) — browser-game development + Playwright testing.

To install third-party skills globally via the separate skills.sh CLI, **review their code** first and run e.g.:
```
npx skills add gamedev-skills/awesome-gamedev-agent-skills \
  --skill game-ui-ux --skill game-feel -g -a codex -a claude-code -a antigravity
```
This uses that CLI's own global installation paths, not this pack's canonical root. Keep independent third-party Skills **outside** `~/GameAgentKit/skills/` (reserved for bundled, release-managed Skills). Once you have checked ownership, permissions, license and compatibility, use `register-external --name <skill-name> --source /your/owned/skill/directory --agents all`. This links only into vacant slots and never copies or upgrades user-owned Skills. See `docs/EXTERNAL_SKILL_UPDATES.md`. Do not copy files you lack rights to redistribute.

Optional tool servers like Comfy MCP, Loopcut, or Blender integrations are **not skills**. Configure them separately for each agent; connecting a skill doesn't provide a remote model, account, token or GPU.
