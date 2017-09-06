file_comp_o = open("/Users/songchangheon/Desktop/what_be_answer.txt")
file_comp_t = open("/Users/songchangheon/Desktop/extract.txt")

total = 0
whole = 0

for line in file_comp_o.readlines():
    line_list = line.split()
    omt = line.split()
    line_t = file_comp_t.readline()
    line_list_c = line_t.split()
    tmo = line_t.split()

    for element in line_list:
        if element in line_list_c:
            omt.remove(element)

    for i in line_list_c:
        if i in line_list:
            tmo.remove(i)
    whole += 1
    if len(omt) > 0:    total += 1
    print "error : %d" %(len(omt))
    print line_list, "->", omt
    #print line_list_c, "->", tmo
    print ""

print "total : %d/%d" %(total, whole)

file_comp_t.close()
file_comp_o.close()