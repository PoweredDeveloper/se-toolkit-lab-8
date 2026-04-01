---
name: lms
description: Use LMS MCP tools for live course data
always: true
---

# LMS Skill

Access the LMS backend for live course data: labs, learners, pass rates, completion, groups, timeline, and top learners.

## Available Tools

| Tool | When to Use |
|------|-------------|
| `lms_health` | Check if LMS is up and get item count |
| `lms_labs` | List all labs — always call this first when a lab choice is needed |
| `lms_learners` | List all registered learners |
| `lms_pass_rates` | Get average score and attempt count **per task** for a lab |
| `lms_completion_rate` | Get passed/total ratio for a lab (single percentage) |
| `lms_groups` | Get avg score + student count **per group** for a lab |
| `lms_timeline` | Get submission counts by date for a lab |
| `lms_top_learners` | Get top N learners by average score for a lab |
| `lms_sync_pipeline` | Trigger a sync (rare, only if data seems stale) |

All tools except `lms_labs`, `lms_learners`, `lms_health`, and `lms_sync_pipeline` require a `lab` parameter (e.g., `"lab-04"`).

## Strategy

- If the user asks for **scores, pass rates, completion, groups, timeline, or top learners** without naming a lab, call `lms_labs` first.
- If multiple labs are available, ask the user to choose one using the **structured-ui skill** and the **`mcp_webchat_ui_message`** tool on WebChat (same payload rules as in structured-ui: `chat_id` from runtime context, `type: "choice"` with `choices` carrying `label` / `value`).
- Use each lab's **title** as the user-facing label (e.g., "Lab 04: Functions" rather than just "lab-04"). If the tool output doesn't include a title, use the lab ID.
- Let the **structured-ui skill** handle how to present the choice — pass lab options as `choices` with `label` (what the user sees) and `value` (the stable lab id for the next `lms_*` tool call).

## Formatting

- **Percentages**: Show as "X%" not "0.X" — e.g., "87% passed" not "0.87 passed"
- **Counts**: Include the total when showing partial numbers — e.g., "23 of 30 students passed"
- **Group/Task names**: Bold or highlight for readability
- **Keep it brief**: One short paragraph per answer, not a full table unless explicitly requested

## What You Can Do

When asked "what can you do?" or similar, explain:

- "I can check if the LMS is healthy and get item counts"
- "I can list all labs and let you pick one"
- "For a chosen lab, I can show pass rates per task, overall completion %, group performance, submission timeline, or top learners"
- "I can also list all learners if needed"

## Error Handling

- If `lms_health` fails, the LMS is down — tell the user and suggest checking the backend.
- If a tool returns an error, report it plainly: "LMS returned an error: ..."
- If the user asks for data that requires a lab but none was specified, do not guess — ask.

## Example Flow

User: "What's the completion rate?"

1. Call `lms_labs` (no args)
2. Receive list of labs, e.g., `[{"id": "lab-01", "title": "Lab 01: Variables"}, {"id": "lab-02", "title": "Lab 02: Functions"}]`
3. Use structured-ui to present choice with labels from `title`, values from `id`
4. User picks "lab-01"
5. Call `lms_completion_rate` with `{"lab": "lab-01"}`
6. Receive e.g., `[{"lab_id": "lab-01", "passed": 23, "total": 30}]`
7. Respond: "Lab 01: Variables — **77%** completed (23 of 30 students passed)"
