## PaperNotes

**Detecting Duplicate Crash Reports Using Crash Traces and Hidden Markov Models**

``Duplicate``

> A bug report is considered a duplicate if it refers to either the same previously reported abnormal execution or a distinct behavior of an existing bug report

`stack trace`

F = f0, f1, ..., fn, f0 represents the last function that is executed before the crash.

**Approach Overview**

![Screen Shot 2018-12-08 at 10.32.48 PM](https://ws3.sinaimg.cn/large/006tNbRwgy1fy0y0h6djzj30vg0f3n2x.jpg)

1. Creating bug report groups

   * They divide the bug reports into groups where each group contains a master bug report and its duplicates.

   * They will use these groups in the case study to derive training and testing sets so as to assess the effectiveness of our approach.
   * Bug reports that do not have duplicates are excluded from the dataset.

2. Generate HMM

   A good video illustrates HMM

   https://www.youtube.com/watch?v=TPRoLreU9lA

   A good blog illustrates HMM

   https://www.cnblogs.com/skyme/p/4651331.html

3. Training the HMM

   The behavior of each bug report can be represented as a discrete sequence of function calls.

   A sequence of function calls (Fi) of a bug report group is mapped to an observation sequence (O).

   ![Screen Shot 2018-12-09 at 2.00.22 AM](https://ws1.sinaimg.cn/large/006tNbRwgy1fy0y1f3c09j31i40ikmzg.jpg)

   Practically, training a well-fit HMM using a discrete sequence of
   observation 𝒪-(𝒪0,𝒪1,...,𝒪𝑇−1), means maximizing the likelihood,
   i.e., maximizing the probability of 𝑃(𝒪| 𝜆) on the parameters space
   represented by 𝐴, 𝐵, and 𝜋. 

4. Classification

   When a new observation sequence comes, we compute L scores for each HMM model, the model with the highest score will be the chosen bug group.

   >We use the FB algorithm to compute the scores or
   >𝑃𝑙 (𝒪|𝛾𝑙 ). As we have 𝐿 trained HMM models (𝜆𝑙 ), we get 𝐿 scores
   >for a new observation sequence 𝒪. If the new observation sequence
   >𝒪 (i.e., the new bug report) is duplicate (let say the duplicate bug
   >report group is 𝑙′ ), the score of that trained HMM model ( 𝜆𝑙′ )
   >should be significantly higher. 
