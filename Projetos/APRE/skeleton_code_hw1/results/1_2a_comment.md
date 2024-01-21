# Comment

## Question
```
Comment the following claim: “A logistic regression model using pixel values
as features is not as expressive as a multi-layer perceptron using relu activations.
However, training a logistic regression model is easier because it is a convex optimization
problem.” Is this true of false? Justify
```

## Answer
```
Logistic regression is a linear classifier, limited to linear decision boundaries, MLP
on the opposite side can learn non-linear relationships between features. Which generally 
allows MLP to be more expressive than logistic regression. 

The relationship between pixels in an image can be very complex, so using pixel values
as features will have negative impact on the Logistic regression performance. 

However, training a MLP (using ReLU activation function) can be very resource intensive 
and can be very time consuming, because this is not a convex problem. On the other hand 
logisitc regression is convex problem wich is easier to solve (since we don't have to 
deal with the loca minima problem)

In conclusion we consider this claim as True
```

