---
layout: page
title: Posters
permalink: /posters/
description: Research posters by Mufeng Chen.
nav: true
nav_order: 4
---

<style>
  .research-poster {
    display: grid;
    grid-template-columns: minmax(180px, 0.8fr) minmax(0, 1.5fr);
    align-items: center;
    gap: 1.5rem;
    padding: 1rem;
    border: 1px solid var(--global-divider-color, #d8dee4);
    border-radius: 0.75rem;
  }

  .research-poster + .research-poster {
    margin-top: 1rem;
  }

  .research-poster img {
    display: block;
    width: 100%;
    max-height: 24rem;
    object-fit: contain;
  }

  .research-poster h2 {
    margin-top: 0;
    font-size: clamp(1.25rem, 2vw, 1.65rem);
    line-height: 1.3;
  }

  @media (max-width: 650px) {
    .research-poster {
      grid-template-columns: minmax(0, 1fr);
    }

    .research-poster img {
      max-height: 20rem;
    }
  }
</style>

<article class="research-poster">
  <a href="/assets/img/posters/cross-layer-memory-systems-poster.png" target="_blank" rel="noopener">
    <img src="/assets/img/posters/cross-layer-memory-systems-poster.png" alt="Cross-Layer Heterogeneous Memory Systems for Scalable AI and Optimization Workloads research poster" />
  </a>
  <div>
    <p><strong>Research poster</strong></p>
    <h2>Cross-Layer Heterogeneous Memory Systems for Scalable AI and Optimization Workloads</h2>
    <p>Mufeng Chen · Purdue University · Advisor: Prof. Haitong Li.</p>
    <p>This work connects AI workloads, memory systems, and compute-in-memory.</p>
    <p><a href="/assets/img/posters/cross-layer-memory-systems-poster.png" target="_blank" rel="noopener">View full-size PNG</a> · <a href="/assets/pdf/cross-layer-memory-systems-poster.pdf" download>Download PDF</a></p>
  </div>
</article>

<article class="research-poster">
  <a href="/assets/img/posters/mtj-cim-ising-poster.png" target="_blank" rel="noopener">
    <img src="/assets/img/posters/mtj-cim-ising-poster.png" alt="BEOL-Compatible Stochastic MTJ-CIM for DAC-less Ising Machine research poster" />
  </a>
  <div>
    <p><strong>Research poster</strong></p>
    <h2>BEOL-Compatible Stochastic MTJ-CIM for DAC-less Ising Machine</h2>
    <p>Authors: Mufeng Chen, Xuejian Zhang, Joerg Appenzeller, and Haitong Li.</p>
    <p><a href="/assets/img/posters/mtj-cim-ising-poster.png" target="_blank" rel="noopener">View full-size PNG</a> · <a href="/assets/pdf/mtj-cim-ising-poster.pdf" download>Download PDF</a></p>
  </div>
</article>
