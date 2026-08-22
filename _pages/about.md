---
layout: about
title: about
permalink: /
subtitle: Memory-centric architecture and circuits. Ph.D. student, <a href='https://engineering.purdue.edu/ECE'>ECE</a>, Purdue University &middot; <a href='https://engineering.purdue.edu/NanoX/'>NanoX Lab</a>.

profile:
  align: right
  image: prof_pic.png
  image_circular: false
  more_info: >
    <p>West Lafayette, IN, USA</p>
    <p>chen5240 [at] purdue.edu</p>

selected_papers: true
social: true

announcements:
  enabled: true
  scrollable: true
  limit: 5

latest_posts:
  enabled: false
  scrollable: true
  limit: 3
---

I am a Ph.D. student in Electrical and Computer Engineering at **Purdue University**, advised by Prof. [Haitong Li](https://engineering.purdue.edu/NanoX/) in the NanoX Lab. I work on **memory-centric computer architecture and circuits** — building memory that does more than store, and rethinking the hierarchy around it once it does.

My work runs along two threads.

#### Analog hybrid memory systems

Single-technology memory forces a hard trade-off between density, endurance, and retention. I design **mixed-signal macros that fuse complementary technologies into one array** — eDRAM for fast decoupled read/write, RRAM for non-volatile density, and BEOL oxide-semiconductor FETs for retention — so that the trade-off becomes a design knob rather than a constraint.

The circuits only matter if the algorithms above them change too, so this thread is co-designed with the workload: RRAM-assisted multi-level programming paired with zeroth-order optimization for on-device LLM fine-tuning, floating-point dataflows that avoid alignment-induced accuracy loss, and hyperdimensional / vector-symbolic representations that make on-chip learning cheap.

#### HBF + X

I work on **High-Bandwidth Flash (HBF)** — NAND capacity inside the package at HBM-like bandwidth, a new tier in the hierarchy rather than a faster SSD. Three questions interest me: what the HBF–accelerator interface should expose, which state belongs in flash, and how the tier is shared across accelerators. The **X** is the base die: real silicon, one level further down, where this thread meets the first one.

Before Purdue, at **Zhejiang University** I led the RRAM-eDRAM hybrid CiM design group under Prof. Er-Ping Li, covering SNN-based vision models, system-level specification, parts of the digital design, and the heterogeneous-integration issues that come with fused memory. I interned at [SIMS Lab](https://vlsi.rice.edu/) (Prof. Kaiyuan Yang, Rice) in summer 2022 on charge-domain CiM, and at [NanoX Lab](https://engineering.purdue.edu/NanoX/) (Prof. Haitong Li, Purdue) in summer 2023 on hyperdimensional computing.

I received my B.S. from the Department of Optics and Electronic Engineering at **Huazhong University of Science and Technology**, where I worked on silicon photonics, machine learning, and inverse design.
