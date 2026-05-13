# TracePilot Devpost requirements matrix

Known requirement source: local Devpost/rules notes for the Google Cloud Rapid Agent Hackathon / Arize track.

| Requirement | Current status | Evidence / note | Next action |
| --- | --- | --- | --- |
| Select Arize track | Ed approval | Draft positions TracePilot for Arize/Phoenix track. | Select track in Devpost only after approval. |
| Functional agent powered by Gemini | Satisfied locally | Verified run used Gemini via Google ADK; latest fixed model version recorded as `gemini-2.5-flash`. | Keep wording exact; do not overclaim hosted production. |
| Google Cloud Agent Builder / Agent Builder wording | Resolved with caveat | `AGENT_BUILDER_ELIGIBILITY_NOTE.md` documents that TracePilot uses Google ADK + Gemini and that Google documents ADK under Gemini Enterprise Agent Platform / Agent Platform. Risk remains if judges require a deployed Agent Builder/Agent Runtime resource. | Use conservative ADK/Gemini wording, or after approval execute the `GOOGLE_AGENT_PLATFORM_DEPLOYMENT_STUB.md` path before claiming Agent Builder deployment. |
| Meaningful Arize/Phoenix integration | Satisfied locally | OpenInference/Phoenix traces plus Phoenix MCP retrieval; canonical trace `52fa8eaf399d8cc4251a9e7f8441a903`. | Use sanitized proof table and video; avoid raw JSON public dump. |
| More than simple chat/tool-use | Satisfied locally | TracePilot scores task completion, diagnoses failures, emits refined task, and shows 71→71→100 improvement. | Present as operator loop above the agent. |
| Runs on web/Android/iOS | Satisfied / verified hosted web | Static `web_demo/` shell is deployed on Cloud Run and can run in desktop/mobile browsers. | Use verified hosted URL. |
| Hosted project URL | Satisfied / verified | Cloud Run public URL verified: https://tracepilot-demo-thryhyeqga-uc.a.run.app | Include URL in Devpost. |
| Public open-source repo | In progress / approved to publish candidate | Repo has Apache-2.0 license and sanitized candidate package. | Fresh scan and publish candidate to GitHub. |
| Visible OSI license | Satisfied locally | `LICENSE` is Apache-2.0. | Ensure it is included in public repo. |
| Text description | Satisfied locally | `submission_package/DEVPOST_DRAFT.md`. | Final tone/accuracy review before paste. |
| Public YouTube/Vimeo demo video | Needs work / Ed approval | Preferred local candidate: `demo_media_package/first_plus_phoenix/tracepilot_demo_first_plus_phoenix_fixed.mp4`. Not uploaded. | Review video, upload only after approval, verify public link. |
| Completed Devpost form | Needs work / Ed approval | Draft content exists; hosted URL is complete; repo/video links still need final verification. | Fill and submit only after repo/video links are verified and Ed approves final submit. |
| No secrets/private data exposed | Risky until final scan | `.env` is ignored; raw proof JSON and Phoenix UI crops may contain internal metadata. | Run scans and manual clean-file review before any public action. |
