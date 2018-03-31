# Line of sight

In this project, I use [Binary Space Partition](https://en.wikipedia.org/wiki/Binary_space_partitioning) algorithm to order line segments that forms a binary tree data structure. Primarily, this data structure is used to render 3D polygons of a scene in a particular, back to front or far to near. Other uses include ray tracing, collision detection in 3D video games/simulations.

In this application, we randomnly generate a list of line segments (to simulate walls) in 2D confined space with two proabability distributions, uniform and [powerlaw](https://en.wikipedia.org/wiki/Power_law). It is observed that most physical and man made phenomena approximately follow power law distribution. By using random numbers generated with powerlaw distribution, we try to simulate how humans inhabit an area, or how human inhabitants expand into their surroundings, for example, large cities.

We then randomnly position points in our 2D scene (to simulate agents/characters) and determine whether a line of sight exists between any of the agents/characters amidst all the line segments that simulate walls. Between two agents, we can do this by imagining the line of sight as a line segment between the two agents and then testing for intersection against all other line segments but it will take O(m) tests for every possible position of two agents. 

Hence, we take advantage of ordered line segments in BSP tree and reduce our running time between O(log(m)) and O(m). Since most agents in a realistic scenario are close to each other, their line of sight test will close to O(log(m)).

In order to take advantage of least number of intersection tests, our BSP tree should be balanced and have minimum number of nodes. In order to achieve these conditions, we use heuristics while generating our BSP tree.

We use two heuristics, 'EvenDivide' which selects a node as the root node such that both its left and right subtree will have equal number of nodes or as close to equal number of nodes as possible. 'MinPartition' in which we select a node such that it causes the minimum number of splits when partitioning our space on that node but it may not result in a balanced tree.

Finally, I compare perforamce of BSP trees with both heuristics against 2D scene generated with both uniform and powerlaw distributions. Performance charts can be found [here](https://github.com/uzipaz/LineOfSight/blob/master/Final%20Presentation.pdf).

### Required libraries
- Pygame (https://www.pygame.org)
- Numpy (http://www.numpy.org/)
