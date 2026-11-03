# X4 Pro native UI source candidate (archived, unverified)

**Reference only. Not a flashable firmware release and not applied to shipped C++ sources.**

This is the combined ChatGPT Home + Library + Reading Settings source candidate prepared November 3, 2026 against `develop` commit `a93303a210fbc40f99a92be33b17974fe70c31ae`. It includes source-transform scripts, tests, build scripts, a device checklist, and detailed README (13 files total). Its source changes target seven existing C++ files, but **none are modified on this branch**.

## Obtain the complete source package

The archive is stored here as five sequential binary parts to keep it separate from firmware/build files. From the `research/fork-ui-reading/x4pro-native-ui-source/` folder:

```sh
cat source.part-* > candidate.tar.xz
```

```sh
sha256sum candidate.tar.xz
```

Expected SHA-256: `a4ec9ea543b5dfa7e78d19c9e2b8158921dd5de9e177d4bae9b76632d65e6758`.

```sh
mkdir -p candidate && tar -xJf candidate.tar.xz -C candidate
```

Read `candidate/README.md` before applying anything. The default application workflow refuses an altered checkout, and no script should flash the X4 Pro automatically.

## Coordination and limitations

- This archive implements a three-screen pilot using the existing Cover Grid theme, **not** the full seven-screen **Paper** theme accepted on `feat/x4pro-paper-ui`.
- The Paper theme branch is owned by a separate agent; **do not merge this candidate blindly** into that branch. Reuse carefully reviewed approaches (recent-book data, library paging, font steppers) rather than two competing implementations.
- 23 local source/fixture tests passed on the archived candidate. The actual `default` and `x4pro` firmware builds, formatter, four independent firmware reviews, and physical X4 Pro tests **have not been completed**.
- This branch carries the source package for collaboration only. It does not affect `develop`, build targets, OTA, or installed devices.
- Firmware changes must still satisfy `AGENTS.md` and `.agents/skills/firmware-handoff/SKILL.md` before any firmware commit.

Project repo: `BigCatMellow/crosspoint-reader`.