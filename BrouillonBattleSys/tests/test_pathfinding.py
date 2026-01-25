from BrouillonBattleSys.tests.BattleState.Map.MapLogique.MatriceLogique import GrilleCombat
from BrouillonBattleSys.tests.BattleState.Entites.EntitesLogique.Point2D import Point2D


def run_path_test():
    g = GrilleCombat(100, 100)
    start = Point2D(0, 0, "start")
    end = Point2D(1, 0, "end")
    path = g.pathfinding(start, end)
    assert path is not None, "Path should be found on empty grid"
    assert len(path) >= 2
    assert path[0].x == start.x and path[0].y == start.y
    assert path[-1].x == end.x and path[-1].y == end.y
    print("Pathfinding test passed")
    print(path)

if __name__ == '__main__':
    run_path_test()
