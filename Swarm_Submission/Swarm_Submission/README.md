# Swarm Alignment Sprint submission
Author: Urva Upadhyay, Parul University

## Offline reproduction
Run `python audit_results.py` from this folder. No packages or API keys are needed.

## Files
Research_Report.pdf is the submission report. Research_Report.docx is editable and derived from the official sprint template. data/ contains original recorded evidence. Experiment_Record.ipynb preserves the supplied notebook code with outputs and transient metadata removed.

## Live execution
The notebook is an archival development record, not a Run All notebook. It includes interactive manual practice, Colab-specific Drive paths, and API calls. Execute setup before experiment cells. Store GROQ_API_KEY in Colab Secrets. The model is openai/gpt-oss-20b. Calls may consume credits. Existing logs should be preserved, and reruns should use a new directory.

## Provenance
Experiments were conducted during the November 6–8 sprint. Groq SDK, model weights, Adaption platform, and official template are preexisting resources. AI assisted study design, implementation and writing. No public repository or deployment is included.

## Interpretation
The report separates development pilots, synthetic request corruption, and generated peer-message policy tests. Do not pool them into a single success rate. All token-truncated and malformed outcomes are retained. Generated style labels have known contamination.
