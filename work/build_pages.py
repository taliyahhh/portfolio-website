"""Builds the process pages for Fee Fi Fo Fund, In Hindsight and Branch Out
from one template so they match Karl's Friend Bart. Run: python3 build_pages.py"""
import json, html

RESUME = "https://drive.google.com/file/d/1bd_ZmiNHnVtcSxHFkS7MbYG4A5ucGU3_/view?usp=sharing"
e = html.escape


def head(title, desc):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)} · Taliyah Harvey</title>
<meta name="description" content="Product process case study: {e(desc)}">
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
'''


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
    out = head(p["name"], p["desc"])
    labels = "".join(f'<li><span>{k}</span>{v}</li>' for k, v in p["labels"])
    outs = "".join(f'<div><b>{b}</b><span>{s}</span></div>' for b, s in p["outcomes"])
    out += f'''  <section class="cs-hero">
    <div class="wrap">
      <div class="cs-kicker"><i></i>Product process · {e(p["name"])}</div>
      <h1>{p["h1"]}</h1>
      <p class="sub">{p["sub"]}</p>
      <ul class="labels">{labels}</ul>
      <div class="outcomes">{outs}</div>
    </div>
  </section>

  <div class="modebar" id="mode-start">
    <div class="wrap">
      <div class="seg" role="group" aria-label="How much detail">
        <button type="button" data-mode="express" aria-pressed="true">Express <small>1 min</small></button>
        <button type="button" data-mode="local" aria-pressed="false">Local <small>full process</small></button>
      </div>
      <nav class="trip" aria-label="Case study stops">
        <span class="fill"></span>
        <a href="#problem"><i></i><span>Problem</span></a>
        <a href="#research"><i></i><span>Research</span></a>
        <a href="#insight"><i></i><span>Insight</span></a>
        <a href="#iterations"><i></i><span>Iterations</span></a>
        <a href="#decisions"><i></i><span>Decisions</span></a>
        <a href="#outcome"><i></i><span>Outcome</span></a>
        <a href="#next"><i></i><span>What's next</span></a>
      </nav>
    </div>
  </div>

  <section class="cs-sec express-only">
    <div class="wrap">
      <div class="express-card">
        <div><h3>The problem</h3><p>{p["x_problem"]}</p></div>
        <div><h3>What I made</h3><p>{p["x_made"]}</p></div>
        <div><h3>Biggest decision</h3><p>{p["x_decision"]}</p></div>
      </div>
{tryit(p, lazy=False)}      <div class="next-row">
        <button type="button" class="btn fill" data-mode="local" data-scroll><i></i>See the full process</button>
      </div>
    </div>
  </section>

  <section class="cs-sec local-only" id="problem">
    <div class="wrap narrow">
      <div class="stop-tag"><i></i>Stop 1 · Problem <em class="lens d">Desirability</em></div>
      <h2>{p["problem_h"]}</h2>
      <p class="lead">{p["problem_lead"]}</p>
{''.join(f'      <p>{x}</p>{chr(10)}' for x in p["problem_more"])}      <p><b>Goal:</b> {p["goal"]}</p>
    </div>
  </section>

  <section class="cs-sec local-only" id="research">
    <div class="wrap">
      <div class="narrow">
        <div class="stop-tag"><i></i>Stop 2 · Research <em class="lens d">{p["research_lens"]}</em></div>
        <h2>{p["research_h"]}</h2>
        <p class="lead">{p["research_lead"]}</p>
      </div>
{('      <figure class="cs-fig"><img src="' + p["research_img"][0] + '" alt="' + e(p["research_img"][1]) + '" loading="lazy"><figcaption>' + p["research_img"][2] + '</figcaption></figure>' + chr(10)) if p.get("research_img") else ''}      <div class="evidence">
{''.join(f'        <div class="ev{" todo" if t else ""}"><b>{b}</b>{x}</div>{chr(10)}' for b, x, t in p["evidence"])}      </div>
    </div>
  </section>

  <section class="cs-sec local-only" id="insight">
    <div class="wrap narrow">
      <div class="stop-tag"><i></i>Stop 3 · Insight <em class="lens d">Opportunity</em></div>
      <h2>The opportunity</h2>
      <p class="insight">{p["insight"]}</p>
    </div>
  </section>

  <section class="cs-sec local-only" id="iterations">
    <div class="wrap">
      <div class="narrow">
        <div class="stop-tag"><i></i>Stop 4 · Iterations <em class="lens d">Design</em></div>
        <h2>{p["iter_h"]}</h2>
        <p class="lead">Drag through the real versions. Each one fixed what the last got wrong.</p>
      </div>
      <div class="iter">
        <figure><img src="{p["iters"][0]["img"]}" alt="" width="1280" height="800"></figure>
        <div class="controls">
          <span class="ver" data-out="ver"></span>
          <h3 data-out="title"></h3>
          <p class="what" data-out="what"></p>
          <p class="why" data-out="why"></p>
          <input type="range" min="0" max="{len(p["iters"]) - 1}" step="1" value="0" aria-label="Choose a version">
          <div class="ticks"></div>
          <div class="nav"><button type="button" data-step="-1">Previous</button><button type="button" data-step="1">Next version</button></div>
        </div>
      </div>
      <script type="application/json" id="iterations-data">
      {json.dumps(p["iters"], ensure_ascii=False)}
      </script>
    </div>
  </section>

  <section class="cs-sec local-only" id="decisions">
    <div class="wrap">
      <div class="narrow">
        <div class="stop-tag"><i></i>Stop 5 · Decisions <em class="lens">Trade-offs</em></div>
        <h2>Why this, not that</h2>
        <p class="lead">One call each for design, product strategy and tech.</p>
      </div>
'''
    for d in p["decisions"]:
        pair = ""
        if d.get("pair"):
            (na, nalt, ncap), (ya, yalt, ycap) = d["pair"]
            nl, yl = d.get("labels", ("Not this", "This"))
            pair = f'''        <div class="pair">
          <figure><span class="verdict no">{nl}</span><img src="{na}" alt="{e(nalt)}" loading="lazy"><figcaption>{ncap}</figcaption></figure>
          <figure><span class="verdict yes">{yl}</span><img src="{ya}" alt="{e(yalt)}" loading="lazy"><figcaption>{ycap}</figcaption></figure>
        </div>
'''
        out += f'''      <article class="decision">
        <header><h3>{d["h"]}</h3><p>{d["lens"]}</p></header>
{pair}        <p class="because"><b>Because:</b> {d["because"]}</p>
      </article>
'''
    feats = "".join(f'        <li>{x}</li>\n' for x in p["features"])
    out += f'''    </div>
  </section>

  <section class="cs-sec local-only" id="outcome">
    <div class="wrap">
      <div class="narrow">
        <div class="stop-tag"><i></i>Stop 6 · Outcome <em class="lens t">Feasibility</em></div>
        <h2>{p["outcome_h"]}</h2>
        <p class="lead">{p["outcome_lead"]}</p>
      </div>
      <ul class="feature-list">
{feats}      </ul>
{tryit(p)}{''.join(f'      <div class="evidence"><div class="ev todo"><b>{b}</b>{x}</div></div>{chr(10)}' for b, x in p.get("outcome_todo", []))}    </div>
  </section>

  <section class="cs-sec local-only" id="next">
    <div class="wrap">
      <div class="narrow">
        <div class="stop-tag"><i></i>Stop 7 · Learnings and next <em class="lens b">Viability</em></div>
        <h2>What I'd take forward</h2>
      </div>
      <div class="learn">
{''.join(f'        <div><h3>{h}</h3><p>{x}</p></div>{chr(10)}' for h, x in p["learn"])}      </div>
    </div>
  </section>

  <section class="next">
    <div class="wrap">
      <a class="next-card" href="{p["next"][0]}">
        <span><small>Next stop</small><b>{p["next"][1]}</b></span>
        <span class="go" aria-hidden="true">&rarr;</span>
      </a>
      <div class="next-row">
        <a class="btn" href="/#contact">Get in touch</a>
{('        <a class="btn" href="' + p["code"] + '" target="_blank" rel="noopener">View the code</a>' + chr(10)) if p.get("code") else ''}      </div>
    </div>
  </section>
</main>
<footer>
  <div class="wrap"><span>Taliyah Harvey</span><span>{p["foot"]}</span></div>
</footer>
<script src="case-study.js"></script>
</body>
</html>
'''
    assert "—" not in out, p["slug"]
    open(p["slug"] + ".html", "w").write(out)
    print("wrote", p["slug"] + ".html")


FEE = dict(
    slug="fee-fi-fo-fund", name="Fee Fi Fo Fund",
    desc="type a zip code and see what your city, state and the federal government spent your tax dollars on.",
    h1="Where did your tax dollars actually go?",
    sub="Taxes come out of every paycheck, but where the money goes is buried in budget PDFs. I designed and built a site where you type your zip code and see what your city, your state and the federal government spent it on, told like a fairy tale.",
    labels=[("Role", "Design and development"), ("Team", "Me, plus a teammate on video and mood board"), ("Timeline", "Oct 2026"), ("Type", "SVSD design competition")],
    outcomes=[("41,000+", "Zip codes on the map, every one in the US"), ("3 levels", "Federal, state and city spending side by side"), ("Self-updating", "City data rebuilds monthly from public sources")],
    x_problem="Spending data is public but unreadable: billions of dollars in PDFs, split across three levels of government nobody can keep straight.",
    x_made="Type a zip code and get a collage of where your money went, as dollars out of every $100, across nation, state and city.",
    x_decision="Show every number out of $100 instead of in billions. A scale people can actually feel.",
    live="https://feefifo.fund", try_="", tryimg="img/fee-v4-land.jpg", tryalt="Fee Fi Fo Fund's landing page: a hand-lettered logo over a colorful dot map of every US zip code",
    problem_h="Public, but not readable",
    problem_lead="Budgets live in PDFs and spreadsheets. Most people pay taxes every paycheck and never see where it goes, or which level of government is spending it.",
    problem_more=["Even when you find the numbers, they're in billions. Nobody can picture $1.6 trillion, so the data might as well be hidden."],
    goal="make your tax dollars feel personal in under a minute: one zip code, one picture.",
    research_lens="Data", research_h="Where the numbers come from",
    research_lead="Before designing anything, I had to find spending data that covered every town, not just big cities.",
    research_img=None,
    evidence=[
        ("Every city", "The 2022 Census of Governments covers every local government in the US. California's State Controller API adds all 482 California cities.", False),
        ("Hard truth", "Social Security alone is about $22 of every $100 the federal government spends. Leaving it out would make the picture prettier and wrong.", False),
        ("Surprise", "Some things barely show up where you'd expect. California's General Fund spends almost nothing on transit, because that money comes from gas taxes and fees.", False),
    ],
    insight="People don't think in billions. They think in their own town, and in a single dollar.",
    iter_h="Four versions in four days",
    iters=[
        {"short": "Taxonomy", "date": "Oct 18", "img": "img/fee-v1-res.jpg", "alt": "First version, called Taxonomy: spending shown as a grid of boxed cards with big dollar amounts",
         "title": "Taxonomy: every category in a box", "what": "A dark dot map of zip codes, then a grid of boxes, one per spending category.",
         "why": "Readable, but it looked like a spreadsheet with pictures. Nothing made you want to keep looking."},
        {"short": "Floating", "date": "Oct 18", "img": "img/fee-v2-res.jpg", "alt": "Second version: spending categories as floating 3D objects sized by how much money they get",
         "title": "Floating objects, sized by money", "what": "Renamed Fee Fi Fo Fund. Categories became loose objects scattered across the page, bigger for more money.",
         "why": "More alive. I also tried psychedelic animations and removed them the same day: fun, but they fought the numbers."},
        {"short": "Folders", "date": "Oct 19", "img": "img/fee-v3-res.jpg", "alt": "Third version: hand-lettered results inside a paper file folder with Nation, State and City tabs",
         "title": "Real file folders", "what": "A hand-lettered brand, paper texture and file folders with Nation, State and City tabs.",
         "why": "Three levels of government finally felt like three separate documents you can pull out and compare."},
        {"short": "The tale", "date": "Oct 21", "img": "img/fee-v4-res.jpg", "alt": "Final version: Santa Clara results with a $100 strip across the top and photo stickers for each category",
         "title": "The tale", "what": "A scroll story on the dot map with you as the main character, read aloud on request, plus a $100 strip that shows the whole split at a glance.",
         "why": "It turned a lookup into something people actually read to the end."},
    ],
    decisions=[
        dict(h="Dollars out of $100, not billions", lens="Design",
             pair=(("img/fee-v1-res.jpg", "Early results with totals in billions", "Accurate, but too big to picture."),
                   ("img/fee-v4-res.jpg", "Final results with a $100 strip", "Out of every $100, here's where yours went.")),
             because="$22 out of every $100 is a number you can feel. $1.6 trillion isn't."),
        dict(h="Show the uncomfortable buckets", lens="Product strategy",
             because="Social Security, paying off debt and the safety net don't fit a tidy list of 12 categories, but together they're a huge share of federal spending. Hiding them would have made the site cleaner and misleading, so they got their own buckets, and barely-funded categories got a gray \"barely any money here\" strip."),
        dict(h="Data that updates itself", lens="Tech",
             because="City budgets change every year. A GitHub Action rebuilds the data for every city each month from the Census and California's Controller, so the site stays plain HTML, CSS and JavaScript with no server to babysit."),
    ],
    outcome_h="What shipped", outcome_lead="Live at feefifo.fund. No framework, no build step.",
    features=["A dot map of every US zip code you can type into, drag and pinch",
              "Nation, State and City folders with every category out of $100",
              "The tale: a scroll story with Read it to me narration",
              "A Sources page listing every dataset, year and category mapping",
              "Shareable links for any zip, like feefifo.fund/?zip=95050"],
    outcome_todo=[("Result", "Add how the SVSD design competition went, and any reactions from people who tried it.")],
    learn=[("Restraint is a design skill", "The psychedelic version was the most fun to build and the first thing I deleted."),
           ("Scale is the story", "Changing billions to dollars out of $100 did more than any visual I added."),
           ("Next: every state", "State budgets are typed in by hand, so only California and New York are done. More states are next."),
           ("Next: from knowing to doing", "The Leave a footprint folder starts here: turning \"where did it go\" into \"what can I do about it.\"")],
    next=("branch-out.html", "Branch Out: how do college students find their first open source project?"),
    code="https://github.com/taliyahhh/tax-site",
    foot="Data: U.S. Census Bureau, California State Controller and state budget reports",
)
FEE["try"] = "type your zip code, or tap anywhere on the map."

HIND = dict(
    slug="in-hindsight", name="In Hindsight",
    desc="a dashboard for your TikTok archive, and Peep, a doomscrolling buddy that turns saves into plans.",
    h1="What if your saved videos weren't stuck in folders?",
    sub="Every save is a promise to come back later, and later rarely comes. In Hindsight turns your TikTok export into a picture of how you scroll, and Peep, a doomscrolling buddy, helps turn saves into plans you actually use.",
    labels=[("Role", "Product, design and development"), ("Platform", "Web, runs in your browser"), ("Timeline", "Oct 2026 to now"), ("Type", "Personal, in beta")],
    outcomes=[("35", "Young adults surveyed to shape the direction"), ("94%", "Have given up looking for a saved TikTok"), ("Private", "Your export is read on your device, never uploaded")],
    x_problem="People save videos to come back to, then never do. 94% of people I surveyed have given up looking for one.",
    x_made="A dashboard of your TikTok history, an Act tab that sends saves to lists, maps and calendars, and Peep, a buddy that keeps you company while you scroll.",
    x_decision="Be a buddy, not a blocker. No screen-time guilt, just help getting something out of the time.",
    live="https://inhindsight.net", tryimg="img/ih-v3-peep.jpg", tryalt="In Hindsight's landing page: 'You're not doomed. You're just scrolling.' next to a phone and Peep, an orange buddy",
    problem_h="Saved for later. Later never came.",
    problem_lead="Every save is a little promise to come back. Then the feed keeps moving, and the saves pile up in folders nobody opens.",
    problem_more=["TikTok lets you download all of it, your likes, favorites, reposts and watch history, but the export is a wall of JSON."],
    goal="give people their scrolling back in a form they can actually look at, and use.",
    research_lens="User needs", research_h="What 35 people told me",
    research_lead="I surveyed 35 young adults in November 2026 about how they save and scroll.",
    research_img=("img/ih-saves-graveyard.jpg", "A pile of printed saved videos, some paperclipped and a few circled in red", "Saved for later. Later never came."),
    evidence=[
        ("94%", "have tried to find a saved TikTok and given up.", False),
        ("69%", "often scroll longer than they meant to.", False),
        ("54%", "rarely or never go back to what they save.", False),
    ],
    insight="People don't need more ways to save. They need their saves to turn into something.",
    iter_h="From archive to buddy",
    iters=[
        {"short": "Upload", "date": "Oct 7", "img": "img/ih-v1-land.jpg", "alt": "First version: a plain page asking you to drop your TikTok export file",
         "title": "Drop in your export", "what": "A plain page: drop your TikTok export file, or try demo data.",
         "why": "It worked, but it asked a lot up front without showing why it was worth it."},
        {"short": "Dashboard", "date": "Oct 7", "img": "img/ih-v1-dash.jpg", "alt": "First dashboard: a timeline of activity and tabs for Mind, Overview, Rhythm, Timeline, Gallery and Rediscover",
         "title": "A dashboard of your scrolling", "what": "A timeline you can drag to filter, and views for your rhythm, your topics and a Second thought prompt on old saves.",
         "why": "Interesting to look at once. But seeing your habits didn't change what happened to your saves."},
        {"short": "Act", "date": "Nov 9", "img": "img/ih-v2-act.jpg", "alt": "The Act tab: saved videos sorted into Lists, Maps and Plans",
         "title": "Saves into action", "what": "An Act tab that sorts saves into things you can do: recipes to a grocery list, places to a map, plans to a calendar.",
         "why": "This is where the survey pointed: 54% never go back, so the value is in doing, not storing."},
        {"short": "Peep", "date": "Nov 10", "img": "img/ih-v3-peep.jpg", "alt": "The current landing page with Peep: 'You're not doomed. You're just scrolling.'",
         "title": "Meet Peep", "what": "A doomscrolling buddy that keeps you company, nudges you when it's been a while, and turns what you save into plans.",
         "why": "It gave the product a personality and a reason to come back, plus a beta waitlist to test demand."},
    ],
    decisions=[
        dict(h="A buddy, not a blocker", lens="Design",
             pair=(("img/ih-v1-dash.jpg", "The analytics dashboard", "A report card on your habits."),
                   ("img/ih-v3-peep.jpg", "Peep on the landing page", "A companion for what you do next.")),
             labels=("Before", "After"),
             because="69% already scroll longer than they meant to. They don't need another guilt trip. They need help getting something out of it."),
        dict(h="Turn saves into plans", lens="Product strategy",
             pair=(("img/ih-v3-rediscover.jpg", "Rediscover view showing one old save", "Rediscover: look back at saves."),
                   ("img/ih-v2-act.jpg", "Act tab sorting saves into lists, maps and plans", "Act: send saves somewhere useful.")),
             because="Looking back is nice. Doing something is the reason to come back. The Act tab is what makes it a product and not a novelty."),
        dict(h="Everything runs in the browser", lens="Tech",
             because="People are handing over their entire scrolling history, so trust is the feature. The export is read on your device and never uploaded, and video details load lazily from TikTok's public embeds, four at a time."),
    ],
    outcome_h="Where it is now", outcome_lead="Live at inhindsight.net with a working demo and a beta waitlist.",
    features=["Upload your TikTok export, or try it with 5,000 demo entries",
              "Seven views: Mind, Act, Overview, Rhythm, Timeline, Gallery, Rediscover",
              "A draggable timeline that filters every view at once",
              "A clickable Peep prototype and an on-site beta waitlist"],
    outcome_todo=[("Traction", "Add how many people joined the beta waitlist so far.")],
    learn=[("Ask before you build more", "The survey changed the direction more than any feature did."),
           ("Privacy is a design choice", "Keeping everything in the browser shaped the whole architecture, and it's a selling point."),
           ("Next: grow the beta", "Get Peep in front of the people on the waitlist and see which saves actually turn into plans."),
           ("Next: Peep in real life", "Exploring a physical Peep on a Particle Photon 2 that syncs with your In Hindsight data.")],
    next=("karls-friend-bart.html", "Karl's Friend Bart: I got off at the wrong station, so I rebuilt the map."),
    code=None,
    foot="Not affiliated with TikTok",
)
HIND["try"] = "click Try the demo to explore with sample data."

BRANCH = dict(
    slug="branch-out", name="Branch Out",
    desc="a swipe-based way for college students to find open source projects matched to their year, languages and interests.",
    h1="How do college students find their first open source project?",
    sub="GitHub has millions of repositories and no obvious place for a student to start. During the Salesforce Futureforce Tech Launchpad, our team of three built Branch Out: tell it your year, languages and interests, then swipe through matched repos with AI summaries.",
    labels=[("Role", "Full-stack engineer, team of 3"), ("Stack", "React, Node, PostgreSQL, Gemini"), ("Timeline", "Jun to Aug 2025"), ("Type", "Salesforce Futureforce Tech Launchpad")],
    outcomes=[("1 of 30", "Students picked from 3,000+ applicants for the program"), ("192", "Commits across the team, shipped through pull requests"), ("AI summaries", "Every repo explained in plain language")],
    x_problem="Open source is the most open door into real engineering work, but search results favor huge, popular repos that aren't built for beginners.",
    x_made="Pick your year, languages and interests, then swipe through repos matched to you, each with a short AI summary.",
    x_decision="Swipe through one repo at a time instead of scrolling a list of hundreds.",
    live="https://branchout.tech", tryimg="img/bo-swipe.jpg", tryalt="Branch Out's swipe screen: one repository card with tags, an AI summary, and accept and reject buttons",
    problem_h="Where do I even start?",
    problem_lead="Students hear that contributing to open source is the best way to get real experience. Then they open GitHub and face millions of repositories with no way to tell which ones welcome beginners.",
    problem_more=["Search rewards stars, so the top results are the biggest, most intimidating projects."],
    goal="get a student from \"I want to contribute\" to a repo that fits them in a few minutes.",
    research_lens="User needs", research_h="Who we built for",
    research_lead="College students, first through fourth year, looking for their first real contribution.",
    research_img=None,
    evidence=[
        ("Skill level", "Students describe themselves by year in school, not \"beginner\" or \"advanced,\" so that became the skill scale.", False),
        ("Languages", "Most students know one or two languages well, so matching on language cuts the field fast.", False),
        ("Your input", "Add who you talked to or what you noticed (for example, classmates who wanted to contribute but didn't know where), plus one real quote.", True),
    ],
    insight="Finding a first project should feel like browsing, not searching.",
    iter_h="From preferences to a swipe",
    iters=[
        {"short": "Preferences", "date": "Jul 2025", "img": "img/bo-prefs.jpg", "alt": "Preferences page with skill level, languages and topic tags",
         "title": "Start with you", "what": "Pick your year, languages and topics. Everything after this is matched to it.",
         "why": "Asking three quick questions up front beats making students filter hundreds of results later."},
        {"short": "Swipe", "date": "Jul 2025", "img": "img/bo-swipe.jpg", "alt": "Swipe card showing one repository with tags and an AI summary",
         "title": "One repo at a time", "what": "Swipe cards with the repo's tags, languages and an AI summary. Keyboard shortcuts (A and D, or arrow keys) for speed.",
         "why": "One card at a time keeps it light, and the summary answers \"what is this?\" before you open GitHub."},
        {"short": "Search", "date": "Aug 2025", "img": "img/bo-search.jpg", "alt": "Search page with language, topic and skill level filters",
         "title": "Search when you know what you want", "what": "A full filter view for languages, topics and skill level, alongside the swipe.",
         "why": "Swiping is great for discovery. Some students already know what they want, so they needed a direct path too."},
    ],
    decisions=[
        dict(h="Swipe, not a list", lens="Design",
             pair=(("img/bo-search.jpg", "Filter-heavy search view", "A wall of filters and results."),
                   ("img/bo-swipe.jpg", "Single swipe card", "One repo, one decision.")),
             because="A list of 200 repos is where students give up. One card asks for one small decision, and saving the good ones is a swipe."),
        dict(h="Year in school as skill level", lens="Product strategy",
             because="\"Intermediate\" means something different to everyone. Every student knows their year, so the onboarding question takes one second to answer honestly."),
        dict(h="AI summaries on every card", lens="Tech",
             because="READMEs are written for maintainers, not newcomers. I built the Gemini client that writes a short, plain-language summary for each repo, so students can judge fit without leaving the app."),
    ],
    outcome_h="What I built", outcome_lead="My part of the app, from my own commits and pull requests.",
    features=["User accounts: API endpoints, login and signup pages",
              "Saving each student's preferences to the database",
              "The Gemini client behind the AI summaries",
              "Swipe controls with keyboard shortcuts and clear accept and reject icons",
              "The discovery carousel, mobile layouts and light and dark mode",
              "Sidebar, about page and in-app feedback messages"],
    outcome_todo=[("Result", "Add how the final demo went at Salesforce, and any feedback from students who tried it.")],
    learn=[("Ship in small pieces", "Working through pull requests on a team of three taught me to keep changes small enough to review."),
           ("Design from the wireframe", "Matching the wireframe closely kept three people's work feeling like one product."),
           ("Next: real usage data", "Track which matches students actually save, and tune the recommendations from that."),
           ("Next: first contribution", "Go one step further than discovery: point students to a good first issue in each repo.")],
    next=("in-hindsight.html", "In Hindsight: what if your saved videos weren't stuck in folders?"),
    code="https://github.com/Team-10-FTL/branch-out",
    foot="Built with Nathan Kenmognie and Jackie Jurado",
)
BRANCH["try"] = "set your preferences, then swipe through matched repos."

for p in (FEE, HIND, BRANCH):
    page(p)
