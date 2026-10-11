#!/usr/bin/env python3
"""Sailoxx static page generator.

Run:  python3 tools/build.py
Writes plain HTML into the project root and /products. The output is what gets deployed
to GitHub Pages; this script is only a convenience so the shared header, mega-menu and
footer live in one place. Content blocks that already existed on the v1 homepage are
reused from tools/src/home-v1.html so wording stays exactly as approved.
"""
import re, os, html, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import home_blocks

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = open(os.path.join(ROOT, 'tools/src/home-v1.html'), encoding='utf-8').read()
SITE = 'https://www.sailoxx.com/'
EMAIL = 'team@sailoxx.com'


def grab(pattern, text=SRC, flags=re.S):
    m = re.search(pattern, text, flags)
    if not m:
        raise SystemExit('missing block: ' + pattern)
    return m.group(0)


# ------------------------------------------------------------------ data
CATS = {
    'review': dict(name='AI Stack Review', unit='One-time', page='ai-stack-review.html',
                   blurb='The full governance report. One flat fee per review, paid before we begin.'),
    'focused': dict(name='Focused Reviews', unit='One-time', page='products.html#focused',
                    blurb='Single-area deep dives. One-time fee, 5-day delivery.'),
    'officer': dict(name='Fractional AI Officer', unit='Monthly', page='products.html#officer',
                    blurb='Ongoing AI advisory on a monthly retainer. Billed monthly, cancel anytime, with no annual lock-in.'),
    'pack': dict(name='AI Governance Policy Pack', unit='One-time', page='products/policy-pack.html',
                 blurb='A digital download for teams that want to start governing AI today, without a full review.'),
}

PRODUCTS = [
    dict(slug='stack-review-startup', cat='review', name='AI Stack Review: Startup', short='Startup',
         service='AI Stack Review — Startup', inr='₹18,000', usd='$220', per='',
         size='Up to 50 employees and up to 10 AI tools', delivery='5-day delivery',
         terms='One flat fee. Paid before we begin.', cta='Request this review',
         intro='The full AI Stack Review for companies with up to 50 employees and up to 10 AI tools. Every tool is mapped, assessed and given a clear verdict.',
         lead_in=None,
         items=['Complete AI tool inventory, every tool mapped', 'Adoption and usage analysis per tool',
                'Ghost and unused subscription detection', 'Duplicate tool and overlap analysis',
                'Shadow AI risk identification', 'KEEP, CUT, FIX and REPLACE verdicts',
                'AI Maturity Score (0 to 100)', 'Savings roadmap with exact amounts',
                'Executive PDF report', '30-minute executive debrief call']),
    dict(slug='stack-review-growth', cat='review', name='AI Stack Review: Growth', short='Growth',
         service='AI Stack Review — Growth', inr='₹35,000', usd='$420', per='',
         size='51 to 150 employees and up to 20 AI tools', delivery='5-day delivery',
         terms='One flat fee. Paid before we begin.', cta='Request this review',
         intro='The full AI Stack Review for companies with 51 to 150 employees and up to 20 AI tools, adding department-level analysis, per-tool ROI and a board-ready summary.',
         lead_in='Everything in Startup, plus:',
         items=['Department-by-department breakdown', 'ROI calculation per tool (time saved × hourly cost)',
                'Anonymous employee usage survey (up to 100 people)', 'Governance gap assessment',
                'Data risk report: unapproved tools handling company data',
                'Vendor renewal calendar with recommendations', 'Board-ready executive summary',
                '45-minute executive debrief call', 'Priority email support for 14 days after delivery']),
    dict(slug='stack-review-scale', cat='review', name='AI Stack Review: Scale', short='Scale',
         service='AI Stack Review — Scale', inr='₹65,000', usd='$780', per='',
         size='151 to 500 employees and unlimited AI tools', delivery='7-day delivery',
         terms='One flat fee. Paid before we begin.', cta='Request this review',
         intro='The full AI Stack Review for companies with 151 to 500 employees and no cap on the number of AI tools, with benchmarking, procurement recommendations and a spend projection.',
         lead_in='Everything in Growth, plus:',
         items=['Unlimited AI tool coverage, no cap', 'Full multi-department analysis',
                'Anonymous survey for unlimited employees',
                'Sector benchmarking against similar Indian companies',
                'AI procurement policy recommendations', '3-year AI spend projection model',
                'Investor or board presentation deck', '60-minute executive debrief with Q&A',
                '30-day WhatsApp support after delivery']),
    dict(slug='stack-review-enterprise', cat='review', name='AI Stack Review: Enterprise', short='Enterprise',
         service='AI Stack Review — Enterprise', inr='Custom', usd='Custom', per='',
         size='500+ employees', delivery='Custom delivery timeline',
         terms='Scoped and priced individually.', cta='Talk to us',
         intro='Custom scope and custom price for large organisations with complex multi-department AI stacks, regulated data environments or specific compliance requirements. We scope every engagement individually.',
         lead_in=None,
         items=['Multi-office support', 'Custom delivery timeline', 'Dedicated audit manager', 'NDA before scoping']),
    dict(slug='ai-tool-cost-map', cat='focused', name='AI Tool Cost Map', short='AI Tool Cost Map',
         service='AI Tool Cost Map', inr='₹8,000', usd='$97', per='',
         size='', delivery='5-day delivery', terms='One-time fee.', cta='Get this review',
         intro='A complete financial map of every AI subscription your company is running, including tools nobody remembers authorising.',
         lead_in=None,
         items=['Full paid tool inventory with verified costs', 'Ghost subscription identification',
                'Duplicate capability detection', 'Total monthly and annual spend summary',
                'Immediate cancellation recommendations']),
    dict(slug='ai-adoption-scan', cat='focused', name='AI Adoption Scan', short='AI Adoption Scan',
         service='AI Adoption Scan', inr='₹9,000', usd='$109', per='',
         size='', delivery='5-day delivery', terms='One-time fee.', cta='Get this review',
         intro='An anonymous employee survey showing which tools your team actually uses, trusts and finds valuable, and which ones are just billing you.',
         lead_in=None,
         items=['Anonymous survey sent to your team', 'Active usage rate per tool',
                'Employee trust and output quality scores', 'Time saved analysis',
                'Adoption gap report per department']),
    dict(slug='shadow-ai-risk-check', cat='focused', name='Shadow AI Risk Check', short='Shadow AI Risk Check',
         service='Shadow AI Risk Check', inr='₹12,000', usd='$145', per='',
         size='', delivery='5-day delivery', terms='One-time fee.', cta='Get this review',
         intro='A focused review of unapproved AI tool usage, finding where sensitive company data may be flowing into tools nobody sanctioned.',
         lead_in=None,
         items=['Shadow AI tool identification', 'Data exposure risk mapping',
                'Unapproved tools handling company data', 'Governance gap summary',
                'Immediate risk mitigation steps']),
    dict(slug='ai-vendor-renewal-review', cat='focused', name='AI Vendor Renewal Review', short='AI Vendor Renewal Review',
         service='AI Vendor Renewal Review', inr='₹6,500', usd='$79', per='',
         size='', delivery='5-day delivery', terms='One-time fee.', cta='Get this review',
         intro='An AI contract is coming up for renewal and you need to know whether to renew, reduce, replace or cancel. We give you the data to decide.',
         lead_in=None,
         items=['Usage and adoption analysis for that tool', 'License right-sizing recommendation',
                'Renew, cancel or replace verdict', 'Market price benchmark',
                'Negotiation brief for your finance team']),
    dict(slug='fractional-ai-officer-essential', cat='officer', name='Fractional AI Officer: Essential', short='Essential',
         service='Fractional AI Officer — Essential', inr='₹15,000', usd='$180', per='per month',
         size='4 hours included per month', delivery='', terms='Billed monthly. Cancel anytime.', cta='Start Essential',
         intro='Ongoing AI advisory on a monthly retainer, with 4 hours included each month.',
         lead_in=None,
         items=['Monthly 1-hour AI strategy call', 'Evaluation of any new AI tool before you buy it',
                'Monthly one-page AI spend update report', 'WhatsApp access for quick questions',
                'Renewal decision support when contracts come due', 'AI tool onboarding guide for new hires']),
    dict(slug='fractional-ai-officer-standard', cat='officer', name='Fractional AI Officer: Standard', short='Standard',
         service='Fractional AI Officer — Standard', inr='₹28,000', usd='$335', per='per month',
         size='8 hours included per month', delivery='', terms='Billed monthly. Cancel anytime.', cta='Start Standard',
         intro='Ongoing AI advisory on a monthly retainer, with 8 hours included each month and department-level guidance.',
         lead_in='Everything in Essential, plus:',
         items=['Monthly 2-hour strategy and planning session', 'Department-level AI tool recommendations',
                'Which departments should use which tools, and how much',
                'Automation opportunity identification per function', 'AI vendor negotiation support',
                'Quarterly AI Maturity Score update', 'AI usage policy drafting and updates',
                'Board-level AI reporting template', 'New AI tool pilot design and evaluation framework']),
    dict(slug='fractional-ai-officer-full', cat='officer', name='Fractional AI Officer: Full Engagement', short='Full Engagement',
         service='Fractional AI Officer — Full Engagement', inr='₹50,000', usd='$600', per='per month',
         size='15 hours included per month', delivery='', terms='Billed monthly. Cancel anytime.', cta='Start Full Engagement',
         intro='Ongoing AI advisory on a monthly retainer, with 15 hours included each month and a dedicated AI Officer for your company.',
         lead_in='Everything in Standard, plus:',
         items=['Dedicated AI Officer for your company', 'Weekly check-in calls with key stakeholders',
                'Full AI stack oversight and governance management',
                'Cross-department AI standardisation programme', 'AI implementation roadmap, 6 and 12 month',
                'ROI tracking system setup and monthly reporting', 'AI tool pilot management end to end',
                'Investor and board AI briefing preparation', 'Priority response within 4 hours on all days']),
    dict(slug='policy-pack', cat='pack', name='AI Governance Policy Pack', short='AI Governance Policy Pack',
         service='AI Governance Policy Pack', inr='₹4,999', usd='$60', per='',
         size='', delivery='Delivered within 5 days as PDF and editable DOCX', terms='One-time fee.', cta='Request the pack',
         intro='Ready-to-use policy documents with an India context, for your HR, IT or operations team to put into practice. No call needed.',
         lead_in=None,
         items=['AI Tool Usage Policy, employee-facing and ready to sign', 'AI Procurement Approval Process document',
                'Data Classification Guide for AI tool inputs', 'AI Vendor Evaluation Checklist (25 criteria)',
                'Board-level AI Reporting Template']),
]
BY_SLUG = {p['slug']: p for p in PRODUCTS}
OFFICER_NOTE = 'The Fractional AI Officer retainer is available to companies that have already completed an AI Stack Review with Sailoxx, or as a standalone engagement for companies with an existing clear understanding of their AI stack. First review, then ongoing advisory.'

NAV = [('problem.html', 'Problem', 'problem'), ('ai-stack-review.html', 'AI Stack Review', 'review'),
       ('process.html', 'Process', 'process'), ('products.html', 'Products &amp; Pricing', 'products'),
       ('get-started.html', 'Get Started', 'start'), ('faq.html', 'FAQ', 'faq')]

CLARITY = '''<script type="text/javascript">
  (function(c,l,a,r,i,t,y){
    c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
    t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
    y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
  })(window, document, "clarity", "script", "xhrq9xfqrm");
</script>'''

CHEV = '<svg width="12" height="12" viewBox="0 0 12 12" fill="none" aria-hidden="true"><path d="M2.5 4.5L6 8l3.5-3.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'
ARROW = '<svg width="14" height="14" viewBox="0 0 14 14" fill="none" aria-hidden="true"><path d="M2 7h10M8 3l4 4-4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'


def price_span(p):
    return f'<span data-inr="{p["inr"]}" data-usd="{p["usd"]}">{p["inr"]}</span>'


# ------------------------------------------------------------------ shared chrome
def head(path, depth, title, desc, noindex=False, jsonld='', og_title=None):
    pre = '../' * depth
    canon = SITE + path
    og_title = og_title or title
    robots = 'noindex, follow' if noindex else 'index, follow'
    home_css = '\n<link rel="stylesheet" href="assets/css/home.css">' if path == '' else ''
    og = '' if noindex else f'''
<meta property="og:type" content="website">
<meta property="og:url" content="{canon}">
<meta property="og:title" content="{html.escape(og_title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:image" content="{SITE}og-image.png">
<meta property="og:locale" content="en_IN">
<meta property="og:site_name" content="Sailoxx">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{html.escape(og_title)}">
<meta name="twitter:description" content="{html.escape(desc)}">
<meta name="twitter:image" content="{SITE}og-image.png">'''
    return f'''<!DOCTYPE html>
<html lang="en-IN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="author" content="Sailoxx">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{canon}">{og}
<link rel="icon" type="image/png" href="{pre}favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{pre}assets/css/site.css">{home_css}
<script>document.documentElement.classList.add('js');</script>{jsonld}
{CLARITY}
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
'''


MEGA_ICONS = {
    'review': '<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round" stroke-linecap="round" aria-hidden="true"><path d="M16 5 4.5 11 16 17l11.5-6L16 5Z"/><path d="m4.5 16 11.5 6 11.5-6"/><path d="m4.5 21 11.5 6 11.5-6"/></svg>',
    'focused': '<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" aria-hidden="true"><circle cx="14" cy="14" r="8.5"/><path d="m20.5 20.5 7 7"/></svg>',
    'officer': '<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="16" cy="11" r="4.4"/><path d="M7.5 26c.8-4.6 4-7.2 8.5-7.2s7.7 2.6 8.5 7.2"/><circle cx="6.5" cy="12.5" r="3"/><path d="M2 23.5c.4-3 2.2-4.7 4.8-5"/><circle cx="25.5" cy="12.5" r="3"/><path d="M30 23.5c-.4-3-2.2-4.7-4.8-5"/></svg>',
    'pack': '<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round" aria-hidden="true"><path d="M16 4 6 7.6v8.1c0 5.5 4 9.6 10 12.3 6-2.7 10-6.8 10-12.3V7.6L16 4Z"/><path d="M16 4v24" stroke-opacity=".0"/><path d="M16 10v13" stroke-linecap="round"/></svg>',
    'doc': '<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round" stroke-linecap="round" aria-hidden="true"><path d="M9 4h10l6 6v17a1 1 0 0 1-1 1H9a1 1 0 0 1-1-1V5a1 1 0 0 1 1-1Z"/><path d="M19 4v6h6M12 16h8M12 20h8M12 24h5"/></svg>',
    'check': '<svg viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="m4 8.4 2.7 2.6L12 5.6" stroke="#fff" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>',
}
MEGA_CARDS = [
    ('review', 'AI Stack Review', 'Full governance report', 'A complete review of your AI tools, spend, usage, and risks with a clear governance plan.', 'ai-stack-review.html', 'Explore AI Stack Review'),
    ('focused', 'Focused Reviews', 'Targeted insights', 'Short, focused reviews to solve specific AI challenges across cost, adoption, risk, or vendor decisions.', 'products.html#focused', 'Explore Focused Reviews'),
    ('officer', 'Fractional AI Officer', 'Ongoing leadership support', 'Strategic and hands-on support to help you adopt AI responsibly and create long-term value.', 'products.html#officer', 'Explore Fractional AI Officer'),
    ('pack', 'AI Governance Policy Pack', 'Policies and guidelines', 'Customizable AI governance policies, templates, and implementation guidance for your organization.', 'products/policy-pack.html', 'Explore Governance Policy Pack'),
]


def mega(pre):
    cards = ''
    for key, eyebrow, title, desc, href, cta in MEGA_CARDS:
        cards += (f'<a class="mc" href="{pre}{href}"><span class="mc-top"><span class="mc-ic">{MEGA_ICONS[key]}</span>'
                  f'<span class="mc-tx"><span class="mc-eb">{eyebrow}</span><span class="mc-ti">{title}</span><span class="mc-de">{desc}</span></span>'
                  f'</span>'
                  f'<span class="mc-foot">{cta}<span class="mc-go" aria-hidden="true">{ARROW}</span></span></a>')
    ticks_ = ''.join(f'<li><span aria-hidden="true">{MEGA_ICONS["check"]}</span>{t}</li>' for t in
                     ['Clear, practical recommendations', 'Plain language reports', 'Support from day one'])
    return f'''<div class="mega" id="mega" role="region" aria-label="Products and pricing">
<div class="wrap mega-inner">
<div class="mx">
<div class="mx-intro"><p class="mx-eyebrow">Our products</p><p class="mx-h">Practical AI governance and spend advisory for modern teams.</p>
<p class="mx-p">Focused services to help you understand, control, and get more value from your AI tools — from a one-time review to ongoing leadership support.</p>
<ul class="mx-ticks">{ticks_}</ul></div>
<div class="mx-cards">{cards}</div>
</div>
<div class="mx-bar"><span class="mx-bar-ic" aria-hidden="true">{MEGA_ICONS["doc"]}</span>
<div class="mx-bar-t"><span class="mx-eyebrow">Not sure which service fits?</span><span class="mx-bar-h">Talk to us about your goals.</span></div>
<p class="mx-bar-p">Book a free 20-minute consultation and we’ll help you choose the right engagement for your team.</p>
<a class="btn btn--primary" href="{pre}get-started.html">Book a consultation</a></div>
</div>
</div>'''


def header(pre, active):
    items = ''
    for href, label, key in NAV:
        cur = ' aria-current="page"' if key == active else ''
        if key == 'products':
            items += (f'<div class="nav-item has-mega"><a href="{pre}{href}"{cur}>{label}</a>'
                      f'<button class="mega-toggle" type="button" aria-expanded="false" aria-controls="mega" aria-label="Show products menu">{CHEV}</button>'
                      f'{mega(pre)}</div>')
        else:
            items += f'<div class="nav-item"><a href="{pre}{href}"{cur}>{label}</a></div>'
    # mobile
    mob = ''
    for href, label, key in NAV:
        cur = ' aria-current="page"' if key == active else ''
        if key == 'products':
            groups = ''
            for k in ['review', 'focused', 'officer', 'pack']:
                c = CATS[k]
                links = ''.join(f'<a href="{pre}products/{p["slug"]}.html">{p["short"] if k in ("review","officer") else p["name"]}'
                                f'<span>{price_span(p)}{(" " + p["per"]) if p["per"] else ""}</span></a>'
                                for p in PRODUCTS if p['cat'] == k)
                groups += f'<p class="m-cat">{c["name"]} <em>{c["unit"]}</em></p>{links}'
            mob += (f'<details class="m-acc"{" open" if active == "products" else ""}><summary>{label}</summary>'
                    f'<a href="{pre}{href}"{cur}>Overview and pricing</a>{groups}</details>')
        else:
            mob += f'<a href="{pre}{href}"{cur}>{label}</a>'
    return f'''<header class="site-header">
  <div class="wrap">
    <a class="brand" href="{pre}index.html" aria-label="Sailoxx home">
      <img src="{pre}assets/img/sailoxx-mark.png" width="43" height="40" alt="">
      <span class="brand-name">Sailoxx</span>
    </a>
    <nav class="nav" aria-label="Primary">{items}</nav>
    <a class="btn btn--primary btn--sm header-cta" href="{pre}get-started.html">Book a consultation</a>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="mobile-menu" aria-label="Open menu"><span></span></button>
  </div>
</header>
<div class="mobile-menu" id="mobile-menu">
{mob}
  <a class="btn btn--primary" href="{pre}get-started.html">Book a consultation</a>
</div>
'''


def footer(pre, home=False):
    home_js = '<script src="assets/js/home.js"></script>\n' if home else ''
    return f'''<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <a class="brand" href="{pre}index.html" aria-label="Sailoxx home">
          <img src="{pre}assets/img/sailoxx-mark.png" width="43" height="40" alt="">
          <span class="brand-name">Sailoxx</span>
        </a>
        <p class="footer-about">AI governance and spend advisory, based in India. We help companies review their AI stack, find hidden waste, surface unapproved tool risk, and build the governance their leadership needs.</p>
      </div>
      <div class="footer-col">
        <h2>Services</h2>
        <a href="{pre}ai-stack-review.html">AI Stack Review</a>
        <a href="{pre}products.html#focused">Focused Reviews</a>
        <a href="{pre}products.html#officer">Fractional AI Officer</a>
        <a href="{pre}products/policy-pack.html">AI Governance Policy Pack</a>
        <a href="{pre}products.html">Pricing</a>
      </div>
      <div class="footer-col">
        <h2>Company</h2>
        <a href="{pre}problem.html">The problem</a>
        <a href="{pre}process.html">How it works</a>
        <a href="{pre}faq.html">FAQ</a>
        <a href="{pre}get-started.html">Book a consultation</a>
        <a href="mailto:{EMAIL}">{EMAIL}</a>
      </div>
      <div class="footer-col">
        <h2>Legal</h2>
        <a href="{pre}privacy.html">Privacy Policy</a>
        <a href="{pre}terms.html">Terms of Service</a>
      </div>
    </div>
    <div class="footer-base"><span>© 2026 Sailoxx. All rights reserved.</span></div>
  </div>
</footer>
<script src="{pre}assets/js/site.js"></script>
{home_js}</body>
</html>
'''


def page_hero(pre, crumb, title, lead, actions='', extra=''):
    return f'''<section class="page-hero wash">
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="{pre}index.html">Home</a><span aria-hidden="true">/</span><span aria-current="page">{crumb}</span></nav>
    <h1 class="h1 hero-reveal">{title}</h1>
    <p class="lead hero-reveal d2">{lead}</p>
    {('<div class="hero-actions hero-reveal d2">' + actions + '</div>') if actions else ''}
    {extra}
  </div>
</section>
'''


def closing(pre, title='Stop guessing. Start knowing.',
            body='Tell us what you are trying to solve. In 20 minutes we will map your situation and tell you which service makes sense, with no pressure and no pitch.'):
    return f'''<section class="section closing wash wash--soft" aria-labelledby="closing-title">
  <div class="wrap closing-grid">
    <div>
      <h2 class="h2" id="closing-title">{title}</h2>
      <p class="lead" style="margin-top:1.5rem">{body}</p>
    </div>
    <div>
      <div class="hero-actions" style="margin-top:0">
        <a class="btn btn--primary" href="{pre}get-started.html">Book a free consultation</a>
        <a class="btn btn--secondary" href="{pre}problem.html#calculator">Estimate my spend first</a>
      </div>
      <p class="small" style="margin-top:1rem">No credit card. No commitment. Just a 20-minute conversation.</p>
    </div>
  </div>
</section>
'''


def currency_bar():
    return '''<div class="currency">
        <span class="small" id="currency-note">Prices exclude applicable taxes.</span>
        <div class="seg" role="group" aria-label="Currency">
          <button type="button" data-currency="INR" aria-pressed="true">₹ INR</button>
          <button type="button" data-currency="USD" aria-pressed="false">$ USD</button>
        </div>
      </div>'''


def ticks(items, lead_in=None):
    li = f'<li class="lead-in">{lead_in}</li>' if lead_in else ''
    return '<ul class="ticks">' + li + ''.join(f'<li>{i}</li>' for i in items) + '</ul>'


def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, 'w', encoding='utf-8').write(content)


def report_img(n, cls='', eager=False, w=794, h=1123):
    loading = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return (f'<img src="ai-stack-review/page-{n:02d}.webp" alt="Sample AI Stack Review, page {n}" width="{w}" height="{h}" '
            f'decoding="async" {loading} onerror="this.parentNode.classList.add(\'is-missing\');this.remove()">')


# ------------------------------------------------------------------ reusable v1 blocks
PROBLEM_LIST = grab(r'<ol class="problem-list">.*?</ol>')
PROBLEM_ITEMS = re.findall(r'<li>.*?</li>', PROBLEM_LIST, re.S)
STEP_BLOCKS = re.findall(r'<ol class="steps[^"]*">.*?</ol>', SRC, re.S)
PROCESS_STEPS, AFTER_STEPS = STEP_BLOCKS[0], STEP_BLOCKS[1]
CAROUSEL = grab(r'<div class="carousel" aria-roledescription.*?<p class="small carousel-note">.*?</p>\n    </div>')
EST = grab(r'<div class="wrap est">.*?</div>\n</section>')[:-len('</section>')]
FAQ = grab(r'<div class="faq">.*?</details>\n    </div>')
ABOUT = grab(r'<div class="wrap split">\s*<div>\s*<p class="tag">About Sailoxx.*?</dl>\n    </div>\n  </div>')
FORM = grab(r'<div class="wrap form-shell">.*?</div>\n</section>')[:-len('</section>')]
ASSURANCES = grab(r'<div class="assurances">.*?</div>\n  </div>')[:-len('\n  </div>')]
_slides = ''.join(
    f'<li class="cf-slide" data-i="{i}"><img src="ai-stack-review/page-{i+1:02d}.webp" alt="Sample AI Stack Review, page {i+1} of 15" width="900" height="1272" decoding="async"{" loading=\"lazy\"" if i > 2 else ""} draggable="false"></li>'
    for i in range(15))
CAROUSEL = f'''<div class="cf" aria-roledescription="carousel" aria-label="Sample AI Stack Review pages">
      <div class="cf-stage" tabindex="0" aria-label="Report pages. Use the left and right arrow keys to change page.">
        <ol class="cf-track">{_slides}</ol>
      </div>
      <div class="cf-controls">
        <button type="button" class="icon-btn" id="cf-prev" aria-label="Previous page"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 6l-6 6 6 6"/></svg></button>
        <span class="cf-count" id="cf-count" aria-live="polite">1 of 15</span>
        <button type="button" class="icon-btn" id="cf-next" aria-label="Next page"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 6l6 6-6 6"/></svg></button>
        <input class="cf-range" id="cf-range" type="range" min="1" max="15" value="1" step="1" aria-label="Go to page">
        <button type="button" class="icon-btn" id="cf-play" aria-label="Pause automatic slideshow" aria-pressed="false"><svg class="i-pause" width="14" height="14" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><rect x="6" y="5" width="4" height="14" rx="1"/><rect x="14" y="5" width="4" height="14" rx="1"/></svg><svg class="i-play" width="14" height="14" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M8 5v14l11-7z"/></svg></button>
      </div>
    </div>'''
for p in PRODUCTS:
    FORM = FORM.replace(f'value="{p["service"]}">', f'value="{p["service"]}" data-slug="{p["slug"]}">')
FORM = FORM.replace('<a href="privacy.html">', '<a href="privacy.html">')
EST = EST.replace('id="est-title"', 'id="est-title"')


# ------------------------------------------------------------------ pages
HOME_LOGO = 'assets/img/sailoxx-mark.png'


def home():
    pre = ''
    jsonld = '''
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"ProfessionalService","name":"Sailoxx","description":"AI spend audit and AI governance advisory service helping companies review their AI tools, identify unused subscriptions and unapproved tools, and manage AI spend.","url":"https://www.sailoxx.com","areaServed":"IN","serviceType":"AI Spend Audit","offers":{"@type":"Offer","name":"AI Stack Review: Startup","price":"18000","priceCurrency":"INR"}}
</script>'''
    out = head('', 0, 'Sailoxx — AI Spend Audit | Know Which AI Tools Are Worth Keeping',
               "Sailoxx reviews your company's AI tools and AI spend and delivers a clear report in 5 days: what to keep, cut, fix or replace. AI Stack Reviews start at ₹18,000.",
               jsonld=jsonld, og_title='Sailoxx — Know Which AI Tools Are Actually Worth Your Money')
    out += header(pre, 'home')
    out += '<main id="main">\n'
    out += f'''
{home_blocks.hero(HOME_LOGO)}
{home_blocks.flow()}

<section class="section wash wash--band" aria-labelledby="problem-title">
  <div class="wrap split">
    <div>
      <p class="tag" style="margin-bottom:1rem">The problem</p>
      <h2 class="h2" id="problem-title">Most companies adopting AI cannot see the full picture.</h2>
      <p class="lead" style="margin-top:1.5rem">Tools get bought team by team, renewals roll over, and nobody owns the total. These are the patterns an AI spend review is built to surface.</p>
      <p style="margin-top:2rem"><a class="btn btn--secondary" href="problem.html">Read the full problem</a></p>
    </div>
    <ol class="problem-list">{''.join(PROBLEM_ITEMS[:3])}</ol>
  </div>
</section>

<section class="section" aria-labelledby="process-title">
  <div class="wrap">
    <div class="sec-head">
      <p class="tag">How it works</p>
      <h2 class="h2" id="process-title" style="margin-top:1rem">Five days to a clear answer.</h2>
      <p class="lead">Low friction for your team, high precision in the output. No lengthy consultancy engagement and no disruption to your workflow.</p>
    </div>
    {PROCESS_STEPS}
    <p style="margin-top:2rem"><a class="link-arrow" href="process.html">See the full process {ARROW}</a></p>
  </div>
</section>

<section class="section wash wash--band sp-sec" aria-labelledby="inside-title">
  <div class="wrap inside sp-wrap">
    <div>
      <p class="hx-eyebrow">Sample AI Stack Review</p>
      <h2 class="h2 sp-title" id="inside-title" style="margin-top:1rem">See the decisions behind the numbers.</h2>
      <p class="lead" style="margin-top:1.5rem">Explore a sample of the analysis, tool-by-tool findings and executive action plan Sailoxx delivers.</p>
      <div class="hero-actions"><a class="btn btn--primary" href="ai-stack-review.html">Explore the sample report</a></div>
    </div>
    <div class="spv" aria-label="Sample AI Stack Review pages">
      <div class="spw spw-1"><img class="sp" src="assets/img/sample-tool-usage.webp" alt="Sample report page: Tool Usage Analysis for ChatGPT and Claude" width="800" height="1131" loading="lazy" decoding="async"></div>
      <div class="spw spw-3"><img class="sp" src="assets/img/sample-action-roadmap.webp" alt="Sample report page: Action Roadmap" width="800" height="1131" loading="lazy" decoding="async"></div>
      <div class="spw spw-2"><img class="sp" src="assets/img/sample-exec-summary.webp" alt="Sample report page: Executive Summary" width="800" height="1131" loading="lazy" decoding="async"></div>
    </div>
  </div>
</section>

<section class="section" id="about" aria-labelledby="about-title">
  {ABOUT.replace('<p class="tag">About Sailoxx</p>', '<p class="tag">About Sailoxx</p>')}
</section>
'''
    out += closing(pre)
    out += '</main>\n' + footer(pre, home=True)
    write('index.html', out)


def simple_page(path, active, title, desc, crumb, h1, lead, body, actions=''):
    pre = ''
    out = head(path, 0, title, desc)
    out += header(pre, active) + '<main id="main">\n'
    out += page_hero(pre, crumb, h1, lead, actions)
    out += body
    out += '</main>\n' + footer(pre)
    write(path, out)


def problem_page():
    body = f'''
<section class="section" aria-labelledby="problem-title">
  <div class="wrap split split--sticky">
    <div>
      <p class="tag" style="margin-bottom:1rem">The problem</p>
      <h2 class="h2" id="problem-title">Most companies adopting AI cannot see the full picture.</h2>
      <p class="lead" style="margin-top:1.5rem">These are the patterns an AI spend review is built to surface.</p>
    </div>
    {PROBLEM_LIST}
  </div>
</section>
<section class="section section--tint" id="calculator" aria-labelledby="est-title">
  <span id="checker"></span>
  {EST}
</section>
{closing('')}'''
    simple_page('problem.html', 'problem', 'The Problem: AI Spend Nobody Can See | Sailoxx',
                'Duplicate tools, ghost subscriptions, no ROI visibility. The patterns a Sailoxx AI spend review is built to surface, and a planning estimator for your own spend.',
                'Problem', 'AI tools are bought team by team. Nobody sees the total.',
                'Adoption moved faster than oversight. Here is what that usually looks like inside a company, and a quick way to size your own exposure.', body,
                '<a class="btn btn--primary" href="get-started.html">Book a free consultation</a><a class="btn btn--secondary" href="#calculator">Estimate my spend</a>')


def review_page():
    startup = BY_SLUG['stack-review-startup']
    rows = ''
    for p in [x for x in PRODUCTS if x['cat'] == 'review']:
        rows += (f'<a class="cmp-row" href="products/{p["slug"]}.html"><span class="cmp-name">{p["short"]}</span>'
                 f'<span class="cmp-size">{p["size"]}</span><span class="cmp-del">{p["delivery"]}</span>'
                 f'<span class="cmp-price">{price_span(p)}</span><span class="cmp-go" aria-hidden="true">{ARROW}</span></a>')
    body = f'''
<section class="section wash wash--band cf-sec" aria-labelledby="review-title">
  <div class="wrap">
    <div class="sec-head">
      <p class="tag">Sample AI Stack Review</p>
      <h2 class="h2" id="review-title" style="margin-top:1rem">See exactly what your review looks like.</h2>
      <p class="lead">A look inside the analysis, findings and executive recommendations Sailoxx delivers. Report length scales with your company size and the number of AI tools in use.</p>
    </div>
    {CAROUSEL}
    <div class="cta-row">
      <a class="btn btn--primary" href="get-started.html?service=stack-review-growth">Request your AI Stack Review</a>
      <div class="dl-wrap">
        <a class="btn btn--secondary" href="downloads/Sailoxx-Sample-AI-Stack-Review.pdf" download="Sailoxx-Sample-AI-Stack-Review.pdf">Download sample report</a>
        <span class="small dl-note">No sign up or email needed.</span>
      </div>
    </div>
  </div>
</section>
<section class="section section--tint" aria-labelledby="inc-title">
  <div class="wrap split">
    <div>
      <p class="tag" style="margin-bottom:1rem">What every review includes</p>
      <h2 class="h2" id="inc-title">The full governance report, scaled to your company.</h2>
      <p class="lead" style="margin-top:1.5rem">All three tiers start from the same core. Larger tiers add depth, not a different method.</p>
    </div>
    <div>{ticks(startup['items'])}</div>
  </div>
</section>
<section class="section" aria-labelledby="tiers-title">
  <div class="wrap">
    <div class="sec-head">
      <h2 class="h2" id="tiers-title">Choose the review that fits your size</h2>
      <p class="lead">One flat fee per review, paid before we begin. Each tier has its own page with the full list of what is included.</p>
    </div>
    <div class="cmp" style="margin-top:2.5rem">{rows}</div>
    {currency_bar().replace('class="currency"', 'class="currency currency--inline"')}
  </div>
</section>
{closing('')}'''
    simple_page('ai-stack-review.html', 'review', 'AI Stack Review: Sample Report and Tiers | Sailoxx',
                'Browse a sample AI Stack Review and compare the Startup, Growth, Scale and Enterprise tiers. Reviews start at ₹18,000.',
                'AI Stack Review', 'A full governance report on every AI tool you run.',
                'Every tool mapped, assessed and given a verdict: keep, cut, fix or replace, with a savings roadmap in exact rupee amounts.', body,
                '<a class="btn btn--primary" href="#tiers-title">Compare tiers</a><a class="btn btn--secondary" href="#review-title">See the sample report</a>')


def process_page():
    body = f'''
<section class="section" aria-labelledby="process-title">
  <div class="wrap">
    <div class="sec-head">
      <p class="tag">How it works</p>
      <h2 class="h2" id="process-title" style="margin-top:1rem">Five days to a clear answer.</h2>
      <p class="lead">Low friction for your team, high precision in the output. No lengthy consultancy engagement and no disruption to your workflow.</p>
    </div>
    {PROCESS_STEPS}
  </div>
</section>
<section class="section section--tint" aria-labelledby="after-title">
  <div class="wrap">
    <div class="sec-head">
      <p class="tag">What to expect</p>
      <h2 class="h2" id="after-title" style="margin-top:1rem">What happens after you book.</h2>
    </div>
    {AFTER_STEPS}
  </div>
</section>
{closing('')}'''
    simple_page('process.html', 'process', 'How It Works: A 5-Day AI Stack Review | Sailoxx',
                'From discovery call to executive report in 5 days: tool inventory, employee survey, ROI calculation and a plain-English report. No system access needed.',
                'Process', 'From discovery call to report in five days.',
                'No system access, no login credentials, and under two hours of your team’s time across the whole review.', body,
                '<a class="btn btn--primary" href="get-started.html">Book a free consultation</a>')


def products_page():
    sections = ''
    for key in ['review', 'focused', 'officer', 'pack']:
        c = CATS[key]
        rows = ''
        for p in [x for x in PRODUCTS if x['cat'] == key]:
            sub = p['size'] or p['intro']
            per = f'<span class="per">{p["per"]}</span>' if p['per'] else ''
            rows += (f'<a class="prod-row" href="products/{p["slug"]}.html"><span class="pr-name">{p["short"] if key in ("review","officer") else p["name"]}</span>'
                     f'<span class="pr-desc">{sub}</span>'
                     f'<span class="pr-price"><b>{price_span(p)}</b>{per}<small>{c["unit"]}</small></span>'
                     f'<span class="pr-go" aria-hidden="true">{ARROW}</span></a>')
        note = f'<p class="note-box">{OFFICER_NOTE}</p>' if key == 'officer' else ''
        sections += f'''<section class="section prod-sec{' section--tint' if key in ('focused','pack') else ''}" id="{key}" aria-labelledby="{key}-t">
  <div class="wrap split">
    <div><h2 class="h3" id="{key}-t">{c["name"]}</h2><p class="small" style="margin-top:.75rem">{c["unit"]}</p><p class="prose" style="margin-top:1rem">{c["blurb"]}</p></div>
    <div><div class="prod-list">{rows}</div>{note}</div>
  </div>
</section>
'''
    body = f'''
<section class="section" style="padding-bottom:0">
  <div class="wrap">{currency_bar()}</div>
</section>
{sections}
<section class="section" aria-labelledby="assure-title">
  <div class="wrap"><h2 class="visually-hidden" id="assure-title">Our commitments</h2>
  {ASSURANCES}
  </div>
</section>
{closing('')}'''
    simple_page('products.html', 'products', 'Products and Pricing | Sailoxx',
                'Every Sailoxx service with fixed prices: AI Stack Review from ₹18,000, Focused Reviews from ₹6,500, Fractional AI Officer from ₹15,000 per month, Policy Pack ₹4,999.',
                'Products &amp; Pricing', 'Every service we offer, and exactly what you pay.',
                'Transparent, fixed pricing. No lengthy proposals and no surprise invoices. Choose the engagement that fits, or start with a free discovery call.', body)


def faq_page():
    body = f'''
<section class="section" aria-labelledby="faq-title">
  <div class="wrap split">
    <div><h2 class="h2" id="faq-title">Common questions</h2><p class="lead" style="margin-top:1.5rem">Cannot find yours? Ask on a free discovery call or write to <a href="mailto:{EMAIL}">{EMAIL}</a>.</p></div>
    {FAQ}
  </div>
</section>
{closing('')}'''
    simple_page('faq.html', 'faq', 'FAQ | Sailoxx AI Spend Audit',
                'Answers on system access, time required from your team, survey anonymity, small AI stacks and what happens after an AI Stack Review.',
                'FAQ', 'Common questions, answered plainly.',
                'Access, time, anonymity and what happens after the report.', body)


def start_page():
    body = f'''
<section class="section" id="forms" aria-labelledby="forms-title">
  {FORM}
</section>
<section class="section section--tint" aria-labelledby="after-title">
  <div class="wrap">
    <div class="sec-head">
      <p class="tag">What to expect</p>
      <h2 class="h2" id="after-title" style="margin-top:1rem">What happens after you book.</h2>
    </div>
    {AFTER_STEPS}
  </div>
</section>'''
    simple_page('get-started.html', 'start', 'Book a Consultation | Sailoxx',
                'Book a free 20-minute discovery call. Tell us about your company and AI tools and we will reply within one business day.',
                'Get Started', 'Book a free consultation.',
                'A 20-minute conversation. We will tell you honestly whether a review would find meaningful savings.', body)


def product_pages():
    for p in PRODUCTS:
        pre = '../'
        c = CATS[p['cat']]
        siblings = [x for x in PRODUCTS if x['cat'] == p['cat'] and x is not p]
        sib = ''.join(f'<a class="rel" href="{x["slug"]}.html"><span>{x["name"]}</span><b>{price_span(x)}{(" " + x["per"]) if x["per"] else ""}</b></a>' for x in siblings)
        per = f'<span class="per">{p["per"]}</span>' if p['per'] else ''
        facts = ''
        if p['size']:
            facts += f'<div><dt>Best suited to</dt><dd>{p["size"]}</dd></div>'
        if p['delivery']:
            facts += f'<div><dt>Delivery</dt><dd>{p["delivery"]}</dd></div>'
        facts += f'<div><dt>Billing</dt><dd>{p["terms"]}</dd></div>'
        note = f'<p class="note-box">{OFFICER_NOTE}</p>' if p['cat'] == 'officer' else ''
        if p['slug'] == 'stack-review-enterprise':
            price_html = '<p class="tier-price"><b>Custom</b></p>'
        else:
            price_html = f'<p class="tier-price"><b>{price_span(p)}</b>{per}</p>'
        inc_title = 'What is included' if p['slug'] != 'stack-review-enterprise' else 'What Enterprise adds'
        out = head(f'products/{p["slug"]}.html', 1, f'{p["name"]} | Sailoxx',
                   f'{p["intro"]}')
        out += header(pre, 'products') + '<main id="main">\n'
        out += f'''<section class="page-hero wash">
  <div class="wrap prod-hero">
    <div>
      <nav class="crumbs" aria-label="Breadcrumb"><a href="../index.html">Home</a><span aria-hidden="true">/</span><a href="../products.html">Products &amp; Pricing</a><span aria-hidden="true">/</span><span aria-current="page">{p["name"]}</span></nav>
      <p class="tag hero-reveal">{c["name"]}, {c["unit"].lower()}</p>
      <h1 class="h1 hero-reveal" style="margin-top:1rem">{p["name"]}</h1>
      <p class="lead hero-reveal d2">{p["intro"]}</p>
    </div>
    <aside class="buy-panel hero-reveal d2" aria-label="Pricing">
      <div class="stage-frame"><div class="stage-inner buy-inner">
        <p class="small">{c["unit"]}</p>
        {price_html}
        <p class="tier-terms">{p["terms"]}</p>
        {('<p class="tier-delivery">' + p["delivery"] + '</p>') if p["delivery"] else ''}
        <a class="btn btn--primary btn--block" href="../get-started.html?service={p["slug"]}">{p["cta"]}</a>
        <div class="seg-wrap">{currency_bar()}</div>
      </div></div>
    </aside>
  </div>
</section>
<section class="section" aria-labelledby="inc-title">
  <div class="wrap split">
    <div>
      <h2 class="h2" id="inc-title">{inc_title}</h2>
      <dl class="facts facts--stack" style="margin-top:2rem">{facts}</dl>
    </div>
    <div>{ticks(p["items"], p["lead_in"])}{note}</div>
  </div>
</section>
<section class="section section--tint" aria-labelledby="rel-title">
  <div class="wrap split">
    <div><h2 class="h3" id="rel-title">{('Compare with the other ' + c["name"] + ' options') if siblings else 'Not the right fit?'}</h2>
    <p class="small" style="margin-top:.75rem">{('Each option has its own page.') if siblings else 'See every service, or talk to us first.'}</p></div>
    <div class="rel-list">{sib}<a class="rel" href="../products.html"><span>All products and pricing</span><b>{ARROW}</b></a></div>
  </div>
</section>
{closing(pre)}
</main>
'''
        out += footer(pre)
        write(f'products/{p["slug"]}.html', out)


def legal_pages():
    for name, title in (('privacy', 'Privacy Policy'), ('terms', 'Terms of Service')):
        v1 = open(os.path.join(ROOT, f'tools/src/{name}-v1.html'), encoding='utf-8').read()
        main = grab(r'<main id="main" class="legal">.*?</main>', v1)
        desc = re.search(r'<meta name="description" content="([^"]*)"', v1).group(1)
        out = head(f'{name}.html', 0, f'{title} (Draft) | Sailoxx', desc, noindex=True)
        out += header('', 'legal') + main + '\n' + footer('')
        write(f'{name}.html', out)


def sitemap():
    urls = ['', 'problem.html', 'ai-stack-review.html', 'process.html', 'products.html', 'get-started.html', 'faq.html'] + \
           [f'products/{p["slug"]}.html' for p in PRODUCTS]
    x = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + \
        ''.join(f'  <url><loc>{SITE}{u}</loc></url>\n' for u in urls) + '</urlset>\n'
    write('sitemap.xml', x)
    write('robots.txt', f'User-agent: *\nAllow: /\nSitemap: {SITE}sitemap.xml\n')


if __name__ == '__main__':
    home(); problem_page(); review_page(); process_page(); products_page(); faq_page(); start_page()
    product_pages(); legal_pages(); sitemap()
    print('built', 7 + len(PRODUCTS) + 2, 'pages')
