def getGrade(charGrade: str) -> float|None :
    charGrade = charGrade.upper()
    
    if charGrade == 'A' :
        return 4
    elif charGrade == 'B+' :
        return 3.5
    elif charGrade == 'B' :
        return 3
    elif charGrade == 'C+' :
        return 2.5
    elif charGrade == 'C' :
        return 2
    elif charGrade == 'D+' :
        return 1.5
    elif charGrade == 'D' :
        return 1
    elif charGrade == 'F' :
        return 0
    elif charGrade == 'I' or charGrade == 'N' :
        return -1
    
    return None