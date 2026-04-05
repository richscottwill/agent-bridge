---
inclusion: auto
name: "Process Execution"
description: "Background processes, nohup, setsid, npm commands, server startup, long-running commands, log files"
---

# Process Execution Rule

**Always use this template for background processes:**

( cd "$WORKDIR" && setsid nohup env CI=true TERM=dumb "$CMD" > "$LOGFILE" 2>&1 < /dev/null & )

**When:** ANY command with &, npm commands, servers, long-running processes

**Why it works:**
- < /dev/null prevents tty input suspension
- setsid creates new session 
- nohup survives parent exit
- CI=true TERM=dumb disables prompts
- > logfile 2>&1 captures all output for debugging

**Logging best practices:**
- Always redirect output to log files
- Use descriptive log names (server.log, build.log, etc.)
- Include both stdout and stderr (2>&1)
- Log files help debug issues when processes fail
