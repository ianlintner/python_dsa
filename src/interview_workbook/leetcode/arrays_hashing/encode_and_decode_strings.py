"""
Encode and Decode Strings - LeetCode Problem (Premium)

Design an algorithm to encode a list of strings to a string. The encoded string
is then sent over the network and is decoded back to the original list of strings.

Machine 1 (sender) has the function:
string encode(vector<string> strs) {
  // ... your code
  return encoded_string;
}

Machine 2 (receiver) has the function:
vector<string> decode(string s) {
  // ... your code
  return strs;
}

So Machine 1 does: string encoded_string = encode(strs);
and Machine 2 does: vector<string> strs2 = decode(encoded_string);
strs2 in Machine 2 should be the same as strs in Machine 1.

Implement the encode and decode methods.

Note:
- The string may contain any possible characters out of 256 valid ASCII characters.
- Your algorithm should be generalized enough to work on any possible characters.
- Do not use class member/global/static variables to store states.
- Do not rely on any library method such as eval or serialize methods.
"""

from typing import List

from .._registry import register_problem
from .._runner import TestCase, create_demo_output
from .._types import Category, Difficulty


class Solution:
    def encode(self, strs: List[str]) -> str:
        """
        Encode list of strings using length prefix format.
        Format: "length#string" for each string

        Time Complexity: O(n) - where n is total characters in all strings
        Space Complexity: O(n) - for the encoded string

        Args:
            strs: List of strings to encode

        Returns:
            str: Encoded string
        """
        encoded = ""
        for s in strs:
            # Format: length + '#' + string
            encoded += str(len(s)) + "#" + s
        return encoded

    def decode(self, s: str) -> List[str]:
        """
        Decode string back to list of strings.

        Time Complexity: O(n) - single pass through encoded string
        Space Complexity: O(n) - for the result list

        Args:
            s: Encoded string

        Returns:
            List[str]: Decoded list of strings
        """
        result = []
        i = 0

        while i < len(s):
            # Find the delimiter '#'
            delimiter_pos = s.find("#", i)

            # Extract the length
            length = int(s[i:delimiter_pos])

            # Extract the string of specified length
            start = delimiter_pos + 1
            string = s[start : start + length]
            result.append(string)

            # Move to next encoded string
            i = start + length

        return result

    def encodeAlternative(self, strs: List[str]) -> str:
        """
        Alternative encoding using escape characters.

        Time Complexity: O(n)
        Space Complexity: O(n)
        """
        encoded = ""
        for s in strs:
            # Replace special chars with escape sequences
            escaped = s.replace("/", "//").replace(":", "/:")
            encoded += escaped + ":"
        return encoded

    def decodeAlternative(self, s: str) -> List[str]:
        """
        Alternative decoding using escape characters.

        Time Complexity: O(n)
        Space Complexity: O(n)
        """
        result = []
        i = 0
        start = 0

        while i < len(s):
            if s[i] == ":":
                # Found end of string
                string = s[start:i]
                # Unescape: replace "/:" with ":" and "//" with "/"
                string = string.replace("/:", ":").replace("//", "/")
                result.append(string)
                i += 1
                start = i
            elif s[i] == "/" and i + 1 < len(s) and s[i + 1] in ["/", ":"]:
                # Skip escape sequence
                i += 2
            else:
                i += 1

        return result


def demo():
    """Demonstrate Encode and Decode Strings solution with test cases."""
    solution = Solution()

    def test_encode_decode(strs):
        """Helper to test round trip encoding/decoding."""
        encoded = solution.encode(strs)
        decoded = solution.decode(encoded)
        return decoded == strs

    test_cases = [
        TestCase(input_args=(["hello", "world"],), expected=True, description="Basic string list"),
        TestCase(input_args=([""],), expected=True, description="Single empty string"),
        TestCase(input_args=([],), expected=True, description="Empty list"),
        TestCase(input_args=(["", "", ""],), expected=True, description="Multiple empty strings"),
        TestCase(
            input_args=(["a", "bb", "ccc"],), expected=True, description="Different length strings"
        ),
        TestCase(
            input_args=(["#", "##", "###"],),
            expected=True,
            description="Strings with delimiter characters",
        ),
        TestCase(
            input_args=(["123", "45#67", "8#9#0"],),
            expected=True,
            description="Strings with numbers and delimiters",
        ),
        TestCase(
            input_args=(["hello#world", "test:case", "escape//slash"],),
            expected=True,
            description="Strings with special characters",
        ),
        TestCase(input_args=(["ä", "中文", "🚀"],), expected=True, description="Unicode strings"),
    ]

    # Test the round-trip encoding and decoding
    results = []
    for i, test_case in enumerate(test_cases):
        try:
            import time

            start_time = time.perf_counter()

            strs = test_case.input_args[0]
            encoded = solution.encode(strs)
            decoded = solution.decode(encoded)
            actual = decoded == strs

            end_time = time.perf_counter()

            results.append(
                {
                    "test_case": i + 1,
                    "description": test_case.description,
                    "input": strs,
                    "encoded": encoded,
                    "decoded": decoded,
                    "expected": test_case.expected,
                    "actual": actual,
                    "passed": actual == test_case.expected,
                    "time_ms": (end_time - start_time) * 1000,
                }
            )
        except Exception as e:
            results.append(
                {
                    "test_case": i + 1,
                    "description": test_case.description,
                    "input": test_case.input_args[0],
                    "encoded": f"Error: {str(e)}",
                    "decoded": f"Error: {str(e)}",
                    "expected": test_case.expected,
                    "actual": False,
                    "passed": False,
                    "time_ms": 0,
                }
            )

    # Format results as test results string
    test_results_lines = ["=== Encode and Decode Strings ===", ""]
    passed_count = 0
    total_time = sum(r["time_ms"] for r in results)
    
    for result in results:
        status = "✓ PASS" if result["passed"] else "✗ FAIL"
        test_results_lines.append(f"Test Case {result['test_case']}: {status}")
        test_results_lines.append(f"  Description: {result['description']}")
        test_results_lines.append(f"  Input: {result['input']}")
        test_results_lines.append(f"  Expected: {result['expected']}")
        test_results_lines.append(f"  Got: {result['actual']}")
        test_results_lines.append(f"  Time: {result['time_ms']:.3f}ms")
        test_results_lines.append("")
        if result["passed"]:
            passed_count += 1
    
    test_results_lines.append(f"Results: {passed_count}/{len(results)} passed")
    test_results_lines.append(f"Total time: {total_time:.3f}ms")
    
    if passed_count == len(results):
        test_results_lines.append("🎉 All tests passed!")
    else:
        test_results_lines.append(f"❌ {len(results) - passed_count} test(s) failed")
    
    test_results_str = "\n".join(test_results_lines)
    
    approach_notes = """
Key Insights:
• Length prefix format handles any characters including delimiters
• Format: 'length#string' allows unambiguous parsing
• Alternative escape character approach is more complex
• Must handle empty strings and edge cases correctly

Common Pitfalls:
• Don't use characters that appear in input as delimiters
• Length prefix approach is safer than escape sequences
• Handle empty strings and empty lists correctly
• Consider Unicode and multi-byte character handling

Follow-up Questions:
• How would you optimize for repeated encoding/decoding?
• What if strings are very large and memory is limited?
• How would you handle compression in the encoding?
• What about thread safety for concurrent operations?
"""

    return create_demo_output(
        problem_title="Encode and Decode Strings",
        test_results=test_results_str,
        time_complexity="O(n) - where n is total characters in all strings",
        space_complexity="O(n) - for encoded string and result list",
        approach_notes=approach_notes,
    )


# Register this problem
register_problem(
    id=271,  # LeetCode Premium problem number
    slug="encode-and-decode-strings",
    title="Encode and Decode Strings",
    category=Category.ARRAYS_HASHING,
    difficulty=Difficulty.MEDIUM,
    tags=["array", "string", "design"],
    url="https://leetcode.com/problems/encode-and-decode-strings/",
    notes="Length prefix encoding for safe string serialization",
)
