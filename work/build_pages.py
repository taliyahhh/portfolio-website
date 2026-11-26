"""Builds the four process pages: a short dated log of what I did, then a reflection.
Run from this folder: python3 build_pages.py
Rules: short, first person, no fluff. Titles get Title Case via tools/titles.py."""
import html, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tools"))
import titles

RESUME = "https://drive.google.com/file/d/1bd_ZmiNHnVtcSxHFkS7MbYG4A5ucGU3_/view?usp=sharing"
e = html.escape
TAG = {"Design": "d", "Tech": "t", "Business": "b", "Research": "r", "Product": "b"}


def shot(src, alt, cap=""):
    c = f"<figcaption>{cap}</figcaption>" if cap else ""
    return f'<figure class="shot"><img src="{src}" alt="{e(alt)}" loading="lazy">{c}</figure>'


def entry(it):
    tag = f'<span class="tag {TAG[it["tag"]]}">{it["tag"]}</span>' if it.get("tag") else ""
    body = "".join(f"<p>{x}</p>" for x in it.get("text", []))
    if it.get("nums"):
        body += '<div class="inline-nums">' + "".join(f"<div><b>{b}</b><span>{s}</span></div>" for b, s in it["nums"]) + "</div>"
    if it.get("list"):
        body += "<ul>" + "".join(f"<li>{x}</li>" for x in it["list"]) + "</ul>"
    if it.get("img"):
        body += shot(*it["img"])
    if it.get("pair"):
        body += '<div class="shots">' + "".join(shot(*s) for s in it["pair"]) + "</div>"
    return f'''      <li>
        <div class="when">{it["when"]}{tag}</div>
        <h3>{it["title"]}</h3>
        {body}
      </li>
'''


def page(p):
    meta = "".join(f"<li><span>{k}</span><b>{v}</b></li>" for k, v in p["meta"])
    links = "".join(f'<a class="{"main" if i == 0 else ""}" href="{u}" target="_blank" rel="noopener">{t} &nearr;</a>' for i, (t, u) in enumerate(p["links"]))
    nums = ('<div class="nums">' + "".join(f"<div><b>{b}</b><span>{s}</span></div>" for b, s in p["nums"]) + "</div>") if p.get("nums") else ""
    video = ""
    if p.get("video"):
        vid, cap = p["video"]
        video = f'''    <div class="video"><iframe src="https://www.youtube-nocookie.com/embed/{vid}" title="{e(cap)}" loading="lazy" allow="accelerometer; encrypted-media; gyroscope; picture-in-picture; fullscreen" allowfullscreen></iframe></div>
    <p class="video-cap">{cap}</p>
'''
    log = "".join(entry(it) for it in p["log"])
    refl = "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in p["reflect"])
    o = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(p["name"])} · Taliyah Harvey</title>
<meta name="description" content="Process and reflection: {e(p["desc"])}">
<link rel="icon" type="image/png" href="../assets/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap">
<link rel="stylesheet" href="process.css">
</head>
<body>
<header class="top">
  <div class="bar">
    <a class="mark" href="/" aria-label="Taliyah Harvey, home"><b>tj</b> <span>Taliyah Harvey</span></a>
    <nav aria-label="Site">
      <a href="/#work">Work</a>
      <a href="/#about">About</a>
      <a href="/#contact">Contact</a>
      <a href="{RESUME}" target="_blank" rel="noopener">Resume</a>
    </nav>
  </div>
</header>

<main class="col">
  <section class="head">
    <a class="back" href="/#work">&larr; All work</a>
    <p class="kick"><b>{e(p["name"])}</b> · {p["when"]}</p>
    <h1>{p["h1"]}</h1>
    <p class="sub">{p["sub"]}</p>
    <ul class="meta">{meta}</ul>
    <div class="links">{links}</div>
    {nums}
{video}  </section>

  <section class="sect" aria-labelledby="how-h">
    <h2 id="how-h">How it went</h2>
    <ol class="log">
{log}    </ol>
  </section>

  <section class="reflect" aria-labelledby="look-h">
    <h2 id="look-h">Looking back</h2>
    <dl>{refl}</dl>
  </section>

  <a class="nextp" href="{p["next"][0]}"><span><small>Next project</small><b>{p["next"][1]}</b></span><span class="go" aria-hidden="true">&rarr;</span></a>
</main>

<footer><div class="bar"><span>Taliyah Harvey</span><span>{p["foot"]}</span></div></footer>
</body>
</html>
'''
    assert "—" not in o, p["slug"]
    path = p["slug"] + ".html"
    open(path, "w").write(o)
    titles.run(path)
    print("wrote", path)


BART = dict(
    slug="karls-friend-bart", name="Karl's Friend Bart", when="Oct 2026",
    desc="an interactive BART map that keeps the official look and shows what's running right now.",
    h1="I got off at the wrong station. So I rebuilt the map.",
    sub="A BART rider who feels confused by the map needs to see where their train is actually going, but the official map is a still picture of every line at once.",
    meta=[("Role", "Solo: design and front-end"), ("Time", "5 days"), ("Type", "Personal")],
    links=[("Try the live map", "https://taliyahhh.github.io/bart-revamp/"), ("Code", "https://github.com/taliyahhh/bart-revamp")],
    nums=[("5 days", "from idea to live site"), ("Live", "trains from BART's API")],
    log=[
        dict(when="Oct 24", tag="Research", title="The problem",
             text=["The official map shows every line at once and never changes. After 9pm, Red and Green stop running and transfers change. Nothing tells you. I found out at the wrong stop."]),
        dict(when="Oct 24", tag="Design", title="My own map first",
             text=["I started with a dark custom map. It looked cool, but it didn't look like BART, and that was the problem."],
             img=("img/bart-v1-fogline.jpg", "My first version: a dark custom map")),
        dict(when="Oct 24", tag="Design", title="Back to the real map",
             text=["Riders already know the official map, so I rebuilt it. Then I added a trip planner, and it got crowded."],
             img=("img/bart-v2-official.jpg", "The official layout with a Plan a Trip box")),
        dict(when="Oct 24", tag="Product", title="Cut the trip planner",
             text=["Other apps already plan trips. I cut it and moved the line controls to a bottom bar your thumb can reach."],
             img=("img/bart-v3-bottombar.jpg", "Line controls in a bottom bar")),
        dict(when="Oct 28", tag="Tech", title="Live trains and a night mode",
             text=["Mini trains from BART's live API. At 9pm the site switches to the evening network on its own."],
             pair=[("img/bart-v4-final-day.jpg", "Day service", "Day"), ("img/bart-v4-final-evening.jpg", "Evening service", "After 9pm")]),
    ],
    reflect=[("What worked", "Keeping the official look. Nobody had to learn anything new."),
             ("What I'd do differently", "I built from my own frustration. Next time I'd watch a few riders use it before building."),
             ("What's next", "Test it with riders, then pitch it to BART as a clearer map.")],
    next=("fee-fi-fo-fund.html", "Fee Fi Fo Fund"),
    foot="Karl is what locals call SF's fog. A fan project, not affiliated with BART.",
)

FEE = dict(
    slug="fee-fi-fo-fund", name="Fee Fi Fo Fund", when="Oct 2026 · SVSD design challenge",
    desc="a storytelling site that shows teens and young adults where their tax dollars go, by zip code.",
    h1="Where did your tax dollars actually go?",
    sub="A teen who feels confused about where their paycheck goes needs to see how their taxes are spent, but the answers are buried in budget PDFs written in billions.",
    meta=[("Role", "Design and development"), ("Team", "Me and Christine Lai"), ("Time", "Oct 2026")],
    links=[("Try it", "https://feefifo.fund"), ("Watch the video", "https://youtu.be/RaYq0kSAdkA"), ("Code", "https://github.com/taliyahhh/tax-site")],
    video=("RaYq0kSAdkA", "Our SVSD submission video, made by Christine Lai."),
    log=[
        dict(when="Oct 17", tag="Research", title="The question",
             text=["Crossing the Bay Bridge, my friend asked why we still pay a toll if our taxes cover roads. I didn't know. Government sites didn't help, and they definitely didn't tell a story.",
                   "SVSD's prompt: pick a specific group and build around storytelling. I picked teens and young adults getting their first paychecks."]),
        dict(when="Oct 18", tag="Tech", title="Finding the data",
             text=["The Census covers every local government, and California's Controller has all 482 cities. Social Security alone is $22 of every $100 federal dollars, so it had to be in there."]),
        dict(when="Oct 18", tag="Design", title="Every category in a box",
             text=["Accurate, but it read like a spreadsheet."],
             img=("img/fee-v1-res.jpg", "First version: a grid of boxed categories")),
        dict(when="Oct 18", tag="Design", title="Floating, sized by money",
             text=["More alive. I added psychedelic animations and deleted them the same day."],
             img=("img/fee-v2-res.jpg", "Second version: floating objects sized by spending")),
        dict(when="Oct 19", tag="Design", title="File folders",
             text=["Hand lettering and real folders for Nation, State and City."],
             img=("img/fee-v3-res.jpg", "Third version: hand-lettered file folders")),
        dict(when="Oct 21", tag="Product", title="Everything out of $100",
             text=["Nobody can picture $1.6 trillion. Everyone gets $100. I added a $100 strip and a story where you're the main character."],
             img=("img/fee-v4-res.jpg", "Final version with a $100 strip")),
    ],
    reflect=[("What worked", "Switching from billions to $100. That's when the numbers clicked."),
             ("What I'd do differently", "We didn't make finals. I'd put it in front of real teens before submitting, not after."),
             ("What's next", "More states, and a way to act on what you learn.")],
    next=("branch-out.html", "Branch Out"),
    foot="Data: U.S. Census Bureau, California State Controller and state budget reports",
)

BRANCH = dict(
    slug="branch-out", name="Branch Out", when="Summer 2025 · Salesforce",
    desc="a swipe-based way for college students to find open source projects matched to their year, languages and interests.",
    h1="Finding your first open source project shouldn't be this hard.",
    sub="A college student who feels intimidated about contributing to open source needs to find a project that fits their level, but GitHub shows the biggest, scariest repos first.",
    meta=[("Role", "Full-stack engineer"), ("Team", "Me, Nathan Kenmognie and Jackie Jurado"), ("Program", "Futureforce Tech Launchpad")],
    links=[("Try it", "https://branchout.tech"), ("Code", "https://github.com/Team-10-FTL/branch-out")],
    nums=[("1 of 30", "picked from 3,000+ applicants"), ("192", "commits as a team")],
    log=[
        dict(when="Jun 2025", tag="Research", title="Talking to our cohort",
             text=["Everyone says contribute to open source. Then you open GitHub and the top results are the biggest, scariest repos.",
                   "We interviewed a few students in our cohort. They wanted to start but didn't know where, and they described themselves by year in school, not skill level."]),
        dict(when="Jul 2025", tag="Design", title="Three questions up front",
             text=["Your year, your languages, your interests. Everything after is matched to that."],
             img=("img/bo-prefs.jpg", "Preferences: skill level by year, languages and topics")),
        dict(when="Jul 2025", tag="Design", title="Swipe, not a list",
             text=["One repo at a time instead of a wall of results."],
             img=("img/bo-swipe.jpg", "A single swipe card for one repo")),
        dict(when="Jul 2025", tag="Tech", title="AI summaries",
             text=["READMEs are written for maintainers. I built the Gemini client that explains each repo in plain language."],
             img=("img/bo-summary.jpg", "A repo card with an AI summary")),
        dict(when="Aug 2025", tag="Tech", title="What I built",
             list=["Accounts, login and signup", "Saving preferences to the database", "The Gemini client", "Swipe with keyboard shortcuts", "Mobile layouts and dark mode"]),
    ],
    reflect=[("What worked", "Small pull requests. Three people, one product, no chaos."),
             ("What I'd do differently", "We built a lot before testing the swipe with students. I'd test the core idea first."),
             ("What's next", "Point students to a good first issue, not just a repo.")],
    next=("in-hindsight.html", "In Hindsight"),
    foot="Built with Nathan Kenmognie and Jackie Jurado",
)

HIND = dict(
    slug="in-hindsight", name="In Hindsight", when="Oct 2026 to now",
    desc="Peep, an AI doomscrolling buddy that turns your TikTok saves into plans.",
    h1="You saved it. Now use it.",
    sub="A TikTok user who feels guilty about how long they scroll needs to get something out of what they save, but their saves disappear into folders they never open.",
    meta=[("Role", "Founder: product, design, code"), ("Platform", "Web now, iOS next"), ("Stage", "In beta")],
    links=[("Try it", "https://inhindsight.net"), ("Meet Peep", "https://inhindsight.net/peep")],
    nums=[("94%", "gave up finding a saved video"), ("11", "waitlist signups in one day")],
    log=[
        dict(when="Oct 2026", tag="Research", title="The idea",
             text=["My saves were a graveyard. I wanted to see them as something other than a folder."],
             img=("img/ih-saves-graveyard.jpg", "Printed saved videos piled up")),
        dict(when="Oct 2026", tag="Tech", title="A dashboard of my scroll",
             text=["Upload your TikTok export and see your scrolling as a timeline, topics and rhythm. It all runs in your browser."],
             img=("img/ih-dash.jpg", "The In Hindsight dashboard")),
        dict(when="Nov 2026", tag="Research", title="Asking people",
             text=["35 surveys and 5 interviews, mostly USC students. Seeing your habits wasn't enough. People wanted their saves to do something."],
             nums=[("94%", "gave up finding a save"), ("54%", "never rewatch"), ("66%", "have 200+ saves")]),
        dict(when="Nov 2026", tag="Design", title="Saves to action",
             text=["Recipes, places and plans sent to Maps, Calendar and Reminders."],
             img=("img/ih-v2-act.jpg", "The Act tab")),
        dict(when="Nov 2026", tag="Design", title="Meet Peep",
             text=["A buddy, not a blocker. Peep asks what you're on TikTok for, gets sleepy when you scroll too long, and files what you find."],
             img=("img/ih-peep-flow.jpg", "Peep before, during and after you scroll")),
        dict(when="Nov 2026", tag="Business", title="Free, then $4 a month",
             text=["63% of people I surveyed would pay or consider it. 11 people joined the waitlist in one day."],
             img=("img/ih-business.jpg", "Free, Plus at $4 a month, and sharing")),
    ],
    reflect=[("What worked", "Asking people. The survey changed the product more than any feature."),
             ("What I'd do differently", "I built the dashboard before talking to anyone. I'd flip that."),
             ("What's next", "A 100-person private beta in January, then Peep on iOS in the spring.")],
    next=("karls-friend-bart.html", "Karl's Friend Bart"),
    foot="Not affiliated with TikTok",
)

for p in (BART, FEE, BRANCH, HIND):
    page(p)
