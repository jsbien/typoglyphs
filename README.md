# typoglyphs
## An inventory of glyphs used in some 16th century fonts of Polish printers

*Polonia Typographica Saeculi Sedecimi*, published between 1962 and
1981, contains 89 font tables. Scans of these tables have been split
into images of individual glyphs, which were used to create a
repository and reconstruct the tables in a *LuaLaTeX* document
(https://zenodo.org/records/14992305).

Typoglyphs are assigned identifiers with the table number, row number
and the glyph number.  Row 0 is reserved for additions for specific
tables, e.g. `t65_l00g01`.

More information is available in
https://tug.org/TUGboat/tb46-3/tb144bien-typoglyphs.html and
https://www.researchgate.net/publication/397770258.

A simple repository browser is available at
https://jsbien.github.io/typoglyphs/.

Clicking on the glyph ID displayes the metadata in the side panel. The
metadata consists of the content of the appropriate keywords file,
which always exists, and the appropriate description file, which exists
only for some glyphs.

Clicking on the glyph images switches the display to a special windows
with the glyph image which can be zoomed with the mouse
wheel. Clicking anywhere outside the scan returns to the standard
gallery windows.

You can filter the displayed typoglyphs by file names or their
fragments, e.g. `t63`,`t63_l03`,`t63_l03g28.png`, or the glyphs ID or
their fragments, e.g. `U2`, `U2-14`, `U2-14_0328`.

![Gallery screenshot](docs/gallery.png?raw=true "Gallery screenshot")

More sophisticated functions can be provided by the *geeqie* program or a
similar tool.

![Qeegie screenshot](geeqie/rubryka.png?raw=true "Qeegie screenshot")
