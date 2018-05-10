# COMP90024 Team 4 Group Assignment, Melbourne
# Hongxiang Yang: 674136 hongxiangy@student.unimelb.edu.au
# Jiaming Wu: 815465 jiamingw@student.unimelb.edu.au
# Qingyang Li: 899636 qingyangl4@student.unimelb.edu.au
# Xueyao Chen: 851312 xueyaoc@student.unimelb.edu.au
import json
import sys

#FILTER_NUM = 100  # number of twitters at least in one suburb


def main(argv):
    input_file_name = "classified_twt_SSC.json"
    #input_SSC_list="all_SSC_list.json"
    #SSC_list=json.load(open(input_SSC_list, 'r'))
    output_file_name = "result/cal_all_SSC.json"
    #output_SSC_file_name = "cal_all_SSC_code.json"
    data = json.load(open(input_file_name, 'r'))
    all_sub_count = {}
    for each in data:
        if each["SSC"] in all_sub_count.keys():
            if each["sent"] == 'pos':
                all_sub_count[each["SSC"]][0] += 1
            else:
                all_sub_count[each["SSC"]][1] += 1
        else:
            all_sub_count[each["SSC"]]=[0,0,0]
            if each["sent"] == 'pos':
                all_sub_count[each["SSC"]][0] += 1
            else:
                all_sub_count[each["SSC"]][1] += 1
    for key in all_sub_count.keys():
        total = all_sub_count[key][0] + all_sub_count[key][1]
        if total==0:
            all_sub_count[key][2]=0
        else:
            all_sub_count[key][2] = round(all_sub_count[key][0] / float(total), 4)
    print len(all_sub_count)

    sorted_all_sub_count = sorted(all_sub_count.items(), key=lambda e: e[1][2], reverse=True)
    output_sorted_all_sub_count = [{"SSC": str(item[0]), "postive_twt_rate": str(item[1][2])} for item in
                                   sorted_all_sub_count]
    #output_SSC = [item[0] for item in sorted_all_sub_count]
    with open(output_file_name, 'w') as fp:
        json.dump(output_sorted_all_sub_count, fp)
    #with open(output_SSC_file_name, 'w') as fp:
        #json.dump(output_SSC, fp)


if __name__ == "__main__":
    main(sys.argv[1:])

    #
