# Shopping Research

[中文](README.md) | [English](README.en.md)

**Version: v1.3.0 · Trial** · [Changelog](CHANGELOG.md) · [Validation scope](VALIDATION.md)

A Codex skill for consumer purchase decisions. It researches products against the intended use, budget, and hard constraints, checking quality, safety, prices, customer feedback, long-term costs, and company practices. The result identifies specific versions, purchasing channels, material trade-offs, and evidence gaps.

The entry point is [skills/shopping-research/SKILL.md](skills/shopping-research/SKILL.md). The skill instructions are currently written in Chinese. Runtime questions, options, explanations, and reports follow the user's current conversation language, with an explicitly requested output language taking priority.

## Main capabilities

- Investigates 3–5 meaningfully different ordinary-product candidates per independent need by default, checking different solutions before comparing brands, configurations, and prices. It does not fill a quota when fewer suitable options exist, and may expand to an important new solution.
- Discovers brands and purchasing channels openly, supporting one market, several countries or regions, or no market restriction. China is not assumed as the default market.
- Matches evidence to the exact model, market version, seller, specification, and batch. Standards, inspections, recalls, and test results retain their actual scope.
- Distinguishes public product-page prices, conditional discounted prices, reproduced checkout prices, and historical or aggregated reference prices. Unknown fees are not treated as zero, and public quotes are not presented as confirmed final prices.
- Places a supported score and its meaning, purchase status, purchasing links, and coupon information before each product's complete 12-part assessment.
- Adds a separate farmer-support section for relevant food purchases, following source relationships and purchasing links across relevant platforms.

## Shopping markets, privacy, and language

When the research scope needs clarification, the skill uses the following questions in the current conversation language:

> Which country or region's shopping channels would you like me to focus on? For example, mainland China, Japan, or the United States. You can choose one market, several markets, or no restriction.
>
> Should cross-border purchasing channels be included as well?

This selects the research market. The skill does not ask for a delivery destination, current location, or street address, and does not infer location from a device or account. The selected market does not establish the user's location, a brand's nationality, or the conversation language. Existing answers are reused; unanswered questions do not prevent independent research from continuing with an open channel scope.

Delivery coverage, shipping, taxes, and regional applicability are checked against public conditions. Unconfirmed conditions remain explicit rather than becoming a promise of delivery to the user. Original-currency prices are preserved; conversions are added when a budget currency or another requested currency is clear.

## The 12-part product assessment

| Item | Main focus |
|---|---|
| Fit for the need | Fit for the intended use and hard constraints |
| Actual price and value | Matched-version quotes, price type, necessary conditions, and supported benefits |
| Strengths | Evidence-supported advantages |
| Weaknesses and trade-offs | Known issues, usage burdens, and costs of the choice |
| Quality and reliability | Actual performance, durability, and evidence coverage |
| Safety and compliance | Relevant risks, applicable requirements, and verified or pending results |
| Real customer feedback | Attributable reviews, long-term experience, and seller responses |
| Long-term costs | Consumables, repairs, subscriptions, accessories, and relevant usage costs |
| After-sales support | Warranty, returns, service, and repair conditions |
| R&D and marketing | Verifiable technical investment, outcomes, and support for claims |
| Labor practices and benefits | Attributable working conditions, compensation, disputes, and remedies |
| Conditional conclusion | Who it suits, its purchase status, and what could change the conclusion |

These are separate explanatory perspectives, not 12 overlapping weighted scores. Specific indicators are adapted to the product category, and unknowns remain unknown.

## Ordinary-product scoring and purchase status

The seven default weights total 100:

| Dimension | Weight |
|---|---:|
| Quality and reliability | 35 |
| Fit for the need | 20 |
| Actual price and value | 15 |
| Long-term costs | 10 |
| After-sales support and repairability | 10 |
| R&D and marketing supplementary factors | 5 |
| Labor practices and benefits supplementary factors | 5 |

Weights are declared before scoring, may be adjusted to the user's requirements, and are applied consistently across candidates. Evidence-based weighted totals, partial scores, and subjective recommendation scores are distinguished. Missing evidence does not receive invented points or inflated remaining weights; candidates are not forced into a ranking when their core evidence is not comparable. Negative findings are separated from missing evidence, and the same issue is not deducted twice. Safety requirements and hard constraints are separate gates: a high score cannot offset a proven failure of a critical requirement.

Each score is accompanied by one purchase status:

- **Ready for a purchase decision:** sufficient evidence supports the version, core need, hard constraints, critical safety requirements, quote, and necessary transaction conditions.
- **Prioritize verification:** the candidate may be useful, but a decision-changing gap remains.
- **Insufficient evidence; not ranked:** evidence does not support a meaningful choice or comparable ordering.
- **Does not meet this purchase's conditions / exclude from purchase:** a hard constraint is confirmed unmet, or a critical safety requirement is proven unmet.

“There is currently insufficient evidence to recommend a purchase” is an allowed conclusion. The absence of a publicly available full test report does not by itself establish that a product is unsafe or noncompliant; findings stay tied to specific models, requirements, risks, and evidence coverage.

## Separate farmer-support section

For relevant food research, the skill actively looks for farmers, family farms, cooperatives, and merchants with specific, traceable relationships to agricultural producers. This includes fresh produce, grains and dried goods, and processed agricultural products. It follows promising leads, expands to meaningful alternatives, and continues across relevant platforms and sales channels to locate actual purchasing links after identifying a product.

Seller identity, product origin, and the farmer-support relationship receive separate verification labels. The section name does not imply official certification or guarantee an actual financial benefit to farmers. Broad origin claims, rural imagery, and promotional slogans are leads only.

Farmer-support products are listed separately. They are not compared, scored, or ranked against ordinary products, do not consume the ordinary-product candidate slots, have no fixed quota, and do not inherit the ordinary composite score by default. The full 12-part assessment, safety gates, purchase statuses, and evidence requirements remain. Comparable farmer-support products may receive evidence-based, conditional comparisons within that section.

## Installation

### Workbook, review, and default archiving

Each delivery saves the complete report, [research workbook/evidence index](skills/shopping-research/references/research-workbook.md), review record, and version/acceptance record by default, then checks the actual saved files. A reviewer in a separate context first reads the request and raw evidence, then compares the draft. If independent review is unavailable, same-agent review and its reason are disclosed. Material disagreements must be resolved or retain purchase limitations; averaging scores cannot hide them.

The [review and archiving rules](skills/shopping-research/references/review-and-archive.md) use a writable project/task output directory. Failed saves report the actual scope saved. Individual fields distinguish newly checked, reused, expired, and pending evidence; refreshing one quote does not refresh all other data.

[Category cards](skills/shopping-research/references/category-cards.md) cover pillows, personal care, electrical products, and cycling equipment. They guide evidence collection and limits, rather than providing brand lists, certification quotas, or verified product lists.

### Installation options

In an environment supporting Codex skills, use the built-in `$skill-installer` with a request such as:

```text
Install the skills/shopping-research skill from https://github.com/muhuaH-TK/shopping-research.
```

Alternatively, copy the entire `skills/shopping-research` directory into the personal skills directory configured for your client. Preserve the directory name and the relative structure of `SKILL.md`, `agents`, and `references`; copying only the entry file is insufficient. If a skill with the same name already exists, inspect the differences and back it up first. Invoke the installed skill in the next conversation turn.

## Example

```text
Use $shopping-research to compare adjustable-height pillows for long hours of desk work.
My budget is USD 100. Focus on US and Japanese shopping channels, including cross-border options.
Please respond in English.
```

You can also provide existing candidates, product links, screenshots, or an earlier report for continued research or an update. The skill should retain the source dates and verified scope; rearranging text does not constitute a new price check.

## Capability and action boundaries

- This repository provides research instructions and reference rules. Live browsing, web access, and file operations depend on the client's available tools and permissions. It does not automatically install dependencies or guarantee access to every platform.
- It does not bypass sign-in requirements, CAPTCHAs, or access controls. Contacting sellers, joining private groups, creating accounts, claiming offers, or placing orders is not authorized by default; additional actions follow the current authorization boundaries.
- After a failed page read, it makes reasonable alternatives based on the observed problem. If important evidence remains missing, it investigates other candidates first. Research may end with an explained scope and remaining gaps after targeted follow-up; exhaustive web coverage is not required.
- At the start of a new shopping task, known saved shopping outputs strictly older than 30 days are only cleanup candidates, subject to retention exceptions. Moving them to the recycle bin requires confirmation of the specific list. There is no scheduled or automatic deletion, and failed operations preserve the files.
- Instruction and file checks do not establish successful end-to-end testing of real stores, multilingual conversations, or checkout flows. Each result should identify what was actually verified and what remains uncertain.

## Layout

```text
README.md
README.en.md
LICENSE
CHANGELOG.md
VALIDATION.md
tests/                  # Clearly fictional fixtures and observed scoring runs
skills/
  shopping-research/
    SKILL.md
    agents/openai.yaml
    references/
```

See [adapted-methods.md](skills/shopping-research/references/adapted-methods.md) for method references and adoption boundaries. External references do not grant access to their services or imply that this repository inherits an external project's license.

## Tests and license

The [fixed tests](tests/README.md) check scoring and status consistency. Complete inputs, acceptance criteria, and observed runs are stored separately; blind evaluators do not receive expected answers. Real shopping requests, reports, evidence, and ordinary-search comparisons remain internal and are not published as cases. See [validation scope](VALIDATION.md) for observed, failed, and unverified checks. Complete instructions do not establish purchase-ready capability.

Original content that the project can license, including its skill, templates, and fictional tests, uses the [MIT license](LICENSE), copyright muhuaH-TK. Third-party quotations and product materials retain separate source attribution and are not relicensed by this project.
