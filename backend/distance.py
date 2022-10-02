from geopy import distance

def avg_distance(start, end, loc):
    return (distance.distance(start, loc).km + distance.distance(end, loc).km)/2

def find_closest(cam, speed):
    closest_dist = []
    closest = []
    for i in range(len(speed.LinkID)):
        minDist = 1000
        minLoc = 0
        for j in range(len(cam.Latitude)):
            start = (speed["Lat Start"][i], speed["Long Start"][i])
            end = (speed["Lat End"][i], speed["Long End"][i])
            loc = (cam["Latitude"][j], cam["Longitude"][j])
            dist = avg_distance(start, end, loc)
            if (dist < minDist):
                minDist = dist
                minLoc = j
        closest_dist.append(minDist * 1000)
        closest.append(cam["CameraID"][minLoc])
    
    s2 = speed.copy()
    s2["Closest Cam"] = closest
    s2["dist (m)"] = closest_dist
    return s2



    
