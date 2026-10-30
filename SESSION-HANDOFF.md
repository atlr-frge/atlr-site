# SESSION-HANDOFF: atlr.pro (Atelier Superintelligence site)

Updated 30 Oct 2026, evening, the day of the TiECon Canada 2026 keynote. Second pass of the day: a full audit of the staged site from the buyer, investor and partner seats, with the fixes applied and pushed to staging.

## Canonical artifacts (edit these, nothing else)

| Artifact | Where | Notes |
|---|---|---|
| Site source | `src/` (layout.html, css/site.css, js/site.js, pages/*.html, assets/img, assets/fonts) | Pages carry a `<!--meta {...}-->` header read by build.py; `preload` in the meta adds image preloads |
| Build script | `build.py` | Commands in the docstring; no defaults, pass `--base --origin --out` |
| Live output | `docs/` on `main` (GitHub Pages main:/docs, CNAME atlr.pro) | TODAY this holds the **temp site** (the v7 deck), not a build of src/ |
| Staging output | `../atlr-staging/` (repo atlr-frge/atlr-staging, Pages from main root) | https://atlr-frge.github.io/atlr-staging/ (noindex, robots Disallow) |
| Holding page | `src/static/holding/index.html` (served at /holding/) | The one-screen page from the first hour; kept for the record |
| Brand source | `~/workspace/atelier-intro-v7/index.html` | site.css is a port of its stylesheet plus additions |
| Copy gate | `~/workspace/atelier-doc-system/skills/atelier-proposal/scripts/slop-gate.py` | Run on extracted copy (see Process) |
| Fonts | `src/assets/fonts/*.woff2` + `fonts.css` (latin subsets, OFL) | Self-hosted; the @font-face rules are prepended to site.css. No Google Fonts request remains. |

## State

- **DNS:** atlr.pro points at GitHub Pages (A 185.199.108/109/110/111.153, www CNAME atlr-frge.github.io), changed in GoDaddy at about 16:00 ET on 30 Oct with Michael's go. MX, SPF, DMARC, DKIM, site-verification TXT untouched.
- **HTTPS:** live and enforced. GitHub's certificate needed a remove/re-add of the custom domain through the API (`PUT .../pages` with `{"cname":null}` then `{"cname":"atlr.pro"}`); it approved within a minute. GitHub committed "Delete CNAME" / "Create CNAME" on main during that nudge, so pull before pushing from another checkout.
- **What visitors see now:** the Intro v7 deck as a one-page temp site (Michael's call). Evening fix: the page had no og:image, so LinkedIn and WhatsApp previews of atlr.pro were bare on keynote day; `docs/images/og-default.jpg` and the tags were added (commit d596d12). Michael's deck bio line carried claims outside the bio facts ("Built and exited 7 companies", "Ran Deloitte's Novel & Exponential Tech group", "$500M", "MIT") and was replaced with the facts-only line used on the full site. Sean's deck line is his own wording and was left as is.
- **Full site, after the audit:** eight indexable pages: / (deck spine refreshed, Sprint defined under the hero, proof line beneath it, five controls, selected work, team, Materiality), /work/ (four number-led cards, seventeen systems in five groups with anchors, state key without "Live", Conformer and Conduit, controls), /method/, /team/ (long bios with receipts linked), /materiality/, /contact/ (Sprint checklist, NDA line, FormSubmit form, partner section), /trust/ (ten answers for a model-risk team), /privacy/; plus /thanks/ (noindex, the form's landing) and 404.
- **Copy gate:** all pages pass; the only hit is "bespoke" in the positioning line, the accepted exception.
- **Lighthouse (live staging, like for like, before → after):** home mobile 82 → 98 (LCP 4.6 s → 2.4 s), home desktop 97 → 99, work mobile 98 → 100; accessibility 96 → 100 on every page; best practices 100. SEO reads 66 on staging only because of the noindex; the production dry run has no noindex. What moved it: fonts self-hosted and preloaded (the Google Fonts CSS was render-blocking for up to 970 ms), hero image preloaded with a 1080 px variant for phones, grey text token raised from #555 (2.65:1) to #808080 (5.0:1), dark ink instead of white for small text and buttons on Ember (5.7:1 instead of 3.5:1), focus rings added, contact heading order fixed.
- **Rendering QA:** desktop and phone width (iframe harness) checked in Chrome after the changes: hero note and proof strip, close section in dark ink, work cards and groups, form, partner section, trust page.

## The audit (30 Oct, evening)

Three fresh agent reads plus Lighthouse, link and structured-data checks. Full outputs are in the session transcript; the findings that matter are folded into the decisions below.

1. **Enterprise buyer and partner seat.** P0s: "Start with a Sprint" sold before Sprint was defined; no door for partners; no proof on the first screen. All three applied (hero note, proof strip, partner section with its own mailto subject, home echo).
2. **Investor seat and a receipts table.** Every checkable claim was traced. Applied: FINTRAC's 1,087 STR rules confirmed on the Government of Canada page and linked; No Dress Rehearsal did not get "seven nominations", it won all seven categories it was nominated in and TIFF's People's Choice Documentary Award (POV Magazine, 31 May 2025), now said and linked; The Holy City line had fused two facts (it was a Cannes XR 2019 official selection and won the Advanced Imaging Society's Lumiere for Best Educational XR), corrected and linked to the Jerusalem Film Fund page; Spots of Light linked to the Biennale and SIGGRAPH archive pages; "named by Forbes" dropped (no Forbes 100 list exists in the public record; "a Top 100 CMO" stays); "flagship keynote" became "the keynote" with the talk title and the TiE site linked; the 2024 TiECon keynote added as a dated prior stage with the Ottawa Business Journal as receipt; "four years at Deloitte" became "nearly four years"; Conformer row dates fixed; Canaccord advisor page linked.
3. **Benchmark of seven comparable studios** (AE Studio, Fractional AI/Ode, Prolego, Tribe AI, Neurons Lab, Focused, Rootstrap). Applied from existing material: a qualifying form with a named reply time, number-led case cards, a trust/FAQ page, privacy link. Kept as the site's edge: the state key, a Sprint that ends with something running, the record itself.

## Source material and what the site may and may not say

- `~/Desktop/ATELIER-SET-v001-2026-10-23`: confidential pursuit material. The site uses the capability wording, the five controls, the selected-work list and the Oct 2026 bios from it, and never names Accenture or TRIYO. The compliance platform is "a Canadian compliance platform"; the FOX series is "a US series".
- Named on the site because the work is public: Warner Music / Daniel Lanois, Design Exchange Toronto, Amazon Prime / Prime Video (No Dress Rehearsal), Kawartha Dairy. **Sean to confirm** each may appear.
- Build-state vocabulary (delivered / released / demo environment / tested / built / demonstrated / phase 1 alpha / running) follows the Accenture deck's legend. "Live" was removed from the key because no row carries it; the Work lede now says so in plain words.
- Bio rules from `~/.claude/CLAUDE.md` applied: Nvidia work is "developed", Kognitiv raise figure omitted, LifeLabs not named, "7 companies" and "MIT" dropped, Top 100 CMO without a Forbes attribution.

## Decisions for Sean and Michael (in order of weight)

1. **Client naming** on /work/ and the home page (above). The proof strip under the hero repeats the names already in the work list, so it widens nothing, but it does put them on the first screen.
2. **Sean's No Dress Rehearsal credit.** The site says executive producer and Animation Director. The CSA Best Biography or Arts Documentary producer list and Wikipedia name Mike Downie, Jake Gold and others; Sean is not in the public producer list and IMDb's full credits were not reachable. Settle the on-screen credit title. Related: does the 2024 pipeline belong on the Atelier work list (Atelier postdates it) or only in Sean's bio?
3. **Two deck headlines were replaced on staging** because four independent reads flagged them and the doc system's own rule bars people-to-agent ratios: "Five people doing fifty people's work" is now "Two and a half weeks for six weeks' work" (its own warrant), and "Polymaths who have shipped this before" is now "Two founders who have shipped this before". Both revert in one line each if Michael wants them back. Kept as Michael's language: "Frankensteins", "made in-house, because it was", the slogan line in the team section.
4. **A Sprint price or band.** The site says "fixed price" without a number. Prolego publishes $80k per release; Neurons Lab "$20K to $50K" for short engagements. A band on /method/ and /contact/ would remove the first question every buyer emails.
5. **Who owns the code.** The Trust page says the client owns its data and tuning, and that code ownership and the Conformer/Conduit licence are set in the SOW. AE Studio says "you own all the IP and code"; a plainer sentence needs a founder decision.
6. **The bench.** "the engineers they have worked with for years" names no number. One sentence with a count and disciplines (Sean supplies).
7. **Sean's LinkedIn and IMDb URLs** for /team/, the footer and the JSON-LD (only Michael has a sameAs today). Not found by search; Sean supplies.
8. **Materiality in the primary nav**, with its capital-allocation framing and disclaimer, on a consultancy site a board may be sent to. Option: footer and home section only.
9. **Testimonials and vendor badges** (one attributed sentence each from Warner/Lanois, Design Exchange, the platform; Anthropic/AWS/Azure partner listings) are the two benchmark patterns that need material that does not exist yet.
10. **Verify before the flip:** Sean's "28 years" (his public bios say over 25), "co-founder" of Occupied VR, the Samsung client line, Viveport, the Eagle digital-production credit, the Academy of Digital Arts and Sciences membership, CES and SXSW as stages (dates pending in the bio facts), the DX system's name "Athena" and whether it is still in use, the nine US tour rooms, the Kawartha spot URL. All are Sean's or Michael's own wording; none has a public receipt yet.
11. **On 3 Nov:** swap the No. 04 card on /materiality/ from the dashed "next" card to a linked episode. Materiality No. 03 links to Michael's post; if Al posted it too, link Al's.

## Process (repeatable)

```
# staging
python3 build.py --base /atlr-staging --origin https://atlr-frge.github.io --staging --out ../atlr-staging
cd ../atlr-staging && git add -A . && git commit -m "Staging rebuild" && <token-dance push to atlr-frge/atlr-staging>

# copy gate: extract then gate, per page (the extractor is the session's extract_copy.py: headings/labels -> "# " lines)
python3 extract_copy.py <built page>/index.html > copy-<page>.md && python3 .../slop-gate.py copy-<page>.md

# the flip, only after Sean signs off
python3 build.py --base "" --origin https://atlr.pro --cname atlr.pro --out docs
git add docs && git commit -m "Production build for atlr.pro" && <token-dance push>
curl -sI https://atlr.pro/ | head -3
```

Token dance: `TOKEN=$(gh auth token); git push "https://x-access-token:${TOKEN}@github.com/atlr-frge/<repo>.git" main; unset TOKEN` (the token never enters .git/config this way).

**After the flip, in this order:** (1) submit one test from https://atlr.pro/contact/; FormSubmit ties activation to the origin, so this sends a one-time activation email to hello@atlr.pro; Michael clicks Activate (submissions are held 30 days until then; do not activate from staging, it would not carry over). (2) `site-qa` on https://atlr.pro. (3) Update the canonical table in `~/.claude/CLAUDE.md` (live column) and the `atelier-site` memory. (4) Point the aiimaginelabs links to the Atelier deck at https://atlr.pro (noted in the aiimaginelabs handoff).

## Next

- WhatsApp note to Sean with the staging URL and decisions 1 to 3 (sean-note skill).
- After sign-off: the flip and the four steps above.
- Later: an OG image with the wordmark (today's og-default.jpg is a brand-safe crop with no text); a Writing page gathering Materiality and the Mashup under atlr.pro if an email capture is wanted; a terms page if the form ever takes anything beyond an enquiry.
