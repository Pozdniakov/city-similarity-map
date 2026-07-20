#!/usr/bin/env python3
"""Driver for the city-similarity map — build the page and screenshot it in
any interaction state, using the installed Google Chrome in headless mode.

The deliverable is a single self-contained interactive page (docs/index.html):
all data is inlined, so there are NO external fetches and file:// works — no
web server needed. Interaction state (layout / cutoff / pinned city) is applied
by injecting a tiny script into a temp copy of the page before screenshotting,
so we get reproducible "pinned Dubai at cutoff 0.65 on UMAP" shots without a
CDP/Node driver.

Because headless Chrome's `--screenshot` only captures the top viewport (it does
NOT honour scroll), `shot` captures the WHOLE page by default: it first measures
document height, then sizes the window to it. A pinned drawer / the scrollspy
rail are position:fixed, so in a full-page shot they render at full height down
the side — that's expected, not a bug. Pass --size WxH for a fixed top-anchored
viewport instead.

Run from the repo root (paths are relative to it).

  python3 .claude/skills/run-map-similarity/driver.py build
  python3 .claude/skills/run-map-similarity/driver.py shot out.png
  python3 .claude/skills/run-map-similarity/driver.py shot out.png \
      --layout UMAP --cutoff 0.65 --pin Dubai
  python3 .claude/skills/run-map-similarity/driver.py shot top.png --size 1400x1000
  python3 .claude/skills/run-map-similarity/driver.py dom     # post-JS DOM to stdout

For live click-driving (hover previews, keyboard, pixel-accurate scrolled views)
prefer the Claude Browser MCP against
`python3 -m http.server 8731 --directory docs`. This driver covers the
build + rendered-state screenshot + DOM-dump path that most edits to
combined_template.html / build_combined.py actually need.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

REPO = os.getcwd()
PAGE = os.path.join(REPO, "docs", "index.html")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def chrome_bin():
    if os.path.exists(CHROME):
        return CHROME
    for c in ("google-chrome", "chromium", "chromium-browser"):
        p = shutil.which(c)
        if p:
            return p
    sys.exit("Google Chrome not found — install it or edit CHROME in driver.py")


def py():
    v = os.path.join(REPO, ".venv", "bin", "python")
    return v if os.path.exists(v) else sys.executable


def build():
    # build_combined.py has a hardcoded absolute scratchpad path (SCRATCH=...)
    # and crashes with FileNotFoundError writing to it if that dir is absent.
    # Pre-create it so the build is reproducible on any machine.
    try:
        src = open(os.path.join(REPO, "build_combined.py"), encoding="utf-8").read()
        # SCRATCH may be a parenthesised group of adjacent string literals
        # split across lines, or a single literal — handle both, join fragments.
        m = re.search(r'SCRATCH\s*=\s*\((.*?)\)', src, re.S) or \
            re.search(r'SCRATCH\s*=\s*(["\'][^"\']*["\'])', src)
        if m:
            path = "".join(re.findall(r'["\']([^"\']*)["\']', m.group(1)))
            if path:
                os.makedirs(os.path.dirname(path), exist_ok=True)
    except OSError:
        pass
    r = subprocess.run([py(), "build_combined.py"], cwd=REPO)
    if r.returncode:
        sys.exit(r.returncode)
    print("built docs/index.html")


def _require_page():
    if not os.path.exists(PAGE):
        sys.exit("docs/index.html missing — run `driver.py build` first")


# Injected on load: apply requested UI state by driving the page's real handlers.
INJECT = """
<script>
(function(){
  function byText(t){
    return [...document.querySelectorAll('button')].find(function(e){
      return e.textContent.trim() === t; });
  }
  function apply(){
    var L = %LAYOUT%, C = %CUTOFF%, P = %PIN%;
    if (L){ var b = byText(L); if (b) b.click(); }
    if (C != null){ var s = document.getElementById('thr');
      if (s){ s.value = C; s.dispatchEvent(new Event('input',{bubbles:true})); } }
    if (P){ var pb = byText(P); if (pb) pb.click(); }
  }
  if (document.readyState !== 'loading') apply();
  else document.addEventListener('DOMContentLoaded', apply);
})();
</script>
"""


def _temp_page(extra_script):
    """Write docs/<tmp>.html = index.html + injected script; return its path.
    Lives inside docs/ so relative refs (there are none, but safe) resolve."""
    html = open(PAGE, encoding="utf-8").read()
    html = html.replace("</body>", extra_script + "</body>", 1)
    fd = tempfile.NamedTemporaryFile("w", suffix=".html", delete=False,
                                     dir=os.path.join(REPO, "docs"),
                                     encoding="utf-8")
    fd.write(html)
    fd.close()
    return fd.name


def _measure_height(inject):
    """Return document scrollHeight after applying `inject` (so a pinned drawer's
    height is reflected)."""
    stamp = ('<script>document.addEventListener("DOMContentLoaded",function(){'
             'setTimeout(function(){document.title="H="+'
             'document.documentElement.scrollHeight;},0);});</script>')
    p = _temp_page(inject + stamp)
    try:
        r = subprocess.run(
            [chrome_bin(), "--headless=new", "--disable-gpu",
             "--virtual-time-budget=3000", "--dump-dom", "file://" + p],
            capture_output=True, text=True)
        m = re.search(r"<title>H=(\d+)", r.stdout)
        return int(m.group(1)) if m else 9000
    finally:
        os.unlink(p)


def shot(args):
    _require_page()
    inject = (INJECT
              .replace("%LAYOUT%", json.dumps(args.layout))
              .replace("%CUTOFF%", json.dumps(args.cutoff))
              .replace("%PIN%", json.dumps(args.pin)))
    if args.size:
        w, h = args.size.lower().split("x")
    else:
        w = "1400"
        h = str(min(_measure_height(inject) + 40, 25000))  # cap runaway pages
    p = _temp_page(inject)
    try:
        out = os.path.abspath(args.out)
        cmd = [chrome_bin(), "--headless=new", "--disable-gpu",
               "--hide-scrollbars", "--force-device-scale-factor=1",
               "--virtual-time-budget=%d" % args.wait,
               "--window-size=%s,%s" % (w, h),
               "--screenshot=" + out, "file://" + p]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode or not os.path.exists(out):
            sys.exit("chrome failed:\n" + r.stderr[-2000:])
        print("wrote %s (%sx%s)" % (out, w, h))
    finally:
        os.unlink(p)


def dom(args):
    """Dump post-JS DOM to stdout (pipe to grep to assert on rendered content)."""
    _require_page()
    r = subprocess.run(
        [chrome_bin(), "--headless=new", "--disable-gpu",
         "--virtual-time-budget=3000", "--dump-dom", "file://" + PAGE],
        capture_output=True, text=True)
    sys.stdout.write(r.stdout)


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("build")
    s = sub.add_parser("shot")
    s.add_argument("out")
    s.add_argument("--layout", choices=["MDS", "PCA", "t-SNE", "UMAP"])
    s.add_argument("--cutoff", type=float)
    s.add_argument("--pin", help="exact city name, e.g. Dubai")
    s.add_argument("--size", help="fixed viewport WxH, e.g. 1400x1000; "
                                  "default = auto full-page height")
    s.add_argument("--wait", type=int, default=4000,
                   help="virtual-time-budget ms before capture")
    sub.add_parser("dom")
    a = ap.parse_args()
    {"build": lambda: build(), "shot": lambda: shot(a),
     "dom": lambda: dom(a)}[a.cmd]()


if __name__ == "__main__":
    main()
