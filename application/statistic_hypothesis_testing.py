from statsmodels.stats import weightstats as stests
from scipy import stats
import random
import math

if __name__ == '__main__':
    arrayj = [random.randint(700, 800) for _ in range(100)]
    arrayv = [random.randint(800, 900) for _ in range(100)]
    nj = len(arrayj)
    nv = len(arrayv)

    """
    Own version
    """
    # Calculate mean
    meanj = stats.hmean(arrayj)
    meanv = stats.hmean(arrayv)

    # Calculate sample variance
    sj = stats.tvar(arrayj)
    sv = stats.tvar(arrayv)

    # Calculate standard error
    se = math.sqrt(sj/nj + sv/nv)

    # Calculate z-score
    zscore = (meanj - meanv) / se

    # Calculate p-value
    # Confidence interval = 95%
    pvalue = stats.norm.sf(zscore)

    print(zscore)
    print(pvalue)

    """
    Statsmodels
    """
    # Confidence interval = 95%
    (ztest, pvalue) = stests.ztest(arrayj, x2=arrayv, value=0, alternative='larger')
    print(ztest, pvalue)

    if(pvalue < 0.05):
        print('Null hypothesis rejected')
    else:
        print('Null hypothesis not rejected')