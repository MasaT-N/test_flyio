# ベースイメージ
FROM python:3.9-slim-buster

# 作業ディレクトリ
WORKDIR /app

# 依存関係のインストール
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt && rm -rf /root/.cache

# アプリケーションコードのコピー
COPY . .

# 実行コマンド
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
