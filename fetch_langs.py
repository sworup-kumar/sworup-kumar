#!/usr/bin/env python3
"""Aggregate language bytes across the user's owned repos -> langs.json.

Data source:
  - If GH_PAT is set (a personal access token with `repo` scope), reads the
    authenticated user's repos INCLUDING private ones (/user/repos).
  - Otherwise reads only PUBLIC repos (/users/<user>/repos).

The profile repo itself (name == GH_USER) is excluded so build.py's own
Python file doesn't pollute the stats. Writes langs.json only if there is
real data; otherwise leaves the curated fallback in build.py in place.
"""
import os, json, urllib.request

USER = os.environ.get("GH_USER", "sworup-kumar")
PAT = os.environ.get("GH_PAT") or ""            # optional: unlocks private repos
TOKEN = PAT or os.environ.get("GITHUB_TOKEN")   # for rate limit / auth
TOP_N = 6
HERE = os.path.dirname(os.path.abspath(__file__))

def api(url):
    req = urllib.request.Request(url)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", f"{USER}-profile-langs")
    if TOKEN:
        req.add_header("Authorization", f"Bearer {TOKEN}")
    with urllib.request.urlopen(req) as r:
        return json.load(r)

def list_repos():
    repos, page = [], 1
    while True:
        if PAT:
            url = f"https://api.github.com/user/repos?per_page=100&affiliation=owner&visibility=all&page={page}"
        else:
            url = f"https://api.github.com/users/{USER}/repos?per_page=100&type=owner&page={page}"
        batch = api(url)
        repos += batch
        if len(batch) < 100:
            return repos
        page += 1

def main():
    totals = {}
    for repo in list_repos():
        if repo.get("fork"):
            continue
        if repo["name"].lower() == USER.lower():   # skip the profile repo
            continue
        for lang, size in api(repo["languages_url"]).items():
            totals[lang] = totals.get(lang, 0) + size

    total = sum(totals.values())
    if total == 0:
        print("no language data found; keeping curated fallback")
        return

    top = sorted(totals.items(), key=lambda kv: -kv[1])[:TOP_N]
    out = [[name, max(round(size / total * 100), 1)] for name, size in top]
    with open(os.path.join(HERE, "langs.json"), "w") as f:
        json.dump(out, f, indent=2)
    print("wrote langs.json:", out)

if __name__ == "__main__":
    main()
