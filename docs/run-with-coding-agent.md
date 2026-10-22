# Run CivicFund Radar With Claude Code or Codex

This page is for people who want a coding assistant to run CivicFund Radar for
them. You are using the product; you are not contributing to the repo.

Paste the block below into Claude Code, Codex, or another coding agent. The
agent will install the local CLI, run the OpenProse CivicFund Radar example, and
return a source-cited funding report.

Before you start, have a paragraph ready that describes the research lab,
startup, nonprofit team, or technical project you want funding for. CivicFund Radar
is currently U.S.-focused and does not apply to grants, email sponsors, or
submit anything on your behalf.

## Copy-Paste Prompt

````markdown
You are helping me run OpenProse CivicFund Radar as a product user.

My goal is to get a source-cited report of non-dilutive funding opportunities
for my research lab, startup, or project. I am not asking you to contribute code
to the repo.

Follow these rules:

- Use the public `openprose/civicfund-radar` repo.
- Do not add API keys or paid services.
- Do not wire Exa, SAM.gov, browser automation, OpenAI, Anthropic, Stripe, or
  any other paid or keyed service into CivicFund Radar retrieval.
- Do not put an LLM inside the Go CLI.
- Treat the CLI as deterministic retrieval and provenance machinery.
- Use the OpenProse agent layer to judge fit and write the final report.
- If there are no credible matches, say that directly. Do not force weak
  recommendations.
- Do not apply, email, submit, register, purchase, or mutate any upstream
  service.

First, check prerequisites:

```bash
command -v git
command -v go
command -v prose
```

If any of those are missing, stop and tell me exactly which prerequisite is
missing. Do not fake a report.

Then clone or update CivicFund Radar:

```bash
WORKDIR="${HOME}/openprose-civicfund-radar-run"
mkdir -p "$WORKDIR"
cd "$WORKDIR"

if [ -d civicfund-radar/.git ]; then
  cd civicfund-radar
  git pull --ff-only
else
  git clone https://github.com/openprose/civicfund-radar.git
  cd civicfund-radar
fi
```

Build the CLI from this clone and make sure this exact binary is used:

```bash
mkdir -p "$HOME/.local/bin"
cd "$WORKDIR/civicfund-radar/cli/civicfund-radar"
go build -o "$HOME/.local/bin/civicfund-radar" ./cmd/civicfund-radar
export PATH="$HOME/.local/bin:$PATH"
civicfund-radar version
```

Install the host-harness skill for whichever agent harness is available. Do not
overwrite an existing custom skill directory; if a path already exists and is
not a symlink, stop and tell me. Rerun this step after every `git pull`; it is
meant to refresh stale symlinks that point at an older checkout.

```bash
cd "$WORKDIR/civicfund-radar"

install_skill_link() {
  skills_dir="$1"
  target="$skills_dir/civicfund-radar"
  mkdir -p "$skills_dir"
  if [ -e "$target" ] && [ ! -L "$target" ]; then
    echo "Existing non-symlink skill path: $target"
    echo "Leaving it untouched. Ask me before changing it."
    return 1
  fi
  ln -sfn "$PWD/skills/civicfund-radar" "$target"
}

install_skill_link "$HOME/.claude/skills" || exit 1
install_skill_link "$HOME/.codex/skills" || exit 1
install_skill_link "$HOME/.agents/skills" || exit 1
```

Now get my brief:

- If I included a research-lab, startup, nonprofit, or project brief in this chat, save it to
  `$WORKDIR/funding-brief.txt`.
- If I did not include a brief, ask me for one before running anything else.

Run the OpenProse CivicFund Radar example from the repo root:

```bash
cd "$WORKDIR/civicfund-radar"

PROSE_CODEX_SANDBOX_MODE=workspace-write \
PROSE_CODEX_APPROVAL_POLICY=never \
PROSE_CODEX_ADD_DIR="$HOME/.local/share/civicfund-radar" \
PROSE_CODEX_NETWORK=true \
CIVICFUND_RADAR_BIN="$HOME/.local/bin/civicfund-radar" \
prose run examples/openprose/src/civicfund-radar.prose.md \
  --startup_brief "$(cat "$WORKDIR/funding-brief.txt")"
```

If that fails only because the installed `prose` version does not support the
granular sandbox env vars, retry once with the broader fallback:

```bash
cd "$WORKDIR/civicfund-radar"

PROSE_CODEX_SANDBOX_MODE=danger-full-access \
PROSE_CODEX_APPROVAL_POLICY=never \
CIVICFUND_RADAR_BIN="$HOME/.local/bin/civicfund-radar" \
prose run examples/openprose/src/civicfund-radar.prose.md \
  --startup_brief "$(cat "$WORKDIR/funding-brief.txt")"
```

When the run finishes, show me:

- the final Markdown report
- where the run artifacts were written
- any credible matches and any rejected weak matches
- any important caveats about source coverage or freshness

Do not summarize unsupported opportunities as good fits. Every recommended
opportunity must have source evidence from the run.
````

## What The Agent Should Return

A good final response from the coding assistant should include the Markdown
funding report, the run path, and a short note about confidence and gaps. If
the report has no credible current opportunities, that is a valid result.

If the agent reports missing prerequisites, install those first and run the same
prompt again.
