"""Render a self-contained cinematic assessment demo with FFmpeg/Pillow.

This is a deterministic fallback render. Live mode is intended to hand the selected
storyboard to OpenMontage for richer generated media.
"""
from pathlib import Path
import math, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output'; OUT.mkdir(exist_ok=True)
W,H,FPS=1280,720,24
frames=48*FPS
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
bold='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

def text(draw, xy, s, size, fill=(235,240,245), anchor='la', f=font):
    try: ft=ImageFont.truetype(f,size)
    except: ft=ImageFont.load_default()
    draw.text(xy,s,font=ft,fill=fill,anchor=anchor)

def frame(t):
    im=Image.new('RGB',(W,H),(4,7,12)); d=ImageDraw.Draw(im)
    # cinematic vignette/scanlines
    phase=t/48
    # blue/green-ish market glow without branded assets
    glow=Image.new('RGBA',(W,H),(0,0,0,0)); gd=ImageDraw.Draw(glow)
    for r in range(600,40,-25):
        a=max(0,int(1.5*(600-r)))
        gd.ellipse((W//2-r,H//2-r,W//2+r,H//2+r),outline=(30,150,190,max(0,20-a//4)),width=2)
    im=Image.alpha_composite(im.convert('RGBA'),glow).convert('RGB'); d=ImageDraw.Draw(im)
    # moving grid
    for x in range(0,W,80): d.line((x,0,x,H),fill=(16,28,38),width=1)
    for y in range(0,H,60): d.line((0,y,W,y),fill=(16,28,38),width=1)
    # floating signal particles
    for i in range(90):
        x=(i*137 + int(t*55*(1+(i%5)/10)))%W; y=(i*71 + int(math.sin(t/2+i)*35)+H//3)%H
        r=1+(i%3); d.ellipse((x-r,y-r,x+r,y+r),fill=(70,160,185))
    # chart
    pts=[]
    for i in range(80):
        x=80+i*14
        y=470 - int(75*math.sin(i*.19+t*.6)-35*math.sin(i*.051+t*.2))
        pts.append((x,y))
    d.line(pts,fill=(90,210,175),width=4)
    # scene-specific visual storytelling
    if t<8:
        text(d,(W/2,100),'THE NOISE',56,(245,248,250),'ma',bold)
        for i in range(8):
            yy=170+i*52
            xx=90+int(math.sin(t*2+i)*40)
            label=['BUY','SELL','BREAKOUT','CRASH','BULLISH','BEARISH','FOMO','NOW'][i]
            text(d,(xx,yy),label,24,(230,90 if i%2 else 210,100),'la',bold)
        text(d,(W/2,650),'Every screen has an opinion.',30,(190,200,210),'ma')
    elif t<17:
        text(d,(W/2,105),'TOO MANY SIGNALS',44,(240,245,250),'ma',bold)
        cx,cy=W//2,350
        for i in range(24):
            a=i*math.tau/24+t*.5; r=110+35*math.sin(t+i)
            x=cx+math.cos(a)*r; y=cy+math.sin(a)*r*.65
            d.line((cx,cy,x,y),fill=(70,90,105),width=2); d.ellipse((x-8,y-8,x+8,y+8),fill=(220,80,90) if i%2 else (80,190,200))
    elif t<25:
        # convergence
        cx,cy=W//2,360
        for i in range(140):
            a=i*2.399+t*.15; start=1; r=300*(1-(t-17)/8)
            x=cx+math.cos(a)*r; y=cy+math.sin(a)*r*.55
            d.ellipse((x-3,y-3,x+3,y+3),fill=(120,210,225))
        text(d,(W/2,110),'WHAT IF THE NOISE AGREED?',42,(245,245,245),'ma',bold)
    elif t<36:
        # network and insight card
        cx,cy=W//2,350
        for i in range(60):
            a=i*2.399; r=180+70*math.sin(i*1.7+t)
            x=cx+math.cos(a)*r; y=cy+math.sin(a)*r*.55
            d.line((cx,cy,x,y),fill=(35,85,105),width=1); d.ellipse((x-4,y-4,x+4,y+4),fill=(95,210,190))
        d.rounded_rectangle((760,190,1160,520),radius=22,fill=(9,18,27),outline=(75,180,190),width=2)
        text(d,(800,230),'CROWDWISDOM',32,(235,245,245),'la',bold)
        text(d,(800,285),'16,564',50,(100,220,190),'la',bold)
        text(d,(800,345),'traders & investors',22,(190,205,215))
        text(d,(800,400),'ENTRY   TARGETS   STOPS',22,(225,230,235),'la',bold)
        d.line((800,445,1110,445),fill=(70,150,165),width=3)
        text(d,(800,475),'CONSENSUS + CONTEXT',18,(170,190,200))
    else:
        # calm final hero
        d.rectangle((120,130,1160,560),fill=(7,14,21),outline=(60,130,145),width=2)
        d.ellipse((500,175,780,455),outline=(80,180,185),width=3)
        text(d,(W/2,270),'CROWDWISDOM',52,(240,245,245),'ma',bold)
        text(d,(W/2,335),'See the signal beyond the noise.',30,(170,210,215),'ma')
        text(d,(W/2,420),'crowdwisdomtrading.com',24,(120,210,190),'ma')
        text(d,(W/2,640),'Informational & educational only. Trading involves significant risk.',18,(135,145,155),'ma')
    # vignette
    vign=Image.new('L',(W,H),0); vd=ImageDraw.Draw(vign); vd.ellipse((-200,-120,W+200,H+120),fill=255); vign=vign.filter(ImageFilter.GaussianBlur(120))
    dark=Image.new('RGB',(W,H),(0,0,0)); im=Image.composite(im,dark,Image.eval(vign,lambda p:255-p//3))
    return im

import sys
proc=subprocess.Popen(['ffmpeg','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-f','lavfi','-i','sine=frequency=48:sample_rate=48000:duration=48','-f','lavfi','-i','sine=frequency=96:sample_rate=48000:duration=48','-filter_complex','[1:a]volume=0.03[a1];[2:a]volume=0.012[a2];[a1][a2]amix=inputs=2:duration=first[a]','-map','0:v','-map','[a]','-c:v','libx264','-pix_fmt','yuv420p','-crf','20','-c:a','aac','-b:a','128k','-shortest',str(OUT/'crowdwisdom_demo_ad.mp4')],stdin=subprocess.PIPE)
for i in range(frames):
    proc.stdin.write(frame(i/FPS).tobytes())
proc.stdin.close(); proc.wait()
print(OUT/'crowdwisdom_demo_ad.mp4')
