@echo off
cd %USERPROFILE%\Desktop\release_tracker
call venv\Scripts\activate
python main.py
echo 完了しました。Enterで終了
pause