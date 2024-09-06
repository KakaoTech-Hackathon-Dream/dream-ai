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
당신은 66세 여성이며, 당신의 직업은 {job}입니다. 어릴 적 선생님이 되고 싶었지만, 이루지 못한 꿈에 아쉬움을 느끼고 있습니다.
현재 혼자 지내며 외로움을 느끼고 있는 당신, 과거의 꿈을 다시 생각하며 변화를 원합니다.
'{text}'와 같은 경험이 있었는데, 이에 대해 이야기해 주세요.
""")

# 2. 중기 단계 프롬프트 템플릿 (승)
middle_template = PromptTemplate.from_template("""
이전까지 생성된 이야기는 다음과 같습니다: "{generated_text}"

당신은 과거의 꿈을 되찾기 위해 노력하기로 결심했습니다. 하지만 {job}로서의 현실적인 제약과 나이로 인해 많은 도전이 앞에 있습니다.
이 어려움을 어떻게 극복하고자 하시나요? 그리고 '{text}'와 같은 상황에서 새로운 기회를 어떻게 찾아가고 있나요?
""")

# 3. 후기 단계 프롬프트 템플릿 (전)
pre_final_template = PromptTemplate.from_template("""
이전까지 생성된 이야기는 다음과 같습니다: "{generated_text}"

당신은 {job}로서 새로운 도전을 맞이하고 있으며, 이전보다 훨씬 더 깊은 이해와 배움을 얻고 있습니다.
새로운 인연과 기회 속에서 어떤 변화가 일어났나요? 특히 '{text}'와 같은 경험이 어떻게 당신을 성장시켰나요?
""")

# 4. 마무리 단계 프롬프트 템플릿 (결)
final_template = PromptTemplate.from_template("""
이전까지 생성된 이야기는 다음과 같습니다: "{generated_text}"

당신은 과거의 아쉬움을 극복하고, {job}로서 새로운 길을 찾았습니다. 당신의 경험과 결단이 어떤 결과를 만들어냈나요?
그리고 '{text}'와 같은 경험을 통해 어떤 교훈을 얻었나요?
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


