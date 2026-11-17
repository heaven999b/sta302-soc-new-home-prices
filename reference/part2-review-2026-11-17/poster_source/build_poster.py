from pathlib import Path
import csv,json
import numpy as np
from statistics import NormalDist
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor,white
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
O=Path(__file__).resolve().parent.parent
# Copied into poster_source/ before execution.
rows=list(csv.DictReader(open(O/'results/regional_effects.csv')))
S=json.loads((O/'results/summary.json').read_text())
mc=list(csv.DictReader(open(O/'results/model_comparison.csv')))
dn=list(csv.DictReader(open(O/'results/diagnostic_numbers.csv')))
W,H=841/25.4*72,594/25.4*72
C=canvas.Canvas(str(O/'Poster_Part2_review.pdf'),pagesize=(W,H),pageCompression=1)
C.setTitle('Bigger homes, different regional price patterns');C.setAuthor('')
navy='#133343';teal='#176C75';ink='#233C47';light='#EAF1F3';orange='#C85C37'
def text(t,x,y,w,size=28,leading=None,color=ink,bold=False):
 st=ParagraphStyle('p',fontName='Helvetica-Bold' if bold else 'Helvetica',fontSize=size,leading=leading or size*1.2,textColor=HexColor(color))
 p=Paragraph(t,st);_,h=p.wrap(w,4000);p.drawOn(C,x,y-h);return y-h

def heading(t,x,y,w):
 C.setFillColor(HexColor(teal));C.rect(x,y-5,w,4,fill=1,stroke=0)
 return text(t,x,y-20,w,32,bold=True,color=navy)-12

def body(t,x,y,w):return text(t,x,y,w)-12
C.setFillColor(white);C.rect(0,0,W,H,fill=1,stroke=0)
C.setFillColor(HexColor(navy));C.rect(0,H-170,W,170,fill=1,stroke=0)
text('Bigger homes, different regional price patterns',64,H-39,W-128,60,color='#FFFFFF',bold=True)
text('New U.S. home sales in 2025 | Adjusting for land, rooms and amenities',66,H-117,W-132,31,color='#D3E8EC')
C.setFillColor(HexColor(light));C.roundRect(64,H-288,W-128,90,12,fill=1,stroke=0)
text('<b>Size is positively associated with price in every division; fitted associations differ.</b><br/>A better response transformation stabilizes residual spread. Regional comparisons remain exploratory.',88,H-210,W-176,31,36,color=navy)
x1,x2,x3=64,816,1570;cw=686;top=H-315
# LEFT: why, what data, and actual evidence for the model decision.
Y=heading('1  Motivation & question',x1,top,cw)
Y=body('Do size-price associations differ across nine regions? Buyers comparing new homes need size adjustments that account for land, rooms and amenities, rather than a national average [1-3].',x1,Y,cw)
Y=heading('2  Data collection',x1,Y,cw)
Y=body('2025 Census Survey of Construction [4]: permit sampling, area canvassing and builder/owner interviews. Documented collection aids reliability; privacy coding alters values.',x1,Y,cw)
# A compact, labelled data flow rather than another paragraph.
for i,(n,label) in enumerate([('7,382','eligible homes'),('6,185','complete cases'),('4,330','training cases')]):
 x=x1+i*230
 C.setFillColor(HexColor(light));C.roundRect(x,Y-88,216,82,7,fill=1,stroke=0)
 text(n,x+12,Y-15,192,33,bold=True,color=navy);text(label,x+12,Y-55,200,28)
Y-=108
Y=body('New detached, non-condominium sales; price includes land. Missing-case loss: 16.2%. Reserve 1,855 cases; size/region fields suit the question.',x1,Y,cw)
Y=heading('3  Methods & model choice',x1,Y,cw)
Y=body('Diagnose → transform → select → recheck.<br/>After log(area), Box-Cox power is -0.504 (95% interval -0.554 to -0.455): choose -0.5.',x1,Y,cw)
# Model choice table, all columns use the same response and body font size.
text('Table 1. Same response; lower BIC preferred.',x1,Y,cw,28,bold=True);Y-=50
C.setFillColor(HexColor(light));C.rect(x1,Y-42,cw,42,fill=1,stroke=0)
for t,dx,w in [('Model',12,220),('Coefficients',260,195),('BIC',525,150)]:text(t,x1+dx,Y-6,w,28,bold=True)
Y-=48
for r in [mc[0],mc[2]]:
 label='Full' if r is mc[0] else 'BIC choice'
 text(label,x1+12,Y,240,28);text(r['coefficients'],x1+310,Y,110,28)
 text(f"{float(r['BIC']):,.1f}",x1+490,Y,196,28);Y-=43
Y-=10
Y=body('BIC balances fit and model size. We automate selection to limit manual discretion, retain area × region and lot size, disclose selection bias, and compare AIC.',x1,Y,cw)
left_bottom=Y
# CENTRE: understandable effect illustration, explicit model and inference boundary.
Y=heading('4  Results & final model',x2,top,cw)
Y=body('Figure 1. <b>10% more area:</b> illustrated price-index change (%) from <b>$500,000</b>. Ordinary 95% intervals.',x2,Y,cw)
plot_top=Y-16;labelw=275;px=x2+labelw;pw=cw-labelw-80
lo,hi=2,10
xx=lambda v:px+(float(v)-lo)/(hi-lo)*pw
for i,row in enumerate(rows):
 yy=plot_top-i*50
 if i%2==0:
  C.setFillColor(HexColor('#F3F6F7'));C.rect(x2,yy-25,cw,49,fill=1,stroke=0)
 text(row['division'],x2+6,yy+16,labelw-12,28)
 C.setStrokeColor(HexColor(teal));C.setLineWidth(4);C.line(xx(row['pct_low']),yy,xx(row['pct_high']),yy)
 C.setFillColor(HexColor(teal));C.circle(xx(row['pct']),yy,6,fill=1,stroke=0)
 text(f"{float(row['pct']):.1f}%",x2+cw-72,yy+16,72,28,bold=True)
yaxis=plot_top-9*50+8
C.setStrokeColor(HexColor('#9BAEB6'));C.setLineWidth(1);C.line(px,yaxis,px+pw,yaxis)
for v in [2,4,6,8,10]:C.line(xx(v),yaxis,xx(v),yaxis-7);text(str(v),xx(v)-10,yaxis-13,44,28)
Y=yaxis-65
Y=body('Index: inverse-transformed fitted mean, <b>not average sale price</b>. Changes depend on starting price. Selection makes intervals uncertain.',x2,Y,cw)
Y=body('<b>Final model:</b> z = 2 - 2/sqrt(P), P in $1000s;<br/>z = regional intercept + regional slope × log(area) + controls + error.',x2,Y,cw)
Y=body('Controls: lot, stories, bedrooms, full/half baths, garage, foundation, fireplaces, wall and heating fuel.',x2,Y,cw)
pval=f"{S['F']['p']:.2e}"
Y=body(f"<b>Equal-slope F(8, 4284) = {S['F']['F']:.2f};</b> nominal p = {pval}. Selection prevents confirmatory inference.",x2,Y,cw)
center_bottom=Y
# RIGHT: before/after plots, with all labels and ticks at body size.
Y=heading('5  Diagnostics: before & after',x3,top,cw)
def panel(x,y,title,xlabel,xv,yv,xlim,ylim,xticks,yticks,line=None,ylabel='Std. residual'):
 w=320;left=x+68;bottom=y-200;pw=237;ph=132
 text(title,x,y,w,28,bold=True)
 xf=lambda a:left+(a-xlim[0])/(xlim[1]-xlim[0])*pw
 yf=lambda a:bottom+(a-ylim[0])/(ylim[1]-ylim[0])*ph
 C.saveState();cl=C.beginPath();cl.rect(left,bottom,pw,ph);C.clipPath(cl,stroke=0,fill=0)
 C.setFillColor(HexColor(teal));C.setFillAlpha(.20)
 for a,b in zip(xv,yv):C.circle(xf(a),yf(b),1.35,stroke=0,fill=1)
 C.setFillAlpha(1)
 if line is not None:
  C.setStrokeColor(HexColor(orange));C.setLineWidth(3);p=C.beginPath()
  for i,(a,b) in enumerate(line):
   if i==0:p.moveTo(xf(a),yf(b))
   else:p.lineTo(xf(a),yf(b))
  C.drawPath(p)
 C.restoreState();C.setStrokeColor(HexColor('#809AA6'));C.setLineWidth(1)
 C.line(left,bottom,left+pw,bottom);C.line(left,bottom,left,bottom+ph)
 for v in xticks:C.line(xf(v),bottom,xf(v),bottom-5);text(str(v),xf(v)-19,bottom-10,66,28)
 for v in yticks:text(str(v),left-50,yf(v)+15,50,28)
 text(xlabel,left-18,bottom-48,pw+36,28)
 C.saveState();C.translate(x+15,bottom-9);C.rotate(90);C.setFillColor(HexColor(ink));C.setFont('Helvetica',28);C.drawString(0,0,ylabel);C.restoreState()
normal=NormalDist()
for k,nm in enumerate(['raw','final']):
 d=np.genfromtxt(O/f'figures/poster_{nm}_data.csv',delimiter=',',names=True)
 sm=np.genfromtxt(O/f'figures/poster_{nm}_smoother.csv',delimiter=',',names=True)
 yy=Y-k*295
 ttl='Before' if k==0 else 'After'
 xlim=(0,2700) if k==0 else (1.85,1.98);xt=[0,1000,2000] if k==0 else [1.86,1.92,1.98]
 panel(x3,yy,ttl+': spread','Fitted P' if k==0 else 'Fitted z',d['fitted'],np.sqrt(abs(d['standardized'])),xlim,(0,4),xt,[0,2,4],list(zip(sm['x'],sm['y'])),ylabel='sqrt(|r|)')
 ys=np.sort(d['standardized']);xs=np.array([normal.inv_cdf((i+.5)/len(ys)) for i in range(len(ys))]);q=np.quantile(ys,[.25,.75]);slope=(q[1]-q[0])/(normal.inv_cdf(.75)-normal.inv_cdf(.25));inter=q[0]-slope*normal.inv_cdf(.25)
 panel(x3+355,yy,ttl+': normal Q-Q','Normal quantile',xs,ys,(-4,4),(-8,14),[-3,0,3],[-5,5,13],[(-4,inter-4*slope),(4,inter+4*slope)])
Y-=584
Y=body('Figure 2. Spread flattens and tails improve (r: standardized residual). Tail departures and unverified builder dependence remain.',x3,Y,cw)
Y=heading('6  Conclusion & limitations',x3,Y,cw)
Y=body('Regional fitted associations differ, consistent with [1]. This sample cannot establish renovation returns or a reliable regional ranking.',x3,Y,cw)
Y=body(f"New England: 39 training homes. Excluding coded prices/areas/lots shifts an illustrated effect by up to <b>{S['max_flags_pctpoint_change']:.1f} percentage points</b>.",x3,Y,cw)
Y=body('Next: finer location/builder IDs, survey-design information and new data to assess a fixed model.',x3,Y,cw)
right_bottom=Y
print('Column bottoms:',left_bottom,center_bottom,right_bottom)
assert min(left_bottom,center_bottom,right_bottom)>220,'Content overlaps footer'
fy=205
C.setStrokeColor(HexColor('#BCCDD2'));C.line(64,fy,W-64,fy)
text('The $500,000 reference is fixed for illustration, not an estimated average. Covariates stay fixed within comparisons; test performance is not yet evaluated.',64,fy-13,W-128,28)
refs='<b>References</b> [1] Sirmans et al. (2006). The value of housing characteristics: A meta analysis. <i>JREFE, 33</i>, 215-240. doi:10.1007/s11146-006-9983-5. [2] Gyourko &amp; Saiz (2006). Construction costs and the supply of housing structure. <i>JRS, 46</i>, 661-680. doi:10.1111/j.1467-9787.2006.00472.x.<br/>[3] Zietz, Sirmans, &amp; Smersh (2008). The impact of inflation on home prices and the valuation of housing characteristics across the price distribution. <i>JHR, 17</i>, 119-137. doi:10.1080/10835547.2008.12091992. [4] U.S. Census Bureau (2026). <i>Survey of Construction: 2025 microdata and variable guide.</i> census.gov/construction/chars/microdata.html.'
ref_bottom=text(refs,64,fy-86,W-128,18,22)
print("Reference bottom:",ref_bottom)
assert ref_bottom>20
C.save()
