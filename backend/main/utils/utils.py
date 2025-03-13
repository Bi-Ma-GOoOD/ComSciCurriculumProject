def getGrade(charGrade: str) -> tuple[float|None, str|None] :
    charGrade = charGrade.upper()
    
    if charGrade == 'A' :
        return 4.0, None
    elif charGrade == 'B+' :
        return 3.5, None
    elif charGrade == 'B' :
        return 3.0, None
    elif charGrade == 'C+' :
        return 2.5, None
    elif charGrade == 'C' :
        return 2.0, None
    elif charGrade == 'D+' :
        return 1.5, None
    elif charGrade == 'D' :
        return 1.0, None
    elif charGrade == 'F' :
        return 0.0, None
    
    return None, charGrade