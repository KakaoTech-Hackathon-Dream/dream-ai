from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
# from services.nlp_service import extract_keywords
# from services.elasticsearch_service import search_resume_data
from services.llm_service import generate_story

# FastAPI 인스턴스 생성
app = FastAPI()

# Pydantic을 사용해 요청 모델 정의
class StoryRequest(BaseModel):
    input_text: str

# # 스토리 생성 엔드포인트 정의
# @app.post("/generate_story")
# async def generate_story_endpoint(request: StoryRequest):
#     try:
#         user_input = request.input_text

#         # 1. NLP로 키워드 추출
#         age, dream = extract_keywords(user_input)

#         # 2. Elasticsearch에서 자소서 검색
#         resume_data = search_resume_data(age, dream)

#         # 3. Langchain과 LLM을 이용해 스토리 생성
#         story = generate_story(user_input, resume_data)

#         # 결과 반환
#         return {"story": story}

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# uvicorn ai_server:app --reload