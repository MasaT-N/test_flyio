# Fly.ioでの購買申請データ登録・参照アプリ

## 購買申請データ登録・参照アプリ(app.py)の要件
* コラボフローからWebhook送信されたデータをSqliteのpurchase_requisitionデータベースのテーブルに格納する。
* 登録されて蓄積したデータは、get_document_listエンドポイントにセキュリティキーをPOSTするとレスポンスをjsonとして受信できる。
* get_document_listで得たデータを用いて、update_downloadedエンドポイントで文書IDと対応するdownloadedの値をPOSTするとpurchase_requisitionテーブル上の該当レコードの値を更新することができる。
* get_document_listとupdate_downloadedの２つのエンドポイントについては、config.yamlに記述したセキュリティキー(secret_key)をPOST送信しなければエラーになるようにする。

#### リポジトリ内ファイルの説明
* app.py　・・・　Webアプリの本体(FASTAPI版)
* test_document_list.py ・・・ 登録された文書情報をリストで取得するサンプルコード
* test_update_downloades　・・・　文書IDと対応するdownloadedの値を更新するサンプルコード
* config.yaml.sample　・・・　デプロイ時にリネーム（.sampleを削除）して実運用のパラメータ値に書き換えてconfig.yamlとして保存する。
* requirements.txt　・・・　必要なPythonモジュールリスト。

