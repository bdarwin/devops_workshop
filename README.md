# Go East Travel Concierge — Agentic AI CI/CD Workshop

A small multi-agent travel concierge plus the CI/CD pipeline that ships it.

## The app

    static/index.html  front end
    app/main.py        backend API  (/chat, /healthz, /version)
    app/agents.py      supervisor + 5 specialist agents
    app/tools.py       mock external services
    app/prompts.py     prompts + agent config (versioned)
    app/llm.py         Claude, with an offline stub when no API key is set

A request flows: **supervisor classifies → specialist agent calls tools → reply
composed from tool facts only.**

| Intent | Agent | Tools |
|---|---|---|
| plan | planner | flights, hotels, weather |
| flight | flight_agent | flights, payments |
| hotel | hotel_agent | hotels, payments |
| advisory | advisory | weather, visa, insurance |
| disruption | rescue | rebooking, customer profile |

Prompt-injection attempts are blocked before routing.

## Run it

    make install
    make run        # http://localhost:8000

With no `ANTHROPIC_API_KEY` the app uses a deterministic stub, so it runs
offline and the pipeline costs nothing. Set the key to use Claude:

    export ANTHROPIC_API_KEY=sk-...

## Test it

    make test   # 15 tests
    make eval   # agent evaluation gate
    make lint

## The pipeline

`.github/workflows/pipeline.yml` — see [docs/pipeline.md](docs/pipeline.md).

    developer → repo → CI → tests → security → build → staging
              → agent eval → production → monitoring
