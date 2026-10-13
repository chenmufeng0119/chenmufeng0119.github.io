---
layout: default
permalink: /cv/
title: CV
nav: true
nav_order: 6
cv_pdf: /assets/pdf/cv.pdf
cv_format: rendercv # options: rendercv, jsonresume
description: Curriculum vitae for Mufeng Chen, a Ph.D. student in Electrical and Computer Engineering at Purdue University.
toc:
  sidebar: left
---

<link rel="stylesheet" href="{{ '/assets/css/al-folio-cv.css' | relative_url | bust_file_cache }}" />

<style>
  #selected-publications + .card strong {
    font-weight: 700;
    text-decoration: underline;
  }
</style>

{% al_folio_cv_render %}
