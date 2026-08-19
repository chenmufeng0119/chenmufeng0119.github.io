---
title: "CENTAUR: A 38.5-TFLOPS/W 600MHz Floating-Point Digital Compute-In-Memory Engine with 40nm Fusion RRAM-eDRAM Macros Featuring 3D-MAC Operation"
collection: publications
permalink: /publication/CENTAUR
excerpt: 'A floating-point digital CIM engine built on fused RRAM-eDRAM macros with a 3D-MAC dataflow that removes alignment-induced accuracy loss.'
date: 2025-11-01
venue: 'IEEE Asian Solid-State Circuits Conference (A-SSCC)'
paperurl: 'https://ieeexplore.ieee.org/document/11349414'
citation: 'L. Zheng, A. M. Bavani, S. Du, T.-Y. Hsin, M. Chen, W.-S. Khwa, A. Lele, H. Chuang, Y.-D. Chih, M.-F. Chang and H. Li, "CENTAUR: A 38.5-TFLOPS/W 600MHz Floating-Point Digital Compute-In-Memory Engine with 40nm Fusion RRAM-eDRAM Macros Featuring 3D-MAC Operation," 2025 IEEE Asian Solid-State Circuits Conference (A-SSCC), 2025.'
---
Abstract: Existing NVM-based floating-point CIM macros face three major challenges: significant area and energy overhead from on-chip integer/FP conversion or large pre-alignment logic, accuracy degradation from architectural limitations such as row-wise pre-alignment of weights, and limited operating frequency constrained by slow NVM sensing. CENTAUR is a floating-point CIM engine featuring RRAM-eDRAM fusion macros and a novel FP 3D-MAC dataflow that eliminates non-computational (alignment-induced) accuracy loss, reduces area overhead, and enables high-speed, energy-efficient FP computation. Fabricated in 40 nm CMOS with foundry RRAM and validated on a full-stack testing platform, CENTAUR achieves 600 MHz operating frequency and 38.5 TFLOPS/W energy efficiency, running Tiny-ViT on CIFAR-10 with only 1.75% accuracy degradation versus the software baseline.

[Download paper here](/files/asscc25-centaur.pdf)
