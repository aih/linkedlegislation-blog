---
title: A Clean Slate for the Law
subtitle: Squashing Bugs and Cleaning the U.S. Code
author: Ari Hershowitz
date: 2026-11-16T12:13:00-08:00
tags:
  - law
  - legislation
  - Law Revision Counsel
  - US Code
  - Congress
  - technology
  - legaltech
  - uscode.house.gov
  - uscode.linkedlegislation.org
  - codification.linkedlegislation.org
thumbnail-img: /assets/img/uploads/Gemini_Generated_Image_xr5yugxr5yugxr5y.jpeg
cover-img: /assets/img/uploads/Gemini_Generated_Image_53vq9353vq9353vq.jpeg
---

## A Clean Slate

The new congress taking office in January 2027 has a once-in-a-century opportunity to start with a clean slate. It has taken more than 100 years to organize half of U.S. law into official titles of the United States Code (positive law). In what I believe is the **best use of AI for law**, Congress can pass all remaining titles of U.S. law in a single Congress.

The Office of Law Revision Counsel has written [five codification bills](https://uscode.house.gov/codification/legislation.html) and is working on four more. However, Congress has not prioritized passing them. Working with Anthropic's latest foundational model, Fable 5.2, I have built a **bill reader** to make it easier to review these codification bills, as well as a **suite of analysis tools** (e.g. confirming citations, checking all words in enacted laws against the words in the codified titles, etc.) to perform Quality Assurance on any codification bill, and have directed agents to **draft all remaining codification bills** in waves of increasing complexity. In total, 21 draft codification bills are ready for analysis, human review, correction and enactment.


The human effort involved in reviewing and validating these codification bills will not be trivial. But AI has **taken a 100-year effort and condensed it to a few weeks**. The review phase could take a few months of focused effort by a few dozen legislative drafting experts, working with software engineers. While codification involves editorial judgement, much of the work involves tedious checking of citations (e.g. find all references to the old section and change them to refer to the new codified section). All of this can be done in seconds with AI and validated deterministically with software querying digital law databases.


Which of the legislators joining the 120th Congress is willing to invest their new mandate into a bipartisan effort to clean up the law?

## Background

The process of making laws in a democracy is famously messy. As a [19th century U.S. lawyer](https://freakonomics.com/2009/03/our-daily-bleg-uncovering-more-quote-authors/) noted, "laws, like sausages, cease to inspire respect in proportion as we know how they are made." And at least one U.S. sausage maker (a former political scientist) has objected that [this comparison unfairly prejudices](https://www.nytimes.com/2010/12/05/weekinreview/05pear.html) sausage factories.

The problem for governing is that the mess remains -- and actually worsens -- after laws are enacted. Our laws are written as standalone acts that amend previous acts, which themselves amend the acts before them, creating a complex network of redlines worse than any contract you've seen in Microsoft Word.

It's a problem I've railed against in previous posts and on LinkedIn. The solution is relatively straightforward: positive law codification.

The Office of Law Revision Counsel (LRC) maintains the United States Code, an orderly set of 54 Titles of U.S. federal law. However, only about half of them are officially enacted as law. The remaining Titles show how the law _could_ be reorganized out of hundreds of underlying standalone Acts, but Congress has not passed these titles as-is.

The mess persists even though the Law Revision Counsel [has prepared “clean-up” bills](https://uscode.house.gov/editorialreclassification/BillsToUpdateStatutoryReferences/index.html) that correct the citations in various laws and U.S. Code sections to point to the correct authority. These are the equivalent of “bug fixes” to correct errors that plague U.S. law and make it more difficult to automate legal analysis. As noted above, LRC has also prepared a number of “[positive law codification](https://uscode.house.gov/codification/legislation.html)” bills, that would bring more of U.S. law into an orderly, codified form. However, each Congress, most of the codification bills are not taken up for a vote, and the next congress has to start over. This is the ultimate legislative sisyphean task. A careful and strategic use of AI, combined with some political will, can finally get the boulder up Capitol Hill.
