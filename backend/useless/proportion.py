from flow import flow1
from flow import flow2
from utils import retrieve_images

def proportion(df):
    if flow1(df)[0][0] != 0:
        p108 = flow2(df)[0][0]/flow1(df)[0][0]
    else:
        p108 = 0
    if flow1(df)[0][1] != 0:
        p110 = flow2(df)[0][1]/flow1(df)[0][1]
    else:
        p110 = 0
    if flow1(df)[1][0] != 0:
        p208 = flow2(df)[1][0]/flow1(df)[1][0]
    else:
        p208 = 0
    if flow1(df)[1][1] != 0:
        p210 = flow2(df)[1][1]/flow1(df)[1][1]
    else:
        p210 = 0

    print(p108, p110, p208, p210)
    return [p108, p110, p208, p210]

if __name__ == "__main__":
    proportion(retrieve_images())
