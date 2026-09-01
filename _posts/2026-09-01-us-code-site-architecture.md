---
title: U.S. Code Site Architecture
subtitle: FastAPI Powering a Modern U.S. Code Website
author: Ari Hershowitz
date: 2026-09-01T12:15:00-07:00
tags:
  - API
  - FastAPI
  - law
  - legislation
  - Law Revision Counsel
  - US Code
  - Congress
  - technology
  - LLMs
  - Claude
  - Claude Code
  - AI
  - legaltech
  - uscode.house.gov
  - LII
  - Cornell Legal Information Institute
thumbnail-img: /assets/img/uploads/sample.jpg
cover-img: /assets/img/uploads/sample.png
---

My [previous post](https://blog.linkedlegislation.org/2026-08-20-the-secret-us-code-revealed/) introduced a proof-of-concept modern display for the United States Code, and five design principles that I propose for the official web publication of laws and regulations: hierarchical navigation, keyword and citation search, section-level display, history and text comparison (version management), copy and paste.\
\
This post describes the architectural choices that drive the new site, and how this architecture supports the design principles. My driving aim has been simplicity: modular design with clean, simple UI design. Achieving such simplicity requires more effort and more careful architecture than the kitchen-sink or bag-of-features approach. It's easy to list hundreds of features and just pile them on to the application. But that leads to a complex and interconnected UI that is unpleasant to navigate.\
\
In keeping with this goal of simplicity, I lay out the architectural principles here: 

1. **API-first** design using Python [FastAPI](https://fastapi.tiangolo.com/)
    1. The API follows the identifier structure for United States Legislative Markdown (USLM), derived originally from LegalDocML. An identifier at any level (title, chapter, section, subsection, paragraph...) resolves.
    2. FastAPI was chosen because of its speed, its automated generation of OpenAPI documentation and the FastAPI team's focus on simplicity, performance and innovation.
2. **Section** is the canonical unit of information
    1. All identifiers at the section level or below resolve to the section, highlighting the sub-section provision; identifiers above the section resolve to a table of contents (navigation hierarchy). 
    2. This reflects the way that Congress treats sections -- as a unit of law, that is (usually) self-contained with definitions and other metadata. This choice flows through to display and storage -- version control is *also* stored and managed at the section level. While sub-section changes can be tracked, they are in the context of the section. 
    3. Section-level focus also aligns with and is validated by the Office of Law Revision Counsel's Classification tables, which assign each new provision of law to a section and then collect historical notes at the section level.
3. Preserves and shows **change history**
    1. The change history for the U.S. Code is meticulously documented by the LRC in Historical Notes at the end of each section. With digital analysis, it is possible to complement that narrative history with data: which release points include changes: text changed by law (recorded in the Classification table; editorial changes, including citations changed by LRC to keep up with changes elsewhere in the law; metadata and XML structural changes. The data for these changes is documented in the site documentation (how many changes, across which sections, over what period of time).
    2. The automated "diff" of section version changes relies on deterministic text comparison algorithms, so that there is no chance of AI hallucination.
4. **No generative AI** on the site
    1. I used generative AI (mostly Claude Code with Fable or the latest Opus model) to *build* the site, but have been careful to avoid using it in the site itself. Search is built with OpenSearch and is processed locally using indices. My intention with this site is to demonstrate the boundaries I believe that an *official government* site should use when publishing the law. In that case, absolute accuracy and fidelty to the text of the law (and eventually regulations) is essential. The official data can be accessed by third parties, either through an official API (and ideally supported by the nascent cross-site storage protocol) or download, and new features can be explored on third-party sites. It is my belief that the official site should avoid generative AI, with its potential for hallucinations and incorrect publication, as part of the feature set of the site.
    2. I have gotten feedback recommending that I include a chatbot or a semantic search feature; my belief is that such features are best accomplished on third-party sites. Take this as my wholehearted invitation to you to build such a site, using this data. I've even created a [Hugging Face US Code data set](https://huggingface.co/datasets/dreamproit/uscode) to make this easy for you!
    3. If you read the documentation on the site, you'll find AI-generated text. I have gone through and edited most of it, so that it has gone through human review. In an ideal world, the official site will have human review of *all* text on the site. However, generative AI can build documentation much faster and more efficiently, and practical constraints would mean that much of this documentation would not get written or would be quickly out of date. Including AI documentation (and even analytical statistics, like how many sections of the code are included) is a conscious choice I've made, and I think reflects the balance of utility and full human-reviewed accuracy that we will increasingly face with legal and legislative work product. For now, I accept generative text for documentation, but not in the search or text comparison features of the site itself. That dividing line may change as LLM models become more powerful and there are better harnesses to ensure the determinitive output of such models.
5. **Open source** code, based on open source
    1. The code for this is open source, with a permissive MIT license. That will allow experimentation, public contributions, and importantly will allow Congress and the Law Revision Counsel to reuse this code -- not just the design and idea -- in future versions of uscode.house.gov.
    2. The components of this site are open source, including FastAPI and the display using the [Astro static web framework](https://astro.build/).
6. **Modular**
    1. The site consists of self-contained units -- both in the data processing pipeline and in the front-end display, which interact with each other according to well-defined APIs. The API-first design (principle 1) carries through to the component design, where underlying technologies may change, but the communication surface will stay relatively stable. This modularity will allow different government agencies (and members of the public) to re-use these components as needed (e.g. the Classification Tables dataset), without the overhead of the rest of the site.
7. **Accessible** and **responsive**
    1. Components were drawn from USWDS, to be accessible, and there are accessibility tests. This is a proof-of-concept site, and before putting it into official production, a much more thorough accessibility audit will need to be done to ensure maximum accessibility. The site itself, or third-party providers (hello Google?) can convert the text to speech or to sign language or ensure support for other readers.

Other design principles for the site are general to all web development, particularly generative AI-assisted coding: a robust test suite which ties directly to the documentation and features (the site documentation doubles as a UX test suite); automated CI/CD pipelines; containerization for easy transfer; DevOps as code -- deployment with well defined configurations, etc. For more details on the infrastructure, I invite you to consult the site documentation itself, including the [User Guide](https://uscode.linkedlegislation.org/app/guide); the [API documentation](https://uscode.linkedlegislation.org/app/docs) in three flavors: [Swagger UI](https://uscode.linkedlegislation.org/docs), [ReDoc](https://uscode.linkedlegislation.org/redoc), and [OpenAPI schema](https://uscode.linkedlegislation.org/openapi.json); and the developer documentation in the README.md at https://github.com/aih/uscode-redesign.\

## Call to Action

I've built this site as open source and published it live so that it will inspire. If you are reading this, I hope this inspires you to build with this data and this design; add issues to the repository, branch the code, think out of the box. What do you think I got wrong, what do you think could be done better?\
\
I also hope it will inspire Congress to **clean up the code**. My next blog post will be about Marie Kondo-ing the Code -- enacting bills to correct mistakes and "technical debt" in the US Code. And I hope to inspire LRC and other government agencies to collaborate on a standardized modernization of display of legislative and regulatory documents: congress.gov,  uscode.house.gov, regulations.gov and federalregister.gov all working from a compatible code base and with data standards  both in the XML (USLM) and in the APIs that connect them.
