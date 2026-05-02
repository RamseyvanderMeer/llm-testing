# LLM Testing

An early LLM evaluation sandbox for comparing how different model providers handle structured data correction and self-evaluation tasks.

The project runs prompts through multiple providers, extracts JSON-like outputs, repairs malformed responses when possible, and records scores for later comparison. It was built to explore practical failure modes in LLM pipelines: invalid JSON, inconsistent scoring, brittle formatting, and evaluator disagreement.

## What It Explores

- Prompting LLMs to correct structured records
- Using a second model to evaluate generated corrections
- Recovering malformed JSON responses from model output
- Comparing model performance across providers and datasets
- Writing repeatable evaluation artifacts to JSON and CSV

## Providers / Backends

- OpenAI-style clients
- Anthropic-style clients
- Gemini-style experiments
- Local/open model experiments with Llama and Mistral-style folders

## Tech Stack

- Python
- Jupyter notebooks
- Provider-specific LLM client wrappers
- JSON/CSV evaluation outputs

## Notes

This is a research/prototyping repo rather than a polished product. The useful part is the evaluation pattern: run model output through a repeatable pipeline, repair what can be repaired, and make failures visible instead of manually inspecting every response.
