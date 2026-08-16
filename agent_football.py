import json, os, sys, urllib.request

USER = "a18-n03"
TOKEN = os.environ.get("GITHUB_TOKEN", "")

W, H = 860, 340
SQ, GAP = 12, 2
COLS, ROWS = 53, 7
GRID_W = COLS * (SQ + GAP) - GAP
GRID_H = ROWS * (SQ + GAP) - GAP
X0 = (W - GRID_W) // 2
Y0 = (H - GRID_H) // 2

LEVELS = ["#1c1c1c", "#123f22", "#1a7a3a", "#2ec95c", "#00FF41"]

def fetch():
    if TOKEN:
        q = 'query{user(login:"%s"){contributionsCollection(from:"2025-08-16T00:00:00Z",to:"2026-08-16T00:00:00Z"){contributionCalendar{weeks{contributionDays{contributionCount color}}}}}}' % USER
        req = urllib.request.Request("https://api.github.com/graphql",
                                     data=json.dumps({"query": q}).encode(),
                                     headers={"Authorization": "Bearer " + TOKEN, "Content-Type": "application/json"})
        data = json.load(urllib.request.urlopen(req))
        weeks = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
    else:
        with open(sys.argv[1] if len(sys.argv) > 1 else "contrib.json", encoding="utf-8") as f:
            data = json.load(f)
        weeks = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
    grid = []
    for w in weeks:
        col = []
        for d in w["contributionDays"]:
            c = d["contributionCount"]
            col.append(4 if c >= 20 else 3 if c >= 10 else 2 if c >= 5 else 1 if c >= 1 else 0)
        while len(col) < ROWS:
            col.append(0)
        grid.append(col[:ROWS])
    return grid[:COLS]

def draw_pitch(grid):
    s = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" font-family="Courier New, monospace">' % (W, H)]
    s.append('<rect x="0" y="0" width="%d" height="%d" fill="#0D0D0D"/>' % (W, H))
    s.append('<rect x="%d" y="%d" width="%d" height="%d" fill="#11160f" stroke="#FFE900" stroke-opacity="0.35" stroke-width="1"/>' % (X0 - 16, Y0 - 16, GRID_W + 32, GRID_H + 32))
    for ci, col in enumerate(grid):
        for ri, lvl in enumerate(col):
            x = X0 + ci * (SQ + GAP)
            y = Y0 + ri * (SQ + GAP)
            s.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x, y, SQ, SQ, LEVELS[lvl]))
    return s

def draw_goal(s, x, y, h):
    s.append('<path d="M %d %d L %d %d M %d %d L %d %d M %d %d L %d %d" stroke="#FAF7F0" stroke-width="3" fill="none"/>' % (x, y, x, y + h, x, y + h, x + 6, y + h, x, y, x + 6, y))
    for i in range(4):
        s.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#FAF7F0" stroke-opacity="0.35" stroke-width="1"/>' % (x, y + (h // 4) * (i + 1), x + 6, y + (h // 4) * (i + 1)))

LOGOS = {
    "claude": '<path d="m4.7144 15.9555 4.7174-2.6471.079-.2307-.079-.1275h-.2307l-.7893-.0486-2.6956-.0729-2.3375-.0971-2.2646-.1214-.5707-.1215-.5343-.7042.0546-.3522.4797-.3218.686.0608 1.5179.1032 2.2767.1578 1.6514.0972 2.4468.255h.3886l.0546-.1579-.1336-.0971-.1032-.0972L6.973 9.8356l-2.55-1.6879-1.3356-.9714-.7225-.4918-.3643-.4614-.1578-1.0078.6557-.7225.8803.0607.2246.0607.8925.686 1.9064 1.4754 2.4893 1.8336.3643.3035.1457-.1032.0182-.0728-.164-.2733-1.3539-2.4467-1.445-2.4893-.6435-1.032-.17-.6194c-.0607-.255-.1032-.4674-.1032-.7285L6.287.1335 6.6997 0l.9957.1336.419.3642.6192 1.4147 1.0018 2.2282 1.5543 3.0296.4553.8985.2429.8318.091.255h.1579v-.1457l.1275-1.706.2368-2.0947.2307-2.6957.0789-.7589.3764-.9107.7468-.4918.5828.2793.4797.686-.0668.4433-.2853 1.8517-.5586 2.9021-.3643 1.9429h.2125l.2429-.2429.9835-1.3053 1.6514-2.0643.7286-.8196.85-.9046.5464-.4311h1.0321l.759 1.1293-.34 1.1657-1.0625 1.3478-.8804 1.1414-1.2628 1.7-.7893 1.36.0729.1093.1882-.0183 2.8535-.607 1.5421-.2794 1.8396-.3157.8318.3886.091.3946-.3278.8075-1.967.4857-2.3072.4614-3.4364.8136-.0425.0304.0486.0607 1.5482.1457.6618.0364h1.621l3.0175.2247.7892.522.4736.6376-.079.4857-1.2142.6193-1.6393-.3886-3.825-.9107-1.3113-.3279h-.1822v.1093l1.0929 1.0686 2.0035 1.8092 2.5075 2.3314.1275.5768-.3218.4554-.34-.0486-2.2039-1.6575-.85-.7468-1.9246-1.621h-.1275v.17l.4432.6496 2.3436 3.5214.1214 1.0807-.17.3521-.6071.2125-.6679-.1214-1.3721-1.9246L14.38 17.959l-1.1414-1.9428-.1397.079-.674 7.2552-.3156.3703-.7286.2793-.6071-.4614-.3218-.7468.3218-1.4753.3886-1.9246.3157-1.53.2853-1.9004.17-.6314-.0121-.0425-.1397.0182-1.4328 1.9672-2.1796 2.9446-1.7243 1.8456-.4128.164-.7164-.3704.0667-.6618.4008-.5889 2.386-3.0357 1.4389-1.882.929-1.0868-.0062-.1579h-.0546l-6.3385 4.1164-1.1293.1457-.4857-.4554.0608-.7467.2307-.2429 1.9064-1.3114Z" fill="#0D0D0D"/>',
    "codex": '<path d="M12 1.8 20.4 6.9v10.2L12 22.2 3.6 17.1V6.9Z" fill="none" stroke="#0D0D0D" stroke-width="1.8"/><path d="M12 6.6 16.2 9v6L12 17.4 7.8 15V9Z" fill="none" stroke="#0D0D0D" stroke-width="1.8"/>',
    "cursor": '<path d="M11.503.131 1.891 5.678a.84.84 0 0 0-.42.726v11.188c0 .3.162.575.42.724l9.609 5.55a1 1 0 0 0 .998 0l9.61-5.55a.84.84 0 0 0 .42-.724V6.404a.84.84 0 0 0-.42-.726L12.497.131a1.01 1.01 0 0 0-.996 0M2.657 6.338h18.55c.263 0 .43.287.297.515L12.23 22.918c-.062.107-.229.064-.229-.06V12.335a.59.59 0 0 0-.295-.51l-9.11-5.257c-.109-.063-.064-.23.061-.23" fill="#0D0D0D"/>',
    "gemini": '<path d="M11.04 19.32Q12 21.51 12 24q0-2.49.93-4.68.96-2.19 2.58-3.81t3.81-2.55Q21.51 12 24 12q-2.49 0-4.68-.93a12.3 12.3 0 0 1-3.81-2.58 12.3 12.3 0 0 1-2.58-3.81Q12 2.49 12 0q0 2.49-.96 4.68-.93 2.19-2.55 3.81a12.3 12.3 0 0 1-3.81 2.58Q2.49 12 0 12q2.49 0 4.68.96 2.19.93 3.81 2.55t2.55 3.81" fill="#0D0D0D"/>',
    "copilot": '<path d="M23.922 16.997C23.061 18.492 18.063 22.02 12 22.02 5.937 22.02.939 18.492.078 16.997A.641.641 0 0 1 0 16.741v-2.869a.883.883 0 0 1 .053-.22c.372-.935 1.347-2.292 2.605-2.656.167-.429.414-1.055.644-1.517a10.098 10.098 0 0 1-.052-1.086c0-1.331.282-2.499 1.132-3.368.397-.406.89-.717 1.474-.952C7.255 2.937 9.248 1.98 11.978 1.98c2.731 0 4.767.957 6.166 2.093.584.235 1.077.546 1.474.952.85.869 1.132 2.037 1.132 3.368 0 .368-.014.733-.052 1.086.23.462.477 1.088.644 1.517 1.258.364 2.233 1.721 2.605 2.656a.841.841 0 0 1 .053.22v2.869a.641.641 0 0 1-.078.256Zm-11.75-5.992h-.344a4.359 4.359 0 0 1-.355.508c-.77.947-1.918 1.492-3.508 1.492-1.725 0-2.989-.359-3.782-1.259a2.137 2.137 0 0 1-.085-.104L4 11.746v6.585c1.435.779 4.514 2.179 8 2.179 3.486 0 6.565-1.4 8-2.179v-6.585l-.098-.104s-.033.045-.085.104c-.793.9-2.057 1.259-3.782 1.259-1.59 0-2.738-.545-3.508-1.492a4.359 4.359 0 0 1-.355-.508Zm2.328 3.25c.549 0 1 .451 1 1v2c0 .549-.451 1-1 1-.549 0-1-.451-1-1v-2c0-.549.451-1 1-1Zm-5 0c.549 0 1 .451 1 1v2c0 .549-.451 1-1 1-.549 0-1-.451-1-1v-2c0-.549.451-1 1-1Zm3.313-6.185c.136 1.057.403 1.913.878 2.497.442.544 1.134.938 2.344.938 1.573 0 2.292-.337 2.657-.751.384-.435.558-1.15.558-2.361 0-1.14-.243-1.847-.705-2.319-.477-.488-1.319-.862-2.824-1.025-1.487-.161-2.192.138-2.533.529-.269.307-.437.808-.438 1.578v.021c0 .265.021.562.063.893Zm-1.626 0c.042-.331.063-.628.063-.894v-.02c-.001-.77-.169-1.271-.438-1.578-.341-.391-1.046-.69-2.533-.529-1.505.163-2.347.537-2.824 1.025-.462.472-.705 1.179-.705 2.319 0 1.211.175 1.926.558 2.361.365.414 1.084.751 2.657.751 1.21 0 1.902-.394 2.344-.938.475-.584.742-1.44.878-2.497Z" fill="#0D0D0D"/>',
    "opencode": '<path d="M22 24H2V0h20zM17 4.8H7v14.4h10z" fill="#0D0D0D"/>',
    "kilo": '<rect x="3" y="3" width="18" height="18" rx="4" fill="#0D0D0D"/><path d="M8 7v10M8 9l8 8M16 7l-8 8" stroke="#FFFFFF" stroke-width="2" fill="none" stroke-linecap="round"/>',
    "freebuf": '<path d="M12 3 20 5.8V12c0 5-3.3 8.4-8 10-4.7-1.6-8-5-8-10V5.8Z" fill="#0D0D0D"/><path d="M9.5 8v8M9.5 12h4M12 12v4" stroke="#FFFFFF" stroke-width="1.8" fill="none" stroke-linecap="round"/>',
}

def player(s, cx, cy, color, label, lx, ly, logo):
    s.append('<circle cx="%d" cy="%d" r="13" fill="%s" stroke="#0D0D0D" stroke-width="2"/>' % (cx, cy, color))
    s.append('<g transform="translate(%d,%d) scale(0.875)">%s</g>' % (cx - 12, cy - 12, LOGOS[logo]))
    s.append('<text x="%d" y="%d" text-anchor="middle" font-size="9" fill="#FAF7F0">%s</text>' % (lx, ly, label))

def main():
    grid = fetch()
    s = draw_pitch(grid)
    draw_goal(s, X0 - 14, Y0 + 20, GRID_H - 40)
    draw_goal(s, X0 + GRID_W + 8, Y0 + 20, GRID_H - 40)

    player(s, X0 + 60, Y0 + GRID_H // 2, "#D97757", "CLAUDE", X0 + 60, Y0 + GRID_H + 26, "claude")
    player(s, X0 + 120, Y0 + 30, "#00FF41", "CODEX", X0 + 120, Y0 + 16, "codex")
    player(s, X0 + 200, Y0 + GRID_H - 30, "#FAF7F0", "CURSOR", X0 + 200, Y0 + GRID_H + 26, "cursor")
    player(s, X0 + 290, Y0 + GRID_H // 2, "#9B59B6", "GEMINI", X0 + 290, Y0 - 24, "gemini")

    player(s, X0 + GRID_W - 60, Y0 + GRID_H // 2, "#FFE900", "OPENCODE", X0 + GRID_W - 60, Y0 + GRID_H + 26, "opencode")
    player(s, X0 + GRID_W - 130, Y0 + 30, "#3D5AFE", "KILO CODE", X0 + GRID_W - 130, Y0 + 16, "kilo")
    player(s, X0 + GRID_W - 210, Y0 + GRID_H - 30, "#FF3EA5", "FREEBUF", X0 + GRID_W - 210, Y0 + GRID_H + 26, "freebuf")
    player(s, X0 + GRID_W - 300, Y0 + GRID_H // 2, "#8b949e", "COPILOT", X0 + GRID_W - 300, Y0 - 24, "copilot")

    s.append('<text x="%d" y="%d" text-anchor="middle" font-size="11" fill="#FFE900">AI AGENTS FC</text>' % (X0 + 145, Y0 - 30))
    s.append('<text x="%d" y="%d" text-anchor="middle" font-size="11" fill="#FF3EA5">OPENCODE FC</text>' % (X0 + GRID_W - 145, Y0 - 30))

    s.append('<circle cx="0" cy="0" r="6" fill="#FAF7F0" stroke="#0D0D0D" stroke-width="1">')
    s.append('  <animateMotion dur="5s" repeatCount="indefinite" rotate="auto" path="M %d,%d C %d,%d %d,%d %d,%d C %d,%d %d,%d %d,%d C %d,%d %d,%d %d,%d"/>' % (
        X0 + GRID_W // 2, Y0 + GRID_H // 2,
        X0 + GRID_W // 2 + 80, Y0 + 30, X0 + GRID_W // 2 + 160, Y0 + GRID_H - 20, X0 + GRID_W // 2 + 260, Y0 + GRID_H // 2 + 10,
        X0 + GRID_W // 2 + 330, Y0 + 20, X0 + GRID_W // 2 + 380, Y0 + GRID_H - 10, X0 + GRID_W - 40, Y0 + GRID_H // 2 + 5,
        X0 + GRID_W // 2 + 420, Y0 + 40, X0 + GRID_W // 2 + 470, Y0 + GRID_H - 30, X0 + GRID_W - 30, Y0 + GRID_H // 2 + 2))
    s.append('</circle>')

    s.append('<text x="%d" y="%d" text-anchor="middle" font-size="34" font-weight="bold" fill="#00FF41">GOAL!<animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;0.75;0.82;0.94;1" dur="5s" repeatCount="indefinite"/></text>' % (X0 + GRID_W - 70, Y0 + GRID_H // 2 - 40))

    s.append('<text x="16" y="H-14" font-size="10" fill="#8b949e">pitch = your contribution graph // auto-updates daily</text>'.replace("H-14", str(H - 14)))
    s.append('</svg>')
    open("agent-football.svg", "w", encoding="utf-8").write("\n".join(s))
    print("agent-football.svg generated | weeks:", len(grid))

main()