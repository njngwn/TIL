# Initial Approach and Pitfall for LeetCode's Word Break Problem

The [Word Break](https://leetcode.com/problems/word-break/) problem on LeetCode asks whether a given string `s` can be fully segmented into a sequence of one or more words from a provided dictionary (`wordDict`).

## Initial Approach

My first intuitive approach was to iterate through the words in the dictionary and, if a word was found within the string `s`, remove it. If the string `s` becomes empty after checking all the words, the function would return `true`.

```java
class Solution {
    public boolean wordBreak(String s, List<String> wordDict) {
        for (String word : wordDict) {
            if (s.contains(word)) {
                s = s.replaceAll(word, "");
            }

            // no more string left
            if (s.equals("")) {
                return true;
            }
        }

        return false;
    }
}

```

### Discovering the Flaw (Trial and Error)

This approach failed on a specific test case. The input that caused the failure was:

-   `s = "cars"`
-   `wordDict = ["car", "ca", "rs"]`

My code would iterate through the dictionary, find `"car"` first, and remove it from `s`. This would leave a remainder of `"s"`. Since the remaining string `"s"` cannot be formed by any other word in the dictionary, the function would ultimately return `false`.

However, the correct answer for this case is `true`, as `s` should be segmented using the words `"ca"` and `"rs"`.