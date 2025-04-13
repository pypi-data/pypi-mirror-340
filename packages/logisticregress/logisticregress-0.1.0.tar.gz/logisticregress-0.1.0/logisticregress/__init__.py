def addition(numbers: list) -> float:
    return sum(numbers)
def show_code():
    code = '''
# Load dataset
library(datasets)
ir_data <- iris
head(ir_data)
str(ir_data)
levels(ir_data$Species)
# Check for missing values
sum(is.na(ir_data))
# Subset the data for two species and 100 observations
ir_data <- ir_data[1:100, ]
# Split data into training and testing sets
set.seed(100)
samp <- sample(1:100, 80)
ir_test <- ir_data[samp, ]
ir_ctrl <- ir_data[-samp, ]
# Install and load libraries for visualization
if (!require("ggplot2")) install.packages("ggplot2", dependencies = TRUE)
library(ggplot2)
if (!require("GGally")) install.packages("GGally", dependencies = TRUE)
library(GGally)
# Pair plot for test data
ggpairs(ir_test)
# Logistic regression: Predict Species using Sepal.Length
y <- as.numeric(ir_test$Species == "setosa") # Convert Species to binary
x <- ir_test$Sepal.Length
glfit <- glm(y ~ x, family = "binomial")
summary(glfit)
# Predict on control data
newdata <- data.frame(x = ir_ctrl$Sepal.Length)
predicted_val <- predict(glfit, newdata, type = "response")
# Combine predictions with control data
prediction <- data.frame(
  Sepal.Length = ir_ctrl$Sepal.Length,
  Actual.Species = ir_ctrl$Species,
  Predicted.Probability = predicted_val
)
print(prediction)
# Plot predictions
qplot(
  prediction$Sepal.Length,
  round(prediction$Predicted.Probability),
  col = prediction$Actual.Species,
  xlab = "Sepal Length",
  ylab = "Prediction using Logistic Regression"
)

    '''
    print(code)