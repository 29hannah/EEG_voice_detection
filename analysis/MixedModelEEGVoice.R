# LMER ANALYSIS EEG VOICE 
library(BayesFactor)
library(plotrix)
library(lme4)
library(lmerTest)
library(emmeans)
library(afex)
library(car)
library(sjPlot)
library(brms)
library(plotly)
library(performance)
library(ggeffects)  
require(gridExtra)

# read data
data <- read.csv("/Users/hannahsmacbook/EEG_voice/EEG_data.csv", header=T, na.strings = "NaN")

data$subj <- as.factor(data$subj)

# Scale the amplitude
data$ampz = scale(data$amp)
# Scale the behaviour
data$X.Voicez = scale(data$X.Voice)


#####################################################

# Check distribution of response variable
hist(data$X.Voicez)
# Check distribution of explanatory variable 
hist(data$ampz) #amplitude seems to be more or less normally distributed

# Clustered data?!
(split_plot <- ggplot(aes(ampz, X.Voicez), data = data) + 
    geom_point() + 
    facet_wrap(~ subj) + # create a facet for each mountain range
    xlab("ampz") + 
    ylab("X.Voicez"))


# MIXED EFFECTS MODEL 1
mixed.lmer <- lmer(X.Voicez ~ ampz+ condition + (1|subj), data=data)
summary(mixed.lmer)

# Check the assumptions 
plot(mixed.lmer)
qqnorm(resid(mixed.lmer))
qqline(resid(mixed.lmer)) 

# Plotting the model predictions
# Extract the prediction data frame
pred.mm <- ggpredict(mixed.lmer, terms = c("ampz"))  

# Plot the predictions-Overall
fig1<-(ggplot(pred.mm) + 
         geom_line(aes(x = x, y = predicted)) +      
         geom_ribbon(aes(x = x, ymin = predicted - std.error, ymax = predicted + std.error), 
                     fill = "lightgrey", alpha = 0.5) +  # error band
         geom_point(data = data,                      # adding the raw data (scaled values)
                    aes(x = ampz, y = X.Voicez, colour = subj)) + 
         labs(x = "ampz", y = "X.Voicez", 
              title = "") + 
         theme_minimal()
)
fig1

# Results table
tab_model(mixed.lmer)

# BASELINE MODEL
mixed.lmer2 <- lmer(X.Voicez ~  condition  + (1|subj), data=data)
summary(mixed.lmer2)
plot(mixed.lmer2)
qqnorm(resid(mixed.lmer2))
qqline(resid(mixed.lmer2)) # Residuals are not normally distributed!


# Comparison to reduced model: Drop fixed effect for reduced model 
anova(mixed.lmer, mixed.lmer2) 







