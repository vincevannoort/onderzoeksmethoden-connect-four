from statsmodels.stats import weightstats as stests
from scipy import stats
import random
import math

def hypothesis_testing(samples1, samples2):
  """
  Hypothesis testing
  H0: meanj == meanv
  Ha: meanj > meanv
  """
  n1 = len(samples1)
  n2 = len(samples2)

  """
  Own version
  """
  # Calculate mean
  mean1 = stats.hmean(samples1)
  mean2 = stats.hmean(samples2)

  # Calculate sample variance
  s1 = stats.tvar(samples1)
  s2 = stats.tvar(samples2)

  # Calculate standard error
  se = math.sqrt(sj/nj + sv/nv)

  # Calculate z-score
  zscore = (meanj - meanv) / se

  # Calculate p-value
  # Confidence interval = 95%
  pvalue = stats.norm.sf(abs(zscore))

  print(zscore)
  print(pvalue)

  """
  Statsmodels
  """
  # Confidence interval = 95%
  # Returns pvalue = 1.0 when zscore is negative
  # (ztest, pvalue) = stests.ztest(arrayj, x2=arrayv, value=0, alternative='larger')
  # print(ztest, pvalue)

  if(pvalue < 0.05):
    print('Null hypothesis rejected')
  else:
    print('Null hypothesis not rejected')


if __name__ == '__main__':
  samples1 = [random.randint(700, 800) for _ in range(100)]
  samples2 = [random.randint(800, 900) for _ in range(100)]
  hypothesis_testing(samples1, samples2)

    