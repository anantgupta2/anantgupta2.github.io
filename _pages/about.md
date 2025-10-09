---
layout: about
title: about
permalink: /
subtitle: <a href='https://tail.cc.gatech.edu/people.html'>Georgia Institute of Technology</a> 

profile:
  align: right
  image: prof_pic.jpg
  image_circular: false # crops the image to make it circular
  more_info: >
    <p></p>
    <p>Atlanta GA, 30332</p>

selected_papers: true # includes a list of papers marked as "selected={true}"
social: true # includes social icons at the bottom of the page

announcements:
  enabled: false # includes a list of news items
  scrollable: true # adds a vertical scroll bar if there are more than 3 news items
  limit: 5 # leave blank to include all the news in the `_news` folder

latest_posts:
  enabled: false
  scrollable: true # adds a vertical scroll bar if there are more than 3 new posts items
  limit: 3 # leave blank to include all the blog posts
---

### About Me

Hello there! I’m Anant Gupta, a first-year M.S. student in Computer Science at Georgia Tech, where I also completed my B.S. in Computer Science and Mathematics. I’m interested in continual learning, meta-learning, and information retrieval, and more broadly in how we might build systems that learn, adapt, and teach like humans. I’m particularly fascinated by the question of how models could one day learn efficiently from limited data and generalize their knowledge across domains, much like people do.
Before beginning my M.S., I worked on chaotic dynamical systems and large-scale dataset generation. I’m also deeply passionate about teaching and have served as a Teaching Assistant for Automata and Complexity (CS 4510) for four semesters, an experience that continues to shape how I think about learning itself — in both humans and machines.

### Research Interests

I’m broadly interested in understanding how humans learn, retain, and reason, and how these processes can inspire the design of more adaptive learning systems. Human learning is inherently interconnected — when we encounter new information, we recall what we already know, build context around it, and refine our understanding through explanation and teaching. We learn continuously, without forgetting past knowledge, and our ability to retrieve, relate, and reinterpret concepts allows us to develop deep, transferable understanding.

My research explores how to bring these abilities to machine learning models. I’m interested in how we can enable systems to teach in ways that reveal and strengthen their own understanding, retain knowledge across time without catastrophic forgetting, and retrieve and contextualize information based on prior experience. Together, these directions aim to move toward models that not only store information but can revisit, refine, and truly learn from it — much like humans do.

To that end, my current work explores how these ideas can be realized across three directions:

**Information Retrieval** : Developing a cognitive-inspired model for information retrieval that achieves performance rivaling state-of-the-art neural systems using only PCA and ICA whitening, without any gradient-based training. The model organizes information into incremental concept hierarchies, allowing for interpretable and adaptive retrieval that mirrors how humans categorize and recall knowledge.

**Continual Learning** : Investigating class-incremental continual learning with diffusion models, where we found that their Fisher Information matrices are inherently low-rank. By exploiting this property, we use elastic weight consolidation to mitigate catastrophic forgetting, allowing models to learn new tasks while preserving prior knowledge.

**LLM Tutor for Deep Theoretical Courses** : Building a Large Language Model–based tutor for teaching advanced theoretical computer science and mathematics. The goal is to create systems that don’t just deliver answers but engage, explain, and refine their understanding through teaching. By employing these models as teachers, we can better uncover weaknesses in their reasoning and move toward AI systems capable of genuine conceptual understanding.
