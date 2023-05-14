import analysis as analyzer
import matplotlib.pyplot as plt
import sys

teamArg = None
teams = ["csk", "mi", "gt", "rcb", "pbks", "lsg", "srh", "rr"]
if len(sys.argv) > 1:
    teamArg = sys.argv[1]
    isPresent = False
    for team in teams: 
        if teamArg == team:
            isPresent = True
            break
    else: 
        print("Please choose one of these values: csk, mi, gt, rcb, pbks, lsg, srh, rr")
        print("For analysis of all available teams use 'all'")
        exit(1)
else:
    print("Please choose one of these values: csk, mi, gt, rcb, pbks, lsg, srh, rr")
    print("For analysis of all available teams use 'all'")
    exit(1)

if teamArg == "all":
    for team in teams:
        analyzer.analyze_team(team)
else:
    analyzer.analyze_team(teamArg)

