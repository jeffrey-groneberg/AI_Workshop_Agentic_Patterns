# References

A curated collection of resources for deepening your understanding of agentic AI patterns.

## OpenAI

- [Chat Completions API Guide](https://platform.openai.com/docs/guides/text-generation) — Primary API used in this workshop
- [Function Calling Guide](https://platform.openai.com/docs/guides/function-calling) — Tool definitions and usage
- [Structured Outputs Guide](https://platform.openai.com/docs/guides/structured-outputs) — `response_format` with Pydantic
- [Responses API Guide](https://platform.openai.com/docs/guides/responses-vs-chat-completions) — OpenAI's new primary API
- [API Reference](https://platform.openai.com/docs/api-reference/chat) — Complete API documentation
- [OpenAI Cookbook](https://cookbook.openai.com/) — Practical examples and recipes
- [Tokenizer Tool](https://platform.openai.com/tokenizer) — Visualize how text is tokenized
- [Model Overview](https://platform.openai.com/docs/models) — Available models and capabilities

## Microsoft / Azure

- [AI Agent Design Patterns (MS Learn)](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns) — The primary reference for orchestration patterns in this workshop
- [Azure OpenAI Service Documentation](https://learn.microsoft.com/en-us/azure/ai-services/openai/) — Azure-hosted OpenAI models
- [Azure AI Foundry](https://learn.microsoft.com/en-us/azure/ai-studio/) — Model deployment and management
- [Semantic Kernel](https://learn.microsoft.com/en-us/semantic-kernel/overview/) — Microsoft's enterprise AI orchestration SDK for Python, .NET, and Java
- [Azure AI Agent Service](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/) — Managed service for building and deploying AI agents at scale in Azure AI Foundry
- [Microsoft Agent Framework](https://learn.microsoft.com/en-us/agent-framework/) — Next-gen multi-language SDK (Python + .NET) combining AutoGen and Semantic Kernel; supports sequential, concurrent, group chat, and handoff patterns

## Anthropic / Claude

- ["Building Effective Agents"](https://www.anthropic.com/engineering/building-effective-agents) — Excellent overview of agent patterns including evaluator-optimizer and tool use
- [Prompt Engineering Guide](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering) — Best practices for writing effective prompts

## Blog Posts & Articles

- [Lilian Weng — "LLM Powered Autonomous Agents"](https://lilianweng.github.io/posts/2023-06-23-agent/) — Comprehensive survey of agent architectures, planning, memory, and tool use
- [Chip Huyen — "Building a Generative AI Platform"](https://huyenchip.com/2024/07/25/genai-platform.html) — Production considerations for AI systems

## YouTube / Video

- [Andrej Karpathy — "Intro to Large Language Models"](https://www.youtube.com/watch?v=zjkBMFhNj_g) — Foundational understanding of how LLMs work
- [Andrew Ng — "What's next for AI agentic workflows"](https://www.youtube.com/watch?v=sal78ACtGTc) — Overview of agentic design patterns (reflection, tool use, planning, multi-agent)
- [Sam Witteveen — Multi-Agent Systems](https://www.youtube.com/@samwitteveenai) — Practical tutorials on building multi-agent systems

## Research Papers

- [ReAct: Synergizing Reasoning and Acting in Language Models (Yao et al., 2023)](https://arxiv.org/abs/2210.03629) — The foundational Reason-Act-Observe loop used in our agent abstraction
- [Reflexion: Language Agents with Verbal Reinforcement Learning (Shinn et al., 2023)](https://arxiv.org/abs/2303.11366) — Self-reflection and self-evaluation patterns; basis for the maker-checker exercise
- [CAMEL: Communicative Agents for "Mind" Exploration (Li et al., 2023)](https://arxiv.org/abs/2303.17760) — Multi-agent collaboration and communication protocols
- [Toolformer: Language Models Can Teach Themselves to Use Tools (Schick et al., 2023)](https://arxiv.org/abs/2302.04761) — How models learn to use tools effectively
- [Chain-of-Thought Prompting (Wei et al., 2022)](https://arxiv.org/abs/2201.11903) — Step-by-step reasoning that improves complex task performance

## Python Libraries Used

- [OpenAI Python SDK](https://github.com/openai/openai-python) — `pip install openai`
- [Pydantic](https://docs.pydantic.dev/latest/) — Data validation and settings management
- [python-dotenv](https://github.com/theskumar/python-dotenv) — `.env` file loading
- [MKDocs Material](https://squidfunk.github.io/mkdocs-material/) — Documentation theme

## Frameworks (for Reference)

These frameworks implement the patterns taught in this workshop. Understanding the patterns from scratch makes you a more effective user of any of these:

- [Microsoft Agent Framework](https://learn.microsoft.com/en-us/agent-framework/) — The next-generation multi-language SDK (Python + .NET) for building AI agents and multi-agent workflows, created by the AutoGen and Semantic Kernel teams. Supports sequential, concurrent, group chat, and handoff patterns with graph-based orchestration, session state management, and MCP tool integration
- [LangGraph](https://langchain-ai.github.io/langgraph/) — Graph-based agent orchestration (state machines, conditional routing)
- [Pydantic AI](https://ai.pydantic.dev/) — Type-safe agent framework built on Pydantic
- [CrewAI](https://docs.crewai.com/) — Role-based multi-agent orchestration
