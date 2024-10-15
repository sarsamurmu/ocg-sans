family = 'OCG Sans'

variations = [
    ('Extra Light', -32.2, 0, 200),
    ('Light', -14, 0, 300),
    ('Regular', 0, 0, 400),
    ('Medium', 10.2, 0, 500),
    ('Bold', 25, 0, 700),
    ('Extra Bold', 38.3, 0, 800),
]

italics = []

for variation in variations:
  itVar = list(variation)
  if (variation[0] == 'Regular'):
    itVar[0] = 'Italic'
  else:
    itVar[0] += ' Italic'
  itVar[2] = 1
  italics.append(tuple(itVar))

variations.extend(italics)
