cls
cls
echo build exe
python setup.py install
echo copy files
copy *.png c:\livros
copy *.ini c:\livros
xcopy Z:\source\livros\build\exe.win-amd64-3.7 c:\livros /e /Y
echo O.K.