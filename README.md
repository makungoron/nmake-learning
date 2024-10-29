# NMAKE check

WindowsでC++をビルドする際に、
- コンパイラにMSVC++の`cl.exe`を使う
- makeの代わりに使う`nmake.exe`を使う

場合のサンプルプログラム集。

## 開発環境

Visual Studioが動かせるWindowsマシンであれば、古すぎなければ多分動く。

- OS: Windows 11
- [Visual Studio Build Tools 2022](https://visualstudio.microsoft.com/ja/downloads/?q=build+tools#build-tools-for-visual-studio-2022)
  - 多分、2019や2022以降のVSでも動く。
  - C++関係のビルドツールをVisual Studio Installerでインストールしておく。
  - VSについてくる**開発者用Command Prompt**または**開発者用Powershell**を使う。この中に入って`cl.exe`や`nmake`にパスが通っていることを確認する。
- Python 3.8 or above
  - このリポジトリの開発時はPython 3.10を使用。ただ、標準的な使い方しかしてないので3.8以上ならそのまま動くと思う。
  - 一部、Makefileを生成するために使用する。
  - WSL上ではなく、Windows上でネイティブに動くPython。Python.orgやパッケージマネージャ、ストアなどからインストールする必要がある。
  - これも開発者用Command Prompt or PS上で`python`コマンドが使えるようになっていればOK。
    - インストール方法によるが、おそらくPATHを通す必要あり。

## 実行方法

VSのBuild Toolsに入っている開発者用CMDか開発者用PowerShellで以下を実行。
開発者用CMD/PSは`cl.exe`や`nmake.exe`などのパスが通っている。

実行例(`01-hello_world`)

```powershell
cd <このリポジトリのルートフォルダ>\01-hello_world
nmake /nologo /f makefile.nmake
```

`make clean`に相当するクリーンアップを実行する際は、以下のように`clean`を足す。
- GNUの`make`でもよく行われるように、`clean`という疑似ターゲットに対して削除処理を実装しているだけ。
- NMAKEだから`clean`に特殊な処理が入っている…というわけではない。

```powershell
nmake /nologo /f makefile.nmake clean
```

### 引数

- `/nologo`: nmakeで最初に出てくる2行分の著作権表示を表示しない。ビルド自体に特に影響はない。
- `/f <ファイルパス>`: `makefile`ではなく、任意のファイルをmakefileとして読み込む。
  - 実は`makefile.nmake`とわざわざしなくても、`makefile`にすれば`/f`はいらなくなる。
    - しかし、GNU makeの`makefile`と共存させたい時、互換性のない`makefile`同士があたかも互換性があるかのように共存するのはよくないので、個人的には`.nmake`などとして別物であることを明示している。

## 確認方法、その他tips

- nmakeのコマンドライン引数について、`/f`のような形式の他、`-f`でもOK。動作は同じ。

- `/n`を入れると実際にビルドは行わず、実行する予定のコマンドをprintするようになる。

実行例(`01-hello_world`)

```powershell
cd <このリポジトリのルートフォルダ>\01-hello_world
nmake /nologo /f makefile.nmake /n
```

## References

### NMAKE関連

- [NMAKEリファレンス(Microsoft)](https://learn.microsoft.com/ja-jp/cpp/build/reference/nmake-reference?view=msvc-170)

- [nmake リファレンス(Qiita; @hana_moto さん)](https://qiita.com/hana_moto/items/30ed1cf4340d416d9003)

- [C/C++入門 - makefile と nmake ～ makefile を読み解く](https://c.keicode.com/windows/windows-programming-06.php)

### MSVC++関連

- [MSVCコンパイラのコマンドライン構文(Microsoft)](https://learn.microsoft.com/ja-jp/cpp/build/reference/compiler-command-line-syntax?view=msvc-170)
