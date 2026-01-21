from BrouillonBattleSys.Pointetmatricelogique.EssaiMatriceLogique import GrilleCombat
from BrouillonBattleSys.Pointetmatricelogique.EssaiPoint2D import Point2D


def run_tests():
    g = GrilleCombat(8, 8)

    # Test placer_element
    a = Point2D(1, 1, "A")
    g.placer_element(a)
    assert g.grid[1][1].element is a

    # Test retirer_element
    g.retirer_element(1, 1)
    assert g.grid[1][1].element is None

    # Test deplacer_element
    g.placer_element(a)
    g.deplacer_element(a, 2, 2)
    assert g.grid[2][2].element is a
    assert g.grid[1][1].element is None

    # Test moving to occupied
    b = Point2D(3, 3, "B")
    g.placer_element(b)
    try:
        g.deplacer_element(a, 3, 3)
        raise AssertionError("Expected ValueError when moving to occupied cell")
    except ValueError:
        pass

    print("All basic tests passed")


if __name__ == '__main__':
    run_tests()
