# Amazon Business - Paid Search Measurement
*Converted from DOCX. Original: Richard's writing/Amazon Business - Paid Search Measurement.docx*


## Amazon Business - Paid Search Measurement
Link:
USA: https://issues.amazon.com/P77886853
UK: https://issues.amazon.com/issues/P78696791
DE: https://issues.amazon.com/P78696830 (cancelled)
This document presents the Randomized Control Trial (RCT) design recommendation for Amazon Business for Q2 2023 using Synthetic Regional Testing Methodology. Synthetic Regional Test (SyRT, pronounced "sert") is an experimental model for measuring Amazon marketing campaign’s impact on ordered product sales (OPS) and High Value Actions (HVAs). It uses a randomized control trial (RCT) framework — the scientific gold standard for deriving ground truth. It operates by dividing a marketplace into geographic regions, and randomly assigning a set of regions to receive advertising (the treated regions) and the remaining regions to suppress advertising (the holdout regions).

There are two objectives of this measurement:
To measure if Paid Search is driving incremental AB registration.
To test the hypothesis that brand and non-brand paid search keyword have different incrementally effect.
Campaign Background:

|  | A | B |
| --- | --- | --- |
| 1 | Quarter | Q2 2023 |
| 2 | Business Unit | Amazon Business |
| 3 | Country | USA: 4/4/2023 - 5/1/2023 |
| 4 |  | UK: 5/25/2023 - 6/28/2023 |
| 5 |  |  |
| 6 | Channel | Paid Search |
| 7 | Sub Channels | Google-Google.com, Microsoft-Bing |
| 8 | Campaign Name | Amazon Business paid search campaign |
| 9 | Spend | US: $3M   UK: $400K   DE: $400K |
| 10 | Dark period | USA: 3/28 - 4/3 |
| 11 |  | UK: 5/18 - 5/25 |
| 12 |  |  |
| 13 | HVAs of importance | ab_registration_1st |

Proposed Experimental Design with Treatment Allocation:
Before we proceed to the proposed RCT design, we make the following design assumptions:
This will be a multi arm design where we will test the incrementally of brand vs non – brand keyword.
This is an evergreen campaign; therefore, we will have a week of blackout period before the measurement
US, LA and NY will be removed from the measurement due to the uniqueness of data, however stakeholder can still advertise on the excluded regions.
Minimum Detectable Effect calculation will be used to determine optimal treatment/control allocation
MDE stands for minimum detectable effects. It is the minimum effect size that we are able to correctly detect in a SyRT experiment with certain power (e.g. 80%) at a certain significance criterion (e.g test size = 10%). It measures the sensitivity of an experiment, and a lower MDE means that we are more empowered to detect smaller effect sizes. Power and test size are two important parameters that are used in MDE calculations.

(Figure 1: MDE calculation for Germany)
By performing MDEs for 3 arm test it’s determined that for DE the optimal treatment allocation we need is 60% which gives us regional allocation of treated0 = 30%, treated1 = 30% and control = 40%. Similar calculation was performed for US and UK.

|  | A | B | C | D |
| --- | --- | --- | --- | --- |
| 1 | Country | Treated 0 = non-brand keywords | Treated 1 = brand keywords | Control = no advertisement |
| 2 | UK | 35% | 35% | 30% |
| 3 | US | 30% | 30% | 40% |

AB Registration Incremental Measurement results
T1 = only ‘brand’ keywords advertisement
T0 = only ‘non-brand’ keywords advertisement

|  | A | B | C | D | E | F | G | H | I |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 |  |  | p_lift | standard_error | low_90 | high_90 | p-value | base | N_lift |
| 2 | US | T1 | 2.8% | 2.6% | -1.5% | 7.0% | 0.284 | 23,197 | 638 |
| 3 |  | T0 | 16.4% | 1.8% | 13.5% | 19.4% | 0.000 | 30,320 | 4,986 |
| 4 | UK | T1 | -0.4% | 2.5% | -4.6% | 3.7% | 0.861 | 5964 | -26 |
| 5 |  | T0 | 2.8% | 2.8% | -2.0% | 7.5% | 0.335 | 5989 | 165 |

Key Findings:
In US ‘non-brand’ keyword (T0) drove positive statistically significant lift on ab_registration HVA of 16.4%.
In US ‘brand’ keyword (T1) didn’t drive statistically significant lift, however drove directionally positive lift.
Based on the findings above ‘non-brand’ keyword drove higher incremental effect compare to ‘brand’ keywords
In UK ‘non-brand’ keyword (T0) didn’t drive statistically significant lift, however drove directionally positive lift.
In UK ‘brand’ keyword (T1) didn’t drive neither statistically significant/directionally positive lift.
Based on the finding above even though non-brand’ keyword were able to drive directional lift, ‘brand’ keyword was unsuccessful at driving any lift.

Note:
US notes:
After the incrementality test, based on your team’s analysis, the P_lift value is 16.4%, means 16.4% of AB registrations were driven by Paid search Non Brand.
Before we launch the incrementality test, Paid search Non Brand counted around 18% to 20% of AB all channels registrations. We expect, if based on a 100% incrementality impact, 18% to 20% of AB registrations were driven by Paid search Non Brand.
To calculate the incrementality impact, we use the P_lift value divided by average Paid search Non Brand registration penetration. Then we get the incrementality impact is 82% to 92%.
AB Paid search Non Brand Incrementality calculation: 16.4%/20% = 82%; 16.4% /18% = 92%;
Note that since SyRT calculates it’s incrementality impact with the usage of 90% confidence interval, this means that it is 90% likely that the true lift is contained for the represented incrementally impact.
Additionally, there is a difference in how SyRT calculates the incrementality effect vs how Amazon Business calculates its average incrementality impact. This means that the average incrementality impact calculated by Amazon Business doesn’t account for marketing interaction effect of the customers. Therefore, two metrics can not be used for ‘apple-to-apple’ comparison/calculations.
