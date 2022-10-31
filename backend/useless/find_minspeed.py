
from utils import retrieve_speedbands

def find_speedband(df):
    minspeed6708 = df[df['LinkID'] == str(103000078)]['MinimumSpeed'].astype(str).astype(int).values/12
    minspeed6710 = df[df['LinkID'] == str(103000080)]['MinimumSpeed'].astype(str).astype(int).values/12
    return [minspeed6708, minspeed6710]

if __name__ == "__main__":
    find_speedband(retrieve_speedbands())
