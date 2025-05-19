新商品情報収集ツール
このツールは、飲料メーカーのウェブサイトから新商品の情報を自動で集めて、Excelファイルに保存します。サントリーやアサヒの新商品情報を簡単にチェックできます！
このツールでできること

ウェブサイトから新商品の発売日、商品名、品目、リンクを収集。
データをnew_releases_test.xlsxというExcelファイルに整理。
すでに登録済みの情報は重複しないように追加。

必要なもの

パソコン: Windows 10/11 または Mac。
インターネット接続: ウェブサイトから情報を取得するため。
Chromeブラウザ: 最新バージョン。
約20～30分: 初回のセットアップ時間。

セットアップ手順（初めて使う人向け）
以下の手順を一つずつ進めてください。プログラミングの知識は不要です！
ステップ1: ファイルを準備する

メールで送られたrelease_tracker.zipをデスクトップに保存。
Windows: ファイルを右クリックして「すべて展開」を選択して解凍。Mac: ファイルをダブルクリックして解凍。
release_trackerフォルダができます。


フォルダの中身を確認：
main.py: メインのプログラム
scrapersフォルダ: 各メーカーのデータ収集プログラム
new_releases_test.xlsx: 結果を保存するExcelファイル
requirements.txt: 必要なツールのリスト
run.bat: Windowsで簡単に実行するファイル
run.command: Macで簡単に実行するファイル



ステップ2: Pythonをインストールする（Anacondaを推奨）
このツールは「Python」という無料ソフトで動きます。以下の2つの方法から選べます。Anaconda（方法A）が簡単です。
方法A: Anacondaをインストール（推奨）
Windows:

ウェブブラウザでAnacondaの公式サイトを開く。
「Individual Edition」を選び、Windows用の「Download」ボタンをクリック（Python 3.xバージョン）。
ダウンロードしたファイル（例: Anaconda3-2025.04-Windows-x86_64.exe）をダブルクリック。
画面の指示に従ってインストール：
「Next」を押して進む。
インストール先はデフォルト（C:\Users\YourName\anaconda3）でOK。
「Add Anaconda to PATH」にチェックを入れる（推奨）。
所要時間: 5～10分。


インストール後、スタートメニューから「Anaconda Prompt」を開き、以下のコマンドで確認：python --version


出力例: Python 3.12.x



Mac:

ウェブブラウザでAnacondaの公式サイトを開く。
「Individual Edition」を選び、Mac用の「Download」ボタンをクリック（Python 3.xバージョン）。
ダウンロードしたファイル（例: Anaconda3-2025.04-MacOSX-x86_64.pkg）をダブルクリック。
画面の指示に従ってインストール：
「次へ」を押して進む。
インストール先はデフォルト（/Users/yourname/anaconda3）でOK。
所要時間: 5～10分。


インストール後、Launchpadで「ターミナル」を検索して開き、以下のコマンドで確認：python3 --version


出力例: Python 3.12.x



方法B: 標準Pythonをインストール
Windows:

ウェブブラウザでPython公式サイトを開く。
「Python 3.12.x」の「Download」ボタンをクリック（Windows用のインストーラ）。
ダウンロードしたファイル（例: python-3.12.7-amd64.exe）をダブルクリック。
インストール時に「Add Python 3.12 to PATH」にチェックを入れて「Install Now」をクリック。
インストール後、Windowsキーを押して「cmd」と検索してコマンドプロンプトを開き、以下のコマンドで確認：python --version


出力例: Python 3.12.x



Mac:

ウェブブラウザでPython公式サイトを開く。
「Python 3.12.x」の「Download」ボタンをクリック（macOS用のインストーラ）。
ダウンロードしたファイル（例: python-3.12.7-macosx.pkg）をダブルクリック。
画面の指示に従ってインストール。
インストール後、ターミナルで以下のコマンドで確認：python3 --version


出力例: Python 3.12.x



ステップ3: Chromeブラウザを準備する

Google Chromeがインストール済みか確認。なければこちらからダウンロード。
Chromeを最新バージョンに更新：
Chromeの右上「メニュー」（3つの点）→「ヘルプ」→「Google Chromeについて」。
自動で更新され、再起動が必要な場合は指示に従う。



ステップ4: ツールのセットアップを行う
PythonまたはAnacondaをインストールしたら、ツールを動かす準備をします。
方法A: Anacondaを使う場合
Windows:

スタートメニューから「Anaconda Prompt」を検索して開く。
release_trackerフォルダに移動：cd %USERPROFILE%\Desktop\release_tracker


以下のコマンドを1行ずつコピー＆ペーストしてEnter：conda create -n coca-py312 python=3.12
conda activate coca-py312
pip install -r requirements.txt
pip install webdriver-manager


コマンドの意味:
1行目: 新しい環境（coca-py312）を作成。
2行目: 環境を有効化（(coca-py312)と表示される）。
3～4行目: 必要なツール（ライブラリ）をインストール。


所要時間: 5～15分（インターネット速度による）。
エラーが出たら、スクリーンショットを撮って送ってください！



Mac:

Launchpadで「ターミナル」を検索して開く。
release_trackerフォルダに移動：cd ~/Desktop/release_tracker


以下のコマンドを1行ずつ入力：conda create -n coca-py312 python=3.12
conda activate coca-py312
pip install -r requirements.txt
pip install webdriver-manager


所要時間: 5～15分。



方法B: 標準Pythonを使う場合
Windows:

Windowsキーを押して「cmd」と検索し、コマンドプロンプトを開く。
release_trackerフォルダに移動：cd %USERPROFILE%\Desktop\release_tracker


仮想環境を作成：python -m venv venv
venv\Scripts\activate


(venv)と表示されれば成功。


ライブラリをインストール：pip install -r requirements.txt
pip install webdriver-manager


所要時間: 5～10分。



Mac:

Launchpadで「ターミナル」を検索して開く。
release_trackerフォルダに移動：cd ~/Desktop/release_tracker


仮想環境を作成：python3 -m venv venv
source venv/bin/activate


(venv)と表示されれば成功。


ライブラリをインストール：pip install -r requirements.txt
pip install webdriver-manager


所要時間: 5～10分。



ステップ5: ツールを実行する
準備ができたら、ツールを動かします。以下のいずれかの方法を選んでください。
方法1: ダブルクリックで実行
Windows:

release_trackerフォルダ内のrun.batをダブルクリック。
黒い画面（コマンドプロンプト）が開き、自動でデータ収集が始まります。
処理が終わると「完了しました。Enterで終了」と表示されるので、Enterキーを押して閉じる。
デスクトップのマクロフォルダにあるnew_releases_test.xlsxを開いて、結果を確認！

Mac:

release_trackerフォルダ内のrun.commandをダブルクリック。
初回は「ターミナルにアクセス権限を許可」するよう求められる場合があります。指示に従って許可。


ターミナルが開き、自動でデータ収集が始まります。
処理が終わると「完了しました。Enterで終了」と表示されるので、Enterキーを押して閉じる。
デスクトップのマクロフォルダにあるnew_releases_test.xlsxを開いて、結果を確認！

方法2: コマンドラインで実行
Windows:

Anaconda Prompt（またはコマンドプロンプト）で環境を有効化：
Anaconda: conda activate coca-py312
標準Python: venv\Scripts\activate


以下のコマンドを入力：cd %USERPROFILE%\Desktop\release_tracker
python main.py



Mac:

ターミナルで環境を有効化：
Anaconda: conda activate coca-py312
標準Python: source venv/bin/activate


以下のコマンドを入力：cd ~/Desktop/release_tracker
python main.py



結果の確認

new_releases_test.xlsx（デスクトップのマクロフォルダ内）には、以下のようなデータがシート（Asahi, Suntoryなど）ごとに保存されます：
発売日
商品名
品目
リンク


新しいデータだけが追加され、過去のデータは保持されます。

よくある問題と解決方法

「run.bat/run.commandが開かない」:
Windows: run.batを右クリック→「管理者として実行」を試す。
Mac: run.commandを右クリック→「情報を見る」→「すべての人」に読み書き権限を付与。ターミナルでchmod +x run.commandを実行。
または、方法2（コマンドライン）で実行。


「ChromeDriverエラー」:
Chromeブラウザが最新か確認。
Windows: Anaconda Promptでpip install webdriver-managerを再実行。
Mac: ターミナルでpip install webdriver-managerを再実行。


「Excelファイルが見つからない」:
new_releases_test.xlsxがデスクトップのマクロフォルダにあるか確認。
フォルダがない場合、デスクトップにマクロフォルダを作成し、ファイルを移動。


エラーメッセージが出た:
エラーのスクリーンショットをメールで送ってください。すぐにサポートします！



注意

初回実行時はウェブページの読み込みに時間がかかる場合があります（数分程度）。
Excelファイルは実行前に閉じておいてください。
Linuxで使いたい場合、別途手順をお伝えします。

サポート
何か問題や質問があれば、メールでご連絡ください。スクリーンショットやエラーメッセージを添付していただけると助かります！

作成者: [あなたの名前]最終更新: 2025年5月18日
