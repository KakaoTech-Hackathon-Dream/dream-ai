from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnableLambda
import os

# OpenAI API 설정
openai_api_key = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(api_key=openai_api_key, model="gpt-3.5-turbo")

# 1. 초기 단계 프롬프트 템플릿 (기)
initial_template = PromptTemplate.from_template("""
당신은 66세 여성입니다. 어릴 적 선생님이 되고 싶었지만, 이루지 못한 꿈에 아쉬움을 느끼고 있습니다.
현재 혼자 지내며 외로움을 느끼고 있는 당신, 과거의 꿈을 다시 생각하며 변화를 원합니다.
당신의 이야기를 시작해 보세요.
""")

# 2. 중기 단계 프롬프트 템플릿 (승)
middle_template = PromptTemplate.from_template("""
이전까지 생성된 이야기는 다음과 같습니다: "{generated_text}"

당신은 과거의 꿈을 되찾기 위해 노력하기로 결심합니다. 그러나 현실적인 제약과 나이로 인해 많은 도전이 앞에 있습니다.
이 어려움을 어떻게 극복하고자 하시나요? 그리고 새로운 기회를 어떻게 찾아가고 있나요?
""")

# 3. 말기 단계 프롬프트 템플릿 (결)
final_template = PromptTemplate.from_template("""
이전까지 생성된 이야기는 다음과 같습니다: "{generated_text}"

당신은 과거의 아쉬움을 극복하고, 새로운 길을 찾았습니다. 당신의 경험과 결단이 어떤 결과를 만들어냈나요?
그리고 당신은 어떤 교훈을 얻었나요? 이 이야기를 마무리해 주세요.
""")

# Runnable을 사용하여 프롬프트와 모델 실행을 체인으로 연결
initial_chain = RunnableLambda(lambda _: initial_template.format()) | llm

# 중기 및 말기 단계 프롬프트 템플릿에 generated_text를 포함
def create_completion_prompt(generated_text, template):
    return RunnableLambda(lambda _: template.format(generated_text=generated_text)) | llm

# 프롬프트 실행 및 content 추출
def generate_story(chain):
    response = chain.invoke({})
    return response.content  # 'content' 속성으로 접근

# 전체 스토리 생성 로직
def interactive_story_generation():
    # 1. 초기 단계 스토리 생성
    story_part = generate_story(initial_chain)
    print("Generated Story - Initial Phase:")
    print(story_part)
    
    full_story = story_part

    # 2. 중기 단계 스토리 생성
    user_input = input("이야기의 다음 부분을 진행하시겠습니까? (yes/no): ").lower()
    if user_input == 'yes':
        middle_chain = create_completion_prompt(full_story, middle_template)
        story_part = generate_story(middle_chain)
        full_story += "\n" + story_part
        print("\nGenerated Story - Middle Phase:")
        print(story_part)
    
    # 3. 말기 단계 스토리 생성
    user_input = input("이야기의 마지막 부분으로 넘어가시겠습니까? (yes/no): ").lower()
    if user_input == 'yes':
        final_chain = create_completion_prompt(full_story, final_template)
        story_part = generate_story(final_chain)
        full_story += "\n" + story_part
        print("\nGenerated Story - Final Phase:")
        print(story_part)

    # 전체 스토리 출력
    print("\n\n\n--------------------------------------")
    print(full_story)

# 스토리 생성 실행
interactive_story_generation()




