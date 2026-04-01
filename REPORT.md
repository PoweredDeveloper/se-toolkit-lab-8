# Lab 8 — Report

Paste your checkpoint evidence below. Add screenshots as image files in the repo and reference them with `![description](path)`.

## Task 1A — Bare agent

<!-- Paste the agent's response to "What is the agentic loop?" and "What labs are available in our LMS?" -->
The agentic loop is the fundamental cycle that an AI agent follows to accomplish tasks autonomously. It typically consists of these core stages:                                                                                                            

 1 Perceive — Gather information about the current state (user input, environment, tool outputs, memory)                                                                                                                                                    
 2 Reason/Plan — Analyze the situation, determine goals, and decide on a course of action                                                                                                                                                                   
 3 Act — Execute actions using available tools (file operations, API calls, shell commands, etc.)                                                                                                                                                           
 4 Observe — Receive feedback from the actions taken (success, failure, new data)                                                                                                                                                                           
 5 Reflect/Iterate — Evaluate results, update understanding, and decide whether to continue, adjust, or complete the task                                                                                                                                   

This loop repeats until the task is complete or a stopping condition is met.                                                                                                                                                                                

                                                                                                                                                                                                                                                            
 ┌─────────────┐                                                                                                                                                                                                                                            
 │   Perceive  │                                                                                                                                                                                                                                            
 └──────┬──────┘                                                                                                                                                                                                                                            
        ▼                                                                                                                                                                                                                                                   
 ┌─────────────┐                                                                                                                                                                                                                                            
 │   Reason    │                                                                                                                                                                                                                                            
 └──────┬──────┘                                                                                                                                                                                                                                            
        ▼                                                                                                                                                                                                                                                   
 ┌─────────────┐                                                                                                                                                                                                                                            
 │    Act      │                                                                                                                                                                                                                                            
 └──────┬──────┘                                                                                                                                                                                                                                            
        ▼                                                                                                                                                                                                                                                   
 ┌─────────────┐                                                                                                                                                                                                                                            
 │   Observe   │                                                                                                                                                                                                                                            
 └──────┬──────┘                                                                                                                                                                                                                                            
        ▼                                                                                                                                                                                                                                                   
 ┌─────────────┐                                                                                                                                                                                                                                            
 │   Reflect   │───(continue?)───┐                                                                                                                                                                                                                          
 └─────────────┘                 │                                                                                                                                                                                                                          
        │                        │                                                                                                                                                                                                                          
        ▼ (done)                 │                                                                                                                                                                                                                          
     Complete ◄──────────────────┘                                                                                                                                                                                                                          
                                                                                                                                                                                                                                                            

The quality of an agent depends on how well it executes each stage—especially its ability to reason about complex situations and learn from observations to improve subsequent iterations. 

---

Based on my exploration of the workspace, here are the available labs in this LMS (Learning Management System) course:                                                                                                                                      

Lab 8 — The Agent is the Interface                                                                                                                                                                                                                          

This is the current lab you're working on. It focuses on building an AI agent (nanobot) as a natural-language interface for the LMS.                                                                                                                        

Required Tasks:                                                                                                                                                                                                                                             

 1 Task 1: Set Up the Agent — install nanobot, configure Qwen API, add MCP tools, write skill prompt                                                                                                                                                        
 2 Task 2: Deploy and Connect a Web Client — Dockerize nanobot, add WebSocket channel + Flutter chat UI                                                                                                                                                     
 3 Task 3: Give the Agent New Eyes — explore observability data, write log/trace MCP tools                                                                                                                                                                  
 4 Task 4: Diagnose a Failure and Make the Agent Proactive — investigate a failure, schedule in-chat health checks, fix a planted bug                                                                                                                       

Optional Tasks:                                                                                                                                                                                                                                             

 1 Task 1: Add a Telegram Bot Client — same agent, different interface                                                                                                                                                                                      

The LMS system itself includes:                                                                                                                                                                                                                             

 • Backend: FastAPI application with endpoints for items, interactions, and learners                                                                                                                                                                        
 • Database: PostgreSQL with seeded data                                                                                                                                                                                                                    
 • Frontend: React dashboard (client-web-react)                                                                                                                                                                                                             
 • Infrastructure: Docker Compose with Caddy reverse proxy, pgAdmin, and observability tools (OpenTelemetry, VictoriaLogs, VictoriaTraces)                                                                                                                  

Would you like me to read more details about any specific task or explore the LMS data (learners, items, interactions)?    

## Task 1B — Agent with LMS tools

<!-- Paste the agent's response to "What labs are available?" and "Describe the architecture of the LMS system" -->

Here are the available labs:                                                                                                                                                                                                                                

Required Labs (/lab/tasks/required/):                                                                                                                                                                                                                       

 • task-1.md                                                                                                                                                                                                                                                
 • task-2.md                                                                                                                                                                                                                                                
 • task-3.md                                                                                                                                                                                                                                                
 • task-4.md                                                                                                                                                                                                                                                
 • task-5.md                                                                                                                                                                                                                                                

Optional Labs (/lab/tasks/optional/):                                                                                                                                                                                                                       

 • task-1.md                                                                                                                                                                                                                                                

Wiki/Lab Documentation (/wiki/):                                                                                                                                                                                                                            

 • lab-1/ (directory with lab materials)                                                                                                                                                                                                                    
 • Plus extensive documentation on various topics (architecture, databases, Docker, Git, Linux, Python, web APIs, etc.)                                                                                                                                     

Would you like me to read the contents of any specific lab task or the lab-1 wiki documentation?                                                                                                                                                            

2026-03-28 16:36:40.249 | INFO     | nanobot.agent.loop:_process_message:479 - Response to cli:user: Here are the available labs:

**Required Labs** (`/lab/tasks/required/`):
- task-1.md
- task-2.md
- task-3.md
- task-4.m...

---

Yes, the LMS backend is healthy! ✅                                                                                                                                                                                                                         

Health Check Results:                                                                                                                                                                                                                                       

                                                                        
 Metric               Status                                            
 ────────────────────────────────────────────────────────────────────── 
 Container            se-toolkit-lab-8-backend-1 - Running (Up ~1 hour) 
 Port                 127.0.0.1:42001 -> 8000/tcp                       
 CPU / Memory         0.30% / 83.09 MiB (2.12%)                         
 Database Connection  ✅ Connected to db-lab-8                          
 Item Count           56 items (8 labs, 48 tasks)                       
 Recent Requests      HTTP 200 OK on /items/ endpoint                   
 Errors               None                                              
                                                                        

The backend is fully operational, connected to PostgreSQL, and successfully serving learning items from the database. 

## Task 1C — Skill prompt

<!-- Paste the agent's response to "Show me the scores" (without specifying a lab) -->

Lab 01 – Products, Architecture & Roles                                                                                                                                                                                                                     

 • Completion: 100% (258/258 students)                                                                                                                                                                                                                      
 • Top Group: B25-DSAI-03 (82.8% avg)                                                                                                                                                                                                                       
 • Top Learners: 6 students with 100% average                                                                                                                                                                                                               

Lab 02 — Run, Fix, and Deploy a Backend Service                                                                                                                                                                                                             

 • Completion: 89.1% (131/147 students)                                                                                                                                                                                                                     
 • Top Group: B25-CSE-01 (77.6% avg)                                                                                                                                                                                                                        
 • Top Learners: 3 students with 100% average                                                                                                                                                                                                               

Lab 03 — Backend API: Explore, Debug, Implement, Deploy                                                                                                                                                                                                     

 • Completion: 89.1% (156/175 students)                                                                                                                                                                                                                     
 • Top Group: unknown (84.1% avg)                                                                                                                                                                                                                           
 • Top Learners: 3 students with 100% average                                                                                                                                                                                                               

Lab 04 — Testing, Front-end, and AI Agents                                                                                                                                                                                                                  

 • Completion: 96.7% (238/246 students)                                                                                                                                                                                                                     
 • Top Group: B25-CSE-01 (67.2% avg)                                                                                                                                                                                                                        
 • Top Learners: 3 students with 100% average                                                                                                                                                                                                               

Lab 05 — Data Pipeline and Analytics Dashboard                                                                                                                                                                                                              

 • Completion: 98.4% (246/250 students)                                                                                                                                                                                                                     
 • Top Group: B25-CSE-01 (80.8% avg)                                                                                                                                                                                                                        
 • Top Learners: 3 students with 100% average                                                                                                                                                                                                               

Lab 06 — Build Your Own Agent                                                                                                                                                                                                                               

 • Completion: 98.4% (242/246 students)                                                                                                                                                                                                                     
 • Top Group: unknown (66.3% avg)                                                                                                                                                                                                                           
 • Top Learners: 3 students with 100% average                                                                                                                                                                                                               

Lab 07 — Build a Client with an AI Coding Agent                                                                                                                                                                                                             

 • Completion: 99.6% (236/237 students)                                                                                                                                                                                                                     
 • Top Group: unknown (83.6% avg)                                                                                                                                                                                                                           
 • Top Learners: Learner #241 (100%), Learner #105 (97.1%), Learner #84 (97.1%)                                                                                                                                                                             

Lab 08 — (Empty)                                                                                                                                                                                                                                            

 • Completion: 0% (no students yet)   

## Task 2A — Deployed agent

<!-- Paste a short nanobot startup log excerpt showing the gateway started inside Docker -->

## Task 2B — Web client

<!-- Screenshot of a conversation with the agent in the Flutter web app -->

## Task 3A — Structured logging

**Happy path** — After a successful LMS request, from `docker compose --env-file .env.docker.secret logs backend --tail 30` you should see structured `event` values such as `request_started` and `request_completed` with `status` 200.

<!-- Paste your excerpt here (request_started → request_completed, status 200). -->

**Error path** — With PostgreSQL stopped, a failing request should show error-level / failed completion in logs (e.g. `db_query` or non-2xx `request_completed`).

<!-- Paste your error-path excerpt here. -->

**VictoriaLogs** — Query example: `_time:1h service.name:"Learning Management Service" severity:ERROR`

<!-- Screenshot: ![VictoriaLogs LogsQL results](report-assets/task-3a-victorialogs.png) -->

## Task 3B — Traces

<!-- Healthy trace: ![Healthy trace](report-assets/task-3b-trace-healthy.png) -->
<!-- Error trace: ![Error trace](report-assets/task-3b-trace-error.png) -->

## Task 3C — Observability MCP tools

Ask the agent: **“Any LMS backend errors in the last 10 minutes?”** (narrower than “last hour” so the answer tracks fresh LMS telemetry.)

**Normal conditions (PostgreSQL up):**

<!-- Paste agent response here. -->

**After failure (PostgreSQL stopped, a few LMS requests, then same question):**

<!-- Paste agent response here. -->

## Task 4A — Multi-step investigation

With PostgreSQL stopped, after an LMS list-labs/items failure, ask **“What went wrong?”**

<!-- Paste the agent response (log + trace evidence, affected service, failing operation). -->

## Task 4B — Proactive health check

<!-- Screenshot or transcript: proactive cron health report in the same Flutter chat while DB is down. -->

## Task 4C — Bug fix and recovery

1. **Root cause** — `GET /items/` in `backend/src/lms_backend/routers/items.py` used a broad `except Exception` and always raised **404 “Items not found”**, hiding real database/session errors (e.g. PostgreSQL down).

2. **Fix** — Removed that handler so failures propagate; the global exception handler returns **500** with the real error instead of a fake 404.

3. **Post-fix “What went wrong?”** (PostgreSQL stopped, after redeploy; newest request only):

<!-- Paste agent response showing real DB/backend failure, not misleading 404. -->

4. **Healthy follow-up** (PostgreSQL up, cron or manual check):

<!-- Paste or screenshot: “system looks healthy” / no recent errors. -->
