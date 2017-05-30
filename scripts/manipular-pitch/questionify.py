import sys

file_name = sys.argv[1]
output_file = sys.argv[2]

#def questionify_pitch(file_name):
with open(file_name, 'rb') as f:
    points = 0
    text = f.read()
    lines = text.split('\n')
    for line in lines:
        if "points: size" in line:
            points = int(line.split("= ",1)[1])
            break

    limit1 = points * 0.80
    limit2 = points * 0.93

    pointvalues = text.split("points [")

    i = 0
    ans = pointvalues[0]
    constant = 1.05
    for p in pointvalues:
        if i > limit1:
            aux = p.split("value = ", 1)
            tmp = float(aux[1])
            tmp = tmp * constant
            if i < limit2:
                constant += 0.02
            else:
                constant -= 0.04
            ans += "points [" + aux[0] + "value = " + str(tmp) + "\n"
            print constant
        else:
            if i != 0:
                ans += "points [" + p
        i += 1
    
with open(output_file, 'w') as output:
    output.write(ans)
