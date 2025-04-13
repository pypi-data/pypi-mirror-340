def addition(numbers: list) -> float:
    return sum(numbers)
def show_code():
    code = '''
data_iris <- iris[1:4]
cov_data <- cov(data_iris)
print(cov_data) # Print covariance matrix to check
Eigen_data <- eigen(cov_data)
print(Eigen_data$values) # Print eigenvalues to check
PCA_data <- princomp(data_iris, cor = FALSE) # Set cor=FALSE instead of "False"
summary(PCA_data) # Print summary to ensure PCA ran correctly
model2 <- PCA_data$loadings[, 1]
print(model2) # Print the first principal component
model2_scores <- as.matrix(data_iris) %*% model2
print(head(model2_scores)) # Print the first few PCA scores
if (!require(e1071)) install.packages("e1071", dependencies = TRUE)
library(e1071)
mod1 <- naiveBayes(iris[, 1:4], iris[, 5])
mod2 <- naiveBayes(model2_scores, iris[, 5])
table(predict(mod1, iris[, 1:4]), iris[, 5])
table(predict(mod2, model2_scores), iris[, 5])

    '''
    print(code)