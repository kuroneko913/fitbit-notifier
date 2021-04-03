# Fitbit Notifier

## 概要

以下のようなFitbitのサマリーをツイートする。

```
本日(2021-04-03)の運動 from Fitbit

座っていた時間: 507分
軽い運動の時間: 3分
アクティブな運動の時間: 0分
激しい運動の時間: 0分

本日の歩数: 42歩 (0.029km)

消費カロリー: 791kcal (基礎代謝: 770kcal)
```

### トークン自動更新用ラムダ 
lambda/fitbit-api-token-refresh

### Twitter投稿
lambda/FitbitNotifier

## 前提条件

* 以下のpackageをインストールしたレイヤーを作成しておく。
    * boto3
    * requests
    * fitbit
    * twitter

* Fitbit APIを利用する準備が整っていること。
    
    * https://dev.fitbit.com/apps でアプリ登録をする
    * OAuth 2.0 tutorial page で以下の各種トークンを取得する。
        
        * CLIENT_ID
        * CLIENT_SECRET
        * ACCESS_TOKEN
        * REFRESH_TOKEN
        * BASIC_TOKEN (ヘッダーのBASICの部分のパラメータ)
* AWS SecretManagerにFitbitのTokenを登録しておく。
* Twitter APIのトークンをAWS SecretManagerに登録しておく。

    * API_KEY
    * API_SECRET
    * ACCESS_TOKEN
    * ACCESS_TOKEN_SECRET 

* AWS SecretManagerでFitbit Oauthトークンの自動更新を実行できるようにLambdaに権限を追加する。

[シークレットを自動的に更新するために必要なアクセス許可](https://docs.aws.amazon.com/ja_jp/secretsmanager/latest/userguide/rotating-secrets-required-permissions.html)

```
aws lambda add-permission --function-name '{lambda関数:fitbit-api-token-refreshのarn}' --principal secretsmanager.amazonaws.com --action lambda:InvokeFunction --statement-id 'SecretsManagerAccess'
```

* 定期実行する際は、AWS EventBridge に登録する。(以下の例では00:10に設定)

    * スケジュール式: cron(10 0 ? * *? *)
