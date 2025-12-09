def validate(data):
        
    data = data.fillna(0)
    data.loc[:, 'YEAR'] = data['YEAR'].fillna("")
    return data
    
    
    