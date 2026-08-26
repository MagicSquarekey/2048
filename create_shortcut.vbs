' Create shortcut for 2048 Game (in project directory)
Set WScriptShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

' Get script directory (project root)
ScriptDir = fso.GetParentFolderName(WScript.ScriptFullName)

' exe file path
ExePath = ScriptDir & "\dist\2048.exe"

' Check if exe exists
If Not fso.FileExists(ExePath) Then
    MsgBox "Error: Game file not found." & vbCrLf & vbCrLf & _
           ExePath & vbCrLf & vbCrLf & _
           "Please run build.bat first.", vbCritical, "2048 Game"
    WScript.Quit 1
End If

' Create shortcut in project directory (NOT desktop)
ShortcutPath = ScriptDir & "\2048_Game.lnk"
Set Shortcut = WScriptShell.CreateShortcut(ShortcutPath)
Shortcut.TargetPath = ExePath
Shortcut.WorkingDirectory = ScriptDir
Shortcut.Description = "2048 Casual Game"
Shortcut.WindowStyle = 1
Shortcut.Save

' Success message
MsgBox "Shortcut created successfully!" & vbCrLf & vbCrLf & _
       "Location: " & ScriptDir & vbCrLf & _
       "Name: 2048_Game.lnk" & vbCrLf & vbCrLf & _
       "Double-click to play!", vbInformation, "2048 Game"