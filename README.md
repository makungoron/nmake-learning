# NMAKE check

## 実行方法

VSのBuild Toolsに入っている開発者用CMDか開発者用PowerShellで以下を実行。
開発者用CMD/PSは`cl.exe`や`nmake.exe`などのパスが登録済み。

```powershell
cd <このリポジトリのルートフォルダ>
nmake /nologo /f makefile.nmake
```
