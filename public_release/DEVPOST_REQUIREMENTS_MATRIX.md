# TracePilot Devpost requirements matrix

Known requirement source: local Devpost/rules notes for the Google Cloud Rapid Agent Hackathon / Arize track.

| Requirement | Current status | Evidence / note | Next action |
| --- | --- | --- | --- |
| Select Arize track | Ed approval | Draft positions TracePilot for Arize/Phoenix track. | Select track in Devpost only after approval. |
| Functional agent powered by Gemini | Satisfied locally | Verified run used Gemini through Google ADK; latest fixed model version recorded as `gemini-2.5-flash`. | Keep wording exact; do not overclaim hosted production. |
| Multi-agent system built with Google ADK | Satisfied locally / needs fresh live proof after code change | Local app now wires a root ADK coordinator (`personalized_shopping_agent`) with two ADK specialist sub-agents (`product_selection_agent`, `purchase_verification_agent`) via `root_agent.sub_agents`; `proof_gate/check_multi_agent_structure.py` verifies this without external calls. | Run a fresh real Gemini/Phoenix proof gate before final submission if claiming the updated multi-agent code path publicly. |
| Google Cloud Agent Builder / Agent Builder wording | Resolved with caveat | `AGENT_BUILDER_ELIGIBILITY_NOTE.md` documents that TracePilot uses Google ADK + Gemini and that Google documents ADK under Gemini Enterprise Agent Platform / Agent Platform. Risk remains if judges require a deployed Agent Builder/Agent Runtime resource. | Use conservative ADK/Gemini wording, or after approval execute the `GOOGLE_AGENT_PLATFORM_DEPLOYMENT_STUB.md` path before claiming Agent Builder deployment. |
| Meaningful Arize/Phoenix integration | Satisfied locally | OpenInference/Phoenix traces plus Phoenix MCP retrieval; canonical trace `52fa8eaf399d8cc4251a9e7f8441a903`. | Use sanitized proof table and video; avoid raw JSON public dump. |
| More than simple chat/tool-use | Satisfied locally | TracePilot scores task completion, diagnoses failures, emits refined task, and shows 71→71→100 improvement. | Present as operator loop above the agent. |
| Runs on web/Android/iOS | Locally improved / redeploy required | `web_demo/` now has a judge-testable safe browser interaction (“Run safe demo proof”) using sanitized proof facts; it can run in desktop/mobile browsers without secrets. | Redeploy after approval and verify the live URL reflects the upgraded interaction. |
| Hosted project URL | Public URL exists; content stale until redeploy | Cloud Run URL was verified for the earlier static shell: https://tracepilot-demo-thryhyeqga-uc.a.run.app. Local page now has safer interactive hosted-demo mode. | Redeploy after approval, then rerun HTTP/browser proof on the live URL. |
| Public open-source repo | Needs work / Ed approval / risky | Repo has Apache-2.0 license, but many generated/local artifacts need exact clean-file review. | Run public repo checklist, then publish only after approval. |
| Visible OSI license | Satisfied locally | `LICENSE` is Apache-2.0. | Ensure it is included in public repo. |
| Text description | Satisfied locally | `submission_package/DEVPOST_DRAFT.md`. | Final tone/accuracy review before paste. |
| Public YouTube/Vimeo demo video | Link drafted / visibility still needs owner verification | Draft points to the correct video link: https://youtu.be/Old2pqRtC70. | Main must verify public/unlisted status and Devpost acceptability before final submission. |
| Completed Devpost form | Needs work / Ed approval | Draft content exists; hosted URL/video/repo gaps remain. | Fill and submit only after approval. |
| No secrets/private data exposed | Improved locally / final scan still required | Hosted demo uses deterministic sanitized proof data and makes no external calls. `.env` is ignored; raw proof JSON and Phoenix UI crops remain excluded from public page. | Run final scans/manual clean-file review before push/deploy/submit. |
