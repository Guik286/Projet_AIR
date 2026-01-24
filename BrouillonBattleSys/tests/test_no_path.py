from BrouillonBattleSys.tests.BattleState.EssaiMatriceLogique import GrilleCombat
from BrouillonBattleSys.tests.BattleState.EssaiPoint2D import Point2D


def test_no_path():
    g = GrilleCombat(5, 5)
    # Block all paths
    for i in range(5):
        for j in range(5):
            if (i,j) != (0,0) and (i,j) != (4,0):
                g.placer_element(Point2D(i,j, f"block{i}{j}"))
    start = Point2D(0, 0, "start")
    end = Point2D(4, 0, "end")
    path = g.pathfinding(start, end)
    assert path is None, "Should return None when no path"
    print("No path test passed")

if __name__ == '__main__':
    test_no_path()