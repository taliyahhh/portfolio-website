"""Builds all four process pages from one template.
Run from this folder: python3 build_pages.py
Voice: short, direct, first person. No "this, not that" labels, no "Because:" lines."""
import html

RESUME = "https://drive.google.com/file/d/1bd_ZmiNHnVtcSxHFkS7MbYG4A5ucGU3_/view?usp=sharing"
e = html.escape
STOPS = [("problem", "Problem"), ("research", "Research"), ("iterations", "Iterations"),
         ("decisions", "Decisions"), ("outcome", "Outcome"), ("next", "What's next")]
LENS_CLASS = {"Design": "d", "Tech": "t", "Business": "b", "Product strategy": "b"}


def fig(src, alt, cap, cls="dfig"):
    capt = f'<figcaption>{cap}</figcaption>' if cap else ''
    return f'<figure class="{cls}"><img src="{src}" alt="{e(alt)}" loading="lazy">{capt}</figure>'


def tryit(p, lazy=True):
    if not p.get("live"):
        return ""
    return f'''      <div class="tryit">
        <div class="bar"><span><b>Try it:</b> {p["try"]}</span><a href="{p["live"]}" target="_blank" rel="noopener">Open full site</a></div>
        <button type="button" class="start" data-src="{p["live"]}" data-title="{e(p["name"])}, live">
          <img src="{p["tryimg"]}" alt="{e(p["tryalt"])}"{' loading="lazy"' if lazy else ''}>
          <span><i></i>Start the live site</span>
        </button>
      </div>
'''


def page(p):
    labels = "".join(f'<li><span>{k}</span>{v}</li>' for k, v in p["labels"])
    stats = "".join(f'<div><b>{b}</b><span>{s}</span></div>' for b, s in p["stats"])
    trip = "".join(f'<a href="#{i}"><i></i><span>{t}</span></a>' for i, t in STOPS)
    n = len(p["iters"])
    tabs = "".join(f'          <button type="button" role="tab" aria-selected="{str(k == n - 1).lower()}" data-i="{k}"><small>v{k + 1} · {it["date"]}</small>{it["short"]}</button>\n' for k, it in enumerate(p["iters"]))
    panels = "".join(f'        <figure class="steps-panel"{"" if k == n - 1 else " hidden"} data-panel="{k}"><img src="{it["img"]}" alt="{e(it["alt"])}" loading="lazy"><figcaption>{it["cap"]}</figcaption></figure>\n' for k, it in enumerate(p["iters"]))
    prob = "".join(f'      <p>{x}</p>\n' for x in p["problem"][2:])
    evid = "".join(f'        <div class="ev"><b>{b}</b>{x}</div>\n' for b, x in p["evidence"])
    rfig = ('      ' + fig(*p["research_fig"], cls="cs-fig") + '\n') if p.get("research_fig") else ''
    o = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(p["name"])} · Taliyah Harvey</title>
<meta name="description" content="Product process case study: {e(p["desc"])}">
<link rel="icon" type="image/png" href="../assets/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap">
<link rel="stylesheet" href="case-study.css">
</head>
<body class="express">

<header class="top">
  <div class="wrap">
    <a class="mark" href="/" aria-label="Taliyah Harvey, home"><b>tj</b> <span>Taliyah Harvey</span></a>
    <nav aria-label="Site">
      <a href="/#work">Work</a>
      <a href="/#about">About</a>
      <a href="/#contact">Contact</a>
      <a href="{RESUME}" target="_blank" rel="noopener">Resume</a>
    </nav>
  </div>
</header>

<main>
  <section class="cs-hero">
    <div class="wrap">
      <div class="cs-kicker"><i></i>Process · {e(p["name"])}</div>
      <h1>{p["h1"]}</h1>
      <p class="sub">{p["sub"]}</p>
      <ul class="labels">{labels}</ul>
      <div class="outcomes">{stats}</div>
    </div>
  </section>

  <div class="modebar" id="mode-start">
    <div class="wrap">
      <div class="seg" role="group" aria-label="How much detail">
        <button type="button" data-mode="express" aria-pressed="true">Short <small>1 min</small></button>
        <button type="button" data-mode="local" aria-pressed="false">Full <small>whole process</small></button>
      </div>
      <nav class="trip" aria-label="Sections"><span class="fill"></span>{trip}</nav>
    </div>
  </div>

  <section class="cs-sec express-only">
    <div class="wrap">
      <div class="express-card">
        <div><h3>The problem</h3><p>{p["x"][0]}</p></div>
        <div><h3>What I made</h3><p>{p["x"][1]}</p></div>
        <div><h3>The big call</h3><p>{p["x"][2]}</p></div>
      </div>
{tryit(p, lazy=False)}      <div class="next-row">
        <button type="button" class="btn fill" data-mode="local" data-scroll><i></i>See the whole process</button>
      </div>
    </div>
  </section>

  <section class="cs-sec local-only" id="problem">
    <div class="wrap narrow">
      <div class="stop-tag"><i></i>Problem <em class="lens d">Desirability</em></div>
      <h2>{p["problem"][0]}</h2>
      <p class="lead">{p["problem"][1]}</p>
{prob}    </div>
  </section>

  <section class="cs-sec local-only" id="research">
    <div class="wrap">
      <div class="narrow">
        <div class="stop-tag"><i></i>Research <em class="lens d">Users</em></div>
        <h2>{p["research"][0]}</h2>
        <p class="lead">{p["research"][1]}</p>
      </div>
      <div class="evidence">
{evid}      </div>
{rfig}      <p class="insight">{p["insight"]}</p>
    </div>
  </section>

  <section class="cs-sec local-only" id="iterations">
    <div class="wrap">
      <div class="narrow">
        <div class="stop-tag"><i></i>Iterations <em class="lens d">Design</em></div>
        <h2>{p["iter_h"]}</h2>
      </div>
      <div class="steps" data-steps>
        <div class="steps-tabs" role="tablist" aria-label="Versions">
{tabs}        </div>
{panels}      </div>
    </div>
  </section>

  <section class="cs-sec local-only" id="decisions">
    <div class="wrap">
      <div class="narrow">
        <div class="stop-tag"><i></i>Decisions <em class="lens">Trade-offs</em></div>
        <h2>The calls I made</h2>
      </div>
'''
    for d in p["decisions"]:
        if d.get("pair"):
            vis = '<div class="pair">' + "".join(f'<figure><img src="{s}" alt="{e(a)}" loading="lazy"><figcaption>{c}</figcaption></figure>' for s, a, c in d["pair"]) + '</div>'
        elif d.get("fig"):
            vis = fig(*d["fig"])
        else:
            steps = "".join(f'<li class="{c}"><b>{t}</b><span>{x}</span></li>' for c, t, x in d["diagram"])
            vis = f'<figure class="dfig flowd"><ol>{steps}</ol></figure>'
        o += f'''      <article class="decision">
        <header><em class="lens {LENS_CLASS[d["lens"]]}">{d["lens"]}</em><h3>{d["h"]}</h3></header>
        {vis}
        <p class="because">{d["why"]}</p>
      </article>
'''
    feats = "".join(f'        <li>{x}</li>\n' for x in p["features"])
    extra = "".join(f'      {fig(*f, cls="cs-fig")}\n' for f in p.get("outcome_figs", []))
    result = (f'      <div class="evidence one"><div class="ev"><b>{p["result"][0]}</b>{p["result"][1]}</div></div>\n'
              if p.get("result") else "")
    learn = "".join(f'        <div><h3>{h}</h3><p>{x}</p></div>\n' for h, x in p["learn"])
    code = (f'        <a class="btn" href="{p["code"]}" target="_blank" rel="noopener">View the code</a>\n'
            if p.get("code") else "")
    o += f'''    </div>
  </section>

  <section class="cs-sec local-only" id="outcome">
    <div class="wrap">
      <div class="narrow">
        <div class="stop-tag"><i></i>Outcome <em class="lens t">Feasibility</em></div>
        <h2>{p["outcome"][0]}</h2>
        <p class="lead">{p["outcome"][1]}</p>
      </div>
      <ul class="feature-list">
{feats}      </ul>
{result}{extra}{tryit(p)}    </div>
  </section>

  <section class="cs-sec local-only" id="next">
    <div class="wrap">
      <div class="narrow">
        <div class="stop-tag"><i></i>What's next <em class="lens b">Viability</em></div>
        <h2>What I'm taking with me</h2>
      </div>
      <div class="learn">
{learn}      </div>
    </div>
  </section>

  <section class="next">
    <div class="wrap">
      <a class="next-card" href="{p["next"][0]}">
        <span><small>Next project</small><b>{p["next"][1]}</b></span>
        <span class="go" aria-hidden="true">&rarr;</span>
      </a>
      <div class="next-row">
        <a class="btn" href="/#contact">Get in touch</a>
{code}      </div>
    </div>
  </section>
</main>
<footer>
  <div class="wrap"><span>Taliyah Harvey</span><span>{p["foot"]}</span></div>
</footer>
<script src="case-study.js"></script>
<script>
// version tabs: click or use arrow keys to step through the real versions
document.querySelectorAll('[data-steps]').forEach(box => {{
  const tabs = [...box.querySelectorAll('[role=tab]')], panels = [...box.querySelectorAll('[data-panel]')];
  const show = i => {{ tabs.forEach((t, k) => t.setAttribute('aria-selected', k === i)); panels.forEach((q, k) => q.hidden = k !== i); }};
  tabs.forEach((t, i) => {{
    t.addEventListener('click', () => show(i));
    t.addEventListener('keydown', ev => {{
      const j = ev.key === 'ArrowRight' ? i + 1 : ev.key === 'ArrowLeft' ? i - 1 : null;
      if (j !== null && tabs[j]) {{ ev.preventDefault(); tabs[j].focus(); show(j); }}
    }});
  }});
}});
</script>
</body>
</html>
'''
    assert "—" not in o, p["slug"]
    open(p["slug"] + ".html", "w").write(o)
    print("wrote", p["slug"] + ".html")


BART = dict(
    slug="karls-friend-bart", name="Karl's Friend Bart",
    desc="an interactive BART map that keeps the official look and shows what's running right now.",
    h1="I got off at the wrong station. So I rebuilt the map.",
    sub="BART's map is a still picture. It can't tell you where your train is going or what changes at night. So I made one that can.",
    labels=[("Role", "Solo: design and front-end"), ("Platform", "Web and mobile"), ("Timeline", "5 days, Oct 2026"), ("Type", "Personal")],
    stats=[("5 days", "from idea to live site"), ("Live", "trains and departures from BART's API"), ("0", "new maps for riders to learn")],
    x=["The official map shows every line at once and never changes. I got off at the wrong stop because of it.",
       "The same map, but it moves. Spotlight your line, tap a station, see what's running tonight.",
       "Keep the official look. Nobody wants to learn a new map."],
    live="https://taliyahhh.github.io/bart-revamp/", tryimg="img/bart-v4-final-day.jpg",
    tryalt="Karl's Friend Bart: the official-style BART map with a station panel", try_="tap a line or a station.",
    problem=["A map that just sits there.",
             "Every line, all at once, looking the same at 8am and midnight.",
             "After 9pm, Red and Green stop running and transfers change. The map doesn't say so. You find out on the platform. I found out at the wrong stop.",
             "<b>The question:</b> where does my train go, right now?"],
    research=["Learning the map inside out.", "I studied the official map and BART's service rules until I could rebuild both."],
    evidence=[("Riders know it", "The official map is already in everyone's head. That's worth keeping."),
              ("Live data exists", "BART's public API has real-time departures and alerts, so a live map was possible."),
              ("Nights are different", "Evening service is basically a different network, and nothing shows it.")],
    insight="Keep the map. Make it move.",
    iter_h="Four versions to get it right",
    iters=[
        {"short": "Fogline", "date": "Oct 24", "img": "img/bart-v1-fogline.jpg", "alt": "First version: a dark custom map with a line list and trip planner", "cap": "My own dark map. It looked cool, but it didn't look like BART."},
        {"short": "Official", "date": "Oct 24", "img": "img/bart-v2-official.jpg", "alt": "Second version: the official layout with a Plan a Trip box", "cap": "Rebuilt the real map. Familiar, but the trip planner crowded it."},
        {"short": "Bottom bar", "date": "Oct 24", "img": "img/bart-v3-bottombar.jpg", "alt": "Third version: controls in a bottom bar and a station panel", "cap": "Cut trip planning. The controls moved to a bottom bar your thumb can reach."},
        {"short": "Karl's Friend Bart", "date": "Oct 28", "img": "img/bart-v4-final-evening.jpg", "alt": "Final version in evening mode with live mini trains", "cap": "Live mini trains, a name, and a night mode that flips on at 9pm."},
    ],
    decisions=[
        dict(lens="Design", h="Keep the official map",
             pair=[("img/bart-v1-fogline.jpg", "My custom dark map", "Mine: a new map to learn."),
                   ("img/bart-v4-final-day.jpg", "The official-style map", "BART's: readable in a second.")],
             why="Familiarity is the feature. My job was to make it more useful, not more mine."),
        dict(lens="Product strategy", h="Cut trip planning",
             pair=[("img/bart-v2-official.jpg", "Version with a Plan a Trip box", "A trip planner, like every transit app."),
                   ("img/bart-v3-bottombar.jpg", "Version with line chips in a bottom bar", "Just your line, one tap away.")],
             why="Other apps already plan trips. Seeing your whole line at a glance didn't exist, so that's all I built."),
        dict(lens="Tech", h="Night mode runs itself",
             pair=[("img/bart-v4-final-day.jpg", "Day service, light theme", "Day: all five lines."),
                   ("img/bart-v4-final-evening.jpg", "Evening service, dark theme", "After 9pm: dark, with Red and Green off.")],
             why="A label is easy to miss. The site checks the time and switches to the evening network on its own."),
    ],
    outcome=["What shipped", "Live on desktop and phone. No framework, no build step."],
    features=["Official-style map with pan, pinch zoom and readable labels",
              "Line spotlight from a thumb-friendly bottom bar",
              "Live mini trains, with an estimate if the feed drops",
              "Station panel with departures, connections and alerts"],
    learn=[("Familiar beats clever", "My custom map had the most personality. The official one was the one people could read."),
           ("Cutting is a feature", "Dropping trip planning did more than anything I added."),
           ("Next: test with riders", "Time people finding their route home on both maps."),
           ("Next: pitch it", "Bring it to BART and rider groups as a model for clearer maps.")],
    next=("fee-fi-fo-fund.html", "Fee Fi Fo Fund: where did your tax dollars actually go?"),
    code="https://github.com/taliyahhh/bart-revamp",
    foot="Karl is what locals call SF's fog. A fan project, not affiliated with BART.",
)

FEE = dict(
    slug="fee-fi-fo-fund", name="Fee Fi Fo Fund",
    desc="a storytelling site that shows teens and young adults where their tax dollars go, by zip code.",
    h1="Where did your tax dollars actually go?",
    sub="Crossing the Bay Bridge, my friend asked why we still pay a toll if our taxes cover roads. I didn't know, and no government site made it easy to find out. So I built one for teens and young adults.",
    labels=[("Role", "Design and development"), ("Team", "Me + a teammate on video and mood board"), ("Timeline", "Oct 2026"), ("Type", "SVSD design challenge")],
    stats=[("41,000+", "zip codes, every one in the US"), ("3", "levels of government, side by side"), ("$100", "how every number is shown")],
    x=["Teens and young adults pay taxes and have no idea where the money goes. The sites that explain it are boring and don't tell a story.",
       "Type your zip code. See where every $100 went, told like a fairy tale.",
       "Dollars out of $100, not billions. Nobody can picture $1.6 trillion."],
    live="https://feefifo.fund", tryimg="img/fee-v4-land.jpg",
    tryalt="Fee Fi Fo Fund's landing page: a hand-lettered logo over a colorful dot map of every US zip code",
    try_="type your zip code, or tap anywhere on the map.",
    problem=["Public, but impossible to read.",
             "It started on the Bay Bridge. My friend asked: why do tolls exist, how long does a bridge take to pay off, and what's the point of taxes if we still pay the toll?",
             "The answers are out there, in budget PDFs, in billions, with zero story.",
             "<b>Who it's for:</b> teens and young adults getting their first paychecks and wondering where the money goes.",
             "<b>The brief:</b> SVSD asked for a product built for a specific group of people, centered on storytelling."],
    research=["Finding data for every town.", "Big cities publish budgets. Small towns don't make it easy. I needed both."],
    evidence=[("Every city", "The Census of Governments covers every local government in the US, and California's Controller adds all 482 California cities."),
              ("$22 of every $100", "federal dollars go to Social Security. Leaving it out would make the picture prettier and wrong."),
              ("Almost $0", "of California's General Fund goes to transit. That money comes from gas taxes and fees instead.")],
    insight="Nobody thinks in billions. Everyone gets $100.",
    iter_h="Four versions in four days",
    iters=[
        {"short": "Taxonomy", "date": "Oct 18", "img": "img/fee-v1-res.jpg", "alt": "First version: spending shown as a grid of boxed cards", "cap": "Every category in a box. Readable, but it felt like a spreadsheet."},
        {"short": "Floating", "date": "Oct 18", "img": "img/fee-v2-res.jpg", "alt": "Second version: floating objects sized by spending", "cap": "Objects sized by money. I tried psychedelic animations and deleted them the same day."},
        {"short": "Folders", "date": "Oct 19", "img": "img/fee-v3-res.jpg", "alt": "Third version: hand-lettered results in Nation, State and City file folders", "cap": "Hand-lettered, with real file folders for Nation, State and City."},
        {"short": "The tale", "date": "Oct 21", "img": "img/fee-v4-res.jpg", "alt": "Final version: results with a $100 strip and photo stickers", "cap": "A story where you're the main character, read aloud if you want, plus a $100 strip."},
    ],
    decisions=[
        dict(lens="Design", h="$100, not billions",
             pair=[("img/fee-v1-res.jpg", "Early results in billions", "Billions: too big to picture."),
                   ("img/fee-v4-res.jpg", "Final results out of $100", "Out of every $100: you get it instantly.")],
             why="$22 out of $100 you can feel. $1.6 trillion you can't."),
        dict(lens="Product strategy", h="Show the uncomfortable stuff",
             fig=("img/fee-buckets.jpg", "Santa Clara's federal breakdown with Social Security, debt and the safety net at full size", ""),
             why="Together they're a huge share of federal spending. Hiding them would look cleaner and be wrong."),
        dict(lens="Tech", h="Data that updates itself",
             diagram=[("src", "Public data", "Census and California's Controller"),
                      ("job", "Monthly GitHub Action", "Downloads and sorts every city into 12 categories"),
                      ("out", "One data file", "Saved to the repo, so every change is visible"),
                      ("site", "feefifo.fund", "Plain HTML reads it. No server.")],
             why="City budgets change every year. Nobody should have to retype them."),
    ],
    outcome=["What shipped", "Live at feefifo.fund. No framework, no build step."],
    features=["A dot map of every US zip code you can type into, drag and pinch",
              "Nation, State and City folders, everything out of $100",
              "The tale: a scroll story with a Read it to me button",
              "A Sources page with every dataset and how it's sorted",
              "Shareable links for any zip, like feefifo.fund/?zip=95050"],
    result=("Didn't make finals.", " Kept building it anyway."),
    learn=[("Restraint is a skill", "The psychedelic version was the most fun to make and the first thing I cut."),
           ("Scale is the story", "Switching to $100 did more than any visual I added."),
           ("Next: more states", "Only California and New York state budgets are in so far."),
           ("Next: so what can I do?", "The Leave a footprint folder is the start: from where did it go to what can I do about it.")],
    next=("branch-out.html", "Branch Out: finding your first open source project shouldn't be this hard."),
    code="https://github.com/taliyahhh/tax-site",
    foot="Data: U.S. Census Bureau, California State Controller and state budget reports",
)

BRANCH = dict(
    slug="branch-out", name="Branch Out",
    desc="a swipe-based way for college students to find open source projects matched to their year, languages and interests.",
    h1="Finding your first open source project shouldn't be this hard.",
    sub="GitHub has millions of repos and no starting point for students. In Salesforce's Futureforce Tech Launchpad, our team of three built Branch Out: pick your year, languages and interests, then swipe.",
    labels=[("Role", "Full-stack engineer, team of 3"), ("Stack", "React, Node, PostgreSQL, Gemini"), ("Timeline", "Jun to Aug 2025"), ("Type", "Salesforce Futureforce Tech Launchpad")],
    stats=[("1 of 30", "picked from 3,000+ applicants"), ("192", "commits, all through pull requests"), ("3", "people, one product")],
    x=["Students want open source experience, but search shows the biggest, scariest repos first.",
       "Pick your year, languages and interests, then swipe through repos matched to you, each with an AI summary.",
       "Swipe, not a list. One repo, one decision."],
    live="https://branchout.tech", tryimg="img/bo-swipe.jpg",
    tryalt="Branch Out's swipe screen: one repository card with tags and an AI summary", try_="set your preferences, then swipe.",
    problem=["Where do I even start?",
             "Everyone says contribute to open source. Then you open GitHub and see millions of repos with no idea which ones want beginners.",
             "Search sorts by stars, so the top results are the most intimidating ones."],
    research=["Asking students in our cohort.", "We interviewed a few students in our Futureforce cohort about trying to make a first contribution."],
    evidence=[("Stuck at step one", "They wanted to contribute but didn't know where to start."),
              ("Year, not level", "They described themselves by year in school, not as beginner or advanced."),
              ("1 or 2 languages", "Most wanted to start with what they already knew.")],
    insight="Finding a project should feel like browsing, not searching.",
    iter_h="Three screens, one flow",
    iters=[
        {"short": "Preferences", "date": "Jul 2025", "img": "img/bo-prefs.jpg", "alt": "Preferences page with skill level, languages and topics", "cap": "Three quick questions: your year, your languages, your interests."},
        {"short": "Swipe", "date": "Jul 2025", "img": "img/bo-swipe.jpg", "alt": "Swipe card with tags and an AI summary", "cap": "One repo at a time, with tags and an AI summary. Keyboard shortcuts too."},
        {"short": "Search", "date": "Aug 2025", "img": "img/bo-search.jpg", "alt": "Search page with filters", "cap": "For when you already know what you want."},
    ],
    decisions=[
        dict(lens="Design", h="Swipe, not a list",
             pair=[("img/bo-search.jpg", "A filter-heavy search view", "A wall of filters and results."),
                   ("img/bo-swipe.jpg", "A single swipe card", "One card, one decision.")],
             why="A wall of results is where people give up. One card is one small decision."),
        dict(lens="Product strategy", h="Your year is your level",
             fig=("img/bo-skill.jpg", "Preferences with skill level as 1st to 4th year", ""),
             why="\"Intermediate\" means something different to everyone. Everyone knows their year."),
        dict(lens="Tech", h="AI summaries on every card",
             fig=("img/bo-summary.jpg", "A repo card with a plain-language AI summary", ""),
             why="READMEs are written for maintainers. I built the Gemini client that explains each repo in plain language."),
    ],
    outcome=["What I built", "My part, straight from my commits."],
    features=["User accounts: API endpoints, login and signup pages",
              "Saving each student's preferences to the database",
              "The Gemini client behind the AI summaries",
              "Swipe controls with keyboard shortcuts",
              "The discovery carousel, mobile layouts and light and dark mode",
              "Sidebar, about page and in-app feedback messages"],
    learn=[("Small PRs win", "Working through pull requests on a team of three taught me to keep changes easy to review."),
           ("Stick to the wireframe", "It kept three people's work feeling like one product."),
           ("Next: learn from saves", "Use which repos students save to tune the matches."),
           ("Next: first issue", "Point students to a good first issue, not just a repo.")],
    next=("in-hindsight.html", "In Hindsight: you saved it. Now use it."),
    code="https://github.com/Team-10-FTL/branch-out",
    foot="Built with Nathan Kenmognie and Jackie Jurado",
)

HIND = dict(
    slug="in-hindsight", name="In Hindsight",
    desc="Peep, an AI doomscrolling buddy that turns your TikTok saves into plans.",
    h1="You saved it. Now use it.",
    sub="We save everything, then forget it all. In Hindsight reads your TikTok data, and Peep, your doomscrolling buddy, turns your saves into plans.",
    labels=[("Role", "Founder: product, design and development"), ("Platform", "Web now, iOS next"), ("Timeline", "Oct 2026 to now"), ("Type", "Startup, in beta")],
    stats=[("94%", "gave up finding a saved video"), ("66%", "have 200+ saves"), ("11", "waitlist signups in one day")],
    x=["We save everything, then forget it all. 94% of people I surveyed have given up finding a saved video.",
       "Peep: an AI buddy that scrolls with you and sends your saves to Maps, Calendar and Reminders.",
       "A buddy, not a blocker. No guilt, just help getting something out of it."],
    live="https://inhindsight.net", tryimg="img/ih-v3-peep.jpg",
    tryalt="In Hindsight's landing page: You're not doomed. You're just scrolling.", try_="hit Try the demo to explore with sample data.",
    problem=["Saves pile up. Nothing happens.",
             "Every save is a promise to come back. Then the feed moves on and the saves pile up.",
             "Screen time apps track your time. Collections store your saves. Nothing actually does anything with them."],
    research=["35 surveys, 5 interviews.", "Young adults, mostly USC students, reached through SideChat, Snapchat, Reddit and iMessage."],
    evidence=[("94%", "have given up finding a saved video."),
              ("69%", "scroll longer than they meant to."),
              ("54%", "never rewatch what they save."),
              ("66%", "have 200+ saves.")],
    research_fig=("img/ih-competition.jpg", "Competitive map: time-focused apps like Opal and Screen Time versus content-focused tools like TikTok Collections, with In Hindsight proactive and content-focused", "Everyone else tracks your time or stores your saves. Peep understands what you saved and acts on it."),
    insight="Your data already exists. Peep just makes it useful.",
    iter_h="From a dashboard to a buddy",
    iters=[
        {"short": "Dashboard", "date": "Oct 2026", "img": "img/ih-dash.jpg", "alt": "In Hindsight dashboard with a timeline and tabs", "cap": "Know your scroll: your history as a timeline, your topics and your rhythm."},
        {"short": "Act", "date": "Nov 2026", "img": "img/ih-v2-act.jpg", "alt": "The Act tab sorting saves into lists, maps and plans", "cap": "Saves to action: recipes, places and plans sorted into things you can actually do."},
        {"short": "Features", "date": "Nov 2026", "img": "img/ih-features.jpg", "alt": "Scrolling Score, Attention Map and Saves to Action cards", "cap": "Scrolling Score, Attention Map and Saves to Action."},
        {"short": "Peep", "date": "Nov 2026", "img": "img/ih-peep-flow.jpg", "alt": "Five phone screens showing Peep before, during and after scrolling", "cap": "Peep asks what you're on TikTok for, gets sleepy when you scroll too long, and files what you find."},
    ],
    decisions=[
        dict(lens="Design", h="A buddy, not a blocker",
             fig=("img/ih-peep-sleepy.jpg", "Peep asking what you are on TikTok for, then getting sleepy on the lock screen as you keep scrolling", ""),
             why="69% already scroll longer than they meant to. They don't need guilt. They need help getting something out of it."),
        dict(lens="Business", h="Free, then $4 a month",
             fig=("img/ih-business.jpg", "Business model: Free, Plus at $4 a month, and a sharing growth loop", ""),
             why="Upload and explore for free. Plus adds AI on every save and lets Peep act on its own. 63% of people I surveyed would pay or consider it."),
        dict(lens="Tech", h="Private by default",
             fig=("img/ih-how.jpg", "How it works: your TikTok data, AI reads the content, Peep picks the action, sent to your apps", ""),
             why="People are handing over their whole scrolling history. It's read in your browser and never sold."),
    ],
    outcome=["Where it's at", "MVP live at inhindsight.net, built in 2 months."],
    features=["Upload your TikTok export, or try the demo",
              "Scrolling Score, Attention Map and Saves to Action",
              "A clickable Peep prototype at inhindsight.net/peep",
              "A beta waitlist, live on the site"],
    result=("11 signups", " on the waitlist in one day."),
    outcome_figs=[("img/ih-milestones.jpg", "Roadmap: MVP now, private beta of 100 users in January 2027, Peep on iOS in spring 2027, 1,000 users by summer 2027", "Next up: a 100-user private beta, then Peep on iOS.")],
    learn=[("Talk to people first", "The survey changed the product more than any feature did."),
           ("Privacy sells", "Keeping data on your device shaped everything, and it's a reason to trust it."),
           ("Next: private beta", "100 users in January 2027."),
           ("Next: Peep on iOS", "TestFlight in spring 2027, 1,000 users by summer.")],
    next=("karls-friend-bart.html", "Karl's Friend Bart: I got off at the wrong station. So I rebuilt the map."),
    code=None,
    foot="Not affiliated with TikTok",
)

for p in (BART, FEE, BRANCH, HIND):
    p["try"] = p.pop("try_")
    page(p)
