' TXD - by benzoXdev
' Minesweeper in VBScript (simplified)

' Game initialization
Dim board(5, 5)
Dim mines(5, 5)
Dim i, j, row, col
Dim mina_count, max_mines, game_over

' Configuration
max_mines = 5
mina_count = 0
game_over = False

' Initialize board (no mines)
For i = 0 To 5
    For j = 0 To 5
        board(i, j) = 0
    Next
Next

' Place mines randomly
Do While mina_count < max_mines
    row = Int(Rnd * 5)
    col = Int(Rnd * 5)
    If mines(row, col) = 0 Then
        mines(row, col) = 1
        mina_count = mina_count + 1
    End If
Loop

' Show instructions
MsgBox "Welcome to Minesweeper! You must avoid the mines. Use coordinates (row,col) to select.", vbInformation, "Instructions"

' Check if selected cell is a mine
Function IsMine(row, col)
    If mines(row, col) = 1 Then
        IsMine = True
    Else
        IsMine = False
    End If
End Function

' Main game loop
Do While Not game_over
    ' Ask player for cell coordinates
    row = InputBox("Enter row (0-5):", "Row selection")
    col = InputBox("Enter column (0-5):", "Column selection")
    
    ' Validate input (ensure numbers)
    If IsNumeric(row) And IsNumeric(col) Then
        row = CInt(row)
        col = CInt(col)
        
        ' Validate coordinates are in range
        If row < 0 Or row > 5 Or col < 0 Or col > 5 Then
            MsgBox "Coordinates must be between 0 and 5. Try again.", vbExclamation, "Error"
        Else
            ' Check if player selected a mine
            If IsMine(row, col) Then
                MsgBox "BOOM! You hit a mine. Game over.", vbCritical, "You Lost"
                game_over = True
            Else
                MsgBox "Good job! Not a mine. Keep searching.", vbInformation, "Continue"
            End If
        End If
    Else
        MsgBox "Please enter valid numbers for row and column.", vbExclamation, "Input Error"
    End If
Loop

MsgBox "Game Over", vbInformation, "Game Over"
