# Diagrams: flowcharts, org charts, sequence diagrams, mind maps

Source of truth: the parsed graph (Mermaid, Graphviz, PlantUML, a node and edge list), never the image alone. Vision
models misread arrows and directions. If only an image exists, say so and read labels you can see, no more.

Shapes, colours and line styles are not spoken unless a legend gives them meaning (dashed = optional, red = error).

## Flowchart (process, decision tree)

Follows the NCAM pattern (overview, then numbered boxes with their transitions), adapted to speech.

1. Announce: "A flowchart with {N} steps and {D} decisions, {E} entry point(s), {X} exit(s), from {start} to {end}."
   Convention: a step is any box that is not a decision, start and end boxes included; decisions are counted apart.
2. Message: what the process does, one sentence: "It takes an order from receipt to delivery, with a stock check."
3. Main path: the most direct path from start to end, steps numbered:
   "Step 1, order received. Step 2, check stock. Decision: in stock? If yes, step 3, pack. If no, step 5, back-order,
   then back to step 2."
   - A decision is a question with each outcome and its target.
   - A loop: "back to step {n}". A merge: "joins step {n}". A parallel split: "then two things happen at once: …".
   - Groups of 3 to 4 steps, then a pause.
4. Branches: after the main path, each side branch from its decision, on request or if short.
5. Detail on request: "Step 3: pack. It comes from step 2 when stock is available, and leads to step 4, ship."

Mermaid cues: `{ }` is a decision, `(( ))` start/end, `[ ]` process, `-->|label|` the edge label (the answer).

## Org chart (hierarchy)

Announce: "An org chart with {L} levels and {N} positions, led by {top}."
Message: "{Top} has {k} direct reports: {names if ≤ 4, else the count and the first three}."
Detail: one branch at a time, top-down, one level per turn: "Under Finance: accounting, 3 people; treasury, 2 people."
Say "{n} reports" rather than listing more than four names; list them on request. Dotted lines: "also reports to".

## Sequence diagram

Announce: "A sequence diagram with {P} participants: {in order}; {M} messages."
Message: the scenario: "A user logs in: the app asks the server, which checks the database."
Detail: in order, "from {A} to {B}: {message}", groups of 3 to 4; replies as "back to {A}: {message}"; loops "repeat
while …"; alternatives "if …, otherwise …"; activations are not spoken.

## Mind map, concept map

Announce: "A mind map centred on {centre}, with {B} main branches, up to {depth} levels deep."
Message: the main branches by name (≤ 6; else the first four and "and {B−4} more").
Detail: one branch at a time, outward: "Branch Marketing has 3 items: social, email, events." Deeper levels on request.
Concept map with labelled links: "{A} {link} {B}" ("photosynthesis produces oxygen").

## State machine, ER diagram, network

State machine: states count, initial state, then transitions as "from {state}, on {event}, go to {state}".
ER diagram: entities count, then "an {A} has many {B}" per relation; attributes on request.
Network/architecture: components count, the data flow in order, then each component on request.

## Loops, cycles and unreachable parts

Detect them from the graph and say them: "Steps 4 and 5 form a loop until stock is available." "Two steps are not
connected to the rest." Never silently linearise a cycle.
