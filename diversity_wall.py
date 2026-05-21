#!/usr/bin/env python3
"""
diversity_wall_vulva.py
Python port of the vulva diversity wall from The Uninformed Generation (guide.html).

Install:  pip install pycairo pillow
Run:      python diversity_wall_vulva.py
Output:   ./diversity_wall/vulva_00.png … vulva_25.png
          ./diversity_wall/montage.png
"""

import math, random, os
import cairo

OUTPUT_DIR = "diversity_wall"
os.makedirs(OUTPUT_DIR, exist_ok=True)

NORMAL_W,  NORMAL_H  = 220, 270
SPECIAL_W, SPECIAL_H = 440, 540

# ── SKIN TONE PALETTE ──────────────────────────────────────────────────────────
SKIN_TONES = [
    {'skin':'#f5d5b8','mid':'#e4bb98','shadow':'#c48858','deep':'#9a6038','inner':'#e0a880','hair':'#3a1e08','label':'Very light'},
    {'skin':'#e8b896','mid':'#d49a78','shadow':'#b07040','deep':'#845030','inner':'#cc8858','hair':'#28150a','label':'Light'},
    {'skin':'#d4a070','mid':'#bc8450','shadow':'#966030','deep':'#7a4820','inner':'#b87848','hair':'#1e0e06','label':'Light-medium'},
    {'skin':'#c08050','mid':'#a46438','shadow':'#804020','deep':'#602808','inner':'#a06038','hair':'#130a04','label':'Medium'},
    {'skin':'#a06040','mid':'#884830','shadow':'#633018','deep':'#441808','inner':'#865030','hair':'#0e0602','label':'Medium-dark'},
    {'skin':'#7a4020','mid':'#622c10','shadow':'#481808','deep':'#2e0e04','inner':'#663018','hair':'#070402','label':'Dark'},
    {'skin':'#5a2808','mid':'#441808','shadow':'#301004','deep':'#1e0800','inner':'#4a1e10','hair':'#040201','label':'Very dark'},
    {'skin':'#381408','mid':'#280e06','shadow':'#1c0a04','deep':'#100600','inner':'#301008','hair':'#020101','label':'Deep'},
]

# ── VARIATIONS DATA ────────────────────────────────────────────────────────────
VULVA_VARIATIONS = [
    {'tone':0,'iS':0,'asym':0,'hairStyle':0,'oS':2,'hood':1,'gV':0.2,'ruf':0,   'desc':'Fully contained · very light · bare'},
    {'tone':0,'iS':1,'asym':0,'hairStyle':1,'oS':2,'hood':2,'gV':0.4,'ruf':0.3, 'desc':'Small inner labia · light · sparse'},
    {'tone':1,'iS':2,'asym':0,'hairStyle':2,'oS':2,'hood':2,'gV':0.5,'ruf':0.7, 'desc':'Medium inner labia · light · natural'},
    {'tone':1,'iS':3,'asym':0,'hairStyle':0,'oS':2,'hood':2,'gV':0.6,'ruf':1.1, 'desc':'Prominent inner labia · light · bare'},
    {'tone':1,'iS':4,'asym':0,'hairStyle':5,'oS':2,'hood':3,'gV':0.7,'ruf':2.2, 'desc':'Very prominent · ruffled · curly dense'},
    {'tone':2,'iS':0,'asym':0,'hairStyle':4,'oS':3,'hood':2,'gV':0.4,'ruf':0,   'desc':'Contained · medium · landing strip · full outer'},
    {'tone':2,'iS':2,'asym':1,'hairStyle':2,'oS':3,'hood':2,'gV':0.4,'ruf':0.8, 'desc':'Asymmetric · medium · natural · full outer'},
    {'tone':2,'iS':4,'asym':0,'hairStyle':3,'oS':2,'hood':2,'gV':0.5,'ruf':1.6, 'desc':'Very prominent · med · trimmed triangle'},
    {'tone':3,'iS':0,'asym':0,'hairStyle':2,'oS':1,'hood':1,'gV':0.3,'ruf':0,   'desc':'Contained · med-dark · natural · slim outer'},
    {'tone':3,'iS':1,'asym':0,'hairStyle':3,'oS':2,'hood':1,'gV':0.2,'ruf':0.3, 'desc':'Small inner · med-dark · trimmed · small hood'},
    {'tone':3,'iS':3,'asym':1,'hairStyle':5,'oS':2,'hood':3,'gV':0.8,'ruf':1.3, 'desc':'Prominent · asymmetric · large hood · curly'},
    {'tone':4,'iS':0,'asym':0,'hairStyle':0,'oS':2,'hood':2,'gV':0.5,'ruf':0,   'desc':'Contained · med-dark · bare'},
    {'tone':4,'iS':2,'asym':0,'hairStyle':1,'oS':3,'hood':2,'gV':0.4,'ruf':0.7, 'desc':'Medium · med-dark · sparse · full outer'},
    {'tone':4,'iS':4,'asym':1,'hairStyle':2,'oS':3,'hood':1,'gV':0.2,'ruf':2.1, 'desc':'Very prominent · asymmetric · full outer'},
    {'tone':5,'iS':1,'asym':0,'hairStyle':0,'oS':2,'hood':2,'gV':0.5,'ruf':0.2, 'desc':'Small inner · dark · bare'},
    {'tone':5,'iS':3,'asym':0,'hairStyle':2,'oS':2,'hood':2,'gV':0.6,'ruf':1.4, 'desc':'Prominent · dark · natural'},
    {'tone':5,'iS':4,'asym':1,'hairStyle':0,'oS':2,'hood':3,'gV':0.9,'ruf':2.4, 'desc':'Very prominent · asymmetric · dark · bare'},
    {'tone':6,'iS':0,'asym':0,'hairStyle':4,'oS':2,'hood':2,'gV':0.4,'ruf':0,   'desc':'Contained · very dark · landing strip'},
    {'tone':6,'iS':2,'asym':0,'hairStyle':5,'oS':1,'hood':2,'gV':0.5,'ruf':1.0, 'desc':'Medium · very dark · curly · slim outer'},
    {'tone':6,'iS':3,'asym':0,'hairStyle':0,'oS':2,'hood':1,'gV':0.3,'ruf':1.5, 'desc':'Prominent · very dark · bare · small hood'},
    {'tone':7,'iS':0,'asym':0,'hairStyle':2,'oS':2,'hood':2,'gV':0.4,'ruf':0,   'desc':'Contained · deep · natural'},
    {'tone':7,'iS':2,'asym':0,'hairStyle':0,'oS':2,'hood':2,'gV':0.5,'ruf':0.9, 'desc':'Medium · deep · bare'},
    {'tone':7,'iS':3,'asym':0,'hairStyle':2,'oS':3,'hood':2,'gV':0.5,'ruf':1.2, 'desc':'Prominent · deep · natural · full outer'},
    {'tone':0,'iS':3,'asym':0,'hairStyle':0,'oS':1,'hood':3,'gV':0.95,'ruf':1.9,'desc':'Prominent · light · bare · visible glans'},
    {'tone':5,'iS':4,'asym':0,'hairStyle':6,'oS':2,'hood':2,'gV':0.4,'ruf':1.6,
     'special':True,'reclined':True,'asymIS':1,'asymRufScale':0.12,
     'desc':'One side small, one large · dark · full bush',
     'note':"Asymmetric inner labia · entirely normal · more common than you've been told"},
    {'tone':5,'iS':3,'asym':0,'hairStyle':6,'oS':3,'hood':1,'gV':0.99,'ruf':1.0,
     'innerTone':6,'special':True,'reclined':True,'clitPenis':True,
     'desc':'Macroclitoris · always visible · very dark · full bush',
     'note':'Large clitoris · entirely normal · part of natural anatomical variation'},
]

# ── COLOR HELPERS ──────────────────────────────────────────────────────────────
def parse_rgba(c):
    """CSS color string → (r,g,b,a) floats 0–1."""
    c = c.strip()
    if c.startswith('#'):
        h = c[1:]
        r=int(h[0:2],16)/255; g=int(h[2:4],16)/255; b=int(h[4:6],16)/255
        a=int(h[6:8],16)/255 if len(h)>=8 else 1.0
        return r,g,b,a
    if c.startswith('rgba('):
        p=c[5:-1].split(','); return float(p[0])/255,float(p[1])/255,float(p[2])/255,float(p[3])
    if c.startswith('rgb('):
        p=c[4:-1].split(','); return float(p[0])/255,float(p[1])/255,float(p[2])/255,1.0
    return 0,0,0,1

def add_stop(g, pos, c):
    r,gv,b,a = parse_rgba(c); g.add_color_stop_rgba(pos,r,gv,b,a)

def lighten_hex(h, t):
    """Return hex string mixing colour h toward white by t."""
    r,g,b,_ = parse_rgba(h)
    r2=r+(1-r)*t; g2=g+(1-g)*t; b2=b+(1-b)*t
    return '#{:02x}{:02x}{:02x}'.format(int(r2*255),int(g2*255),int(b2*255))

# ── CANVAS CONTEXT WRAPPER ─────────────────────────────────────────────────────
class Ctx:
    """cairo.Context wrapper with HTML5 Canvas 2D API."""
    def __init__(self, cr):
        self.cr=cr; self.globalAlpha=1.0
        self.fillStyle=None; self.strokeStyle=None
        self.lineWidth=1.0; self.lineCap=cairo.LINE_CAP_BUTT
        self._stack=[]

    def save(self):
        self.cr.save()
        self._stack.append((self.globalAlpha,self.fillStyle,self.strokeStyle,
                            self.lineWidth,self.lineCap))

    def restore(self):
        self.cr.restore()
        if self._stack:
            (self.globalAlpha,self.fillStyle,self.strokeStyle,
             self.lineWidth,self.lineCap) = self._stack.pop()

    def beginPath(self): self.cr.new_path()
    def moveTo(self,x,y): self.cr.move_to(x,y)
    def lineTo(self,x,y): self.cr.line_to(x,y)
    def closePath(self): self.cr.close_path()

    def bezierCurveTo(self,cp1x,cp1y,cp2x,cp2y,x,y):
        self.cr.curve_to(cp1x,cp1y,cp2x,cp2y,x,y)

    def quadraticCurveTo(self,cpx,cpy,x,y):
        x0,y0=self.cr.get_current_point()
        self.cr.curve_to(x0+2/3*(cpx-x0),y0+2/3*(cpy-y0),
                         x+2/3*(cpx-x),  y+2/3*(cpy-y), x,y)

    def ellipse(self,cx,cy,rx,ry,rot=0.0,a0=0.0,a1=2*math.pi):
        self.cr.save()
        self.cr.translate(cx,cy); self.cr.rotate(rot); self.cr.scale(rx,ry)
        self.cr.arc(0,0,1,a0,a1)
        self.cr.restore()

    def arc(self,cx,cy,r,a0,a1): self.cr.arc(cx,cy,r,a0,a1)

    def _fill_op(self,style,alpha,preserve=False):
        if isinstance(style,str):
            r,g,b,a=parse_rgba(style); self.cr.set_source_rgba(r,g,b,a*alpha)
            self.cr.fill_preserve() if preserve else self.cr.fill()
        elif style is not None:
            if alpha>=0.999:
                self.cr.set_source(style)
                self.cr.fill_preserve() if preserve else self.cr.fill()
            else:
                self.cr.push_group(); self.cr.set_source(style)
                self.cr.fill_preserve() if preserve else self.cr.fill()
                pat=self.cr.pop_group(); self.cr.set_source(pat)
                self.cr.paint_with_alpha(alpha)

    def fill(self):          self._fill_op(self.fillStyle,self.globalAlpha)
    def fill_preserve(self): self._fill_op(self.fillStyle,self.globalAlpha,True)

    def stroke(self):
        self.cr.set_line_width(self.lineWidth); self.cr.set_line_cap(self.lineCap)
        style=self.strokeStyle; alpha=self.globalAlpha
        if isinstance(style,str):
            r,g,b,a=parse_rgba(style); self.cr.set_source_rgba(r,g,b,a*alpha)
            self.cr.stroke()
        elif style is not None:
            if alpha>=0.999:
                self.cr.set_source(style); self.cr.stroke()
            else:
                self.cr.push_group(); self.cr.set_source(style); self.cr.stroke()
                pat=self.cr.pop_group(); self.cr.set_source(pat)
                self.cr.paint_with_alpha(alpha)

    def fillRect(self,x,y,w,h):
        self.cr.rectangle(x,y,w,h); self.fill()

    def clearRect(self,x,y,w,h):
        self.cr.save(); self.cr.set_operator(cairo.OPERATOR_CLEAR)
        self.cr.rectangle(x,y,w,h); self.cr.fill(); self.cr.restore()

    def createRadialGradient(self,x0,y0,r0,x1,y1,r1):
        return cairo.RadialGradient(x0,y0,r0,x1,y1,r1)
    def createLinearGradient(self,x0,y0,x1,y1):
        return cairo.LinearGradient(x0,y0,x1,y1)

# ── HAIR ───────────────────────────────────────────────────────────────────────
def drawHairByStyle(ctx, cx, topY, width, style, hairColor):
    if style == 0: return
    ctx.save(); ctx.strokeStyle = hairColor
    r = lambda a,b: a + random.random()*(b-a)
    lw = 0.65 if style==5 else 0.85

    def drawS(sx,sy,length,ang,curl,alpha):
        ctx.globalAlpha=alpha; ctx.lineWidth=lw
        ex=sx+math.cos(ang)*length; ey=sy+math.sin(ang)*length
        cpx=sx+math.cos(ang+0.45)*length*0.5+curl
        cpy=sy+math.sin(ang+0.45)*length*0.5
        ctx.beginPath(); ctx.moveTo(sx,sy); ctx.quadraticCurveTo(cpx,cpy,ex,ey); ctx.stroke()

    if style==1:
        for _ in range(24):
            drawS(cx+r(-width*.42,width*.42),topY+r(2,20),r(5,10),-math.pi/2+r(-.8,.8),r(-4,4),r(.5,.8))
    elif style==2:
        for _ in range(78):
            drawS(cx+r(-width*.56,width*.56),topY+r(-1,28),r(6,14),-math.pi/2+r(-1,1),r(-5,5),r(.6,.9))
    elif style==3:
        for _ in range(54):
            sy=topY+r(0,25); mW=width*.5*(1-(sy-topY)/28)
            drawS(cx+r(-mW,mW),sy,r(5,11),-math.pi/2+r(-.7,.7),r(-3,3),r(.65,.9))
    elif style==4:
        for _ in range(50):
            drawS(cx+r(-width*.17,width*.17),topY+r(-2,28),r(6,12),-math.pi/2+r(-.5,.5),r(-3,3),r(.65,.9))
    elif style==5:
        for _ in range(95):
            drawS(cx+r(-width*.62,width*.62),topY+r(-3,26),r(4,9),r(0,math.pi*2),r(-8,8),r(.55,.85))
    elif style==6:
        for _ in range(170):
            sy=topY+r(-12,44); frac=max(0,(sy-topY+12)/56); maxX=width*(0.82-frac*0.28)
            drawS(cx+r(-maxX,maxX),sy,r(5,15),-math.pi/2+r(-1.5,1.5),r(-8,8),r(.52,.90))

    ctx.globalAlpha=1; ctx.restore()

# ── DRAW VULVA (frontal, 220×270) ─────────────────────────────────────────────
def drawVulva(ctx, v, W, H):
    st  = SKIN_TONES[v['tone']]
    ist = SKIN_TONES[v.get('innerTone', v['tone'])]
    ctx.clearRect(0,0,W,H)
    cx=W/2; top=20; bot=H-26; totalH=bot-top; midY=top+totalH*0.43
    oF=v.get('oS',2); outerBulge=16+oF*9
    iS=v.get('iS',0); asym=v.get('asym',0); ruf=v.get('ruf',0)
    hs=v.get('hairStyle',v.get('hair',0)); hood=v.get('hood',2); gVis=v.get('gV',0.4)

    # 0 — warm background
    bgG=ctx.createRadialGradient(W*.42,H*.42,8, W*.5,H*.48, H*.72)
    add_stop(bgG,0,'#fdf4ec'); add_stop(bgG,0.6,'#faeae0'); add_stop(bgG,1,'#f5dece')
    ctx.fillStyle=bgG; ctx.fillRect(0,0,W,H)
    glowG=ctx.createRadialGradient(W*.5,H*.44,12, W*.5,H*.44, H*.48)
    add_stop(glowG,0,'rgba(255,210,170,0.20)'); add_stop(glowG,1,'rgba(255,210,170,0)')
    ctx.fillStyle=glowG; ctx.fillRect(0,0,W,H)

    # 1 — depth shadow
    dG=ctx.createRadialGradient(cx,midY,4, cx,midY, outerBulge*1.35)
    add_stop(dG,0,'rgba(0,0,0,0.22)'); add_stop(dG,0.55,'rgba(0,0,0,0.08)'); add_stop(dG,1,'rgba(0,0,0,0)')
    ctx.fillStyle=dG; ctx.beginPath(); ctx.ellipse(cx,midY,outerBulge*1.35,totalH*0.58); ctx.fill()

    # 2 — mons pubis
    mG=ctx.createRadialGradient(cx-5,top+5,5, cx,top+17,48)
    add_stop(mG,0,st['mid']); add_stop(mG,0.55,st['skin']); add_stop(mG,1,st['shadow'])
    ctx.fillStyle=mG
    ctx.beginPath(); ctx.moveTo(cx-outerBulge-7,top+25)
    ctx.bezierCurveTo(cx-outerBulge-5,top-5, cx+outerBulge+5,top-5, cx+outerBulge+7,top+25)
    ctx.bezierCurveTo(cx+outerBulge*.65,top+11, cx-outerBulge*.65,top+11, cx-outerBulge-7,top+25)
    ctx.fill()
    monsHL=ctx.createRadialGradient(cx-4,top+8,2, cx,top+16,outerBulge*0.75)
    add_stop(monsHL,0,'rgba(255,255,255,0.16)'); add_stop(monsHL,1,'rgba(255,255,255,0)')
    ctx.fillStyle=monsHL; ctx.globalAlpha=0.7
    ctx.beginPath(); ctx.ellipse(cx,top+16,outerBulge*0.75,22); ctx.fill(); ctx.globalAlpha=1

    # 3 — pubic hair
    drawHairByStyle(ctx,cx,top+3,outerBulge*1.7,hs,st['hair'])

    # 4 — labia majora
    def drawMajora(side):
        s=side; outerX=cx+s*outerBulge; innerX=cx+s*(7+oF*3)
        g=ctx.createRadialGradient(cx+s*outerBulge*.38,midY-20,3, cx+s*outerBulge*.52,midY+2,outerBulge*1.15)
        add_stop(g,0,st['mid']); add_stop(g,0.28,st['skin'])
        add_stop(g,0.65,st['shadow']); add_stop(g,0.88,st['deep']); add_stop(g,1,'#0d0604')
        ctx.fillStyle=g
        ctx.beginPath(); ctx.moveTo(cx,top+20)
        ctx.bezierCurveTo(cx+s*14,top+13, outerX-s*2,top+38, outerX,midY)
        ctx.bezierCurveTo(outerX,midY+33, cx+s*16,bot-20, cx,bot)
        ctx.bezierCurveTo(innerX-s*2,bot-11, innerX,midY+25, innerX,midY)
        ctx.bezierCurveTo(innerX,midY-29, cx+s*10,top+24, cx,top+20)
        ctx.closePath(); ctx.fill()
        hG=ctx.createLinearGradient(cx,top+20, cx+s*outerBulge*.6,top+52)
        add_stop(hG,0,'rgba(255,255,255,0.20)'); add_stop(hG,1,'rgba(255,255,255,0)')
        ctx.fillStyle=hG; ctx.globalAlpha=0.45
        ctx.beginPath(); ctx.moveTo(cx,top+20)
        ctx.bezierCurveTo(cx+s*14,top+13, outerX-s*2,top+38, outerX,midY-10)
        ctx.bezierCurveTo(cx+s*outerBulge*.7,midY-18, cx+s*10,top+28, cx,top+20)
        ctx.fill(); ctx.globalAlpha=1
        ctx.save(); ctx.strokeStyle=st['deep']; ctx.lineWidth=1.5; ctx.globalAlpha=0.20
        ctx.beginPath(); ctx.moveTo(cx+s*4,top+25)
        ctx.bezierCurveTo(innerX,top+37, innerX+s,midY, innerX,bot-24)
        ctx.stroke(); ctx.globalAlpha=1; ctx.restore()
    drawMajora(-1); drawMajora(1)

    # 5 — vestibule
    vW=10+oF*2.4
    vG=ctx.createLinearGradient(cx,top+24, cx,bot-16)
    add_stop(vG,0,ist['shadow']+'bb'); add_stop(vG,0.48,ist['inner']+'cc'); add_stop(vG,1,ist['deep']+'77')
    ctx.fillStyle=vG
    ctx.beginPath(); ctx.moveTo(cx,top+23)
    ctx.bezierCurveTo(cx-vW,top+35, cx-vW,bot-30, cx,bot-14)
    ctx.bezierCurveTo(cx+vW,bot-30, cx+vW,top+35, cx,top+23); ctx.fill()

    # 6 — labia minora
    iSpreads=[0,6,10,14,18]; iBotFrac=[0,0.55,0.68,0.80,0.89]
    def drawMinora(side, sizeScale):
        s=side; spread=iSpreads[min(iS,4)]*sizeScale
        if spread<1: return
        tA=top+23; bA=top+totalH*iBotFrac[min(iS,4)]; steps=38
        ctx.beginPath(); ctx.moveTo(cx,tA)
        for i in range(1,steps+1):
            t=i/steps; arc=math.sin(t*math.pi*0.88); bx=cx+s*spread*arc; by=tA+(bA-tA)*t
            wave=math.sin(t*math.pi*(3+ruf*1.6))*ruf*4.2 if ruf>0 else 0
            ctx.lineTo(bx+wave*(s*0.28), by+wave*0.36)
        tipX=cx+s*spread*0.70; tipY=bA+5
        ctx.bezierCurveTo(tipX+s*1.5,tipY+3, cx+s*1.5,tipY+2, cx,bA)
        for i in range(steps,-1,-1):
            t=i/steps; bx=cx+s*spread*0.18*math.sin(t*math.pi); by=tA+(bA-tA)*t
            wave=math.sin(t*math.pi*2.2+0.8)*ruf*2.0 if ruf>0 else 0
            ctx.lineTo(bx, by+wave*0.12)
        ctx.closePath()
        mG2=ctx.createLinearGradient(cx+s*spread*0.5,tA, cx+s*spread*0.5,bA)
        add_stop(mG2,0,ist['shadow']); add_stop(mG2,0.22,ist['inner'])
        add_stop(mG2,0.60,ist['deep']); add_stop(mG2,1,'#1a0808')
        ctx.fillStyle=mG2; ctx.fill()
        ctx.save(); ctx.strokeStyle=ist['deep']; ctx.lineWidth=0.9; ctx.globalAlpha=0.42
        ctx.beginPath(); ctx.moveTo(cx,tA)
        for i in range(1,steps+1):
            t=i/steps; arc=math.sin(t*math.pi*0.88); bx=cx+s*spread*arc; by=tA+(bA-tA)*t
            wave=math.sin(t*math.pi*(3+ruf*1.6))*ruf*4.2 if ruf>0 else 0
            ctx.lineTo(bx+wave*(s*0.28), by+wave*0.36)
        ctx.stroke(); ctx.globalAlpha=1; ctx.restore()
        # catch-light
        ctx.save(); ctx.strokeStyle='rgba(255,255,255,0.14)'; ctx.lineWidth=1.1; ctx.globalAlpha=0.65
        ctx.beginPath(); ctx.moveTo(cx+s*1.5,tA+8)
        for i in range(1,15):
            t=i/14; wave=math.sin(t*math.pi*(3+ruf))*ruf*3.0 if ruf>0 else 0
            arc=math.sin(t*math.pi*0.88)
            ctx.lineTo(cx+s*spread*0.72*arc+wave*s*0.22, tA+(bA-tA)*t*0.65+wave*0.28)
        ctx.stroke(); ctx.globalAlpha=1; ctx.restore()
    drawMinora(-1, 1+asym*0.7); drawMinora(1, 1)

    # 7 — clitoral complex
    hoodW=4.5+hood*2.6; hoodH=6+hood*3.2; hoodY=top+15
    hG=ctx.createRadialGradient(cx-2.5,hoodY,1, cx,hoodY+5,hoodH)
    add_stop(hG,0,st['mid']); add_stop(hG,0.5,st['skin']); add_stop(hG,1,st['inner'])
    ctx.fillStyle=hG
    ctx.beginPath(); ctx.moveTo(cx-hoodW,hoodY+hoodH)
    ctx.bezierCurveTo(cx-hoodW-1,hoodY-4, cx+hoodW+1,hoodY-4, cx+hoodW,hoodY+hoodH)
    ctx.bezierCurveTo(cx+hoodW*.5,hoodY+hoodH+6, cx-hoodW*.5,hoodY+hoodH+6, cx-hoodW,hoodY+hoodH)
    ctx.fill()
    ctx.save(); ctx.strokeStyle=st['shadow']; ctx.lineWidth=1; ctx.globalAlpha=0.17
    ctx.beginPath(); ctx.moveTo(cx-hoodW*.6,hoodY+2)
    ctx.bezierCurveTo(cx-hoodW*.4,hoodY-2, cx+hoodW*.4,hoodY-2, cx+hoodW*.6,hoodY+2)
    ctx.stroke(); ctx.globalAlpha=1; ctx.restore()
    ctx.save(); ctx.fillStyle=st['deep']; ctx.globalAlpha=0.42+gVis*0.48
    ctx.beginPath(); ctx.ellipse(cx,hoodY+1,hoodW*.48,hoodH*.36); ctx.fill(); ctx.globalAlpha=1; ctx.restore()
    ctx.save(); ctx.fillStyle='rgba(255,255,255,0.18)'
    ctx.beginPath(); ctx.ellipse(cx-hoodW*.28,hoodY-1,hoodW*.2,hoodH*.18,-0.3); ctx.fill(); ctx.restore()
    ctx.save(); ctx.strokeStyle=st['shadow']; ctx.lineWidth=0.8; ctx.globalAlpha=0.26
    ctx.beginPath(); ctx.moveTo(cx-hoodW+1,hoodY+hoodH+2)
    ctx.quadraticCurveTo(cx,hoodY+hoodH+7, cx+hoodW-1,hoodY+hoodH+2)
    ctx.stroke(); ctx.globalAlpha=1; ctx.restore()

    # 8 — urethral opening
    ctx.save(); ctx.fillStyle=st['deep']; ctx.globalAlpha=0.35
    ctx.beginPath(); ctx.ellipse(cx,top+37,1.5,2.3); ctx.fill(); ctx.globalAlpha=1; ctx.restore()

    # 9 — vaginal opening
    vagY=bot-30; vagRx=6.0+oF*0.8; vagRy=8.5
    vagRG=ctx.createRadialGradient(cx,vagY-1,1, cx,vagY,vagRx*1.9)
    add_stop(vagRG,0,ist['deep']); add_stop(vagRG,0.55,ist['deep']+'aa'); add_stop(vagRG,1,ist['deep']+'00')
    ctx.fillStyle=vagRG; ctx.globalAlpha=0.75
    ctx.beginPath(); ctx.ellipse(cx,vagY,vagRx,vagRy); ctx.fill(); ctx.globalAlpha=1
    if iS>0:
        ctx.save(); ctx.strokeStyle=st['shadow']; ctx.lineWidth=0.75; ctx.globalAlpha=0.22
        ctx.beginPath(); ctx.moveTo(cx-iS*3,vagY-7); ctx.lineTo(cx,vagY+3); ctx.lineTo(cx+iS*3,vagY-7)
        ctx.stroke(); ctx.globalAlpha=1; ctx.restore()

    # 10 — perineum
    ctx.save(); ctx.fillStyle=st['shadow']; ctx.globalAlpha=0.07
    ctx.beginPath(); ctx.ellipse(cx,bot-9,outerBulge*.55,8); ctx.fill(); ctx.globalAlpha=1; ctx.restore()

    # 11 — vignette
    vigG=ctx.createRadialGradient(cx,H*.44,H*.28, cx,H*.44,H*.82)
    add_stop(vigG,0,'rgba(0,0,0,0)'); add_stop(vigG,1,'rgba(90,40,10,0.09)')
    ctx.fillStyle=vigG; ctx.fillRect(0,0,W,H)

    # 12 — label
    ctx.save()
    ctx.cr.set_font_size(8.5)
    ctx.cr.select_font_face('Georgia', cairo.FONT_SLANT_ITALIC, cairo.FONT_WEIGHT_NORMAL)
    r,g,b,_=parse_rgba('#b08060'); ctx.cr.set_source_rgb(r,g,b)
    label = v.get('desc','')
    ext = ctx.cr.text_extents(label)
    ctx.cr.move_to(cx - ext.width/2, H-13); ctx.cr.show_text(label)
    ctx.restore()


# ── DRAW VULVA RECLINED (special 440×540, sc=2) ────────────────────────────────
def drawVulvaReclined(ctx, v, W, H):
    st  = SKIN_TONES[v['tone']]
    ist = SKIN_TONES[v.get('innerTone', v['tone'])]
    ctx.clearRect(0,0,W,H)
    cx=W/2; sc=W/220
    oF=min(3,(v.get('oS',2)+0.5)); outerBulge=(18+oF*10)*sc
    iS=v.get('iS',0); asym=v.get('asym',0); ruf=v.get('ruf',0)
    hs=v.get('hairStyle',0); hood=v.get('hood',2); gVis=v.get('gV',0.4)
    top=18*sc; bot=H-20*sc; totalH=bot-top; midY=top+totalH*0.46

    # background
    bgG=ctx.createRadialGradient(cx,H*.36,H*.05, cx,H*.54,H*.92)
    add_stop(bgG,0,'#fcf0e0'); add_stop(bgG,0.5,'#f4dfc9'); add_stop(bgG,1,'#e3ccb5')
    ctx.fillStyle=bgG; ctx.fillRect(0,0,W,H)

    # inner thighs
    def drawThigh(side):
        s=side; innerEdgeX=cx+s*outerBulge*1.02
        ctx.beginPath()
        if s<0:
            ctx.moveTo(0,0)
            ctx.bezierCurveTo(W*.20,H*.01, W*.32,H*.16, innerEdgeX,H*.44)
            ctx.bezierCurveTo(innerEdgeX+sc*2,H*.72, W*.22,H*.91, 0,H)
        else:
            ctx.moveTo(W,0)
            ctx.bezierCurveTo(W*.80,H*.01, W*.68,H*.16, innerEdgeX,H*.44)
            ctx.bezierCurveTo(innerEdgeX-sc*2,H*.72, W*.78,H*.91, W,H)
        ctx.lineTo(0 if s<0 else W, 0); ctx.closePath()
        tG=ctx.createRadialGradient(cx+s*W*.21,H*.25,sc*3, cx+s*W*.30,H*.50,W*.40)
        add_stop(tG,0,st['mid']); add_stop(tG,0.32,st['skin'])
        add_stop(tG,0.70,st['shadow']); add_stop(tG,1,st['deep']+'dd')
        ctx.fillStyle=tG; ctx.fill()
        # highlight
        ctx.beginPath()
        if s<0:
            ctx.moveTo(0,0); ctx.bezierCurveTo(W*.20,H*.01,W*.32,H*.16,innerEdgeX,H*.44)
            ctx.bezierCurveTo(innerEdgeX+sc*2,H*.72,W*.22,H*.91,0,H)
        else:
            ctx.moveTo(W,0); ctx.bezierCurveTo(W*.80,H*.01,W*.68,H*.16,innerEdgeX,H*.44)
            ctx.bezierCurveTo(innerEdgeX-sc*2,H*.72,W*.78,H*.91,W,H)
        ctx.lineTo(0 if s<0 else W, 0); ctx.closePath()
        hlG=ctx.createLinearGradient(cx+s*W*.10,H*.04, cx+s*W*.25,H*.30)
        add_stop(hlG,0,'rgba(255,255,255,0.20)'); add_stop(hlG,1,'rgba(255,255,255,0)')
        ctx.fillStyle=hlG; ctx.fill()
        # crease shadow
        creaseDir= 1 if s<0 else -1
        cG=ctx.createLinearGradient(innerEdgeX,H*.3, innerEdgeX+creaseDir*outerBulge*0.28,H*.3)
        add_stop(cG,0,'rgba(20,5,2,0.30)'); add_stop(cG,1,'rgba(20,5,2,0)')
        ctx.fillStyle=cG
        rx=innerEdgeX-outerBulge*0.28 if s<0 else innerEdgeX
        ctx.cr.rectangle(rx, H*.10, outerBulge*0.28, H*.78); ctx.fill()
    drawThigh(-1); drawThigh(1)

    # depth shadow
    dG=ctx.createRadialGradient(cx,midY,4*sc, cx,midY,outerBulge*1.30)
    add_stop(dG,0,'rgba(0,0,0,0.25)'); add_stop(dG,0.55,'rgba(0,0,0,0.09)'); add_stop(dG,1,'rgba(0,0,0,0)')
    ctx.fillStyle=dG; ctx.beginPath(); ctx.ellipse(cx,midY,outerBulge*1.30,totalH*0.60); ctx.fill()

    # mons
    mG=ctx.createRadialGradient(cx-4*sc,top+4*sc,4*sc, cx,top+14*sc,outerBulge*1.1)
    add_stop(mG,0,st['mid']); add_stop(mG,0.45,st['skin']); add_stop(mG,1,st['shadow'])
    ctx.fillStyle=mG
    ctx.beginPath(); ctx.moveTo(cx-outerBulge-8*sc,top+20*sc)
    ctx.bezierCurveTo(cx-outerBulge-4*sc,top-4*sc, cx+outerBulge+4*sc,top-4*sc, cx+outerBulge+8*sc,top+20*sc)
    ctx.bezierCurveTo(cx+outerBulge*.65,top+10*sc, cx-outerBulge*.65,top+10*sc, cx-outerBulge-8*sc,top+20*sc)
    ctx.fill()
    monsHL=ctx.createRadialGradient(cx-3*sc,top+7*sc,2*sc, cx,top+14*sc,outerBulge*0.82)
    add_stop(monsHL,0,'rgba(255,255,255,0.25)'); add_stop(monsHL,1,'rgba(255,255,255,0)')
    ctx.fillStyle=monsHL; ctx.globalAlpha=0.85
    ctx.beginPath(); ctx.ellipse(cx,top+14*sc,outerBulge*0.82,20*sc); ctx.fill(); ctx.globalAlpha=1

    # hair
    drawHairByStyle(ctx,cx,top+2*sc,outerBulge*1.8,hs,st['hair'])

    # labia majora
    def drawMajoraR(side):
        s=side; outerX=cx+s*outerBulge*1.10; innerX=cx+s*(8*sc+oF*3*sc)
        g=ctx.createRadialGradient(cx+s*outerBulge*.40,midY-18*sc,3*sc, cx+s*outerBulge*.55,midY+4*sc,outerBulge*1.2)
        add_stop(g,0,st['mid']); add_stop(g,0.26,st['skin'])
        add_stop(g,0.63,st['shadow']); add_stop(g,0.88,st['deep']); add_stop(g,1,'#0d0604')
        ctx.fillStyle=g
        ctx.beginPath(); ctx.moveTo(cx,top+18*sc)
        ctx.bezierCurveTo(cx+s*16*sc,top+12*sc, outerX-s*2*sc,top+36*sc, outerX,midY)
        ctx.bezierCurveTo(outerX,midY+34*sc, cx+s*18*sc,bot-18*sc, cx,bot)
        ctx.bezierCurveTo(innerX-s*2*sc,bot-10*sc, innerX,midY+26*sc, innerX,midY)
        ctx.bezierCurveTo(innerX,midY-28*sc, cx+s*11*sc,top+22*sc, cx,top+18*sc)
        ctx.closePath(); ctx.fill()
        hG=ctx.createLinearGradient(cx,top+18*sc, cx+s*outerBulge*.62,top+50*sc)
        add_stop(hG,0,'rgba(255,255,255,0.24)'); add_stop(hG,1,'rgba(255,255,255,0)')
        ctx.fillStyle=hG; ctx.globalAlpha=0.52
        ctx.beginPath(); ctx.moveTo(cx,top+18*sc)
        ctx.bezierCurveTo(cx+s*16*sc,top+12*sc, outerX-s*2*sc,top+36*sc, outerX,midY-10*sc)
        ctx.bezierCurveTo(cx+s*outerBulge*.72,midY-16*sc, cx+s*10*sc,top+27*sc, cx,top+18*sc)
        ctx.fill(); ctx.globalAlpha=1
    drawMajoraR(-1); drawMajoraR(1)

    # vestibule
    vW=(10+oF*2.4)*sc
    vG=ctx.createLinearGradient(cx,top+22*sc, cx,bot-14*sc)
    add_stop(vG,0,ist['shadow']+'bb'); add_stop(vG,0.48,ist['inner']+'cc'); add_stop(vG,1,ist['deep']+'77')
    ctx.fillStyle=vG
    ctx.beginPath(); ctx.moveTo(cx,top+21*sc)
    ctx.bezierCurveTo(cx-vW,top+33*sc, cx-vW,bot-28*sc, cx,bot-12*sc)
    ctx.bezierCurveTo(cx+vW,bot-28*sc, cx+vW,top+33*sc, cx,top+21*sc); ctx.fill()

    # labia minora (reclined)
    reclSpread=[0,8,12,17,22]; reclBotFrac=[0,0.58,0.72,0.83,0.91]
    def drawMinoraR(side, sizeScale, iSOverride=None, rufScale=1.0):
        s=side; effectiveIS=min(iSOverride,4) if iSOverride is not None else min(iS,4)
        spread=reclSpread[effectiveIS]*sizeScale*sc
        if spread<1: return
        tA=top+21*sc; bA=top+totalH*reclBotFrac[effectiveIS]; steps=48
        eRuf=ruf*rufScale

        def buildPath():
            ctx.beginPath(); ctx.moveTo(cx,tA)
            for i in range(1,steps+1):
                t=i/steps; lb=1.0+0.18*math.sin(t*math.pi); arc=math.sin(t*math.pi*0.88)
                bx=cx+s*spread*lb*arc; by=tA+(bA-tA)*t
                wave=math.sin(t*math.pi*(3+eRuf*1.6))*eRuf*4.2 if eRuf>0 else 0
                ctx.lineTo(bx+wave*(s*0.28), by+wave*0.35)
            tipX=cx+s*spread*0.72; tipY=bA+4*sc
            ctx.bezierCurveTo(tipX+s*1.5*sc,tipY+3*sc, cx+s*1.5*sc,tipY+2*sc, cx,bA+sc)
            for i in range(steps,-1,-1):
                t=i/steps; bx=cx+s*spread*0.22*math.sin(t*math.pi); by=tA+(bA-tA)*t
                wave=math.sin(t*math.pi*2.2+0.8)*eRuf*2.2*0.35 if eRuf>0 else 0
                ctx.lineTo(bx, by+wave*0.12)
            ctx.closePath()

        # layer 1: shadow behind tissue
        ctx.save(); ctx.globalAlpha=0.48
        buildPath(); ctx.fillStyle=ist['shadow']; ctx.fill(); ctx.restore()

        # layer 2: main tissue fill
        buildPath()
        mG2=ctx.createLinearGradient(cx+s*spread*0.5,tA, cx+s*spread*0.5,bA)
        add_stop(mG2,0,ist['shadow']); add_stop(mG2,0.20,ist['inner'])
        add_stop(mG2,0.58,ist['deep']); add_stop(mG2,1,'#1a0808')
        ctx.fillStyle=mG2; ctx.fill()

        # layer 3: raised front face
        buildPath()
        hlG=ctx.createLinearGradient(cx+s*spread*0.38,tA+totalH*0.06, cx+s*spread*0.38,bA*0.90)
        add_stop(hlG,0,ist['mid']+'aa'); add_stop(hlG,0.38,ist['inner']+'66')
        add_stop(hlG,0.72,ist['inner']+'28'); add_stop(hlG,1,ist['deep']+'00')
        ctx.fillStyle=hlG; ctx.globalAlpha=0.58; ctx.fill(); ctx.globalAlpha=1

        # catch-light
        ctx.save(); ctx.strokeStyle='rgba(255,248,238,0.22)'; ctx.lineWidth=0.85*sc; ctx.globalAlpha=0.78
        ctx.beginPath(); ctx.moveTo(cx+s*1.8*sc,tA+6*sc)
        for i in range(1,17):
            t=i/16; lb=1.0+0.18*math.sin(t*math.pi); wave=math.sin(t*math.pi*(3+eRuf))*eRuf*3.0 if eRuf>0 else 0
            arc=math.sin(t*math.pi*0.88)
            ctx.lineTo(cx+s*spread*0.76*lb*arc+wave*s*0.22, tA+(bA-tA)*t*0.66+wave*0.26)
        ctx.stroke(); ctx.globalAlpha=1; ctx.restore()

    drawMinoraR(-1, 1)
    drawMinoraR(1, 1, v.get('asymIS'), v.get('asymRufScale', 1.0))

    # clitoral complex
    hoodW=(4.5+hood*2.6)*sc; hoodH=(6+hood*3.2)*sc; hoodY=top+14*sc
    clitPenis=v.get('clitPenis',False)

    if not clitPenis:
        hG2=ctx.createRadialGradient(cx-2.5*sc,hoodY,sc, cx,hoodY+5*sc,hoodH)
        add_stop(hG2,0,st['mid']); add_stop(hG2,0.5,st['skin']); add_stop(hG2,1,st['inner'])
        ctx.fillStyle=hG2
        ctx.beginPath(); ctx.moveTo(cx-hoodW,hoodY+hoodH)
        ctx.bezierCurveTo(cx-hoodW-sc,hoodY-4*sc, cx+hoodW+sc,hoodY-4*sc, cx+hoodW,hoodY+hoodH)
        ctx.bezierCurveTo(cx+hoodW*.5,hoodY+hoodH+6*sc, cx-hoodW*.5,hoodY+hoodH+6*sc, cx-hoodW,hoodY+hoodH)
        ctx.fill()

    if clitPenis:
        shW=7.2*sc; shWc=6.0*sc; gR=9.4*sc
        rootY=hoodY+hoodH*0.54; shLen=44*sc; corY=rootY+shLen; gCy=corY+gR*0.46
        shG=ctx.createLinearGradient(cx-gR*1.05,0, cx+gR*1.05,0)
        add_stop(shG,0,ist['shadow']); add_stop(shG,0.13,ist['deep']); add_stop(shG,0.32,ist['inner'])
        add_stop(shG,0.50,ist['mid']); add_stop(shG,0.70,ist['inner']); add_stop(shG,0.88,ist['deep']); add_stop(shG,1,ist['shadow'])
        ctx.save()
        ctx.beginPath(); ctx.moveTo(cx-shW, rootY+6*sc)
        ctx.bezierCurveTo(cx-shW*1.07,rootY+shLen*.30, cx-shWc*1.04,corY-shLen*.18, cx-shWc,corY)
        ctx.bezierCurveTo(cx-shWc*.90,corY+gR*.20, cx-gR*.96,gCy-gR*.32, cx-gR,gCy)
        ctx.bezierCurveTo(cx-gR*.88,gCy+gR*.92, cx+gR*.84,gCy+gR*.90, cx+gR,gCy)
        ctx.bezierCurveTo(cx+gR*.94,gCy-gR*.34, cx+shWc*.88,corY+gR*.18, cx+shWc,corY)
        ctx.bezierCurveTo(cx+shWc*1.06,corY-shLen*.20, cx+shW*1.05,rootY+shLen*.32, cx+shW,rootY+6*sc)
        ctx.closePath(); ctx.fillStyle=shG; ctx.fill()
        ctx.strokeStyle=ist['shadow']; ctx.lineWidth=0.8*sc; ctx.globalAlpha=0.26; ctx.stroke(); ctx.globalAlpha=1
        ctx.restore()
        # glans specular
        ctx.save(); ctx.beginPath()
        ctx.ellipse(cx-gR*.27,gCy-gR*.32,gR*.24,gR*.15,-0.28)
        ctx.fillStyle='rgba(255,255,255,0.23)'; ctx.fill(); ctx.restore()
    elif gVis>0.45:
        glansR=(1.8+gVis*5.2)*sc; glansY=hoodY+hoodH-glansR*0.22
        glG=ctx.createRadialGradient(cx-glansR*.28,glansY-glansR*.32,glansR*.08, cx,glansY,glansR*1.15)
        add_stop(glG,0,st['mid']); add_stop(glG,0.40,st['inner']); add_stop(glG,0.78,st['deep']); add_stop(glG,1,st['shadow'])
        ctx.save(); ctx.beginPath(); ctx.ellipse(cx,glansY,glansR,glansR*1.10)
        ctx.fillStyle=glG; ctx.fill(); ctx.restore()
    else:
        ctx.save(); ctx.fillStyle=st['deep']; ctx.globalAlpha=0.42+gVis*0.48
        ctx.beginPath(); ctx.ellipse(cx,hoodY+sc,hoodW*.48,hoodH*.36); ctx.fill(); ctx.globalAlpha=1; ctx.restore()

    if not clitPenis:
        ctx.save(); ctx.fillStyle='rgba(255,255,255,0.22)'
        ctx.beginPath(); ctx.ellipse(cx-hoodW*.28,hoodY-sc,hoodW*.20,hoodH*.18,-0.3); ctx.fill(); ctx.restore()

    # urethral opening
    if not clitPenis:
        ctx.save(); ctx.fillStyle=ist['deep']; ctx.globalAlpha=0.36
        ctx.beginPath(); ctx.ellipse(cx,top+35*sc,1.5*sc,2.3*sc); ctx.fill(); ctx.globalAlpha=1; ctx.restore()

    # vaginal opening
    vagY=bot-28*sc; vagRx=7.0*sc+oF*0.9*sc; vagRy=9.0*sc
    vagRG=ctx.createRadialGradient(cx,vagY-sc,sc, cx,vagY,vagRx*1.9)
    add_stop(vagRG,0,ist['deep']); add_stop(vagRG,0.55,ist['deep']+'aa'); add_stop(vagRG,1,ist['deep']+'00')
    ctx.fillStyle=vagRG; ctx.globalAlpha=0.74
    ctx.beginPath(); ctx.ellipse(cx,vagY,vagRx,vagRy); ctx.fill(); ctx.globalAlpha=1

    # perineum
    ctx.save(); ctx.fillStyle=st['shadow']; ctx.globalAlpha=0.08
    ctx.beginPath(); ctx.ellipse(cx,bot-8*sc,outerBulge*.52,7*sc); ctx.fill(); ctx.globalAlpha=1; ctx.restore()

    # vignette
    vigG=ctx.createRadialGradient(cx,H*.44,H*.26, cx,H*.44,H*.82)
    add_stop(vigG,0,'rgba(0,0,0,0)'); add_stop(vigG,1,'rgba(75,30,8,0.14)')
    ctx.fillStyle=vigG; ctx.fillRect(0,0,W,H)


# ── ENHANCE VULVA CANVAS (special entries only) ────────────────────────────────
def enhanceVulvaCanvas(ctx, v, W, H):
    st  = SKIN_TONES[v['tone']]
    ist = SKIN_TONES[v.get('innerTone', v['tone'])]
    cx=W/2; sc=W/220; top=20*sc; bot=H-26*sc; totalH=bot-top; midY=top+totalH*0.43
    oF=v.get('oS',2); outerBulge=(16+oF*9)*sc; iS=v.get('iS',0)
    hood=v.get('hood',2); gVis=v.get('gV',0.4); ruf=v.get('ruf',0)
    iSpreads=[0,6,10,14,18]

    # colour temperature variation
    ctx.save()
    monsWarm=ctx.createRadialGradient(cx-W*.06,top+totalH*.07,2, cx,top+totalH*.15,outerBulge*.95)
    add_stop(monsWarm,0,'rgba(255,225,150,0.13)'); add_stop(monsWarm,1,'rgba(255,225,150,0)')
    ctx.fillStyle=monsWarm; ctx.fillRect(0,0,W,H)
    crC=ctx.createLinearGradient(cx-outerBulge*.45,midY-totalH*.06, cx,midY+totalH*.08)
    add_stop(crC,0,'rgba(70,35,80,0.09)'); add_stop(crC,1,'rgba(70,35,80,0)')
    ctx.fillStyle=crC; ctx.fillRect(0,0,W,H)
    crCR=ctx.createLinearGradient(cx+outerBulge*.45,midY-totalH*.06, cx,midY+totalH*.08)
    add_stop(crCR,0,'rgba(70,35,80,0.09)'); add_stop(crCR,1,'rgba(70,35,80,0)')
    ctx.fillStyle=crCR; ctx.fillRect(0,0,W,H)
    vestiWarm=ctx.createRadialGradient(cx,midY+totalH*.04,sc*2, cx,midY+totalH*.08,outerBulge*.72)
    add_stop(vestiWarm,0,'rgba(215,75,65,0.14)'); add_stop(vestiWarm,0.45,'rgba(200,68,60,0.08)'); add_stop(vestiWarm,1,'rgba(185,60,55,0)')
    ctx.fillStyle=vestiWarm; ctx.fillRect(0,0,W,H)
    hoodHeat=ctx.createRadialGradient(cx,top+totalH*.24,sc, cx,top+totalH*.27,outerBulge*.36)
    add_stop(hoodHeat,0,'rgba(225,100,80,0.15)'); add_stop(hoodHeat,1,'rgba(225,100,80,0)')
    ctx.fillStyle=hoodHeat; ctx.fillRect(0,0,W,H)
    ctx.restore()

    # skin texture stipple
    ctx.save()
    def stipple(count,xRange,yMin,yMax,a1,a2,r1,r2,col):
        for _ in range(count):
            dx=cx+random.uniform(-xRange,xRange); dy=random.uniform(yMin,yMax)
            dxN=(dx-cx)/(xRange+sc*4); dyN=(dy-(top+totalH*0.5))/(totalH*0.62)
            if dxN*dxN+dyN*dyN>1.15: continue
            ctx.globalAlpha=random.uniform(a1,a2)
            ctx.fillStyle=col
            ctx.beginPath(); ctx.arc(dx,dy,random.uniform(r1,r2)*sc,0,2*math.pi); ctx.fill()
    stipple(340,outerBulge+sc*8,top,midY+totalH*.38, 0.014,0.044,0.28,0.95,st['shadow'])
    stipple(180,outerBulge+sc*6,top,midY+totalH*.32, 0.010,0.030,0.20,0.60,st['deep'])
    stipple(110,outerBulge*.72,top,top+totalH*.24,   0.022,0.058,0.18,0.48,'rgba(255,255,255,1)')
    ctx.globalAlpha=1; ctx.restore()

    # enhanced clitoral detail
    if gVis>0.50:
        hoodW=(4.5+hood*2.6)*sc; hoodH=(6+hood*3.2)*sc; hoodY=top+15*sc
        ctx.save()
        gHaloG=ctx.createRadialGradient(cx,hoodY+hoodH*.08,sc, cx,hoodY+hoodH*.14,hoodW*1.1)
        add_stop(gHaloG,0,f'rgba(228,105,85,{gVis*0.26})')
        add_stop(gHaloG,0.5,f'rgba(215,90,75,{gVis*0.12})')
        add_stop(gHaloG,1,'rgba(200,80,65,0)')
        ctx.fillStyle=gHaloG
        ctx.cr.rectangle(cx-hoodW*1.4,hoodY-hoodH*.4,hoodW*2.8,hoodH*2.0); ctx.fill()
        ctx.fillStyle='rgba(255,255,255,0.45)'; ctx.globalAlpha=gVis*0.72
        ctx.beginPath(); ctx.ellipse(cx-hoodW*.15,hoodY-hoodH*.08,hoodW*.11,hoodH*.09,-0.42); ctx.fill()
        ctx.globalAlpha=1; ctx.restore()

    # edge vignette
    ctx.save()
    vig2=ctx.createRadialGradient(cx,H*.46,H*.22, cx,H*.46,H*.82)
    add_stop(vig2,0,'rgba(0,0,0,0)'); add_stop(vig2,0.75,'rgba(40,15,5,0.04)'); add_stop(vig2,1,'rgba(40,15,5,0.14)')
    ctx.fillStyle=vig2; ctx.fillRect(0,0,W,H); ctx.restore()


# ── SCULPTURAL LIGHTING LAYER (all entries) ───────────────────────────────────
def addSculpturalLayer(ctx, v, W, H):
    st=SKIN_TONES[v['tone']]; cx=W/2; sc=W/220
    rl=v.get('reclined',False)
    top=(18 if rl else 20)*sc; bot=H-(20 if rl else 26)*sc; totalH=bot-top
    midY=top+totalH*(0.46 if rl else 0.43)
    oF=(v.get('oS',2))+(0.5 if rl else 0); outerBulge=((18 if rl else 16)+oF*(10 if rl else 9))*sc
    iS=v.get('iS',0); ruf=v.get('ruf',0); hood=v.get('hood',2)
    iSpr=[0,8,12,17,22] if rl else [0,6,10,14,18]

    # directional light sweep
    sweep=ctx.createLinearGradient(0,0, W*.82,H*.86)
    add_stop(sweep,0,'rgba(255,250,228,0.22)'); add_stop(sweep,0.36,'rgba(255,250,228,0.04)')
    add_stop(sweep,0.60,'rgba(10,3,0,0.03)');   add_stop(sweep,1,'rgba(10,3,0,0.20)')
    ctx.fillStyle=sweep; ctx.fillRect(0,0,W,H)

    # outer labia rim highlights
    for side in [-1,1]:
        s=side; outerX=cx+s*outerBulge*(1.10 if rl else 1.0)
        startY=top+(18 if rl else 20)*sc; cp1y=top+13*sc
        cp2y=top+(36 if rl else 38)*sc; endY1=midY; endY2=midY+(34 if rl else 33)*sc
        cp3y=bot-(18 if rl else 20)*sc
        ctx.save()
        ctx.beginPath(); ctx.moveTo(cx,startY)
        ctx.bezierCurveTo(cx+s*14*sc,cp1y, outerX-s*2*sc,cp2y, outerX,endY1)
        ctx.bezierCurveTo(outerX,endY2, cx+s*(18 if rl else 16)*sc,cp3y, cx,bot)
        lh=lighten_hex(st['skin'],0.52); ctx.strokeStyle=lh; ctx.lineWidth=5.5*sc; ctx.globalAlpha=0.24; ctx.stroke()
        lh=lighten_hex(st['skin'],0.65); ctx.strokeStyle=lh; ctx.lineWidth=2.2*sc; ctx.globalAlpha=0.38; ctx.stroke()
        lh=lighten_hex(st['skin'],0.80); ctx.strokeStyle=lh; ctx.lineWidth=0.9*sc; ctx.globalAlpha=0.55; ctx.stroke()
        ctx.globalAlpha=1; ctx.restore()

    # ambient occlusion
    aoG=ctx.createRadialGradient(cx,midY,sc*1.5, cx,midY+totalH*.04,outerBulge*.50)
    add_stop(aoG,0,'rgba(0,0,0,0.45)'); add_stop(aoG,0.42,'rgba(0,0,0,0.18)')
    add_stop(aoG,0.72,'rgba(0,0,0,0.06)'); add_stop(aoG,1,'rgba(0,0,0,0)')
    ctx.fillStyle=aoG; ctx.fillRect(0,0,W,H)
    for side in [-1,1]:
        innerX=cx+side*(8*sc+oF*3*sc); shW=outerBulge*0.20
        cG=ctx.createLinearGradient(innerX,0, innerX-side*shW,0)
        add_stop(cG,0,'rgba(0,0,0,0.22)'); add_stop(cG,1,'rgba(0,0,0,0)')
        ctx.fillStyle=cG
        rx=innerX-shW if side<0 else innerX
        ctx.cr.rectangle(rx,top+totalH*.08,shW,totalH*.80); ctx.fill()

    # inner labia rim highlights
    if iS>=2:
        spread=iSpr[min(iS,4)]*sc; tA=top+(21 if rl else 23)*sc; bA=top+totalH*0.665
        for side in [-1,1]:
            s=side
            ctx.save()
            ctx.beginPath()
            for i in range(19):
                t=i/18; lb=(1.0+0.26*math.sin(t*math.pi)) if rl else 1.0
                wave=math.sin(t*math.pi*(3+ruf*1.6))*ruf*(4.5 if rl else 3.8) if ruf>0 else 0
                bx=cx+s*spread*lb*math.sin(t*math.pi*0.9)+wave*s*0.50
                by=tA+(bA-tA)*t+wave*0.17
                if i==0: ctx.moveTo(bx,by)
                else:     ctx.lineTo(bx,by)
            lh=lighten_hex(st['skin'],0.48); ctx.strokeStyle=lh; ctx.lineWidth=4.0*sc; ctx.globalAlpha=0.20; ctx.stroke()
            lh=lighten_hex(st['skin'],0.68); ctx.strokeStyle=lh; ctx.lineWidth=1.0*sc; ctx.globalAlpha=0.52; ctx.stroke()
            ctx.globalAlpha=1; ctx.restore()

    # clitoral hood highlight
    hoodW=(4.5+hood*2.6)*sc; hoodH=(6+hood*3.2)*sc; hoodY=top+(14 if rl else 15)*sc
    ctx.save(); ctx.fillStyle=lighten_hex(st['skin'],0.68); ctx.globalAlpha=0.46
    ctx.beginPath(); ctx.ellipse(cx-hoodW*.18,hoodY+hoodH*.10,hoodW*.60,hoodH*.40,-0.10); ctx.fill()
    ctx.globalAlpha=1; ctx.restore()

    # mons highlight
    monsG=ctx.createRadialGradient(cx-4*sc,top+5*sc,2*sc, cx,top+13*sc,outerBulge*.80)
    add_stop(monsG,0,lighten_hex(st['skin'],0.60)); add_stop(monsG,0.45,lighten_hex(st['skin'],0.28))
    add_stop(monsG,1,'rgba(255,255,255,0)')
    ctx.fillStyle=monsG; ctx.globalAlpha=0.52
    ctx.beginPath(); ctx.ellipse(cx,top+13*sc,outerBulge*.80,20*sc); ctx.fill(); ctx.globalAlpha=1


# ── RENDER ────────────────────────────────────────────────────────────────────
def render_variation(v, idx):
    special = v.get('special', False)
    W = SPECIAL_W if special else NORMAL_W
    H = SPECIAL_H if special else NORMAL_H

    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    cr = cairo.Context(surface)
    ctx = Ctx(cr)

    random.seed(idx * 137 + 42)  # deterministic hair per variation

    if v.get('reclined', False):
        drawVulvaReclined(ctx, v, W, H)
    else:
        drawVulva(ctx, v, W, H)

    addSculpturalLayer(ctx, v, W, H)

    if special:
        random.seed(idx * 137 + 99)  # separate seed for stipple
        enhanceVulvaCanvas(ctx, v, W, H)

    path = os.path.join(OUTPUT_DIR, f'vulva_{idx:02d}.png')
    surface.write_to_png(path)
    print(f'  [{idx:02d}] {v["desc"][:55]}')
    return path, W, H


def make_montage(paths_dims):
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        print('  (pillow not installed — skipping montage)')
        return

    COLS=4; PAD=8; LABEL_H=22; BG=(245,240,232)
    max_w=max(w for _,w,_ in paths_dims); max_h=max(h for _,_,h in paths_dims)
    cell_w=max_w+PAD*2; cell_h=max_h+LABEL_H+PAD*2
    rows=math.ceil(len(paths_dims)/COLS)
    montage=Image.new('RGB',(COLS*cell_w, rows*cell_h), BG)
    draw=ImageDraw.Draw(montage)

    for i,(path,w,h) in enumerate(paths_dims):
        col=i%COLS; row=i//COLS
        x=col*cell_w+PAD; y=row*cell_h+PAD
        img=Image.open(path).convert('RGBA')
        bg=Image.new('RGB',(w,h),(245,240,232))
        bg.paste(img,(0,0),img)
        montage.paste(bg,(x,y))
        v=VULVA_VARIATIONS[i]; label=v['desc'][:38]
        draw.text((x+w//2, y+h+4), label, fill=(160,100,70), anchor='mt')

    out=os.path.join(OUTPUT_DIR,'montage.png')
    montage.save(out)
    print(f'\n  Montage → {out}')


if __name__ == '__main__':
    print(f'Rendering {len(VULVA_VARIATIONS)} vulva variations...')
    paths_dims=[]
    for i,v in enumerate(VULVA_VARIATIONS):
        path,w,h = render_variation(v,i)
        paths_dims.append((path,w,h))
    make_montage(paths_dims)
    print(f'\nDone. PNGs in ./{OUTPUT_DIR}/')
