# Founder's Way: simulating the player's idea

Goal: the game should model *your* idea, not a generic business. It should be a training ground for real founders and for learners, and produce evidence that could interest investors.

This file covers stages 1 and 3, without AI. AI comes later as an optional extra.

## 1. Player profile
When you first open the game, Doc asks who you are. You can change it in every new game.
- **🎓 Learner** (students, curious people): a short interview made of choices, more explanations from Doc, and a **Learning report** at the end.
- **🚀 Founder** (testing a real idea): numeric ranges, reminders to load real data, and an **Investor memo**.

## 2. The idea model (assumptions)
Each idea has 12 assumptions. Each one stores four things:
- **prior range**: built from benchmarks for the business model, adjusted by the player's answers;
- **player's guess**: the price they set, or their estimate;
- **hidden truth**: sampled once per project with a seed, so it is reproducible;
- **known range**: what the player has learned so far, which narrows with tests and real data.

| key | meaning | plugs into |
|---|---|---|
| market | reachable customers | market size ceiling |
| wtp | willingness to pay (per period) | fair price |
| need | problem intensity | conversion |
| reach | organic reach of the chosen channels | leads per day |
| cpl | cost per lead with paid ads | campaign results |
| cycle | sales cycle in days | sales effort and self-serve |
| churn | monthly churn | lost customers |
| cogs | cost of goods (share of revenue) | margin |
| build | build difficulty | cost of each release |
| viral | word of mouth | referrals |
| comp | competition | price pressure and competitor events |
| reg | regulation | permits, fines, inspections |

Seasonality (strength and peak month) and platform dependency are idea facts. They drive leads and events.

**Benchmarks** are stored per business model (software, store, café, agency) × B2C/B2B, as approximate public ranges.

### How the "truth" is chosen
- **Optimism bias:** truths lean against the founder. Good things (price, demand, reach) skew toward the low end of the range, bad things (churn, costs, sales cycle) toward the high end. Real founders overestimate, and the game reflects that.
- **Doc's interview** turns answers into ranges. Example: "how sure are you of the price?" sets the width of the WTP range.

## 3. Validation (🔬 Validate)
Actions cost money and time. Some use the founder's days (no product work meanwhile); others run in the background.
- **🗣️ Customer interviews:** reveal need and competition, and give a rough WTP that is **biased upward**. People say they would pay more than they do (*The Mom Test*).
- **🌐 Landing page + ads:** reveals need, cost per lead and reach.
- **💲 Pre-sales / pricing test:** reveals the real willingness to pay. Needs a landing page.
- **📊 Desk research:** market size, competition and seasonality.
- **⚖️ Legal consult:** regulation and platform risk.
- **🏭 Supplier/dev quotes:** cost of goods and build difficulty.
- **🧪 Pilot/beta:** churn, sales cycle and word of mouth. Needs v1 and customers.

Results narrow the known range around a **noisy** measurement, so the player can learn something slightly wrong, as in real life.

## 4. Idea-specific challenges
Events are built from the weak points of the idea:
- competition: price wars;
- regulation: permits and fines;
- platform dependency: rule changes;
- long sales cycles: deals stuck in procurement;
- high churn: exit surveys;
- word of mouth: referral waves;
- seasonality: peak and low seasons.

They come on top of the general events and the industry events.

## 5. Calibrating with reality
In the memo, any assumption can get **real data**: a value, a source (interviews, landing page, pre-sales, pilot, research, other) and a note. The known range snaps to it, and the hidden truth is redrawn near it, so the simulation becomes a model of the real business.

## 6. Stress test and "what must be true"
- The current plan (team, price, spending) runs forward 6, 12 or 24 months in 100 worlds. Each world samples the truth from what the player **knows now**.
- Output: survival rate, MRR at percentiles 10, 50 and 90, and the assumptions that most decide success (correlation and a tornado chart).
- It uses the same economic formulas as the live game, with an aggregate model of the team's work that is calibrated against the agent simulation.

## 7. Memo / report
Contents:
- the pitch;
- an assumptions table (guess → known range → source);
- the evidence log;
- the stress test and the most sensitive assumptions;
- the founder's decisions: validated before scaling, runway, pivots;
- lessons, for learners.

It can be copied as Markdown or printed to PDF. A disclaimer applies: it is a simulation, not an investment offer.

## 8. Pace
- **New-game option:** Relaxed (90 s per day), Normal (45 s) or Fast (25 s).
- **⏭ Skip a week:** fast-forwards and stops if something needs a decision.

## 9. Career layer: proof you can use (v11)
Goal: help players get jobs, funding and value, the way Football Manager's database and scout network opened doors in football.
- **🕵️ Scout mode:**
  - Deal flow of 5 generated startups, each with real simulated history, evidence and an ask.
  - The player estimates survival at 12 months, names the biggest risk and invests up to 5 × $100k.
  - Then the game fast-forwards 12 months and reports results.
  - Track record: Brier score, risk spotting, fund multiple and a level.
  - Rounds close more often for startups with traction. About 55–60% of startups survive.
- **🎯 Challenges:**
  - 5 standard cases with a fixed seed: the same company and the same hidden truth for everyone.
  - No prize money, investor offers or grants inside a challenge; loans count against cash scores.
  - Medals, plus a result code that includes the decision log, ready for server replay later.
  - Tuned with a simple bot: passive play fails, a sensible strategy reaches silver or gold.
- **🪪 Profile:**
  - 7 skills measured from play: validation, cash discipline, growth, pricing, team, scouting, execution.
  - Radar chart, roles that match the player's skills, and a funding-readiness checklist.
  - Founder CV to copy or print.
  - Opt-in for partners to make contact (local only until the portal exists).
- **🎤 Pitch deck:** 13 slides generated from the memo, with real data marked as real.
- **Next, online:** accounts, verified rankings (server replay of result codes), public profiles, partners (start with UDD), and a researcher network contributing real benchmarks.
