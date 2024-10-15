# Ol Chiki Gaban Sans
An Ol Chiki font focusing on better legibility.

## How to build
Make sure you have FontForge and Python installed

- Use Affinity Designer to open the `glyphs.afdesign` file
- Export all artboards to `eps` directory
- Create a python virtual environment and activate it, then install all the dependencies
  ```cmd
  py -m venv .venv
  .venv\Scripts\activate
  python -m pip -r requirements.txt
  ```
- Run command to generate fonts
  ```cmd
  ffpython ff.py && python finalize.py
  ```
- Find the generated fonts:
  - `/fonts/`: Fonts built by fontforge
  - `/fonts/rounded/`: Fonts with their coordinates rounded to integer. Must compare with original fonts, beacause sometimes these font slightly deviate from original design

## How to preview while building
- Open [Live Server](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer) in VS Code
- Open `/preview/basic.html` for basic preview
- There are also other pages (like `/preview/kern.html`, ...) for different purposes
- In your browser, open DevTools. Go to `Network` tab, then check `Disable cache`, keep the devtools open while previewing
- Run this command
  ```bash
  # You would need NodeJS and nodemon installed for this to work
  nodemon -e eps,py --exec "ffpython ff.py testmode"
  ```
- Now the page will update with new font everytime you make changes to your design

## Why am I using such complex build steps instead of using any font designing program?
I could have just used FontLab, FontCreator, or maybe Glyphs. But I wanted to incorporate
all the programs that I already use to develop font, that would be more comfortable for me.
I personally think Affinity Designer has more features for designing than any other font
designing programs (except, maybe Glyphs), since it is a generic designing program. Also, there's more flexibility in using scripts, I could automate almost all aspects of font post-processing.

## License
This Font is licensed under the SIL Open Font License. See [LICENSE](./LICENSE.txt)
