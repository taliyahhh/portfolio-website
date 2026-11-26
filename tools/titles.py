"""Title Case every h1/h2/h3 and drop trailing periods. Usage: python3 tools/titles.py file.html ..."""
import re, sys

SMALL = {"a", "an", "the", "and", "but", "or", "for", "nor", "on", "at", "to", "by", "of", "in", "up", "as", "vs", "via", "with", "from", "into", "per"}


def tc_text(text, state):
    def fix(m):
        w = m.group(0)
        first = state["first"]; state["first"] = False
        core = w.lstrip("\"'(“")
        if not core or not core[0].isalpha():
            return w
        bare = core.rstrip(".,:;!?\"')”")
        if any(c.isupper() for c in bare[1:]) or bare in ("tj",):   # iOS, GitHub, tj
            return w
        if not first and core.lower() in SMALL:
            return w[: len(w) - len(core)] + core.lower()
        return w[: len(w) - len(core)] + core[0].upper() + core[1:]
    out = re.sub(r"[^\s]+", fix, text)
    if re.search(r"[.:!?]\s*$", text):
        state["first"] = True   # next sentence starts fresh
    return out


def title(inner):
    state = {"first": True}
    parts = re.split(r"(<[^>]+>)", inner)
    parts = [p if p.startswith("<") else tc_text(p, state) for p in parts]
    s = "".join(parts)
    # drop a trailing period (keep ? and !), even if it sits before closing tags
    s = re.sub(r"\.(\s*(?:</[^>]+>\s*)*)$", r"\1", s)
    # the last word is always capitalized ("Where It's At")
    s = re.sub(r"(?<![\w'$])([a-z])([a-z']*)([?!]?\s*(?:</[^>]+>\s*)*)$", lambda m: m.group(0) if m.group(1) + m.group(2) == "tj" else m.group(1).upper() + m.group(2) + m.group(3), s)
    return s


def run(path):
    s = open(path).read()
    head, sep, body = s.partition("<body")
    # skip <script> and <style> blocks
    chunks = re.split(r"(<script\b.*?</script>|<style\b.*?</style>)", body, flags=re.S)
    for i, c in enumerate(chunks):
        if c.startswith("<script") or c.startswith("<style"):
            continue
        c = re.sub(r"(<h([123])\b[^>]*>)(.*?)(</h\2>)", lambda m: m.group(1) + title(m.group(3)) + m.group(4), c, flags=re.S)
        c = re.sub(r'(<a class="wlink"[^>]*>)(.*?)(</a>)', lambda m: m.group(1) + title(m.group(2)) + m.group(3), c, flags=re.S)
        chunks[i] = re.sub(r'(<small>Next project</small><b>)(.*?)(</b>)', lambda m: m.group(1) + title(m.group(2)) + m.group(3), c, flags=re.S)
    open(path, "w").write(head + sep + "".join(chunks))


if __name__ == "__main__":
    for f in sys.argv[1:]:
        run(f)
        print("titled", f)
