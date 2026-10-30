# SESSION-HANDOFF: atlr.pro (Atelier Superintelligence site)

Updated 30 Oct 2026, late afternoon, the day of the TiECon Canada 2026 keynote.

## Canonical artifacts (edit these, nothing else)

| Artifact | Where | Notes |
|---|---|---|
| Site source | `src/` (layout.html, css/site.css, js/site.js, pages/*.html, assets/img) | Pages carry a `<!--meta {...}-->` header read by build.py |
| Build script | `build.py` | Commands in the docstring; no defaults, pass `--base --origin --out` |
| Live output | `docs/` on `main` (GitHub Pages main:/docs, CNAME atlr.pro) | TODAY this holds the **temp site** (the v7 deck), not a build of src/ |
| Staging output | `../atlr-staging/` (repo atlr-frge/atlr-staging, Pages from main root) | https://atlr-frge.github.io/atlr-staging/ (noindex, robots Disallow) |
| Holding page | `src/static/holding/index.html` (served at /holding/) | The one-screen page from the first hour; kept for the record |
| Brand source | `~/workspace/atelier-intro-v7/index.html` | site.css is a port of its stylesheet plus additions |
| Copy gate | `~/workspace/atelier-doc-system/skills/atelier-proposal/scripts/slop-gate.py` | Run on extracted copy (see Process) |

## State

- **DNS:** atlr.pro points at GitHub Pages (A 185.199.108/109/110/111.153, www CNAME atlr-frge.github.io), changed in GoDaddy at about 16:00 ET on 30 Oct with Michael's go. MX, SPF, DMARC, DKIM, site-verification TXT untouched. Authoritative and public resolvers confirmed within minutes.
- **HTTPS:** GitHub's certificate was still `null` at 16:25 ET. A background monitor (scratchpad `dns-monitor.sh`) polls every two minutes, nudges the custom-domain setting, and sets `https_enforced` once the certificate is approved. If a new session finds `gh api repos/atlr-frge/atlr-site/pages --jq .https_certificate.state` still null hours later, remove and re-add the custom domain (`PUT .../pages -f cname=`, then `-f cname=atlr.pro`) and pull main afterwards, since GitHub commits the CNAME file.
- **What visitors see now:** the Intro v7 deck as a one-page temp site (Michael's call). Fixes applied from the deck source: headshots copied into the repo, the two 19 MB swarm PNGs cut to 2048px WebP, placeholder client logo strip removed, em dashes removed, fold dev marker hidden, Materiality in the nav, hello@/Materiality/LinkedIn in the footer, canonical/OG/JSON-LD added.
- **Full site:** built and staged. Six pages: / (deck spine refreshed, plus five controls, selected work, team, Materiality), /work/ (seventeen systems with build states and a state key, Conformer and Conduit, controls), /method/ (Sprint, Learn/Build/Prove/Stay, how it thinks), /team/ (long bios), /materiality/ (episodes 01 to 04 with LinkedIn links, the word, how it is made, disclaimer), /contact/ (Sprint-first, mailto), 404.
- **Copy gate:** all six pages pass slop-gate.py; the only hit is the kill-list word "bespoke", which is the brand positioning line and is the accepted exception. A fresh doc-critic agent graded the copy the same afternoon; apply any rewrites it returned before the flip.
- **Rendering QA:** desktop (1440) checked page by page in Chrome. Phone width is checked through `_mobile.html` (an iframe harness in the preview build) because the Chrome extension would not shrink the window below desktop width.

## Source material and what the site may and may not say

- `~/Desktop/ATELIER-SET-v001-2026-10-23`: the Triyo and Accenture decks, the two founder dossiers, the Song deck. Confidential pursuit material. The site uses the capability wording, the five controls, the selected-work list and the Oct 2026 bios from it, and never names Accenture or TRIYO. The compliance platform is "a Canadian compliance platform"; the FOX series is "a US network series" (show in production).
- Named on the site because the work is public: Warner Music / Daniel Lanois (Belladonna Nocturne released; tour films delivered), Design Exchange Toronto (Athena installed), Amazon Prime (No Dress Rehearsal), Kawartha Dairy. **Sean to confirm** each client name may appear publicly.
- Build-state vocabulary (live / delivered / released / demo environment / tested / built) follows the Accenture deck's legend; nothing is called live.
- Bio rules from `~/.claude/CLAUDE.md` applied: Nvidia work is "developed", Kognitiv raise figure omitted (the $500M caveat), LifeLabs not named, "7 companies" and "MIT" from the old deck bio dropped (not in the bio facts).

## Open decisions for Sean and Michael

1. Client naming on /work/ and the home page (see above).
2. Sean's No Dress Rehearsal credit: the v7 deck says executive produced, the Song deck says Animation Director; the site says both.
3. The deck's "vs. consultancies / platforms / automation / dev shops" table is kept on the home page; the taste rules would drop it.
4. Contact is mailto only. A FormSubmit form (as on aiimaginelabs) needs Michael to click the activation email for hello@atlr.pro.
5. Temp-site bio text still says "Built and exited 7 companies" and "MIT" (unchanged canonical deck copy) until the full site replaces it.

## Process (repeatable)

```
# staging
python3 build.py --base /atlr-staging --origin https://atlr-frge.github.io --staging --out ../atlr-staging
cd ../atlr-staging && git add -A . && git commit -m "Staging rebuild" && <token-dance push to atlr-frge/atlr-staging>

# copy gate (extract then gate; extractor lives in the session scratchpad, re-create from the handoff if missing:
# headings/labels -> "# " lines, paragraphs -> text, then slop-gate.py per page)

# the flip, only after Sean signs off
python3 build.py --base "" --origin https://atlr.pro --cname atlr.pro --out docs
git add docs && git commit -m "Production build for atlr.pro" && <token-dance push>
curl -sI https://atlr.pro/ | head -3
```

Token dance: `TOKEN=$(gh auth token); git push "https://x-access-token:${TOKEN}@github.com/atlr-frge/<repo>.git" main` (the token never enters .git/config this way).

## Next

- Read the critic's report, apply rewrites, rebuild staging, re-run the gate.
- WhatsApp note to Sean with the staging URL and the five open decisions (sean-note skill).
- After sign-off: the flip (above), then `site-qa` on https://atlr.pro, then update `~/.claude/CLAUDE.md` canonical table (live column) and the `atelier-site` memory.
- Later: OG image with the wordmark (today's og-default.jpg is a brand-safe crop with no text), a contact form, and the aiimaginelabs links to the Atelier deck that should now point at https://atlr.pro (noted in the aiimaginelabs handoff).
