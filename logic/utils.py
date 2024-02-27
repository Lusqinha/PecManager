
def db_to_rows(data, keys:list[str], headers:list[tuple]) -> list[tuple]:
    
    try:
        ROWS:list[tuple[str]] = headers
            
        for item in data:
            row = tuple([item[key] for key in keys])
            ROWS.append(row)
        
        return ROWS
    
    except Exception as e:
        print(e)
        return [()]