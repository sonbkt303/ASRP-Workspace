# Knowledge Constitution (Writing Rules)

## Mission
Build a Security Knowledge Base that is:
- Accurate
- Structured
- Non-duplicated
- Scalable
- Searchable
- Maintainable
- AI/RAG-friendly

## Core Principles

1. One Concept = One Home
- Every concept must have exactly one canonical location.
- Never duplicate knowledge across folders.
- Use links/references instead of copying content.

2. Domain-driven Taxonomy
- Organize by technical domain, not by learning path, framework, feature, or use case.

3. Theory ≠ Practice ≠ Research
- `knowledge/` = theory
- `labs/` = practice
- `apps/` = implementation
- `research/` = investigation
- `tools/` = automation

4. Single Responsibility
- One document explains one concept.
- One folder owns one domain.

5. Link, Don't Copy
- Cross-reference related topics.
- Never rewrite existing knowledge.

6. Explain from First Principles
- Start with fundamentals before implementation.
- Focus on understanding, not memorization.

7. Progressive Learning
Follow this order whenever possible:

Why
→ What
→ Core Concepts
→ How It Works
→ Internal Architecture
→ Implementation
→ Security Considerations
→ Common Mistakes
→ Best Practices
→ Related Topics
→ References

8. Knowledge Before Opinion
Prioritize:
- RFC
- Standards
- Official Documentation
- Books
- Research Papers

Personal notes should always come last.

9. Keep Documents Atomic
- Small topics → single markdown file.
- Large topics → folder with `README.md`.
- Avoid oversized documents.

10. Consistency
Every topic should follow the same writing style, terminology, and template.

11. Define Boundaries
Every topic should clearly define:
- In Scope
- Out of Scope

12. Security Mindset
Whenever applicable, explain:
- Attack Surface
- Threats
- Risks
- Mitigations
- Best Practices

13. Keep Knowledge Timeless
- Store concepts, not framework versions.
- Framework-specific examples belong in Implementation sections.

14. Refactor Continuously
Knowledge should evolve like source code.
Split, merge, move and reorganize documents when necessary.

15. Rule Zero
If you're unsure where a topic belongs,
DO NOT duplicate it.
Refine the taxonomy first.

