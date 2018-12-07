

def readlabels():
    
    files = ['prevention.txt',  'education.txt', "quality.txt", "financing.txt", "healthcare.txt", "affordability.txt"]
    labels = ['prevention',  'education', "quality", "financing", "healthcare", "affordability"]
   
    data = {}
    for idx,file in enumerate(files):
        fin = open(file, 'r')
        fin_data = fin.readlines()[0].split(",")
        data[labels[idx]] = fin_data
        
        fin.close()
        
    
    for key, val in data.items():
        print(key)
        print(val)
        
    




if __name__ == "__main__":
    readlabels()
    





