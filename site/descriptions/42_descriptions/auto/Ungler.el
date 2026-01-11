;; -*- lexical-binding: t; -*-

(TeX-add-style-hook
 "Ungler"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-class-options
                     '(("mwart" "withmarginpar" "12pt")))
   (TeX-add-to-alist 'LaTeX-provided-package-options
                     '(("geometry" "a4paper" "margin=1.5cm") ("fontspec" "") ("polyglossia" "") ("csquotes" "") ("metalogo" "") ("xcolor" "") ("relsize" "") ("graphicx" "") ("url" "") ("setspace" "doublespacing") ("xfrac" "")))
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "url")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "path")
   (add-to-list 'LaTeX-verbatim-macros-with-delims-local "url")
   (add-to-list 'LaTeX-verbatim-macros-with-delims-local "path")
   (TeX-run-style-hooks
    "latex2e"
    "U"
    "mwart"
    "mwart12"
    "geometry"
    "fontspec"
    "polyglossia"
    "csquotes"
    "metalogo"
    "xcolor"
    "relsize"
    "graphicx"
    "url"
    "setspace"
    "xfrac")
   (TeX-add-symbols
    '("mcode" 1)
    '("mname" 1)
    '("acode" 1)
    '("aname" 1)
    '("usi" 1)
    '("ucode" 1)
    '("uname" 1)
    '("fname" 1)
    '("pname" 1)
    '("Ju" 1)
    '("Sy" 1)
    '("J" 1)
    "autocite"
    "vref"
    "Hb"
    "Htest"
    "apostrof")
   (LaTeX-add-fontspec-newfontcmds
    "JX"
    "bJ"
    "znak"
    "bS")
   (LaTeX-add-polyglossia-langs
    '("polish" "mainlanguage" "")
    '("english" "otherlanguage" "")))
 :latex)

