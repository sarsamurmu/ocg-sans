from pathlib import Path
import os
from defcon import Font
import ufo2ft
import extractor
import font_info as fi

cssFaces = []
rCssFaces = []
names = []
weightMap = {
    200: 2,
    300: 3,
    400: 5,
    500: 6,
    600: 7,
    700: 8,
    800: 9
}


dirsToMake = ('./fonts/rounded/', './generated/')
for dir in dirsToMake:
    if not os.path.isdir(dir):
        os.makedirs(dir)

for (name, _, italic, weight) in fi.variations:
    ufo = Font()
    extractor.extractUFO(f'./fonts/{fi.family} {name}.otf', ufo, doInfo=False)

    # https://robofont.com/documentation/tutorials/setting-font-names/
    info = ufo.info
    info.familyName = f'{fi.family}'
    info.styleName = name
    info.styleMapFamilyName = f'{fi.family} {name}'
    info.styleMapStyleName = 'italic' if italic else 'regular'
    versionMajor = 1
    versionMinor = 0
    info.versionMajor = versionMajor
    info.versionMinor = versionMinor
    info.year = 2024
    info.copyright = 'Copyright (c) 2024 Sarsa Murmu'
    # info.note = ''

    info.openTypeNameDesigner = 'Sarsa Murmu'
    info.openTypeNameDesignerURL = 'https://sarsamurmu.github.io'
    info.openTypeNameManufacturer = 'Sarsa Murmu'
    info.openTypeNameManufacturerURL = 'https://sarsamurmu.github.io'
    info.openTypeNameLicense = 'This Font Software is licensed under the SIL Open Font License, Version 1.1. This license is available with a FAQ at: http://scripts.sil.org/OFL'
    info.openTypeNameLicenseURL = 'http://scripts.sil.org/OFL'
    info.openTypeNameVersion = f'Version {versionMajor}.{versionMinor}'
    # info.openTypeNameUniqueID
    # info.openTypeNameDescription
    info.openTypeNamePreferredFamilyName = info.familyName
    info.openTypeNamePreferredSubfamilyName = info.styleName

    info.openTypeOS2WeightClass = weight
    info.openTypeOS2Panose = [2, 2, weightMap[weight] or 1, 3, 4, 2, 2, 5, 2, 3]
    info.openTypeOS2Type = [0]

    info.postscriptFontName = f"{fi.family}-{name}".replace(' ', '-')
    info.postscriptFullName = info.postscriptFontName

    if (italic):
        info.italicAngle = -15

    otf = ufo2ft.compileOTF(ufo, removeOverlaps=False, roundTolerance=0)
    outputPath = f'./fonts/{fi.family} {name}.otf'
    otf.save(outputPath)
    rOtf = ufo2ft.compileOTF(ufo, removeOverlaps=False)
    rOtf.save(f'./fonts/rounded/{fi.family} {name}.otf')

    fontName = f'{fi.family} {name}'

    baseCssFace = f"""
@font-face {{
  font-family: '{fontName}';
  src: url('/{outputPath}');
  font-weight: {weight};
  font-style: {'italic' if italic else 'normal'};
}}
"""

    cssFaces.append(baseCssFace)
    rCssFaces.append(baseCssFace
                     .replace('/fonts/', '/fonts/rounded/')
                     .replace(f"'{fontName}'", f"'{fontName} R'"))
    names.append(f'"{fontName}"')

dir = Path(os.path.dirname(os.path.realpath(__file__)))
(dir / './generated/fonts.css').write_text(''.join(cssFaces).strip())
(dir / './generated/fonts_rounded.css').write_text(''.join(rCssFaces).strip())
(dir / './generated/fonts.json').write_text(f'[{", ".join(names)}]')
