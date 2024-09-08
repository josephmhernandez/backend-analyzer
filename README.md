# backend-analyzer

Use LangChain to orchestrate workflows to analyze candidate digital footprints

uvicorn main:app --reload

Running AI model locally:
pipenv run python ./services/LangChain/Analyzer.py

Sample Request
curl -X POST http://127.0.0.1:8000/analyze-repository \
 -H "Content-Type: application/json" \
 -d '{"repoUrl": "https://github.com/josephmhernandez/SpatialRecognition", "repoName":"SpatialRecognition", "dbRepoId": "f4aedd2b-14e5-43e6-abab-aea1d598c733", "userId": "ee040e73-d678-4b95-b8f2-f3f8468ff2a8"}'


curl -X POST http://127.0.0.1:8000/analyze-repository \
 -H "Content-Type: application/json" \
 -d '{"repoUrl": "https://github.com/josephmhernandez/SkinCancerDetection", "repoName":"SkinCancerDetection", "dbRepoId": "28a3c30c-ff85-4d2e-8929-6baaaab0a09b", "userId": "ee040e73-d678-4b95-b8f2-f3f8468ff2a8"}'

Sample Response
curl -X POST http://127.0.0.1:8000/input-data-local \
 -H "Content-Type: application/json" \
 -d '{"user_id": "ee040e73-d678-4b95-b8f2-f3f8468ff2a8", "repo_id":"4687dc3c-e0e3-4e98-8e32-c324b4407124"}'

USER: ee040e73-d678-4b95-b8f2-f3f8468ff2a8 -> josephmhernandez15@gmail.com email
