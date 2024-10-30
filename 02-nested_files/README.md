# 02_nested_files

`src/`以下に直接置かれたいたmain.cpp, lib.cppに加えて、`tool/`というディレクトリがさらに掘られている場合です。

## ソースの説明

- build_tools/
  - configure.py: Makefileを自動生成するPythonプログラムです。
- src/
  - main.cpp: main関数があるプログラム。`lib.cpp`内の`hello()`を呼び出すだけ。
  - lib.cpp: `hello()`の実装が書かれているプログラム
  - tool/calc.cpp: `tool/calc.h`の実装。
- include/
  - lib.h: lib.cppに対応するヘッダファイル。hello()の前方宣言が書かれている。
  - tool/calc.h: `add(int, int)`のプロトタイプ宣言が書かれているヘッダファイル。
- configure.bat: `configure`を模して、Makefileを自動生成するプログラムを実行するバッチファイルです。
- makefile01.nmake: 01からの地続きで、考え方として最もわかりやすい形で動くようにしたmakefileです。
- makefile.nmake: configure.batの生成物です。

## 出力物

01と仕様は同じです。

- `obj/`: 各cppファイルのビルド結果であるオブジェクトファイルが出力される。
- `bin/`: 最終的な実行ファイルが出力される。

## Makefileのポイント

01のmakefileと同じmakefileだと、`tools/`以下がビルドターゲットにならずに以下のエラーが発生します。

```
cl.exe /nologo obj\main.obj obj\lib.obj /Fe"bin\01-hello_world.exe"
main.obj : error LNK2019: 未解決の外部シンボル "int __cdecl add(int,int)" (?add@@YAHHH@Z) が関数 main で参照されました
  定義済みの一致する可能性があるシンボルに関するヒント:
    "bool __cdecl __crt_strtox::add(struct __crt_strtox::big_integer &,unsigned int)" (?add@__crt_strtox@@YA_NAEAUbig_integer@1@I@Z)
bin\01-hello_world.exe : fatal error LNK1120: 1 件の未解決の外部参照
```

SRC_DIR, OBJ_DIRのところをディレクトリ含むワイルドカード`**`にすればできそうですが、残念ながらこれはうまくいきません。

```
# {$(SRC_DIR)*\}.cpp{$(OBJ_DIR)\}.obj: # BEFORE
{$(SRC_DIR)\**\}.cpp{$(OBJ_DIR)\**\}.obj: # AFTER(うまくいかない)

NMAKE : fatal error U1073: 'obj\tool\calc.obj' のビルド方法が指定されていません。
```

また、推論規則の部分を`.cpp.obj:`に変えても同じエラーになってしまいます。

---

解決策としては、
- SRCS, OBJSで、`tools\`以下も含む全てのcppと対応するobjファイルを依存関係に含めるようにして
- それぞれのcppのビルド方法を定義すれば

動きます。

これの実現方法はいくつか考えられるので、01-hello_worldから地続きで、わかりやすいように複数の解決策を試していきます。

### 改善方法1: 直接指定する

以下のように追加した依存関係について,
ビルド方法を直接指定すればとりあえずは動きます。

このMakefileファイルの全体は`makefile01.nmake`に書いてあります。

```makefile
# Makefile.nmake
# 中略

# tool\calc.{cpp|obj} を依存関係に追加
SRCS = src\lib.cpp src\main.cpp src\tool\calc.cpp
OBJS = obj\lib.obj obj\main.obj obj\tool\calc.obj

all: $(TARGET)
$(TARGET) : $(OBJS)
	@echo Linking...
	@if NOT EXIST $(@D) mkdir $(@D)
	$(CPP) /nologo $(OBJS) /Fe"$(BIN_DIR)\$(TARGET)"

# ここはsrc直下のみしかターゲットにしない
{src\}.cpp{obj\}.obj:
	@echo Compiling $< $@
	@echo $(@D)
	@if NOT EXIST $(@D) mkdir $(@D)
	$(CPP) /nologo /c $(CFLAGS) $< /Fo"$@"

# tool\calc.{cpp|obj}に対する依存関係と、ビルド方法を直接定義
obj\tool\calc.obj : src\tool\calc.cpp
	@echo Compiling $? $@
	@echo $(@D)
	@if NOT EXIST $(@D) mkdir $(@D)
	$(CPP) /nologo /c $(CFLAGS) $? /Fo"$@"

# Clean up build files
clean:
# 中略

```

- ちなみに、追加部分では`$<`は使えません。`$?`を代わりに使っています。
  - nmakeでは`$<`は推論規則の中だけで有効です。
    - 推論規則の外で使おうとすると空文字列になります。また、この旨のWarningが出ます。
  - 推論規則というのはざっくり言えば`{src\}.cpp{obj\}.obj:`のような書き方のことです。
  - 代用している`$?`は`$<`と同じく、タイムスタンプが新しいすべての依存対象のことを指します。
  - 今回、依存対象はcalc.cppだけですので、`$?`は`src\tool\calc.cpp`になります。

- しれっと`clean`の`del`に`/S`を追加しています。これはサブディレクトリの中身も対象とするための引数です。

---

### 改善方法2: tool/以下を推論規則に書き換える

改善方法1では、新しいcppファイルを依存関係に追加するたびにMakefileを書き直す必要があり、保守が大変になってしまいます。
- たとえば`tool/`以下に新しいcppファイル`calc2.cpp`を追加しようとした場合、`SRCS`, `OBJS`に依存関係を追加し、さらに、`obj\tool\calc2.obj : src\tool\calc2.cpp`のブロックを書かなければなりません。

そもそも、同じビルド手法をファイルごとに別々に書くのは、かなり冗長でわかりにくくなってしまいます。

少なくとも、`tools/`以下については`src/`と同じく、`{src\}.cpp{obj\}.obj:`のような書き方ができれば楽そうです。
これは以下のように書けば動きます。

このMakefileファイルの全体は`makefile02.nmake`に書いてあります。

```makefile
{src\tool\}.cpp{obj\tool\}.obj:
	@echo Compiling $< $@
	@echo $(@D)
	@if NOT EXIST $(@D) mkdir $(@D)
	$(CPP) /nologo /c $(CFLAGS) $< /Fo"$@"
```

これで、少なくとも`src/`と`src/tool/`以下にあるcppであれば、追加しても自動でビルド対象になるように設定できました。

ちなみに、以下のような書き方はできません。

```
# この書き方はエラーになる
{src\}.cpp{obj\}.obj:
{src\tool\}.cpp{obj\tool\}.obj:
	@echo Compiling $< $@
	@echo $(@D)
	@if NOT EXIST $(@D) mkdir $(@D)
	$(CPP) /nologo /c $(CFLAGS) $< /Fo"$@"
```
