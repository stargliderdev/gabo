cls
pyinstaller --noconfirm --log-level=WARN ^
    -D ^
    --name livros ^
    --distpath c:\ ^
    -y ^
    --icon=books.ico ^
    main.py
copy *.png c:\livros
copy *.ini c:\livros

echo O.K.