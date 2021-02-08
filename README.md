# Coecara Summarize API

良い感じに文章を整えてくれる・音声文字起こしサービスコエカラ(Coecara)の要約APIです。  
Mecabで形態素解析した結果を LexRank・tf-idfを使って要約しています。  

デモ： https://coecara.com/


## 環境
- Python3.8
- Amazon API Gateway
- AWS Lambda
- Amazon EFS


## デプロイ
src/functionsはzipファイルにしてAWS管理画面よりアップロード。
Mecabやその他のPythoパッケージをビルドしてLambdaから呼びだせるようにするにはこちらを参照。
https://qiita.com/rtaguchi/items/f2b39572299b5399df76