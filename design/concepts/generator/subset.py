from fontTools import subset
from fontTools.ttLib import TTFont
chars=open('chars.txt').read()+''.join(chr(i) for i in range(0x20,0x7f))+'，。、；：？！「」『』（）《》・—–…'
opt=subset.Options(); opt.flavor='woff2'; opt.layout_features=['*']; opt.name_IDs=['*']; opt.notdef_outline=True
f=TTFont('../fontsrc/jf-openhuninn-2.1.ttf'); s=subset.Subsetter(opt); s.populate(text=chars); s.subset(f)
f.flavor='woff2'; f.save('project/fonts/jf-openhuninn-2.1-subset.woff2')
