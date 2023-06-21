import numpy as np
import math

EDGE_HINT = "EDGE_WEIGHT_SECTION"
NODE_HINT = "DISPLAY_DATA_SECTION"
EDGE_HINT_LEN = len(EDGE_HINT)
NODE_HINT_LEN = len(NODE_HINT)

def read_init_info(init_section):
    lines = init_section.split('\n')
    name = ""
    dimension = 0
    edge_weight_foramat = ""
    for line in lines:
        key,value = line.split(":")
        key.rstrip()
        if key=='NAME':
            name = value.lstrip()
        elif key=='DIMENSION':
            dimension = int(value.lstrip())
        elif key=='EDGE_WEIGHT_FORMAT':
            edge_weight_foramat=value.strip()
    return name,dimension,edge_weight_foramat


def read_node_pos(dim,node_section):
    node_pos = np.zeros((2,dim+1))
    dis_matrix = np.zeros((dim+1,dim+1))

    lines = node_section.split('\n')
    i = 1
    for line in lines:
        nums=line.split()
        x = float(nums[1])
        y = float(nums[2])
        node_pos[0][i] = x
        node_pos[1][i] = y
        for j in range(1,i):
            dx = abs(node_pos[0][i]-node_pos[0][j])
            dy = abs(node_pos[1][i]-node_pos[1][j])
            dis_matrix[i][j] = dis_matrix[j][i] = math.sqrt(dx*dx+dy*dy)
        i += 1
    return node_pos,dis_matrix


def read_edge_upper(dim,edge_str):
    edge_weight = np.zeros((dim+1,dim+1))
    nums = edge_str.split()
    count = 0
    for i in range(1,dim):
        for j in range(i+1,dim+1):
            edge_weight[i][j] = edge_weight[j][i] = float(nums[count])
            count += 1
    return edge_weight


def read_edge_lower(dim,edge_str):
    edge_weight = np.zeros((dim+1,dim+1))
    nums = edge_str.split()
    count = 0
    for i in range(1,dim+1):
        for j in range(1,i+1):
            edge_weight[i][j] = edge_weight[j][i] = float(nums[count])
            count += 1
    return edge_weight


def read_edge_full(dim,edge_str):
    edge_weight = np.zeros((dim+1,dim+1))
    nums = edge_str.split()
    for i in range(1,dim+1):
        for j in range(1,dim+1):
            edge_weight[i][j] = float(nums[(i-1)*dim+(j-1)])
    return edge_weight


def read_tsp_file(file_name):
    with open(file_name,'r') as file:
        content = file.read()
        init_end_index = content.find(EDGE_HINT)
        edge_start_index = init_end_index+EDGE_HINT_LEN
        edge_end_index = content.find(NODE_HINT)
        node_start_index = edge_end_index+ NODE_HINT_LEN
        node_end_index = content.find("EOF")
        
        init_section = content[0:init_end_index].strip()
        edge_weight_section = content[edge_start_index:edge_end_index].strip()
        node_section = content[node_start_index:node_end_index].strip()
 
        name,dim,format = read_init_info(init_section)
        print("[info]: name: ",name,", dim: ",dim,", format: ",format)
        node_position,dis_matrix = read_node_pos(dim,node_section)
        
        if format=="UPPER_ROW":
          edge_weight_matrix = read_edge_upper(dim,edge_weight_section)
        elif format=="LOWER_DIAG_ROW":
                edge_weight_matrix = read_edge_lower(dim,edge_weight_section)
        elif format=="FULL_MATRIX":
                edge_weight_matrix = read_edge_full(dim,edge_weight_section)
        print("[info]: position:\n",node_position)
        print("[info]: dis_matrix:\n",dis_matrix)
        print("[info]: edge_weight:\n",edge_weight_matrix)
        return dim,node_position,dis_matrix,edge_weight_matrix

# 把原始数据文件改写成框架需要的权重文件
# 格式参考：https://github.com/moead-framework/data/blob/master/weights/SOBOL-2objs-10wei.ws
# def write_weight_file(data_file,weight_file):
def write_weight_file(dim,dis_matrix,edge_weight_matrix,weight_file):
    # dim,node_position,dis_matrix,edge_weight_matrix = read_tsp_file(data_file)
    weight_list = np.zeros((dim*dim,2))
    for i in range(1,dim+1):
        for j in range(1,dim+1):
            line = (i-1)*dim+(j-1)
            weight_list[line][0] = dis_matrix[i][j]
            weight_list[line][1] = edge_weight_matrix[i][j]
    
    with open(weight_file,"w") as file:
        for weight in weight_list:
            file.write(f"{weight[0]} {weight[1]}\n")
    return weight_list


# for test
if __name__ == '__main__':
    dim,node_position,dis_matrix,edge_weight_matrix = read_tsp_file("../../Data/bays29.tsp")
    # write_weight_file("../../Data/bays29.tsp","./output.txt")
    write_weight_file(dim,dis_matrix,edge_weight_matrix,"./output.txt")