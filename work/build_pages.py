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


def num(b, s, src=""):
    return f'<div><b>{b}</b><span>{s}</span>' + (f'<small class="src">{src}</small>' if src else "") + "</div>"


def entry(it):
    tag = f'<span class="tag {TAG[it["tag"]]}">{it["tag"]}</span>' if it.get("tag") else ""
    body = "".join(f"<p>{x}</p>" for x in it.get("text", []))
    if it.get("nums"):
        body += '<div class="inline-nums">' + "".join(num(*n) for n in it["nums"]) + "</div>"
    if it.get("list"):
        body += "<ul>" + "".join(f"<li>{x}</li>" for x in it["list"]) + "</ul>"
    if it.get("src"):
        body += f'<p class="src">Source: {it["src"]}</p>'
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


import re as _re
def fill(t):
    m = _re.match(r"^A (.+?) who feels (.+?) about (.+?) needs to (.+?), but (.+)\.$", t)
    assert m, t
    a, f, k, st, o = (f'<span class="blank">{x}</span>' for x in m.groups())
    return f"A {a} who feels {f} about {k} needs to {st}, but {o}."


def page(p):
    meta = "".join(f"<li><span>{k}</span><b>{v}</b></li>" for k, v in p["meta"])
    links = "".join(f'<a class="{"main" if i == 0 else ""}" href="{u}" target="_blank" rel="noopener">{t} &nearr;</a>' for i, (t, u) in enumerate(p["links"]))
    nums = ('<div class="nums">' + "".join(num(*n) for n in p["nums"]) + "</div>") if p.get("nums") else ""
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
    <p class="kick">{p["when"]}</p>
    <h1>{e(p["name"])}</h1>
    <p class="plabel">Problem statement</p>
    <p class="sub">{fill(p["sub"])}</p>
    <ul class="meta">{meta}</ul>
    {f'<div class="links">{links}</div>' if links else ''}
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
    desc="an interactive BART map that keeps the official look and shows what's actually running.",
    sub="A BART rider who feels confused about the map needs to see where their train is actually going, but the official map is a still picture of every line at once.",
    meta=[("Role", "Design and front end"), ("Team", "Solo")],
    links=[("Try the live map", "https://taliyahhh.github.io/bart-revamp/"), ("Code", "https://github.com/taliyahhh/bart-revamp")],
    nums=[("5 days", "idea to live site"), ("Live", "trains from BART's API")],
    log=[
        dict(when="Oct 24", tag="Research", title="Same Map, All Day",
             text=["BART's map shows every line at once, all day. After 9pm the Red and Green lines stop running, and the map still shows them.",
                   "Even if you grew up on BART, you still have to stop and decode it. The map isn't wrong. It just doesn't move."]),
        dict(when="Oct 24", tag="Design", title="Fogline",
             text=["My first version was a dark custom map I called Fogline. It looked good. It also didn't look like BART at all, and BART's map is the one people already know how to read."],
             img=("img/bart-v1-fogline.jpg", "Fogline, my first version")),
        dict(when="Oct 24", tag="Design", title="Back to the Official Map",
             text=["So I rebuilt the official one. Same colors, same layout. Then I added a trip planner and the screen got crowded fast."],
             img=("img/bart-v2-official.jpg", "The official layout with a Plan a Trip box")),
        dict(when="Oct 24", tag="Product", title="Cut the Trip Planner",
             text=["Google Maps already plans trips. Mine was just more stuff on the screen, so it went. The line controls moved to a bar at the bottom, where your thumb already is."],
             img=("img/bart-v3-bottombar.jpg", "Line controls in a bottom bar")),
        dict(when="Oct 28", tag="Tech", title="Live Trains and Evening Service",
             text=["Little trains move along the map using BART's live departures. At 9pm the site switches to evening service on its own, goes dark, and marks Red and Green as off tonight."],
             pair=[("img/bart-v4-final-day.jpg", "Day service", "Day"), ("img/bart-v4-final-evening.jpg", "Evening service", "After 9pm")]),
    ],
    reflect=[("What worked", "Keeping the official map. The less I changed, the easier it was to read."),
             ("What I'd do differently", "Nobody but me has really used it yet. I'd put it in front of riders before adding anything else."),
             ("What's next", "Get it in front of BART riders.")],
    next=("fee-fi-fo-fund.html", "Fee Fi Fo Fund"),
    foot="Karl is what locals call SF's fog. A fan project, not affiliated with BART.",
)

FEE = dict(
    slug="fee-fi-fo-fund", name="Fee Fi Fo Fund", when="Oct 2026 · SVSD design challenge",
    desc="a storytelling site that shows teens and young adults where their tax dollars go, by zip code.",
    sub="A teen who feels confused about where their paycheck goes needs to see how their taxes are spent, but government budgets are bland and hard to navigate.",
    meta=[("Role", "Design and development"), ("Team", '<a href="https://www.linkedin.com/in/chrstnlai/" target="_blank" rel="noopener">Christine Lai</a> and me')],
    links=[("Try it", "https://feefifo.fund"), ("Watch the video", "https://youtu.be/RaYq0kSAdkA"), ("The challenge", "https://svsdschool.github.io/competition/"), ("Code", "https://github.com/taliyahhh/tax-site")],
    video=("RaYq0kSAdkA", "Our SVSD submission video, made by Christine Lai."),
    log=[
        dict(when="Oct 17", tag="Research", title="Why Do We Pay the Toll?",
             text=["Crossing the Bay Bridge, my friend asked why we pay a toll if our taxes already cover roads. I didn't know, and the budgets that would tell me were bland and hard to navigate.",
                   "SVSD asked for a storytelling project for a specific group. Ours was teens and young adults getting their first paychecks."]),
        dict(when="Oct 18", tag="Tech", title="Every Zip Code",
             text=["All 50 states and about 41,000 zip codes, at three levels:"],
             list=["Nation: federal spending, clearly marked", "State: your state's spending, plus the federal money it gets", "City or county: local budgets and services"],
             src="Census Bureau, 2022 Census of Governments; U.S. Treasury, Final Monthly Treasury Statement, FY2026"),
        dict(when="Oct 18", tag="Research", title="Maps I Looked At",
             text=["zipdecode lights up zip codes as you type. Climate Zones asks how your own city will feel. I wanted both: type your zip, and now it's about you."],
             pair=[("img/fee-ref-zipdecode.jpg", "A US map of zip code dots", "zipdecode by Ben Fry"), ("img/fee-ref-climate.jpg", "Climate Zones world map", "Climate Zones by Derek Taylor, The Pudding")]),
        dict(when="Oct 18", tag="Design", title="Version 1: Boxes",
             text=["Every category in its own box. Accurate, and it read like a spreadsheet."],
             img=("img/fee-v1-res.jpg", "First version: a grid of boxed categories")),
        dict(when="Oct 18", tag="Design", title="Version 2: Floating",
             text=["Objects floating around the page, sized by how much money went there. I also added psychedelic animations. They lasted about a day."],
             img=("img/fee-v2-res.jpg", "Second version: floating objects sized by spending")),
        dict(when="Oct 19", tag="Design", title="Version 3: File Folders",
             text=["Hand lettering and folders for Nation, State and City."],
             img=("img/fee-v3-res.jpg", "Third version: hand-lettered file folders")),
        dict(when="Oct 21", tag="Product", title="Out of $100",
             text=["Nobody can picture $1.7 trillion. Everybody can picture $100. So every number became dollars out of $100, and the story makes you the main character."],
             src="$1.7 trillion is federal Social Security spending. U.S. Treasury, Final Monthly Treasury Statement, FY2026",
             img=("img/fee-v4-res.jpg", "Final version with a $100 strip")),
        dict(when="Oct 21", tag="Product", title="Now What?",
             text=["Knowing where it went is half of it. The Footprint page is the other half: find your representatives, register to vote, get free tax help, show up to a budget hearing."]),
        dict(when="Oct 22", tag="Design", title="Video Direction and Mood Board",
             text=["Christine made the video and the mood board. The video is real places taxes pay for: parks, libraries, beaches, courts. The mood board is loud collage with cut-out photos everywhere."],
             pair=[("img/fee-video-direction.jpg", "Collage of parks, libraries, beaches and courts", "Video direction"), ("img/fee-moodboard.jpg", "Collage-style poster references", "Mood board")]),
    ],
    reflect=[("What worked", "Out of $100. That's when the numbers started making sense."),
             ("What I'd do differently", "The mood board called for real photo cutouts. We shipped with emoji stand-ins, and that's the first thing I'd fix."),
             ("What's next", "Waiting on feedback from the SVSD organizer.")],
    next=("branch-out.html", "Branch Out"),
    foot="Data: U.S. Treasury, U.S. Census Bureau and state budget reports",
)

BRANCH = dict(
    slug="branch-out", name="Branch Out", when="Summer 2025 · Salesforce",
    desc="a swipe-based way for college students to find open source projects matched to their year, languages and interests.",
    sub="A college student who feels intimidated about contributing to open source needs to find a project that fits their level, but it's hard to find a good range of open source projects on GitHub.",
    meta=[("Role", "Front end and design lead"), ("Team", "Nathan, Jackie and me"), ("Program", "Futureforce Tech Launchpad")],
    links=[("Try it", "https://branchout.tech"), ("Code", "https://github.com/Team-10-FTL/branch-out")],
    nums=[("1 of 30", "picked from 3,000+ applicants", "Salesforce Futureforce Tech Launchpad, 2025"), ("3 of 3", "of us got return offers")],
    log=[
        dict(when="Jun 2025", tag="Research", title="Where Do You Even Start?",
             text=["Everyone tells students to contribute to open source. Then you search GitHub and it's hard to find a good range of projects to start with.",
                   "Our cohort was 30 students trying to get into tech, so we built for people like us."]),
        dict(when="Jul 2025", tag="Design", title="Three Questions",
             text=["Your year in school, your languages, what you're into. Every match after that comes from those three answers."],
             img=("img/bo-prefs.webp", "Preferences: year, languages and topics")),
        dict(when="Jul 2025", tag="Design", title="One Repo at a Time",
             text=["Swipe right to save, left to skip. One card is a lot less scary than a page of results."],
             img=("img/bo-swipe.webp", "Swiping through repos one at a time")),
        dict(when="Jul 2025", tag="Tech", title="READMEs You Can Actually Read",
             text=["READMEs are written for the people who already work on the project. Gemini summarizes each one in plain language for someone seeing it for the first time."],
             img=("img/bo-summary.jpg", "A repo card with an AI summary")),
        dict(when="Aug 2025", tag="Tech", title="Who Did What",
             text=["I led design and the front end, and did some of the MCP work. Nathan and Jackie owned the back end."],
             list=["Design across the app", "Swipe cards, preferences and search", "Keyboard shortcuts for swiping", "Mobile layouts and dark mode", "Some of the MCP work"],
             img=("img/bo-team.jpg", "Taliyah, Nathan and Jackie")),
        dict(when="Aug 2025", tag="Business", title="Demo Day",
             text=["Our pitch put Branch Out next to GitHub, Devpost and LeetCode. GitHub helps you find projects. Devpost feels made for students. LeetCode matches your skill level and teaches you. Branch Out does all of it in one place.",
                   "The product worked live, and all three of us got return offers."],
             img=("img/bo-demo.jpg", "Presenting at Salesforce: Branch Out next to GitHub, Devpost and LeetCode")),
    ],
    reflect=[("What worked", "Splitting it cleanly. I owned what you see, Nathan and Jackie owned what you don't, and we didn't step on each other."),
             ("What I'd do differently", "We were our own users. I'd get it in front of students outside our program before calling it done."),
             ("What's next", "Match people to a good first issue inside the repo.")],
    next=("in-hindsight.html", "In Hindsight"),
    foot="Built with Nathan Kenmognie and Jackie Jurado",
)

HIND = dict(
    slug="in-hindsight", name="In Hindsight", when="Oct 2026 to now",
    desc="Peep, an AI doomscrolling buddy that turns your TikTok saves into plans.",
    sub="A TikTok user who feels guilty about how long they scroll needs to get something out of what they save, but their saves disappear into folders they never open.",
    meta=[("Role", "Founder"), ("Platform", "Web, iOS next"), ("Stage", "MVP live")],
    links=[("Try it", "https://inhindsight.net"), ("Meet Peep", "https://inhindsight.net/peep")],
    nums=[("94%", "gave up finding a saved video", "Survey of 35 young adults, Nov 2026"), ("11", "waitlist signups in one day", "In Hindsight waitlist, Nov 2026")],
    log=[
        dict(when="Oct 2026", tag="Research", title="We Save Everything, Then Forget It All",
             text=["Recipes, places, career advice. We save all of it and almost never go back.",
                   "Over half the world is on social media, and the apps barely do anything with what you save. In my research doc I called it a lack of depth in social media archival formatting. Basically, your saves go nowhere.",
                   "Hence the name. You look back at what you already watched, in hindsight, and actually use it."],
             img=("img/ih-saves-graveyard.jpg", "Printed saved videos piled up")),
        dict(when="Oct 2026", tag="Tech", title="Know Your Scroll",
             text=["First I built a dashboard. Upload your TikTok export and see your scroll as a timeline, your topics and your rhythm. Everything stays in your browser."],
             img=("img/ih-dash.jpg", "The In Hindsight dashboard")),
        dict(when="Nov 9", tag="Research", title="35 Surveys, 5 Interviews",
             text=["I posted a survey on SideChat, Snapchat, Reddit and iMessage and got 35 responses in a day. The surveys told me what people do. The interviews told me how scrolling feels.",
                   "The answers I kept rereading were people wanting something out of it:"],
             list=["“I wish I could turn my inspiration, recipes, outfits, and products into something tangible.”",
                   "“For my links to be organized automatically”",
                   "“Feeling like I remember or was impacted by what I watched”"],
             src="In Hindsight survey of 35 young adults, mostly USC students, shared on SideChat, Snapchat, Reddit and iMessage, Nov 9, 2026",
             nums=[("94%", "gave up finding a save"), ("69%", "scroll longer than they meant to"), ("66%", "have 200+ saves")]),
        dict(when="Nov 2026", tag="Design", title="You Saved It. Now Use It.",
             text=["So the product changed. Recipes go to Reminders, places go to Maps, plans go to Calendar."],
             img=("img/ih-v2-act.jpg", "The Act tab")),
        dict(when="Nov 2026", tag="Design", title="Peep",
             text=["Peep, as in “I peeped it.” Also, it's cute.",
                   "Before you scroll, Peep asks what you're on TikTok for. While you scroll, Peep gets sleepy. Find something good, share it to Peep, and it gets filed. Every Sunday your week gets recapped like a feed.",
                   "Peep is a concept right now. It's next on the list to build."],
             img=("img/ih-peep-screens.jpg", "Peep concept screens: what you're here for, a sleepy timer, share to Peep, a weekly recap, and keep or let it go")),
        dict(when="Nov 2026", tag="Business", title="Who Else Is Doing This",
             text=["Opal, one sec and Screen Time track your time. TikTok Collections, Dewey and TapFold hold your saves. None of them look at what you saved and do something with it. That's the gap."],
             img=("img/ih-competition.jpg", "Competitive map: time-focused versus content-focused, passive versus proactive")),
        dict(when="Nov 2026", tag="Business", title="How High Is Up?",
             text=["19.4 million U.S. college students to start, then 100 million U.S. adults on TikTok. Free to use, Plus at $4 a month. 63% of people I surveyed said yes or maybe to paying, and 11 joined the waitlist in one day."],
             src="DataReportal 2026; Pew Research Center 2025; U.S. Census Bureau 2025; National Student Clearinghouse, Fall 2025; In Hindsight survey of 35 young adults, mostly USC students, shared on SideChat, Snapchat, Reddit and iMessage, Nov 9, 2026",
             img=("img/ih-business.jpg", "Free, Plus at $4 a month, and sharing")),
        dict(when="2027", tag="Business", title="Where It's Going",
             text=["The MVP is live and took 2 months. Next is a private beta for 100 people in January, Peep on iOS in the spring, and 1,000 users by summer. I applied for a $3,000 IYA Ignite grant to get to the beta."],
             img=("img/ih-milestones.jpg", "Milestones from MVP to 1,000 users")),
    ],
    reflect=[("What worked", "Asking. The survey is the reason it went from a dashboard to Peep."),
             ("What I'd do differently", "I built the dashboard first and asked people second. It worked out, but I'd flip it."),
             ("What's next", "Build Peep and get it to 100 beta users.")],
    next=("bite-back.html", "Bite Back"),
    foot="Not affiliated with TikTok",
)

BITE = dict(
    slug="bite-back", name="Bite Back", when="Fall 2026 to now · IYA Garage Experience",
    desc="a small-plates dinner built around invasive species, with education and community at the table.",
    sub="A food lover who feels unaware about invasive species needs to see that eating them can help, but they almost never show up on a menu.",
    meta=[("Program", "IYA Garage Experience (GX)"), ("Team", '<a href="https://www.linkedin.com/in/maya-parthasarathy/" target="_blank" rel="noopener">Maya Parthasarathy</a>, <a href="https://www.linkedin.com/in/jones-mays-ii-21a2a6215/" target="_blank" rel="noopener">Jones Mays</a>, <a href="https://www.linkedin.com/in/maxine-ivey-624070268/" target="_blank" rel="noopener">Maxine Ivey</a> and me'), ("Stage", "Applying for a grant")],
    links=[("About GX", "https://iovine-young.usc.edu/careers-learning-outcomes#capstone-experience-fusing-innovation-and-industry")],
    log=[
        dict(when="Fall 2026", tag="Business", title="What GX Is",
             text=["GX is the Garage Experience, the Iovine and Young Academy's senior capstone. It's a student-led research and development project that runs two semesters, with mentorship from faculty and people in industry. You pick the problem, and you have the whole year to build toward it."]),
        dict(when="Fall 2026", tag="Product", title="Invasiv",
             text=["It started as Invasiv, a food product made from invasive species. Then we tried invasive food consulting. Then back to products: a brand making different things from invasive species."]),
        dict(when="Oct 2026", tag="Design", title="Bite Back",
             text=["Now it's a dinner. Bite Back is small and exclusive, served as small plates, with the education and the community built into the night."]),
        dict(when="Oct 2026", tag="Research", title="Why Animals",
             text=["We focus on invasive animals over plants. They're easier to source."]),
        dict(when="Oct 2026", tag="Tech", title="The Landing Page",
             text=["A landing page for Invasiv, which I worked on."]),
        dict(when="Nov 2026", tag="Business", title="Grant Application",
             text=["We're applying for a grant for Bite Back."]),
    ],
    reflect=[("What's next", "Finish the grant application and plan the first dinner.")],
    next=("karls-friend-bart.html", "Karl's Friend Bart"),
    foot="An IYA Garage Experience project",
)

for p in (BART, FEE, BRANCH, HIND, BITE):
    page(p)
