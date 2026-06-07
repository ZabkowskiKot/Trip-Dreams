# Trip Dreams — Product Roadmap

> Last updated: June 2026

---

## Vision

A shared workspace where a group can go from "where should we go?" all the way to "here's what we owe each other" — without switching between WhatsApp, a Google Doc, and Splitwise.

The goal is not to replicate Wanderlog. It is to be the best tool for small groups of friends planning European trips together, with a smooth European-first UX (EUR, CET, no dollar assumptions).

---

## Competitive landscape

### Key players we studied

| App | Strength | Gap relevant to us |
|-----|----------|--------------------|
| **Wanderlog** | Map-based itinerary, group editing, expense tracking | No group decision-making / voting |
| **TripIt** | Auto-import from email, flight alerts | No planning tools, no group features |
| **NomadCrew** | Chat + expenses + live map in one | Complex, native app required |
| **Splitwise** | Expense splitting UX | Not travel-context-aware |
| **Groop / Jettova** | Frictionless no-account join | Single-purpose (dates/votes only) |
| **TripMates** | Itinerary + expenses + voting in one | Early-stage, limited polish |
| **SmartTrippy** | Real-time collaborative editing | No expense splitting |

### What the market demands (must-haves by 2026)

1. **Shared workspace** — everyone can contribute, not just the organiser
2. **Group decision-making** — polls/votes on destinations and activities
3. **Frictionless invite** — join via link, no account required to view/vote
4. **Expense splitting in-context** — inside the trip, not a separate app
5. **Real-time sync** — changes visible to the whole group immediately
6. **Role-based access** — owner, editor, viewer
7. **Works during travel** — not just the planning phase
8. **European-friendly** — multi-currency, EU timezones, GDPR-aware

### Where Trip Dreams currently stands

| Must-have | Status | Gap size |
|-----------|--------|----------|
| Shared workspace (groups) | ✅ Built | — |
| Group decision-making / voting | ❌ Missing | **HIGH** |
| Frictionless invite | 🟡 Invite codes planned | Medium |
| Expense splitting | 🟡 UI placeholder only | **HIGH** |
| Real-time sync | 🟡 Firestore ready, frontend not wired | Medium |
| Role-based access | ❌ Missing | Medium |
| Works during travel | ❌ Not considered yet | Low (later) |
| European-first UX | ✅ EUR/CET defaults, locale inference | — |

---

## Epic structure

Epics map to GitHub **milestones**. Features and PBIs are **issues** inside each milestone.

```
Epic 1 — Foundation & Auth          ✅ Done
Epic 2 — Groups & Collaboration     ← Current sprint
Epic 3 — Dream Planner & Voting     ← Next sprint
Epic 4 — Expenses & Settlement      ← Iteration 4
Epic 5 — Calendar & Availability    ← Iteration 5
Epic 6 — Trip Execution             ← Iteration 6
Epic 7 — Platform & UX Quality      ← Ongoing
```

---

## Epic 1 — Foundation & Auth ✅ Done

OAuth, Firestore, user profiles, groups API, group-scoped dreams.

---

## Epic 2 — Groups & Collaboration

**Goal:** A group owner can invite friends; members can join and contribute. No one gets left out because they don't want to create an account.

**Key UX principle:** One shared link drops anyone into the trip in seconds.

| Feature | Issues | Priority |
|---------|--------|----------|
| Invite codes & join links | #5, #6 | HIGH |
| Member list on group detail | #7 | MEDIUM |
| Group member roles (owner / member) | TBD | MEDIUM |
| Frictionless viewer join (no account) | TBD | MEDIUM |
| Leave / remove a member | #8 | LOW |
| Real-time Firestore listeners on frontend | TBD | HIGH |

---

## Epic 3 — Dream Planner & Voting

**Goal:** Every group member can add, edit, and vote on destinations. The group sees which dream has the most support.

**Key insight from research:** This is the most overlooked feature — apps let you list destinations but not *decide* together. Voting replaces 200 WhatsApp messages.

| Feature | Issues | Priority |
|---------|--------|----------|
| Edit a dream destination | #9 | HIGH |
| Delete a dream destination | #10 | HIGH |
| Vote / react on dream destinations | TBD | **CRITICAL** |
| Dream ranking / consensus view | TBD | HIGH |
| Dream status (proposed → chosen → booked) | TBD | MEDIUM |
| Map view for destinations | TBD | LOW |

---

## Epic 4 — Expenses & Settlement

**Goal:** Log what was spent and who paid; the app works out the net balances so settlement is one simple list.

**Key UX principle (from Splitwise research):** Show one net balance per person — not a list of individual transactions. Green = owed to you, red = you owe.

| Feature | Issues | Priority |
|---------|--------|----------|
| Expense entry (who paid, how much, for whom) | #17 | HIGH |
| Multi-currency support | TBD | MEDIUM |
| Itinerary builder (Stage 3) | #16 | MEDIUM |
| Split types: equal / custom / percentage | TBD | MEDIUM |
| Net balance view (settlement summary) | TBD | HIGH |
| Settle up flow | TBD | MEDIUM |

---

## Epic 5 — Calendar & Availability

**Goal:** Find the dates that work for everyone without a 10-reply thread asking "when are you free?"

| Feature | Issues | Priority |
|---------|--------|----------|
| Connect Google Calendar | #13 | MEDIUM |
| Show group availability | #14 | MEDIUM |
| Suggest meeting time windows | #15 | LOW |

---

## Epic 6 — Trip Execution

**Goal:** Useful during the trip, not just before it. Where are people? What's the plan for today?

| Feature | Issues | Priority |
|---------|--------|----------|
| Trip status (planning → active → completed) | TBD | MEDIUM |
| Document / booking storage per trip | TBD | LOW |
| Trip summary & memories (Stage 4) | #18 | LOW |
| Group activity feed (what changed recently) | TBD | LOW |

---

## Epic 7 — Platform & UX Quality

**Goal:** The app works reliably on all devices, is accessible, and the codebase stays clean.

| Feature | Issues | Priority |
|---------|--------|----------|
| Mobile responsive QA | #11 | MEDIUM |
| Update README / API docs | #12 | LOW |
| Accessibility audit (WCAG touch targets, labels) | TBD | MEDIUM |
| In-app notifications (activity changes) | TBD | LOW |

---

## What we are NOT building (yet)

- Native mobile app (web-first for now)
- AI trip suggestions (post-MVP)
- Live location sharing (post-MVP)
- Flight tracking / booking integrations
- Social sharing / public trip pages

---

## Suggested sprint sequence

```
Now      Epic 2 — Groups (invite + real-time)
Sprint 2 Epic 3 — Voting + dream polish
Sprint 3 Epic 4 — Expenses (entry + net balance)
Sprint 4 Epic 5 — Calendar availability
Sprint 5 Epic 6 — Trip execution basics
Ongoing  Epic 7 — Platform quality
```
