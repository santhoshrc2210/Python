
# You should write your whole answer within the function provided. The autograder will call
# this function and compare the return value against the correct solution value
def answer_zero():
    # This function returns the number of features of the breast cancer dataset, which is an integer. 
    # The assignment question description will tell you the general format the autograder is expecting
    
    # YOUR CODE HERE
    #print(cancer['feature_names'])
    return len(cancer['feature_names'])
    #raise NotImplementedError()

#print(answer_zero())
# You can examine what your function returns by calling it in the cell. If you have questions
# about the assignment formats, check out the discussion forums for any FAQs

def answer_one():
    # YOUR CODE HERE
    df_cancer = pd.DataFrame(data=cancer.data, columns=cancer.feature_names)
    df_cancer['target'] = cancer['target']
    return df_cancer
    #raise NotImplementedError()
    
#print(answer_one().tail())

def answer_two():
    
    # YOUR CODE HERE
    unique, counts = np.unique(cancer.target, return_counts=True)
    #print(unique, counts)
    target = pd.Series(counts, index=['malignant', 'benign'])
    #print(dict(zip(cancer.target_names, counts)))
    return target
    #raise NotImplementedError()
    
#print(answer_two())

def answer_three():
    # YOUR CODE HERE
    df_cancer = answer_one()
    # Select all rows (:) and the first 30 columns
    X = df_cancer.iloc[:, :30].copy()
    y = df_cancer['target']
    #return (X.shape, y.head())
    return (X, y)
    #raise NotImplementedError()
    
#print(answer_three())

from sklearn.model_selection import train_test_split

def answer_four():
    # YOUR CODE HERE
    X_train, X_test, y_train, y_test = train_test_split(answer_three()[0], answer_three()[1], test_size=0.25, random_state=0)
    #print(y_train)
    #return (X_train.shape, X_test.shape, y_train.shape, y_test.shape)
    return (X_train, X_test, y_train, y_test)
    #raise NotImplementedError()
    
#print(answer_four())

from sklearn.neighbors import KNeighborsClassifier

def answer_five():
    # YOUR CODE HERE
    knn = KNeighborsClassifier(n_neighbors = 1)
    #print(answer_four()[2])
    knn.fit(answer_four()[0], answer_four()[2])
    return knn
    #raise NotImplementedError()
    
#print(answer_five())

def answer_six():
    # YOUR CODE HERE
    #df.mean(): Calculates the average value for each numeric column. It returns a pandas Series where the index contains the column names.
    #[:-1]: Slices the Series to select all elements except the very last one.
    #.values: Converts the sliced pandas Series into a 1D NumPy array of raw numbers.
    #.reshape(1, -1): Converts the 1D array into a 2D array with 1 row and an automatically calculated number of columns (-1).
    cancerdf=answer_one()
    cancer_prediction = answer_five().predict(cancerdf.mean()[:-1].values.reshape(1, -1))
    return cancer_prediction
    #raise NotImplementedError()
    
#print(answer_six())

def answer_seven():
    # YOUR CODE HERE    
    return answer_five().predict(answer_four()[1])
    #raise NotImplementedError()
    
#print(len(answer_seven()))

def answer_eight():
    # YOUR CODE HERE
    return answer_five().score(answer_four()[1], answer_four()[3])
    #raise NotImplementedError()
    
#print(answer_eight())
