def addition(numbers: list) -> float:
    return sum(numbers)
def show_code():
    code = '''
y1 <- c(18.2, 20.1, 17.6, 16.8, 18.8, 19.7, 19.1)
y2 <- c(17.4, 18.7, 19.1, 16.4, 15.9, 18.4, 17.7)
y3 <- c(15.2, 18.8, 17.7, 16.5, 15.9, 17.1, 16.7)
y <- c(y1, y2, y3)
group <- factor(rep(1:3, each = length(y1)))
tapply(y, group, stem)
tmpfn <- function(x) {
  list(sum = sum(x), mean = mean(x), var = var(x), n = length(x))
}
tapply(y, group, tmpfn)
data <- data.frame(y = y, group = group)
fit <- lm(y ~ group, data)
anova_fit <- anova(fit)
df <- anova_fit[,"Df"]
names(df) <- c("trt", "err")
df
alpha <- c(0.05, 0.01)
qf(alpha, df["trt"], df["err"], lower.tail = FALSE)
anova_fit["Residuals", "Sum Sq"]
anova_fit["Residuals", "Sum Sq"] / qchisq(c(0.025, 0.975), df["err"], lower.tail = FALSE)

    '''
    print(code)