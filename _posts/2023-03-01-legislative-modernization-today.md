---
published: false
---
## Legislative Modernization: Where we are today

I’ve done a lot of thinking about the original sources of U.S. federal law. And I’m fortunate to work with the people who draft, amend, organize, and analyze the law. Much of the law has been published in fragments distributed across paper volumes and across various federal websites. Today I believe we are just a few steps from joining those fragments into an offial, online, citeable public framework of law.

This post will summarize the progress that has been made in modernizing the digital publication of law: in solving three key problems of digitization (citations, version control and cloud deployment) and in connecting three key sources of federal law (bills, U.S. Code, Statute Compilations). I plan to write separate posts to further explore of each of those areas. The topic of regulations deserves its own treatment.

Much of the progress I will describe is due to the collaboration between some very dedicated people across many government organizations. The nature of our federal system is that different organizations are responsible for each of the sources of federal law: bills, statutes and the United States Code are each managed by independent entities. Some of what I discuss here can be found in various earlier forms on this blog. This is an attempt to update the information and identify the remaining challenges.

### Citations as URL

An essential component of laws is the ability to cite a portion of law with some precision. Legislative citations typically cite a level in a hierarchical structure (Section 401(c) of Title 26 of the United States Code or 26 U.S.C.401(c)). Digital citations refer to a URL. Modernization of law begins with creating a one-to-one relationship between the structure of a traditional citation and a URL: 26 U.S.C. 401(c) becomes `/us/usc/t26/s401/c`. (We can quibble in the comments about the differences between a URL and URI.)

Each of the three sources of federal law I describe below is now published as downloadable files in United States Legislative Markup (USLM), a standardized XML format that includes digital citations for each portion of the text, or provision. 

### Version Control

“Just put laws into git” is a familiar refrain for anyone who has been working with digital law for a while. I gave a presentation at a Github conference about why solving the problem is both not that simple, but also not impossibly complex. In fact, my colleague Sela Mador-Haim has built an XML database, XCiteDB, that manages versions of every level of XML, and also tracks metadata about each level in a data-friendly format (JSON). This database is now being used by the House of Representatives to manage versions of the law as part of the Comparative Suite tools. The version control is essential to be able to ask the question—how would a bill written two years ago have changed the law as it existed at the time.

A major obstacle to version control is that intermediate versions of many documents are not stored. The sooner we start to save documents in a version-control database, the further back our record will go. That is why a second important step of modernization—after digital citations—is to manage documents in version control as soon as possible. 

An alternative is to try to reconstruct the history of a document—something that is possible by tracking amendments to laws from their original enactment. However, that process is more involved and labor intensive than storing each document, as it is currently updated, in a version-control database.

Although the technology now exists, with XCiteDB, there is currently no public site where federal law is being stored in a way that provisions can be retrieved using a point-in-time query.

### Digital Publication and Cloud Deployment

The third important technical challenge is how laws are digitally published. We know that posting pdfs is not enough to modernize publication. The next evolutionary stage of online publication, ‘Bulk Data’, allowed technical users to download laws, process them, and sometimes republish them—as trailblazing sites like govtrack.us and Cornell’s LII have done. A third stage is to publish API’s, where documents, and information about the documents, can be downloaded selectively by technical usersL. GPO and the Library of Congress have provided very useful API’s to legislative data.

The next stage, however, is publication of the laws as a public resource: a searchable, dynamic online publication, where citations translate to URLs and URLs translate to citations. To do this requires solving the earlier two challenges (citations as urls and updating laws with version control), as well as developing a modern cloud infrastructure and robust deployment processes for the law. 

As mentioned earlier, it will also require careful coordination between the stewards of our laws, in various entities across the federal government. Below, I briefly describe each data source and its current state of digitization.

### Bills

Federal bills originate in Congress. These have been published in a structured digital format for years and are now available from the Government Publishing Office in United States Legislative Markup (USLM), the common standard for federal legislative materials. Each level of a bill in USLM has its digital citation, or ‘identifier’. Currently, congress.gov publishes bills in a form that it is possible to scroll to an individual provision. In the near future it should be possible to refer to section 1010(b)(i) of a bill and retrieve just that portion of the bill.

### U.S. Code

The United States Code is an organized collection of the law maintained by the Law Revision Counsel (LRC), an independent organization that is part of the legislative branch. The Code is now published in USLM and is updated with the enactment of new laws in ‘release points’ that are published by LRC at uscode.house.gov. Each portion of the Code in USLM also carries its digital citation in the form of an ‘identifier’.

### Statute Compilations

Each law that is enacted becomes part of the ‘Statutes at Large’. The House Office of Legislative Counsel (HOLC) organizes these freestanding statutes and maintains up-to-date versions of the statutes that can be further amended by future laws. This collection is called the ‘Statute Compilations’, and many (but not all) of these statutes are also now published in USLM, with an embedded digital citation at each provision.

With these three data sources, and the tools described above, we are closer today than we have been since I started working in this area to a modernized online publication of federal law.