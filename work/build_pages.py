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
    m = _re.match(r"^An? (.+?) who feels (.+?) about (.+?) needs to (.+?), but (.+)\.$", t)
    assert m, t
    a, f, k, st, o = (f'<span class="blank">{x}</span>' for x in m.groups())
    return f"{t.split()[0]} {a} who feels {f} about {k} needs to {st}, but {o}."


def book_html(b):
    pages = b["pages"]
    thumbs = "".join(f'<button type="button" data-i="{i}" aria-label="Page {i+1}"><img src="{src}" alt="" loading="lazy"></button>' for i, src in enumerate(pages))
    import json as _json
    return f'''
  <section class="sect bookwrap" aria-labelledby="book-h">
    <h2 id="book-h">{b["title"]}</h2>
    <p class="book-hint">{b["hint"]}</p>
    <div class="book" id="book" data-pages='{_json.dumps(pages)}'>
      <div class="spread"><div class="slot l"><img alt=""></div><div class="slot r"><img alt=""></div></div>
      <div class="leaf" aria-hidden="true"><img class="f" alt=""><img class="b" alt=""></div>
      <button type="button" class="edge prev" aria-label="Previous page"></button>
      <button type="button" class="edge next" aria-label="Next page"></button>
    </div>
    <div class="book-ctrl"><button type="button" class="bprev" aria-label="Previous page">&larr;</button><span class="bcount" aria-live="polite"></span><button type="button" class="bnext" aria-label="Next page">&rarr;</button></div>
    <div class="book-thumbs">{thumbs}</div>
  </section>
<script src="book.js" defer></script>
'''


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
    book = book_html(p["book"]) if p.get("book") else ""
    back = p.get("back", "/#work")
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
    <a class="back" href="{back}">&larr; {p.get("backlabel", "All work")}</a>
    <p class="kick">{p["when"]}</p>
    <h1>{e(p["name"])}</h1>
    <p class="plabel">Problem statement</p>
    <p class="sub">{fill(p["sub"])}</p>
    <ul class="meta">{meta}</ul>
    {f'<div class="links">{links}</div>' if links else ''}
    {nums}
{video}  </section>
{book}
  <section class="sect" aria-labelledby="how-h">
    <h2 id="how-h">How it went</h2>
    <ol class="log">
{log}    </ol>
  </section>

{f'''  <section class="reflect" aria-labelledby="look-h">
    <h2 id="look-h">Looking back</h2>
    <dl>{refl}</dl>
  </section>
''' if refl else ""}
  <a class="nextp" href="{p["next"][0]}"><span><small>{p.get("nextlabel", "Next project")}</small><b>{p["next"][1]}</b></span><span class="go" aria-hidden="true">&rarr;</span></a>
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
             ("What I'd do differently", "Talk to the people who ride it every day, especially first-timers, older riders and people who don't use much tech, and ask where the map lets them down."),
             ("What's next", "Get it in front of people at BART, ask what they think is missing, and see if there's room to collaborate, even as a part-time contractor on the site.")],
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
             ("What I'd do differently", "Build a much bigger database, and create our own open source challenges by skill and topic. A little like LeetCode, but for contributing to real projects.")],
    next=("bite-back.html", "Bite Back"),
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
             ("What's next", "Get a grant, publish In Hindsight to the public as an app or browser extension, and stay on the timeline: a 100-person beta in January, Peep on iOS in the spring, and 1,000 users by summer.")],
    next=("karls-friend-bart.html", "Karl's Friend Bart"),
    foot="Not affiliated with TikTok",
)

BITE = dict(
    slug="bite-back", name="Bite Back", when="Fall 2026 to now · IYA Garage Experience",
    desc="chef-led small plates dinners made from invasive species, with the story behind every bite.",
    sub="An adventurous eater who feels unsure about eating invasive species needs to taste them and hear why they matter, but they almost never show up on a menu.",
    meta=[("Role", "Product"), ("Team", '<a href="https://www.linkedin.com/in/maya-parthasarathy/" target="_blank" rel="noopener">Maya Parthasarathy</a>, <a href="https://www.linkedin.com/in/jones-mays-ii-21a2a6215/" target="_blank" rel="noopener">Jones Mays</a>, <a href="https://www.linkedin.com/in/maxine-ivey-624070268/" target="_blank" rel="noopener">Maxine Ivey</a> and me'), ("Program", "IYA Garage Experience (GX)"), ("Stage", "First dinner in December")],
    links=[("Instagram", "https://www.instagram.com/biteback.la/"), ("About GX", "https://iovine-young.usc.edu/careers-learning-outcomes#capstone-experience-fusing-innovation-and-industry")],
    nums=[("30+", "guests across 3 test dinners", "Bite Back validation data, 2026"), ("$40", "a seat at Dinner #1")],
    log=[
        dict(when="Fall 2026", tag="Business", title="What GX Is",
             text=["GX is the Garage Experience, the Iovine and Young Academy's senior capstone. It's a student-led research and development project that runs two semesters, with mentorship from faculty and people in industry. You pick the problem, and you have the whole year to build toward it."]),
        dict(when="Fall 2026", tag="Product", title="Invasiv",
             text=["It started as Invasiv, a food product made from invasive species. Then we tried invasive food consulting. Then back to products: a brand making different things from invasive species."]),
        dict(when="Fall 2026", tag="Research", title="Nobody's Eating Them",
             text=["Lots of invasive species are edible. People just don't know they're available, what they taste like, or that eating them helps. It's exposure, and it's what we think belongs in our diets."],
             nums=[("$21B", "a year: what invasive species cost the U.S."), ("6\u20137", "exposures before people start liking a new food")],
             src="Fantle-Lepczyk et al., Science of the Total Environment (2022); chef Bun Lai via CBC"),
        dict(when="Oct 2026", tag="Design", title="Pull Up a Chair",
             text=["So it became a dinner. Chef-led small plates made from edible invasive species, with the story behind each one. Familiar formats make a new ingredient easier to try.",
                   "It's for adventurous eaters, 21 to 35, who care about the environment and like a curated night out."],
             list=["Discover: see the menu and the concept", "Book: reserve a seat and share dietary needs", "Arrive and eat: small plates, a story with each", "Take away: recipes and where to find the ingredients locally", "Follow up: a short survey"],
             img=("img/bb-brand.jpg", "Brand direction from our deck: Pull up a chair. Eat the invasion.")),
        dict(when="Oct 2026", tag="Design", title="Mood Board",
             text=["Supper clubs, handwritten menus, ingredients labeled right on the plate, long tables with candles. Warm, a little playful, and close enough to touch."],
             img=("img/bb-moodboard.jpg", "Our prototype mood board")),
        dict(when="Oct 2026", tag="Research", title="Why Animals",
             text=["We focus on invasive animals over plants. They're easier to source. For plants, our only real option was basically trespassing."]),
        dict(when="Oct 2026", tag="Research", title="Three Test Dinners",
             text=["Before calling it anything, we hosted three test dinners. 30+ people came and we made $300. We also got 10 email signups and 12 QR scans on campus."],
             img=("img/bb-dinners.jpg", "Three previous dinners: 30+ people, $300")),
        dict(when="Nov 2026", tag="Design", title="Four Courses",
             text=["Every dish is built around an invasive species."],
             list=["Green crab bisque, with seasonal salad and warm bread", "Catfish nuggets", "Asian carp hush puppies", "Ice plant ice cream"],
             img=("img/bb-menu.jpg", "The four course menu")),
        dict(when="Nov 2026", tag="Business", title="Does It Make Money?",
             text=["Dinner #1 is 10 paying guests at $40. That's $400 in, $364 in costs, and $36 left over. Small, but it breaks even, which is the goal.",
                   "Bigger picture: about $11M a year in LA adults 20 to 34 who'd book a dinner like this, and about $43K we could realistically capture by year two."],
             src="Market Intelo Supper Club Market Report (2025); U.S. Census ACS, Los Angeles County; Bite Back estimates",
             img=("img/bb-model.jpg", "Dinner #1 financial model")),
        dict(when="Nov 2026", tag="Business", title="Who Else Is Doing This",
             text=["There are one-night invasive dinners in Vancouver and Kaua\u02bbi, invasive restaurants in Connecticut and London, and supper clubs all over LA. Nobody is doing recurring invasive species dinners in LA at $40 a seat."]),
        dict(when="Nov 2026", tag="Business", title="Every Dinner Becomes Content",
             text=["10 people at the table, thousands watching online. We host, film, post, grow, then scale. Our socials are set up at @biteback.la and we're drafting posts now. The goal is 50K followers by May 2027."]),
        dict(when="Dec 2026", tag="Product", title="Dinner #1",
             text=["A 10-person dinner for IYA's C10 cohort. We want to see who shows up, what they'll pay, and whether it breaks even."],
             img=("img/bb-dinner1.jpg", "Dinner #1 concept")),
    ],
    reflect=[("What's next", "Submit a grant application and get posts out before our first small plates dinner in December. Stay tuned on <a href=\"https://www.instagram.com/biteback.la/\" target=\"_blank\" rel=\"noopener\">our Instagram</a>.")],
    next=("in-hindsight.html", "In Hindsight"),
    foot="An IYA Garage Experience project",
)

HANG = dict(
    slug="the-hangout", name="The Hangout", when="Spring 2026 · IDSN-522, Inclusive Design and Design Allyship",
    desc="an inclusive design toolkit for low-pressure third spaces where tween girls can connect, create and just be.",
    sub="A tween girl who feels pressure about how she looks online needs to find a low-pressure place to figure out who she is, but third spaces have disappeared and social media fills the gap.",
    meta=[("Team", "Natalie Guldalian, Sierra McRay, Bradli Powell, Maia Weingard and me"), ("Class", "IDSN-522 with Professor Wolter"), ("Deliverable", "Inclusive design toolkit")],
    links=[],
    back="/#classwork", backlabel="All class projects", nextlabel="Next class project",
    book=dict(title="The Toolkit", hint="Our final group deliverable. Click a page edge, swipe, or use your arrow keys to flip through.",
              pages=[f"img/hangout/p{n:02d}.jpg" for n in range(1, 21)]),
    log=[
        dict(when="Start", tag="Research", title="Where It Started",
             text=["I came in curious about third spaces, and how few of them are left now that so much of life has moved online. One teammate cared about mental health. Another wanted to focus on teen girls. Put together, that was our niche: third spaces where teen girls can actually thrive."]),
        dict(when="Research", tag="Research", title="The In-Between Is Collapsing",
             text=["\u201cTween\u201d started in the 1980s as a marketing term. Now the stage itself is shrinking. Girls 10 to 13 have adult beauty routines, and in 2023 tweens 8 to 12 drove 49% of U.S. skincare sales growth."],
             src="Figures as cited in our toolkit"),
        dict(when="Research", tag="Research", title="Third Spaces",
             text=["Third spaces are Ray Oldenburg's term for places outside home and school: parks, libraries, diners. Most of them are gone or cost money. When there's nowhere to go, identity gets built online, out of whatever the algorithm surfaces."]),
        dict(when="Solution", tag="Design", title="The Hangout",
             text=["Free pop-ups in libraries, parks and community centers, built around four kinds of activities: creative expression, social connection, physical play and STEAM. Brands can bring materials or expertise, but nothing gets sold."],
             list=["No likes, followers or public metrics", "Drop in, drop out, nothing graded", "Walk-ins always welcome, so no phone is required"]),
        dict(when="Solution", tag="Product", title="A Companion App",
             text=["The app tracks events, badges and photo booth pictures. There's no messaging. Parents approve every event and get a pickup code at check-in."]),
        dict(when="My part", tag="Design", title="What I Made",
             text=["I helped design the toolkit itself, and made the cover, Goals, Third Spaces and Design Guidelines pages."],
             pair=[("img/hangout/p07.jpg", "Third Spaces page", "Third Spaces"), ("img/hangout/p14.jpg", "Design Guidelines page", "Design Guidelines")]),
        dict(when="Guidelines", tag="Design", title="Design Guidelines",
             text=["Six inclusive design principles for anyone building a space like this:"],
             list=["Recognize exclusion", "Design for a range of needs", "Provide flexibility and choice", "Reduce physical and social barriers", "Prioritize clarity and simplicity", "Support independence and belonging"]),
    ],
    reflect=[],
    next=("eruca.html", "Eruca"),
    foot="IDSN-522 · Professor Wolter",
)

ERUCA = dict(
    slug="eruca", name="Eruca", when="Fall 2024 · ACAD-324, Practice of Design",
    desc="a carry-on with caterpillar-inspired wheels for cobblestones, transit and old stairs.",
    sub="A young traveler who feels frustrated about dragging a suitcase through European cities needs to roll over cobblestones and stairs easily, but standard suitcase wheels get stuck and break.",
    meta=[("Role", "Product management"), ("Team", "Altamush Merchant, Lauren Budovsky, Cayetana Moncayo, Henry Yin and me"), ("Class", "ACAD-324 with Professor Wolter")],
    links=[],
    back="/#classwork", backlabel="All class projects", nextlabel="Next class project",
    log=[
        dict(when="Analysis", tag="Research", title="Built for Airports",
             text=["The brief was biomimicry x luggage. Suitcases work fine in an airport. Then you hit cobblestone streets, public transit and stairs in historic buildings, and the wheels give out.",
                   "How might we redesign luggage for travelers 18 to 35 so it actually works in European cities, beyond the airport?"],
             img=("img/eruca/problem.jpg", "Travelers dragging suitcases over cobblestones")),
        dict(when="Definition", tag="Research", title="Rachel",
             text=["We surveyed and interviewed travelers, then built a persona: Rachel Chen, a 28-year-old UI/UX designer and digital nomad. Carry-on only, hard-shell, efficiency-obsessed, and loyal to her suitcase brand even though it lets her down on the road."]),
        dict(when="Ideation", tag="Design", title="Wheels, Carrying, Structure",
             text=["We grouped our brainstorm into wheels, carrying and structure, pinned two standouts from each, and put all six on an impact and feasibility matrix. Filtering by our How Might We first meant nothing landed in the reject corner."],
             img=("img/eruca/matrix.jpg", "Impact and feasibility matrix")),
        dict(when="Selection", tag="Design", title="Move Like a Caterpillar",
             text=["Millipedes, centipedes and caterpillars move in a wave, with each leg handling its own bump. So instead of 2 wheels per side, we designed a train of 6 to 8 small wheels, each with its own suspension. Tank treads were the other reference."],
             img=("img/eruca/inspiration.jpg", "Caterpillar movement study and tank tread reference")),
        dict(when="Branding", tag="Business", title="Eruca",
             text=["Eruca is Latin for caterpillar. The brand pairs Art Nouveau curves with earthy colors and metal accents, so it reads European and a little luxury."],
             img=("img/eruca/moodboard.jpg", "Art Nouveau mood board")),
        dict(when="Implementation", tag="Tech", title="Renders and CAD",
             text=["Sketches became renders, then CAD models of the wheel and rail system."],
             pair=[("img/eruca/renders.jpg", "Suitcase renders with wheel trains", "Renders, made with Vizcom"), ("img/eruca/cad.jpg", "CAD models of wheels and rails", "CAD")]),
        dict(when="Evaluation", tag="Research", title="Testing It on Real Ground",
             text=["We ran usability tests with people in our target age range and scenario tests on different surfaces. Rolling it felt natural. But people wanted 360-degree spin like the suitcases they already own, and to roll it tilted."],
             pair=[("img/eruca/lofi.jpg", "Lo-fi wheel prototype", "Lo-fi prototype"), ("img/eruca/testing.jpg", "Scenario testing on cobblestone and fabric", "Scenario testing")]),
        dict(when="Implementation", tag="Product", title="Rebuild",
             text=["Testing left us with three problems: the mechanism, direction and feasibility. So we ripped the wheels out of a real suitcase, 3D printed new wheels and rails, assembled, cut the rails shorter, reprinted, and spray painted it."],
             img=("img/eruca/finishing.jpg", "Final build: spray painting and assembly")),
        dict(when="Final", tag="Product", title="The Eruca Pod",
             text=["A luxury carry-on with arthropod wheels. If it went to production: a polycarbonate shell, sealed cork wheels for shock absorption, and a polyurethane coating."],
             img=("img/eruca/final.jpg", "The Eruca Pod")),
    ],
    reflect=[],
    next=("alcove.html", "Alcove"),
    foot="ACAD-324 · Professor Wolter",
)

TABLE = dict(
    slug="alcove", name="Alcove", when="Spring 2026 · ACAD-445, Designing Products for Licensing",
    desc="a nesting coffee table for small first apartments: the smaller table slides out to expand the surface.",
    sub="A young adult who feels stuck about furnishing a first apartment needs to find one piece that works for work, living and hosting, but most furniture is cheap, bulky or single-use.",
    meta=[("Team", "Bodie Currier, Maya Parthasarathy, David Rodin, Jones Mays II and me"), ("Class", "ACAD-445, Designing Products for Licensing"), ("Built", "1/4 scale prototype")],
    links=[],
    back="/#classwork", backlabel="All class projects", nextlabel="Back to",
    nums=[("1/4", "scale prototype we built"), ("1 motion", "to expand the surface")],
    log=[
        dict(when="Purpose", tag="Research", title="Furniture That Grows With You",
             text=["Young adults furnishing their first apartment need furniture that's affordable and works for work, living and hosting, without taking over a small space. Most options make you pick: cheap but temporary, stylish but single-purpose, or functional but huge.",
                   "Our idea: furniture that works by day, lives by night, and hosts friends without crowding the room."]),
        dict(when="Research", tag="Research", title="Julie and Alex",
             text=["We built two personas from our interviews."],
             list=["<b>Julie</b>, a UX designer in a 500 sq ft downtown studio. Curated, warm neutrals, hosts small dinners. Hates visually heavy furniture and pieces that look too convertible.",
                   "<b>Alex</b>, a junior marketing associate with a roommate, working from home 3 to 4 days a week. Wants something that feels adult and affordable. Hates bulky, wobbly lift-top tables."]),
        dict(when="Research", tag="Research", title="The Gap",
             text=["We mapped what's out there twice: simple versus complex, and compact versus space-consuming. The corner we wanted, simple, multi-functional and compact, was basically empty."],
             pair=[("img/table/map1.jpg", "Competitor map: intuitive versus complex, single-purpose versus multi-functional", "Simple and multi-functional"), ("img/table/map2.jpg", "Competitor map: modern versus over-complicated, space-consuming versus compact", "Modern and compact")]),
        dict(when="Definition", tag="Design", title="How Might We",
             text=["How might we design a coffee table that intuitively transforms between experiences without overwhelming a small apartment?"],
             list=["Simple: one motion, no tools, stable for years", "Multi-functional: coffee table, work surface and dining", "Space-efficient: small when closed, never doubles its visual footprint", "Aesthetically pleasing: clean, neutral, premium"]),
        dict(when="Ideation", tag="Design", title="My Sketches",
             text=["Two of my concepts: a charcuterie tray with removable ceramic dishes that fit together like puzzle pieces, basically adult Lunchables, and Jenga seats, small cushions that stack into one corner piece and make cleaning up kind of fun."],
             img=("img/table/sketch-concepts.jpg", "My sketches for a charcuterie tray and Jenga seats")),
        dict(when="Ideation", tag="Design", title="Other Directions",
             text=["The team explored a rising top that separates private and social space, a game table with ottomans tucked underneath, and a boxy walnut nesting set with a glass top and an ottoman."],
             pair=[("img/table/gametable.jpg", "Game table with ottomans tucked underneath", "Game table"), ("img/table/render.jpg", "Walnut nesting set with glass top and ottoman", "Walnut nesting set")]),
        dict(when="Development", tag="Design", title="Waterfall Edges",
             text=["We landed on three nesting tables with soft waterfall edges. The smaller tables slide out from under the largest one to expand the surface. No hardware, no moving parts."],
             pair=[("img/table/waterfall.jpg", "Light wood nesting tables with waterfall edges", "Direction"), ("img/table/cad2.jpg", "CAD models of the nesting pieces", "CAD")]),
        dict(when="Development", tag="Tech", title="Making It",
             text=["We 3D printed molds, bent and glued the wood layers, clamped them, and sanded and stained the finished pieces."],
             img=("img/table/print.jpg", "3D printing the molds")),
        dict(when="Development", tag="Product", title="In the Shop",
             pair=[("img/table/build2.jpg", "Gluing and pressing the wood layers", "Pressing"), ("img/table/build3.jpg", "Clamping the bent pieces", "Clamping")]),
        dict(when="Final", tag="Product", title="Final Prototype",
             text=["Built at 1/4 scale. The smaller table slides out from beneath the larger one to instantly expand the surface: compact, intuitive and clean."],
             pair=[("img/table/assembled.jpg", "Raw assembled nesting tables", "Before finishing"), ("img/table/proto.jpg", "Finished stained prototype, closed and open", "Finished")]),
        dict(when="Final", tag="Product", title="Alcove at Home",
             img=("img/table/renders2.jpg", "Renderings of Alcove in a living room")),
    ],
    reflect=[],
    next=("/#work", "Selected Work"),
    foot="ACAD-445 · Designing Products for Licensing",
)

for p in (BART, FEE, BRANCH, HIND, BITE, HANG, ERUCA, TABLE):
    page(p)
