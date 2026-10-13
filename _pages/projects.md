---
layout: page
title: projects
permalink: /projects/
description: Cross-layer heterogeneous memory systems for scalable AI and optimization workloads.
nav: true
nav_order: 3
---

<style>
  .research-projects {
    --project-border: var(--global-divider-color, #d8dee4);
    --project-surface: var(--global-bg-color, #fff);
  }

  .research-projects .research-overview {
    display: grid;
    grid-template-columns: minmax(0, 0.82fr) minmax(0, 1fr);
    align-items: center;
    gap: 1.5rem;
    margin-bottom: 1rem;
    padding: 1rem;
    border: 1px solid var(--project-border);
    border-radius: 0.75rem;
    background: var(--project-surface);
  }

  .research-projects .overview-figure {
    margin: 0;
  }

  .research-projects .overview-figure a {
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .research-projects .overview-figure img {
    display: block;
    width: 100%;
    max-height: 21rem;
    object-fit: contain;
  }

  .research-projects .overview-figure figcaption {
    margin-top: 0.45rem;
    font-size: 0.85rem;
  }

  .research-projects .overview-copy h2 {
    margin-top: 0;
    font-size: clamp(1.35rem, 2vw, 1.8rem);
    line-height: 1.25;
  }

  .research-projects .overview-copy ul {
    padding-left: 1.2rem;
  }

  .research-projects .overview-copy li + li {
    margin-top: 0.45rem;
  }

  .research-projects .overview-paper,
  .research-projects .gpu-feature,
  .research-projects .hbf-feature {
    display: flex;
    align-items: center;
    gap: 0.85rem;
    margin: 0.9rem 0 1.5rem;
    padding: 0.75rem 0.9rem;
    border: 1px solid var(--project-border);
    border-radius: 0.65rem;
    background: var(--project-surface);
  }

  .research-projects .overview-paper {
    flex-wrap: wrap;
  }

  .research-projects .overview-paper-label {
    flex: 0 0 auto;
    font-weight: 600;
  }

  .research-projects .overview-paper-title {
    flex: 1 1 18rem;
  }

  .research-projects .overview-paper-links {
    display: flex;
    flex: 0 0 auto;
    gap: 0.8rem;
  }

  .research-projects .gpu-feature {
    justify-content: space-between;
  }

  .research-projects .hbf-feature p {
    margin: 0;
  }

  .research-projects .gpu-feature h3,
  .research-projects .gpu-feature p {
    margin: 0;
  }

  .research-projects .gpu-feature h3 {
    margin-bottom: 0.25rem;
    font-size: 1.05rem;
  }

  .research-projects .gpu-actions {
    display: flex;
    flex: 0 0 auto;
    gap: 1rem;
  }

  .research-projects .cache-level {
    margin: 1.5rem 0 1.75rem;
  }

  .research-projects .section-kicker,
  .research-projects .project-kind {
    margin: 0 0 0.25rem;
    color: var(--global-text-color-light, #626c75);
    font-size: 0.8rem;
    font-weight: 600;
    letter-spacing: 0.02em;
    text-transform: uppercase;
  }

  .research-projects .cache-level h2,
  .research-projects .hbf-level h2,
  .research-projects .published-work h2 {
    margin-top: 0;
  }

  .research-projects .published-list {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    align-items: stretch;
    gap: 0.9rem;
    margin: 1rem 0 1.5rem;
  }

  .research-projects .published-row {
    display: flex;
    flex-direction: column;
    align-items: stretch;
    height: 100%;
    box-sizing: border-box;
    gap: 0.7rem;
    padding: 0.7rem;
    border: 1px solid var(--project-border);
    border-radius: 0.7rem;
    background: var(--project-surface);
  }

  .research-projects .published-row-wide {
    display: grid;
    grid-column: 1 / -1;
    grid-template-columns: minmax(0, 1.65fr) minmax(0, 1fr);
    align-items: center;
    height: auto;
    gap: 1rem;
  }

  .research-projects .published-image,
  .research-projects .published-image img {
    display: block;
    width: 100%;
    height: auto;
  }

  .research-projects .published-row:not(.published-row-wide) .published-image {
    display: grid;
    aspect-ratio: 412 / 477;
    place-items: center;
  }

  .research-projects .published-row h3,
  .research-projects .published-row p {
    margin: 0 0 0.45rem;
  }

  .research-projects .published-row h3 {
    font-size: 1.2rem;
  }

  .research-projects .published-copy {
    display: flex;
    flex: 1 1 auto;
    flex-direction: column;
    min-height: 0;
  }

  .research-projects .published-copy p {
    font-size: 0.95rem;
  }

  .research-projects .published-copy .project-link {
    margin-top: auto;
  }

  .research-projects .published-row-wide .published-copy {
    align-self: center;
  }

  .research-projects .publication-entry {
    display: flex;
    align-items: baseline;
    flex-wrap: wrap;
    gap: 0.4rem 0.8rem;
    margin: 0 0 1.5rem;
    padding: 0.75rem 0.9rem;
    border: 1px solid var(--project-border);
    border-radius: 0.65rem;
    background: var(--project-surface);
  }

  .research-projects .publication-entry .publication-title {
    flex: 1 1 20rem;
  }

  .research-projects .earlier-list {
    margin: 0 0 1.5rem;
    padding: 0;
    list-style: none;
    border-top: 1px solid var(--project-border);
  }

  .research-projects .earlier-list li {
    padding: 0.65rem 0;
    border-bottom: 1px solid var(--project-border);
  }

  @media (max-width: 760px) {
    .research-projects .research-overview {
      grid-template-columns: minmax(0, 1fr);
    }

    .research-projects .overview-figure img {
      max-height: 18rem;
    }

    .research-projects .published-list {
      grid-template-columns: minmax(0, 1fr);
    }

    .research-projects .published-row:not(.published-row-wide) .published-image {
      aspect-ratio: auto;
    }
  }

  @media (max-width: 520px) {
    .research-projects .published-row-wide {
      grid-template-columns: minmax(0, 1fr);
    }

    .research-projects .gpu-feature {
      align-items: flex-start;
      flex-direction: column;
    }
  }
</style>

<div class="research-projects">
  <section class="research-overview" id="research-overview" aria-labelledby="research-overview-title">
    <figure class="overview-figure">
      <a href="{{ '/assets/img/research/memory-compute-overview.png' | relative_url }}" target="_blank" rel="noopener">
        <img src="{{ '/assets/img/research/memory-compute-overview.png' | relative_url }}" alt="Research landscape overview connecting AI workloads, memory hierarchies, complementary memory technologies, and cross-layer design." loading="lazy" />
      </a>
      <figcaption>Research landscape overview: conceptual connections across processor/cache, domain-specific accelerator, and memory/storage levels.</figcaption>
    </figure>
    <div class="overview-copy">
      <h2 id="research-overview-title">Cross-Layer Heterogeneous Memory Systems for Scalable AI and Optimization Workloads</h2>
      <p>My research asks how memory systems can better serve AI and optimization workloads through complementary technologies and cross-layer design.</p>
      <p>My current focus is GPU and heterogeneous memory-system architecture for AI and LLM workloads.</p>
      <ul>
        <li>AI and optimization workloads can reshape memory-hierarchy requirements.</li>
        <li>Complementary memory technologies can support domain-specific accelerator designs.</li>
        <li>Workload, device, circuit, and system considerations interact, including noise, bandwidth, and thermal tradeoffs.</li>
      </ul>
    </div>
  </section>

{% assign gpu_project = site.projects | where: "category", "Cache Level" | first %}
{% if gpu_project %}
{% assign gpu_code_url = gpu_project.code_url | default: gpu_project.repo_url %}
<section class="cache-level" aria-labelledby="cache-level-title">
<p class="section-kicker">Architecture project</p>
<h2 id="cache-level-title">Cache Level</h2>
<div class="gpu-feature">
<div>
<h3><a href="{{ gpu_project.url | relative_url }}">{{ gpu_project.title }}</a></h3>
<p>{{ gpu_project.description }}</p>
</div>
<div class="gpu-actions">
{% if gpu_code_url %}<a href="{{ gpu_code_url }}" target="_blank" rel="noopener">Code ↗</a>{% endif %}
<a href="{{ gpu_project.url | relative_url }}">Details</a>
</div>
</div>
</section>
{% endif %}

{% assign accelerator_projects = site.projects | where: "category", "Domain-Specific Accelerators" | where_exp: "project", "project.project_type != 'publication'" | sort: "importance" %}
{% assign accelerator_publications = site.projects | where: "category", "Domain-Specific Accelerators" | where: "project_type", "publication" %}
  <section class="published-work" aria-labelledby="published-work-title">
    <p class="section-kicker">Published work</p>
    <h2 id="published-work-title">Domain-Specific Accelerators</h2>
    <div class="published-list">
      {% for project in accelerator_projects %}
        {% if project.img %}
          <article class="published-row{% if project.preview_layout == 'wide' %} published-row-wide{% endif %}">
            <a class="published-image" href="{{ project.url | relative_url }}" aria-label="Read {{ project.title }} project">
              <img src="{{ project.img | relative_url }}" alt="{{ project.title }} publication preview" loading="lazy" />
            </a>
            <div class="published-copy">
              <h3><a href="{{ project.url | relative_url }}">{{ project.title }}</a></h3>
              <p>{{ project.description }}</p>
              <a class="project-link" href="{{ project.url | relative_url }}">Project details</a>
            </div>
          </article>
        {% endif %}
      {% endfor %}
    </div>
    {% for paper in accelerator_publications %}
      <div class="publication-entry">
        <a class="publication-title" href="https://ieeexplore.ieee.org/document/11534674">{{ paper.title }}</a>
        <span>ISQED 2026</span>
        <span><a href="https://ieeexplore.ieee.org/document/11534674">Publication</a> · <a href="{{ '/assets/pdf/isqed26-heterogeneous-cim.pdf' | relative_url }}">PDF</a></span>
      </div>
    {% endfor %}
  </section>

  <section class="hbf-level" aria-labelledby="hbf-level-title">
    <p class="section-kicker">In progress</p>
    <h2 id="hbf-level-title">Main/Storage-Class Memory Level</h2>
    <div class="hbf-feature">
      <p>Exploring high-bandwidth flash within heterogeneous memory systems for GPU-based AI and LLM workloads.</p>
    </div>
  </section>

{% assign earlier_projects = site.projects | where: "category", "Earlier Research" | where_exp: "project", "project.show_in_projects != false" | where_exp: "project", "project.title != 'Hyperdimensional computing'" | sort: "importance" %}
  <section class="earlier-work" aria-labelledby="earlier-work-title">
    <h2 id="earlier-work-title">Earlier research</h2>
    <ul class="earlier-list">
      {% for project in earlier_projects %}
        <li><a href="{{ project.url | relative_url }}">{{ project.title }}</a> — {{ project.description }}</li>
      {% endfor %}
    </ul>
  </section>
</div>
