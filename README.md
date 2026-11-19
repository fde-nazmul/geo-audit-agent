# geo-audit-agent

**Audit any web page for classic SEO *and* GEO (Generative Engine Optimization), then ask Claude for a prioritized fix plan.**

Google is no longer the only place buyers search. ChatGPT, Claude, Perplexity and Google AI Overviews now answer the question directly — and they quote pages they can crawl, parse and trust. This tool checks both sides in one pass.

Built from real client work at [ZeekWeb](https://zeekweb.com), where I deploy AI search and automation systems for B2B exporters and SMEs.

```text
GEO Audit — https://acme-lighting.test/
SEO score: 79/100   GEO score: 82/100

[SEO]
  PASS  title                Title (48 chars): Acme Lighting — Wholesale Table Lamps from China
  FAIL  image_alt            1/2 images missing alt
  FAIL  content_depth        ~67 words of visible text
  ...
[GEO]
  PASS  entity_schema        Organization / LocalBusiness / Person entity defined
  FAIL  ai_crawlers_allowed  Blocked: GPTBot
  FAIL  llms_txt             No /llms.txt
```

## What it checks

| Area | Check | Why it matters |
|---|---|---|
| SEO | Title, meta description, single H1, canonical, `lang`, viewport | The basics Google still ranks on |
| SEO | Image alt text, Open Graph, content depth, internal links | Accessibility, sharing, topical depth |
| GEO | JSON-LD structured data + entity schema (Organization / LocalBusiness / Person) | LLMs resolve *who* you are before they cite you |
| GEO | FAQ schema or question-style headings | Matches how people prompt AI assistants |
| GEO | Answer-first summary, H2 chunking | Pages split cleanly into quotable passages |
| GEO | `robots.txt` rules for GPTBot, ClaudeBot, PerplexityBot, Google-Extended… | Blocked crawlers = invisible in AI answers |
| GEO | `/llms.txt` | Emerging convention for guiding LLMs to key content |

## Quick start

No dependencies — Python 3.9+ standard library only.

```bash
git clone https://github.com/fde-nazmul/geo-audit-agent
cd geo-audit-agent

python geo_audit.py https://example.com                 # live audit
python geo_audit.py https://example.com --json out.json # save machine-readable report
python geo_audit.py --file examples/sample.html         # offline demo

export ANTHROPIC_API_KEY=sk-ant-...
python geo_audit.py https://example.com --ai            # + Claude fix plan
```

Run the tests:

```bash
python -m unittest -v
```

## How it fits a real deployment

In production this audit is one step in a larger loop:

1. **Discover** — crawl a client's site or a prospect list.
2. **Audit** — this tool scores every page for SEO + GEO.
3. **Plan** — Claude turns failed checks into a ranked, client-readable fix plan.
4. **Ship** — fixes go out through the CMS (WordPress/Elementor) with human approval.
5. **Measure** — Search Console, GA4 and AI-visibility tracking close the loop.

See [`supplier-outreach-pipeline`](https://github.com/fde-nazmul/supplier-outreach-pipeline) for the audit used as a lead-generation signal.

## Roadmap

- [ ] Multi-page crawl with sitemap discovery
- [ ] Baidu-specific checks for China-facing sites
- [ ] HTML/PDF client report output

## License

MIT
