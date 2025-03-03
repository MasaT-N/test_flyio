# Fly.io(render.comでもテスト中)での購買申請データ登録・参照アプリ

## 購買申請データ登録・参照アプリ(app.py)の要件
* コラボフローからWebhook送信されたデータをSqliteのpurchase_requisitionデータベースのテーブルに格納する。
* 登録されて蓄積したデータは、get_document_listエンドポイントにセキュリティキーをPOSTするとレスポンスをjsonとして受信できる。
* get_document_listで得たデータを用いて、update_downloadedエンドポイントで文書IDと対応するdownloadedの値をPOSTするとpurchase_requisitionテーブル上の該当レコードの値を更新することができる。
* get_document_listとupdate_downloadedの２つのエンドポイントについては、環境変数に記述したセキュリティキー(SECRET_KEY)をPOST送信しなければエラーになるようにする。

#### リポジトリ内ファイルの説明
* app.py　・・・　Webアプリの本体(FASTAPI版)
* test_document_list.py ・・・ 登録された文書情報をリストで取得するサンプルコード
* test_update_downloades　・・・　文書IDと対応するdownloadedの値を更新するサンプルコード
* config.yaml.sample　・・・　デプロイ時にリネーム（.sampleを削除）して実運用のパラメータ値に書き換えてconfig.yamlとして保存する。
* requirements.txt　・・・　必要なPythonモジュールリスト。

#### エンドポイントリスト
* '/' : ルート。データの総数とDBのサイズが表示される。
* '/submit' : コラボフローの承認データがポストされるエンドポイント
* '/get_document_list' : 登録された文書のリストを取得する。未ダウンロードは全てとダウンロード済みは100件まで
* '/update_downloaded' : 添付ファイルをダウンロードしたらフラグを更新するためのエンドポイント(document_idを必要とする。)
* '/init_db' : データベースを一旦クリアする。

#### render.comでの注意点
###### render.com上に設置したWebサイトは、15分間アクセスが無いと休止モードに入る。これを防ぐために、以下のサービスを利用して定期的に通信を確保する。
* cron-job.orgサービスを利用して、render.comのURLを定期的に叩く設定をする。
