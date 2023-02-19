# PyQt5 Hypothesis Testing Visualization
## This is a project created in order to demonstrate the process of hypothesis testing

<br>

Ever think hypothesis testing is difficult? What is type I error? What is type II error?
And what is power?😕 Well, you are at the right place.😀

This project won't teach you the
theory behind hypothesis testing. However, it will demonstrate some easy graph to help you truly understand how the hypothesis testing works.

# Introduction
This application demonstrates the so-called "two tailed test". Two assupmtions are set to simplify the process

- The distribution is normally distributed
- The normal distribution has variance 1

The null hypothesis is about testing the mean of the distribution, hence, the hypothesis can be written as

$$ 
\begin{align}
H_0: \mu = \mu_0 \\
H_a: \mu \neq \mu_0
\end{align}
$$

# Interface Introduction
<p align = "center">
<img src = "picture/interface intro.jpg" width = "800"/>
</p>

To start, you have to enter three parameter
- Null Hypothesis: The mean for the null hypothesis, which is the mean that going to be tested
- True Parameter: The mean of true value, meaning that one will draw sample from this distribution(Note: In reality, this value is unknown.)
- Type I Error: The level of significance. Greater type I error indicates larger probability to reject null hypothesis even if $H_0$ is true

# Demonstration

Suppose that one wants to test the null hypothesis of $\mu = 0$, 
and the distribution that one draws samples from has $\mu = 1.5$. Also, we set the type I error as $0.05$. So we could input the these arguments as following then press enter

<p align = "center">
<img src = "picture/demo 1.jpg" width = "800"/>
</p>


Here, as we can see, the <span style = "color: #3DFCFF"><i>blue line</i></span> represents the normal curve of null hypothesis, and the <span style = "color: #FFC327"><i>orange line</i></span> represents the normal curve of the true parameter. Also, the app will automatically calculate the value of type II error and power as shown in the picture. <br>

The <span style = "color: #20ff1c"><i>green area</i></span> represents the type I error, the <span style = "color: #f25449"><i>red area</i></span> represents the type II error. You could check and uncheck the check box to decide what areas you want to see

<p align = "center"><img src = "picture/gif 1.gif" width = "800"/></p>

In addition, you could also check and uncheck the check box of power to see the area which power represents

<p align = "center"><img src = "picture/demo 2.jpg" width = "800"/></p>

The <span style = "color: #FFFD1B"><i>yellow area</i></span> represents the power

<br>
To see a full explanation of each number in the application and its statistical meaning, you could refer to the text area on the left. The text area provides complete explanation of the meaning of the parameters which help you to better understand hypothesis testing.

<hr>

That's all for this project, hope that this app can help you better understand the hypothesis testing. 

If you want to try on the application youself, please click <a href = "https://drive.google.com/file/d/1PxKwqLB1ZlR1uVHM4OuEoHsF4MkH4re7/view?usp=share_link">  HERE </a> to download the EXE file that could easily run on your computer.

