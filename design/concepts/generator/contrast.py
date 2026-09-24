def lum(h):
    h=h.lstrip('#')
    if len(h)==3: h=''.join(c*2 for c in h)
    r,g,b=[int(h[i:i+2],16)/255 for i in (0,2,4)]
    f=lambda c: c/12.92 if c<=0.03928 else ((c+0.055)/1.055)**2.4
    return 0.2126*f(r)+0.7152*f(g)+0.0722*f(b)
def cr(a,b):
    la,lb=lum(a),lum(b); la,lb=max(la,lb),min(la,lb); return (la+0.05)/(lb+0.05)
if __name__=='__main__':
    day=dict(bg='#FAF6EF',surface='#FFFDF8',text='#1E1A16',text2='#5A5249',border='#E4DDD1',borderS='#8A8075',primary='#C23B1C',primaryH='#A8321A',primaryP='#8E2A15',onP='#FFFFFF',accent='#FFE1D2',success='#2E6B45',error='#A8251A',secondaryH='#F1EBE1')
    night=dict(bg='#16130F',surface='#201C17',text='#F3EDE4',text2='#BFB5A8',border='#3A332B',borderS='#857A6D',primary='#FF8A66',primaryH='#FFA285',primaryP='#F07350',onP='#1B130E',accent='#4A2518',success='#86CFA0',error='#FF9285',secondaryH='#2B261F')
    for n,t in (('day',day),('night',night)):
        print(n)
        for fg in ('text','text2','primary','success','error'):
            print(' ',fg,[round(cr(t[fg],t[g]),2) for g in ('bg','surface','accent','secondaryH')])
        print('  onP on primary/H/P',[round(cr(t['onP'],t[k]),2) for k in ('primary','primaryH','primaryP')])
        print('  borderS on bg/surface',round(cr(t['borderS'],t['bg']),2),round(cr(t['borderS'],t['surface']),2))
        print('  text on accent', round(cr(t['text'],t['accent']),2))
