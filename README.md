# NMAKE check

WindowsでC++をビルドする際に、
- コンパイラにMSVC++の`cl.exe`を使う
- makeの代わりに使う`nmake.exe`を使う

場合のサンプルプログラム集です。

## 注意

- 当方、NMAKEを勉強しながらこのリポジトリを作っているので、ところどころミスがあったり、noobすぎる実装をしているかもしれません。
- 同じ理由で、リポジトリのコード内容を大きく変更する場合があります。参考にされる場合は注意してください。

このリポジトリが誰かの参考になれば幸いですが、上記を踏まえて、あくまで参考程度にお願いします。

## 開発環境

以下を開発環境として作っています。

とはいえ、Visual Studioが動かせるWindowsマシンであれば、古すぎなければ多分動きます。

- OS: Windows 11
- [Visual Studio Build Tools 2022](https://visualstudio.microsoft.com/ja/downloads/?q=build+tools#build-tools-for-visual-studio-2022)
  - 多分、2019や2022以降のVSでも大丈夫です。
  - C++関係のビルドツールをVisual Studio Installerでインストールしてください。
  - VSについてくる**開発者用Command Prompt**または**開発者用Powershell**を使います。この中に入って`cl.exe`や`nmake`にパスが通っていることを確認してください。
- Python 3.8 or above
  - このリポジトリの開発時はPython 3.10を使用しています。ただ、標準的な使い方しかしてないので3.8以上ならそのまま動くと思います。
  - 一部、Makefileを生成するために使用します。
  - WSL上ではなく、Windows上でネイティブに動くPythonです。Python.orgやパッケージマネージャ（wingetなど）、ストアなどからインストールしてください。
  - これも開発者用Command Prompt or PS上で`python`コマンドが使えるようになっていればOKです。
    - インストール方法によりますが、おそらくPATHを通す必要があります。

## 実行方法

VSのBuild Toolsに入っている開発者用CMDか開発者用PowerShellで以下を実行してください。

開発者用CMD/PSは`cl.exe`や`nmake.exe`などのパスが通っています。

実行例(`01-hello_world`)

```powershell
cd <このリポジトリのルートフォルダ>\01-hello_world
nmake /nologo /f makefile.nmake
```

`make clean`に相当するクリーンアップを実行する際は、以下のように`clean`を追加してください。
- GNUの`make`でもよく行われるように、`clean`という疑似ターゲットに対して削除処理を実装しているだけです。
- NMAKEだから`clean`に特殊な処理が入っている…というわけではありません。

```powershell
nmake /nologo /f makefile.nmake clean
```

### 引数

- `/nologo`: nmakeで最初に出てくる2行分の著作権表示を表示しない設定。ビルド自体に特に影響はありません。
- `/f <ファイルパス>`: `makefile`ではなく、任意のファイルをmakefileとして読み込む際に使用します。
  - したがって、`makefile.nmake`でなく`makefile`にしておけば、`/f`の部分は不要になります。
    - しかし、同じプロジェクト内でGNU makeの`makefile`を共存させたいとき、`makefile`がGNU makeのものかnmakeのものかわかりずらくなってしまう可能性があります。
    そのため、個人的にはnmake版に`.nmake`をつけ、nmake用のMakefileであることを明示するほうが好みです。

## 確認方法、その他tips

- nmakeのコマンドライン引数について、`/f`のような形式のほか、`-f`でもOKです。動作は同じです。

- `/n`を入れるとビルドは行わず、実行する予定のコマンドをprintするようになります。
Makefileの動作確認に有用です。

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
