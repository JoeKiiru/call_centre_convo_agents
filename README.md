# Conversational AI Agent for Customer Support Analytics

**Candidate:** Joseph Kiiru  
**Submission Deadline:** Monday, 8:00 AM  
**Estimated Time:** 8-12 hours  

---

## Overview

Welcome to this conversational AI portfolio project. This repository demonstrates building tools that analyze customer support conversations and extract useful insights such as sentiment, quality scores, and recommendations.

The goal is to showcase design and implementation of production-friendly AI components using modern Python frameworks.

---

## Business Context

This project processes customer support conversations (calls and chats) and demonstrates an AI agent that can:

1. **Analyze individual conversations** - sentiment, key issues, resolution status
2. **Answer questions about conversation data** - using natural language queries
3. **Generate quality assurance scores** - automated scoring based on configurable criteria
4. **Provide recommendations** - actionable insights for support team improvement
5. **Perform specialized ML inference** - using domain-specific models for enhanced accuracy
# Conversation Agents — Portfolio Project

This repository contains a compact example project that demonstrates building AI-powered conversational tools for analyzing customer support transcripts. It includes Pydantic models, a small agent composition using Pydantic-AI, a FastAPI interface, and a lightweight Hugging Face integration for inference.

This copy has been refactored for use as a portfolio project — company-specific references were removed and code was annotated with docstrings and comments to explain design decisions.

Features
- Domain models for conversations and messages
- An analysis agent that produces structured conversation insights
- A QA scoring agent for basic quality-assurance metrics
- A simple Hugging Face-based sentiment inference service
- FastAPI endpoints demonstrating async inference and validation

Quick start

Use the included `Makefile` to create a virtual environment, install dependencies, run the app, and run tests.

```bash
make init      # create venv and install requirements
make run       # start the API (no need to activate the venv manually)
make test      # run the test suite
```

Run tests

```bash
pytest
```

Notes
- This repository is a compact educational/portfolio example — models are loaded from Hugging Face and may require network access the first time they are used.
- See `docs/ARCHITECTURE.md` for decisions and rationale.

If you'd like, I can also:
- run the test suite locally and report results
- further tidy module names or update packaging for PyPI
- add a short demo script that exercises the API