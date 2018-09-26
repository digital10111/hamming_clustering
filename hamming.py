from itertools import combinations
import unionfind
import json

bit_flips_1 = list(combinations(range(24), 1))
bit_flips_2 = list(combinations(range(24), 2))


def calculate_one_flips(number, bit_flips_1):
    one_flips = []
    for ind in bit_flips_1:
        one_flips.append('%s%s%s'%(number[:ind[0]],str(1 - int(number[ind[0]])),number[ind[0]+1:]))
    return one_flips


def calculate_two_flips(number, bit_flips_2):
    two_flips = []
    for index in bit_flips_2:
        ind1 = index[0]
        ind2 = index[1]
        inter = '%s%s%s'%(number[:ind1], str(1 - int(number[ind1])),number[ind1+1:])
        two_flips.append( '%s%s%s'%(inter[:ind2], str(1 - int(inter[ind2])),number[ind2+1:]) )
    return two_flips


def get_flip_dict():
    hash_map = {}
    one_flips_dict = {}
    zero_flip_dict = {}
    with open("clustering1.txt", "r") as f:
        for i, line in enumerate(f.readlines()):
            if i == 0:
                num_nodes = int(line.split(' ')[0])
                num_bits = int(line.split(' ')[1])
                continue
            number = line.replace(" ", "")[:-1]
            if number not in zero_flip_dict:
                zero_flip_dict[number] = [i]
            else:
                zero_flip_dict[number].append(i)
            hash_map[i] = number
            one_flips_dict[number] = calculate_one_flips(number, bit_flips_1)
    print "done 1"
    two_flips_dict = json.load(open("two_flip_dict.txt", "r"))
    print "done 2"
    parent = unionfind.XVec()
    for v in range(0, num_nodes):
        parent.append(-1)

    return hash_map, one_flips_dict, two_flips_dict, parent, zero_flip_dict


def form_clusters():
    hash_map, one_flips_dict, two_flips_dict, parent, zero_flip_dict = get_flip_dict()
    total_components = 200000

    for number in zero_flip_dict.keys():
        first_number_index = zero_flip_dict[number][0]
        for i in zero_flip_dict[number]:
            ret = unionfind.union(parent, first_number_index, i)
            if ret:
                total_components -= 1

    print total_components

    for indx in hash_map.keys():
        number = hash_map[indx]
        for one_flip_neighbor in one_flips_dict[number]:
            if one_flip_neighbor in zero_flip_dict:
                list_of_indx_with_one_hamming_distance = zero_flip_dict[one_flip_neighbor]
                for ohmd in list_of_indx_with_one_hamming_distance:
                    ret = unionfind.union(parent, indx, ohmd)
                    if ret:
                        total_components -= 1
    print total_components

    for indx in hash_map.keys():
        number = hash_map[indx]
        for two_flip_neighbor in two_flips_dict[number]:
            if two_flip_neighbor in zero_flip_dict:
                list_of_indx_with_two_hamming_distance = zero_flip_dict[two_flip_neighbor]
                for ohmd in list_of_indx_with_two_hamming_distance:
                    ret = unionfind.union(parent, indx, ohmd)
                    if ret:
                        total_components -= 1
                        if total_components % 1000 == 0:
                            print total_components
    print total_components

form_clusters()