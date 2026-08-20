---
title: The Secret US Code Revealed
subtitle: A Natural Web Reader for US Law
author: Ari Hershowitz
date: 2026-08-20T12:10:00-07:00
tags:
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
thumbnail-img: /assets/img/uploads/codeofhammurabi.jpg
cover-img: /assets/img/uploads/hammurabi-uscode-linkedlegislation-montage-1-.png
---
From the Code of Hammurabi to the United States Code, statutory law is naturally built for web display. And yet until today no web site has done true justice to the law.  Tl;dr, compare for yourself, the official site for the United States Code ([uscode.house.gov](uscode.house.gov)) and my new unofficial reconception and proof of concept at [uscode.linkedlegislation.org](uscode.linkedlegislation.org). The site is open source (MIT license) and it is my hope that the concept, if not the software code itself, will serve as inspiration for the next official version of the Law Revision Counsel's U.S. Code site.

This post will cover the principles I followed in creating this site. Let me know if you think there are principles I missed or mangled, and whether the new site fulfills or flubs these principles. A subsequent post will discuss **how I built it** (Claude Code) and **how to ensure its accuracy** (textual validation using hashes).

## Web of Law

Law is highly structured (titles, chapters, sections, subsections, paragraphs, clauses), has internal and external references (the original hyperlink), and consists of plain text. Reading the law requires no images, SVG, streaming, polling or any of the complications that have accrued over years to transform web browsers into powerful engines for digital applications. The text includes definitions and indices, and responsive -- it displays in neat columns and rows on a tablet.

It has been a deep and longstanding frustration for me that this natural structure has not been reflected in the official publications of law. We've come a long way from the display of single, large pdfs for some law (c.f. the U.S. statutes at large -- another worthy digitization project), and some jurisdictions (shout out to [legislation.gov.uk](legislation.gov.uk)), but for the most part, public law is still stuck in the 1990s. 

Here, I'll lay out the top principles for effective and reader-friendly web display of the law, and I hope you can see those reflected in the new site:

1. **Hierarchical navigation.** the structure of the law should be navigable and it should be easy to jump up (from section to chapter), down (from title to section) and across (next and previous sections) the hierarchy. The Law Revision Counsel has invested years of deep expertise in creating this hierarchy; a great deal of information is stored in the hierarchy and proximity, and this becomes accessible with a good table of contents and sensible breadcrumb in the display. Note the table of contents on the left side of each section display, as well as the breadcrumbs at the top and bottom.
2. **Keyword and citation search accessible anywhere**. A researcher needs to be able to survey the entire Code at once (where is this concept found) and from that initial search, to ***sort*** by relevance, location and recency; ***filter*** by *location* (I want "resource" in the context of Title 16 - Conservation, not Title 26 - Taxes) and *status* (current, repealed, omitted).
3. **Section-level display.** The U.S. Code, and much statutory and regulatory law, is anchored at the section level. The legal concept is embodied by the section and amendments, classification and history are all stored at the section level. This is the organizational principle that the Law Revision Counsel implements, and it should be reflected by the web display. The section-level display in this new site is, if I must say so myself, beautiful. See, e.g. [§ 51501. Establishment of Office of Spaceports](https://uscode.linkedlegislation.org/app/us/usc/t51/s51501?release=119-83).
4. **History and text comparison**. The law evolves, and one of the most challenging tasks for any legal researcher is to know **what the law is today** and **how it compares** to the law at any particular point in time. This is a technically fraught subject, as I discussed in my 2019 Github Satellite talk on [Version Control and the Law](https://www.youtube.com/watch?v=SmLpJEZyvI0). The published record, in the form of **release points** for the U.S. Code, provide an incomplete history of the text of the law. This is supplemented by the meticulous notes prepared by the Law Revision Counsel (see, e.g. the [notes on the section on income tax rates](https://uscode.linkedlegislation.org/app/us/usc/t26/s1401?release=119-83#section-notes), including both rate tables and each historical change). The new site, makes it easy to navigate to the notes, to know each historical release point where the section was changed, to navigate to that release point and **to compare the text between any two versions**. This still leaves a small gap that release points don't incorporate each change of each law, one at a time. So in the cases where multiple laws in a release point change the same section, there is no data record of the granular changes. These can be reconstructed with the notes and consulting the Classification tables.
5. **Copy and paste**. One of the most important and powerful functions of electronic data is the ability to copy and paste. I often say that I went from law to legal technology because there was not good way to copy and paste legal text with properly formatted citations. This new site provides a number of text copy options (just text, text + citation, hyperlink) and places a copy button next to each provision at each hierarchical level. This is public law with a public copy right, so copy away!

That's it. While implementation isn't trivial, the display principles are not actually that sophisticated or complex. Yet consult other examples of legal text display across the web and you'll see where they fall short. This version can also continue to evolve, but I think it hits the key pain points that have plagued most web law displays.
