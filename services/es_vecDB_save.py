from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer

# Elasticsearch 연결 설정
es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])

# 사전 학습된 Sentence-BERT 모델 로드
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

# 인덱스 이름 설정
index_name = 'biographies_vecdb'

# # 인덱스 매핑 설정 (384 차원으로 수정)
# mapping = {
#     "mappings": {
#         "properties": {
#             "content": {
#                 "type": "text"
#             },
#             "content_vector": {
#                 "type": "dense_vector",
#                 "dims": 384  # 모델의 벡터 차원을 384로 설정
#             },
#             "title": {
#                 "type": "text"
#             }
#         }
#     }
# }

# # 인덱스 생성 (필요시)
# if not es.indices.exists(index=index_name):
#     es.indices.create(index=index_name, body=mapping)

# print("인덱스가 384 차원으로 생성되었습니다.")

# 자서전 데이터 예시
biographies = [
    {
        "title": "나의 교직 생활",
        "content": """
        나는 1980년대에 교직에 들어서면서 처음으로 초등학교 교사로 근무를 시작했습니다. 
        학생들과의 첫 만남은 잊을 수 없는 경험이었고, 그들의 눈빛 속에서 호기심과 열정을 보았습니다. 
        교사로서의 삶은 항상 도전적이었지만, 학생들의 성장을 직접 목격하며 보람을 느꼈습니다. 
        특히, 나는 과학 교육에 많은 관심을 가지고 있어 학생들에게 실험과 탐구 학습을 적극적으로 도입하려 노력했습니다.
        30년 동안의 교직 생활 동안, 수많은 제자들이 사회에서 훌륭한 성과를 내는 것을 볼 수 있었습니다.
        이 경험은 교사로서의 삶이 단순한 직업이 아닌 소명의 길이라는 것을 깨닫게 해주었습니다.
        """
    },
    {
        "title": "나의 의사 생활",
        "content": """
        나는 1990년대에 의학을 전공하고 처음으로 병원에서 근무를 시작했습니다. 
        환자들을 치료하는 과정에서 생명을 다루는 책임감을 크게 느꼈으며, 그들이 회복하는 모습을 보면서 보람을 느꼈습니다. 
        특히, 나는 내과 진료에 관심이 많아 다양한 환자의 질병을 진단하고 치료하는 데 집중했습니다.
        또한, 나는 의학 연구에도 참여하여 새로운 치료법 개발에 기여하려고 노력했습니다.
        25년간의 의사 생활 동안 수많은 환자들을 만나고 그들의 삶의 질을 향상시키는 데 도움을 줄 수 있었습니다.
        이 경험은 나의 인생에서 가장 중요한 가치 중 하나가 되었고, 의료 분야에서 계속 발전하고자 하는 동기가 되었습니다.
        """
    },
    {
        "title": "무역가의 길",
        "content": """
        2000년에 나는 국제 무역 회사에서 일을 시작하며 처음으로 무역 업계에 발을 들였습니다. 
        세계 각국과의 거래를 통해 다양한 문화와 경제적 이해를 넓혔고, 이를 바탕으로 나는 점점 더 큰 프로젝트를 맡게 되었습니다.
        특히, 나는 아시아와 유럽 시장 간의 무역 관계를 주도하며 회사의 성장을 이끌었습니다.
        20년 동안의 무역가 생활은 매우 도전적이었지만, 동시에 보람찬 경험이었습니다. 
        다양한 국가와의 협상을 통해 얻은 인사이트는 내가 계속해서 이 분야에서 성공할 수 있는 기반이 되었습니다.
        """
    }
]


# 텍스트를 벡터로 변환 (384 차원)
biography_texts = [f"{bio['title']}: {bio['content']}" for bio in biographies]
biography_vectors = model.encode(biography_texts)

# 벡터 데이터를 Elasticsearch에 저장
for i, (bio, bio_vector) in enumerate(zip(biographies, biography_vectors)):
    doc = {
        "title": bio['title'],
        "content": bio['content'],
        "content_vector": bio_vector.tolist()  # 벡터 데이터를 리스트로 변환하여 저장
    }
    res = es.index(index=index_name, id=i+1, body=doc)
    print(f"Document {i+1} indexed: {res['result']}")
    
