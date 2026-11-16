# SESSION-HANDOFF: atlr.pro (Atelier Superintelligence site)

Updated 16 Nov 2026. **The full site is live at https://atlr.pro** (Michael's go on 16 Nov: "make the shift, Sean can tweak as needed once live"). Between the 30 Oct audit and the flip: Materiality poster captions removed (they covered the Canaccord Genuity and Verma marks), Sean invited as a collaborator (write) on atlr-site and atlr-staging, Sean's LinkedIn added site-wide, and Materiality brought up to date on the day of the flip.

## Canonical artifacts (edit these, nothing else)

| Artifact | Where | Notes |
|---|---|---|
| Site source | `src/` (layout.html, css/site.css, js/site.js, pages/*.html, assets/img, assets/fonts) | Pages carry a `<!--meta {...}-->` header read by build.py; `preload` in the meta adds image preloads |
| Build script | `build.py` | Commands in the docstring; no defaults, pass `--base --origin --out` |
| Live output | `docs/` on `main` (GitHub Pages main:/docs, CNAME atlr.pro) | The production build of src/ since 16 Nov 2026 (commit cfc7f1d). Rebuild with the flip command below after any src/ change; never `--staging` into docs |
| Staging output | `../atlr-staging/` (repo atlr-frge/atlr-staging, Pages from main root) | https://atlr-frge.github.io/atlr-staging/ (noindex, robots Disallow) |
| Holding page | `src/static/holding/index.html` (served at /holding/) | The one-screen page from the first hour; kept for the record |
| Brand source | `~/workspace/atelier-intro-v7/index.html` | site.css is a port of its stylesheet plus additions |
| Copy gate | `~/workspace/atelier-doc-system/skills/atelier-proposal/scripts/slop-gate.py` | Run on extracted copy (see Process) |
| Fonts | `src/assets/fonts/` four variable woff2 (cormorant-garamond, cormorant-garamond-italic, dm-sans, jetbrains-mono; latin subsets, OFL) + `fonts.css` | Self-hosted; one @font-face per family and style with a weight range; the same four rules are prepended to site.css; three preloads in layout. No Google Fonts request anywhere, the holding page included (fixed 16 Nov). |

## State

- **DNS:** atlr.pro points at GitHub Pages (A 185.199.108/109/110/111.153, www CNAME atlr-frge.github.io), changed in GoDaddy at about 16:00 ET on 30 Oct with Michael's go. MX, SPF, DMARC, DKIM, site-verification TXT untouched.
- **HTTPS:** live and enforced. GitHub's certificate needed a remove/re-add of the custom domain through the API (`PUT .../pages` with `{"cname":null}` then `{"cname":"atlr.pro"}`); it approved within a minute. GitHub committed "Delete CNAME" / "Create CNAME" on main during that nudge, so pull before pushing from another checkout.
- **What visitors see now:** the full site. The v7 deck served as the temp page from 30 Oct to 16 Nov (with an og:image and a facts-only bio line added on 30 Oct); it is still published at https://atlr-frge.github.io/atelier-intro-v7/ and the old `/images/og-default.jpg` path no longer exists (the site's share image is `/assets/img/og-default.jpg`). Verified on 16 Nov after the push: every page, the sitemap, robots, llms.txt and the holding page return 200, www and http both 301 to https://atlr.pro/, no noindex on indexable pages.
- **Materiality, 16 Nov:** /materiality/ lists No. 01 to 05 with Al Verma's posts for 04 (Robots) and 05 (Nvidia), covers 04 and 05 converted from the aiimaginelabs posters (506 x 900 webp, marks visible), and No. 06 Power as the dashed next card dated Tuesday 17 November. The home strip and the page strip show the latest three frames (03, 04, 05). **Each Tuesday the page needs the new episode** (copy, cover, Al's URL from aiimaginelabs' materiality page) and the next card moved on; No. 06 is due 17 Nov.
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
7. **Sean's IMDb URL** (and any other public profile) for his JSON-LD sameAs. His LinkedIn (https://www.linkedin.com/in/seanthomasevans/) came from Michael on 31 Oct and is now on /team/, /contact/, the footer, the Person node in every page's JSON-LD, and the live temp deck.
8. **Materiality in the primary nav**, with its capital-allocation framing and disclaimer, on a consultancy site a board may be sent to. Option: footer and home section only.
9. **Testimonials and vendor badges** (one attributed sentence each from Warner/Lanois, Design Exchange, the platform; Anthropic/AWS/Azure partner listings) are the two benchmark patterns that need material that does not exist yet.
10. **Verify before the flip:** Sean's "28 years" (his public bios say over 25), "co-founder" of Occupied VR, the Samsung client line, Viveport, the Eagle digital-production credit, the Academy of Digital Arts and Sciences membership, CES and SXSW as stages (dates pending in the bio facts), the DX system's name "Athena" and whether it is still in use, the nine US tour rooms, the Kawartha spot URL. All are Sean's or Michael's own wording; none has a public receipt yet.
11. **Weekly:** turn the dashed next card on /materiality/ into a linked episode each Tuesday (No. 06 on 17 Nov), add the cover, move the strips on. Source: aiimaginelabs `src/pages/materiality.html` and `assets/img/materiality/`.

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

**After the flip (16 Nov), all done:** (1) **FormSubmit is active.** A test submission went from https://atlr.pro/contact/ at Michael's word; FormSubmit's Action Required email reached hello@atlr.pro at 13:09 ET, Michael activated (FormSubmit's site was throwing Cloudflare 522/525 for a while, the click eventually took), and the held test enquiry was delivered at 13:14 ET as a table with the `_subject` "atlr.pro: a new enquiry". Real enquiries now arrive at hello@ and the sender lands on /thanks/. (2) site-qa ran on the live site: no deploy-breakers; its eight polish items were applied the same afternoon (Materiality share card regenerated from covers 03/04/05; sitemap lastmod now reads today for uncommitted sources; holding page on the self-hosted fonts; architecture diagram min-width 760 px so its labels are legible on a phone; four variable font files instead of fifteen copies; the "four systems" sentence on the home and Method pages now matches the four Work rows; the TV row label no longer says "In production"; the open mobile menu pins the body so iOS stops scrolling behind it). Left as notes: "Weeks 02–12" keeps its en dash as a range; the hero swarm image is light trails, not flame. (3) `~/.claude/CLAUDE.md` canonical table and the `atelier-site` memory say live. (4) aiimaginelabs' technology page links to https://atlr.pro (its build.py llms.txt line still names the v7 deck URL as the intro deck, which is still published).

## Next

- WhatsApp note to Sean: the site is live, he has write access to both repos, decisions 1 to 10 above are his to tweak in place (edit src/, commit, run the flip command, commit docs, push). **Commit src/ before building** so the sitemap lastmod is right (build.py now also treats a dirty source as changed today).
- Materiality share card (`src/assets/img/og-materiality.jpg`) is the latest three covers and ages weekly with the page; regenerate it with the Tuesday episode or make an evergreen card.
- Keep staging (atlr-frge.github.io/atlr-staging/) in step or retire it now that production is live; it was rebuilt alongside the flip (ec07654).
- Later: an OG image with the wordmark (today's og-default.jpg is a brand-safe crop with no text); a Writing page gathering Materiality and the Mashup under atlr.pro if an email capture is wanted; a terms page if the form ever takes anything beyond an enquiry.
