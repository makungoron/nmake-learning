# 03-more_nested_files

`02-nested_files`に加え、src/以下にさらにディレクトリが掘られている場合です。

- このプロジェクトではビルドに**Python**を使用します。

## ソースの説明

`src/`, `include/`については説明を省略します。
プログラムの内容自体に特に意味はありません。

- build-tools/
  - configure.py: Makefileを自動生成するPythonスクリプトです。
- configure.bat: configure.pyを呼び出すバッチプログラムです。`configure`を簡易的に模したものです。
- makefile.nmake: configure.pyで作ったMakefileと同じものです。

## 出力物

01, 02と仕様は同じです。

- `obj/`: 各cppファイルのビルド結果であるオブジェクトファイルが出力される。
- `bin/`: 最終的な実行ファイルが出力される。

## Makefileのポイント

02から飛躍してしまいますが、MakefileをPythonで自動生成するようにしました。

C/C++でよくある`configure`, `make` でビルドする流れを模して、
- `configure(.bat)`を実行して、Makefileを動的に生成
- `nmake`でビルド

するようにしました。

```cmd
cd 03-more_nested_files
configure
nmake /f makefile.nmake /nologo
```

以下、Pythonで自動生成するようにした理由です。

---

03においても、`02-nested_files`と同じ書き方で、全てのディレクトリの依存関係をMakefile内に直接書けば動きます。

しかし、複雑になってくるとMakefile自体が長くなってしまいます。

makeの機能でcppがあるフォルダを全取得してビルドタスクを書く…こともできると思いますが、これにはかなりのMakefile力が必要です。
少なくとも、これを書いている段階の私ではmakeの機能だけでスマートに書く方法がわかりませんでした。

そこで、**Python**を使ってmakefileを自動生成するスクリプトを用意しました。
cppが入っているディレクトリが増えても、SRCSなどを自動で更新し、正しく動くMakefileを生成するようにしています。

Pythonはmake/nmakeよりは慣れているので、私にとってこちらのほうが柔軟で書きやすいと感じています。
開発者にPythonの実行環境を追加で要求することになりますが、それでも書きやすさ・管理のしやすさのメリットのほうが大きいことも多いと思います。

さらに、Makefileの生成方法がわかりやすいほうが良いと感じたので、インターフェースとしてconfigure.batを作りました。
`configure`を模して`configure(.bat)`を実行するだけでMakefileを作成できるようにしています。
configure.batの中身は、ただPythonを呼び出しているだけです。

```cmd
python .\build-tools\configure.py
```

また、
よくある`configure`には引数を指定することができますが、今回、この実装には引数はありません。

configure.bat, pythonに引数を
configure.batなら`%1`などの記法、Python側では`argparse`などを使って実装することになると思います。

### おまけ

GNU makeは以下のように`wildcard`を使って`$(SRC_DIR)/`以下の全ディレクトリを再帰的に拾うことができますが、残念ながらnmakeではできないようです。

このあたりの機能がnmakeでも簡単に実現できれば、Pythonを使う必要はなかったかもしれません。

```makefile
# GNU make
SRCS := $(wildcard $(SRC_DIR)/*.cpp) $(wildcard $(SRC_DIR)/**/*.cpp)
OBJS := $(patsubst $(SRC_DIR)/%.cpp,$(OBJ_DIR)/%.o,$(SRCS))
```
