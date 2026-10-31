#!/usr/bin/env bash
# land.sh — one-command landing for this repo.
#
#   tools/land.sh "Commit message"
#
# Commits the current feature branch, pushes it, opens a PR if needed, merges
# that PR, and fast-forwards the main worktree. Run it yourself — it is a
# deliberate, user-invoked action, not a background automation.
#
# Requires the GitHub CLI (`gh`) authenticated for this repo.
set -euo pipefail

command -v gh >/dev/null || { echo "error: gh CLI is required" >&2; exit 1; }
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || { echo "error: not a git repo" >&2; exit 1; }

repo_root=$(git rev-parse --show-toplevel)
cd "$repo_root"

branch=$(git rev-parse --abbrev-ref HEAD)
if [[ "$branch" == "main" || "$branch" == "master" ]]; then
  echo "error: refusing to land from $branch; create a feature branch first" >&2
  exit 1
fi

msg=${1:-"Update $(date '+%Y-%m-%d %H:%M')"}

git add -A
if git diff --cached --quiet; then
  echo "nothing to commit"
else
  git commit -m "$msg"
fi

git push -u origin "$branch"

pr=$(gh pr list --head "$branch" --state open --json number --jq '.[0].number // empty')
if [[ -z "$pr" ]]; then
  gh pr create --base main --head "$branch" --title "$msg" --body "Land $branch."
  pr=$(gh pr list --head "$branch" --state open --json number --jq '.[0].number')
fi

gh pr merge "$pr" --merge --delete-branch

# Fast-forward the main worktree (this works whether the script runs in the
# main checkout or in a linked worktree).
main_path=$(git worktree list --porcelain | awk '/^worktree /{p=$2} /^branch refs\/heads\/main$/{print p; exit}')
if [[ -n "${main_path:-}" ]]; then
  git -C "$main_path" switch main >/dev/null 2>&1 || true
  git -C "$main_path" pull --ff-only
else
  git switch main
  git pull --ff-only
fi

echo "landed $branch; main is up to date"
