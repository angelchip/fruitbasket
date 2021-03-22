#!/usr/bin/python

#Readme
#Author Angel Hernandez
#Using bash 2.7.18 on Windows 10
#Script takes as a parameter a csv file, it checks for the extension and parameter.
#Once the file is pulled, it get all the data to answer the questions required.
#The results are printed to the console/
#Usage: python solution.py <filename.extension>
#Note: I added a minor logging file to the first two methods, just to show how you normally would log script actions; which can later be parsed by Splunk.

import sys
import csv
import array
import datetime 

#Start of Global variables
paramleng = len(sys.argv)
totalf = 0
fruitc = []
days = []
ch1 = []
ch2 = []
ft = []
ft2 = []
dict_fruits=dict()
dict_fruitsf=dict()
dict_ftf=dict()
#End of Global variables

#Start of Method "CSV" to pull the data from the csv file and also work on counting frutis based on characteristic1 and 2
def my_csv(file):
  ts = datetime.datetime.now()
  ts = ts.strftime("%Y-%m-%d %H:%M:%S")
  f = open("logfile.txt", "a") 
  f.write("Headers .....")
  f.write(ts)
  f.write(" Entering method my_csv")
  with open(file,'rt')as f:
    data = csv.reader(f)
    for row in data:
        fruitc.append(row[0])
        days.append(row[1])
        ch1.append(row[2])
        ch2.append(row[3])
        ft.append([row[0].strip(),row[1].strip(),row[2].strip(),row[3].strip()])
#End of Method "CSV"

#Start of Method of "fruit types" and total
def fruit_type(fruits):
    ts = datetime.datetime.now()
    ts = ts.strftime("%Y-%m-%d %H:%M:%S")
    f = open("logfile.txt", "a") 
    f.write(ts)
    f.write(" Entering method fruit_type")
    for fs in fruits:
        if dict_fruits.has_key(fs):
            fv = dict_fruits.get(fs)
            dict_fruits[fs] = fv + 1
        else:
            dict_fruits[fs] = 1
    typefruit = 0
    for key in dict_fruits.keys():
        if key != 'fruit':
            typefruit += 1 
            dict_fruitsf[key] = dict_fruits.get(key)
    print ""
    print "Types of fruits:", typefruit
    totalf = 0
    for key, value in sorted(dict_fruitsf.items()):
        totalf += value
        print "     *", value,key,"(s)"
    print ""
    print "Total Number of fruits:", totalf
#End of Method of "fruit types"

#Start of Method "fruit_char"
def fruit_char():
    ftl= len(ft)
    ftl2= len(ft2)
    i = 0
    j = 0
    if ftl2 == 0:
        ft2.append(ft[1])
        ft2[0].append(1)
        ft2[0][4] = 0
    ftl2= len(ft2)
    for r in range(1,ftl):
        for i in range(i,ftl2):
            if ft[r][0] == ft2[i][0]:
                if ft[r][2] == ft2[i][2]:
                    if ft[r][3] == ft2[i][3]:
                        if ft[r][1] > ft2[i][1]:                          
                            ft2[i][1]=ft[r][1]
                            ft2[i][4] += 1
                        else:
                            ft2[i][4] += 1
                    break
                else:
                    j = i
                    indexcheck = len(ft2)     
                    vc = indexcheck - 1
                    if j < indexcheck:                   
                        for j in range(j,indexcheck):
                            if ft[r][0] == ft2[j][0]:
                                if ft[r][2] == ft2[j][2]:    
                                    if ft[r][3] == ft2[j][3]:
                                        if ft[r][1] > ft2[j][1]:                          
                                            ft2[j][1]=ft[r][1]
                                            ft2[j][4] += 1
                                        else:
                                            ft2[j][4] += 1                                         
                                    break
                                elif j==vc:       
                                    ft2.append(ft[r])
                                    ft2[indexcheck].append(1)                               
                            elif j==vc:                            
                                ft2.append(ft[r])
                                ft2[indexcheck].append(1)                    
                    else:
                        ft2.append(ft[r])
                        ft2[indexcheck].append(1)               
            else:
                j = i
                indexcheck = len(ft2)     
                vc = indexcheck - 1
                if j < indexcheck:                   
                    for j in range(0,indexcheck):
                        if ft[r][0] == ft2[j][0]:
                            if ft[r][2] == ft2[j][2]:
                                if ft[r][3] == ft2[j][3]:
                                    if ft[r][1] > ft2[j][1]:                          
                                        ft2[j][1]=ft[r][1]
                                        ft2[j][4] += 1                                        
                                    else:                                                                                
                                        ft2[j][4] += 1                                        
                                break
                            elif j==vc:       
                                ft2.append(ft[r])
                                ft2[indexcheck].append(1)                              
                        elif j==vc:                            
                            ft2.append(ft[r])
                            ft2[indexcheck].append(1)
                else:
                    ft2.append(ft[r])
                    ft2[indexcheck].append(1)
#End of Method "fruit_char"

#Start of Method "fruit_bychar"
def fruit_bychar():
        print ""
        print "The characteristics (size, color, shape, etc.) of each fruit by type"        
        sorted_list = sorted(ft2)
        over = []
        di = len(sorted_list)
        di2 = len(over)
        for i in range(0,di):
            print "   ",sorted_list[i][4], sorted_list[i][0], "(s):",sorted_list[i][2],',',sorted_list[i][3],sorted_list[i][1]
            if int(sorted_list[i][1]) >= 3:
                di2 = len(over)
                if di2 > 0: 
                    for j in range (0,di2):
                        if over[j][0] == sorted_list[i][0]:
                            over[j][4] += int(sorted_list[i][4])
                            break
                        elif j==di2-1: 
                            over.append(sorted_list[i])  
                            break                            
                else:
                    over.append(sorted_list[i])                    
        print ""
        print "Have any fruit been in the basket for over 3 days"
        di2 = len(over)
        for i in range(0,di2):            
            print  over[i][4], over[i][0], "(s) over 3 days"
#End of Method "fruit_bychar"
                                                         
#Start of the main section of the script, validation of arguments and usage.            
if paramleng == 2:
    extvalid = str(sys.argv[1])
    if extvalid.endswith('.csv'):
        my_csv(extvalid)
        fruit_type(fruitc)
        fruit_char()
        fruit_bychar()
    else:
        print "check file extension, should be csv. Example: basket.csv" 
else:
    print "Usage: python solution.py <filename.extension>"
    print "csv field should have the following columns: fruit,days,characteristic1,characteristic2 as the first row"
#End of the main section

