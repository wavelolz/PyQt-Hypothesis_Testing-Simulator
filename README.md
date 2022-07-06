# PyQt5 Hypothesis Testing Visualization
## This is a project created in order to demonstrate the process of hypothesis testing

<br>

Ever think hypothesis testing is difficult? What is type I error? What is type II error?
And what is power?😕 Well, you are at the right place.😀

This project won't teach you the
theory behind hypothesis testing. However, it will demonstrate some easy graph to help you truly understand how the hypothesis testing works.

# Introduction
This application demonstrate the so-called "two tailed test". Two assupmtions are set to simplify the process

- The distribution is normally distributed
- The normal distribution has variance 1

The null hypothesis lies with the mean of the distribution, hence, the hypothesis can be written as

$$ H_0: \mu = \mu_0\\
H_a: \mu \neq \mu_0$$

# Interface Introduction
<p align = "center">
<img src = "picture/interface intro.jpg" width = "800"/>
</p>

To start, you have to enter three parameter
- Null Hypothesis: the mean for the null hypothesis
- True Parameter: the mean of true value, meaning that one will draw sample from this distribution(Note: In reality, this value
is unknown.)
- Type I Error: just type I error

# Demonstration

Suppose that one wants to test the null hypothesis of $\mu = 0$, and the distribution that one draws samples from has $\mu = 1.5$. Also, we set the type I error as $0.05$. The argument should be type as following:

<p align = "center">
<img src = "picture/demo 1.jpg" width = "800"/>
</p>

Then we can press <i>enter</i> to show the graph

<p align = "center"><img src = "picture/demo 2.jpg" width = "800"/></p>

Here, as we can see, the <span style = "color: #3DFCFF"><i>blue line</i></span> represents the normal curve of null hypothesis, and the <span style = "color: #FFC327"><i>orange line</i></span> represents the normal curve of the true parameter. Also, the app will automatically calculate the value of type II error and power as marked in the picture. <br>
Next, you can click on the checkbox above the visualize the area of type I error and type II error.

<p align = "center"><img src = "picture/gif 1.gif" width = "800"/></p>

The <span style = "color: #20ff1c"><i>green area</i></span> represents the type I error, the <span style = "color: #f25449"><i>red area</i></span> represents the type II error. From this process, you can easily understand how these abstract words are formed. By merely clicking on few button, your understanding toward the foundation of hypothesis testing will increase.
Not only type I error and type II error, you can also click on the checkbox of <i>power</i> to see the area of power

<p align = "center"><img src = "picture/gif 2.gif" width = "800"/></p>

The <span style = "color: #FFFD1B"><i>yellow area</i></span> represents the type I error

<hr>
That's all for this project, hope that this app can help you better understand the hypothesis testing. However, things will not end here. More functions like left-tailed test or right-tailed test are expected to published in the future ☺️
