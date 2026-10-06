#!/usr/bin/env python3
"""TP4057 USB-C charger module (LX-LBES) Fritzing part generator. Units: 1/1000 in."""
import os, sys, zipfile
OUT = sys.argv[1]; NAME = "tp4057_usbc_charger"
MM = 39.3701
# board (top/component side, USB-C at top)
BX0, BX1 = 54, 546                 # 12.5 mm wide
BY0 = 174; BY1 = BY0 + 661         # 16.8 mm long
UX0, UX1 = 300 - 176, 300 + 176    # USB-C 8.94 mm wide, centred
UY0 = BY0 - 67                     # 1.7 mm overhang
PADY = 800
# connectors: (name, kind, x, y, description)
PINS = [
    ("OUT-", "male", 100, PADY, "Protected load output, negative"),
    ("BAT-", "male", 200, PADY, "Battery negative (B-)"),
    ("BAT+", "male", 400, PADY, "Battery positive (B+)"),
    ("OUT+", "male", 500, PADY, "Load output, positive"),
    ("IN-", "pad", BX0 + 41, BY0 + 262, "Power input negative (solder pad, alongside USB-C)"),
    ("IN+", "pad", BX1 - 41, BY0 + 262, "Power input positive, 5 V (solder pad, alongside USB-C)"),
]
FT = 'font-family="Droid Sans, sans-serif"'
def svg(w, h):
    return f'<svg xmlns="http://www.w3.org/2000/svg" version="1.2" baseProfile="tiny" width="{w/1000}in" height="{h/1000}in" viewBox="0 0 {w} {h}">'
def breadboard():
    p = [svg(600, 960), '<g id="breadboard">']
    p.append(f'<rect x="{BX0}" y="{BY0}" width="{BX1-BX0}" height="{BY1-BY0}" rx="6" fill="#16181d" stroke="#05060a" stroke-width="4"/>')
    p.append(f'<rect x="{UX0}" y="{UY0}" width="{UX1-UX0}" height="300" rx="26" fill="#c9cbd0" stroke="#7d8087" stroke-width="4"/>')
    p.append(f'<rect x="{UX0+30}" y="{UY0+20}" width="{UX1-UX0-60}" height="40" rx="18" fill="#4a4c52"/>')
    # SOP-8 chip, LEDs, caps (simplified)
    p.append('<rect x="225" y="470" width="150" height="70" rx="4" fill="#2b2d33" stroke="#555a63" stroke-width="3"/>')
    for k in range(4):
        p.append(f'<rect x="{235+k*36}" y="452" width="20" height="18" fill="#b9bcc4"/>')
        p.append(f'<rect x="{235+k*36}" y="540" width="20" height="18" fill="#b9bcc4"/>')
    p.append('<rect x="120" y="470" width="24" height="44" fill="#e8e4d8" stroke="#555" stroke-width="2"/>')
    p.append('<rect x="456" y="470" width="24" height="44" fill="#e8e4d8" stroke="#555" stroke-width="2"/>')
    p.append('<rect x="258" y="590" width="30" height="40" fill="#30c060" stroke="#106030" stroke-width="2"/>')
    p.append('<rect x="312" y="590" width="30" height="40" fill="#e03030" stroke="#701010" stroke-width="2"/>')
    for n, k, x, y, _ in PINS:
        lab = {"BAT+": "B+", "BAT-": "B-"}.get(n, n)
        if k == "male":
            p.append(f'<rect x="{x-34}" y="{y-34}" width="68" height="68" fill="#cfd2d8" stroke="#888b92" stroke-width="3"/>')
            p.append(f'<circle cx="{x}" cy="{y}" r="22" fill="#3a2a10"/>')
            p.append(f'<rect id="connector{PINS.index((n,k,x,y,_))}pin" x="{x-14}" y="{y-10}" width="28" height="140" fill="#d9ae2c" stroke="#8a6a10" stroke-width="3"/>')
            i = PINS.index((n, k, x, y, _))
            p.append(f'<rect id="connector{i}terminal" x="{x-5}" y="{y+120}" width="10" height="10" fill="none" stroke="none"/>')
            p.append(f'<text transform="translate({x+14},{y-50}) rotate(-90)" {FT} font-weight="bold" font-size="40" fill="#ffffff">{lab}</text>')
        else:
            i = PINS.index((n, k, x, y, _))
            p.append(f'<circle id="connector{i}pin" cx="{x}" cy="{y}" r="36" fill="#cfd2d8" stroke="#888b92" stroke-width="3"/>')
            p.append(f'<circle cx="{x}" cy="{y}" r="20" fill="#3a2a10"/>')
            p.append(f'<rect id="connector{i}terminal" x="{x-5}" y="{y-5}" width="10" height="10" fill="none" stroke="none"/>')
            if n == "IN-":
                p.append(f'<text x="{x+46}" y="{y+14}" {FT} font-weight="bold" font-size="40" fill="#ffffff">{n}</text>')
            else:
                p.append(f'<text x="{x-46}" y="{y+14}" {FT} font-weight="bold" font-size="40" fill="#ffffff" text-anchor="end">{n}</text>')
    p.append('</g></svg>'); return "\n".join(p)
def schematic():
    p = [svg(1100, 900), '<g id="schematic">']
    p.append('<rect x="300" y="200" width="500" height="600" fill="#ffffff" stroke="#000000" stroke-width="10"/>')
    p.append(f'<text x="550" y="470" {FT} font-size="56" fill="#000000" text-anchor="middle">TP4057</text>')
    p.append(f'<text x="550" y="515" {FT} font-size="36" fill="#000000" text-anchor="middle">USB-C Li-Ion</text>')
    p.append(f'<text x="550" y="555" {FT} font-size="36" fill="#000000" text-anchor="middle">charger module</text>')
    layout = {"IN+": ("L", 300), "IN-": ("L", 400), "BAT+": ("R", 300), "BAT-": ("R", 400), "OUT+": ("R", 600), "OUT-": ("R", 700)}
    for i, (n, k, *_r) in enumerate(PINS):
        side, y = layout[n]
        if side == "L":
            p.append(f'<line id="connector{i}pin" x1="100" y1="{y}" x2="300" y2="{y}" stroke="#000" stroke-width="10"/>')
            p.append(f'<rect id="connector{i}terminal" x="100" y="{y-5}" width="10" height="10" fill="none" stroke="none"/>')
            p.append(f'<text x="330" y="{y+18}" {FT} font-size="50" fill="#000">{n}</text>')
            p.append(f'<text x="125" y="{y-14}" {FT} font-size="36" fill="#000">{i+1}</text>')
        else:
            p.append(f'<line id="connector{i}pin" x1="800" y1="{y}" x2="1000" y2="{y}" stroke="#000" stroke-width="10"/>')
            p.append(f'<rect id="connector{i}terminal" x="990" y="{y-5}" width="10" height="10" fill="none" stroke="none"/>')
            p.append(f'<text x="770" y="{y+18}" {FT} font-size="50" fill="#000" text-anchor="end">{n}</text>')
            p.append(f'<text x="975" y="{y-14}" {FT} font-size="36" fill="#000" text-anchor="end">{i+1}</text>')
    p.append('</g></svg>'); return "\n".join(p)
def pcb():
    p = [svg(600, 900), '<g id="silkscreen">']
    p.append(f'<rect x="{BX0}" y="{BY0}" width="{BX1-BX0}" height="{BY1-BY0}" fill="none" stroke="#000" stroke-width="8"/>')
    p.append(f'<rect x="{UX0}" y="{UY0}" width="{UX1-UX0}" height="{BY0-UY0}" fill="none" stroke="#000" stroke-width="8"/>')
    for n, k, x, y, _ in PINS:
        lab = {"BAT+": "B+", "BAT-": "B-"}.get(n, n)
        if k == "male":
            p.append(f'<text transform="translate({x+12},{y-55}) rotate(-90)" font-family="Droid Sans, sans-serif" font-size="34" fill="#000">{lab}</text>')
        elif n == "IN-":
            p.append(f'<text x="{x+46}" y="{y+12}" font-family="Droid Sans, sans-serif" font-size="34" fill="#000">{n}</text>')
        else:
            p.append(f'<text x="{x-46}" y="{y+12}" font-family="Droid Sans, sans-serif" font-size="34" fill="#000" text-anchor="end">{n}</text>')
    p.append('</g><g id="copper1"><g id="copper0">')
    for i, (n, k, x, y, _) in enumerate(PINS):
        p.append(f'<circle id="connector{i}pin" cx="{x}" cy="{y}" r="30" fill="none" stroke="#F7BD13" stroke-width="20"/>')
    p.append('</g></g></svg>'); return "\n".join(p)
def icon():
    return (svg(400, 560) + '<g id="icon">\n<rect x="40" y="90" width="320" height="440" fill="#16181d"/>\n'
            '<rect x="100" y="30" width="200" height="190" rx="14" fill="#c9cbd0"/>\n<rect x="150" y="300" width="100" height="70" fill="#2b2d33"/>\n</g></svg>')
def fzp():
    o = ['<?xml version="1.0" encoding="UTF-8"?>', '<module fritzingVersion="0.9.3" moduleId="TP4057_USBC_Charger_LX-LBES_ModuleID">',
 '  <version>1</version>', '  <title>TP4057 USB-C Li-Ion Charger Module</title>', '  <label>U</label>', '  <date>2026-10-03</date>',
 '  <author>Markus</author>',
 '  <tags><tag>TP4057</tag><tag>charger</tag><tag>lithium</tag><tag>LiPo</tag><tag>18650</tag><tag>USB-C</tag><tag>LX-LBES</tag></tags>',
 '  <properties>', '    <property name="family">battery charger module</property>', '    <property name="variant">TP4057 USB-C</property>',
 '    <property name="chip">TP4057</property>', '    <property name="input voltage">5V</property>', '    <property name="charge current">1A</property>', '  </properties>',
 '  <description>TP4057 USB-C single-cell Li-Ion/LiPo (3.7 V, e.g. 18650) charging module, board marking LX-LBES. 5 V input via USB-C or IN+/IN- pads, 1 A charge current, B+/B- battery pads and OUT+/OUT- load pads.</description>',
 '  <views>',
 f'    <iconView><layers image="icon/{NAME}_icon.svg"><layer layerId="icon"/></layers></iconView>',
 f'    <breadboardView><layers image="breadboard/{NAME}_breadboard.svg"><layer layerId="breadboard"/></layers></breadboardView>',
 f'    <schematicView><layers image="schematic/{NAME}_schematic.svg"><layer layerId="schematic"/></layers></schematicView>',
 f'    <pcbView><layers image="pcb/{NAME}_pcb.svg"><layer layerId="copper0"/><layer layerId="silkscreen"/><layer layerId="copper1"/></layers></pcbView>',
 '  </views>', '  <connectors>']
    for i, (n, k, x, y, d) in enumerate(PINS):
        o += [f'    <connector id="connector{i}" name="{n}" type="{k}">', f'      <description>{d}</description>', '      <views>',
 f'        <breadboardView><p layer="breadboard" svgId="connector{i}pin" terminalId="connector{i}terminal"/></breadboardView>',
 f'        <schematicView><p layer="schematic" svgId="connector{i}pin" terminalId="connector{i}terminal"/></schematicView>',
 f'        <pcbView><p layer="copper0" svgId="connector{i}pin"/><p layer="copper1" svgId="connector{i}pin"/></pcbView>',
 '      </views>', '    </connector>']
    o += ['  </connectors>', '</module>']; return "\n".join(o)
files = {f"{NAME}.fzp": fzp(), f"breadboard/{NAME}_breadboard.svg": breadboard(), f"schematic/{NAME}_schematic.svg": schematic(),
         f"pcb/{NAME}_pcb.svg": pcb(), f"icon/{NAME}_icon.svg": icon()}
for d in ("breadboard", "schematic", "pcb", "icon"): os.makedirs(f"{OUT}/{d}", exist_ok=True)
for k, v in files.items(): open(f"{OUT}/{k}", "w").write(v + "\n")
with zipfile.ZipFile(f"{OUT}/{NAME}.fzpz", "w", zipfile.ZIP_DEFLATED) as z:
    for k in files: z.write(f"{OUT}/{k}", ("part." + k) if k.endswith(".fzp") else "svg." + k.replace("/", "."))
