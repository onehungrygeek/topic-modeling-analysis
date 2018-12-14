__author__ = "Akshay Kulkarni, Vishal Jasrotia"
__copyright__ = ""
__credits__ = ["Akshay Kulkarni", "Vishal Jasrotia"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Vishal Jasrotia"
__email__ = "jvishal@cs.stonybrook.edu"
__status__ = "Production"

#imports
import os
import csv
import sys
import pandas


CATEGORY_SIZE = 200

def readlabels():
    """ read descriptive files for labels ad keywords
    """
    
    files = ['prevention.txt',  'education.txt', "quality.txt", "financing.txt", "healthcare.txt", "affordability.txt"]
    labels = ['prevention',  'education', "quality", "financing", "healthcare", "affordability"]
   
    data = {}
    for idx,file in enumerate(files):
        fin = open(file, 'r')
        fin_data = fin.readlines()[0].split(",")
        data[labels[idx]] = fin_data
        fin.close()
    
    return data
    

def calculate_overlapping(keywords, data):
    """
    """
    
    if keywords:
        pass
    else:
        path = os.path.join(os.getcwd(), "Output_Files")
        files = os.listdir(path)
        files = [file for file in files if file.endswith(".csv")]
        
#         for idx, file in enumerate(files):
#             print(idx, file)
        # print(files[5])
        file_num = 5 #input('Enter file number for analysis:\t')
        
        time_string =  ""#time.strftime("%m-%d-%Y_%H-%M-%S")
                
        outcsv = open(os.path.join(os.getcwd(), "Output_Files","category.csv"), 'w')
        csvwriter = csv.writer(outcsv, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        categories = sorted(data.keys())
        csvwriter.writerow(["Keywords"] + categories + ["Category"])
        
        df = pandas.read_csv(os.path.join(os.getcwd(), "Output_Files",files[int(file_num)]))
        
        dominator = {}
        
        
        for index, row in df.iterrows():
            keywords = row['Keywords_In_Dominant_Topic'].replace(" ", "").split(",")
            max_val = 0
            max_category = "Cannot determine"
            total_keywords = len(keywords) 
            row  = [" ".join(keywords)]
            for category in categories:
                overlap_count = len(set(data[category]) & set(keywords))
                overlap_count_percent = (overlap_count/total_keywords) *100
                if max_val < overlap_count_percent:
                    max_val = overlap_count_percent
                    max_category = category
                row.append(overlap_count_percent)
            
            row.append(max_category)
            
            if index % CATEGORY_SIZE == 0 and index != 0 :
               
                freq = ""
                for category in categories:
                    freq +=  category + ":" + str(dominator.get(category, 0)) + ", "
                print(freq)
                dominator = {}    
            else:
                dominator[max_category] = dominator.get(max_category, 0) + 1
                
            csvwriter.writerow(row)
            
        
        outcsv.close()   
#         
        print("file name : " , os.path.join(os.getcwd(), "Output_Files",files[int(file_num)]))
        print("out name : " , os.path.join(os.getcwd(), "Output_Files","category.csv"))
       
        
        

def main(keywords = None):
    """
    """
    data = readlabels()
    calculate_overlapping(keywords, data)
    
    
if __name__ == "__main__":
    main()
    
    





