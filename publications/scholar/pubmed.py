import csv
import re
doi_abstract = {}
with open('abstract.txt') as file:
    lines = file.readlines()
    lines = [line.rstrip() for line in lines]
    i = 0
    blank = 0
    abstract = []
    doi = ""
    start = 0
    end = 1
    author_mode = False

    for line in lines:
        #if re.match('[0-9].*\.\s',line):
        if "Author information:" in line:
            author_mode = True
        if "doi: " in line:
            x = line.split("doi:",1)[1] 
            doi = x.split()[0]
            doi = doi[0:len(doi)-1]
        if line=='':
            blank = blank + 1
            if end-start >6 and not author_mode and blank>3:
                abstract = ' '.join(abstract)
                #print(doi)
                #input("here")
                doi_abstract[doi]=abstract
            author_mode = False
            abstract = []
            start = end
        abstract.append(line)
        i = i +1
        end = end + 1
        
print(doi_abstract)
with open('todd.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    next(spamreader, None)
    year_index = 7
    author_index = 2
    doi_index = 10
    journal_index = 5
    title_index = 1
    i = 0
    for row in spamreader:
        author = row[author_index]
        doi = row[doi_index]
        journal = row[journal_index]
        title = row[title_index].replace('"', '')
        year = row[year_index]
        year = year.split("/")[0]+"-"+year.split("/")[1] + "-"+year.split("/")[2]
        with open(year+"_"+journal+"_"+str(i)+".md", 'w') as f:
            f.write("+++\n")
            f.write("date = \""+year+"\"\n")
            f.write("title = \""+title+"\"\n")
            f.write("description = \"publication\"\n")
            f.write("category = \"journal\"\n")
            f.write("publish = \""+journal+"\""+"\n")
            
            f.write("weight=3\n")
            f.write("author = "+"\""+author+"\"\n")
            f.write("+++\n")
            f.write("\n")
            f.write("# Abstract\n")
            f.write("\n")
            if doi in doi_abstract:
                f.write(doi_abstract[doi])
            else:
                f.write("To be imported ..\n")

            i = i + 1
