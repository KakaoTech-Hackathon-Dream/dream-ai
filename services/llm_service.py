from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnableLambda
from dotenv import load_dotenv
import os

load_dotenv()

# OpenAI API 설정
openai_api_key = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(api_key=openai_api_key, model="gpt-3.5-turbo")

# 1. 초기 단계 프롬프트 템플릿 (기)
initial_template = PromptTemplate.from_template("""
너는 오랫동안 {job}가 되고 싶었어 
드디어 내일이면 처음으로 근무를 하게 되었어 너는 어떤 상황에 놓여있고 해당 상황에 어떤 생각 중인지 딱딱하지 않게 일기처럼 이야기 해줘
""")

# 2. 중기 단계 프롬프트 템플릿 (승)
middle_template = PromptTemplate.from_template("""
"{generated_text}"
위의 이야기에서 자연스럽게 이어지게
시간이 꽤 지나고 {job}에 조금은 능숙해진 너는 어떤 상황에 놓여있고 해당 상황에 어떤 생각 중인지 딱딱하지 않게 일기처럼 이야기 해줘
""")

# 3. 후기 단계 프롬프트 템플릿 (전)
pre_final_template = PromptTemplate.from_template("""
"{generated_text}"
위의 이야기에서 자연스럽게 이어지게
이제는 선배 축에 속할만큼 {job}에 능숙해진 너는 어떤 상황에 놓여있고 해당 상황에 어떤 생각 중인지 딱딱하지 않게 일기처럼 이야기 해줘
""")

# 4. 마무리 단계 프롬프트 템플릿 (결)
final_template = PromptTemplate.from_template("""
"{generated_text}"
위의 이야기에서 자연스럽게 이어지게
{job}에서 은퇴를 앞둔 너는 어떤 상황에 놓여있고 해당 상황에 어떤 생각 중인지 딱딱하지 않게 일기처럼 이야기 해줘
""")

# Runnable을 사용하여 프롬프트와 모델 실행을 체인으로 연결
def initial_chain(job, text, doc_content):
    return RunnableLambda(lambda _: initial_template.format(job=job, text=text, doc_content=doc_content)) | llm

# 중기, 후기, 결 단계 프롬프트 템플릿에 generated_text, job, text, doc_content를 포함하는 함수
def create_completion_prompt(generated_text, job, text, doc_content, template):
    return RunnableLambda(lambda _: template.format(generated_text=generated_text, job=job, text=text, doc_content=doc_content)) | llm

# 프롬프트 실행 및 content 추출
def generate_story(chain):
    response = chain.invoke({})
    return response.content  # 'content' 속성으로 접근

# 전체 스토리 생성 로직
def interactive_story_generation(job, text, doc_content, current_index):
    flag = False
    full_story = ""

    # 1. 초기 단계 스토리 생성 (기)
    if current_index == 0:
        initial_chain = create_completion_prompt(text, job, text, doc_content, initial_template)
        story_part = generate_story(initial_chain)
        full_story = story_part

    # 2. 중기 단계 스토리 생성 (승)
    elif current_index == 1:
        middle_chain = create_completion_prompt(full_story, job, text, doc_content, middle_template)
        story_part = generate_story(middle_chain)
        full_story += "\n" + story_part

    # 3. 후기 단계 스토리 생성 (전)
    elif current_index == 2:
        pre_final_chain = create_completion_prompt(full_story, job, text, doc_content, pre_final_template)
        story_part = generate_story(pre_final_chain)
        full_story += "\n" + story_part

    # 4. 마무리 단계 스토리 생성 (결)
    elif current_index == 3:
        final_chain = create_completion_prompt(full_story, job, text, doc_content, final_template)
        story_part = generate_story(final_chain)
        full_story += "\n" + story_part
        flag = True  # 결 단계에서만 flag True로 설정

    # 전체 스토리, flag, index 반환
    return full_story, flag, current_index + 1


