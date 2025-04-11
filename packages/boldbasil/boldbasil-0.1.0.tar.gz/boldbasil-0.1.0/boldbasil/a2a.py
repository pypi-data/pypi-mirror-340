def a2a():
    graph = {
        '5': ['3', '7'],
        '3': ['2', '4'],
        '7': ['8'],
        '2': [],
        '4': ['8'],
        '8': [],
    }

    visited = set()

    def dfs(visited, graph, node):
        if node not in visited:
            print(node)
            visited.add(node)
            for neighbour in graph[node]:
                dfs(visited, graph, neighbour)

    print("Following is the depth-first search")
    dfs(visited, graph, '5')

    import numpy as np
    from sklearn.datasets import load_iris
    from sklearn.model_selection import train_test_split
    from sklearn.neighbors import KNeighborsClassifier

    iris=load_iris()
    x=iris.data
    y=iris.target

    x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2,random_state=42)

    knn=KNeighborsClassifier(n_neighbors=3)

    knn.fit(x_train,y_train)

    y_pred = knn.predict(x_test)

    for i in range(len(y_test)):
        if y_test[i] == y_pred[i]:
            print(f"correct prediction : actual class - {iris.target_names[y_test[i]]}, predicted class - {iris.target_names[y_pred[i]]}")
        else:
            print(f"Incorrect prediction : actual class - {iris.target_names[y_test[i]]}, predicted class - {iris.target_names[y_pred[i]]}")