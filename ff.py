# https://github.com/RobertWinslow/Simple-SVG-to-Font-with-Fontforge/blob/main/build_simple_black_font_with_fontforge.py
# Thanks Robert Winslow

import fontforge  # type: ignore
import os
import sys
import font_info as fi

testmode = 'testmode' in sys.argv

outDir = './fonts/'
if not os.path.isdir(outDir):
    os.makedirs(outDir)

mapping = {}
with open('mapping.txt') as fileName:
    content = fileName.read().strip()
    lines = content.splitlines()
    for line in lines:
        line = line.strip()
        if (len(line) == 0):
            continue
        [a, b] = line.split(' ', 1)
        mapping[b.lower()] = a

sourceDir = 'eps'
files = os.listdir(sourceDir)
codeTuples = []
for fileName in files:
    if (not fileName.endswith('.eps')):
        continue
    name = fileName[:-4].lower()
    if (name.endswith('_2')):
        continue
    if name in mapping:
        codePoint = mapping[name]
        codeTuples.append((codePoint, fileName))

rawAccOverride = {}
accuracyOverride = {}

for x in rawAccOverride:
    if x in mapping:
        accuracyOverride['u'+mapping[x]] = rawAccOverride[x]

variations = [x for x in fi.variations if x[0] == 'Regular'] if testmode else fi.variations

for (name, dWeight, italic, _) in variations:
    font = fontforge.font()
    font.familyname = fi.family
    font.fullname = f'{fi.family} {name}'

    def adjustFont():
        def getGlyph(key: str):
            return font['u'+mapping[key]]

        font.selection.all()
        font.autoWidth(140)
        font.selection.none()

        spaceChar = font.createChar(32, 'u0020')
        spaceChar.width = 350

        fancyChar = font.createChar(-1, 'fancy')
        fancyChar.importOutlines(
            f'{sourceDir}/fancy info.eps', correctdir=False, accuracy=0.0001, scale=False)

        muc = getGlyph('mucaad')
        dMuc = getGlyph('double mucaad')
        muc.left_side_bearing = \
            muc.right_side_bearing = \
            dMuc.left_side_bearing = \
            dMuc.right_side_bearing = 280
        
        if (italic):
            font.selection.all()
            font.italicize()

        featureTuple = (('kern', (('DFLT', ('dflt')),)),)
        # featureTuple = (('kern', (('latn', ('dflt')),)),)
        # featureTuple = (('kern', (('olck', ('dflt')),)),)
        font.addLookup('kernLookup', 'gpos_pair', None, featureTuple)
        font.addLookupSubtable('kernLookup', 'kernSub')

        def kern(a, b, kern):
            a = getGlyph(a)
            b = getGlyph(b)
            a.addPosSub('kernSub', b.glyphname, kern)

        # Round stuff then ir
        for x in ('la', 'at', 'ag', 'al', 'laa', 'aak', 'aaj', 'aaw', 'is', 'ir', 'lu', 'ep', 'en', 'ott', 'oh', 'ahad', 'gaahlaa ttuddaag', 'mu-gaahlaa ttuddaag'):
            kern(x, 'ir', -40)

        # Round then round
        kern('laa', 'uy', 10)

        # (Round or straight) then line
        for x in ('la', 'at', 'ag', 'al', 'laa', 'aak', 'aaj', 'aam', 'aaw', 'li', 'ih', 'iny', 'ir', 'lu', 'unn', 'edd', 'en', 'err', 'lo', 'ott', 'ob', 'oh', 'ahad'):
            for y in ('al', 'aak', 'aaj', 'is', 'ott', 'lu'):
                kern(x, y, 40)
        
        # aak, en
        # aak, edd
        # li, en
        # ??, en
        # ??, ir

        # Not categorized yet
        kern('laa', 'ud', 40)
        kern('la', 'ud', 40)
        kern('ir', 'ud', 40)
    

    def importAndCleanOutlines(outlinefile, glyph):
        # print(outlinefile)
        glyphName = glyph.glyphname
        accuracy = accuracyOverride[glyphName] if glyphName in accuracyOverride else 0.25
        glyph.importOutlines(outlinefile, correctdir=False,
                            accuracy=accuracy, scale=False)

        glyph.addExtrema()
        glyph.simplify()
        glyph.round()

        if (testmode):
            # glyph.changeWeight(-4, 'CJK', 1, 0, 'squish', 1)
            # glyph.changeWeight(-17, 'CJK', 1, 0, 'squish', 1)
            # glyph.changeWeight(-5, 'auto', 1, 0, 'squish', 1)
            pass

        if (not dWeight == 0):
            glyph.changeWeight(dWeight, 'CJK', 1, 0, 'squish', 1)
        
        glyph.removeOverlap()

        SCALEFACTOR = 1.04
        foregroundlayer = glyph.foreground
        for contour in foregroundlayer:
            contour.transform((1, 0, 0, 1, 0, -200))
            contour.transform((SCALEFACTOR, 0, 0, SCALEFACTOR, 0, 0))
        glyph.setLayer(foregroundlayer, 'Fore')

        glyph.autoHint()

    for codePoint, fileName in codeTuples:
        char = font.createChar(int(codePoint, 16), f'u{codePoint}')
        importAndCleanOutlines(f'{sourceDir}/{fileName}', char)

    adjustFont()

    print(f'Generating - {name} ...')
    font.generate(f'{outDir}/{fi.family} {name}.otf')
    font.close()

# nodemon -e eps,py --exec "ffpython ff.py testmode"
# ffpython ff.py && python finalize.py
