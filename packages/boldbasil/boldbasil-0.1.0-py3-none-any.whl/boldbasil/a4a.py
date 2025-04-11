def a4a():
    import pandas as pd
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.model_selection import train_test_split
    from sklearn.naive_bayes import MultinomialNB
    from sklearn.metrics import accuracy_score

    # Sentiment Analysis
    data = {'review': ['I love this movie!', 'This movie is terrible.', 'Great Movie.', 'Awful movie.', 'I love it!'],
            'sentiment': [1, 0, 1, 0, 1]}

    df = pd.DataFrame(data)

    X_train, X_test, y_train, y_test = train_test_split(df['review'], df['sentiment'], test_size=0.3, random_state=42)

    vectorizer = CountVectorizer()
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    model = MultinomialNB()
    model.fit(X_train_vec, y_train)

    y_pred = model.predict(X_test_vec)

    print("Sentiment Analysis Accuracy:", accuracy_score(y_test, y_pred))


    def tower_of_hanoi():
        # Tower of Hanoi
        def TowerOfHanoi(n, source, destination, auxiliary):
            if n == 1:
                print(f"Move disk 1 from source {source} to destination {destination}")
                return
            TowerOfHanoi(n - 1, source, auxiliary, destination)
            print(f"Move disk {n} from source {source} to destination {destination}")
            TowerOfHanoi(n - 1, auxiliary, destination, source)

        n = int(input('Enter number of disks: '))
        TowerOfHanoi(n, 'A', 'B', 'C')


    # Call functions
        a4a()
        tower_of_hanoi()
