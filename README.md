# backend-analyzer

Use LangChain to orchestrate workflows to analyze candidate digital footprints

uvicorn main:app --reload


Sample Request
curl -X POST http://127.0.0.1:8000/analyzeRepository \
     -H "Content-Type: application/json" \
     -d '{"username": "josephmhernandez", "repository_name":"lyfe-captures"}'