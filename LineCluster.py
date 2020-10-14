import math

def LineCluster(lines, max_dis = 15, max_ang = 5 / 180 * math.pi):
    groups = []
    polars = []
    for line in lines:
        x1, y1, x2, y2 = line
        rho = abs(x1 * y2 - x2 * y1) / ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
        theta = math.atan2((y2 - y1), (x2 - x1)) + 0.5 * math.pi

        j = 0
        while j < len(polars):
            line_rho, line_theta = polars[j][0]
            if abs(rho - line_rho) < max_dis and (
                    abs(theta - line_theta) < max_ang or abs(theta - line_theta) >= 180 - max_ang):
                groups[j].append(line)
                polars[j].append([rho, theta])
                j = len(polars)
            j += 1
        if j == len(polars):
            polars.append([[rho, theta]])
            groups.append([line])

    # Lines merge with weighted mean
    coods = []
    for group in groups:
        x1 = min([_[0] for _ in group])
        x2 = max([_[2] for _ in group])
        weight = sum([_[2] - _[0] for _ in group]) + 1 / 1000000

        # lines = []
        lines_weighted = []
        for line in group:
            y1 = (x1 - line[0]) / (line[2] - line[0] + 1 / 1000000) * (line[3] - line[1]) + line[1]
            y2 = (x2 - line[0]) / (line[2] - line[0] + 1 / 1000000) * (line[3] - line[1]) + line[1]
            # lines.append([x1, y1, x2, y2]) #This is extending line of each detected line
            lines_weighted.append([y1 * (line[2] - line[0]) / weight, y2 * (line[2] - line[0]) / weight])
        cood = [x1, sum([_[0] for _ in lines_weighted]), x2, sum([_[1] for _ in lines_weighted])]
        coods.append(cood)
    return coods