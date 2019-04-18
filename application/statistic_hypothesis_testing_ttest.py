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

  """
  Statsmodels
  """
  (tstat, pvalue, df) = stests.ttest_ind(samples1, x2=samples2, value=0, alternative='two-sided')

  print(f"TScore: {tstat}")
  print(f"Pvalue: {pvalue}")
  print(f"Degrees of freedom: {df}")

  if(pvalue < 0.05):
    print('Rejected Null Hypothesis')
    return True
  else:
    print('Not Rejected Null Hypothesis')
    return False


if __name__ == '__main__':
  samples1 = [random.randint(800, 900) for _ in range(20)]
  samples2 = [random.randint(700, 900) for _ in range(20)]
  hypothesis_testing(samples1, samples2)

    