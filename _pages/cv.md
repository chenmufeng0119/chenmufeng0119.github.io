---
layout: archive
title: "CV"
permalink: /cv/
author_profile: true
redirect_from:
  - /resume
---

{% include base_path %}

A PDF version of this CV is available [here](/files/cv.pdf).

Education
======
* **Ph.D. in Electrical and Computer Engineering**, Purdue University, 2024 - present
  * Advisor: Prof. Haitong Li (NanoX Lab)
  * Focus: fused analog compute-in-memory, neuro-symbolic computing
* **B.S. in Optics and Electronic Engineering**, Huazhong University of Science and Technology, 2017 - 2021

Research experience
======
* **2024 - present: Graduate Research Assistant**, Purdue University
  * NanoX Lab, advised by Prof. Haitong Li
  * Fused analog eDRAM-RRAM CiM macros; zeroth-order on-device LLM fine-tuning; neuro-symbolic algorithm design

* **2021 - 2024: Research Assistant**, Zhejiang University
  * RFNE Research Center, advised by Prof. Er-Ping Li
  * Group leader for RRAM-eDRAM hybrid CiM; SNN-based vision models; system-level spec and heterogeneous integration

* **Summer 2023: Research Assistant**, Purdue University
  * Advised by Prof. Haitong Li
  * Monolithic 3D-RRAM CiM; hyperdimensional computing for vision transformers

* **Summer 2022: Research Assistant**, Rice University
  * SIMS Lab, advised by Prof. Kaiyuan Yang
  * Charge-domain SRAM-CiM for Bayesian neural networks

* **Summer 2019: Research Assistant**, Wuhan National Laboratory for Optoelectronics
  * Advised by Prof. Chen Lin
  * Optical metasurface design (achromatic metalenses)

Skills
======
* **Circuit / EDA:** Cadence Virtuoso, Synopsys VCS, Design Compiler, Innovus
* **Programming:** Python (PyTorch), C/C++, MATLAB, Verilog/SystemVerilog
* **Research areas:** compute-in-memory, mixed-signal CMOS+X design, spiking neural networks, hyperdimensional computing, neuro-symbolic AI

Publications
======
  <ul>{% for post in site.publications reversed %}
    {% include archive-single-cv.html %}
  {% endfor %}</ul>
  
Projects
======
  <ul>{% for post in site.projects reversed %}
    {% include archive-single-talk-cv.html %}
  {% endfor %}</ul>

Transcripts
======
* B.S. transcript [here](/files/B.S.Transcript.pdf)
* M.S. transcript [here](/files/M.S.Transcript.pdf)
