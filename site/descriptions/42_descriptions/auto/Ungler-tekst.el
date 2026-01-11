;; -*- lexical-binding: t; -*-

(TeX-add-style-hook
 "Ungler-tekst"
 (lambda ()
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "href")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "nolinkurl")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperbaseurl")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperimage")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperref")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "path")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "url")
   (add-to-list 'LaTeX-verbatim-macros-with-delims-local "path")
   (LaTeX-add-labels
    "sec:majuskuy"
    "fig:Ungler1_pismo01_A"
    "fig:Ungler1_pismo01_B"
    "fig:Ungler1_pismo01_C"
    "fig:Ungler1_pismo01_D"
    "fig:Ungler1_pismo01_E"
    "fig:Ungler1_pismo01_H"
    "fig:Ungler1_pismo01_I"
    "fig:Ungler1_pismo01_L"
    "fig:Ungler1_pismo01_M"
    "fig:Ungler1_pismo01_N"
    "fig:Ungler1_pismo01_O"
    "fig:Ungler1_pismo01_P"
    "fig:Ungler1_pismo01_Q"
    "fig:Ungler1_pismo01_R"
    "fig:Ungler1_pismo01_S"
    "fig:Ungler1_pismo01_T"
    "fig:Ungler1_pismo01_U"
    "sec:minuskuy"
    "fig:Ungler1_pismo01_amacron"
    "fig:Ungler1_pismo01_bx"
    "fig:Ungler1_pismo01_dd"
    "fig:Ungler1_pismo01_emacron"
    "fig:Ungler1_pismo01_f"
    "fig:Ungler1_pismo01_h"
    "fig:Ungler1_pismo01_Rh"
    "fig:Ungler1_pismo01_i-"
    "fig:Ungler1_pismo01_i_"
    "fig:Ungler1_pismo01_ij"
    "fig:Ungler1_pismo01_Rl"
    "fig:Ungler1_pismo01_mmacron"
    "fig:Ungler1_pismo01_nmacron"
    "fig:Ungler1_pismo01_Rn"
    "fig:Ungler1_pismo01_omacron"
    "fig:Ungler1_pismo01_p_"
    "fig:Ungler1_pismo01_pf"
    "fig:Ungler1_pismo01_q_"
    "fig:Ungler1_pismo01_qku"
    "fig:Ungler1_pismo01_qet"
    "fig:Ungler1_pismo01_qetd"
    "fig:Ungler1_pismo01_sed"
    "fig:Ungler1_pismo01_sub"
    "fig:Ungler1_pismo01_con"
    "fig:Ungler1_pismo01_et"
    "sec:inne-znaki"
    "fig:Ungler1_pismo01_rum"))
 :latex)

