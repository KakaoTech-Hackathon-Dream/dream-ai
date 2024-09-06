#!/bin/bash

runNetwork(){
  # 네트워크가 존재하는지 확인
  if [ -z "$(docker network ls | grep dream)" ]
  then
      echo "dream 네트워크를 생성합니다."
      docker network create dream
  else
      echo "dream 네트워크가 이미 존재합니다."
  fi

  if [ -z "$(docker network ls | grep datasource)" ]
    then
        echo "datasource 네트워크를 생성합니다."
        docker network create datasource
    else
        echo "datasource 네트워크가 이미 존재합니다."
    fi
}

serviceDown(){
  if [ $(docker ps -a -q -f name=$CONTAINER_NAME) ]
  then
      echo "컨테이너 $CONTAINER_NAME 종료 및 삭제 중..."

      IMAGE_ID=$(docker images -q $CONTAINER_NAME)

      if [ "$IMAGE_ID" ]; then
          echo "이미지 $CONTAINER_NAME 삭제 중..."

      docker rmi -f $IMAGE_ID
      fi
  fi
}

cleanUpImages(){
  docker rmi $(docker images -f "dangling=true" -q)
  sudo docker system prune -af
}


runNetwork

cd /home/ubuntu/deploy-ai
mv env .env
serviecDown ai
docker-compose up -d --build

cleanUpImages


