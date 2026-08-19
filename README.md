# Hormozi-Inspired Business Strategy Assistant

This repo packages a local knowledge base of Alex Hormozi-style business education materials into a cloneable AI assistant starter kit.

It is designed for founders, creators, agencies, and operators who want a practical assistant for:

- Building Grand Slam-style offers
- Writing sales scripts and hooks
- Diagnosing pricing, proof, retention, and lead nurture
- Turning course transcripts and playbooks into searchable answers

Important: this project is not Alex Hormozi, is not affiliated with Alex Hormozi or Acquisition.com, and should not be used to impersonate him. The assistant should describe itself as a business strategy assistant trained on a provided knowledge base.

## What Is Inside

- `course-transcripts/` - long-form course transcripts
- `course-videos/` - offer and lead generation transcript files
- `playbooks/` - topic playbooks covering hooks, pricing, closing, retention, lead nurture, and more
- `prompts/` - reusable prompt templates
- `demos/` - example outputs
- `src/build_index.py` - chunks the knowledge base into a local JSONL index
- `src/ask.py` - retrieves relevant chunks and answers questions

## Quick Start

```bash
git clone <your-repo-url>
cd hormozi-assistant
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python src/build_index.py
python src/ask.py "Build me a Grand Slam Offer for a med spa AI appointment setter"
```

On macOS/Linux, activate the virtual environment with:

```bash
source .venv/bin/activate
```

## Optional: Use OpenAI For Full Answers

The assistant can run in two modes:

- Without `OPENAI_API_KEY`: shows the most relevant excerpts from the corpus.
- With `OPENAI_API_KEY`: uses retrieved excerpts to generate a practical answer.

```bash
set OPENAI_API_KEY=your_key_here
python src/ask.py "How should I raise prices without crushing conversion?"
```

On macOS/Linux:

```bash
export OPENAI_API_KEY=your_key_here
```

## Example Questions

```bash
python src/ask.py "Create a lead nurture sequence for a real estate AI setter"
python src/ask.py "Diagnose why my offer is not converting"
python src/ask.py "Give me 20 hooks for a bookkeeping automation agency"
python src/ask.py "What stage of scaling am I in if I have inconsistent fulfillment?"
```

## Safety And Identity Rules

Use this repo to build an assistant inspired by publicly discussed business frameworks. Do not present generated answers as if they came from Alex Hormozi personally.

Recommended assistant framing:

> I am a business strategy assistant trained on a Hormozi-style knowledge base. I am not Alex Hormozi and I am not affiliated with him.

## Content Rights

Before publishing this repository publicly, confirm you have the rights to distribute every transcript and playbook included here. If you do not, keep the repo private or replace raw transcripts with your own notes, summaries, or links to authorized source material.

## Rebuild The Index

Run this after adding or editing source files:

```bash
python src/build_index.py
```

The generated index is written to `data/index.jsonl` and ignored by git.
