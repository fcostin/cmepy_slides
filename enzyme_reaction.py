def main():
    """
    the complete example from the slides
    """
    
    import numpy
    from cmepy import solver, recorder, model
    from cmepy.util import non_neg

    s_0 = 50
    e_0 = 10

    s = lambda *x : x[0]
    e = lambda *x : non_neg(e_0 - x[1])
    c = lambda *x : x[1]
    p = lambda *x : non_neg(s_0 - x[0] - x[1])

    m = model.create(
        species_counts = (s, e, c, p, ),
        propensities = (
            lambda *x : 0.01*s(*x)*e(*x),
            lambda *x : 35.0*c(*x),
            lambda *x : 30.0*c(*x),
        ),
        transitions = (
            (-1, 1),
            (1, -1),
            (0, -1)
        ),
        shape = (s_0 + 1, min(s_0, e_0) + 1),
        initial_state = (s_0, 0)
    )

    enzyme_solver = solver.create(
        model = m,
        sink = False
    )

    time_steps = numpy.linspace(0.0, 10.0, 101)

    r = recorder.create(
        (['S', 'E', 'C', 'P'], m.species_counts)
    )

    for t in time_steps:
        enzyme_solver.step(t)
        r.write(t, enzyme_solver.y)   

    recorder.display_plots(r)

if __name__ == '__main__':
    main()

