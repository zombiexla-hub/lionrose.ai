import json, random, os
GREEN="#33ff9c"; SOFT="#8dffc7"; DIM="#1c6b48"; MUTED="#78a08d"; BG="#060a08"; PANEL="#0b110e"; WHITE="#eafff5"
W,H=1200,630
def mesh(seed):
    random.seed(seed)
    nodes=[(random.uniform(20,W-20),random.uniform(20,H-20)) for _ in range(26)]
    out=[]
    for i in range(len(nodes)):
        for j in range(i+1,len(nodes)):
            ax,ay=nodes[i]; bx,by=nodes[j]; d=((ax-bx)**2+(ay-by)**2)**0.5
            if d<210:
                al=round((1-d/210)*0.26,3)
                out.append(f'<line x1="{ax:.1f}" y1="{ay:.1f}" x2="{bx:.1f}" y2="{by:.1f}" stroke="rgba(51,255,156,{al})" stroke-width="1"/>')
    out+= [f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2" fill="rgba(51,255,156,0.5)"/>' for x,y in nodes]
    return "".join(out)
DEFS=f'''<defs>
<radialGradient id="pg" cx="30%" cy="42%" r="90%"><stop offset="0%" stop-color="{PANEL}" stop-opacity="0.25"/><stop offset="100%" stop-color="{BG}" stop-opacity="0.95"/></radialGradient>
<linearGradient id="beam" x1="0" y1="0" x2="1" y2="0"><stop offset="0%" stop-color="{GREEN}" stop-opacity="0"/><stop offset="50%" stop-color="{GREEN}" stop-opacity="0.05"/><stop offset="100%" stop-color="{GREEN}" stop-opacity="0"/></linearGradient>
</defs>'''
def esc(s): return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
def render(name, tagline, status, fname):
    # wrap long names on two lines if needed
    fs=64
    disp=name
    two=None
    if len(name)>18:
        # split at a space near middle
        words=name.split(" ")
        if len(words)>1:
            mid=len(name)//2; acc=0; idx=0
            for k,w in enumerate(words):
                acc+=len(w)+1
                if acc>=mid: idx=k+1; break
            two=(" ".join(words[:idx])," ".join(words[idx:])); fs=58
    beam=f'<rect x="{W*0.62}" y="0" width="160" height="{H}" fill="url(#beam)"/>'
    if two:
        title=f'<text x="72" y="292" font-family="Georgia,serif" font-size="{fs}" fill="{WHITE}">{esc(two[0])}</text><text x="72" y="{292+fs+8}" font-family="Georgia,serif" font-size="{fs}" fill="{WHITE}">{esc(two[1])}</text>'
        ty2=292+fs+8+52
    else:
        title=f'<text x="72" y="316" font-family="Georgia,serif" font-size="{fs}" fill="{WHITE}">{esc(disp)}</text>'
        ty2=316+52
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
{DEFS}
<rect width="{W}" height="{H}" fill="{BG}"/>
<rect width="{W}" height="{H}" fill="url(#pg)"/>
{beam}
<g>{mesh(hash(name)%9999)}</g>
<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" fill="none" stroke="rgba(120,255,190,0.14)"/>
<text x="72" y="86" font-family="ui-monospace,monospace" font-size="20" letter-spacing="6" fill="{GREEN}">L I O N R O S E</text>
<text x="72" y="150" font-family="ui-monospace,monospace" font-size="15" letter-spacing="5" fill="{MUTED}">// {esc(status)}</text>
{title}
<text x="72" y="{ty2}" font-family="ui-monospace,monospace" font-size="22" letter-spacing="1" fill="{SOFT}">{esc(tagline)}</text>
<text x="72" y="{H-56}" font-family="ui-monospace,monospace" font-size="18" letter-spacing="3" fill="{MUTED}">lionrose.ai</text>
</svg>'''
    open(f"/tmp/build/og/{fname}.svg","w").write(svg)

d=json.load(open("/tmp/build/products.json"))
for p in d["products"]:
    if p.get("has_detail"):
        render(p["name"], p["card_tagline"], "LIONROSE STUDIO // "+p["status"].upper(), "og-"+p["slug"])
render("Creative Solutions for Dynamic Times", "AI . Web . HR . Media . Production", "LIONROSE ENTERTAINMENT INC.", "og-default")
print("og svgs:", sorted(os.listdir("/tmp/build/og")))
