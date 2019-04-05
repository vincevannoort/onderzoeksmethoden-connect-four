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
  se = math.sqrt(s1/n1 + s2/n2)

  # Calculate z-score
  zscore = (mean1 - mean2) / se

  # Calculate p-value
  # Confidence interval = 95%
  pvalue = stats.norm.sf(zscore)

  print(f"ZScore: {zscore}")
  print(f"PValue: {pvalue}")

  """
  Statsmodels
  """
  print(stests.ztest(samples1, x2=samples2, value=0, alternative='larger'))
  print(stests.ztest(samples2, x2=samples1, value=0, alternative='larger'))

  (zscore, pvalue) = stests.ztest(samples1, x2=samples2, value=0, alternative='larger')

  if(pvalue < 0.05):
    print('Null hypothesis rejected')
  else:
    print('Null hypothesis not rejected')

  return pvalue


if __name__ == '__main__':
  samples1 = [random.randint(800, 900) for _ in range(100)]
  samples2 = [random.randint(800, 900) for _ in range(100)]
  hypothesis_testing(samples1, samples2)

    