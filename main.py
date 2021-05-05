import io
import streamlit as st
import requests
import json
from PIL import Image
from PIL import ImageDraw

st.title('顔認識アプリ')  #タイトル

#Microsoft API情報
with open('D:/Python_Exanmple/streamlit-MS API/secret.json') as f:
    secret_json = json.load(f)
subscription_key = secret_json['subscription_key']
assert subscription_key

face_api_url ='https://20210501ozasa.cognitiveservices.azure.com/face/v1.0/detect'

# 画像のアップロード
upload_file = st.file_uploader("Choose an image....",type='jpg')

#imgに画像ファイルを入れる
#upload_fileが入っていたら
if upload_file is not None:
    img = Image.open(upload_file)
    
    with io.BytesIO() as output:
          img.save(output,format="JPEG")
          binary_img = output.getvalue()
    
    headers = {
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': subscription_key}

    params = {
        'returnFaceId': 'true',
        'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise'
        }

    res = requests.post(face_api_url, params=params,headers=headers, data = binary_img)
    results = res.json()

    for result in results:
    	rect = result['faceRectangle']

    	draw = ImageDraw.Draw(img)
    	draw.rectangle([(rect['left'],rect['top']),(rect['left']+rect['width'],rect['top']+rect['height'])],fill=None,outline='green',width=5)
    
    	text =  result['faceAttributes']['gender'] + '/' + str(result['faceAttributes']['age']) #性別/年齢
    	draw.text((rect['left'] -15,rect['top'] -12), text, fill='#FFF')

    st.image(img,caption = 'Uploaded Image.',use_column_width=True)
