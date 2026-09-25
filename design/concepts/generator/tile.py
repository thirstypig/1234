import sys
from PIL import Image
src,out,seg=sys.argv[1],sys.argv[2],int(sys.argv[3])
im=Image.open(src); w,h=im.size
parts=[im.crop((0,y,w,min(h,y+seg))) for y in range(0,h,seg)]
if w>600:
    for i,p in enumerate(parts): p.save(out.replace('.png',f'_{i}.png'))
else:
    c=Image.new('RGB',(w*len(parts)+20*len(parts),seg),'white')
    for i,p in enumerate(parts): c.paste(p,(i*(w+20),0))
    c.save(out)
