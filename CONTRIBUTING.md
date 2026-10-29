# Contributing to Founder's Way

Thanks for helping! The game is shaped by its players, and you don't need to code to take part.

## Ideas and votes
1. Search the issues first. If the idea already exists, give it a 👍 instead of opening a new one.
2. Otherwise open a **Feature request**. Explain the problem you want solved, not only the solution.
3. Ideas tagged `accepted` go into the roadmap. Ideas tagged `wontfix` don't fit the vision of the game (realistic, educational, no pay-to-win).

## Code contributions
1. **Open or comment on an issue first** and wait for a 👍 from the maintainer before you start big changes. PRs without a linked issue may be closed.
2. Fork the repo and create a branch from `main`.
3. Keep PRs small: one feature or fix per PR.
4. Run the smoke test before you push:
   ```
   npm install
   npx playwright install chromium
   npm test
   ```
5. Open the PR using the template and tick the contributor agreement.

### What gets merged
- Every PR is reviewed by the maintainer. **Nothing reaches `main` without approval and a passing test run.**
- In-game text is in English. New strings must work with the translator (see `// @@I18N-START`).
- No new external dependencies, trackers, ads or network calls without discussion.
- Balance changes need a reason (data, a source or a playtest).

### Automatic safety check
Every PR runs a safety check (`guard`) that must pass before it can be merged. It is a plain script, not an AI, so text in a PR cannot change its result. A PR may only change `index.html`, images in `media/` and documentation files. It is blocked if the new code adds:
- network calls, new `<script>`/`<iframe>` tags or links to unknown sites;
- dynamic code (`eval`, `new Function`…), calls built from strings, or obfuscated text;
- invisible or direction-changing Unicode characters;
- instructions aimed at an AI reviewer;
- edits to the security header or the pinned three.js script.

If you need one of these for a good reason, open an issue first and explain it.

### What gets closed
- Joke, offensive or off-topic content.
- Changes to the license, credits, trademark files or CI.
- Large rewrites nobody asked for.

## Contributor License Agreement
By opening a pull request you agree to the [CLA](CLA.md). In short: you keep the copyright of your work, and you allow the maintainer to distribute it under the AGPL-3.0 **and** under other licenses (for example, a store version of the game).

## Code of conduct
Be respectful. See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
