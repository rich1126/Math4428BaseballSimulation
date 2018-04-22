# Math4428BaseballSimulation

This contains the code for the Monte Carlo simulation of a baseball game. It is written generally enough that any line-up of any teams can be used, given you limit yourself to 9 players, and are willing to input the relevant data by hand.

The simulation takes into account On Base Percentage as the main metric, and then breaks that into singles, doubles, triples, homeruns and walks (which include HBPs). A walk only forces the appropriate runners, as per baseball rules. An actual hit moves every runner the proper number of bases. If a runner is on first, and a double is hit, the runner on first will move to third but never score.

No pitching/defense is currently implemented in the code on here, although a simple way to include pitching would be to scale on base percentages by a ratio of a pitcher's statistics compared to the league average.
