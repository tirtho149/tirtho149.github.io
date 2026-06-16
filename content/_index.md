---
# Leave the homepage title empty to use the site title
title:
type: landing

sections:
  - block: about.biography
    id: about
    content:
      title: Biography
      # Choose a user profile to display (a folder name within `content/authors/`)
      username: admin

  - block: experience
    id: experience
    content:
      title: Experience
      date_format: Jan 2006
      items:
        - title: Graduate Research Assistant
          company: Translational AI Center, Iowa State University
          company_url: 'https://trac.iastate.edu/'
          company_logo: ''
          location: Ames, IA
          date_start: '2025-01-01'
          date_end: ''
          description: |2-
              - Lead M.S. thesis research on **agentic vision-language systems for cyber-agriculture** under Prof. Soumik Sarkar; co-first-authored work accepted at a **CVPR 2026** workshop.
              - Co-engineered **SAGE**, an autonomous crop-disease-diagnosis agent powered by the largest plant-disease image–symptom dataset to date (335 crops, 1,251 classes, ~839K images); symptom grounding raised accuracy by **+16.2 points** and generalizes to unseen crops with no retraining.
              - Build large-scale LLM/VLM evaluation pipelines and reproducible benchmarks spanning agriculture, healthcare, and finance.
        - title: Undergraduate Research Assistant
          company: Translational AI Center, Iowa State University
          company_url: 'https://trac.iastate.edu/'
          location: Ames, IA
          date_start: '2024-04-01'
          date_end: ''
          description: |2-
              - Built a GPT-4o pipeline analyzing 430 Shark Tank pitches to quantify how market orientation and brand storytelling drive investor decisions; published in the *Journal of Business & Industrial Marketing*.
        - title: Undergraduate Software Developer
          company: Dept. of Agricultural & Biosystems Engineering, Iowa State University
          company_url: 'https://www.abe.iastate.edu/'
          location: Ames, IA
          date_start: '2024-06-01'
          date_end: '2024-12-31'
          description: |2-
              - Developed a chatbot web frontend for an agricultural research tool with Prof. Ryan McGhee, improving usability through iterative, user-tested design.
        - title: Undergraduate Research Volunteer
          company: Dept. of Computer Science, Iowa State University
          company_url: 'https://www.cs.iastate.edu/'
          location: Ames, IA
          date_start: '2024-04-01'
          date_end: '2024-05-31'
          description: |2-
              - Ran controlled probing experiments on how large language models resolve knowledge conflicts (conflicting context vs. parametric memory) under Prof. Qi Li.
    design:
      columns: '2'

  - block: skills
    id: skills
    content:
      title: Technical Skills
      text: ''
      items:
        - name: Languages
          description: 'Python, TypeScript, JavaScript, SQL'
          icon: code
          icon_pack: fas
        - name: Web & Full-Stack
          description: 'React, REST APIs, responsive UI/UX, web app development'
          icon: laptop-code
          icon_pack: fas
        - name: ML & AI
          description: 'PyTorch, deep learning, computer vision, VLMs, LLMs, multi-agent systems'
          icon: brain
          icon_pack: fas
        - name: Data & Infrastructure
          description: 'Data pipelines, large-scale datasets, databases/SQL, cloud (AWS/GCP), Git'
          icon: database
          icon_pack: fas
    design:
      columns: '2'

  - block: collection
    id: publications
    content:
      title: Publications & Presentations
      text: ''
      count: 0
      order: desc
      filters:
        folders:
          - publication
    design:
      view: citation
      columns: '2'

  - block: portfolio
    id: projects
    content:
      title: Projects
      filters:
        folders:
          - project
      default_button_index: 0
      buttons:
        - name: All
          tag: '*'
    design:
      view: showcase
      columns: '1'
      flip_alt_rows: true

  - block: accomplishments
    id: awards
    content:
      title: 'Honors & Awards'
      subtitle: ''
      date_format: Jan 2006
      items:
        - title: Dean's High Impact Award for Undergraduate Research
          organization: Iowa State University
          organization_url: 'https://www.iastate.edu/'
          date_start: '2025-08-01'
          description: ''
        - title: 'Best-In-Show, George Washington Carver Poster Challenge'
          organization: Iowa State University
          date_start: '2025-04-01'
          description: ''
        - title: 'Borlaug Poster Competition — 1st Place (Undergraduate Division)'
          organization: Iowa State University, College of Agriculture and Life Sciences
          date_start: '2025-03-01'
          description: ''
        - title: Bangladesh–Sweden Trust Fund Travel Grant
          organization: ''
          date_start: '2025-01-01'
          description: ''
        - title: College of Liberal Arts and Sciences Travel Grant
          organization: Iowa State University
          date_start: '2025-01-01'
          description: ''
        - title: Dean's List
          organization: Iowa State University
          date_start: '2024-12-01'
          description: ''

  - block: markdown
    id: service
    content:
      title: Academic Service
      subtitle: 'Peer review & ethics review'
      text: |-
        - **Ethics Reviewer**, NeurIPS 2025 — Main Conference and Datasets & Benchmarks tracks
        - **Reviewer**, CV4Animals Workshop @ CVPR 2026
        - **Reviewer**, AI for Good (AI4GOOD) Workshop @ ICML 2026
        - **Reviewer**, AI for Critical National Infrastructure (AI4CNI) Workshop @ AAMAS 2026
        - **Reviewer**, Rashomon Effect Workshop @ AAAI 2026
        - **Reviewer**, LatinX in AI (LXAI) Workshop @ NeurIPS 2025
        - **Reviewer**, LatinX in Computer Vision Workshop @ CVPR 2025
        - **Reviewer**, Second Workshop on Bangla Language Processing @ IJCNLP-AACL 2025
    design:
      columns: '1'

  - block: contact
    id: contact
    content:
      title: Contact
      subtitle: ''
      email: tirtho@iastate.edu
      # Secondary email shown in the text below.
      text: |-
        Also reachable at [tirthoroyapon@gmail.com](mailto:tirthoroyapon@gmail.com).
      autolink: true
    design:
      columns: '1'
---
