import py7zr

archive23 = py7zr.SevenZipFile("202307/CAGEDMOV202307.7z", mode="r")
archive23.extractall()
archive23.close()


