import numpy as np

# random_DAG = [[-1,  125,  175, 700, -1, -1, -1, -1, -1, -1, -1, -1, -1],
#               [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
#               [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
#               [-1, -1, -1, -1,  700, -1, -1, -1, -1, -1, -1, -1, -1],
#               [-1, -1, -1, -1, -1,  110,  500,  90, -1, -1, -1, -1, -1],
#               [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1,  110, -1, -1],
#               [-1, -1, -1, -1, -1, -1, -1, -1,  120,  100,  150,  130, -1],
#               [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1,  90, -1, -1],
#               [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,  120],
#               [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
#               [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,  350],
#               [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,  130],
#               [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]]


def gnd(loc: float, min: float, max: float, num_samples: int):
    return np.random.normal(loc=loc, scale=max-min, size=num_samples)


random_DAG = [[-1,  125,  175, 700, -1, -1, -1, -1, -1, -1, -1, -1, -1],
              [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
              [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
              [-1, -1, -1, -1,  700, -1, -1, -1, -1, -1, -1, -1, -1],
              [-1, -1, -1, -1, -1,  100,  250,  350, -1, -1, -1, -1, -1],
              [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1,  100, -1, -1],
              [-1, -1, -1, -1, -1, -1, -1, -1,  60,  50,  75,  65, -1],
              [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
              [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,  60],
              [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
              [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,  175],
              [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,  65],
              [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]]

random_dag_images = ['f0:latest', 'f1:latest', 'f2:latest', 'f3:latest', 'f4:latest', 'f5:latest',
                     'f6:latest', 'f7:latest', 'f8:latest', 'f9:latest', 'f10:latest', 'f11:latest', 'f12:latest',]

# random_dag_ex = [1, 1, 0.5, 1.5, 2, 1, 0.5, 2.5, 1, 3, 0.5, 1.5, 2]
# random_dag_cs = [0.9, 0.55, 0.77, 0.4, 0.28,
#                  0.8, 0.25, 0.85, 0.25, 0.24, 0.6, 0.58, 0.75]

# random_dag_ram = [5, 5, 5, 5, 5,
#                   5, 5, 5, 5, 5, 5, 5, 5]
# random_dag_ex = [
#     gnd(1, 0.75, 1.25, 500),
#     gnd(0.5, 0.25, 0.75, 500),
#     gnd(0.5, 0.25, 0.75, 500),
#     gnd(1.5, 1.25, 1.75, 500),
#     gnd(2, 1.75, 2.25, 500),
#     gnd(1, 0.75, 1.25, 500),
#     gnd(0.5, 0.25, 0.75, 500),
#     gnd(2.5, 2.25, 2.75, 500),
#     gnd(1, 0.75, 1.25, 500),
#     gnd(3, 2.75, 3.25, 500),
#     gnd(0.5, 0.25, 0.75, 500),
#     gnd(1.5, 1.25, 1.75, 500),
#     gnd(2, 1.75, 2.25, 500),
# ]
# random_dag_cs = [
#     gnd(1.9, 1.7, 2.2, 500),
#     gnd(1.55, 1.35, 1.75, 500),
#     gnd(1.77, 1.57, 1.97, 500),
#     gnd(1.4, 1.2, 1.6, 500),
#     gnd(1.25, 1.2, 1.3, 500),
#     gnd(1.8, 1.6, 2, 500),
#     gnd(1.25, 1.2, 1.3, 500),
#     gnd(1.85, 1.65, 2.05, 500),
#     gnd(1.25, 1.2, 1.3, 500),
#     gnd(1.25, 1.2, 1.3, 500),
#     gnd(1.6, 1.4, 1.8, 500),
#     gnd(1.58, 1.38, 1.78, 500),
#     gnd(1.75, 1.55, 1.95, 500),
# ]
random_dag_ex = [
    gnd(10, 9.75, 10.25, 500),
    gnd(4.5, 4.25, 4.75, 500),
    gnd(2.5, 2.25, 2.75, 500),
    gnd(8.5, 8.25, 8.75, 500),
    gnd(6, 5.75, 6.25, 500),
    gnd(4, 3.75, 4.25, 500),
    gnd(12.5, 12.25, 12.75, 500),
    gnd(9.5, 9.25, 9.75, 500),
    gnd(5, 4.75, 5.25, 500),
    gnd(7, 6.75, 7.25, 500),
    gnd(1.5, 1.25, 1.75, 500),
    gnd(6.5, 6.25, 6.75, 500),
    gnd(3, 2.75, 3.25, 500),
]
random_dag_cs = [
    gnd(3.9, 3.7, 4.2, 500),
    gnd(6.55, 6.35, 6.75, 500),
    gnd(2.77, 2.57, 2.97, 500),
    gnd(3.4, 3.2, 3.6, 500),
    gnd(1.25, 1.2, 1.3, 500),
    gnd(7.8, 7.6, 8, 500),
    gnd(12.25, 12.2, 12.3, 500),
    gnd(9.85, 9.65, 10.05, 500),
    gnd(2.25, 2.2, 2.3, 500),
    gnd(5.25, 5.2, 5.3, 500),
    gnd(8.6, 8.4, 8.8, 500),
    gnd(6.58, 6.38, 6.78, 500),
    gnd(3.75, 3.55, 3.95, 500),
]
# random_dag_ex = [
#     gnd(5, 4.75, 5.25, 500),
#     gnd(4.5, 4.25, 4.75, 500),
#     gnd(4.5, 4.25, 4.75, 500),
#     gnd(5.5, 5.25, 5.75, 500),
#     gnd(6, 5.75, 6.25, 500),
#     gnd(5, 4.75, 5.25, 500),
#     gnd(4.5, 4.25, 4.75, 500),
#     gnd(6.5, 6.25, 6.75, 500),
#     gnd(5, 4.75, 5.25, 500),
#     gnd(7, 6.75, 7.25, 500),
#     gnd(4.5, 4.25, 4.75, 500),
#     gnd(5.5, 5.25, 5.75, 500),
#     gnd(6, 5.75, 6.25, 500),
# ]
# random_dag_cs = [
#     gnd(3.9, 3.7, 4.2, 500),
#     gnd(3.55, 3.35, 3.75, 500),
#     gnd(3.77, 3.57, 3.97, 500),
#     gnd(3.4, 3.2, 3.6, 500),
#     gnd(3.25, 3.2, 3.3, 500),
#     gnd(3.8, 3.6, 4, 500),
#     gnd(3.25, 3.2, 3.3, 500),
#     gnd(3.85, 3.65, 4.05, 500),
#     gnd(3.25, 3.2, 3.3, 500),
#     gnd(3.25, 3.2, 3.3, 500),
#     gnd(3.6, 3.4, 3.8, 500),
#     gnd(3.58, 3.38, 3.78, 500),
#     gnd(3.75, 3.55, 3.95, 500),
# ]

# random_dag_ex = [
#     gnd(10, 9.75, 10.25, 500),
#     gnd(10, 9.75, 10.25, 500),
#     gnd(10, 9.75, 10.25, 500),
#     gnd(10, 9.75, 10.25, 500),
#     gnd(10, 9.75, 10.25, 500),
#     gnd(20, 19.75, 20.25, 500),
#     gnd(20, 19.75, 20.25, 500),
#     gnd(10, 9.75, 10.25, 500),
#     gnd(10, 9.75, 10.25, 500),
#     gnd(10, 9.75, 10.25, 500),
#     gnd(10, 9.75, 10.25, 500),
#     gnd(10, 9.75, 10.25, 500),
#     gnd(10, 9.75, 10.25, 500),
# ]

# random_dag_cs = [
#     gnd(5, 4.75, 5.25, 500),
#     gnd(5, 4.75, 5.25, 500),
#     gnd(5, 4.75, 5.25, 500),
#     gnd(5, 4.75, 5.25, 500),
#     gnd(5, 4.75, 5.25, 500),
#     gnd(10, 9.75, 11.25, 500),
#     gnd(10, 9.75, 11.25, 500),
#     gnd(5, 4.75, 5.25, 500),
#     gnd(5, 4.75, 5.25, 500),
#     gnd(5, 4.75, 5.25, 500),
#     gnd(5, 4.75, 5.25, 500),
#     gnd(5, 4.75, 5.25, 500),
#     gnd(5, 4.75, 5.25, 500),
# ]

# random_dag_ram = [gnd(1024, 512, 2048, 500)] * 13
random_dag_ram = [gnd(512, 512, 512, 500)] * 13


w1_dist_funcs = {
    'cold_start': random_dag_cs,
    'ex_time': random_dag_ex,
    'ram': random_dag_ram
}


### ----------- RANDOM MATRICE 2 -------------###
#################################################
#################################################
#################################################
#################################################


random_DAG_2 = [
    [-1, 450, 550, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, 100, 350, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, 550, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, 500, 250, 150, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, 300, 200, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, 250, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, 150, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 300, 100, 50, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 50, 50, 100, 50, 200],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
]

random_dag_2_images = ['f0-w2:latest', 'f1-w2:latest', 'f2-w2:latest', 'f3-w2:latest', 'f4-w2:latest', 'f5-w2:latest',
                       'f6-w2:latest', 'f7-w2:latest', 'f8-w2:latest', 'f9-w2:latest', 'f10-w2:latest', 'f11-w2:latest', 'f12-w2:latest', 'f13-w2:latest', 'f14-w2:latest']
# random_dag_2_ex = [
#     1.75,
#     1,
#     1,
#     0.5,
#     0.5,
#     0.5,
#     0.5,
#     1,
#     1.75,
#     0.75,
#     1.5,
#     1,
#     1.75,
#     1.5,
#     2,
# ]
# random_dag_2_cs = [0.53, 0.45, 0.75, 0.45, 0.49, 0.73,
#                    0.17, 0.92, 0.69, 0.5, 0.22, 0.65, 0.7, 0.64, 0.4]

# random_dag_2_ram = [5, 5, 5, 5, 5,
#                     5, 5, 5, 5, 5, 5, 5, 5, 5, 5]


random_dag_2_ex = [
    gnd(1.75, 1.5, 2, 500),
    gnd(1, 0.75, 1.25, 500),
    gnd(1, 0.75, 1.25, 500),
    gnd(0.5, 0.25, 0.75, 500),
    gnd(2, 1.75, 2.25, 500),
    gnd(0.5, 0.25, 0.75, 500),
    gnd(0.5, 0.25, 0.75, 500),
    gnd(1, 0.75, 1.25, 500),
    gnd(1.75, 1.5, 2, 500),
    gnd(0.75, 0.5, 1, 500),
    gnd(1.5, 1.25, 1.75, 500),
    gnd(1, 0.75, 1.25, 500),
    gnd(1.75, 1.5, 2, 500),
    gnd(1.5, 1.25, 1.75, 500),
    gnd(2, 1.75, 2.25, 500),
]

random_dag_2_cs = [
    gnd(0.5, 0.25, 0.75, 500),
    gnd(2.5, 2.25, 2.75, 500),
    gnd(0.75, 0.5, 1, 500),
    gnd(0.5, 0.25, 0.75, 500),
    gnd(0.5, 0.25, 0.75, 500),
    gnd(0.75, 0.5, 1, 500),
    gnd(0.75, 0.5, 1, 500),
    gnd(1, 0.75, 1.25, 500),
    gnd(0.75, 0.5, 1, 500),
    gnd(3.5, 3.25, 3.75, 500),
    gnd(0.5, 0.25, 0.75, 500),
    gnd(2.5, 2.25, 2.75, 500),
    gnd(0.75, 0.5, 1, 500),
    gnd(0.75, 0.5, 1, 500),
    gnd(2.5, 2.25, 2.75, 500),
]

# random_dag_2_ex = [
#     gnd(10, 9.25, 10.75, 500),
#     gnd(10, 9.25, 10.75, 500),
#     gnd(10, 9.25, 10.75, 500),
#     gnd(10, 9.25, 10.75, 500),
#     gnd(10, 9.25, 10.75, 500),
#     gnd(10, 9.25, 10.75, 500),
#     gnd(10, 9.25, 10.75, 500),
#     gnd(10, 9.25, 10.75, 500),
#     gnd(10, 9.25, 10.75, 500),
#     gnd(10, 9.25, 10.75, 500),
#     gnd(10, 9.25, 10.75, 500),
#     gnd(10, 9.25, 10.75, 500),
#     gnd(10, 9.25, 10.75, 500),
#     gnd(10, 9.25, 10.75, 500),
#     gnd(10, 9.25, 10.75, 500),

# ]
# random_dag_2_cs = [
#     gnd(5, 4, 6, 500),
#     gnd(10, 4, 6, 500),
#     gnd(5, 4, 6, 500),
#     gnd(5, 4, 6, 500),
#     gnd(5, 4, 6, 500),
#     gnd(5, 4, 6, 500),
#     gnd(5, 4, 6, 500),
#     gnd(5, 4, 6, 500),
#     gnd(5, 4, 6, 500),
#     gnd(10, 4, 6, 500),
#     gnd(5, 4, 6, 500),
#     gnd(10, 4, 6, 500),
#     gnd(5, 4, 6, 500),
#     gnd(5, 4, 6, 500),
#     gnd(10, 4, 6, 500),
# ]

random_dag_2_ram = [gnd(5, 4, 6, 500)] * 15

w2_dist_funcs = {
    'cold_start': random_dag_2_cs,
    'ex_time': random_dag_2_ex,
    'ram': random_dag_2_ram
}
