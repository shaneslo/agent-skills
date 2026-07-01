# Architecture — {{PROJECT_NAME}}

<!--
  STRUCTURE NOTE: this template follows a C4-lite / arc42 shape (context →
  containers → components → decisions → cross-cutting concerns). This is the
  placeholder to be reconciled against the "WS Hobson" architecture style you
  prefer — once you share an example, adjust the section set to match it. Keep
  whatever structure you land on identical across repos so any engineer can
  jump between projects and know where to look.
-->

## 1. Purpose & scope

<!-- FILL: one paragraph. What this system does, and — just as important — what
     it explicitly does NOT do. Draw the boundary. -->

## 2. Context (who/what it talks to)

<!-- FILL: the system as a single box, and every external actor and system it
     exchanges data with. A simple list or a diagram. Answer: what are the
     inputs, what are the outputs, who are the users? -->

- **Users / actors:**
- **Upstream (we consume):**
- **Downstream (we produce / call):**

## 3. Containers (the deployable/runnable pieces)

<!-- FILL: the major runnable units — services, jobs, the web app, the database,
     queues. For each: its responsibility, its tech, and how it's reached. -->

| Container | Responsibility | Tech | Interface |
| --- | --- | --- | --- |
| | | | |

## 4. Components (inside the main container)

<!-- FILL: the internal modules and how they depend on each other. The key thing
     a new engineer needs: "if I'm changing X, which files/modules do I touch?"
     A dependency sketch beats prose here. -->

## 5. Data & state

<!-- FILL: the core data model / the source-of-truth. Where does state live, what
     owns it, and what are the invariants that must never be violated? -->

## 6. Key decisions

<!-- FILL: the 3-7 decisions that shaped this system and would surprise someone.
     Link each to its ADR under docs/adr/. If a decision has real consequences,
     it deserves a record, not a sentence. -->

- **<decision>** — why, and the alternative rejected. See [ADR-000X](docs/adr/).

## 7. Cross-cutting concerns

<!-- FILL: the things that touch every component. Delete rows that don't apply. -->

- **Configuration & secrets:**
- **Auth / authorization:**
- **Error handling & retries:**
- **Observability (logs / metrics / traces):**
- **Performance / scale assumptions:**
- **Security & data handling:**

## 8. Known limitations & risks

<!-- FILL: what's brittle, what's deferred, what you'd fix with more time. Being
     honest here saves the next person a week of confusion. -->
