import textwrap
from pathlib import Path

ROOT = Path('remote/cloudways-server/vhxvtajnbg/public_html')

NAV_ITEMS = [
    ("What We Do", "/what-we-do/", "what-we-do"),
    ("Who We Are", "/who-we-are/", "who-we-are"),
    ("Insights", "/insights/", "insights"),
    ("Case Studies", "/case-studies/", "case-studies"),
    ("Careers", "/careers/", "careers"),
    ("Contact", "/contact/", "contact"),
]

BASE_TEMPLATE = textwrap.dedent("""
<!DOCTYPE html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
  <title>{title}</title>
  <meta name=\"description\" content=\"{meta_description}\"/>
  <link rel=\"canonical\" href=\"https://mosaicpolicy.com{canonical}\"/>
  <link rel=\"stylesheet\" href=\"/assets/css/main.v1.css\">
  <link rel=\"preload\" href=\"/assets/css/main.v1.css\" as=\"style\">
  <link rel=\"icon\" href=\"/favicon.svg\" type=\"image/svg+xml\">
  <meta property=\"og:title\" content=\"{og_title}\"/>
  <meta property=\"og:description\" content=\"{og_description}\"/>
  <meta property=\"og:type\" content=\"website\"/>
  <meta property=\"og:url\" content=\"https://mosaicpolicy.com{canonical}\"/>
  <meta property=\"og:image\" content=\"https://mosaicpolicy.com/assets/img/og-default.png\"/>
  <meta name=\"twitter:card\" content=\"summary_large_image\"/>
  <meta name=\"twitter:title\" content=\"{og_title}\"/>
  <meta name=\"twitter:description\" content=\"{og_description}\"/>
  <meta name=\"twitter:image\" content=\"https://mosaicpolicy.com/assets/img/og-default.png\"/>
  <script type=\"application/ld+json\">
  {{
    \"@context\": \"https://schema.org\",
    \"@type\": \"Organization\",
    \"name\": \"MOSAIC Health Policy\",
    \"url\": \"https://mosaicpolicy.com\",
    \"logo\": \"https://mosaicpolicy.com/assets/img/og-default.png\",
    \"sameAs\": [\"https://www.linkedin.com/company/mosaic-health-policy\"],
    \"contactPoint\": {{
      \"@type\": \"ContactPoint\",
      \"contactType\": \"media relations\",
      \"email\": \"info@mosaicpolicy.com\",
      \"telephone\": \"+1-202-503-9540\"
    }}
  }}
  </script>
  <script type=\"application/ld+json\">
  {{
    \"@context\": \"https://schema.org\",
    \"@type\": \"WebSite\",
    \"url\": \"https://mosaicpolicy.com\",
    \"potentialAction\": {{
      \"@type\": \"SearchAction\",
      \"target\": \"https://mosaicpolicy.com/?s={{search_term_string}}\",
      \"query-input\": \"required name=search_term_string\"
    }}
  }}
  </script>
</head>
<body>
  <a class=\"skip-link\" href=\"#main\">Skip to content</a>
  <header class=\"site-header\" role=\"banner\">
    <div class=\"site-header__inner\">
      <a class=\"brand\" href=\"/\">
        <span class=\"brand__mark\" aria-hidden=\"true\">M</span>
        <span class=\"brand__type\">MOSAIC Health Policy</span>
      </a>
      <button class=\"nav-toggle\" type=\"button\" data-nav-toggle aria-expanded=\"false\" aria-controls=\"primary-navigation\">
        <span class=\"sr-only\">Toggle navigation</span>
        ☰
      </button>
      <nav class=\"site-nav\" id=\"primary-navigation\" data-site-nav aria-label=\"Primary\">
        {nav_links}
      </nav>
    </div>
  </header>
  <main id=\"main\">
{content}
  </main>
  <footer class=\"site-footer\" role=\"contentinfo\">
    <div class=\"site-footer__inner\">
      <div>
        <h2 class=\"card__title\">MOSAIC Health Policy Inc.</h2>
        <p>409 7th Street NW, Suite 450<br>Washington, D.C. 20004</p>
        <p><a href=\"tel:2025039540\">202-503-9540</a><br><a href=\"mailto:info@mosaicpolicy.com\">info@mosaicpolicy.com</a></p>
      </div>
      <div>
        <h3>Navigate</h3>
        <ul style=\"list-style:none; padding:0; margin:0; display:grid; gap:var(--space-8);\">
          <li><a href=\"/what-we-do/\">What We Do</a></li>
          <li><a href=\"/who-we-are/\">Who We Are</a></li>
          <li><a href=\"/insights/\">Insights</a></li>
          <li><a href=\"/case-studies/\">Case Studies</a></li>
          <li><a href=\"/careers/\">Careers</a></li>
          <li><a href=\"/contact/\">Contact</a></li>
        </ul>
      </div>
      <div>
        <h3>Newsletter</h3>
        <p>Sign up for Appropriations Pulse™ alerts and executive digests.</p>
        <form aria-label=\"Newsletter signup\">
          <label for=\"newsletter-email\">Email</label>
          <input id=\"newsletter-email\" name=\"email\" type=\"email\" autocomplete=\"email\" required>
          <button class=\"btn btn-primary\" type=\"submit\">Join</button>
          <small>We respect confidentiality. Unsubscribe anytime.</small>
        </form>
      </div>
    </div>
    <div style=\"max-width:1200px;margin:var(--space-40) auto 0 auto;display:flex;justify-content:space-between;gap:var(--space-16);flex-wrap:wrap;color:rgba(255,255,255,0.6);\">
      <span>&copy; <span id=\"year\">2025</span> MOSAIC Health Policy.</span>
      <span>Policy Intelligence. Clarity for the C-Suite.</span>
    </div>
  </footer>
  <script>document.getElementById('year').textContent = new Date().getFullYear();</script>
  <script src=\"/assets/js/app.v1.js\" defer></script>
</body>
</html>
""")


def render_nav(current: str) -> str:
    items = []
    for label, href, key in NAV_ITEMS:
        attrs = []
        if key == current:
            attrs.append('aria-current="page"')
        attr_str = ' '.join(attrs)
        if attr_str:
            items.append(f'<a href="{href}" {attr_str}>{label}</a>')
        else:
            items.append(f'<a href="{href}">{label}</a>')
    return "\n        ".join(items)


def write_page(rel_path: str, *, title: str, meta_description: str, og_title: str, og_description: str, nav_current: str, content: str):
    path = ROOT / rel_path
    path.parent.mkdir(parents=True, exist_ok=True)
    canonical = canonical_for(rel_path)
    html = BASE_TEMPLATE.format(
        title=title,
        meta_description=meta_description,
        canonical=canonical,
        og_title=og_title,
        og_description=og_description,
        nav_links=render_nav(nav_current),
        content=textwrap.indent(textwrap.dedent(content).strip(), '    ')
    )
    path.write_text(html, encoding='utf-8')


def canonical_for(rel_path: str) -> str:
    rel = Path(rel_path)
    if rel.name == 'index.html':
        parts = rel.parent.parts
        if not parts:
            return '/'
        return '/' + '/'.join(parts) + '/'
    return '/' + str(rel)


# Data definitions for pages (excluding homepage)
PAGES = [
    {
        'rel_path': 'what-we-do/index.html',
        'title': 'What We Do | MOSAIC Health Policy',
        'meta': 'Explore MOSAIC Health Policy services: Sentinel monitoring, policy intelligence, advocacy, Precision Influence™, and executive advisory.',
        'og_title': 'What We Do',
        'og_desc': 'See how MOSAIC Health Policy delivers Sentinel monitoring, targeted intelligence, and Precision Influence™ for healthcare leaders.',
        'nav': 'what-we-do',
        'content': '''
<section class="section section--hero" role="region" aria-labelledby="page-title">
  <div class="section__inner" data-reveal>
    <p class="hero__eyebrow">Practices</p>
    <h1 id="page-title" class="hero__title">Strategic capacity built around your policy priorities.</h1>
    <p class="hero__subtitle">Every engagement aligns human intelligence, data signals, and executive counsel so the C-suite stays ahead of congressional, regulatory, and funding shocks.</p>
    <div class="hero__cta-group">
      <a class="btn btn-primary" href="#practices">View practices</a>
      <a class="btn btn-secondary" href="/contact/">Schedule a briefing</a>
    </div>
  </div>
</section>
<section class="section" id="practices" aria-labelledby="practices-heading">
  <div class="section__inner">
    <h2 id="practices-heading">Our practice lineup</h2>
    <p>Each practice can stand alone or integrate into a bespoke program. We start with your board-level outcomes, then build the mix of monitoring, analysis, influence, and activation needed to win.</p>
    <div class="practice-grid" data-reveal>
      <a class="card practice" href="/what-we-do/sentinel/">
        <h3 class="card__title">MOSAIC Sentinel™</h3>
        <p>Continuous watch on Congress, agencies, and stakeholder chatter with alerts that translate directly into executive action.</p>
      </a>
      <a class="card practice" href="/what-we-do/policy-intelligence/">
        <h3 class="card__title">Targeted Policy &amp; Funding Intelligence</h3>
        <p>Deep dives on legislation, rulemaking, and federal funding opportunities—complete with scenario planning and decision trees.</p>
      </a>
      <a class="card practice" href="/what-we-do/advocacy/">
        <h3 class="card__title">Strategic Advocacy &amp; Relationship Management</h3>
        <p>Senior advocates who choreograph briefings, draft testimony, and steward bipartisan champions around your story.</p>
      </a>
      <a class="card practice" href="/what-we-do/precision-influence/">
        <h3 class="card__title">Precision Influence™ — Decision-Network Targeting</h3>
        <p>Identify the handful of advisors who actually decide policy outcomes—and reach them with relevance and speed.</p>
      </a>
      <a class="card practice" href="/what-we-do/executive-advisory/">
        <h3 class="card__title">Executive Advisory &amp; Crisis Support</h3>
        <p>War-room counsel for CEOs, boards, and general counsel navigating hearings, investigations, or surprise headlines.</p>
      </a>
      <a class="card practice" href="/what-we-do/stakeholder-activation/">
        <h3 class="card__title">Stakeholder &amp; Coalition Activation</h3>
        <p>Mobilize clinicians, patients, and strategic allies with disciplined messaging, training, and accountability.</p>
      </a>
      <a class="card practice" href="/what-we-do/executive-advisory/">
        <h3 class="card__title">Executive Comms &amp; Creative Studio</h3>
        <p>Board decks, Hill leave-behinds, and motion content that make complex health policy legible to any audience.</p>
      </a>
    </div>
  </div>
</section>
<section class="section" aria-labelledby="outcomes-heading">
  <div class="section__inner" data-reveal>
    <h2 id="outcomes-heading">How we measure success</h2>
    <div class="card-grid">
      <div class="card">
        <span class="card__eyebrow">So what</span>
        <h3 class="card__title">Protect revenue and reputation</h3>
        <p>Sentinel™ keeps executives ahead of CMS, OMB, and Hill surprises so decisions are proactive, not reactive.</p>
      </div>
      <div class="card">
        <span class="card__eyebrow">Now what</span>
        <h3 class="card__title">Build winning influence plans</h3>
        <p>Policy intelligence and Precision Influence™ map the path from insight to action in plain numbers.</p>
      </div>
      <div class="card">
        <span class="card__eyebrow">By when</span>
        <h3 class="card__title">Deliver outcomes on deadline</h3>
        <p>We track milestones, risk, and accountability weekly, reporting the metrics your board expects.</p>
      </div>
    </div>
  </div>
</section>
'''
    },
    {
        'rel_path': 'what-we-do/sentinel/index.html',
        'title': 'MOSAIC Sentinel™ | 24/7 Federal Monitoring',
        'meta': 'MOSAIC Sentinel™ delivers nonstop Washington monitoring, plain-English alerts, and board-ready briefings for healthcare leaders.',
        'og_title': 'MOSAIC Sentinel™',
        'og_desc': 'Stay ahead of Washington with MOSAIC Sentinel™—continuous monitoring, executive alerts, and decisive recommendations.',
        'nav': 'what-we-do',
        'content': '''
<section class="section section--hero" role="region" aria-labelledby="page-title">
  <div class="section__inner" data-reveal>
    <p class="hero__eyebrow">MOSAIC Sentinel™</p>
    <h1 id="page-title" class="hero__title">Washington never sleeps. Neither do we.</h1>
    <p class="hero__subtitle">Sentinel™ fuses human intelligence and machine monitoring to surface the few developments that matter to your balance sheet—before they break.</p>
    <div class="hero__cta-group">
      <a class="btn btn-primary" href="/contact/">Request a Sentinel™ demo</a>
      <a class="btn btn-secondary" href="/insights/appropriations-pulse/">See Appropriations Pulse™</a>
    </div>
  </div>
</section>
<section class="section" aria-labelledby="promise-heading">
  <div class="section__inner" data-reveal>
    <h2 id="promise-heading">Promise</h2>
    <p>Deliver fast, accurate, executive-ready briefs with clear So-What / Now-What / By-When guidance. Every alert is tailored to your portfolio, stakeholders, and decision cadence.</p>
  </div>
</section>
<section class="section" aria-labelledby="proof-heading">
  <div class="section__inner" data-reveal>
    <h2 id="proof-heading">Proof</h2>
    <ul>
      <li>Median alert-to-decision time: 36 hours across flagship clients.</li>
      <li>Coverage spans Congress, CMS, FDA, OMB, GAO, and key think tanks.</li>
      <li>Board-ready weekly intelligence decks curated for CEOs and CFOs.</li>
    </ul>
  </div>
</section>
<section class="section" aria-labelledby="services-heading">
  <div class="section__inner" data-reveal>
    <h2 id="services-heading">Services</h2>
    <div class="card-grid">
      <div class="card">
        <h3 class="card__title">Real-time alerting</h3>
        <p>Signals classified by risk level, revenue impact, and recommended owner.</p>
      </div>
      <div class="card">
        <h3 class="card__title">Weekly executive brief</h3>
        <p>Curated memos with visuals and talking points ready for leadership huddles.</p>
      </div>
      <div class="card">
        <h3 class="card__title">Decision support</h3>
        <p>Scenario planning, countermeasure options, and stakeholder implications in one page.</p>
      </div>
    </div>
  </div>
</section>
<section class="section" aria-labelledby="cta-heading">
  <div class="section__inner" data-reveal>
    <h2 id="cta-heading">Stay ahead of the docket</h2>
    <p>Book a 30-minute Sentinel™ walkthrough to see your horizon scan within seven days.</p>
    <a class="btn btn-primary" href="/contact/">Schedule briefing</a>
  </div>
</section>
'''
    },
    {
        'rel_path': 'what-we-do/policy-intelligence/index.html',
        'title': 'Targeted Policy & Funding Intelligence | MOSAIC Health Policy',
        'meta': 'Deep policy analysis, funding landscape assessments, and scenario planning tailored to healthcare growth agendas.',
        'og_title': 'Targeted Policy & Funding Intelligence',
        'og_desc': 'Translate policy complexity into strategic options with MOSAIC’s targeted intelligence practice.',
        'nav': 'what-we-do',
        'content': '''
<section class="section section--hero" aria-labelledby="page-title">
  <div class="section__inner" data-reveal>
    <p class="hero__eyebrow">Policy Intelligence</p>
    <h1 id="page-title" class="hero__title">Clarity on every policy and funding beat.</h1>
    <p class="hero__subtitle">We decode legislation, regulation, and grant streams so your strategy, budgets, and communications align with what Washington will actually decide.</p>
  </div>
</section>
<section class="section" aria-labelledby="promise-heading">
  <div class="section__inner" data-reveal>
    <h2 id="promise-heading">Promise</h2>
    <p>Equip your executive team with evidence-backed options, decision trees, and quantified risk so they can act fast with confidence.</p>
  </div>
</section>
<section class="section" aria-labelledby="proof-heading">
  <div class="section__inner" data-reveal>
    <h2 id="proof-heading">Proof</h2>
    <ul>
      <li>Quarterly Medicare Payment Heat Map™ highlights services facing rate pressure six months ahead of peers.</li>
      <li>Funding Finder Index™ benchmarks discretionary grant velocity for your competitive set.</li>
      <li>Legislative strategy decks adopted by Fortune 100 compliance teams.</li>
    </ul>
  </div>
</section>
<section class="section" aria-labelledby="services-heading">
  <div class="section__inner" data-reveal>
    <h2 id="services-heading">Services</h2>
    <div class="card-grid">
      <div class="card">
        <h3 class="card__title">Policy mapping</h3>
        <p>Line-by-line analysis of bills and rules with stakeholder impact scoring.</p>
      </div>
      <div class="card">
        <h3 class="card__title">Funding intelligence</h3>
        <p>Pipeline tracking for grants, cooperative agreements, and pilot programs.</p>
      </div>
      <div class="card">
        <h3 class="card__title">Scenario planning</h3>
        <p>Decision trees with trigger points tied to key votes and deadlines.</p>
      </div>
    </div>
  </div>
</section>
<section class="section" aria-labelledby="cta-heading">
  <div class="section__inner" data-reveal>
    <h2 id="cta-heading">Request a custom intelligence build</h2>
    <p>We scope targeted deliverables in under two weeks—start with your must-win policy initiative.</p>
    <a class="btn btn-primary" href="/contact/">Launch discovery</a>
  </div>
</section>
'''
    },
    {
        'rel_path': 'what-we-do/advocacy/index.html',
        'title': 'Strategic Advocacy & Relationship Management | MOSAIC Health Policy',
        'meta': 'Trusted advocates orchestrating Hill, agency, and coalition engagement with measurable accountability.',
        'og_title': 'Strategic Advocacy & Relationship Management',
        'og_desc': 'Advance your agenda with disciplined, bipartisan advocacy anchored by MOSAIC senior strategists.',
        'nav': 'what-we-do',
        'content': '''
<section class="section section--hero" aria-labelledby="page-title">
  <div class="section__inner" data-reveal>
    <p class="hero__eyebrow">Advocacy</p>
    <h1 id="page-title" class="hero__title">Relationships built on trust—and results.</h1>
    <p class="hero__subtitle">From briefings to markups, we choreograph every touchpoint so lawmakers, regulators, and influencers know what you need and why it matters.</p>
  </div>
</section>
<section class="section" aria-labelledby="promise-heading">
  <div class="section__inner" data-reveal>
    <h2 id="promise-heading">Promise</h2>
    <p>Deliver disciplined advocacy plans with clear owners, timelines, and metrics tied to concrete policy outcomes.</p>
  </div>
</section>
<section class="section" aria-labelledby="proof-heading">
  <div class="section__inner" data-reveal>
    <h2 id="proof-heading">Proof</h2>
    <ul>
      <li>Secured bipartisan bill sponsors within six weeks for a coverage expansion campaign.</li>
      <li>Coordinated 45+ agency meetings for a national association renewal effort.</li>
      <li>Designed testimony and prep sessions that helped win unanimous committee votes.</li>
    </ul>
  </div>
</section>
<section class="section" aria-labelledby="services-heading">
  <div class="section__inner" data-reveal>
    <h2 id="services-heading">Services</h2>
    <div class="card-grid">
      <div class="card">
        <h3 class="card__title">Advocacy playbooks</h3>
        <p>Roadmaps with prioritized targets, messages, and KPIs.</p>
      </div>
      <div class="card">
        <h3 class="card__title">Relationship management</h3>
        <p>Senior-led meetings, staffing, and follow-up to keep officials engaged.</p>
      </div>
      <div class="card">
        <h3 class="card__title">Hearing prep</h3>
        <p>Rehearsals, Q&amp;A matrices, and media alignment for critical moments.</p>
      </div>
    </div>
  </div>
</section>
<section class="section" aria-labelledby="cta-heading">
  <div class="section__inner" data-reveal>
    <h2 id="cta-heading">Build your influence bench</h2>
    <p>Let’s map the allies, skeptics, and swing voices you need to win the next decision.</p>
    <a class="btn btn-primary" href="/contact/">Start the plan</a>
  </div>
</section>
'''
    },
    {
        'rel_path': 'what-we-do/precision-influence/index.html',
        'title': 'Precision Influence™ — Decision-Network Targeting | MOSAIC Health Policy',
        'meta': 'Identify and engage the decision network that determines your policy outcome with MOSAIC’s Precision Influence™ practice.',
        'og_title': 'Precision Influence™ — Decision-Network Targeting',
        'og_desc': 'Reach the few who matter. Precision Influence™ maps, prioritizes, and engages the decision network behind every policy call.',
        'nav': 'what-we-do',
        'content': '''
<section class="section section--hero" aria-labelledby="page-title">
  <div class="section__inner" data-reveal>
    <p class="hero__eyebrow">Precision Influence™</p>
    <h1 id="page-title" class="hero__title">Decide the conversation before it happens.</h1>
    <p class="hero__subtitle">Precision Influence™ — Decision-Network Targeting isolates the aides, advisors, analysts, and validators who actually sway the outcome—and delivers relevance straight to them.</p>
  </div>
</section>
<section class="section" aria-labelledby="promise-heading">
  <div class="section__inner" data-reveal>
    <h2 id="promise-heading">Promise</h2>
    <p>Turn opaque influence webs into precise lists with message frameworks, cadence plans, and measurement dashboards.</p>
  </div>
</section>
<section class="section" aria-labelledby="proof-heading">
  <div class="section__inner" data-reveal>
    <h2 id="proof-heading">Proof</h2>
    <ul>
      <li>Mapped 275-person decision network for an emerging biotech in 10 days.</li>
      <li>Boosted positive signal share by 42% among top committee staff within six-week sprint.</li>
      <li>Delivered weekly sentiment dashboards integrating earned, owned, and direct feedback.</li>
    </ul>
  </div>
</section>
<section class="section" aria-labelledby="services-heading">
  <div class="section__inner" data-reveal>
    <h2 id="services-heading">Services</h2>
    <div class="card-grid">
      <div class="card">
        <h3 class="card__title">Decision-network mapping</h3>
        <p>Identify influencers, validators, and blockers with weighted scoring.</p>
      </div>
      <div class="card">
        <h3 class="card__title">Message engineering</h3>
        <p>Micro-targeted briefs, creative, and call scripts tailored to each segment.</p>
      </div>
      <div class="card">
        <h3 class="card__title">Signal analytics</h3>
        <p>Dashboard tracking contact velocity, sentiment, and conversions.</p>
      </div>
    </div>
  </div>
</section>
<section class="section" aria-labelledby="cta-heading">
  <div class="section__inner" data-reveal>
    <h2 id="cta-heading">Activate Precision Influence™</h2>
    <p>Bring your policy brief or legislative threat—we’ll chart the decision-network in the first meeting.</p>
    <a class="btn btn-primary" href="/contact/">Book a working session</a>
  </div>
</section>
'''
    },
    {
        'rel_path': 'what-we-do/stakeholder-activation/index.html',
        'title': 'Stakeholder & Coalition Activation | MOSAIC Health Policy',
        'meta': 'Mobilize clinicians, patients, and partners with disciplined programs that align messages and metrics around your goal.',
        'og_title': 'Stakeholder & Coalition Activation',
        'og_desc': 'Build disciplined stakeholder coalitions with MOSAIC—message alignment, mobilization plans, and measurement built in.',
        'nav': 'what-we-do',
        'content': '''
<section class="section section--hero" aria-labelledby="page-title">
  <div class="section__inner" data-reveal>
    <p class="hero__eyebrow">Stakeholder Activation</p>
    <h1 id="page-title" class="hero__title">Mobilize the people who make policy real.</h1>
    <p class="hero__subtitle">We recruit, brief, and equip the practitioners, patients, and partners who give your policy story credibility on every channel.</p>
  </div>
</section>
<section class="section" aria-labelledby="promise-heading">
  <div class="section__inner" data-reveal>
    <h2 id="promise-heading">Promise</h2>
    <p>Design turnkey activation programs that fit busy professionals and deliver measurable momentum toward your policy outcome.</p>
  </div>
</section>
<section class="section" aria-labelledby="proof-heading">
  <div class="section__inner" data-reveal>
    <h2 id="proof-heading">Proof</h2>
    <ul>
      <li>Launched a 50-state clinician rapid-response network within 30 days.</li>
      <li>Coached patient ambassadors featured in national earned media within one campaign cycle.</li>
      <li>Generated 12K+ personalized lawmaker contacts with 98% message adherence.</li>
    </ul>
  </div>
</section>
<section class="section" aria-labelledby="services-heading">
  <div class="section__inner" data-reveal>
    <h2 id="services-heading">Services</h2>
    <div class="card-grid">
      <div class="card">
        <h3 class="card__title">Recruitment &amp; vetting</h3>
        <p>Target the voices that align with your credibility needs and compliance guardrails.</p>
      </div>
      <div class="card">
        <h3 class="card__title">Message &amp; media training</h3>
        <p>Briefing materials, rehearsal sessions, and modular talking points.</p>
      </div>
      <div class="card">
        <h3 class="card__title">Activation analytics</h3>
        <p>Dashboards tracking participation, conversion, and impact by geography and stakeholder type.</p>
      </div>
    </div>
  </div>
</section>
<section class="section" aria-labelledby="cta-heading">
  <div class="section__inner" data-reveal>
    <h2 id="cta-heading">Launch the coalition</h2>
    <p>Share your goal and timeline—we’ll architect the activation path that sustains pressure until the decision drops.</p>
    <a class="btn btn-primary" href="/contact/">Plan activation</a>
  </div>
</section>
'''
    },
    {
        'rel_path': 'what-we-do/executive-advisory/index.html',
        'title': 'Executive Advisory & Crisis Support | MOSAIC Health Policy',
        'meta': 'On-call advisors helping CEOs, boards, and counsel navigate hearings, investigations, and urgent policy inflection points.',
        'og_title': 'Executive Advisory & Crisis Support',
        'og_desc': 'Get 24/7 senior counsel for hearings, investigations, and high-stakes policy negotiations.',
        'nav': 'what-we-do',
        'content': '''
<section class="section section--hero" aria-labelledby="page-title">
  <div class="section__inner" data-reveal>
    <p class="hero__eyebrow">Executive Advisory</p>
    <h1 id="page-title" class="hero__title">When the stakes spike, call MOSAIC first.</h1>
    <p class="hero__subtitle">We sit alongside your CEO, general counsel, and communications leads to navigate hearings, investigations, and last-mile negotiations without missteps.</p>
  </div>
</section>
<section class="section" aria-labelledby="promise-heading">
  <div class="section__inner" data-reveal>
    <h2 id="promise-heading">Promise</h2>
    <p>Provide calm, seasoned counsel and ready-to-execute playbooks whenever Washington moves faster than your org chart.</p>
  </div>
</section>
<section class="section" aria-labelledby="proof-heading">
  <div class="section__inner" data-reveal>
    <h2 id="proof-heading">Proof</h2>
    <ul>
      <li>Managed crisis communications and Hill prep that prevented subpoenas for a national provider.</li>
      <li>Guided a Fortune 200 board through emergency CMS briefings within 48 hours.</li>
      <li>Delivered integrated legal, policy, and media response frameworks adopted company-wide.</li>
    </ul>
  </div>
</section>
<section class="section" aria-labelledby="services-heading">
  <div class="section__inner" data-reveal>
    <h2 id="services-heading">Services</h2>
    <div class="card-grid">
      <div class="card">
        <h3 class="card__title">War-room advisory</h3>
        <p>Real-time decision support with structured escalation protocols.</p>
      </div>
      <div class="card">
        <h3 class="card__title">Hearing &amp; media prep</h3>
        <p>Message grids, rehearsals, and rapid rebuttal guidance.</p>
      </div>
      <div class="card">
        <h3 class="card__title">Post-crisis reset</h3>
        <p>Lessons-learned workshops and roadmap to rebuild trust.</p>
      </div>
    </div>
  </div>
</section>
<section class="section" aria-labelledby="cta-heading">
  <div class="section__inner" data-reveal>
    <h2 id="cta-heading">Put counsel on speed dial</h2>
    <p>We hold dedicated crisis retainer blocks for select partners—ask about availability.</p>
    <a class="btn btn-primary" href="/contact/">Request access</a>
  </div>
</section>
'''
    },
    {
        'rel_path': 'insights/index.html',
        'title': 'Insights | MOSAIC Health Policy',
        'meta': 'Executive intelligence from MOSAIC: Appropriations Pulse™, Medicare Payment Heat Map™, Funding Finder Index™, and more.',
        'og_title': 'Insights from MOSAIC',
        'og_desc': 'Access executive-ready insights including Appropriations Pulse™, Medicare Payment Heat Map™, and Funding Finder Index™.',
        'nav': 'insights',
        'content': '''
<section class="section section--hero" aria-labelledby="page-title">
  <div class="section__inner" data-reveal>
    <p class="hero__eyebrow">Insights</p>
    <h1 id="page-title" class="hero__title">Keep your finger on Washington’s pulse.</h1>
    <p class="hero__subtitle">Our flagship briefings decode federal movement for boards, c-suite teams, and operators who need clarity now.</p>
  </div>
</section>
<section class="section" aria-labelledby="insights-list">
  <div class="section__inner" data-reveal>
    <h2 id="insights-list">Latest executive summaries</h2>
    <div class="card-grid">
      <a class="card" href="/insights/appropriations-pulse/">
        <h3 class="card__title">Appropriations Pulse™</h3>
        <p>Weekly outlook on how House and Senate spending bills impact health priorities—complete with vote forecasts and risk flags.</p>
      </a>
      <a class="card" href="/insights/medicare-payment-heat-map/">
        <h3 class="card__title">Medicare Payment Heat Map™</h3>
        <p>Interactive brief that tracks CMS rulemaking, highlighting service lines facing headwinds or upside.</p>
      </a>
      <a class="card" href="/insights/funding-finder-index/">
        <h3 class="card__title">Funding Finder Index™</h3>
        <p>Monthly benchmarking of discretionary and mandatory program velocity so you capture funds before they're oversubscribed.</p>
      </a>
    </div>
  </div>
</section>
<section class="section" aria-labelledby="cta-insights">
  <div class="section__inner" data-reveal>
    <h2 id="cta-insights">Need enterprise access?</h2>
    <p>We integrate these insights into Sentinel™ dashboards and custom portals for enterprise clients.</p>
    <a class="btn btn-primary" href="/contact/">Discuss licensing</a>
  </div>
</section>
'''
    },
    {
        'rel_path': 'insights/appropriations-pulse/index.html',
        'title': 'Appropriations Pulse™ | MOSAIC Insights',
        'meta': 'Appropriations Pulse™ briefing: weekly intelligence on federal spending dynamics for healthcare executives.',
        'og_title': 'Appropriations Pulse™',
        'og_desc': 'Dive into this week’s Appropriations Pulse™—scenario planning for healthcare leaders navigating federal spending.',
        'nav': 'insights',
        'content': '''
<section class="section section--hero" aria-labelledby="page-title">
  <div class="section__inner" data-reveal>
    <p class="hero__eyebrow">Insight</p>
    <h1 id="page-title" class="hero__title">Appropriations Pulse™</h1>
    <p class="hero__subtitle">Weekly pulse on how House and Senate spending dynamics affect healthcare priorities, complete with decision scenarios for your leadership team.</p>
  </div>
</section>
<section class="section" aria-labelledby="summary-heading">
  <div class="section__inner" data-reveal>
    <h2 id="summary-heading">This week’s executive brief</h2>
    <p>Appropriations Pulse™ integrates live committee markups, leadership negotiations, and budget ceilings to show where healthcare priorities will land before votes are scheduled. This edition flags House-proposed offsets targeting hospital payments while the Senate charts a bipartisan path on emergency supplemental funding, creating divergent risk profiles. We outline three likely outcomes, the whip counts required for each chamber, the procedural maneuvers still available, and the decision dates that could shift cash flow. Finance receives modeled revenue impacts, government relations gets stakeholder assignments, and communications gains draft messaging so every function moves in lockstep. Sentinel™ subscribers also see early indicators on continuing resolutions and offset packages to rehearse with leadership.</p>
  </div>
</section>
<section class="section" aria-labelledby="now-heading">
  <div class="section__inner" data-reveal>
    <h2 id="now-heading">Now, next, watch</h2>
    <ul>
      <li><strong>Now:</strong> CFOs should scenario-test a 2% sequestration patch versus expiration on December 31.</li>
      <li><strong>Next:</strong> Coordinate with MOSAIC Sentinel™ to monitor floor-amendment windows across both chambers.</li>
      <li><strong>Watch:</strong> Potential continuing resolution which shifts grant release calendars by 45 days.</li>
    </ul>
  </div>
</section>
<section class="section" aria-labelledby="cta-heading">
  <div class="section__inner" data-reveal>
    <h2 id="cta-heading">Access the full dashboard</h2>
    <p>Clients receive subscriber-only charts, whip counts, and tailored action prompts each Friday.</p>
    <a class="btn btn-primary" href="/contact/">Upgrade access</a>
  </div>
</section>
'''
    },
    {
        'rel_path': 'insights/medicare-payment-heat-map/index.html',
        'title': 'Medicare Payment Heat Map™ | MOSAIC Insights',
        'meta': 'Medicare Payment Heat Map™ visualizes rate pressure and upside across CMS programs for healthcare executives.',
        'og_title': 'Medicare Payment Heat Map™',
        'og_desc': 'See which Medicare services face rate shifts with MOSAIC’s Medicare Payment Heat Map™.',
        'nav': 'insights',
        'content': '''
<section class="section section--hero" aria-labelledby="page-title">
  <div class="section__inner" data-reveal>
    <p class="hero__eyebrow">Insight</p>
    <h1 id="page-title" class="hero__title">Medicare Payment Heat Map™</h1>
    <p class="hero__subtitle">Rapid readout on Medicare rate trends so service-line leaders know where to defend, invest, or pivot next.</p>
  </div>
</section>
<section class="section" aria-labelledby="summary-heading">
  <div class="section__inner" data-reveal>
    <h2 id="summary-heading">Key executive takeaways</h2>
    <p>The Medicare Payment Heat Map™ blends CMS rule text, claims data, and MOSAIC modeling to spotlight service lines under rate pressure or poised for upside. This cycle shows outpatient behavioral health winning a 3.1% bump, while cardiac imaging faces downward adjustments tied to budget neutrality formulas. Ambulatory surgery centers see mixed results depending on geography and payer mix, and home health remains in the crosshairs of sequestration. Leadership teams receive variance ranges, compliance checkpoints, capital planning prompts, and aligned partner opportunities for each code family, with recommended engagement timelines so finance, clinical ops, and advocacy stay aligned on priorities. Subscribers also gain early-warning triggers that push alerts the moment CMS revises assumptions.</p>
  </div>
</section>
<section class="section" aria-labelledby="actions-heading">
  <div class="section__inner" data-reveal>
    <h2 id="actions-heading">Executive actions</h2>
    <ul>
      <li>Assign stakeholders to validate the revenue impact scenarios within 10 days.</li>
      <li>Pair advocacy outreach with the Precision Influence™ team to reinforce priority services.</li>
      <li>Prep communications to reassure clinicians and investors once the final rule posts.</li>
    </ul>
  </div>
</section>
<section class="section" aria-labelledby="cta-heading">
  <div class="section__inner" data-reveal>
    <h2 id="cta-heading">Get the interactive model</h2>
    <p>Clients unlock dynamic filters by state, payer mix, and site of service.</p>
    <a class="btn btn-primary" href="/contact/">Request model preview</a>
  </div>
</section>
'''
    },
    {
        'rel_path': 'insights/funding-finder-index/index.html',
        'title': 'Funding Finder Index™ | MOSAIC Insights',
        'meta': 'Funding Finder Index™ ranks federal funding streams by velocity and fit so you capture dollars before they move.',
        'og_title': 'Funding Finder Index™',
        'og_desc': 'Benchmark grant and program velocity with MOSAIC’s Funding Finder Index™ for healthcare growth leaders.',
        'nav': 'insights',
        'content': '''
<section class="section section--hero" aria-labelledby="page-title">
  <div class="section__inner" data-reveal>
    <p class="hero__eyebrow">Insight</p>
    <h1 id="page-title" class="hero__title">Funding Finder Index™</h1>
    <p class="hero__subtitle">Monthly playbook ranking the fastest-moving federal dollars and how to win them before competitors do.</p>
  </div>
</section>
<section class="section" aria-labelledby="summary-heading">
  <div class="section__inner" data-reveal>
    <h2 id="summary-heading">Funding landscape at a glance</h2>
    <p>The Funding Finder Index™ scores federal programs by velocity, award size, and competitive intensity. This month, HHS innovation pilots and rural broadband alignments earn top marks, while pandemic-era carve-outs sunset and workforce grants tighten eligibility. We translate the data into heat-score dashboards, eligibility checklists, partner mapping, and pursuit timelines that keep business development, grants, finance, and government relations teams working in sync. Each brief also flags likely offsets, compliance watch-outs, peer benchmarks, and key decision gatekeepers so your team knows when to lead, follow, or hold. Sentinel™ alerts plug directly into calendars with reminders for pre-application engagement and reporting requirements.</p>
  </div>
</section>
<section class="section" aria-labelledby="actions-heading">
  <div class="section__inner" data-reveal>
    <h2 id="actions-heading">Action prompts</h2>
    <ul>
      <li>Assign prospecting teams to pre-brief targeted program officers within two weeks.</li>
      <li>Coordinate coalition statements that strengthen your competitiveness score.</li>
      <li>Sync finance and compliance on reporting obligations before letters of intent drop.</li>
    </ul>
  </div>
</section>
<section class="section" aria-labelledby="cta-heading">
  <div class="section__inner" data-reveal>
    <h2 id="cta-heading">Download the index</h2>
    <p>Enterprise subscribers receive custom slices filtered by geography, operating model, and risk tolerance.</p>
    <a class="btn btn-primary" href="/contact/">Unlock subscriber access</a>
  </div>
</section>
'''
    },
    {
        'rel_path': 'case-studies/index.html',
        'title': 'Case Studies | MOSAIC Health Policy',
        'meta': 'Explore MOSAIC case studies covering hospital revenue stabilization, coalition realignment, and biotech market entry.',
        'og_title': 'Case Studies',
        'og_desc': 'See how MOSAIC Health Policy delivers measurable outcomes for hospitals, associations, and innovators.',
        'nav': 'case-studies',
        'content': '''
<section class="section section--hero" aria-labelledby="page-title">
  <div class="section__inner" data-reveal>
    <p class="hero__eyebrow">Case Studies</p>
    <h1 id="page-title" class="hero__title">Outcomes we can name. Partners we protect.</h1>
    <p class="hero__subtitle">Representative engagements showing how intelligence, advocacy, and Precision Influence™ convert into revenue, credibility, and momentum.</p>
  </div>
</section>
<section class="section" aria-labelledby="cases-heading">
  <div class="section__inner" data-reveal>
    <h2 id="cases-heading">Featured engagements</h2>
    <div class="card-grid">
      <a class="card" href="/case-studies/hospital-turnaround/">
        <h3 class="card__title">Stabilizing Medicare Revenue</h3>
        <p>Integrated health system regained predictable rates through targeted intelligence and advocacy.</p>
      </a>
      <a class="card" href="/case-studies/association-realignment/">
        <h3 class="card__title">Resetting a Fragmented Coalition</h3>
        <p>National association rebuilt trust, secured bipartisan champions, and aligned members around one message.</p>
      </a>
      <a class="card" href="/case-studies/biotech-approval/">
        <h3 class="card__title">Accelerating Breakthrough Approval</h3>
        <p>Emerging biotech mapped the decision network, won FDA alignment, and launched on schedule.</p>
      </a>
    </div>
  </div>
</section>
<section class="section" aria-labelledby="cta-cases">
  <div class="section__inner" data-reveal>
    <h2 id="cta-cases">Let’s script your headline</h2>
    <p>We tailor composite case studies under NDA—share your challenge to see what success can look like.</p>
    <a class="btn btn-primary" href="/contact/">Start the conversation</a>
  </div>
</section>
'''
    },
    {
        'rel_path': 'case-studies/hospital-turnaround/index.html',
        'title': 'Case Study | Stabilizing Medicare Revenue',
        'meta': 'How MOSAIC helped a multi-state hospital network stabilize Medicare revenue during a payment crisis.',
        'og_title': 'Case Study: Stabilizing Medicare Revenue',
        'og_desc': 'Discover how MOSAIC stabilized Medicare revenue for a multi-state hospital system facing payment cuts.',
        'nav': 'case-studies',
        'content': '''
<section class="section section--hero" aria-labelledby="page-title">
  <div class="section__inner" data-reveal>
    <p class="hero__eyebrow">Case Study</p>
    <h1 id="page-title" class="hero__title">Stabilizing Medicare Revenue for a Multi-State System</h1>
    <p class="hero__subtitle">A Fortune 200 health system faced a proposed 5.2% Medicare cut that threatened bond covenants and capital plans. MOSAIC mobilized intelligence, advocacy, and Precision Influence™ to redirect the outcome.</p>
  </div>
</section>
<section class="section" aria-labelledby="challenge-heading">
  <div class="section__inner" data-reveal>
    <h2 id="challenge-heading">Challenge</h2>
    <p>The system lacked real-time visibility into CMS draft policy language and underestimated the coalition needed to counter budget neutrality adjustments. Investor relations and government affairs worked in silos, risking inconsistent messaging and leaving local market CEOs unsure how to engage their delegations.</p>
  </div>
</section>
<section class="section" aria-labelledby="strategy-heading">
  <div class="section__inner" data-reveal>
    <h2 id="strategy-heading">Strategy</h2>
    <p>MOSAIC deployed Sentinel™ rapid alerts, built payment impact models, and convened weekly war-room sessions. Precision Influence™ targeted the decision network—OMB analysts, key committee staff, and allied CEOs—while advocacy leads orchestrated testimony and bipartisan briefings. We paired national messaging with localized hospital stories and delivered investor-ready talking points each time market rumors surfaced.</p>
  </div>
</section>
<section class="section" aria-labelledby="outcome-heading">
  <div class="section__inner" data-reveal>
    <h2 id="outcome-heading">Outcome</h2>
    <p>CMS softened the final rule to a 1.1% reduction, preserving $410M in revenue. The system entered the next fiscal year with unified messaging, an expanded coalition, and an internal decision protocol anchored by MOSAIC dashboards. The board credited the program with restoring confidence to its capital plan and maintaining positive outlooks from rating agencies.</p>
    <blockquote>“MOSAIC delivered command-center clarity. We made decisions within hours, not days.” — Chief Financial Officer</blockquote>
  </div>
</section>
<section class="section" aria-labelledby="proof-heading">
  <div class="section__inner" data-reveal>
    <h2 id="proof-heading">Proof</h2>
    <ul>
      <li>Reduced policy response time from 72 hours to 18 hours.</li>
      <li>Secured support letters from 28 lawmakers across both parties.</li>
      <li>Protected $410M in Medicare revenue across two fiscal years.</li>
    </ul>
  </div>
</section>
'''
    },
    {
        'rel_path': 'case-studies/association-realignment/index.html',
        'title': 'Case Study | Resetting a Fragmented Coalition',
        'meta': 'How MOSAIC realigned a national healthcare association and rebuilt influence in Congress.',
        'og_title': 'Case Study: Resetting a Fragmented Coalition',
        'og_desc': 'See how MOSAIC rebuilt a national association’s advocacy muscle and secured bipartisan wins.',
        'nav': 'case-studies',
        'content': '''
<section class="section section--hero" aria-labelledby="page-title">
  <div class="section__inner" data-reveal>
    <p class="hero__eyebrow">Case Study</p>
    <h1 id="page-title" class="hero__title">Resetting a Fragmented Coalition</h1>
    <p class="hero__subtitle">A national healthcare association faced member fatigue, fractured messaging, and uneven advocacy performance. MOSAIC rebuilt alignment, discipline, and credibility across the network.</p>
  </div>
</section>
<section class="section" aria-labelledby="challenge-heading">
  <div class="section__inner" data-reveal>
    <h2 id="challenge-heading">Challenge</h2>
    <p>Members delivered inconsistent messages, relationships with key committee staff had cooled, and grassroots activation lacked metrics. Regional affiliates pushed competing priorities, confusing Hill and agency partners, and placing funding renewals at risk. Media narratives were drifting negative, eroding brand equity.</p>
  </div>
</section>
<section class="section" aria-labelledby="strategy-heading">
  <div class="section__inner" data-reveal>
    <h2 id="strategy-heading">Strategy</h2>
    <p>MOSAIC ran stakeholder interviews, rebuilt the value proposition, and installed a unified advocacy calendar with disciplined reporting. Precision Influence™ mapped decision-makers while the activation team recruited clinician and patient ambassadors. We produced briefing kits, social toolkits, and meeting scorecards so every touchpoint stayed on message and accountable.</p>
  </div>
</section>
<section class="section" aria-labelledby="outcome-heading">
  <div class="section__inner" data-reveal>
    <h2 id="outcome-heading">Outcome</h2>
    <p>Within a quarter, the coalition secured bipartisan support letters, regained seat-at-table status with agency leads, and delivered member engagement scores 30% higher than baseline. Membership renewals exceeded forecast and affiliated CEOs reported a 40% increase in perceived value, giving the association new leverage heading into reauthorization. Media sentiment flipped positive, setting the table for upcoming legislative pushes.</p>
    <blockquote>“We went from reactive to leading the narrative. MOSAIC gave us back our voice.” — Association CEO</blockquote>
  </div>
</section>
<section class="section" aria-labelledby="proof-heading">
  <div class="section__inner" data-reveal>
    <h2 id="proof-heading">Proof</h2>
    <ul>
      <li>34% increase in lawmaker touchpoints quarter-over-quarter.</li>
      <li>Coalition net promoter score climbed from 21 to 63.</li>
      <li>Secured renewal of a $180M federal partnership program.</li>
    </ul>
  </div>
</section>
'''
    },
    {
        'rel_path': 'case-studies/biotech-approval/index.html',
        'title': 'Case Study | Accelerating Breakthrough Approval',
        'meta': 'How MOSAIC’s Precision Influence™ helped an emerging biotech secure on-time FDA clearance.',
        'og_title': 'Case Study: Accelerating Breakthrough Approval',
        'og_desc': 'Learn how Precision Influence™ mapped the decision network that delivered on-time FDA approval for a biotech innovator.',
        'nav': 'case-studies',
        'content': '''
<section class="section section--hero" aria-labelledby="page-title">
  <div class="section__inner" data-reveal>
    <p class="hero__eyebrow">Case Study</p>
    <h1 id="page-title" class="hero__title">Accelerating Breakthrough Approval</h1>
    <p class="hero__subtitle">An emerging biotech needed rapid FDA clearance while navigating competitive policy pressure and capital constraints. MOSAIC Precision Influence™ charted the decision network required to win.</p>
  </div>
</section>
<section class="section" aria-labelledby="challenge-heading">
  <div class="section__inner" data-reveal>
    <h2 id="challenge-heading">Challenge</h2>
    <p>The company faced skeptical reviewers and a well-funded competitor pushing negative narratives. Internal teams lacked Washington contacts, process fluency, and the bandwidth to manage concurrent investor expectations while preparing for commercial launch.</p>
  </div>
</section>
<section class="section" aria-labelledby="strategy-heading">
  <div class="section__inner" data-reveal>
    <h2 id="strategy-heading">Strategy</h2>
    <p>MOSAIC mapped the regulators, advisors, and medical thought leaders driving the decision. Custom briefing materials and third-party validators delivered credible support, while advocacy teams neutralized misinformation on the Hill and in trade press. We choreographed executive fly-ins, facilitated scientific advisory briefings, and supplied sentiment dashboards to track momentum.</p>
  </div>
</section>
<section class="section" aria-labelledby="outcome-heading">
  <div class="section__inner" data-reveal>
    <h2 id="outcome-heading">Outcome</h2>
    <p>The FDA granted breakthrough approval on the original timeline, and the company launched nationwide with a ready coalition of clinician champions. Investor confidence improved, enabling a successful secondary raise, and policymakers cited the firm as a model for responsible innovation stewardship. Post-launch tracking showed sustained positive sentiment among key decision influencers for 90 days.</p>
    <blockquote>“Precision Influence™ pinpointed the people who mattered—and equipped us to win them over.” — Chief Executive Officer</blockquote>
  </div>
</section>
<section class="section" aria-labelledby="proof-heading">
  <div class="section__inner" data-reveal>
    <h2 id="proof-heading">Proof</h2>
    <ul>
      <li>Decision-network map delivered in seven days.</li>
      <li>Secured supportive statements from four leading medical societies.</li>
      <li>Achieved approval with zero cycle delays despite competitor opposition.</li>
    </ul>
  </div>
</section>
'''
    },
    {
        'rel_path': 'who-we-are/index.html',
        'title': 'Who We Are | MOSAIC Health Policy',
        'meta': 'Meet the bipartisan, multi-disciplinary team behind MOSAIC Health Policy’s intelligence and advocacy.',
        'og_title': 'Who We Are',
        'og_desc': 'Learn about MOSAIC’s bipartisan strategists, data analysts, and communicators delivering clarity for healthcare leaders.',
        'nav': 'who-we-are',
        'content': '''
<section class="section section--hero" aria-labelledby="page-title">
  <div class="section__inner" data-reveal>
    <p class="hero__eyebrow">Team</p>
    <h1 id="page-title" class="hero__title">Bipartisan, disciplined, all-in.</h1>
    <p class="hero__subtitle">MOSAIC blends Capitol veterans, data scientists, former hospital operators, and creative storytellers. We hire for judgment, humility, and outcomes.</p>
  </div>
</section>
<section class="section" aria-labelledby="values-heading">
  <div class="section__inner" data-reveal>
    <h2 id="values-heading">Values that guide every engagement</h2>
    <div class="card-grid">
      <div class="card">
        <h3 class="card__title">Clarity over noise</h3>
        <p>We filter the signal from Washington and deliver it in plain English with a recommendation attached.</p>
      </div>
      <div class="card">
        <h3 class="card__title">Integrity-first</h3>
        <p>Bipartisan trust is our currency—clients rely on our discretion, ethics, and accountability.</p>
      </div>
      <div class="card">
        <h3 class="card__title">Outcomes, not activity</h3>
        <p>We measure influence the way you measure business performance and pivot fast when conditions change.</p>
      </div>
    </div>
  </div>
</section>
<section class="section" aria-labelledby="bench-heading">
  <div class="section__inner" data-reveal>
    <h2 id="bench-heading">The bench</h2>
    <p>Our team includes former Senate and House committee staff, CMS and HHS leaders, state policy strategists, data visualization experts, and executive communications professionals. Together we cover policy, politics, analytics, and narrative design.</p>
    <p>We partner with MOSAIC Sentinel™ analysts, Precision Influence™ strategists, and creative studio leads to keep every engagement connected.</p>
  </div>
</section>
<section class="section" aria-labelledby="careers-heading">
  <div class="section__inner" data-reveal>
    <h2 id="careers-heading">Join the team</h2>
    <p>We’re growing. Explore <a href="/careers/">open roles</a> or send your résumé to <a href="mailto:talent@mosaicpolicy.com">talent@mosaicpolicy.com</a>.</p>
  </div>
</section>
'''
    },
    {
        'rel_path': 'careers/index.html',
        'title': 'Careers | MOSAIC Health Policy',
        'meta': 'Join MOSAIC Health Policy’s bipartisan team delivering intelligence, advocacy, and influence for healthcare leaders.',
        'og_title': 'Careers at MOSAIC',
        'og_desc': 'Help shape policy outcomes—explore careers at MOSAIC Health Policy.',
        'nav': 'careers',
        'content': '''
<section class="section section--hero" aria-labelledby="page-title">
  <div class="section__inner" data-reveal>
    <p class="hero__eyebrow">Careers</p>
    <h1 id="page-title" class="hero__title">Do work that moves policy—and people.</h1>
    <p class="hero__subtitle">We hire curious strategists who can translate complexity, build trust, and deliver outcomes under pressure.</p>
  </div>
</section>
<section class="section" aria-labelledby="roles-heading">
  <div class="section__inner" data-reveal>
    <h2 id="roles-heading">Current priorities</h2>
    <div class="card-grid">
      <div class="card">
        <h3 class="card__title">Senior Policy Strategist</h3>
        <p>Lead client engagements, craft policy analysis, and guide advocacy strategies. Capitol Hill or agency leadership experience preferred.</p>
      </div>
      <div class="card">
        <h3 class="card__title">Director, Precision Influence™</h3>
        <p>Design decision-network programs, manage analytics partners, and advise executives on influence plays.</p>
      </div>
      <div class="card">
        <h3 class="card__title">Creative Communications Lead</h3>
        <p>Translate insights into executive-ready decks, testimony, and digital content.</p>
      </div>
    </div>
  </div>
</section>
<section class="section" aria-labelledby="culture-heading">
  <div class="section__inner" data-reveal>
    <h2 id="culture-heading">How we work</h2>
    <ul>
      <li>Bipartisan respect and integrity—ideas win on merit.</li>
      <li>Remote-first with DC hub collaboration weeks.</li>
      <li>Professional development budgets and monthly learning labs.</li>
      <li>Competitive compensation, 401(k), generous leave, and wellness support.</li>
    </ul>
  </div>
</section>
<section class="section" aria-labelledby="apply-heading">
  <div class="section__inner" data-reveal>
    <h2 id="apply-heading">Apply or refer talent</h2>
    <p>Email <a href="mailto:talent@mosaicpolicy.com">talent@mosaicpolicy.com</a> with your résumé, a note on your policy passions, and availability. We respond within five business days.</p>
  </div>
</section>
'''
    },
    {
        'rel_path': 'contact/index.html',
        'title': 'Contact | MOSAIC Health Policy',
        'meta': 'Connect with MOSAIC Health Policy to request a briefing, schedule an advisory session, or learn about engagement options.',
        'og_title': 'Contact MOSAIC Health Policy',
        'og_desc': 'Request a briefing or start an engagement with MOSAIC Health Policy.',
        'nav': 'contact',
        'content': '''
<section class="section section--hero" aria-labelledby="page-title">
  <div class="section__inner" data-reveal>
    <p class="hero__eyebrow">Contact</p>
    <h1 id="page-title" class="hero__title">Let’s get your brief on the calendar.</h1>
    <p class="hero__subtitle">Share a few details and we’ll respond within one business day with the right MOSAIC experts.</p>
  </div>
</section>
<section class="section" aria-labelledby="form-heading">
  <div class="section__inner" data-reveal>
    <h2 id="form-heading">Start the conversation</h2>
    <form action="https://formsubmit.co/info@mosaicpolicy.com" method="post">
      <label for="name">Name</label>
      <input id="name" name="name" type="text" autocomplete="name" required>
      <label for="email">Email</label>
      <input id="email" name="email" type="email" autocomplete="email" required>
      <label for="organization">Organization</label>
      <input id="organization" name="organization" type="text" autocomplete="organization">
      <label for="message">Message</label>
      <textarea id="message" name="message" required></textarea>
      <input type="hidden" name="_next" value="https://mosaicpolicy.com/thank-you.html">
      <button class="btn btn-primary" type="submit">Submit</button>
      <small>By submitting you consent to MOSAIC contacting you about services. We never share your information.</small>
    </form>
  </div>
</section>
<section class="section" aria-labelledby="details-heading">
  <div class="section__inner" data-reveal>
    <h2 id="details-heading">Office &amp; media contact</h2>
    <p>409 7th Street NW, Suite 450, Washington, D.C. 20004</p>
    <p><a href="tel:2025039540">202-503-9540</a> · <a href="mailto:media@mosaicpolicy.com">media@mosaicpolicy.com</a></p>
  </div>
</section>
'''
    },
    {
        'rel_path': 'thank-you.html',
        'title': 'Thank You | MOSAIC Health Policy',
        'meta': 'Thank you for contacting MOSAIC Health Policy. A strategist will respond within one business day.',
        'og_title': 'Thank You',
        'og_desc': 'We received your message and will respond within one business day.',
        'nav': '',
        'content': '''
<section class="section" aria-labelledby="page-title">
  <div class="section__inner" data-reveal>
    <h1 id="page-title" class="hero__title">Thank you.</h1>
    <p>We received your message. A MOSAIC strategist will respond within one business day to coordinate next steps.</p>
    <p>Need immediate assistance? Call <a href="tel:2025039540">202-503-9540</a>.</p>
    <a class="btn btn-primary" href="/">Return to homepage</a>
  </div>
</section>
'''
    }
]


def main():
    for page in PAGES:
        rel = page['rel_path']
        canonical = canonical_for(rel)
        write_page(
            rel,
            title=page['title'],
            meta_description=page['meta'],
            og_title=page['og_title'],
            og_description=page['og_desc'],
            nav_current=page['nav'],
            content=page['content']
        )


if __name__ == '__main__':
    main()
