# 02_nested_files

`src/`以下に直接置かれたいたmain.cpp, lib.cppに加えて、`tool/`というディレクトリがさらに掘られている場合

## ソースの説明

- src/
  - main.cpp: main関数があるプログラム。`lib.cpp`内の`hello()`を呼び出すだけ。
  - lib.cpp: `hello()`の実装が書かれているプログラム
  - tool/calc.cpp: `tool/calc.h`の実装。
- include/
  - lib.h: lib.cppに対応するヘッダファイル。hello()の前方宣言が書かれている。
  - tool/calc.h: `add(int, int)`のプロトタイプ宣言が書かれているヘッダファイル。

## 出力物

01と仕様は同じ。

- `obj/`: 各cppファイルのビルド結果であるオブジェクトファイルが出力される。
- `bin/`: 最終的な実行ファイルが出力される。

## Makefileのポイント

- 01のmakefileと同じmakefileだと、`tools/`以下がビルドターゲットにならずに以下のエラーが発生するはず。

```
cl.exe /nologo obj\main.obj obj\lib.obj /Fe"bin\01-hello_world.exe"
main.obj : error LNK2019: 未解決の外部シンボル "int __cdecl add(int,int)" (?add@@YAHHH@Z) が関数 main で参照されました
  定義済みの一致する可能性があるシンボルに関するヒント:
    "bool __cdecl __crt_strtox::add(struct __crt_strtox::big_integer &,unsigned int)" (?add@__crt_strtox@@YA_NAEAUbig_integer@1@I@Z)
bin\01-hello_world.exe : fatal error LNK1120: 1 件の未解決の外部参照
```

SRC_DIR, OBJ_DIRのところをディレクトリ含むワイルドカード`**`にすればできそうだが、残念ながらこれはうまくいかない。
```
# {$(SRC_DIR)*\}.cpp{$(OBJ_DIR)\}.obj: # BEFORE
{$(SRC_DIR)\**\}.cpp{$(OBJ_DIR)\**\}.obj: # AFTER(うまくいかない)

NMAKE : fatal error U1073: 'obj\tool\calc.obj' のビルド方法が指定されていません。
```

また、`.cpp.obj:`に変えても同じエラーになる。

---

解決策としては、SRCS, OBJSで全てのcppと、それに対応するobjのパスが網羅できていれば良い。
今回は`tool/calc.cpp`だけなので、OBJSで直接指定すれば一応動く。

```
OBJECTS = $(OBJ_DIR)\main.obj $(OBJ_DIR)\lib.obj $(OBJ_DIR)\tool\calc.obj
```

---

しかし、問題はこの処理を自動化するところにある。
毎回、新しいcppを導入したらmakefileを手動で更新するのは手間がかかるし保守が難しいので、なんとか自動化したいところ。

UNIXの`make`は以下のように`wildcard`を使って`src/`以下の全ディレクトリを再帰的に拾うことができたが、残念ながらnmakeではできない。

```makefile
SRCS := $(wildcard $(SRC_DIR)/*.cpp) $(wildcard $(SRC_DIR)/**/*.cpp)
OBJS := $(patsubst $(SRC_DIR)/%.cpp,$(OBJ_DIR)/%.o,$(SRCS))
```

解決策としては、

- ディレクトリの階層ごとに`{$(SRC_DIR)*\}.cpp{$(OBJ_DIR)\}.obj:` のブロックを作る。
  - また、それらのSRC_DIR, OBJ_DIRの組をなんとか定義する必要がある。
    - Makefile内でなんとか再帰的にSRCS, OBJSを定義するか、外部ファイルに定義して`!INCLUDE`で読み込む方法がある。

Makefile内の機能でゴリゴリに実装してもよいが、複雑になってくるとMakefile自体が煩雑になってしまう。

そこで、Pythonを使ってmakefileを自動生成するスクリプトを作成した。
srcディレクトリが増えても、それに応じてSRCSなどを更新したmakefileを自動で生成する。
`configure`などに近いアプローチ。
Makefileだけで解決しないのはスマートではない気がするが、Pythonでより柔軟に書けるようになるメリットもあるので一長一短ある。

Pythonについては、Windowsの場合は何らかの方法で環境にインストールする必要がある点に注意。
macOS/Linuxではそれなりのバージョンのものが標準でインストールされているので問題ない。

`configure`を模して作ってみた。
このサンプルではオプションは無い。
configure.batはただpythonを呼び出しているだけ。

```cmd
.\configure.bat
nmake /nologo /f makefile.nmake
```
