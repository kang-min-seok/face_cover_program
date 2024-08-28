# 🚀자동으로 얼굴 가려주는 파이썬 프로그램

블로그를 작성하거나 SNS에 이미지를 올릴때 다른 사람들의 얼굴을 쉽고 빠르게 가려주는 프로그램입니다.<br><br>

## ⚙️세팅방법
### 설치해야할 라이브러리
```pip install opencv-python```<br>
```pip install face_recognition```<br>
```pip install retinaface```<br><br>
### ⚠️주의할 점<br>
face_recognition이나 retinaface설치가 안되면 CMake문제이니 정상적으로 설치해야함.<br><br>
```Window```는 ```Visual studio installer```에서 ```Windows용 C++ CMake 도구``` 설치하고 https://cmake.org/download/ 링크로 들어가서 ```Latest Release``` 버전으로 ```Windows x64 Installer```
설치하고 환경변수 설정하면 됨<br><br>
```Mac```은 ```pip install cmake```절대 하면 안되고 ```brew install cmake```로 설치해야함.
## 🔗사용방법
1. ```input_images```폴더안에 작업하고 싶은 이미지들을 집어넣는다.
2. 취향에 맞게 ```faceRecognitionTest``` 혹은 ```retinafaceTest```를 실행한다.
3. 작업이 끝나면 ```output_images```에 저장이 완료된다.


## 🖥️faceRecognitionTest
![얼굴인식](https://github.com/user-attachments/assets/0988b4a7-cd11-4cdf-8545-7211828d5868)

> [블로그 설명](https://velog.io/@min1042004/%ED%8C%8C%EC%9D%B4%EC%8D%AC-openCV-%ED%99%9C%EC%9A%A9%ED%95%B4%EC%84%9C-%EC%96%BC%EA%B5%B4-%EC%9D%B8%EC%8B%9D%ED%95%98%EA%B3%A0-%EA%B0%80%EB%A0%A4%EC%A3%BC%EB%8A%94-%EC%BD%94%EB%93%9C)

해당 코드는 얼굴 검출 라이브러리를 통해 1차적으로 가려내고 부족한 부분은 추가로 작업하는 코드입니다.<br>
그러니 정확하게 작업하고 싶을때 권장드립니다.


## 🖥️retinafaceTest
<img src="https://github.com/user-attachments/assets/0855b4a7-5d4d-4ff6-887b-4d6839ae0c85"  width="800"/>

![retinaface_video](https://github.com/user-attachments/assets/6d6e3074-dc54-497e-a6aa-596d4169c0c2)


> [블로그 설명](https://velog.io/@min1042004/%ED%8C%8C%EC%9D%B4%EC%8D%AC-openCV-%ED%99%9C%EC%9A%A9%ED%95%B4%EC%84%9C-%EC%96%BC%EA%B5%B4-%EC%9D%B8%EC%8B%9D%ED%95%98%EA%B3%A0-%EA%B0%80%EB%A0%A4%EC%A3%BC%EB%8A%94-%EC%BD%94%EB%93%9CRetinaface)

해당 코드는 딥러닝을 통해 얼굴을 검출해내는 라이브러리를 사용했습니다.<br><br>
그만큼 정확도가 뛰어나지만 속도가 느린게 단점입니다.<br><br>
손 안대고 많은 이미지를 모두 작업하고 싶을때 권장드립니다.<br>
