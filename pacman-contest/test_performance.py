"""
Author:      XuLin Yang
Student id:  904904
Date:        2020-2-6 23:31:18
Description: code to test the performance between each agents
"""

import time
import capture

"""
["D:\python\python.exe",
                             "-m",
                              "../capture.py",
                              "--delay 0.0",
                              "-r ./pacman_ai/myTeam.py --redOpts=first=SearchAgent,second=SearchAgent",
                              "-b ../baselineTeam.py --blueOpts=first=DefensiveReflexAgent,second=DefensiveReflexAgent"]
"""

if __name__ == "__main__":
    start_time = time.time()
    options = capture.readCommand([
                              "-r","./teams/pacman_ai/myTeam.py","--redOpts=first=InferenceAgent,second=InferenceAgent",
                                "-b","./baselineTeam.py","--blueOpts=first=DefensiveReflexAgent,second=DefensiveReflexAgent"]
    )
    games = capture.runGames(**options)

    print('\nTotal Time Game: %s' % round(time.time() - start_time, 0))

