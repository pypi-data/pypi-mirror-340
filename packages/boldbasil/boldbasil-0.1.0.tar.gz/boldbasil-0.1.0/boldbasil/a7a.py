def a7a():
    import numpy as np
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D

    def generate_dataset(n):
        x = []
        y = []
        random_x1 = np.random.rand()
        random_x2 = np.random.rand()
        for i in range(n):
            x1 = i
            x2 = i / 2 + np.random.rand() * n
            x.append([1, x1, x2])  # Including a bias term for completeness
            y.append(random_x1 * x1 + random_x2 * x2 + 1)  # Linear combination
        return np.array(x), np.array(y)

    x, y = generate_dataset(200)

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    ax.scatter(x[:, 1], x[:, 2], y, label='y', s=5, color='blue')
    ax.set_xlabel('X1')
    ax.set_ylabel('X2')
    ax.set_zlabel('Y')
    ax.legend()
    ax.view_init(45, 0)

    plt.show()


    def tsp():
        import random

        def hc_tsp(cities, dist):
            route = cities[:]
            random.shuffle(route)
            best = route[:]
            while True:
                neighbors = []
                for i in range(len(cities) - 1):
                    neighbor = route[:]
                    neighbor[i], neighbor[i + 1] = neighbor[i + 1], neighbor[i]
                    neighbors.append(neighbor)

                def route_distance(r):
                    return sum(dist[r[i]][r[i + 1]] for i in range(len(r) - 1)) + dist[r[-1]][r[0]]

                best_neighbor = min(neighbors, key=route_distance)

                if route_distance(best_neighbor) >= route_distance(route):
                    break

                route = best_neighbor
                best = route[:]

            return best, route_distance(best)

        cities = [0, 1, 2, 3]
        dist = [
            [0, 10, 15, 20],
            [10, 0, 35, 25],
            [15, 35, 0, 30],
            [20, 25, 30, 0]
        ]

        best_route, best_dist = hc_tsp(cities, dist)
        print("Best route:", best_route)
        print("Best distance:", best_dist)


    # Call the functions
        a7a()
        tsp()
