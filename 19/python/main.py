import math

def get_delta(p1, p2):
    return (sorted((abs(p1[0] - p2[0]), 
              abs(p1[1] - p2[1]), 
              abs(p1[2] - p2[2]))))

def get_raw_delta(p1, p2):
    return ((((p1[0] - p2[0]), 
              (p1[1] - p2[1]), 
              (p1[2] - p2[2]))))

def distance_to_origin(beacon):
    x,y,z = beacon
    return math.sqrt(x*x + y * y + z *z)

def dist(p1, p2):
    (x1,y1,z1) = p1
    (x2,y2,z2) = p2
    return (abs(x1 - x2)+ abs(y1 - y2)+ abs(z1 - z2))

POSITIONS = [(0,0,0)]

def update_beacons(beacons, normalized):
    already_checked = []
    while len(normalized):
     j = normalized.pop()
     already_checked.append(j)
     b0 = beacons[j]
     print("Normalizing against", j)

     for i in range(len(beacons)):
        if i in normalized or i in already_checked:
            continue
        b1 = beacons[i]
        
        overlapping_left = set()
        overlapping_right = set()
        for pair1 in ([(x,y) for  x in range(len(b0)) for y in range(x+1, len(b0)) ]):
            for pair2 in ([(x,y) for  x in range(len(b1)) for y in range(x+1, len(b1)) ]):
                p1 = b0[pair1[0]]
                p2 = b0[pair1[1]]

                p3 = b1[pair2[0]]
                p4 = b1[pair2[1]]

                d1 = get_delta(p1, p2)
                d2 = get_delta(p3, p4)

                if sorted(d1) == sorted(d2):
                    # print("Found overlapping points", pair1, pair2)
                    overlapping_left.add(pair1[0])
                    overlapping_left.add(pair1[1])

                    overlapping_right.add(pair2[0])
                    overlapping_right.add(pair2[1])


                # Check if the deltas are the same.
        if len(overlapping_right) == len(overlapping_left) >= 12:
            left_points = [b0[i] for i in overlapping_left]
            right_points = [b1[i] for i in overlapping_right]
            

            # Maps a left to a right
            correspondance = {}

            un_mapped_right = right_points[:]

            for p in left_points:
                deltas2 = sorted([get_delta(p, x) for x in left_points])
                for r in un_mapped_right:
                    deltas1 = sorted([get_delta(r, x) for x in right_points])
                    if deltas1 == deltas2:
                        correspondance[left_points.index(p)] = right_points.index(r)
                        un_mapped_right.remove(r)
                        break
            
            # Get a known good delta
            p1 = left_points[0]
            p2 = left_points[1]

            p3 = right_points[correspondance[0]]
            p4 = right_points[correspondance[1]]

            d1 = get_raw_delta(p1, p2)
            d2 = get_raw_delta(p3, p4)
            # Noly do this if the deltas are right.
            x_maps_to = [abs(x) for x in d2].index(abs(d1[0]))
            y_maps_to = [abs(x) for x in d2].index(abs(d1[1]))
            z_maps_to = [abs(x) for x in d2].index(abs(d1[2]))

            x_mult = 1 if d1[0] == d2[x_maps_to] else -1
            y_mult = 1 if d1[1] == d2[y_maps_to] else -1
            z_mult = 1 if d1[2] == d2[z_maps_to] else -1


            p5 = (p3[x_maps_to] * x_mult, p3[y_maps_to] * y_mult, p3[z_maps_to] * z_mult)
            delta_x = p5[0] - p1[0]
            delta_y = p5[1] - p1[1]
            delta_z = p5[2] - p1[2]

            POSITIONS.append((delta_x, delta_y, delta_z))


            beacons[i] = ([
                (b[x_maps_to] * x_mult - delta_x,
                    b[y_maps_to] * y_mult - delta_y,
                    b[z_maps_to] * z_mult - delta_z) for b in b1
            ])
            normalized.append(i)
    return beacons, None

def solution(lines):
    foo = lines.split("\n\n")
    beacons = [x.split("\n")[1:] for x in foo]
    beacons = [[x.split(",") for x in z] for z in beacons]
    beacons = [[(int(x), int(y), int(z)) for (x,y,z) in foo] for foo in beacons]
    # beacons = [sorted(x, key=distance_to_origin) for x in beacons]

    updated = True
    normalized = [0]
    while len(normalized) < len(beacons):
        print(len(normalized))
        (beacons, normed) = update_beacons(beacons, normalized)
        if (normed is None):
            break
        normalized.append(normed)
    
    final = set()
    for x in beacons:
        for b in x:
            final.add(b)
    print(len(final))

    distance = 0
    # print(POSITIONS)
    for i in range(len(POSITIONS)):
        for j in range(i+1, len(POSITIONS)):
            p1 = POSITIONS[i]
            p2 = POSITIONS[j]
            distance = max([distance, dist(p1, p2)])
    print(distance)

with open('input.txt') as f:
    lines = f.read()
    solution(lines)
   