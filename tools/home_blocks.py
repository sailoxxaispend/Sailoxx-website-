"""Homepage-only blocks: the light hero (three report pages) and the dark workflow section.
Plain strings (no f-strings) so CSS-style braces never need escaping."""
import math

IC = {
    'grid': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round" aria-hidden="true"><rect x="4" y="4" width="6.5" height="6.5" rx="1.2"/><rect x="13.5" y="4" width="6.5" height="6.5" rx="1.2"/><rect x="4" y="13.5" width="6.5" height="6.5" rx="1.2"/><rect x="13.5" y="13.5" width="6.5" height="6.5" rx="1.2"/></svg>',
    'rupee': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 5h10M7 9.5h10M7 5h2.5a4 4 0 0 1 0 8H7l7.5 6.5"/></svg>',
    'shield': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round" aria-hidden="true"><path d="M12 3.5 5 6v5.5c0 4.2 2.8 7.4 7 9 4.2-1.6 7-4.8 7-9V6l-7-2.5Z"/></svg>',
    'bars': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 19.5V13M10 19.5V6.5M15 19.5v-9M20 19.5V11"/><path d="M3.5 19.5h17"/></svg>',
    'doc': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round" stroke-linecap="round" aria-hidden="true"><path d="M7 3.5h7l4 4V20a.5.5 0 0 1-.5.5h-10A.5.5 0 0 1 7 20V3.5Z"/><path d="M14 3.5V8h4M9.5 12.5h5M9.5 16h5"/></svg>',
    'scan': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 8V5.5A1.5 1.5 0 0 1 5.5 4H8M16 4h2.5A1.5 1.5 0 0 1 20 5.5V8M20 16v2.5a1.5 1.5 0 0 1-1.5 1.5H16M8 20H5.5A1.5 1.5 0 0 1 4 18.5V16"/><circle cx="12" cy="12" r="2.6"/></svg>',
    'pulse': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3.5 14.5 8 10l3.5 3.5 4-6 5 5.5"/></svg>',
    'people': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="9" cy="8.5" r="3.2"/><path d="M3.5 19c.5-3.2 2.7-5 5.5-5s5 1.8 5.5 5"/><path d="M15.5 5.6a3 3 0 0 1 0 5.8M17 14.4c2 .5 3.2 2.1 3.5 4.6"/></svg>',
}
ARROW_SM = '<svg viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M3 8h9M8.5 4l4 4-4 4" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/></svg>'


def ribbon():
    """Fine contour lines sweeping from the bottom-left to the top-right of the cover page (310 x 435)."""
    A = [(0, 435), (95, 335), (135, 205), (238, 0)]
    B = [(215, 435), (180, 335), (258, 205), (305, 0)]
    def lerp(t):
        return [(a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t) for a, b in zip(A, B)]
    def d(c):
        return 'M%.1f %.1f C%.1f %.1f %.1f %.1f %.1f %.1f' % (c[0] + c[1] + c[2] + c[3])
    n = 40
    lines = []
    for i in range(n):
        t = i / (n - 1)
        op = .08 + .42 * math.sin(math.pi * t) ** 1.4
        lines.append('<path d="%s" stroke="#49a38c" stroke-opacity="%.2f" stroke-width=".5"/>' % (d(lerp(t)), op))
    ca, cb = lerp(0.18), lerp(0.82)
    fill = d(ca) + ' L%.1f %.1f C%.1f %.1f %.1f %.1f %.1f %.1f Z' % (cb[3][0], cb[3][1], cb[2][0], cb[2][1], cb[1][0], cb[1][1], cb[0][0], cb[0][1])
    core = lerp(0.62)
    return ('<svg class="pg-ribbon" viewBox="0 0 310 435" preserveAspectRatio="xMidYMid slice" fill="none" aria-hidden="true">'
            '<defs><linearGradient id="rb" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="#49a38c" stop-opacity=".02"/>'
            '<stop offset=".55" stop-color="#49a38c" stop-opacity=".22"/><stop offset="1" stop-color="#8fd6c0" stop-opacity=".06"/></linearGradient></defs>'
            '<path d="%s" fill="url(#rb)"/>' % fill + ''.join(lines)
            + '<path d="%s" stroke="#49a38c" stroke-opacity=".7" stroke-width="1.4"/>' % d(core) + '</svg>')


def hero(logo_src):
    bars = [('Productivity', '₹72,000', 80), ('Engineering', '₹56,000', 62), ('Design', '₹48,000', 50),
            ('Marketing', '₹32,000', 32), ('Other', '₹40,000', 44)]
    bar_html = ''.join(
        '<li><span>%s</span><i style="--w:%d%%;--d:%.2fs"></i><b>%s</b></li>' % (n, w, 1.15 + k * .12, v)
        for k, (n, v, w) in enumerate(bars))
    return '''
<section class="hx" aria-labelledby="hero-title">
  <div class="hx-bg" aria-hidden="true"></div>
  <div class="wrap hx-grid">
    <div class="hx-copy">
      <p class="hx-eyebrow hero-reveal">AI governance and spend advisory</p>
      <h1 class="hx-title hero-reveal" id="hero-title">Know what your AI tools cost, and what they return.</h1>
      <p class="hx-lead hero-reveal d2">We map every AI tool your company runs, find what is wasting money, identify unapproved tools handling sensitive data, and give your leadership a clear governance plan. Delivered in 5 days, in plain language.</p>
    </div>
    <figure class="hx-pages" aria-label="Sample AI Stack Review report pages">
      <div class="fit" data-fit-w="800" data-fit-h="545"><div class="fit-inner pages">
        <div class="pgw pgw-3" style="--rot:2deg"><div class="pg pg-3">
          <h3>Risk Overview</h3>
          <svg class="donut" viewBox="0 0 120 120" aria-hidden="true"><circle cx="60" cy="60" r="44" fill="none" stroke="#bfe0d4" stroke-width="18"/><circle class="donut-arc" cx="60" cy="60" r="44" fill="none" stroke="#2f9179" stroke-width="18" stroke-dasharray="105 276.5" transform="rotate(-90 60 60)"/></svg>
          <div class="donut-label"><b>38%</b><span>Unapproved<br>Tools</span></div>
          <ul class="legend"><li><i style="background:#bfe0d4"></i>Approved<b>12</b></li><li><i style="background:#2f9179"></i>Unapproved<b>9</b></li><li><i style="background:#7cc4ae"></i>Needs review<b>4</b></li></ul>
        </div></div>
        <div class="pgw pgw-1"><div class="pg pg-1">
          ''' + ribbon() + '''
          <div class="pg-brand"><img src="''' + logo_src + '''" alt="" width="28" height="26"><span>Sailoxx</span></div>
          <h3>AI Stack<br>Review Report</h3>
          <p>Your AI tools. Your spend.<br>Your risks. Your next steps.</p>
          <hr>
        </div></div>
        <div class="pgw pgw-2"><div class="pg pg-2">
          <h3>Executive Summary</h3>
          <div class="tiles"><div><b>23</b><span>AI tools identified</span></div><div><b>₹2,48,000</b><span>Estimated annual spend</span></div><div><b>38%</b><span>Unapproved tools</span></div><div><b>4</b><span>High-risk tools</span></div></div>
          <h4>Key Findings</h4>
          <p class="cap">Spend by Category</p>
          <ul class="bars">''' + bar_html + '''</ul>
        </div></div>
      </div></div>
    </figure>
  </div>

  <div class="wrap">
    <div class="ask stage-frame hero-reveal d2">
      <div class="ask-inner">
        <div class="ask-bar">
          <span class="orb" aria-hidden="true"></span>
          <p>How can Sailoxx help your business with AI?</p>
          <a class="ask-btn" href="get-started.html">Book a free consultation<span aria-hidden="true">''' + ARROW_SM + '''</span></a>
        </div>
        <ul class="ask-chips">
          <li><a href="problem.html#calculator">AI spend</a></li>
          <li><a href="products/shadow-ai-risk-check.html">Tool governance</a></li>
          <li><a href="products/ai-adoption-scan.html">AI adoption</a></li>
        </ul>
      </div>
    </div>
    <ul class="hx-facts">
      <li>Independent. We earn no commissions from any AI vendor.</li>
      <li>No login credentials or system access needed.</li>
      <li>Mutual NDA signed before any engagement begins.</li>
      <li>Delivered in 5 days (7 days for the Scale review).</li>
    </ul>
  </div>
</section>
'''


def flow():
    def lcard(i, y, icon, t, s):
        return ('<div class="dg-card dg-l" style="--x:25px;--y:%dpx;--w:224px;--h:89px;--i:%d"><span class="ic">%s</span><div><b>%s</b><span>%s</span></div></div>'
                % (y, i, IC[icon], t, s))

    def row(i, y, icon, t):
        return ('<div class="dg-row" style="--x:22px;--y:%dpx;--i:%d"><span class="ic">%s</span><b>%s</b></div>' % (y, i, IC[icon], t))

    def rcard(i, y, icon, t, s):
        return ('<div class="dg-out" style="--x:672px;--y:%dpx;--w:279px;--h:%dpx;--i:%d"><span class="ic">%s</span><div><b>%s</b><span>%s</span></div></div>'
                % (y, 83 if i < 2 else 86, i, IC[icon], t, s))

    lpaths = ['M249 133 C300 133 300 243 338 243', 'M249 238 C300 238 300 265 338 265',
              'M249 342 C300 342 300 310 338 310', 'M249 447 C300 447 300 333 338 333']
    rpaths = ['M588 243 C630 243 625 143 666 143', 'M588 265 C630 265 625 240 666 240',
              'M588 310 C630 310 625 335 666 335', 'M588 333 C630 333 625 435 666 435']
    svg = ('<svg class="dg-lines" viewBox="0 0 960 630" aria-hidden="true"><defs>'
           '<marker id="ah" viewBox="0 0 8 8" refX="6" refY="4" markerWidth="7" markerHeight="7" orient="auto"><path d="M1 1l5 3-5 3" fill="none" stroke="#49d3a4" stroke-opacity=".8" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/></marker>'
           '<marker id="au" viewBox="0 0 8 8" refX="4" refY="2" markerWidth="7" markerHeight="7" orient="auto"><path d="M1 6 4 1l3 5" fill="none" stroke="#49d3a4" stroke-opacity=".8" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/></marker></defs>'
           + ''.join('<path d="%s" marker-end="url(#ah)"/>' % p for p in lpaths + rpaths)
           + '<path d="M25 492 H4 V150" marker-end="url(#au)" class="faint"/>'
           + '<path d="M444 535 H117 V506" marker-end="url(#au)" class="dash"/>'
           + '<path d="M488 535 H813 V506" marker-end="url(#au)" class="dash"/></svg>')
    dots = ''
    for k, p in enumerate(lpaths):
        dots += '<i class="dot dot-a" style="offset-path:path(\'%s\');--j:%d"></i>' % (p, k)
    for k, p in enumerate(rpaths):
        dots += '<i class="dot dot-b" style="offset-path:path(\'%s\');--j:%d"></i>' % (p, k)
    dots += '<i class="dot dot-c" style="offset-path:path(\'M444 535 H117 V510\')"></i>'
    dots += '<i class="dot dot-c" style="offset-path:path(\'M488 535 H813 V510\')"></i>'

    return '''
<section class="dk" aria-labelledby="flow-title">
  <div class="dk-bg" aria-hidden="true"></div>
  <div class="wrap dk-grid">
    <div class="dk-copy">
      <p class="dk-pill"><i aria-hidden="true"></i>AI governance &amp; spend advisory</p>
      <h2 class="dk-title" id="flow-title">From AI spend<br>to strategic<br><em>business value.</em></h2>
      <p class="dk-lead">We help you understand what AI tools your team actually uses, uncover wasted spend and hidden risks, and give you a clear governance plan, so you can adopt AI with confidence.</p>
      <div class="dk-actions">
        <a class="dk-btn" href="ai-stack-review.html">Explore AI Stack Review<span aria-hidden="true">''' + ARROW_SM + '''</span></a>
        <a class="dk-link" href="get-started.html"><span aria-hidden="true">''' + IC['people'] + '''</span>Book a free consultation</a>
      </div>
    </div>
    <div class="dg-wrap">
      <div class="fit" data-fit-w="960" data-fit-h="630" data-fit-min="700"><div class="fit-inner dg" role="img" aria-label="How Sailoxx works: your AI landscape is analysed by Sailoxx and turned into clear outcomes, with ongoing support.">
        ''' + svg + '''
        <div class="dg-g dg-g1">
          <div class="dg-head dg-h1" style="--x:30px;--y:3px"><span class="badge" style="--b:0s">1</span><div><b>Your AI landscape</b><span>Bring all your AI usage and spend data into one place</span></div></div>
          ''' + lcard(0, 89, 'grid', 'All AI tools', 'Discover what your team uses') + lcard(1, 194, 'rupee', 'AI spend', 'See where your money goes') + lcard(2, 298, 'shield', 'Risks', 'Identify unapproved and high-risk tools') + lcard(3, 402, 'bars', 'Usage &amp; adoption', 'Understand how tools are used') + '''
        </div>
        <div class="dg-g dg-g2">
          <div class="dg-panel" style="--x:344px;--y:100px;--w:240px;--h:370px"><span class="badge badge-top" style="--b:5.2s">2</span>
            <b class="pt">Sailoxx Analysis</b><span class="ps">We analyse your data and benchmark your AI stack</span>
            ''' + row(0, 116, 'doc', 'Cost analysis') + row(1, 176, 'shield', 'Risk assessment') + row(2, 235, 'bars', 'Usage insights') + row(3, 295, 'scan', 'Governance gaps') + '''
          </div>
        </div>
        <div class="dg-g dg-g3">
          <div class="dg-head dg-h3" style="--x:641px;--y:12px"><span class="badge" style="--b:10.4s">3</span><div><b>Clear outcomes</b><span>A practical plan your leadership can act on</span></div></div>
          ''' + rcard(0, 103, 'rupee', 'Optimized spend', 'Cut waste and improve ROI') + rcard(1, 198, 'shield', 'Lower risk', 'Remove unapproved tools') + rcard(2, 292, 'doc', 'Clear governance', 'Policies and approval process') + rcard(3, 392, 'pulse', 'Confident adoption', 'A roadmap for safe, effective AI use') + '''
        </div>
        <div class="dg-g dg-g4">
          <div class="dg-foot" style="--x:316px;--y:513px"><span class="badge" style="--b:12.6s">4</span><b>Ongoing support</b><span>We help you implement and keep improving</span></div>
        </div>
        ''' + dots + '''
      </div></div>
    </div>
  </div>
</section>
'''
